#!/usr/bin/env python3
"""
verifiers/rtf.py — RTF (.rtf) verify-source plugin.

RTF is a text markup language with control words; use striprtf to strip control
words and get plain text.

Dependency: pip install striprtf
"""

from __future__ import annotations

from pathlib import Path

from .base import BaseVerifier, ExtractResult


class RtfVerifier(BaseVerifier):
    name = "rtf"
    extensions = [".rtf"]

    def extract(self, path: Path) -> ExtractResult:
        from striprtf.striprtf import rtf_to_text  # lazy import

        raw = path.read_text(encoding="utf-8", errors="replace")
        text = rtf_to_text(raw)
        return ExtractResult(
            format="rtf",
            verifier=self.name,
            text=text,
            pages=[{"index": 1, "text": text}],
            tables=[],
        )
