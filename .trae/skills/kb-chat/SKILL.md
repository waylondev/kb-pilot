---
name: kb-chat
description: 基于知识库的问答。LLM 自主驱动 6 步：路由偏好→文档路由→章节定位→内容截取→纠错加载→生成答案。用户提问知识库内容时使用。
config:
  repo_url: ""
  kb_path: knowledge_repo
---

# kb-chat — 像人一样翻书回答

> **LLM 是路由引擎，不是 keyword 匹配器**。给 LLM 一本有目录的完整书，它能精准定位、阅读、回答。

## 设计哲学

| 原则 | 含义 |
|------|------|
| **LLM 是路由引擎** | 通过语义理解 title/summary/keywords 定位文档和章节，不做 keyword 硬匹配 |
| **完整上下文** | 读取原文行范围而非 Chunk，避免断章取义 |
| **行级溯源** | 答案必须标注原文出处（文件路径 + 行号），可追溯可验证 |
| **有据可依** | 答案必须有原文依据，找不到就说"文档中未提及"，禁止凭训练数据编造 |
| **对话即纠错** | 用户纠正自动持久化为 jsonl，重复答案=共识，冲突并列展示 |
| **Git 即真理** | 纠错记录提交 Git，跨会话/跨用户可累积，冲突由 Git merge 解决 |

## 知识库契约

（与 kb-ingest 共享同一契约，此处只列问答侧需要读取的部分）

- `.kb/manifest.json` — 全局路由表，每条含 doc_id、title、domain、summary、tags、**path**（源文件相对仓库根的路径）
- `.kb/index/{path 去掉 .md}/tree.json` — 章节目录树，节点含 id、level、title、summary、keywords、start_line、end_line、children
- `.kb/memory/corrections/{doc_id}.jsonl` — 纠错记录
- `.kb/memory/route_preferences.json` — 路由偏好

**路径计算**：manifest 条目 `path: docs/api/auth.md` → 元数据目录 `.kb/index/docs/api/auth/` → tree.json 在该目录下；源文件在 `{kb_path}/docs/api/auth.md`。

## 问答意图

当用户提问知识库内容时，目标是**像人翻书一样：先查目录定位章节，再读原文回答，并标注出处**。以下 6 步是认知流程，不是机械步骤——LLM 应根据问题难度自主决定每步的深入程度：

### 1. 路由偏好
读取用户历史表达的领域偏好（如有），作为路由的弱先验。仅采纳用户明确表达的偏好，不从对话历史中推断。

### 2. 文档路由
读取 manifest.json，通过 domain/title/summary/tags 的**语义匹配**定位最相关的文档。
- Top 1 明显优于其他 → 直接选定
- 多个文档难以区分 → 列出候选让用户选择，不要猜测

### 3. 章节定位
读取命中文档的 tree.json，通过节点 title/summary/keywords 的**语义匹配**定位到最精确的章节。递归深入 children 直到足够具体。

### 4. 内容截取
按命中章节的 start_line/end_line 从源文件读取对应行范围。
- 答案可能跨节点时，自主扩大读取范围（前后节点或相邻行）
- 子节点信息不足时，回退读父节点范围获取更完整上下文
- 明确记录读取的行号范围，用于答案溯源

### 5. 纠错加载
读取该文档的 corrections jsonl（如有），附加到上下文。LLM 自行判断相关性：
- 重复记录（相同 correct_answer）= 多人共识，提升可信度，不去重
- conflicted 状态 = 答案冲突，并列展示所有版本，不自行裁决

### 6. 生成答案
基于截取的原文生成答案：
- 直接回答，先结论再展开
- **必须标注引用来源**：doc_id、ch_id、文件路径、行号
- 纠错与原文矛盾时，说明"原文为 X，纠错记录为 Y"
- 文档无相关信息时，明确说"文档中未提及"
- 用户明确表达领域偏好时，写入 route_preferences.json

## LLM 不可替代的部分

> **核心约束**：以下必须由 LLM 完成，不能用规则脚本替代。

- **文档路由判断** — 语义理解 manifest 条目，判断与问题的相关性
- **章节定位判断** — 语义理解 tree 节点，判断与问题的相关性
- **相关性判断** — 纠错记录是否适用于当前问题
- **答案生成** — 基于原文推理，而非复制片段
- **何时扩大读取范围** — 根据问题复杂度自主决定

## 对话即纠错

当用户说"不对"、"应该是"、"纠正"时：
1. 定位当前问题的 doc_id 和 ch_id
2. 追加记录到 `.kb/memory/corrections/{doc_id}.jsonl`，含 question、correct_answer、ch_id、session_id、timestamp、status
3. 不同用户对同一问题给出不同答案时，status 标记为 conflicted
4. 提交 Git

## 边界

- **不凭训练数据编造** — 找不到就说"文档中未提及"
- **不做 keyword 硬匹配** — 路由靠语义理解，不靠词频/字面匹配
- **不自行裁决冲突** — conflicted 纠错必须并列展示
- **不物理分片** — 单库超过认知边界时按团队/领域拆分 Git 仓库
- **{kb_path} 占位符** — 执行时替换为实际知识库路径，默认 `knowledge_repo`
