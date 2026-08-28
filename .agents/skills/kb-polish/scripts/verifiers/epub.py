#!/usr/bin/env python3
"""
verifiers/epub.py — EPUB (.epub) verify-source plugin.

EPUB = zip + XHTML. Read XHTML content in spine order and extract the body text.
"""

from __future__ import annotations

import posixpath
from pathlib import Path

from .base import ZipXmlVerifier, ExtractResult

XHTML = "http://www.w3.org/1999/xhtml"
CNT = "urn:oasis:names:tc:opendocument:xmlns:container"
OPF = "http://www.idpf.org/2007/opf"


def _tag(ns: str, t: str) -> str:
    return f"{{{ns}}}{t}"


class EpubVerifier(ZipXmlVerifier):
    name = "epub"
    extensions = [".epub"]

    def extract(self, path: Path) -> ExtractResult:
        chapters = self._chapter_targets(path)
        files = self._read_zip(path, chapters)
        pages, all_texts = [], []
        for idx, target in enumerate(chapters, 1):
            data = files.get(target)
            if data is None:
                continue
            text = self._xhtml_text(data)
            pages.append({"index": idx, "text": text})
            all_texts.append(text)

        full_text = "\n\n".join(all_texts)
        return ExtractResult(
            format="epub", verifier=self.name, text=full_text,
            pages=pages, tables=[],
        )

    def _chapter_targets(self, path: Path) -> list[str]:
        z = self._open_zip(path)
        if z is None:
            return []
        with z:
            names = set(z.namelist())
            # locate the OPF via container.xml
            opf_path = None
            if "META-INF/container.xml" in names:
                root = self._xml(z.read("META-INF/container.xml"))
                if root is not None:
                    for rf in root.iter(_tag(CNT, "rootfile")):
                        opf_path = rf.get("full-path")
                        break
            if not opf_path or opf_path not in names:
                opf_path = next((n for n in names if n.endswith(".opf")), None)
            if not opf_path:
                return []

            manifest = {}
            spine = []
            opf_root = self._xml(z.read(opf_path))
            if opf_root is None:
                return []
            for item in opf_root.iter(_tag(OPF, "item")):
                manifest[item.get("id")] = item.get("href", "")
            # hrefs are relative to the OPF, and may be ./x, ../x, or nested —
            # a plain string replace would mangle them mid-path.
            base = posixpath.dirname(opf_path)
            for ref in opf_root.iter(_tag(OPF, "itemref")):
                idref = ref.get("idref")
                href = manifest.get(idref) if idref else None
                if not href:
                    continue
                target = posixpath.normpath(posixpath.join(base, href)) if base else posixpath.normpath(href)
                spine.append(target)
            return [t for t in spine if t in names]

    def _xhtml_text(self, data: bytes) -> str:
        root = self._xml(data)
        if root is None:
            return ""
        # collect all text in body (incl. tails); images <img> become `[image: <filename>]` placeholders
        parts = []

        def walk(elem):
            if elem.tag == _tag(XHTML, "img"):
                src = elem.get("src") or ""
                if src:
                    parts.append(f"[image: {src.split('/')[-1]}]")
            if elem.text and elem.text.strip():
                parts.append(elem.text.strip())
            for child in elem:
                walk(child)
            if elem.tail and elem.tail.strip():
                parts.append(elem.tail.strip())

        body = root.find(f".//{{{XHTML}}}body")
        if body is not None:
            walk(body)
        return "\n".join(parts)
