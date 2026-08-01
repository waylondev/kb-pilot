---
name: kb-ingest
description: 将 PDF/Word/Excel 文档接入知识库系统。转换文档为 Markdown，创建元数据，构建章节索引树，更新全局路由表。当用户提供新文档需要入库时使用。
---

## 目录结构

```
knowledge_repo/
├── manifest.json          # 全局路由表（脚本自动生成）
├── memory/
│   ├── corrections/       # 纠错记录
│   └── route_preferences.json
└── docs/
    ├── 01_财务合规/
    ├── 02_技术研发/
    ├── 03_人力资源/
    └── 99_归档/
```

每个文档目录：
```
docs/{domain}/{doc_id}_{文档简称}/
├── source.md          # 原始 Markdown 文档
├── tree.json          # 章节索引树
└── metadata.yaml      # 元数据
```

## 接入流程（检查清单）

- [ ] **Step 1: 接收用户输入**
  - 文档路径（PDF/Word/Excel）
  - 所属领域（01_财务合规 / 02_技术研发 / 03_人力资源 / 99_归档）
  - 文档简称（如"2025财务报告"）
  - 维护人

- [ ] **Step 2: 转换文档**
  - 使用 MarkItDown 转换：`python -m markitdown "文档路径" > docs/{domain}/{doc_id}_{简称}/source.md`
  - 检查转换质量：表格是否完整、标题层级是否正常
  - MarkItDown 不可用时，提示用户手动提供 Markdown 内容

- [ ] **Step 3: 创建 metadata.yaml**
  - doc_id 序号规则：查看 docs/ 下所有已有文档，取最大序号+1
  - 字段：doc_id, title, domain, maintainer, source_format, converted_at, conversion_quality, manual_edit

- [ ] **Step 4: 构建 tree.json 骨架**
  - 运行 `python .trae/skills/kb-ingest/scripts/build_tree.py "docs/{domain}/{doc_id}_{简称}/source.md"`
  - 生成骨架包含：id, level, title, anchor, start_line, end_line, page_range, children
  - summary 和 keywords 为空，等待下一步填充

- [ ] **Step 5: 填充 summary 和 keywords**
  - 读取 source.md 和 tree.json 骨架
  - 为每个节点生成：summary（≤20字）、keywords（3~8个）
  - 将填充结果写入 tree.json

- [ ] **Step 6: 更新 manifest.json**
  - 运行 `python .trae/skills/kb-ingest/scripts/build_manifest.py .`

- [ ] **Step 7: 提交到 Git**
  - `git add docs/{domain}/{doc_id}_{简称}/ manifest.json`
  - `git commit -m "feat: 接入文档 {doc_id} - {标题}"`

- [ ] **Step 8: 确认完成**
  - 告知用户 doc_id、文档路径、tree.json 节点数、manifest.json 已更新

## 文档重建

用户说"重建 tree.json"或 source.md 有大幅修改时，直接从 Step 4 开始执行（覆盖已有 tree.json）。

## 质量检查

- 转换质量差时，metadata.yaml 中标记 `conversion_quality: poor`，提示用户手动校验
- 检查 source.md 是否有完整标题层级（#、##、###）
- 检查 tree.json 节点数是否合理（通常 10~30 个节点）

## 常见陷阱（Gotchas）

- **doc_id 序号**：不要依赖记忆或简单计数，必须遍历 docs/ 目录确认最大已有序号
- **转换质量**：MarkItDown 对复杂表格和图文混排可能转换不佳，务必人工检查标题层级
- **tree.json 覆盖**：重建 tree.json 会覆盖之前填充的 summary 和 keywords，需重新填充
- **manifest.json 更新**：必须使用 build_manifest.py 脚本生成，不要手动编辑 manifest.json