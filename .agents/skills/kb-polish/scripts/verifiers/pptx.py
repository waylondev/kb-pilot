#!/usr/bin/env python3
"""
verifiers/pptx.py — PowerPoint (.pptx/.pptm/.ppsx/.ppsm) verify-source plugin.

OOXML = zip + XML. Read ppt/slides/slideN.xml and restore page by page:
per slide walk text frames (a:p -> a:r -> a:t), tables (a:tbl -> a:tr -> a:tc);
images (p:pic -> a:blip) are kept in place as `[image: <filename>]` placeholders.
"""

from __future__ import annotations

import re
from pathlib import Path

from .base import ZipXmlVerifier, ExtractResult, PKG_REL

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
REL = PKG_REL  # namespace of the Relationship element in .rels
REL_ATTR = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"  # r:embed attribute
_IMAGE_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff", ".emf", ".wmf")


def _tag(ns: str, t: str) -> str:
    return f"{{{ns}}}{t}"


class PptxVerifier(ZipXmlVerifier):
    name = "pptx"
    extensions = [".pptx", ".pptm", ".ppsx", ".ppsm"]

    def extract(self, path: Path) -> ExtractResult:
        slide_targets = self._slide_targets(path)
        rel_members = [f"ppt/slides/_rels/{t.rsplit('/', 1)[-1]}.rels" for t in slide_targets]
        files = self._read_zip(path, slide_targets + rel_members)

        pages, all_tables = [], []
        for idx, target in enumerate(slide_targets, 1):
            data = files.get(target)
            if data is None:
                continue
            root = self._xml(data)
            rid2name = self._slide_image_map(files, target)
            slide_texts, tables = [], []
            if root is not None:
                # text frames: under p:sp/p:txBody are a:p (body paragraphs)
                for sp in root.iter(_tag(P, "sp")):
                    txbody = sp.find(f".//{_tag(P, 'txBody')}")
                    if txbody is None:
                        continue
                    for child in txbody:
                        if child.tag == _tag(A, "p"):
                            t = self._clean(self._text(child, _tag(A, "t")))
                            if t:
                                slide_texts.append(t)
                # tables: a:tbl lives inside p:graphicFrame (not inside p:sp);
                # walk the whole slide root or table content will be missed
                for tbl in root.iter(_tag(A, "tbl")):
                    tables.append(self._parse_table(tbl))
                # images: p:pic -> a:blip -> r:embed, kept in place via placeholder
                for pic in root.iter(_tag(P, "pic")):
                    for blip in pic.iter(_tag(A, "blip")):
                        rid = blip.get(_tag(REL_ATTR, "embed")) or blip.get(_tag(REL_ATTR, "link"))
                        if rid and rid in rid2name:
                            slide_texts.append(f"[image: {rid2name[rid]}]")

            page_text = "\n".join(slide_texts)
            for _, rows in tables:
                for row in rows:
                    page_text += "\n" + " | ".join(row)
            pages.append({"index": idx, "text": page_text})
            for _, rows in tables:
                all_tables.append({"name": f"slide{idx}", "rows": rows})

        full_text = "\n\n".join(p["text"] for p in pages)
        return ExtractResult(
            format="pptx", verifier=self.name, text=full_text,
            pages=pages, tables=all_tables,
        )

    def _slide_image_map(self, files: dict, target: str) -> dict[str, str]:
        """rId -> image filename (read slideN.xml.rels relationships pointing to media)."""
        rid2name = {}
        relname = f"ppt/slides/_rels/{target.rsplit('/', 1)[-1]}.rels"
        rels = files.get(relname)
        if not rels:
            return rid2name
        relroot = self._xml(rels)
        if relroot is None:
            return rid2name
        for rel in relroot.iter(_tag(REL, "Relationship")):
            rid = rel.get("Id")
            tgt = (rel.get("Target") or "").replace("\\", "/")
            name = tgt.split("/")[-1]
            if rid and name.lower().endswith(_IMAGE_EXT):
                rid2name[rid] = name
        return rid2name

    def _slide_targets(self, path: Path) -> list[str]:
        """Slide parts in presentation order, as zip-internal paths."""
        rels_name = "ppt/_rels/presentation.xml.rels"
        rels = self._read_zip(path, [rels_name])
        targets = []
        if rels_name in rels:
            rel_root = self._xml(rels[rels_name])
            if rel_root is not None:
                for rel in rel_root.iter(_tag(REL, "Relationship")):
                    part = self._resolve_part(rels_name, rel.get("Target", ""))
                    if re.match(r"^ppt/slides/slide\d+\.xml$", part):
                        targets.append(part)
        if targets:
            targets.sort(key=lambda p: int(re.search(r"\d+", p.rsplit("/", 1)[-1]).group()))
            return targets
        # Fallback: enumerate the zip, ordered numerically so slide10 does not
        # sort before slide2.
        z = self._open_zip(path)
        if z is None:
            return []
        with z:
            parts = [n for n in z.namelist() if re.match(r"^ppt/slides/slide\d+\.xml$", n)]
        parts.sort(key=lambda p: int(re.search(r"\d+", p.rsplit("/", 1)[-1]).group()))
        return parts

    def _parse_table(self, tbl) -> tuple[str, list[list[str]]]:
        rows = []
        for tr in tbl.iter(_tag(A, "tr")):
            row = []
            for tc in tr.iter(_tag(A, "tc")):
                cell = []
                for p in tc.iter(_tag(A, "p")):
                    t = self._clean(self._text(p, _tag(A, "t")))
                    if t:
                        cell.append(t)
                row.append(" ".join(cell))
            rows.append(row)
        return "table", rows
