#!/usr/bin/env python3
"""
verifiers/base.py — base class for verify-source plugins.

One plugin file per format, extending BaseVerifier and implementing extract() to return
a unified ExtractResult. Zip-based formats (docx/pptx/xlsx/odt/epub) share the
ZipXmlVerifier unpacking helpers.

Design principle (per kb-pilot "scripts own the skeleton, the LLM owns the content"):
- Plugins only do deterministic extraction: pull out the document source (text + table
  structure) as-is
- No semantic judgment, no structure normalization — that is the LLM's job in kb-polish
  Steps 3/4
- The output is the "ground-truth source" for the LLM to cross-check against AnyDoc's raw.md
"""

from __future__ import annotations

import re
import zipfile
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

# Namespace of the Relationship element in .rels files (package).
# Note: not the officeDocument/2006/relationships in the Type attribute — that is the
# URI of the referenced target, not the element namespace to search for Relationship.
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"


@dataclass
class ExtractResult:
    """Unified extraction result; all plugins return this structure."""

    format: str            # format family, e.g. pdf / docx / xlsx
    verifier: str          # plugin name
    text: str              # full text (blank line between pages/slides/sheets)
    pages: list = field(default_factory=list)   # [{"index": n, "text": "..."}] per-page text
    tables: list = field(default_factory=list)  # [{"name": "...", "rows": [["a","b"], ...]}]
    images: list = field(default_factory=list)  # [{"name": "...", "data": bytes, "media_type": "..."}] embedded images
    warnings: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "format": self.format,
            "verifier": self.verifier,
            "text": self.text,
            "pages": self.pages,
            "tables": self.tables,
            "images": [{"name": i["name"], "media_type": i.get("media_type", "")} for i in self.images],
            "warnings": self.warnings,
            "stats": {
                "chars": len(self.text),
                "lines": len(self.text.splitlines()),
                "pages": len(self.pages),
                "tables": len(self.tables),
            },
        }


class BaseVerifier(ABC):
    """Plugin interface: declare supported extensions, implement extract()."""

    name: str = ""
    extensions: list[str] = []

    @abstractmethod
    def extract(self, path: Path) -> ExtractResult:
        """Extract the source text from a file, returning a unified ExtractResult."""

    def check(self, path: Path) -> bool:
        return path.suffix.lower() in self.extensions


class ZipXmlVerifier(BaseVerifier):
    """Shared helpers for zip + XML formats (docx/pptx/xlsx/odt/epub are all zip containers)."""

    def _open_zip(self, path: Path) -> zipfile.ZipFile | None:
        """Open a zip container, or None on a corrupt/truncated file (never raises).

        A corrupt file must yield a graceful warning downstream, not a crash.
        """
        try:
            return zipfile.ZipFile(path)
        except (zipfile.BadZipFile, OSError):
            return None

    def _read_zip(self, path: Path, members: list[str]) -> dict[str, bytes]:
        """Unzip, returning {internal path: bytes} (empty dict on corrupt files)."""
        out = {}
        z = self._open_zip(path)
        if z is None:
            return out
        with z:
            names = set(z.namelist())
            for m in members:
                if m in names:
                    out[m] = z.read(m)
        return out

    def _xml(self, data: bytes) -> ET.Element | None:
        try:
            return ET.fromstring(data)
        except ET.ParseError as e:
            return None

    @staticmethod
    def _text(elem: ET.Element | None, tag: str) -> str:
        """Collect all text nodes under the given tag."""
        if elem is None:
            return ""
        return "".join(t.text or "" for t in elem.iter(tag))

    @staticmethod
    def _clean(s: str) -> str:
        """Collapse whitespace and strip."""
        return re.sub(r"[ \t]+", " ", s).strip()
