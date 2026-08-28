#!/usr/bin/env python3
"""
verifiers/pdf.py — PDF verify-source plugin.

Extracts the text layer with PyMuPDF (MuPDF engine), independent of AnyDoc's
implementation. Uses the block-level ``get_text("dict")`` view so embedded
images appear exactly where the source lays them out: text blocks contribute
their text, image blocks contribute an ``[image: <name>]`` placeholder (and
their bytes) right in place — the same 1-pass, position-exact output that the
zip-based plugins get from the document model.

Scans (no text layer) are NOT dropped: every page is rendered to an image
(page_N.png) and embedded as ``![page N](./images/page_N.png)`` so the document
asset survives in the knowledge base for viewing. kb-polish still performs no
OCR and the LLM cannot read page content — the empty-text-layer warning stays
so the caller knows the semantics.

Dependency: pip install pymupdf
"""

from __future__ import annotations

import re
from pathlib import Path

from .base import BaseVerifier, ExtractResult


class PdfVerifier(BaseVerifier):
    name = "pdf"
    extensions = [".pdf"]

    #: render resolution for scanned pages; 150 dpi keeps text legible for
    #: viewing while bounding the asset size
    SCAN_DPI = 150

    def extract(self, path: Path) -> ExtractResult:
        import pymupdf  # lazy import so the entry gives a clear error when the dependency is missing

        warnings = []
        doc = pymupdf.open(str(path))
        pages = []
        page_texts = []
        images = []
        img_no = 0  # running counter across the document -> deterministic `image_N` names
        for i, page in enumerate(doc, 1):
            lines = []  # this page's output, block by block in source order
            for block in page.get_text("dict").get("blocks", []):
                if block.get("type") == 1:  # image block
                    bbox = block.get("bbox") or (0, 0, 0, 0)
                    ext = (block.get("ext") or "").strip() or "png"
                    img_no += 1
                    name = f"image_{img_no}.{ext}"
                    data = block.get("image")
                    # dict view usually carries the decoded bytes; fall back to
                    # matching the page image by geometry when it is None
                    if not data:
                        data = self._image_bytes(doc, page, bbox)
                    if data:
                        images.append({
                            "name": name,
                            "data": data,
                            "media_type": self._media_type(ext),
                        })
                        lines.append(f"[image: {name}]")
                else:  # text block: keep readable line order
                    for entry in block.get("lines", []):
                        spans = entry.get("spans", [])
                        if not spans:
                            continue
                        lines.append("".join(s.get("text", "") for s in spans).strip())
            text = "\n".join(line for line in lines if line)
            pages.append({"index": i, "text": text})
            page_texts.append(text)
        doc.close()

        full_text = "\n\n".join(page_texts)
        # A scan has no real text even if image placeholders were emitted: decide on
        # the text layer after stripping `[image: ...]` markers, so an image-only PDF
        # is reported as a scan rather than treated as body content.
        real_text = re.sub(r"\[image: [^\]]+\]", "", full_text).strip()
        if not real_text:
            # Pure scan: no text layer. Keep the document by embedding every page as
            # an image (rendered, not the original embedded bytes, so it works for
            # every scan incl. JPEG2000 / layered ones). kb-polish does no OCR and
            # the LLM cannot read page content — the warning states the semantics.
            warnings.append("empty text layer: scanned/pure-image PDF; pages embedded as images only (no OCR, LLM cannot read page content)")
            scan_doc = pymupdf.open(str(path))
            images = []
            rendered = []
            for i, page in enumerate(scan_doc, 1):
                name = f"page_{i}.png"
                pix = page.get_pixmap(dpi=self.SCAN_DPI, colorspace=pymupdf.csRGB, alpha=False)
                images.append({
                    "name": name,
                    "data": pix.tobytes("png"),
                    "media_type": "image/png",
                })
                ref = f"![page {i}](./images/{name})"
                rendered.append({"index": i, "text": ref})
                page_texts[i - 1] = ref
            pages = rendered
            full_text = "\n\n".join(page_texts)
            scan_doc.close()

        return ExtractResult(
            format="pdf",
            verifier=self.name,
            text=full_text,
            pages=pages,
            tables=[],  # PDF has no structural tables; table reconstruction needs pdfplumber/Camelot or AnyDoc
            images=images,
            warnings=warnings,
        )

    @staticmethod
    def _image_bytes(doc, page, bbox) -> bytes | None:
        """Fallback bytes for an image block whose dict entry lacks the decoded
        image. Match the closest image xref by its placement rect on the page,
        then extract it from the document stream."""
        try:
            best = None
            best_d = float("inf")
            for img in page.get_images(full=True):
                xref = img[0]
                rect = page.get_image_rects(xref)
                if not rect:
                    continue
                r = rect[0]
                d = abs(r.x0 - bbox[0]) + abs(r.y0 - bbox[1])
                if d < best_d:
                    best_d = d
                    best = xref
            if best is None:
                return None
            info = doc.extract_image(best)
            return info.get("image") if info else None
        except Exception:
            return None

    @staticmethod
    def _media_type(ext: str) -> str:
        return {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
            "bmp": "image/bmp",
            "tif": "image/tiff",
            "tiff": "image/tiff",
            "webp": "image/webp",
        }.get(ext.lower(), "application/octet-stream")
