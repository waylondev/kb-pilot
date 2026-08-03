---
name: kb-chat
description: >-
  Use this skill when the user asks a question that should be answered from the knowledge base,
  or wants to compare/cross-reference content across documents in the knowledge base. Triggers on
  any question about ingested content, even when the user doesn't mention "kb-pilot", "knowledge base",
  or ".kb" — if the question is about documents that have been ingested via kb-ingest, use this skill.
  Also handles corrections: when the user says "不对", "应该是", "纠正", persist the correction.
config:
  repo_url: ""
  kb_path: knowledge_repo
---

# kb-chat — 像人一样翻书回答

> **LLM 是路由引擎，不是 keyword 匹配器**。给 LLM 一本有目录的完整书，它能精准定位、阅读、回答。所有答案必须有原文依据，找不到就说"文档中未提及"。

## 知识库契约

（与 kb-ingest 共享，此处只列问答侧需要读取的部分）

- `.kb/manifest.json` — 全局路由表，每条含 doc_id、title、domain、summary、tags、**path**（源文件相对仓库根的路径）
- `.kb/index/{path 去掉 .md}/tree.json` — 章节目录树，节点含 id、level、title、summary、keywords、start_line、end_line、children
- `.kb/memory/corrections/{doc_id}.jsonl` — 纠错记录
- `.kb/memory/route_preferences.json` — 路由偏好

**路径计算**：manifest 条目 `path: docs/api/auth.md` → 元数据目录 `.kb/index/docs/api/auth/` → tree.json 在该目录下；源文件在 `{kb_path}/docs/api/auth.md`。

## 问答流程

像人翻书：先查目录定位章节，再读原文回答，标注出处。6 步是认知流程，LLM 根据问题难度自主决定每步深入程度。

1. **路由偏好** — 读 `.kb/memory/route_preferences.json`（如存在），作为路由弱先验。仅采纳用户明确表达的偏好，不从对话历史推断
2. **文档路由** — 读 `.kb/manifest.json`，通过 domain/title/summary/tags 的**语义匹配**定位最相关文档
   - Top 1 明显优于其他 → 直接选定
   - 多个文档难以区分 → 列出候选让用户选择，不要猜测
3. **章节定位** — 读命中文档的 `tree.json`，通过节点 title/summary/keywords 的**语义匹配**定位最精确章节，递归深入 children 直到足够具体
4. **内容截取** — 按命中章节的 start_line/end_line 从源文件读对应行范围
   - 答案可能跨节点时，自主扩大读取范围（前后节点或相邻行）
   - 子节点信息不足时，回退读父节点范围获取更完整上下文
   - 明确记录读取的行号范围，用于答案溯源
5. **纠错加载** — 读 `.kb/memory/corrections/{doc_id}.jsonl`（如有），附加到上下文。LLM 自行判断相关性：
   - 重复记录（相同 correct_answer）= 多人共识，提升可信度，不去重
   - conflicted 状态 = 答案冲突，并列展示所有版本，不自行裁决
6. **生成答案** — 基于截取原文生成答案：
   - 直接回答，先结论再展开
   - **必须标注引用来源**：doc_id、ch_id、文件路径、行号
   - 纠错与原文矛盾时，说明"原文为 X，纠错记录为 Y"
   - 文档无相关信息时，明确说"文档中未提及"
   - 用户明确表达领域偏好时，写入 route_preferences.json

## 跨文档对比

分别对每个文档独立执行流程 Step 2-4，生成对比答案，标注各自来源。不要混用路由和定位结果。

## 模糊提问处理

无法定位文档时，列出 Top 2-3 候选（标题 + 摘要）让用户选择，不要猜测。

## 纠错触发

当用户说"不对"、"应该是"、"纠正"时：

1. 定位当前问题的 doc_id 和 ch_id
2. 追加记录到 `.kb/memory/corrections/{doc_id}.jsonl`：
   ```json
   {"question": "问题", "correct_answer": "用户纠正的答案", "ch_id": "ch_x", "session_id": "xxx", "timestamp": "ISO时间", "status": "active"}
   ```
3. 不同用户对同一问题给出不同答案时，status 标记为 conflicted
4. 提交 Git：`git add .kb/memory/ && git commit && git push`

## Gotchas

- **不凭训练数据编造** — 找不到就说"文档中未提及"，禁止凭模型记忆回答
- **不做 keyword 硬匹配** — 路由靠语义理解 title/summary/keywords，不靠词频/字面匹配
- **纠错冲突**：conflicted 状态必须展示所有版本，不能自行裁决
- **纠错重复**：不同 session_id 的相同答案是共识信号，不要去重
- **跨文档对比**：各文档分别独立执行路由和定位，不要混用
- **路由偏好**：仅存储用户明确表达的偏好，不要从对话历史中推断
- **path 字段是关键**：manifest 条目的 path 是源文件相对仓库根的路径，据此读取原文；tree.json 在 `.kb/index/` 镜像目录下
- **大规模知识库**：单库超过几百篇文档时，按认知边界拆分 Git 仓库，不做物理分片
- **{kb_path} 占位符**：执行时替换为实际知识库路径，默认 `knowledge_repo`

## 边界

- **不凭训练数据编造** — 答案必须有原文依据
- **不做 keyword 硬匹配** — 路由靠语义理解
- **不自行裁决冲突** — conflicted 纠错必须并列展示
- **不物理分片** — 超规模时拆分 Git 仓库
