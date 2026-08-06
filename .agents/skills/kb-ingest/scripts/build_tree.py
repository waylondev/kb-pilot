"""
build_tree.py — Markdown heading tree parser

Parses Markdown heading hierarchy (# ~ ######) and produces a tree.json skeleton.
The skeleton contains id/level/title/start_line/end_line/children; summary/keywords
are left empty for the LLM to fill. Pure deterministic parsing; does not call the LLM.

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
from pathlib import Path


def compute_sha256(filepath: Path) -> str:
    return hashlib.sha256(filepath.read_bytes()).hexdigest()


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
        "source_sha256": compute_sha256(source_path),
        "total_lines": total_lines,
        "nodes": nodes
    }


def merge_existing_fillings(new_tree: dict, existing_path: Path) -> dict:
    """If a tree.json already exists, preserve LLM-filled summary/keywords (best-effort mapping when structure changes)."""
    if not existing_path.exists():
        return new_tree

    try:
        old_tree = json.loads(existing_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, KeyError):
        return new_tree

    old_fillings = {}
    def collect(nodes):
        for n in nodes:
            if n.get("summary") or n.get("keywords"):
                old_fillings[n["id"]] = {
                    "summary": n.get("summary", ""),
                    "keywords": n.get("keywords", [])
                }
            collect(n.get("children", []))
    collect(old_tree.get("nodes", []))

    if not old_fillings:
        return new_tree

    new_nodes = {}
    def index(nodes):
        for n in nodes:
            new_nodes[n["id"]] = n
            index(n.get("children", []))
    index(new_tree["nodes"])

    for node_id, filling in old_fillings.items():
        if node_id in new_nodes:
            node = new_nodes[node_id]
            if filling["summary"]:
                node["summary"] = filling["summary"]
            if filling["keywords"]:
                node["keywords"] = filling["keywords"]
        else:
            # Parent may still exist (child id concatenation rule)
            parent_id = "_".join(node_id.split("_")[:-1])
            if parent_id in new_nodes:
                parent = new_nodes[parent_id]
                if filling["summary"]:
                    existing = parent.get("summary", "")
                    parent["summary"] = f"{existing}; {filling['summary']}" if existing else filling["summary"]
                if filling["keywords"]:
                    parent["keywords"] = list(set(parent.get("keywords", []) + filling["keywords"]))

    return new_tree


def infer_title(source_path: Path) -> str:
    """Get title from H1; fall back to file stem if no H1."""
    for line in source_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return source_path.stem


def build(source_path: str, output_path: str, doc_id: str = "", title: str = "") -> dict:
    """Build the tree.json skeleton, write to output_path, return result metadata."""
    source = Path(source_path)
    if not source.exists():
        raise FileNotFoundError(f"source file not found: {source_path}")

    tree = parse_headings(source)
    tree["doc_id"] = doc_id
    tree["title"] = title or infer_title(source)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    tree = merge_existing_fillings(tree, output)
    output.write_text(json.dumps(tree, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "output_path": str(output),
        "doc_id": tree["doc_id"],
        "title": tree["title"],
        "total_lines": tree["total_lines"],
        "source_sha256": tree["source_sha256"],
        "top_level_nodes": len(tree["nodes"])
    }


def main():
    parser = argparse.ArgumentParser(
        prog="build_tree.py",
        description="Parse Markdown heading hierarchy and produce a tree.json skeleton (summary/keywords left empty for the LLM to fill).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python build_tree.py docs/api/auth.md .kb/index/docs/api/auth/tree.json --doc-id doc_001 --title "API Auth"
  python build_tree.py README.md .kb/index/README/tree.json

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
    args = parser.parse_args()

    try:
        result = build(args.source, args.output, args.doc_id, args.title)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)

    # Structured result to stdout; progress to stderr
    print(f"[build_tree] generated tree.json: {result['output_path']}", file=sys.stderr)
    print(f"  doc_id={result['doc_id']} title={result['title']!r}", file=sys.stderr)
    print(f"  top_level_nodes={result['top_level_nodes']} total_lines={result['total_lines']}", file=sys.stderr)
    print(f"  source_sha256={result['source_sha256'][:16]}...", file=sys.stderr)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
