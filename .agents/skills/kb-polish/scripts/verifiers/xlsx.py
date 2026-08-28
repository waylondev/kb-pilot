#!/usr/bin/env python3
"""
verifiers/xlsx.py — Excel (.xlsx/.xlsm) verify-source plugin.

OOXML = zip + XML. Read xl/sharedStrings.xml (shared strings) +
xl/worksheets/sheetN.xml (cells; t="s" references the shared-string index).
Each worksheet is restored as one table. .xlsb (binary) is out of scope.
"""

from __future__ import annotations

import re
from pathlib import Path

from .base import ZipXmlVerifier, ExtractResult, PKG_REL

M = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = PKG_REL  # namespace of the Relationship element in .rels


def _tag(ns: str, t: str) -> str:
    return f"{{{ns}}}{t}"


class XlsxVerifier(ZipXmlVerifier):
    name = "xlsx"
    extensions = [".xlsx", ".xlsm"]

    def extract(self, path: Path) -> ExtractResult:
        files = self._read_zip(path, ["xl/sharedStrings.xml", "xl/workbook.xml",
                                      "xl/_rels/workbook.xml.rels"])
        # shared strings table
        shared = []
        if "xl/sharedStrings.xml" in files:
            root = self._xml(files["xl/sharedStrings.xml"])
            if root is not None:
                for si in root.iter(_tag(M, "si")):
                    shared.append("".join(t.text or "" for t in si.iter(_tag(M, "t"))))

        # sheet file order (from workbook relationships)
        sheet_targets = self._sheet_targets(path, files)
        tables, all_texts = [], []
        for idx, target in enumerate(sheet_targets, 1):
            data = files.get(f"xl/{target}")
            if data is None:
                data = self._read_zip(path, [f"xl/{target}"]).get(f"xl/{target}")
            if data is None:
                continue
            root = self._xml(data)
            rows = []
            if root is not None:
                for row in root.iter(_tag(M, "row")):
                    cells = []
                    for c in row.iter(_tag(M, "c")):
                        cells.append(self._cell_value(c, shared))
                    rows.append(cells)
            tables.append({"name": f"sheet{idx}", "rows": rows})
            text = "\n".join(" | ".join(cell for cell in r) for r in rows if any(r))
            all_texts.append(f"[sheet{idx}]\n{text}")

        full_text = "\n\n".join(all_texts)
        return ExtractResult(
            format="xlsx", verifier=self.name, text=full_text,
            pages=[{"index": i + 1, "text": t} for i, t in enumerate(all_texts)],
            tables=tables,
        )

    def _cell_value(self, c, shared: list[str]) -> str:
        t = c.get("t", "")
        # shared-string reference
        if t == "s":
            v = c.find(_tag(M, "v"))
            if v is not None and v.text:
                try:
                    return shared[int(v.text)]
                except (IndexError, ValueError):
                    return v.text
            return ""
        # inline string
        if t == "inlineStr":
            return "".join(x.text or "" for x in c.iter(_tag(M, "t")))
        # number/formula result
        v = c.find(_tag(M, "v"))
        return v.text if v is not None and v.text else ""

    def _sheet_targets(self, path: Path, files: dict) -> list[str]:
        targets = []
        if "xl/_rels/workbook.xml.rels" in files:
            rel_root = self._xml(files["xl/_rels/workbook.xml.rels"])
            if rel_root is not None:
                for rel in rel_root.iter(_tag(REL, "Relationship")):
                    t = rel.get("Target", "")
                    if re.match(r"^worksheets/sheet\d+\.xml$", t):
                        targets.append(t)
        if targets:
            targets.sort(key=lambda t: int(re.search(r"\d+", t).group()))
            return targets
        with __import__("zipfile").ZipFile(path) as z:
            cand = (n.replace("xl/", "", 1) for n in z.namelist())
            return sorted(c for c in cand if re.match(r"^worksheets/sheet\d+\.xml$", c))
