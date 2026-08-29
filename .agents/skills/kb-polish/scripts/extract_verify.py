#!/usr/bin/env python3
# /// script
# dependencies = ["pymupdf", "striprtf"]
# ///
"""
extract_verify.py — verify-source extraction entry (plugin dispatch).

Detects the input format -> dispatches to the matching verifiers/ plugin -> extracts
source text + table structure, and emits unified JSON (for the LLM to cross-check
against AnyDoc's raw.md).

Plugins are split by format, one file each (verifiers/*.py); adding a format means
adding a plugin + registration.

Usage:
    python extract_verify.py input.docx
    python extract_verify.py input.pdf -o outdir --save-text
    python extract_verify.py --list

Output (stdout): by default a summary (stats + text_preview) to avoid truncating
    large docs; add --full-text for the complete text.

Exit codes:
    0  success
    1  bad args / file not found / unsupported format
    2  missing dependency (e.g. pymupdf / striprtf)
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Force UTF-8 on stdout/stderr so the JSON contract survives non-UTF-8 consoles
# (Windows GBK/cp936 raises UnicodeEncodeError on non-ASCII output, killing the
# machine-readable result; field-tested). The stdout=JSON promise
# must not depend on the caller setting PYTHONIOENCODING.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# allow running directly as a script (scripts/extract_verify.py) so verifiers can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verifiers import find_verifier, supported_extensions  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="verify-source extraction entry: dispatch by format to plugins, output source text for LLM cross-check.",
        epilog="""Examples:
  python extract_verify.py input.docx
  python extract_verify.py input.pdf -o outdir --save-text
  python extract_verify.py --list

Supported formats: %s

Output: JSON to stdout, progress to stderr. Summary by default (a preview plus
stats); add --full-text for the complete text, --save-text to land verify_text.txt.

Exit codes:
  0  success — a plugin that degrades to a warning still exits 0
  1  bad args, file not found, unsupported format, or the plugin failed
  2  missing dependency (e.g. pymupdf / striprtf)""" % ", ".join(supported_extensions()),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", nargs="?", help="input document path")
    parser.add_argument("-o", "--output", help="output directory (optional)")
    parser.add_argument("--full-text", action="store_true",
                        help="output full text on stdout (default only text_preview to avoid truncation)")
    parser.add_argument("--save-text", action="store_true",
                        help="also save the extracted source text as {outdir}/verify_text.txt")
    parser.add_argument("--list", action="store_true", help="list supported formats and plugins")
    args = parser.parse_args()

    if args.list:
        print("Supported formats:")
        for ext in supported_extensions():
            v = find_verifier(Path("x" + ext))
            # the plugin declares its own dependency, so this listing cannot go
            # stale when a format is added
            print(f"  {ext:<10} -> verifiers/{v.name}.py  (dep: {v.dependency or 'stdlib'})")
        return 0

    if not args.input:
        parser.error("missing input argument (or use --list to see supported formats)")

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"[verify] file not found: {input_path}", file=sys.stderr)
        return 1

    verifier = find_verifier(input_path)
    if verifier is None:
        print(
            f"[verify] unsupported format: {input_path.suffix} (supported: {', '.join(supported_extensions())})",
            file=sys.stderr,
        )
        return 1

    try:
        result = verifier.extract(input_path)
    except ImportError as e:
        print(f"[verify] missing dependency: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # noqa: BLE001 - a plugin crash must degrade to a warning, not a traceback
        print(f"[verify] plugin raised for {input_path.name}: {e}", file=sys.stderr)
        payload = {
            "ok": False,
            "input": str(input_path),
            "verifier": verifier.name,
            "warnings": [f"verifier failed: {e}"],
            "hint": "the file may be corrupt or unsupported; review manually",
        }
        print(json.dumps(payload, ensure_ascii=False))
        return 1

    payload = {
        "ok": True,
        "input": str(input_path),
        "format": result.format,
        "verifier": result.verifier,
        "text": result.text if args.full_text else "",
        "text_preview": result.text[:1500],
        "pages": result.pages if args.full_text else [p["index"] for p in result.pages],
        "tables": result.tables if args.full_text else [t["name"] for t in result.tables],
        "images": [i["name"] for i in result.images],
        "warnings": result.warnings,
        "stats": result.to_dict()["stats"],
        "hint": "summary only by default; add --full-text or --save-text for the full text",
    }

    if args.output:
        out_dir = Path(args.output)
        out_dir.mkdir(parents=True, exist_ok=True)
        if args.save_text:
            (out_dir / "verify_text.txt").write_text(result.text, encoding="utf-8")
        img_dir = out_dir / "images"
        img_dir.mkdir(parents=True, exist_ok=True)
        landed = set()
        if result.images:
            # land embedded images in out_dir/images/, so Step 4 can reference
            # them as ![](./images/<name>) exactly like the zip-based formats
            for img in result.images:
                name, data = img.get("name"), img.get("data")
                if not name or not data:
                    continue
                (img_dir / name).write_bytes(bytes(data))
                landed.add(name)
        # Every `[image: <name>]` placeholder in the verify text must resolve to a
        # real file. AnyDoc's asset extraction misses some zip media (e.g. docx OLE
        # preview bitmaps), so pull those bytes straight out of the container; if a
        # placeholder still has no byte source, say so in warnings instead of
        # letting Step 4 emit a dangling image reference (field-tested).
        placeholder_re = re.compile(r"\[image:\s*([^\]]+?)\s*\]")
        for name in placeholder_re.findall(result.text):
            if name in landed or (img_dir / name).is_file():
                continue
            getter = getattr(verifier, "extract_image", None)
            if getter is not None:
                data = getter(input_path, name)
                if data:
                    (img_dir / name).write_bytes(bytes(data))
                    landed.add(name)
                    print(f"[verify] exported missing asset from container: {name}", file=sys.stderr)
                    continue
            result.warnings.append(
                f"image '{name}' is referenced in the verify text but has no byte source "
                "(not extracted by AnyDoc, not found in the container); do not emit a "
                "![...] reference for it — describe it in words or drop it"
            )
            print(f"[verify] missing asset, no byte source: {name}", file=sys.stderr)
        payload["warnings"] = result.warnings
        payload["images"] = sorted(landed)
        (out_dir / "verify_result.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[verify] result saved to {out_dir}", file=sys.stderr)

    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
