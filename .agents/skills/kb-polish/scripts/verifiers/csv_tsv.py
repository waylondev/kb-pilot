#!/usr/bin/env python3
"""
verifiers/csv_tsv.py — CSV/TSV verify-source plugin.

Read directly with the stdlib csv module — it already has structure, no third-party
dependency. Each file is restored as one table.
"""

from __future__ import annotations

import csv
from pathlib import Path

from .base import BaseVerifier, ExtractResult


class CsvVerifier(BaseVerifier):
    name = "csv"
    extensions = [".csv", ".tsv"]

    def extract(self, path: Path) -> ExtractResult:
        delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
        with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
            reader = csv.reader(f, delimiter=delimiter)
            rows = [row for row in reader if any(c.strip() for c in row)]

        text = "\n".join(" | ".join(cell for cell in r) for r in rows)
        return ExtractResult(
            format="csv",
            verifier=self.name,
            text=text,
            pages=[{"index": 1, "text": text}],
            tables=[{"name": path.stem, "rows": rows}],
        )
