#!/usr/bin/env python3
"""
verifiers/docx.py — Word (.docx/.docm) verify-source plugin.

OOXML = zip + XML; unzip with the stdlib and read word/document.xml.
Restore in document order: paragraphs (w:p) and tables (w:tbl) alternate;
inline images in paragraphs (w:drawing/a:blip or VML w:pict/v:imagedata) are emitted as
`[image: <filename>]` placeholders in the text flow, preserving their position in the
body, for the LLM to turn into `![](./images/<filename>)` references during kb-polish Step 4.
"""

from __future__ import annotations

from pathlib import Path

from .base import ZipXmlVerifier, ExtractResult, PKG_REL

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
V = "urn:schemas-microsoft-com:vml"

_IMAGE_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff", ".emf", ".wmf")


def _tag(t: str) -> str:
    return f"{{{W}}}{t}"


def _tag_ns(ns: str, t: str) -> str:
    return f"{{{ns}}}{t}"


class DocxVerifier(ZipXmlVerifier):
    name = "docx"
    extensions = [".docx", ".docm"]

    def extract(self, path: Path) -> ExtractResult:
        files = self._read_zip(path, ["word/document.xml", "word/_rels/document.xml.rels"])
        if "word/document.xml" not in files:
            return ExtractResult(
                format="docx", verifier=self.name, text="", pages=[], tables=[],
                warnings=["not a valid OOXML Word file (missing word/document.xml)"],
            )
        root = self._xml(files["word/document.xml"])
        rid2name = self._image_map(files)

        body = root.find(_tag("body")) if root is not None else None
        texts, tables = [], []
        if body is not None:
            for child in body:
                tag = child.tag
                if tag == _tag("p"):
                    # inline images in paragraphs -> placeholder (keep body position)
                    for img in self._para_images(child, rid2name):
                        texts.append(f"[image: {img}]")
                    t = self._clean(self._text(child, _tag("t")))
                    if t:
                        texts.append(t)
                elif tag == _tag("tbl"):
                    name, rows = self._parse_table(child)
                    tables.append({"name": name, "rows": rows})
                    # insert table rows into the text flow in document order
                    for row in rows:
                        texts.append(" | ".join(row))
        else:
            texts.append("XML parse failed")

        full_text = "\n".join(texts)

        return ExtractResult(
            format="docx",
            verifier=self.name,
            text=full_text,
            pages=[{"index": 1, "text": full_text}],
            tables=tables,
        )

    def _image_map(self, files: dict) -> dict[str, str]:
        """rId -> image filename map (read relationships in document.xml.rels that point to media)."""
        rid2name = {}
        rels = files.get("word/_rels/document.xml.rels")
        if not rels:
            return rid2name
        relroot = self._xml(rels)
        if relroot is None:
            return rid2name
        for rel in relroot.iter(_tag_ns(PKG_REL, "Relationship")):
            rid = rel.get("Id")
            tgt = (rel.get("Target") or "").replace("\\", "/")
            name = tgt.split("/")[-1]
            if rid and name and name.lower().endswith(_IMAGE_EXT):
                rid2name[rid] = name
        return rid2name

    def _para_images(self, p, rid2name: dict) -> list[str]:
        """Image filenames inline in paragraphs (DrawingML a:blip + VML v:imagedata)."""
        names = []
        for blip in p.iter(_tag_ns(A, "blip")):
            rid = blip.get(_tag_ns(REL, "embed")) or blip.get(_tag_ns(REL, "link"))
            if rid and rid in rid2name:
                names.append(rid2name[rid])
        for idata in p.iter(_tag_ns(V, "imagedata")):
            rid = idata.get(_tag_ns(REL, "id"))
            if rid and rid in rid2name:
                names.append(rid2name[rid])
        return names

    def _parse_table(self, tbl) -> tuple[str, list[list[str]]]:
        rows = []
        for tr in tbl.iter(_tag("tr")):
            row = []
            for tc in tr.iter(_tag("tc")):
                cell = []
                for p in tc.iter(_tag("p")):
                    t = self._clean(self._text(p, _tag("t")))
                    if t:
                        cell.append(t)
                row.append(" ".join(cell))
            rows.append(row)
        return "table", rows
