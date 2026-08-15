"""
build_manifest.py — Global routing table generator

Scans all tree.json under .kb/index/ (each tree.json is the document record:
doc_id, title, domain, summary, source_path, ingested_at) and aggregates them,
collecting tags from node keywords, into .kb/manifest.json.
Pure deterministic aggregation; does not call the LLM.

The output is minified JSON by default (to save tokens when the LLM reads it in
kb-chat Step 1); pass --pretty for a human-readable copy.

See --help for usage. Emits JSON result to stdout, progress to stderr.
"""
# /// script
# dependencies = []
# ///
import argparse
import json
import sys
from pathlib import Path


def collect_entry(tree_path: Path) -> dict:
    """Assemble one manifest entry from a tree.json document record."""
    tree = json.loads(tree_path.read_text(encoding="utf-8"))

    entry = {
        "doc_id": tree.get("doc_id", ""),
        "title": tree.get("title", ""),
        "domain": tree.get("domain", ""),
        "summary": tree.get("summary", ""),
        "tags": [],
        "updated_at": tree.get("ingested_at", ""),
        "path": tree.get("source_path", ""),
    }

    # tags: collect keywords from top-level sections only (the document theme),
    # dedupe, preserve traversal order. Sub-section keywords stay in tree.json
    # for localization — top-level tags keep routing focused and the manifest small.
    all_keywords = []
    seen = set()
    for n in tree.get("nodes", []):
        for kw in n.get("keywords", []):
            if kw not in seen:
                seen.add(kw)
                all_keywords.append(kw)

    entry["tags"] = all_keywords
    return entry


def build(repo_root: str, pretty: bool = False) -> dict:
    """Scan all tree.json under .kb/index/ and recompute manifest.json."""
    root = Path(repo_root)
    kb_index = root / ".kb" / "index"

    if not kb_index.exists():
        raise FileNotFoundError(
            f".kb/index/ not found at: {kb_index}. "
            "Run kb-ingest first to initialize the knowledge base."
        )

    entries = []
    for tree_path in sorted(kb_index.rglob("tree.json")):
        entry = collect_entry(tree_path)
        entries.append(entry)
        print(
            f"[build_manifest] {entry['doc_id']}: {entry['title']} (domain={entry['domain']})",
            file=sys.stderr,
        )

    manifest_path = root / ".kb" / "manifest.json"
    if pretty:
        text = json.dumps(entries, ensure_ascii=False, indent=2)
    else:
        text = json.dumps(entries, ensure_ascii=False, separators=(",", ":"))
    manifest_path.write_text(text, encoding="utf-8")

    return {
        "manifest_path": str(manifest_path),
        "document_count": len(entries),
        "domains": sorted({e["domain"] for e in entries if e["domain"]}),
        "pretty": pretty,
    }


def main():
    parser = argparse.ArgumentParser(
        prog="build_manifest.py",
        description="Scan all tree.json under .kb/index/ and aggregate them into .kb/manifest.json (global routing table).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python scripts/build_manifest.py {kb_path}
  python scripts/build_manifest.py {kb_path} --pretty

Output is minified JSON by default (fewer tokens when the LLM reads it); pass --pretty for a readable copy.

Exit codes:
  0  success
  1  unexpected error (see stderr)
  2  .kb/index/ not found (run kb-ingest first)
"""
    )
    parser.add_argument("repo_root", help="Path to the knowledge base Git repo root")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON (default: minified)")
    args = parser.parse_args()

    try:
        result = build(args.repo_root, pretty=args.pretty)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[build_manifest] generated manifest.json: {result['manifest_path']}", file=sys.stderr)
    print(f"  documents={result['document_count']} domains={result['domains']}", file=sys.stderr)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
