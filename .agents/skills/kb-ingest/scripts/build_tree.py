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

Two correctness guarantees the skeleton depends on:

- Lines inside fenced code blocks (``` or ~~~) are never headings. A `# comment`
  in a shell block must not become a node, or it both invents a phantom section
  and truncates the enclosing section's end_line.
- On re-ingest, carried-over LLM fillings are *reported*, not silently applied.
  `reused_fillings` / `reused_doc_summary` / `source_changed` tell the LLM what
  was inherited and whether the text moved underneath it. Deciding whether an
  inherited summary is now stale is the LLM's job, not the script's.

See --help for usage. Emits JSON result to stdout, progress to stderr.
"""
# /// script
# dependencies = []
# ///
import argparse
import bisect
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def compute_sha256(filepath: Path) -> str:
    return hashlib.sha256(filepath.read_bytes()).hexdigest()


def index_root(output_parent: Path) -> Path:
    """Walk up from an output tree.json's parent to the .kb/index/ root."""
    p = output_parent
    while p != p.parent:
        if p.name == "index" and p.parent.name == ".kb":
            return p
        p = p.parent
    return output_parent  # fallback: scan from the given directory as-is


def next_doc_id(kb_index_root: Path) -> str:
    """Scan every tree.json under .kb/index/ and return doc_{max_seq+1:03d}.

    Deterministic counting across the whole index — so sibling documents never
    collide on the same id. The LLM never has to scan and count by hand.
    """
    max_seq = 0
    if kb_index_root.exists():
        for tree_path in kb_index_root.rglob("tree.json"):
            try:
                doc_id = json.loads(tree_path.read_text(encoding="utf-8")).get("doc_id", "")
            except (json.JSONDecodeError, OSError):
                continue
            m = re.match(r"doc_(\d+)", doc_id)
            if m:
                max_seq = max(max_seq, int(m.group(1)))
    return f"doc_{max_seq + 1:03d}"


def resolve_doc_id(output_path: Path, explicit: str = "") -> str:
    """Pick the doc_id for an output tree.json.

    Precedence: an explicit override > the id already in the existing tree.json
    (a re-ingest keeps its id, so manifest references stay stable) > the next
    free id scanned from the whole .kb/index/ root (so siblings never collide).
    The LLM never has to count documents by hand.
    """
    if explicit:
        return explicit
    if output_path.exists():
        try:
            existing = json.loads(output_path.read_text(encoding="utf-8")).get("doc_id", "")
        except (json.JSONDecodeError, OSError):
            existing = ""
        if existing:
            return existing
    return next_doc_id(index_root(output_path.parent))


def dump_json(obj: dict, pretty: bool) -> str:
    """Minified by default (fewer tokens for the LLM); pretty when --pretty."""
    if pretty:
        return json.dumps(obj, ensure_ascii=False, indent=2)
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


# --- Fenced code block detection -------------------------------------------------
# A `# comment` inside a shell or Python code block is not a heading. Skipping
# fenced regions is what keeps the skeleton trustworthy: mistaking one for a
# heading both invents a phantom node and truncates the enclosing section's
# end_line, which silently corrupts every citation built on top of it.
#
# Follows CommonMark: either ``` or ~~~ (3+ chars, up to 3 leading spaces),
# and the closing fence must use the same character and be at least as long as
# the opening one. An unterminated fence runs to the end of the file.

FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
FENCE_CLOSE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})\s*$")


def find_code_fence_regions(lines: list) -> list:
    """Return fenced code regions as [(start, end), ...] with 1-based inclusive lines."""
    regions = []
    open_char = ""
    open_len = 0
    start = 0

    for i, line in enumerate(lines, 1):
        if open_char:
            m = FENCE_CLOSE_RE.match(line)
            if m and m.group(1)[0] == open_char and len(m.group(1)) >= open_len:
                regions.append((start, i))
                open_char, open_len, start = "", 0, 0
            continue

        m = FENCE_OPEN_RE.match(line)
        if not m:
            continue
        fence = m.group(1)
        # A backtick fence's info string may not contain a backtick (CommonMark)
        if fence[0] == "`" and "`" in m.group(2):
            continue
        open_char, open_len, start = fence[0], len(fence), i

    if open_char:
        regions.append((start, len(lines)))  # unterminated fence runs to EOF
    return regions


def make_fence_checker(regions: list):
    """Return an O(log n) predicate `is_inside_code(line_no)` for the given regions."""
    if not regions:
        return lambda line_no: False
    starts = [r[0] for r in regions]

    def is_inside_code(line_no: int) -> bool:
        idx = bisect.bisect_right(starts, line_no) - 1
        return idx >= 0 and line_no <= regions[idx][1]

    return is_inside_code


def parse_headings(source_path: Path) -> dict:
    """Single-pass scan of Markdown headings to build the node tree.

    Lines inside fenced code blocks are never treated as headings.
    """
    lines = source_path.read_text(encoding="utf-8").splitlines()
    total_lines = len(lines)

    heading_pattern = re.compile(r"^(#{1,6})\s+(.+)$")
    is_inside_code = make_fence_checker(find_code_fence_regions(lines))
    nodes = []
    stack = []

    for i, line in enumerate(lines):
        if is_inside_code(i + 1):
            continue
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
    advisory — e.g. a heading that skips a level (H2 → H4), or a tree that
    starts below H2 (top-level node is not an H2), which are structurally
    valid but usually signal a missing level in the source. Whether to fix a
    warning is a judgment call for the LLM (and the user), not the script.
    """
    errors = []
    warnings = []
    total_lines = tree.get("total_lines", 0)
    nodes = tree.get("nodes", [])

    if not nodes:
        errors.append("no headings below H1; tree.json is empty (source has no H2+ sections)")
    elif nodes[0].get("level", 0) != 2:
        warnings.append(
            f"top-level node {nodes[0]['id']} starts at level {nodes[0].get('level')} "
            "(tree should start at H2)"
        )

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


def merge_existing_fillings(new_tree: dict, existing_path: Path) -> tuple:
    """If a tree.json already exists, preserve LLM-filled summary/keywords.

    Matching is anchored on (level, title) rather than positional node ids, so
    fillings survive headings being inserted or removed above or around them.
    Duplicate titles are matched in order (first new occurrence takes the first
    old filling for that (level, title)). Best-effort: a renamed or fully
    restructured section loses its old filling.

    Returns (new_tree, info). `info` reports facts only: how many fillings were
    carried over, and whether the source text changed since the last ingest.
    Whether a carried-over summary is now *stale* is a semantic judgment and
    stays with the LLM — the script cannot know that "the fee is 100" stopped
    being true.

    That distinction matters because matching is structural: a source edit that
    changes only a number or a sentence — the most common kind — keeps every
    filling while silently making it stale. Reporting `source_changed` is what
    lets the LLM notice; swallowing it is what let staleness through before.
    """
    info = {
        "reused_fillings": 0,
        "reused_doc_summary": False,
        "previous_sha256": "",
        "had_existing": False,
    }
    if not existing_path.exists():
        return new_tree, info

    try:
        old_tree = json.loads(existing_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return new_tree, info

    info["had_existing"] = True
    info["previous_sha256"] = old_tree.get("source_sha256", "")

    # preserve the document-level summary when the new skeleton has none yet
    if old_tree.get("summary") and not new_tree.get("summary"):
        new_tree["summary"] = old_tree["summary"]
        info["reused_doc_summary"] = True

    # (level, title) -> queue of fillings, so duplicate titles are consumed in order
    old_fillings: dict = {}
    def collect(nodes):
        for n in nodes:
            if n.get("summary") or n.get("keywords"):
                old_fillings.setdefault((n.get("level"), n.get("title")), []).append({
                    "summary": n.get("summary", ""),
                    "keywords": n.get("keywords", [])
                })
            collect(n.get("children", []))
    collect(old_tree.get("nodes", []))

    if not old_fillings:
        return new_tree, info

    reused = [0]
    def fill(nodes):
        for n in nodes:
            queue = old_fillings.get((n.get("level"), n.get("title")))
            if queue:
                filling = queue.pop(0)
                if filling["summary"]:
                    n["summary"] = filling["summary"]
                if filling["keywords"]:
                    n["keywords"] = filling["keywords"]
                reused[0] += 1
            fill(n.get("children", []))

    fill(new_tree["nodes"])
    info["reused_fillings"] = reused[0]
    return new_tree, info


def infer_title(source_path: Path) -> str:
    """Get title from the first H1; fall back to the file stem if there is none.

    Lines inside fenced code blocks are skipped — otherwise a shell comment such
    as `# Install Guide` becomes the document title and pollutes routing.
    """
    lines = source_path.read_text(encoding="utf-8").splitlines()
    is_inside_code = make_fence_checker(find_code_fence_regions(lines))
    for i, line in enumerate(lines, 1):
        if is_inside_code(i):
            continue
        m = re.match(r"^#\s+(.+)$", line)
        if m:
            return m.group(1).strip()
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

    tree, merge_info = merge_existing_fillings(tree, output)

    errors, warnings = validate_tree(tree)
    for msg in errors:
        print(f"[build_tree] validation: {msg}", file=sys.stderr)
    for msg in warnings:
        print(f"[build_tree] warning: {msg}", file=sys.stderr)

    # A source edit that keeps the heading structure still inherits every old
    # filling — so "did the text change" must be visible, not inferred.
    source_changed = bool(merge_info["previous_sha256"]) and (
        merge_info["previous_sha256"] != tree["source_sha256"]
    )
    if source_changed and (merge_info["reused_fillings"] or merge_info["reused_doc_summary"]):
        print(
            f"[build_tree] source changed since last ingest: "
            f"{merge_info['reused_fillings']} inherited section fillings"
            + (" + document summary" if merge_info["reused_doc_summary"] else "")
            + " must be re-checked against the new text",
            file=sys.stderr,
        )

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
        "reused_fillings": merge_info["reused_fillings"],
        "reused_doc_summary": merge_info["reused_doc_summary"],
        "source_changed": source_changed,
        "previous_sha256": merge_info["previous_sha256"],
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
  python scripts/build_tree.py {abs_kb}/docs/api/auth.md {abs_kb}/.kb/index/docs/api/auth/tree.json \\
    --title "API Auth" --domain api --source-path docs/api/auth.md
  python scripts/build_tree.py {abs_kb}/README.md {abs_kb}/.kb/index/README/tree.json --source-path README.md --pretty

doc_id is auto-inferred (doc_{max_seq+1:03d} from the whole .kb/index/ root) and kept
stable on re-ingest; pass --doc-id only when you must override. Output is minified
JSON by default (fewer tokens when the LLM reads it); pass --pretty for a readable copy.

On re-ingest the result reports what was carried over from the existing tree.json:
  reused_fillings     sections that kept their previous summary/keywords
  reused_doc_summary  whether the document-level summary was kept
  source_changed      whether the source text differs from the recorded sha256
When source_changed is true while fillings were reused, re-read the source and
re-verify them: structure-preserving edits (a number, a sentence) inherit every
old filling without anything else noticing.

Exit codes:
  0  success
  1  unexpected error (see stderr)
  2  source file not found
"""
    )
    parser.add_argument("source", help="Path to the Markdown source file")
    parser.add_argument("output", help="Output path for tree.json (under the .kb/index/ mirrored directory)")
    parser.add_argument("--doc-id", default="", help="Document ID (e.g. doc_001); auto-inferred from existing tree.json if omitted")
    parser.add_argument("--title", default="", help="Document title (inferred from H1 if omitted)")
    parser.add_argument("--domain", default="", help="Document domain, used as a routing hint")
    parser.add_argument("--source-path", required=True, help="Source path relative to the repo root, used in the manifest (e.g. docs/api/auth.md)")
    parser.add_argument("--ingested-at", default="", help="ISO timestamp for ingestion (defaults to now)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON (default: minified)")
    args = parser.parse_args()

    output_path = Path(args.output)
    doc_id = resolve_doc_id(output_path, args.doc_id)

    try:
        result = build(
            args.source,
            args.output,
            doc_id=doc_id,
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
    print(
        f"  reused_fillings={result['reused_fillings']} "
        f"source_changed={result['source_changed']}",
        file=sys.stderr,
    )
    print(f"  validation_issues={result['validation_issues']} warnings={result['validation_warnings']}", file=sys.stderr)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
