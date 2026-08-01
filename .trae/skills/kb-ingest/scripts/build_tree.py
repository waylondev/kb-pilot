"""
build_tree.py — 单遍扫描解析器 (PageIndex 风格)
逐行读取 source.md，遇 `#` 标题即创建节点，累积行号。
纯正则解析，确定性输出，不调用 LLM。
输出 tree.json 骨架（id、level、title、anchor、start_line、end_line、page_range、children）。
"""
import json
import re
import hashlib
import sys
from pathlib import Path


def compute_sha256(filepath: Path) -> str:
    """计算文件 SHA256"""
    return hashlib.sha256(filepath.read_bytes()).hexdigest()


def parse_headings(source_path: Path, page_lines: int = 50) -> dict:
    """
    单遍扫描 source.md，解析标题层级，构建树骨架。
    
    Args:
        source_path: source.md 文件路径
        page_lines: 每页大约行数，用于估算 page_range
    
    Returns:
        tree.json 骨架 dict
    """
    lines = source_path.read_text(encoding="utf-8").splitlines()
    total_lines = len(lines)
    
    # 正则匹配 Markdown 标题: # ## ### ####
    heading_pattern = re.compile(r"^(#{1,4})\s+(.+)$")
    
    nodes = []
    stack = []  # 用栈维护层级关系
    
    for i, line in enumerate(lines):
        m = heading_pattern.match(line)
        if not m:
            continue
        
        level = len(m.group(1))
        title = m.group(2).strip()
        line_num = i + 1  # 1-based
        
        # 层级约束：最多 4 层
        if level > 4:
            level = 4
        
        # 跳过 H1（文档标题），不纳入节点树
        if level == 1:
            continue
        
        node = {
            "id": "",
            "level": level,
            "title": title,
            "anchor": f"{'#' * level} {title}",
            "summary": "",
            "keywords": [],
            "start_line": line_num,
            "end_line": 0,
            "page_range": [line_num // page_lines + 1, 0],
            "children": []
        }
        
        # 关闭前一个同级或更高级节点的 end_line
        while stack and stack[-1]["level"] >= level:
            prev = stack.pop()
            prev["end_line"] = line_num - 1
            prev["page_range"][1] = (line_num - 1) // page_lines + 1
            if prev["page_range"][1] < prev["page_range"][0]:
                prev["page_range"][1] = prev["page_range"][0]
        
        # 生成 ID
        if stack:
            parent = stack[-1]
            child_idx = len(parent["children"]) + 1
            node["id"] = f"{parent['id']}_{child_idx}"
            parent["children"].append(node)
        else:
            node["id"] = f"ch_{len(nodes) + 1}"
            nodes.append(node)
        
        stack.append(node)
    
    # 关闭剩余节点
    while stack:
        prev = stack.pop()
        prev["end_line"] = total_lines
        prev["page_range"][1] = total_lines // page_lines + 1
        if prev["page_range"][1] < prev["page_range"][0]:
            prev["page_range"][1] = prev["page_range"][0]
    
    # 应用约束
    nodes = _apply_constraints(nodes)
    
    return {
        "doc_id": "",
        "title": "",
        "source_sha256": compute_sha256(source_path),
        "total_lines": total_lines,
        "nodes": nodes
    }


def _apply_constraints(nodes: list, max_nodes: int = 50) -> list:
    """
    应用树约束：
    - 层级 ≤ 4（已在解析时处理）
    - 节点数 ≤ 50（超过自动压缩 H3 及以下）
    """
    def count_nodes(node_list):
        total = len(node_list)
        for n in node_list:
            total += count_nodes(n.get("children", []))
        return total
    
    def flatten_children(node_list):
        """压缩 H3 及以下：将子节点合并到父节点"""
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
    """
    将 AI 填充的 summary 和 keywords 合并到骨架中。
    
    Args:
        tree: 骨架 tree dict
        ai_fill: {"ch_1": {"summary": "...", "keywords": [...]}, ...}
    """
    def fill_node(node):
        node_id = node["id"]
        if node_id in ai_fill:
            node["summary"] = ai_fill[node_id].get("summary", "")
            node["keywords"] = ai_fill[node_id].get("keywords", [])
        for child in node.get("children", []):
            fill_node(child)
    
    for node in tree["nodes"]:
        fill_node(node)
    
    return tree


def preserve_existing_data(new_tree: dict, existing_path: Path) -> dict:
    """
    从已有 tree.json 中保留 summary 和 keywords。
    如果已有 tree.json 存在，将其中非空的 summary 和 keywords 合并到新骨架中。
    """
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


def build(source_path: str, output_path: str | None = None, ai_fill: dict | None = None) -> str:
    """
    主入口：构建 tree.json。
    
    Args:
        source_path: source.md 路径
        output_path: 输出路径，默认与 source.md 同目录下的 tree.json
        ai_fill: AI 填充的 summary 和 keywords
    
    Returns:
        tree.json 文件路径
    """
    source = Path(source_path)
    if not source.exists():
        raise FileNotFoundError(f"source.md not found: {source_path}")
    
    tree = parse_headings(source)
    
    # 从文件路径推断 doc_id 和 title
    doc_dir = source.parent
    dir_name = doc_dir.name  # e.g. "doc_001_2025财务报告"
    parts = dir_name.split("_", 2)
    if len(parts) >= 2:
        tree["doc_id"] = parts[0] + "_" + parts[1]
        tree["title"] = parts[2] if len(parts) > 2 else parts[1]
    else:
        tree["doc_id"] = dir_name
        tree["title"] = dir_name
    
    if ai_fill:
        tree = merge_summary_keywords(tree, ai_fill)
    
    if output_path is None:
        output_path = doc_dir / "tree.json"
    else:
        output_path = Path(output_path)
    
    # 保留已有 tree.json 中的 summary 和 keywords（骨架重建时保留 AI 填充数据）
    tree = preserve_existing_data(tree, output_path)
    
    output_path.write_text(json.dumps(tree, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[build_tree] Generated: {output_path}")
    print(f"  - Nodes: {len(tree['nodes'])} top-level")
    print(f"  - Total lines: {tree['total_lines']}")
    print(f"  - SHA256: {tree['source_sha256'][:16]}...")
    
    return str(output_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_tree.py <source.md path> [output path]")
        sys.exit(1)
    
    source = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    build(source, output)