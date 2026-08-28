#!/usr/bin/env python3
"""
verifiers/__init__.py — verify-source plugin registry.

To add a format: create a plugin file under verifiers/ extending BaseVerifier and
implementing extract(), then import it here and add it to REGISTRY — the entry script
needs no changes.

The registry covers every format with a lightweight text layer (stdlib, or a
single small dependency — pymupdf for PDF, striprtf for RTF):
PDF (.pdf), Word (.docx/.docm), Excel (.xlsx/.xlsm),
PowerPoint (.pptx/.pptm/.ppsx/.ppsm), OpenDocument (.odt/.ods/.odp),
RTF (.rtf), EPUB (.epub), CSV (.csv).
Not covered: html/md/txt (AnyDoc does not support them, no verification needed)
and the legacy binary formats .doc/.ppt/.xls/.xlsb, which have no lightweight
library — those extensions stay out of the whitelist.

Dependencies:
Each plugin declares its own third-party requirement via the `dependency`
attribute (see base.py), so `extract_verify.py --list` stays accurate when a
format is added. Currently pdf -> pymupdf, rtf -> striprtf, other plugins run
on the standard library alone.
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
