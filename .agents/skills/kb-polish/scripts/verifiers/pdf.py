#!/usr/bin/env python3
"""
verifiers/pdf.py — PDF verify-source plugin.

Extract the text layer with PyMuPDF (MuPDF engine). Independent of AnyDoc's
implementation; outputs the raw text as the ground truth for checking AnyDoc's
conversion. Scans (no text layer) extract to empty — kb-polish does not process
images, the caller tells the user to provide a text-layer version.

Dependency: pip install pymupdf
"""

from __future__ import annotations

from pathlib import Path

from .base import BaseVerifier, ExtractResult


class PdfVerifier(BaseVerifier):
    name = "pdf"
    extensions = [".pdf"]

    def extract(self, path: Path) -> ExtractResult:
        import pymupdf  # lazy import so the entry gives a clear error when the dependency is missing

        warnings = []
        doc = pymupdf.open(str(path))
        pages = []
        page_texts = []
        for i, page in enumerate(doc, 1):
            text = page.get_text()
            pages.append({"index": i, "text": text})
            page_texts.append(text)
        doc.close()

        full_text = "\n\n".join(page_texts)
        if not full_text.strip():
            warnings.append("empty text layer: scanned/pure-image PDF; kb-polish does not process images, please provide a text-layer version")

        return ExtractResult(
            format="pdf",
            verifier=self.name,
            text=full_text,
            pages=pages,
            tables=[],  # PDF has no structural tables; table reconstruction needs pdfplumber/Camelot or AnyDoc
            warnings=warnings,
        )
