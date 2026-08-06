"""
build_manifest.py — Global routing table generator

Scans all metadata.yaml under .kb/index/, aggregates summary (LLM-filled in metadata.yaml)
and tags (collected from tree.json), and produces .kb/manifest.json.
Pure deterministic aggregation; does not call the LLM.

See --help for usage. Emits JSON result to stdout, progress to stderr.
"""
# /// script
# dependencies = ["pyyaml"]
# ///
import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print(
        "Error: PyYAML is required. Install with: pip install pyyaml",
        file=sys.stderr,
    )
    sys.exit(3)


def collect_entry(meta_path: Path) -> dict:
    """Assemble one manifest entry from metadata.yaml and the sibling tree.json."""
    doc_dir = meta_path.parent
    tree_path = doc_dir / "tree.json"
    metadata = yaml.safe_load(meta_path.read_text(encoding="utf-8"))

    entry = {
        "doc_id": metadata.get("doc_id", ""),
        "title": metadata.get("title", ""),
        "domain": metadata.get("domain", ""),
        "summary": metadata.get("summary", ""),
        "tags": [],
        "updated_at": str(metadata.get("ingested_at", "")),
        "path": metadata.get("source_path", ""),
    }

    if tree_path.exists():
        tree = json.loads(tree_path.read_text(encoding="utf-8"))

        # tags: collect keywords across the whole tree, dedupe, preserve traversal order
        all_keywords = []
        seen = set()
        def collect_keywords(nodes):
            for n in nodes:
                for kw in n.get("keywords", []):
                    if kw not in seen:
                        seen.add(kw)
                        all_keywords.append(kw)
                collect_keywords(n.get("children", []))
        collect_keywords(tree.get("nodes", []))
        entry["tags"] = all_keywords

    return entry


def build(repo_root: str) -> dict:
    """Scan all metadata.yaml under .kb/index/ and recompute manifest.json."""
    root = Path(repo_root)
    kb_index = root / ".kb" / "index"

    if not kb_index.exists():
        raise FileNotFoundError(
            f".kb/index/ not found at: {kb_index}. "
            "Run kb-ingest first to initialize the knowledge base."
        )

    entries = []
    for meta_path in sorted(kb_index.rglob("metadata.yaml")):
        entry = collect_entry(meta_path)
        entries.append(entry)
        print(
            f"[build_manifest] {entry['doc_id']}: {entry['title']} (domain={entry['domain']})",
            file=sys.stderr,
        )

    manifest_path = root / ".kb" / "manifest.json"
    manifest_path.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "manifest_path": str(manifest_path),
        "document_count": len(entries),
        "domains": sorted({e["domain"] for e in entries if e["domain"]}),
    }


def main():
    parser = argparse.ArgumentParser(
        prog="build_manifest.py",
        description="Scan all metadata.yaml under .kb/index/ and aggregate them into .kb/manifest.json (global routing table).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python build_manifest.py knowledge_repo
  python build_manifest.py .

Exit codes:
  0  success
  1  unexpected error (see stderr)
  2  .kb/index/ not found (run kb-ingest first)
  3  PyYAML dependency missing (pip install pyyaml)
"""
    )
    parser.add_argument("repo_root", help="Path to the knowledge base Git repo root")
    args = parser.parse_args()

    try:
        result = build(args.repo_root)
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
