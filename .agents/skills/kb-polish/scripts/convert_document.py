#!/usr/bin/env python3
# /// script
# dependencies = ["firecrawl-anydoc"]
# ///
"""
convert_document.py — source document -> first-draft Markdown + embedded asset extraction.

Uses AnyDoc to convert PDF/Word/Excel/PPT/EPUB/CSV/OpenDocument etc. into Markdown,
and extracts embedded images (-> images/) and other files (-> attachments/).

Note: AnyDoc does not support .html/.md/.txt (already text) or .tsv (rename to .csv),
and does no image OCR; do not run these through this script.

Deterministic layer: conversion and asset landing only; semantic judgment (is the
structure reasonable, where do images go) is the LLM's job.

Usage:
    python convert_document.py input.docx -o outdir
    python convert_document.py input.pdf -o outdir

Output (stdout):
    {"ok": true, "input": "...", "output_dir": "...", "markdown": "...",
     "images": ["..."], "attachments": ["..."], "format": "pdf"}

Exit codes:
    0  success
    1  bad args / file not found / conversion failed
"""

import argparse
import json
import sys
from pathlib import Path

# Force UTF-8 on stdout/stderr so the JSON contract survives non-UTF-8 consoles
# (Windows GBK/cp936; field-tested).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def load_anydoc():
    """Import AnyDoc lazily.

    Kept out of module scope so `--help` still works when the dependency is not
    installed — which is exactly when someone needs to read the usage text.
    """
    try:
        import anydoc
    except ImportError:
        print(
            "[convert] missing dependency firecrawl-anydoc; install it with:\n"
            "          pip install firecrawl-anydoc",
            file=sys.stderr,
        )
        sys.exit(1)
    return anydoc


def sanitize_filename(name: str, fallback: str) -> str:
    """Extract a safe filename from an asset's original path."""
    name = (name or "").replace("\\", "/").split("/")[-1].strip()
    name = "".join(c for c in name if c.isalnum() or c in "._- ").strip()
    return name or fallback


def write_asset(asset, index: int, out_dir: Path, category: str) -> Path | None:
    """Write a single asset to disk, returning the path or None."""
    try:
        data = bytes(asset.data) if not isinstance(asset.data, bytes) else asset.data
    except AttributeError:
        data = asset  # in some versions data is already bytes
    if not data:
        return None

    media_type = getattr(asset, "media_type", "") or ""
    origin = getattr(asset, "origin_part", "") or ""
    name = sanitize_filename(origin, f"{category}_{index}")

    ext = Path(name).suffix
    if not ext:
        # infer the extension from media_type
        ext = {
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/gif": ".gif",
            "image/webp": ".webp",
            "application/pdf": ".pdf",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
        }.get(media_type, ".bin")
        name += ext

    target_dir = out_dir / category
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / name
    target.write_bytes(data)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(
        description="source document -> Markdown + embedded asset extraction (AnyDoc-based, deterministic).",
        epilog="""Examples:
  python convert_document.py input.docx -o outdir
  python convert_document.py input.pdf -o outdir

Output: raw.md (first draft), images/, attachments/

Not supported by AnyDoc: .html/.md/.txt (already text — ingest directly) and
.tsv (rename to .csv first). AnyDoc does no OCR, so scans (no text layer) fail
conversion with a NeedsOcrError — that failure surfaces, not a fabricated result.
Note: AnyDoc exposes no asset API for PDF (to_document refuses PDFs), so PDF
assets are not extracted; images embedded in Word/PPT/Excel etc. land in images/.

Exit codes:
  0  success
  1  bad args, file not found, or conversion failed (see stderr)""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="input document path (PDF/Word/PPT/Excel/CSV etc.)")
    parser.add_argument("-o", "--output", required=True, help="output directory")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"[convert] file not found: {input_path}", file=sys.stderr)
        return 1

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    anydoc = load_anydoc()

    try:
        # 1) convert the body to Markdown
        markdown_text = anydoc.to_markdown(str(input_path))
        raw_md = out_dir / "raw.md"
        raw_md.write_text(markdown_text, encoding="utf-8")

        # 2) extract embedded assets (images -> images/, others -> attachments/)
        images, attachments, asset_warnings = [], [], []
        try:
            document = anydoc.to_document(bytes(input_path.read_bytes()))
            for idx, asset in enumerate(document.assets, 1):
                media_type = getattr(asset, "media_type", "") or ""
                is_image = media_type.startswith("image/")
                category = "images" if is_image else "attachments"
                target = write_asset(asset, idx, out_dir, category)
                if target is not None:
                    (images if is_image else attachments).append(str(target))
                    print(f"[convert] extracted {category}: {target.name}", file=sys.stderr)
        except Exception as e:
            # asset-extraction failure must not block the main conversion, but it
            # must not be silent either — the stdout JSON reports it so the LLM
            # knows the image/attachment list may be incomplete (field-tested:
            # previously only stderr, stdout still ok:true). E.g. AnyDoc gives PDF
            # no asset API (to_document refuses PDFs), so PDFs get this warning.
            msg = f"asset extraction skipped: {e}"
            asset_warnings.append(msg)
            print(f"[convert] {msg}", file=sys.stderr)

        result = {
            "ok": True,
            "input": str(input_path),
            "output_dir": str(out_dir),
            "markdown": str(raw_md),
            "images": images,
            "attachments": attachments,
            "warnings": asset_warnings,
            "format": input_path.suffix.lstrip(".").lower(),
        }
    except Exception as e:
        print(f"[convert] conversion failed: {e}", file=sys.stderr)
        return 1

    # progress to stderr, structured result to stdout (the LLM parses stdout)
    print(f"[convert] done: raw.md written ({len(markdown_text)} chars), images {len(images)}, attachments {len(attachments)}", file=sys.stderr)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
