---
name: kb-ingest
description: 将 Markdown 文档接入知识库。原文不动，元数据集中在 .kb/ 下镜像路径，Git 即真理。当用户提供 Markdown 文档需要入库时使用。
config:
  repo_url: ""
  kb_path: knowledge_repo
---

# kb-ingest — 给文档建目录

> **目录 + 原文 = 知识库**。LLM 足够聪明，只需精准的目录和完整原文，不需要向量、Chunk、图谱。

## 设计哲学

| 原则 | 含义 |
|------|------|
| **LLM 是路由引擎** | summary/keywords 必须由 LLM 理解内容后填充，规则脚本无法替代语义理解 |
| **零侵入** | 原文留在用户原位不动，所有元数据集中在 `.kb/`，删除即卸载 |
| **Git 即真理** | 所有元数据是文本文件，版本/协作/同步/冲突都靠 Git，不在应用层加锁 |
| **确定性骨架 + 语义血肉** | 骨架（章节层级、行号）由脚本确定性生成；血肉（summary、keywords）由 LLM 注入 |
| **少即是多** | 不做向量、不做 Chunk、不做图谱、不做分片、不做格式转换 |

## 知识库契约

知识库是一个 Git 仓库，克隆到本地 `{kb_path}`。`.kb/` 是 kb-pilot 的元数据目录：

- `.kb/manifest.json` — 全局路由表，每条记录代表一个文档（含 doc_id、title、domain、summary、tags、path）
- `.kb/index/{源文件路径去掉 .md}/` — 镜像每个文档，存放该文档的元数据
  - `metadata.yaml` — 文档级元数据（doc_id、title、domain、source_path 等）
  - `tree.json` — 章节目录树（节点含 id、level、title、summary、keywords、start_line、end_line、children）
- `.kb/memory/` — 跨会话记忆
  - `corrections/{doc_id}.jsonl` — 纠错记录
  - `route_preferences.json` — 路由偏好

**路径映射**：源文件 `docs/api/auth.md` → 元数据目录 `.kb/index/docs/api/auth/`。即把文件路径的 `/` 当目录层级，去掉 `.md` 后缀。

## 接入意图

当用户说"接入文档"、"入库"、"初始化知识库"时，目标是**让一份 Markdown 文档可被 kb-chat 路由、定位、阅读**。达成下列子目标即可，实现方式由 LLM 自行裁量：

1. **可达** — 用户原文路径已记录在 `metadata.yaml` 的 `source_path` 字段，kb-chat 据此读取原文
2. **可路由** — 文档出现在 `.kb/manifest.json`，含足够的 summary/tags 让 LLM 通过语义匹配判断相关性
3. **可定位** — `tree.json` 完整反映原文标题层级，每个节点都有 summary 和 keywords，让 LLM 能定位到章节级
4. **可追溯** — 元数据提交到 Git，便于版本回溯和多人协作

## LLM 不可替代的部分

> **核心约束**：以下必须由 LLM 完成，不能用规则脚本替代。规则脚本不理解语义，会破坏路由精度。

- **summary 填充** — 通读每个章节内容，用一句话概括该节主题
- **keywords 提取** — 提取该章节的关键术语、表格字段名、mermaid 节点名、API 名等可路由词
- **domain 推断** — 从一级目录或文档语义判断所属领域
- **title 获取** — 优先从 H1 提取，无 H1 时由 LLM 判断（文件名或内容主题）

## 脚本可做的部分

> **确定性子任务**可由脚本辅助，LLM 也可自行实现等价逻辑。脚本仅作为可选工具，不强制使用。

- **tree.json 骨架生成** — 解析 Markdown `#`~`######` 标题层级，确定节点 id/level/title/start_line/end_line/children
- **manifest.json 重算** — 扫描所有 `metadata.yaml`，聚合顶层 summary 和全部 keywords 生成全局路由表
- **source_sha256 计算** — 用于检测源文件变更，判断是否需要重建 tree.json

## 边界

- **仅 Markdown 输入** — PDF/Word/HTML 转换由客户自行处理
- **不做向量/Chunk/图谱** — 这是 kb-pilot 的核心边界，违反即偏离设计
- **不往用户目录放元数据** — 所有元数据在 `.kb/` 下
- **不在应用层加锁** — 多人协作冲突由 Git merge 解决
- **不物理分片** — 单库超过认知边界（几百篇）时按团队/领域拆分 Git 仓库
- **{kb_path} 占位符** — 执行时替换为实际知识库路径，默认 `knowledge_repo`
