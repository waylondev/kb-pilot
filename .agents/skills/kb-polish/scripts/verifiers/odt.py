#!/usr/bin/env python3
"""
verifiers/odt.py — OpenDocument (.odt/.ods/.odp) verify-source plugin.

ODF = zip + XML; read content.xml.
- Paragraphs: text:p
- Tables: table:table -> table:table-row -> table:table-cell -> text:p
All three office formats share the same content.xml structure; one plugin covers them.
"""

from __future__ import annotations

from pathlib import Path

from .base import ZipXmlVerifier, ExtractResult

TEXT = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
TABLE = "urn:oasis:names:tc:opendocument:xmlns:table:1.0"
OFFICE = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
DRAW = "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"


def _tag(ns: str, t: str) -> str:
    return f"{{{ns}}}{t}"


class OdtVerifier(ZipXmlVerifier):
    name = "odt"
    extensions = [".odt", ".ods", ".odp"]

    def extract(self, path: Path) -> ExtractResult:
        files = self._read_zip(path, ["content.xml"])
        if "content.xml" not in files:
            return ExtractResult(
                format="odt", verifier=self.name, text="", pages=[], tables=[],
                warnings=["not a valid ODF file (missing content.xml)"],
            )
        root = self._xml(files["content.xml"])
        if root is None:
            return ExtractResult(
                format="odt", verifier=self.name, text="", pages=[], tables=[],
                warnings=["content.xml parse failed"],
            )

        body = root.find(f".//{_tag(OFFICE, 'body')}")
        texts, tables = [], []
        if body is not None:
            # pick the container by document type: odt->office:text / ods->office:spreadsheet / odp->office:presentation
            container = (body.find(_tag(OFFICE, "text"))
                         or body.find(_tag(OFFICE, "spreadsheet"))
                         or body.find(_tag(OFFICE, "presentation"))
                         or body)
            for child in container:
                if child.tag == _tag(TEXT, "p"):
                    t = self._clean("".join(child.itertext()))
                    if t:
                        texts.append(t)
                elif child.tag == _tag(TEXT, "h"):
                    # ODF heading element text:h (with outline-level)
                    level = child.get(f"{{{TEXT}}}outline-level", "1")
                    try:
                        level = int(level)
                    except ValueError:
                        level = 1
                    t = self._clean("".join(child.itertext()))
                    if t:
                        texts.append("#" * level + " " + t)
                elif child.tag == _tag(TABLE, "table"):
                    tables.append(self._parse_table(child))
                elif child.tag == _tag(TEXT, "list"):
                    # ODF list text:list -> text:list-item (note: AnyDoc drops ODF lists, so the verify source must cover them)
                    for li in child.iter(_tag(TEXT, "list-item")):
                        t = self._clean("".join(li.itertext()))
                        if t:
                            texts.append("- " + t)
                elif child.tag in (_tag(DRAW, "page"), _tag(DRAW, "frame"), _tag(DRAW, "text-box")):
                    # odp: text lives in draw:text-box -> text:p / text:h
                    for p in child.iter(_tag(TEXT, "p")):
                        t = self._clean("".join(p.itertext()))
                        if t:
                            texts.append(t)
                    for h in child.iter(_tag(TEXT, "h")):
                        t = self._clean("".join(h.itertext()))
                        if t:
                            texts.append(t)

        full_text = "\n".join(texts)
        for _, rows in tables:
            for row in rows:
                full_text += "\n" + " | ".join(row)

        return ExtractResult(
            format="odt", verifier=self.name, text=full_text,
            pages=[{"index": 1, "text": full_text}],
            tables=[{"name": "table", "rows": rows} for _, rows in tables],
        )

    def _parse_table(self, tbl) -> tuple[str, list[list[str]]]:
        rows = []
        for tr in tbl.iter(_tag(TABLE, "table-row")):
            row = []
            for tc in tr.iter(_tag(TABLE, "table-cell")):
                cell = []
                for p in tc.iter(_tag(TEXT, "p")):
                    t = self._clean("".join(p.itertext()))
                    if t:
                        cell.append(t)
                row.append(" ".join(cell))
            if any(row):
                rows.append(row)
        return "table", rows
