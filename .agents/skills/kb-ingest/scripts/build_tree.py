#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
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
- On re-ingest, only *fillings* are carried over, and what is carried over is
  *reported*, not silently applied. `reused_fillings` / `reused_doc_summary` /
  `source_changed` tell the LLM what was inherited and whether the text moved
  underneath it. `title` and `domain` are re-derived every time instead — they are
  single semantic values with no cost argument for inheriting, and keeping them
  would mean the script deciding that last time's classification still holds.
  `previous_title` / `previous_domain` are reported so a dropped value is visible.
  Deciding whether an inherited summary is stale is the LLM's job, not the script's.

See --help for usage. Emits JSON result to stdout, progress to stderr.
"""
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

# What counts as a heading is decided here, in exactly one place: an ATX heading
# with at least one non-space character after the #s, and a trailing closing
# sequence of #s stripped from the title (CommonMark). kb-polish's validators
# borrow `heading()` rather than keeping their own regexes, so a document that
# validates clean here parses the same there.
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


def heading(line: str):
    """Return (level, title) if `line` is an ATX heading, else None."""
    m = HEADING_RE.match(line)
    if not m:
        return None
    return len(m.group(1)), m.group(2).strip()


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


def parse_headings(source_path: Path, lines: list = None) -> dict:
    """Single-pass scan of Markdown headings to build the node tree.

    Lines inside fenced code blocks are never treated as headings.
    `lines` may be passed in by a caller that already read them, so a build does
    not read the same file once per consumer.
    """
    if lines is None:
        lines = source_path.read_text(encoding="utf-8").splitlines()
    total_lines = len(lines)

    is_inside_code = make_fence_checker(find_code_fence_regions(lines))
    nodes = []
    stack = []

    for i, line in enumerate(lines):
        if is_inside_code(i + 1):
            continue
        h = heading(line)
        if not h:
            continue

        level, title = h
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
    """If a tree.json already exists, carry over the fillings a rebuild would blank.

    Only *fillings* are carried over — per-section summary/keywords, and the
    document-level summary — because regenerating them means re-reading the whole
    document, and most of them are still valid when the structure has not moved.

    Record fields (`title`, `domain`) are deliberately **not** carried over. Both
    are semantic judgements the LLM makes per ingest, and both are a single value,
    so there is no cost argument for inheriting one the way there is for a
    document's worth of summaries. Keeping them would mean the script deciding
    that last time's classification still holds — a semantic call, not a skeleton
    fact. What the script does instead is report `previous_title` /
    `previous_domain` so the caller can see what it just dropped.

    Fillings are matched on (level, title) rather than positional node ids, so
    they survive headings inserted or removed around them. Duplicate titles are
    matched in order; a renamed or fully restructured section loses its filling.

    Returns (new_tree, info). `info` reports facts only: how much was carried
    over, and whether the source text changed since the last ingest. Whether a
    carried-over summary is now *stale* is a semantic judgment and stays with
    the LLM — the script cannot know that "the fee is 100" stopped being true.

    That distinction matters because matching is structural: a source edit that
    changes only a number or a sentence — the most common kind — keeps every
    filling while silently making it stale. Reporting `source_changed` is what
    lets the LLM notice; swallowing it is what let staleness through before.
    """
    info = {
        "reused_fillings": 0,
        "reused_doc_summary": False,
        "previous_sha256": "",
        "previous_title": "",
        "previous_domain": "",
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
    # Recorded so the caller can see a value it just let go, without this script
    # second-guessing whether the old one was still right.
    info["previous_title"] = old_tree.get("title", "")
    info["previous_domain"] = old_tree.get("domain", "")

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


def first_h1(source_path: Path, lines: list = None) -> str:
    """Return the first H1's text, or "" when the source has none.

    Lines inside fenced code blocks are skipped — otherwise a shell comment such
    as `# Install Guide` becomes the document title and pollutes routing.

    Returns "" rather than falling back to the file stem, because a caller needs
    to tell the two apart: only a *missing* H1 means a previously authored title
    is still the best one available. Falling back here would overwrite it.
    """
    if lines is None:
        lines = source_path.read_text(encoding="utf-8").splitlines()
    is_inside_code = make_fence_checker(find_code_fence_regions(lines))
    for i, line in enumerate(lines, 1):
        if is_inside_code(i):
            continue
        h = heading(line)
        if h and h[0] == 1:
            return h[1]
    return ""


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
    """Build the tree.json skeleton, write to output_path, return result metadata.

    `doc_id` is resolved here when left empty: the id already in an existing
    tree.json wins (so a re-ingest keeps its id), otherwise the next free one
    scanned from the whole .kb/index/ root.
    """
    src = Path(source)
    if not src.exists():
        raise FileNotFoundError(f"source file not found: {source}")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    # Read the source once as text and hand the same lines to both consumers;
    # the checksum reads bytes separately on purpose (re-encoding text would
    # lose BOM/CRLF differences that the checksum exists to catch).
    lines = src.read_text(encoding="utf-8").splitlines()
    tree = parse_headings(src, lines)
    # doc_id is part of the skeleton, so it is resolved here rather than left to
    # the caller: a re-ingest keeps its id, a new document takes the next free one.
    tree["doc_id"] = doc_id or resolve_doc_id(output)
    # title and domain are re-derived on every ingest, never inherited. Both are
    # the LLM's call (domain is a routing hint; neither appears in the source),
    # and both are a single value, so there is nothing to save by keeping the old
    # one. Title falls back to the source's H1, then the file stem.
    h1 = first_h1(src, lines)
    tree["title"] = title or h1 or src.stem
    tree["domain"] = domain
    tree["source_path"] = source_path
    tree["ingested_at"] = ingested_at or datetime.now(timezone.utc).isoformat()

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

    # A re-ingest that does not re-supply title/domain drops the previous values.
    # That is intended — both are re-derived each time — but losing a value nobody
    # decided to lose is exactly the kind of change that should be announced.
    #
    # The title announcement is not limited to the "no H1 either, so the file stem
    # won" case. An H1 winning is a legitimate re-derivation, but it still replaces
    # a previously recorded title that nobody was asked about — most importantly an
    # LLM-authored one, which is the value the flags exist to set. Reporting it is
    # one line; swallowing it means a --title from a previous ingest disappears
    # with nothing in the run saying so.
    dropped = []
    if merge_info["previous_domain"] and not tree["domain"]:
        dropped.append(f"domain (was {merge_info['previous_domain']!r})")
    if (
        merge_info["previous_title"]
        and tree["title"] != merge_info["previous_title"]
        and not title
    ):
        dropped.append(
            f"title (was {merge_info['previous_title']!r}; re-derived from "
            f"{'the H1' if h1 else 'the file stem'} this run)"
        )
    if dropped:
        print(
            "[build_tree] not supplied this run, previous value dropped: "
            + "; ".join(dropped)
            + " — pass --domain/--title to set it deliberately",
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
        "title_source": "flag" if title else ("h1" if h1 else "stem"),
        "previous_title": merge_info["previous_title"],
        "previous_domain": merge_info["previous_domain"],
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
  title_source        where the title came from: flag / h1 / stem
  previous_title      the previous title, when this run replaced it
  previous_domain     the previous domain, when this run did not re-supply one
When source_changed is true while fillings were reused, re-read the source and
re-verify them: structure-preserving edits (a number, a sentence) inherit every
old filling without anything else noticing.

title and domain are NOT inherited — pass --title/--domain on every re-ingest.
Both are the LLM's judgement per ingest, and dropping one is reported on stderr
rather than done quietly.

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
    print(
        f"  reused_fillings={result['reused_fillings']} "
        f"title_source={result['title_source']} "
        f"domain={result['domain'] or '-'} "
        f"source_changed={result['source_changed']}",
        file=sys.stderr,
    )
    print(f"  validation_issues={result['validation_issues']} warnings={result['validation_warnings']}", file=sys.stderr)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
