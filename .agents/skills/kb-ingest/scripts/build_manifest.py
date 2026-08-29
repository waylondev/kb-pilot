#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
build_manifest.py — Global routing table generator

Scans all tree.json under .kb/index/ (each tree.json is the document record:
doc_id, title, domain, summary, source_path, ingested_at) and aggregates them,
collecting tags from node keywords, into .kb/manifest.json.
Pure deterministic aggregation; does not call the LLM.

The output is minified JSON by default (to save tokens when the LLM reads it in
kb-chat Step 1); pass --pretty for a human-readable copy.

An index that yields no usable tree.json raises instead of writing `[]`: an empty
manifest is indistinguishable from "this knowledge base has no documents", and
kb-chat would answer "not mentioned in the documents" for sources that exist.

See --help for usage. Emits JSON result to stdout, progress to stderr.
"""
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


class EmptyIndexError(Exception):
    """Raised when .kb/index/ yields no usable tree.json at all.

    Serializing an empty list is the one outcome that must never happen quietly:
    kb-chat's failure handling looks for a *missing* manifest, so an empty array
    sails through and every question is answered "not mentioned in the documents"
    for a knowledge base that still has sources. Losing the routing table must
    look like the failure it is.
    """


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
    skipped = []
    missing_sources = []
    for tree_path in sorted(kb_index.rglob("tree.json")):
        try:
            entry = collect_entry(tree_path)
        except (json.JSONDecodeError, OSError) as exc:
            print(
                f"[build_manifest] skipping unreadable tree.json: {tree_path} ({exc})",
                file=sys.stderr,
            )
            skipped.append(str(tree_path))
            continue
        entries.append(entry)
        print(
            f"[build_manifest] {entry['doc_id']}: {entry['title']} (domain={entry['domain']})",
            file=sys.stderr,
        )

    # A `path` that does not resolve makes the document unanswerable: kb-chat reads
    # the source from it, and the failure only surfaces at Step 3 as a
    # FileNotFoundError that its failure handling does not list. Reporting the fact
    # here costs one line and puts it where the ingest that produced it still is.
    # Deciding what to do about it — retype the flag, re-ingest, or delete the
    # entry — is the caller's call, so this warns rather than blocks.
    for entry in entries:
        rel = entry.get("path", "")
        if rel and not (root / rel).is_file():
            missing_sources.append({"doc_id": entry["doc_id"], "path": rel})
            print(
                f"[build_manifest] {entry['doc_id']}: source_path does not resolve "
                f"under the kb root: {rel}",
                file=sys.stderr,
            )

    if not entries:
        raise EmptyIndexError(
            f"no usable tree.json under {kb_index}"
            + (f" ({len(skipped)} unreadable, skipped)" if skipped else " (the directory is empty)")
            + ". Refusing to write an empty manifest: kb-chat would then answer "
            "'not mentioned in the documents' for every question. Re-ingest the "
            "documents, or repair the tree.json files listed above."
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
        "skipped_unreadable": skipped,
        # Facts, not a verdict: an entry listed here is unreachable for kb-chat,
        # never a reason to abort the build.
        "missing_sources": missing_sources,
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
  python scripts/build_manifest.py {abs_kb}
  python scripts/build_manifest.py {abs_kb} --pretty

Output is minified JSON by default (fewer tokens when the LLM reads it); pass --pretty for a readable copy.

`missing_sources` lists entries whose `path` does not resolve under the kb root —
a typo there makes the document unanswerable, and it is reported rather than
enforced. The build still writes the manifest.

An index that yields no usable tree.json is an error, never an empty manifest: an
empty manifest makes kb-chat answer "not mentioned in the documents" for a knowledge
base that still has sources.

Exit codes:
  0  success
  1  unexpected error (see stderr)
  2  .kb/index/ missing, or no usable tree.json in it (run kb-ingest first)
"""
    )
    parser.add_argument("repo_root", help="Path to the knowledge base Git repo root")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON (default: minified)")
    args = parser.parse_args()

    try:
        result = build(args.repo_root, pretty=args.pretty)
    except (FileNotFoundError, EmptyIndexError) as e:
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
