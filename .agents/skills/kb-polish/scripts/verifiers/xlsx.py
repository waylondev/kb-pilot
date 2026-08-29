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

_CELL_REF = re.compile(r"^([A-Z]+)\d+$")


def _tag(ns: str, t: str) -> str:
    return f"{{{ns}}}{t}"


def _col_index(ref: str) -> int | None:
    """0-based column index from an Excel cell reference like `C3`, or None.

    Excel omits the `<c>` elements of empty cells, so a row's cells appear in
    document order only for the columns that have values — appending them blindly
    shifts every later column one slot left (a `0%` lands under the wrong header;
    field-tested). The `r` attribute is the authoritative column
    position; place cells by it and fill the gaps with empty strings.
    """
    m = _CELL_REF.match(ref or "")
    if not m:
        return None
    idx = 0
    for ch in m.group(1):
        idx = idx * 26 + (ord(ch) - ord("A") + 1)
    return idx - 1


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

        # sheet file order (from workbook relationships), read in one pass
        sheet_targets = self._sheet_targets(path, files)
        if sheet_targets:
            files.update(self._read_zip(path, sheet_targets))

        tables, all_texts = [], []
        for idx, target in enumerate(sheet_targets, 1):
            data = files.get(target)
            if data is None:
                continue
            root = self._xml(data)
            rows = []
            if root is not None:
                for row in root.iter(_tag(M, "row")):
                    rows.append(self._row_cells(row, shared))
                # Align every row to the widest one in the sheet: a stray narrow
                # row renders as a ragged table, which validate_structure reports
                # as inconsistent column counts and kb-chat misreads.
                width = max((len(r) for r in rows), default=0)
                rows = [r + [""] * (width - len(r)) for r in rows]
            tables.append({"name": f"sheet{idx}", "rows": rows})
            text = "\n".join(" | ".join(cell for cell in r) for r in rows if any(r))
            all_texts.append(f"[sheet{idx}]\n{text}")

        full_text = "\n\n".join(all_texts)
        return ExtractResult(
            format="xlsx", verifier=self.name, text=full_text,
            pages=[{"index": i + 1, "text": t} for i, t in enumerate(all_texts)],
            tables=tables,
        )

    def _row_cells(self, row, shared: list[str]) -> list[str]:
        """One row as a list of cell texts, positioned by the `r` column reference.

        Cells with a resolvable `r` are placed at their true column, gaps filled
        with "". A row with no usable references falls back to document order —
        the value list, not the column alignment, is then the best available fact.
        """
        placed: list[tuple[int, str]] = []
        for c in row.iter(_tag(M, "c")):
            col = _col_index(c.get("r", ""))
            placed.append((col, self._cell_value(c, shared)))
        if any(col is not None for col, _ in placed):
            width = max(col for col, _ in placed if col is not None) + 1
            out = [""] * width
            for col, val in placed:
                if col is not None:
                    out[col] = val
            return out
        return [val for _, val in placed]

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
        """Worksheet parts in workbook order, as zip-internal paths."""
        rels_name = "xl/_rels/workbook.xml.rels"
        targets = []
        if rels_name in files:
            rel_root = self._xml(files[rels_name])
            if rel_root is not None:
                for rel in rel_root.iter(_tag(REL, "Relationship")):
                    part = self._resolve_part(rels_name, rel.get("Target", ""))
                    if re.match(r"^xl/worksheets/sheet\d+\.xml$", part):
                        targets.append(part)
        if targets:
            targets.sort(key=lambda p: int(re.search(r"\d+", p.rsplit("/", 1)[-1]).group()))
            return targets
        # Fallback: enumerate the zip. Ordered by the numeric part, so sheet10
        # does not sort before sheet2 the way a plain string sort would.
        z = self._open_zip(path)
        if z is None:
            return []
        with z:
            parts = [n for n in z.namelist() if re.match(r"^xl/worksheets/sheet\d+\.xml$", n)]
        parts.sort(key=lambda p: int(re.search(r"\d+", p.rsplit("/", 1)[-1]).group()))
        return parts
