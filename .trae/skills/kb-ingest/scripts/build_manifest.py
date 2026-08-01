"""
build_manifest.py — 全局路由表生成器
扫描 docs/ 下所有 metadata.yaml 和 tree.json，生成 manifest.json。
不人工维护，完全由脚本自动生成。
"""
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required. Install: pip install pyyaml")
    sys.exit(1)


def scan_docs(repo_root: Path) -> list:
    """
    扫描 docs/ 目录，返回所有文档条目。
    每个条目包含：doc_id, title, domain, summary, tags, updated_at, path
    """
    docs_dir = repo_root / "docs"
    if not docs_dir.exists():
        print(f"[build_manifest] docs/ directory not found: {docs_dir}")
        return []
    
    entries = []
    
    for domain_dir in sorted(docs_dir.iterdir()):
        if not domain_dir.is_dir():
            continue
        
        for doc_dir in sorted(domain_dir.iterdir()):
            if not doc_dir.is_dir():
                continue
            
            metadata_path = doc_dir / "metadata.yaml"
            tree_path = doc_dir / "tree.json"
            
            if not metadata_path.exists():
                print(f"[build_manifest] Skipping {doc_dir.name}: no metadata.yaml")
                continue
            
            metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
            
            # 提取文档级 summary 和 tags
            summary = ""
            tags = []
            if tree_path.exists():
                tree = json.loads(tree_path.read_text(encoding="utf-8"))
                # 从根节点 summary 拼接
                summaries = [n["summary"] for n in tree.get("nodes", []) if n.get("summary")]
                summary = "; ".join(summaries[:3]) if summaries else metadata.get("title", "")
                # 从所有节点 keywords 收集 tags
                all_keywords = set()
                def collect_keywords(nodes):
                    for n in nodes:
                        for kw in n.get("keywords", []):
                            all_keywords.add(kw)
                        collect_keywords(n.get("children", []))
                collect_keywords(tree.get("nodes", []))
                tags = sorted(all_keywords)[:50]  # 最多 50 个 tags
            
            # 相对路径（相对于 repo_root）
            rel_path = doc_dir.relative_to(repo_root).as_posix() + "/"
            
            entry = {
                "doc_id": metadata.get("doc_id", ""),
                "title": metadata.get("title", ""),
                "domain": metadata.get("domain", ""),
                "summary": summary,
                "tags": tags,
                "updated_at": str(metadata.get("converted_at", "")),
                "path": rel_path
            }
            entries.append(entry)
    
    return entries


def build(repo_root: str) -> str:
    """
    主入口：生成 manifest.json。
    """
    root = Path(repo_root)
    entries = scan_docs(root)
    
    manifest_path = root / "manifest.json"
    manifest_path.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    
    print(f"[build_manifest] Generated: {manifest_path}")
    print(f"  - Documents: {len(entries)}")
    for e in entries:
        print(f"    - {e['doc_id']}: {e['title']} ({e['domain']})")
    
    return str(manifest_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_manifest.py <knowledge_repo root>")
        sys.exit(1)
    
    build(sys.argv[1])