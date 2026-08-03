---
name: kb-ingest
description: >-
  Use this skill when the user wants to ingest a Markdown document into the knowledge base,
  initialize a knowledge base from a Git repo, or batch-ingest all .md files in a directory.
  Triggers on phrases like "接入文档", "入库", "初始化知识库", "接入整个目录", even when the
  user doesn't explicitly mention "kb-pilot" or ".kb". Only handles Markdown input — PDF/Word/HTML
  conversion is the user's responsibility.
config:
  repo_url: ""
  kb_path: knowledge_repo
---

# kb-ingest — 给文档建目录

> **目录 + 原文 = 知识库**。原文不动，元数据集中在 `.kb/` 镜像路径，Git 即真理。

## 知识库契约

知识库是一个 Git 仓库，克隆到 `{kb_path}`。`.kb/` 是元数据目录：

- `.kb/manifest.json` — 全局路由表（每条含 doc_id、title、domain、summary、tags、path）
- `.kb/index/{源文件路径去掉 .md}/` — 镜像每个文档
  - `metadata.yaml` — 文档级元数据（doc_id、title、domain、source_path、ingested_at）
  - `tree.json` — 章节目录树（节点含 id、level、title、summary、keywords、start_line、end_line、children）
- `.kb/memory/` — 跨会话记忆（corrections/、route_preferences.json）

**路径映射**：源文件 `docs/api/auth.md` → 元数据目录 `.kb/index/docs/api/auth/`（`/` 当目录层级，去掉 `.md`）。

## 接入流程

目标是让一份 Markdown 文档**可被 kb-chat 路由、定位、阅读**。

1. **准备仓库** — `{kb_path}` 不存在则 `git clone {repo_url} {kb_path}`；已存在则 `git pull`。确保 `.kb/index/` 和 `.kb/memory/corrections/` 存在
2. **定位源文件** — 确认 `{kb_path}/{source_rel_path}` 存在；检查标题层级（`#`~`######`）完整，层级缺失提示用户完善后重新入库
3. **分配 doc_id** — 扫描 `.kb/index/` 下所有 metadata.yaml，取最大序号 +1（如 `doc_007`）
4. **创建 metadata.yaml** — 在 `.kb/index/{source_rel_dir}/` 下创建，含 doc_id、title（从 H1 获取）、domain（用户指定或从一级目录推断）、source_path、ingested_at
5. **生成 tree.json 骨架** — 运行 `scripts/build_tree.py`（见下），解析标题层级生成骨架
6. **LLM 填充 summary 和 keywords** — 通读每个章节内容，逐节点填充（**不可用规则脚本替代**，规则脚本不理解语义会破坏路由精度）
7. **更新 manifest.json** — 运行 `scripts/build_manifest.py`（见下），聚合所有文档
8. **提交 Git** — `git add .kb/` + 新源文件，`git commit -m "kb: 接入 {doc_id} - {title}"`，`git push`
9. **告知用户** — doc_id、源文件路径、tree.json 节点数

## 可用脚本

脚本在 `scripts/` 目录下，用相对路径引用。确定性子任务用脚本，语义任务必须 LLM 完成。

- **`scripts/build_tree.py`** — 解析 Markdown 标题层级，生成 tree.json 骨架（summary/keywords 留空待 LLM 填充）
  ```bash
  python scripts/build_tree.py {kb_path}/{source_rel_path} \
    {kb_path}/.kb/index/{source_rel_dir}/tree.json \
    --doc-id {doc_id} --title "{title}"
  ```
- **`scripts/build_manifest.py`** — 扫描所有 metadata.yaml，聚合生成 .kb/manifest.json
  ```bash
  python scripts/build_manifest.py {kb_path}
  ```

两个脚本都支持 `--help`，stdout 输出 JSON 结果，stderr 输出进度。

## 批量接入

当用户说"接入整个目录"、"扫描仓库中的所有 md 文件"、"从现有 Git 仓库初始化"时：

1. `git clone {repo_url} {kb_path}`（若不存在）
2. 递归扫描 `{kb_path}` 下所有 `.md`，排除 `.kb/` 和 `.git/`
3. 对每个尚无 metadata.yaml 的文件，从流程 Step 4 开始执行
4. 最后统一运行 `scripts/build_manifest.py`
5. 一次 Git commit + push

## 文档重建

文档大幅修改时，通过 `tree.json` 的 `source_sha256` 检测漂移：

1. 对比 tree.json 中 `source_sha256` 与源文件当前 SHA256
2. 一致 → 跳过；不一致 → 重新运行 Step 5（脚本会尽量保留已有 summary/keywords）
3. 结构变化时重新执行 Step 6（旧 summary/keywords 可能不匹配新章节）
4. 运行 Step 7 更新 manifest，Step 8 提交 Git

## Gotchas

- **doc_id 序号**：必须扫描 `.kb/index/` 下已有 metadata.yaml 确认最大序号，不要依赖记忆
- **source_path 字段**：metadata.yaml 中的 source_path 是相对于仓库根的路径，build_manifest.py 据此生成 manifest 的 path 字段，kb-chat 据此读取原文——写错会导致问答时找不到源文件
- **标题层级**：源文件必须有完整的标题层级（`#`~`######`），这是 tree.json 构建的基础；H1 作为文档标题不进树，从 H2 开始
- **summary/keywords 不可脚本化**：规则脚本无法理解语义，会破坏 kb-chat 的路由精度。即使看起来"只是提取关键词"，也必须 LLM 逐节点填充
- **并发协作**：多人同时入库时，`.kb/` 下文件冲突由 Git merge 解决，不在应用层加锁
- **大规模知识库**：单库超过几百篇文档时，按团队/领域拆分 Git 仓库，不做物理分片
- **{kb_path} 占位符**：执行时替换为实际知识库路径，默认 `knowledge_repo`

## 边界

- **仅 Markdown 输入** — PDF/Word/HTML 转换由客户自行处理
- **不做向量/Chunk/图谱** — kb-pilot 核心边界，违反即偏离设计
- **不往用户目录放元数据** — 所有元数据在 `.kb/` 下，删除即卸载
- **不在应用层加锁** — 协作冲突由 Git 解决
