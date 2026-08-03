"""
build_tree.py — 单遍扫描解析器 (PageIndex 风格)
逐行读取 Markdown，遇 `#` 标题即创建节点，累积行号。
纯正则解析，确定性输出，不调用 LLM。
输出 tree.json 骨架（id、level、title、summary、keywords、start_line、end_line、children）。
"""
import json
import re
import hashlib
import sys
from pathlib import Path


def compute_sha256(filepath: Path) -> str:
    return hashlib.sha256(filepath.read_bytes()).hexdigest()


def parse_headings(source_path: Path) -> dict:
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
            continue

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

    nodes = _apply_constraints(nodes)

    return {
        "doc_id": "",
        "title": "",
        "source_sha256": compute_sha256(source_path),
        "total_lines": total_lines,
        "nodes": nodes
    }


def _apply_constraints(nodes: list, max_nodes: int = 50) -> list:
    def count_nodes(node_list):
        total = len(node_list)
        for n in node_list:
            total += count_nodes(n.get("children", []))
        return total

    def flatten_children(node_list):
        result = []
        for n in node_list:
            if n.get("children"):
                n["children"] = []
            result.append(n)
        return result

    total = count_nodes(nodes)
    if total > max_nodes:
        nodes = flatten_children(nodes)

    return nodes


def merge_summary_keywords(tree: dict, ai_fill: dict) -> dict:
    all_nodes = {}
    def index_nodes(node_list):
        for n in node_list:
            all_nodes[n["id"]] = n
            index_nodes(n.get("children", []))
    index_nodes(tree["nodes"])

    for node_id, fill_data in ai_fill.items():
        if not fill_data.get("summary") and not fill_data.get("keywords"):
            continue

        if node_id in all_nodes:
            node = all_nodes[node_id]
            if fill_data.get("summary"):
                node["summary"] = fill_data["summary"]
            if fill_data.get("keywords"):
                node["keywords"] = fill_data["keywords"]
        else:
            parent_id = "_".join(node_id.split("_")[:-1])
            if parent_id in all_nodes:
                parent = all_nodes[parent_id]
                if fill_data.get("summary"):
                    existing = parent.get("summary", "")
                    parent["summary"] = f"{existing}; {fill_data['summary']}" if existing else fill_data["summary"]
                if fill_data.get("keywords"):
                    parent["keywords"] = list(set(parent.get("keywords", []) + fill_data["keywords"]))

    return tree


def preserve_existing_data(new_tree: dict, existing_path: Path) -> dict:
    if not existing_path.exists():
        return new_tree

    try:
        old_tree = json.loads(existing_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, KeyError):
        return new_tree

    old_nodes = {}
    def collect_old(nodes):
        for n in nodes:
            if n.get("summary") or n.get("keywords"):
                old_nodes[n["id"]] = {
                    "summary": n.get("summary", ""),
                    "keywords": n.get("keywords", [])
                }
            collect_old(n.get("children", []))
    collect_old(old_tree.get("nodes", []))

    if old_nodes:
        merge_summary_keywords(new_tree, old_nodes)

    return new_tree


def build(source_path: str, output_path: str,
          doc_id: str = "", title: str = "") -> str:
    """
    主入口：构建 tree.json 骨架。

    Args:
        source_path: Markdown 源文件路径
        output_path: tree.json 输出路径（必须指定，写入 .kb/index/ 镜像目录）
        doc_id: 文档 ID（如 doc_001）
        title: 文档标题
    """
    source = Path(source_path)
    if not source.exists():
        raise FileNotFoundError(f"source file not found: {source_path}")

    tree = parse_headings(source)

    # doc_id 和 title：优先用传入参数，否则从 H1/文件名推断
    if doc_id:
        tree["doc_id"] = doc_id

    if title:
        tree["title"] = title
    else:
        # 尝试从 H1 获取标题
        for line in source.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                tree["title"] = line[2:].strip()
                break
        if not tree["title"]:
            tree["title"] = source.stem

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    tree = preserve_existing_data(tree, output_path)

    output_path.write_text(json.dumps(tree, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[build_tree] Generated: {output_path}")
    print(f"  - doc_id: {tree['doc_id']}")
    print(f"  - title: {tree['title']}")
    print(f"  - Nodes: {len(tree['nodes'])} top-level")
    print(f"  - Total lines: {tree['total_lines']}")
    print(f"  - SHA256: {tree['source_sha256'][:16]}...")

    return str(output_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python build_tree.py <source.md path> <output path> [doc_id] [title]")
        sys.exit(1)

    source = sys.argv[1]
    output = sys.argv[2]
    did = sys.argv[3] if len(sys.argv) > 3 else ""
    ttl = sys.argv[4] if len(sys.argv) > 4 else ""
    build(source, output, did, ttl)
