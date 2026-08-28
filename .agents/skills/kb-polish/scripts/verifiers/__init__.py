#!/usr/bin/env python3
"""
verifiers/__init__.py — verify-source plugin registry.

To add a format: create a plugin file under verifiers/ extending BaseVerifier and
implementing extract(), then import it here and add it to REGISTRY — the entry script
needs no changes.

Plugins align strictly with the formats AnyDoc supports (official site):
Excel(xlsx/xls/xlsm/xlsb/ods), Word(docx/doc/docm/odt/rtf),
PowerPoint(pptx/ppt/pptm/odp), EPUB, CSV, PDF.
html/md/txt are not supported (AnyDoc does not support them, no verification needed)
and neither are legacy .doc/.ppt (no lightweight library).

Dependencies:
- pdf:  pymupdf
- rtf:  striprtf
- others: stdlib
"""

from __future__ import annotations

from .base import BaseVerifier, ExtractResult  # noqa: F401  (re-export)

from .pdf import PdfVerifier
from .docx import DocxVerifier
from .pptx import PptxVerifier
from .xlsx import XlsxVerifier
from .odt import OdtVerifier
from .epub import EpubVerifier
from .rtf import RtfVerifier
from .csv import CsvVerifier

# plugin registry (extensions are mutually exclusive; order does not matter)
REGISTRY: list[BaseVerifier] = [
    PdfVerifier(),
    DocxVerifier(),
    PptxVerifier(),
    XlsxVerifier(),
    OdtVerifier(),
    EpubVerifier(),
    RtfVerifier(),
    CsvVerifier(),
]

# extension -> plugin index
EXT_MAP: dict[str, BaseVerifier] = {}
for _v in REGISTRY:
    for _ext in _v.extensions:
        EXT_MAP[_ext] = _v


def find_verifier(path) -> BaseVerifier | None:
    """Find a plugin by extension; return None if not found."""
    ext = path.suffix.lower() if hasattr(path, "suffix") else ""
    if not ext.startswith("."):
        ext = "." + ext
    return EXT_MAP.get(ext)


def supported_extensions() -> list[str]:
    return sorted(EXT_MAP.keys())
