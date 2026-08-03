---
name: kb-chat
description: >-
  Use when the user asks a question that should be answered from the knowledge base,
  or wants to compare/cross-reference content across documents. Triggers on any question
  about ingested content, even without "kb-pilot", "knowledge base", or ".kb" mention.
  Also handles corrections: when the user says "不对", "应该是", "纠正", persist the correction.
config:
  repo_url: ""
  kb_path: knowledge_repo
---

# kb-chat — 像人一样翻书回答

LLM 是路由引擎，不是 keyword 匹配器。通过语义理解 title/summary/keywords 定位文档和章节，读原文回答，标注出处。所有答案必须有原文依据，找不到就说"文档中未提及"。

路径计算：manifest 条目 `path: docs/api/auth.md` → tree.json 在 `.kb/index/docs/api/auth/`，源文件在 `{kb_path}/docs/api/auth.md`。

## 问答流程

像人翻书：先查目录定位章节，再读原文回答，标注出处。LLM 根据问题难度自主决定每步深入程度。

Progress:
- [ ] **1. 路由偏好** — 读 `.kb/memory/route_preferences.json`（如存在），作为路由弱先验。仅采纳用户明确表达的偏好，不从对话历史推断
- [ ] **2. 文档路由** — 读 `.kb/manifest.json`，通过 domain/title/summary/tags 的**语义匹配**定位最相关文档
  - Top 1 明显优于其他 → 直接选定
  - 多个文档难以区分 → 列出候选让用户选择，不要猜测
- [ ] **3. 章节定位** — 读命中文档的 `tree.json`，通过节点 title/summary/keywords 的**语义匹配**定位最精确章节，递归深入 children 直到足够具体
- [ ] **4. 内容截取** — 按命中章节的 start_line/end_line 从源文件读对应行范围
  - 答案可能跨节点时，自主扩大读取范围（前后节点或相邻行）
  - 子节点信息不足时，回退读父节点范围获取更完整上下文
  - 明确记录读取的行号范围，用于答案溯源
- [ ] **5. 纠错加载** — 读 `.kb/memory/corrections/{doc_id}.jsonl`（如有），附加到上下文。LLM 自行判断相关性：
  - 重复记录（相同 correct_answer）= 多人共识，提升可信度，不去重
  - conflicted 状态 = 答案冲突，并列展示所有版本，不自行裁决
- [ ] **6. 生成答案** — 基于截取原文生成答案，使用下方模板。用户明确表达领域偏好时，写入 route_preferences.json

## 答案格式模板

```markdown
[直接结论，一句话]

[展开说明，引用原文关键片段]

来源：{doc_id} {ch_id} {path}#L{start}-L{end}
```

- 纠错与原文矛盾时：说明"原文为 X，纠错记录为 Y"
- 文档无相关信息时：只说"文档中未提及"，不编造
- 跨文档对比时：分别标注两个文档来源

## 纠错流程

当用户说"不对"、"应该是"、"纠正"时：

- [ ] 1. 定位当前问题的 doc_id 和 ch_id
- [ ] 2. 追加记录到 `.kb/memory/corrections/{doc_id}.jsonl`：
  ```json
  {"question": "问题", "correct_answer": "用户纠正的答案", "ch_id": "ch_x", "session_id": "xxx", "timestamp": "ISO时间", "status": "active"}
  ```
- [ ] 3. 不同用户对同一问题给出不同答案时，status 标记为 conflicted
- [ ] 4. 提交 Git：`git add .kb/memory/ && git commit && git push`

## 跨文档对比

分别对每个文档独立执行问答流程 Step 2-4，生成对比答案，标注各自来源。不要混用路由和定位结果。

## 模糊提问

无法定位文档时，列出 Top 2-3 候选（标题 + 摘要）让用户选择，不要猜测。

## Gotchas

- **不凭训练数据编造** — 找不到就说"文档中未提及"，禁止凭模型记忆回答
- **不做 keyword 硬匹配** — 路由靠语义理解 title/summary/keywords，不靠词频/字面匹配
- **path 字段是关键** — manifest 条目的 path 是源文件相对仓库根的路径，据此读取原文；tree.json 在 `.kb/index/` 镜像目录下
- **纠错冲突**：conflicted 状态必须展示所有版本，不能自行裁决
- **纠错重复**：不同 session_id 的相同答案是共识信号，不要去重
- **跨文档对比**：各文档分别独立执行路由和定位，不要混用
- **路由偏好**：仅存储用户明确表达的偏好，不要从对话历史中推断
- **大规模知识库**：单库超过几百篇文档时，按认知边界拆分 Git 仓库，不做物理分片
- **{kb_path} 占位符**：执行时替换为实际知识库路径，默认 `knowledge_repo`
