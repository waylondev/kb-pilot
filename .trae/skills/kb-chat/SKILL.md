---
name: kb-chat
description: 基于知识库的问答，严格按照 6 步流程：路由偏好→文档路由→章节定位→内容截取→纠错加载→生成答案。用户提问知识库内容时使用。
config:
  repo_url: ""
  kb_path: knowledge_repo
---

> **核心原则**：
> - LLM 是路由引擎，不是 keyword 匹配器。通过语义理解 title、summary、keywords 定位文档。
> - 所有答案必须有原文依据，禁止凭训练数据编造。找不到就说"文档中未提及"。
> - 源文件路径从 manifest 条目的 `path` 字段获取（相对于 {kb_path}），tree.json 在 `.kb/index/` 镜像目录下。

> **前置条件**：
> - Git（纠错记录提交需要）
> - 知识库已通过 kb-ingest 初始化（`.kb/manifest.json` 存在）

## 问答流程（6 步）

### 1. 路由偏好
- 读取 `{kb_path}/.kb/memory/route_preferences.json`（如存在）
- 提取用户明确表达的领域偏好

### 2. 文档路由
- 读取 `{kb_path}/.kb/manifest.json`

#### 小/中规模 manifest（≤ 50 条）
- 通过 domain → title → summary → tags 语义匹配，直接定位最相关的文档
- 输出 Top 2 候选文档：
  - 如果 Top 1 明显更相关（得分显著高于 Top 2），直接选 Top 1
  - 如果 Top 1 和 Top 2 难以区分，列出两个文档让用户选择

#### 大 manifest（超过 50 条）
分步过滤：domain 预过滤 → title 初筛 Top 5 → summary + tags 精筛 Top 2。无 domain 匹配时全量 title + summary 匹配。

### 3. 章节定位
- 根据 manifest 条目的 `path` 字段，计算元数据目录：
  - path 如 `docs/api/auth.md` → meta_dir = `.kb/index/docs/api/auth/`
  - 即：`.kb/index/` + path 去掉 `.md`
- 读取 `{kb_path}/{meta_dir}/tree.json`

#### 小/中规模 tree（≤ 30 节点）
- 通过节点 title/summary/keywords 语义匹配定位章节
- 递归遍历 children 直到最精确节点

#### 大 tree（超过 30 节点）
广度优先 + 逐层深入：先匹配第一层子节点取最相关，再深入 children。子节点匹配置信度低时回退父节点范围。

### 4. 内容截取
- 从 Step 2 命中的 manifest 条目 `path` 字段获取源文件路径：`{kb_path}/{path}`
- 按命中 ch_id 的 start_line/end_line 读取对应行范围
- 如果答案可能跨节点，扩大读取范围（包含前后节点或相邻行），但必须明确标注引用行号
- 如果子节点信息不足，可读父节点范围以获取更完整上下文
- 记录：读取的行号范围

### 5. 纠错加载
- 读取 `{kb_path}/.kb/memory/corrections/{doc_id}.jsonl`（如存在）
- 将纠错记录附加到上下文，LLM 自行判断相关性
- 重复记录（相同 correct_answer）= 共识信号，不去重，提升可信度
- conflicted 状态的纠错，并列展示所有版本，不自行裁决

### 6. 生成答案
- 基于截取的内容生成答案
- 答案格式要求：
  - 直接回答问题，先给结论再展开
  - **必须标注引用来源**：`{doc_id} {ch_id} {path}#L{start}-L{end}`
  - 如果有纠错且与原文矛盾，说明"原文为 X，纠错记录为 Y"
  - 如果文档中没有相关信息，明确说"文档中未提及"
- 更新路由偏好：如果用户明确表达了领域偏好，写入 `.kb/memory/route_preferences.json`

## 纠错触发

当用户说"不对"、"应该是"、"纠正"等时：

1. 定位当前问题的 doc_id 和 ch_id
2. 追加记录到 `{kb_path}/.kb/memory/corrections/{doc_id}.jsonl`
3. 记录格式：
```json
{"question": "问题", "correct_answer": "用户纠正的答案", "ch_id": "ch_x", "session_id": "xxx", "timestamp": "ISO时间", "status": "active"}
```
4. 不同用户对同一问题给出不同答案时，status 标记为 "conflicted"
5. 提交 Git：`git add .kb/memory/ && git commit && git push`

## 跨文档对比
分别对 X 和 Y 独立执行 Step 2-4，生成对比答案，标注两个文档来源。

## 模糊提问处理
无法定位文档时，列出 Top 2-3 候选（标题 + 摘要）让用户选择，不要猜测。

## 常见陷阱（Gotchas）

- **纠错冲突**：conflicted 状态必须展示所有版本，不能自行裁决
- **纠错重复**：不同 session_id 的相同答案是共识信号，不要去重
- **跨文档对比**：各文档分别独立执行路由和定位，不要混用
- **路由偏好**：仅存储用户明确表达的偏好，不要从对话历史中推断
- **大规模知识库**：单库超过几百篇文档时，按认知边界拆分 Git 仓库，不做物理分片
- **{kb_path} 占位符**：执行时替换为实际知识库路径，默认为 `knowledge_repo`
