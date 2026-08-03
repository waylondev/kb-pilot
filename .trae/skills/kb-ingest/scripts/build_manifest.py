"""
build_manifest.py — 全局路由表生成器
扫描 .kb/index/ 下所有 metadata.yaml，生成 manifest.json。
源文件路径从 metadata.source_path 读取（相对于仓库根目录）。
"""
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required. Install: pip install pyyaml")
    sys.exit(1)


def build(repo_root: str) -> str:
    root = Path(repo_root)
    kb_index = root / ".kb" / "index"

    if not kb_index.exists():
        print(f"[build_manifest] .kb/index/ not found: {kb_index}")
        print("  Run kb-ingest first to initialize the knowledge base.")
        sys.exit(1)

    entries = []
    for meta_path in sorted(kb_index.rglob("metadata.yaml")):
        doc_dir = meta_path.parent
        tree_path = doc_dir / "tree.json"
        metadata = yaml.safe_load(meta_path.read_text(encoding="utf-8"))

        entry = {
            "doc_id": metadata.get("doc_id", ""),
            "title": metadata.get("title", ""),
            "domain": metadata.get("domain", ""),
            "summary": "",
            "tags": [],
            "updated_at": str(metadata.get("ingested_at", "")),
            "path": metadata.get("source_path", ""),
        }

        if tree_path.exists():
            tree = json.loads(tree_path.read_text(encoding="utf-8"))
            summaries = [n["summary"] for n in tree.get("nodes", []) if n.get("summary")]
            entry["summary"] = "; ".join(summaries[:3]) if summaries else metadata.get("title", "")

            all_keywords = []
            seen = set()
            def collect(nodes):
                for n in nodes:
                    for kw in n.get("keywords", []):
                        if kw not in seen:
                            seen.add(kw)
                            all_keywords.append(kw)
                    collect(n.get("children", []))
            collect(tree.get("nodes", []))
            entry["tags"] = all_keywords[:50]

        entries.append(entry)
        print(f"[build_manifest] {entry['doc_id']}: {entry['title']} ({entry['domain']})")

    manifest_path = root / ".kb" / "manifest.json"
    manifest_path.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"[build_manifest] Generated: {manifest_path}")
    print(f"  - Documents: {len(entries)}")
    return str(manifest_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_manifest.py <repo_root>")
        sys.exit(1)
    build(sys.argv[1])
