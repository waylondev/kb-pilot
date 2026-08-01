import json, re
from pathlib import Path

def parse_simple_yaml(path):
    data = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        m = re.match(r'^(\w+):\s*(.+)$', line.strip())
        if m:
            data[m.group(1)] = m.group(2).strip()
    return data

entries = []
docs_dir = Path('knowledge_repo/docs')
for domain_dir in sorted(docs_dir.iterdir()):
    if not domain_dir.is_dir(): continue
    for doc_dir in sorted(domain_dir.iterdir()):
        if not doc_dir.is_dir(): continue
        meta_path = doc_dir / 'metadata.yaml'
        tree_path = doc_dir / 'tree.json'
        if not meta_path.exists(): continue
        metadata = parse_simple_yaml(meta_path)
        summary = ''
        tags = []
        if tree_path.exists():
            tree = json.loads(tree_path.read_text(encoding='utf-8'))
            summaries = [n['summary'] for n in tree.get('nodes', []) if n.get('summary')]
            summary = '; '.join(summaries[:3]) if summaries else metadata.get('title', '')
            all_keywords = set()
            def collect_keywords(nodes):
                for n in nodes:
                    for kw in n.get('keywords', []):
                        all_keywords.add(kw)
                    # 同时加入章节标题作为文档级标签
                    if n.get('title'):
                        all_keywords.add(n['title'])
                    collect_keywords(n.get('children', []))
            collect_keywords(tree.get('nodes', []))
            # 加入领域标签（从domain路径提取）
            domain_name = metadata.get('domain', '')
            domain_parts = domain_name.split('_')
            if len(domain_parts) > 1:
                all_keywords.add(domain_parts[1])  # e.g. "财务合规"
            # 加入文档标题中的关键词
            title = metadata.get('title', '')
            for word in re.findall(r'[\u4e00-\u9fff\w]+', title):
                if len(word) >= 2:
                    all_keywords.add(word)
            # 优先选择语义标签（长度>=2的中文或英文词），过滤纯数字/符号标签
            semantic_tags = []
            numeric_tags = []
            for kw in all_keywords:
                stripped = kw.strip()
                if re.match(r'^[\d.,%\+\-xX×\s:/]+$', stripped):
                    numeric_tags.append(kw)
                elif len(stripped) >= 2:
                    semantic_tags.append(kw)
                else:
                    numeric_tags.append(kw)
            # 按长度排序（长的优先），语义标签在前
            semantic_tags.sort(key=lambda x: -len(x))
            tags = semantic_tags[:50]
            if len(tags) < 50:
                tags.extend(numeric_tags[:(50 - len(tags))])
        rel_path = doc_dir.relative_to('knowledge_repo').as_posix() + '/'
        entry = {
            'doc_id': metadata.get('doc_id', ''),
            'title': metadata.get('title', ''),
            'domain': metadata.get('domain', ''),
            'summary': summary,
            'tags': tags,
            'updated_at': str(metadata.get('converted_at', '')),
            'path': rel_path
        }
        entries.append(entry)

manifest_path = Path('knowledge_repo/manifest.json')
manifest_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Generated: {manifest_path}')
print(f'Documents: {len(entries)}')
for e in entries:
    print(f'  {e["doc_id"]}: {e["title"]} ({e["domain"]}) [{len(e["tags"])} tags]')