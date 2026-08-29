#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
check_source.py — Has the source drifted from what tree.json recorded?

Compares the source file's current SHA256 against the `source_sha256` stored in
tree.json, and reports whether the recorded line ranges can still be trusted.

This is the precise drift check that reading needs and line counting cannot give:
an edit that replaces "100" with "500" keeps the line count identical, so a
line-count comparison reports "no drift" while every citation into that section
now points at text that says something else.

This is kb-chat's own copy. kb-ingest carries an identical copy for its
"Rebuild on change" step; the two are pinned behaviour-identical by the
cross-skill contract tests in tests/test_consistency.py.

Used by:
- kb-chat Step 3, before reading — to warn that citations may be stale

Reports facts only. Whether a drift matters for the question being asked, and
whether to re-ingest now or continue with a warning, is the caller's judgment.

See --help for usage. Emits JSON result to stdout, progress to stderr.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

# Force UTF-8 on stdout/stderr so the JSON contract survives non-UTF-8 consoles
# (Windows GBK/cp936; field-tested).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def compute_sha256(filepath: Path) -> str:
    return hashlib.sha256(filepath.read_bytes()).hexdigest()


def count_lines(filepath: Path) -> int:
    return len(filepath.read_text(encoding="utf-8").splitlines())


def check(source: str, tree: str) -> dict:
    """Compare a source file against the checksum recorded in its tree.json."""
    src = Path(source)
    tree_path = Path(tree)

    if not src.is_file():
        raise FileNotFoundError(f"source file not found: {source}")
    if not tree_path.is_file():
        raise FileNotFoundError(f"tree.json not found: {tree}")

    try:
        tree_data = json.loads(tree_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"tree.json is not valid JSON: {tree} ({e})") from e

    current_sha = compute_sha256(src)
    recorded_sha = tree_data.get("source_sha256", "")
    current_lines = count_lines(src)
    recorded_lines = tree_data.get("total_lines", 0)

    # A missing recorded checksum means the tree predates the field, or was
    # hand-written. We cannot claim "unchanged" without something to compare to.
    unknown = not recorded_sha
    drifted = bool(recorded_sha) and recorded_sha != current_sha

    return {
        "source": str(src),
        "tree": str(tree_path),
        "doc_id": tree_data.get("doc_id", ""),
        "drifted": drifted,
        "checksum_unknown": unknown,
        "current_total_lines": current_lines,
        "recorded_total_lines": recorded_lines,
        "line_count_changed": current_lines != recorded_lines,
        "trustworthy": not drifted and not unknown,
        "hint": (
            "no recorded checksum; re-ingest to establish one"
            if unknown
            else (
                "source changed since ingest: line anchors may point at different text; "
                "warn the user and offer to re-ingest before citing"
                if drifted
                else "source matches the recorded checksum; line anchors are valid"
            )
        ),
    }


def main():
    parser = argparse.ArgumentParser(
        prog="check_source.py",
        description="Check whether a source file has drifted from the checksum recorded in its tree.json.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python scripts/check_source.py {abs_kb}/docs/api/auth.md \\
    {abs_kb}/.kb/index/docs/api/auth/tree.json

Why not compare line counts: an edit that changes only a number or a sentence
keeps the line count identical while invalidating every citation into that
section. The checksum catches that; a line count does not.

Exit codes:
  0  check completed — read "drifted" in the JSON (a drift is a result, not an error)
  1  source file or tree.json missing / unreadable
  2  unexpected error (see stderr)
"""
    )
    parser.add_argument("source", help="Path to the Markdown source file")
    parser.add_argument("tree", help="Path to the document's tree.json")
    args = parser.parse_args()

    try:
        result = check(args.source, args.tree)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)

    print(
        f"[check_source] {result['doc_id'] or result['source']}: "
        f"drifted={result['drifted']} lines={result['recorded_total_lines']}->{result['current_total_lines']}",
        file=sys.stderr,
    )
    if result["drifted"]:
        print(f"[check_source] {result['hint']}", file=sys.stderr)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
