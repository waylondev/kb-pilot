---
name: kb-ingest
description: 将 Markdown 文档接入知识库系统。创建元数据，构建章节索引树，更新全局路由表。当用户提供 Markdown 文档需要入库时使用。
config:
  repo_url: ""
  kb_path: knowledge_repo
---

> **设计边界**：kb-pilot 专注 Markdown 输入。PDF/Word/Excel/HTML 等格式的转换由客户自行处理，本 SKILL 不负责格式转换。原因：转换质量不可控，引入转换工具会增加复杂度且无法保证输出质量。

## 知识库结构

知识库是一个 Git 仓库，由 `repo_url` 指定远程地址，克隆到本地 `kb_path` 目录（`kb_path` 为可配置默认值，执行时替换为实际路径）。其内部结构如下：

```
{kb_path}/
├── manifest.json          # 全局路由表（脚本自动生成）
├── memory/
│   ├── corrections/       # 纠错记录
│   └── route_preferences.json
└── docs/
    └── {domain}/
        └── {doc_id}_{文档简称}/
            ├── *.md               # 原始 Markdown 文档（约定为 source.md，文件名不限）
            ├── tree.json          # 章节索引树
            └── metadata.yaml      # 元数据
```

## 接入流程（检查清单）

- [ ] **Step 1: 接收用户输入**
  - Markdown 文档路径
  - 所属领域
  - 文档简称
  - 维护人

- [ ] **Step 2: 准备知识库**
  - 若 `kb_path` 目录不存在，从 `repo_url` 克隆：`git clone {repo_url} {kb_path}`
  - 若已存在，执行 `git pull` 同步最新内容
  - 确认 `docs/` 目录结构

- [ ] **Step 3: 放置文档**
  - 在 `{kb_path}/docs/{domain}/{doc_id}_{简称}/` 下放入 Markdown 文档（约定命名为 source.md，文件名不限）
  - 直接使用用户提供的 Markdown 文件，不做格式转换
  - 检查 Markdown 结构：标题层级是否完整（#、##、###）、表格/代码块是否正确

- [ ] **Step 4: 创建 metadata.yaml**
  - doc_id 序号规则：查看 `{kb_path}/docs/` 下所有已有文档，取最大序号+1
  - 字段：doc_id, title, domain, maintainer, source_format, converted_at, conversion_quality, manual_edit

- [ ] **Step 5: 构建 tree.json 骨架**
  - 运行脚本：`python .trae/skills/kb-ingest/scripts/build_tree.py "{kb_path}/docs/{domain}/{doc_id}_{简称}/{文档文件名}"`
  - 脚本会自动在文档同目录下生成 tree.json
  - 生成骨架包含：id, level, title, anchor, start_line, end_line, page_range, children
  - summary 和 keywords 为空，等待下一步填充

- [ ] **Step 6: 填充 summary 和 keywords**
  - 读取文档原文和 tree.json 骨架
  - 为每个节点生成：summary（≤20字）、keywords（3~8个）
  - 将填充结果写入 tree.json

- [ ] **Step 7: 更新 manifest.json**
  - 确保 PyYAML 已安装：`pip install pyyaml`
  - 运行脚本：`python .trae/skills/kb-ingest/scripts/build_manifest.py {kb_path}`
  - 脚本会扫描 `{kb_path}/docs/` 目录，重新生成 manifest.json

- [ ] **Step 8: 提交到 Git**
  - `cd {kb_path} && git add docs/{domain}/{doc_id}_{简称}/ manifest.json`
  - `git commit -m "feat: 接入文档 {doc_id} - {标题}"`
  - `git push`

- [ ] **Step 9: 确认完成**
  - 告知用户 doc_id、文档路径、tree.json 节点数、manifest.json 已更新

## 文档重建

用户说"重建 tree.json"或文档有大幅修改时，直接从 Step 5 开始执行（覆盖已有 tree.json）。

## 质量检查

- 检查文档是否有完整标题层级（#、##、###）
- 检查 tree.json 节点数是否合理（通常 10~30 个节点）
- 标题层级缺失时，提示用户完善 Markdown 结构后重新入库

## 常见陷阱（Gotchas）

- **doc_id 序号**：不要依赖记忆或简单计数，必须遍历 docs/ 目录确认最大已有序号
- **标题层级**：文档必须有完整的标题层级（#、##、###），这是 tree.json 构建的基础
- **tree.json 覆盖**：重建 tree.json 会覆盖之前填充的 summary 和 keywords，需重新填充
- **manifest.json 更新**：必须使用 build_manifest.py 脚本生成，不要手动编辑
- **{kb_path} 占位符**：执行时替换为实际知识库路径，默认为 `knowledge_repo`（可配置）