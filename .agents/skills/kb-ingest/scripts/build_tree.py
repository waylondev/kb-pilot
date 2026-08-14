"""
build_tree.py — Markdown heading tree parser + document record builder

Parses Markdown heading hierarchy (# ~ ######) and produces a tree.json that is
both the heading skeleton and the document record: doc-level fields (doc_id,
title, domain, source_path, summary, ingested_at) plus per-section nodes with
id/level/title/start_line/end_line/children. summary/keywords are left empty for
the LLM to fill. The output is minified JSON by default (to save tokens when the
LLM reads it in kb-chat); pass --pretty for a human-readable copy. It also runs
deterministic structure validation (line-range sanity, parent/child containment).
Pure deterministic parsing; does not call the LLM.

See --help for usage. Emits JSON result to stdout, progress to stderr.
"""
# /// script
# dependencies = []
# ///
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def compute_sha256(filepath: Path) -> str:
    return hashlib.sha256(filepath.read_bytes()).hexdigest()


def dump_json(obj: dict, pretty: bool) -> str:
    """Minified by default (fewer tokens for the LLM); pretty when --pretty."""
    if pretty:
        return json.dumps(obj, ensure_ascii=False, indent=2)
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def parse_headings(source_path: Path) -> dict:
    """Single-pass scan of Markdown headings to build the node tree."""
    lines = source_path.read_text(encoding="utf-8").splitlines()
    total_lines = len(lines)

    heading_pattern = re.compile(r"^(#{1,6})\s+(.+)$")
    nodes = []
    stack = []

    for i, line in enumerate(lines):
        m = heading_pattern.match(line)
        if not m:
            continue

        level = len(m.group(1))
        title = m.group(2).strip()
        line_num = i + 1

        if level == 1:
            continue  # H1 is the document title; does not enter the tree

        node = {
            "id": "",
            "level": level,
            "title": title,
            "summary": "",
            "keywords": [],
            "start_line": line_num,
            "end_line": 0,
            "children": []
        }

        while stack and stack[-1]["level"] >= level:
            prev = stack.pop()
            prev["end_line"] = line_num - 1

        if stack:
            parent = stack[-1]
            child_idx = len(parent["children"]) + 1
            node["id"] = f"{parent['id']}_{child_idx}"
            parent["children"].append(node)
        else:
            node["id"] = f"ch_{len(nodes) + 1}"
            nodes.append(node)

        stack.append(node)

    while stack:
        prev = stack.pop()
        prev["end_line"] = total_lines

    return {
        "doc_id": "",
        "title": "",
        "domain": "",
        "source_path": "",
        "summary": "",
        "ingested_at": "",
        "source_sha256": compute_sha256(source_path),
        "total_lines": total_lines,
        "nodes": nodes
    }


def validate_tree(tree: dict) -> tuple:
    """Deterministic structure checks on the skeleton.

    Returns (errors, warnings). Errors must be 0 — they indicate a broken
    skeleton (line ranges, parent/child containment, empty tree). Warnings are
    advisory — e.g. a heading that skips a level (H2 → H4), which is structurally
    valid but usually signals a missing level in the source. Whether to fix a
    warning is a judgment call for the LLM (and the user), not the script.
    """
    errors = []
    warnings = []
    total_lines = tree.get("total_lines", 0)
    nodes = tree.get("nodes", [])

    if not nodes:
        errors.append("no headings below H1; tree.json is empty (source has no H2+ sections)")

    def walk(nodes, parent=None):
        for n in nodes:
            start, end = n.get("start_line", 0), n.get("end_line", 0)
            if start < 1 or start > total_lines:
                errors.append(f"node {n['id']} start_line={start} out of range [1,{total_lines}]")
            if end < start:
                errors.append(f"node {n['id']} end_line={end} < start_line={start}")
            if parent is not None and (start < parent["start_line"] or end > parent["end_line"]):
                errors.append(
                    f"node {n['id']} [{start},{end}] outside parent {parent['id']} "
                    f"[{parent['start_line']},{parent['end_line']}]"
                )
            if parent is not None and n.get("level", 0) > parent.get("level", 0) + 1:
                warnings.append(
                    f"node {n['id']} level {n.get('level')} skips a level below "
                    f"parent {parent['id']} (level {parent.get('level')})"
                )
            walk(n.get("children", []), n)

    walk(nodes)
    return errors, warnings


def merge_existing_fillings(new_tree: dict, existing_path: Path) -> dict:
    """If a tree.json already exists, preserve LLM-filled summary/keywords.

    Matching is anchored on (level, title) rather than positional node ids, so
    fillings survive headings being inserted or removed above or around them.
    Best-effort: a renamed or fully restructured section loses its old filling.
    """
    if not existing_path.exists():
        return new_tree

    try:
        old_tree = json.loads(existing_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, KeyError):
        return new_tree

    # preserve the document-level summary when the new skeleton has none yet
    if old_tree.get("summary") and not new_tree.get("summary"):
        new_tree["summary"] = old_tree["summary"]

    old_fillings = {}
    def collect(nodes):
        for n in nodes:
            if n.get("summary") or n.get("keywords"):
                old_fillings[(n.get("level"), n.get("title"))] = {
                    "summary": n.get("summary", ""),
                    "keywords": n.get("keywords", [])
                }
            collect(n.get("children", []))
    collect(old_tree.get("nodes", []))

    if not old_fillings:
        return new_tree

    def fill(nodes):
        for n in nodes:
            filling = old_fillings.get((n.get("level"), n.get("title")))
            if filling:
                if filling["summary"]:
                    n["summary"] = filling["summary"]
                if filling["keywords"]:
                    n["keywords"] = filling["keywords"]
            fill(n.get("children", []))

    fill(new_tree["nodes"])
    return new_tree


def infer_title(source_path: Path) -> str:
    """Get title from H1; fall back to file stem if no H1."""
    for line in source_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return source_path.stem


def build(
    source: str,
    output_path: str,
    doc_id: str = "",
    title: str = "",
    domain: str = "",
    source_path: str = "",
    ingested_at: str = "",
    pretty: bool = False,
) -> dict:
    """Build the tree.json skeleton, write to output_path, return result metadata."""
    src = Path(source)
    if not src.exists():
        raise FileNotFoundError(f"source file not found: {source}")

    tree = parse_headings(src)
    tree["doc_id"] = doc_id
    tree["title"] = title or infer_title(src)
    tree["domain"] = domain
    tree["source_path"] = source_path
    tree["ingested_at"] = ingested_at or datetime.now(timezone.utc).isoformat()

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    tree = merge_existing_fillings(tree, output)

    errors, warnings = validate_tree(tree)
    for msg in errors:
        print(f"[build_tree] validation: {msg}", file=sys.stderr)
    for msg in warnings:
        print(f"[build_tree] warning: {msg}", file=sys.stderr)

    output.write_text(dump_json(tree, pretty), encoding="utf-8")

    return {
        "output_path": str(output),
        "doc_id": tree["doc_id"],
        "title": tree["title"],
        "domain": tree["domain"],
        "source_path": tree["source_path"],
        "ingested_at": tree["ingested_at"],
        "total_lines": tree["total_lines"],
        "source_sha256": tree["source_sha256"],
        "top_level_nodes": len(tree["nodes"]),
        "validation_issues": len(errors),
        "validation_warnings": len(warnings),
        "pretty": pretty,
    }


def main():
    parser = argparse.ArgumentParser(
        prog="build_tree.py",
        description="Parse Markdown heading hierarchy and produce a tree.json (document record + heading skeleton; summary/keywords left empty for the LLM to fill).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python scripts/build_tree.py {kb_path}/docs/api/auth.md {kb_path}/.kb/index/docs/api/auth/tree.json \\
    --doc-id doc_001 --title "API Auth" --domain api --source-path docs/api/auth.md
  python scripts/build_tree.py README.md .kb/index/README/tree.json --source-path README.md --pretty

Output is minified JSON by default (fewer tokens when the LLM reads it); pass --pretty for a readable copy.

Exit codes:
  0  success
  1  unexpected error (see stderr)
  2  source file not found
"""
    )
    parser.add_argument("source", help="Path to the Markdown source file")
    parser.add_argument("output", help="Output path for tree.json (under the .kb/index/ mirrored directory)")
    parser.add_argument("--doc-id", default="", help="Document ID (e.g. doc_001)")
    parser.add_argument("--title", default="", help="Document title (inferred from H1 if omitted)")
    parser.add_argument("--domain", default="", help="Document domain, used as a routing hint")
    parser.add_argument("--source-path", required=True, help="Source path relative to the repo root, used in the manifest (e.g. docs/api/auth.md)")
    parser.add_argument("--ingested-at", default="", help="ISO timestamp for ingestion (defaults to now)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON (default: minified)")
    args = parser.parse_args()

    try:
        result = build(
            args.source,
            args.output,
            doc_id=args.doc_id,
            title=args.title,
            domain=args.domain,
            source_path=args.source_path,
            ingested_at=args.ingested_at,
            pretty=args.pretty,
        )
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)

    # Structured result to stdout; progress to stderr
    print(f"[build_tree] generated tree.json: {result['output_path']}", file=sys.stderr)
    print(f"  doc_id={result['doc_id']} title={result['title']!r} domain={result['domain']!r}", file=sys.stderr)
    print(f"  top_level_nodes={result['top_level_nodes']} total_lines={result['total_lines']}", file=sys.stderr)
    print(f"  source_sha256={result['source_sha256'][:16]}...", file=sys.stderr)
    print(f"  validation_issues={result['validation_issues']} warnings={result['validation_warnings']}", file=sys.stderr)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
