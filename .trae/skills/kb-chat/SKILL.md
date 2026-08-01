---
name: kb-chat
description: 基于结构化树索引（tree.json）和全文（Markdown 原文）的知识库问答。处理知识问答、自我纠错、跨文档对比、知识同步、路由偏好记忆。当用户询问知识库中的文档内容时使用。
config:
  repo_url: ""
  kb_path: knowledge_repo
---

## 核心流程

### 0. 准备知识库
- 若 `{kb_path}` 目录不存在，从 `repo_url` 克隆：`git clone {repo_url} {kb_path}`
- 若已存在，执行 `git pull` 同步最新内容
- 以下所有路径均相对于 `{kb_path}` 目录

### 1. 领域路由
- 读取 `memory/route_preferences.json` 检查用户偏好
- 结合用户问题关键词判断目标领域

### 2. 文档路由
- 读取 `manifest.json`，按 title → summary → tags 顺序匹配
- 返回 Top 2 候选文档
- 用户问题明确指向某文档时直接定位
- 匹配到多个候选时列出 Top 2 让用户确认

### 3. 章节定位
- 读取候选文档的 `docs/{domain}/{doc_id}/tree.json`，遍历 nodes
- 按 keywords 匹配用户问题关键词，取匹配数最多者
- 按 anchor 在 `docs/{domain}/{doc_id}/` 下的 Markdown 原文中精确定位

### 4. 内容截取
- 根据选中节点的 start_line 和 end_line 读取 `docs/{domain}/{doc_id}/` 下的 Markdown 原文
- 内容超过 2000 字时启用二次精确定位

### 5. 纠错加载
- 读取 `memory/corrections/{doc_id}.jsonl`（如存在）
- 将全部纠错记录附加到上下文，LLM 自行判断相关性

### 6. 生成答案
- 综合原文内容和纠错记录生成答案
- 包含答案、依据、置信度三段式输出

## 特殊意图处理

### 自我纠错
用户说"不对"/"应该是"/"纠正一下"等：
1. 确认要纠正的信息
2. 检查 `memory/corrections/{doc_id}.jsonl` 是否有相似纠错
3. 不存在 → 追加为 `active`；存在且答案不同 → 追加为 `conflicted`
4. 确认："已记录纠错：[原信息] → [新信息]"
5. 用纠错后信息重新回答

纠错记录格式：
```jsonl
{"timestamp":"ISO8601时间","question":"用户问题","correct_answer":"正确答案","doc_id":"文档ID","source_ref":"纠错来源","status":"active|conflicted"}
```

### 跨文档对比
用户说"对比"/"比较"/"区别"等，涉及两个以上文档/年份/版本：
1. 分别对每个目标文档执行步骤 2-5
2. 各文档内容并列展示
3. 生成对比分析，突出差异点

### 路由偏好
用户说"我以后主要问 X"/"我主要关注 X 领域"等：
1. 更新 `memory/route_preferences.json`，添加或更新 domain_preferences
2. 确认："已记录偏好：后续问题优先检索 {领域} 领域"

### 知识同步
用户说"同步一下"/"更新知识库"/"pull"等：
1. `cd {kb_path} && git pull`
2. 报告更新了哪些文档，无变更则告知"知识库已是最新"

## 回答格式模板

```
**答案**：[直接回答]

**依据**：docs/{domain}/{doc_dir}/{文件名}#L{start}-L{end}（{章节名}）

**置信度**：[高/中/低]（[原因说明]）
```

多文档对比时，每个文档单独列出依据。

## 重要约束

- 答案必须基于文档原文，不能凭空编造
- 知识库中找不到相关信息时，明确告知"知识库中未找到相关信息"
- 优先使用 active 状态的纠错记录
- 每次回答必须引用具体行号范围
- 不要提及 tree.json、manifest.json 等内部实现细节

## 常见陷阱（Gotchas）

- **用户表达模糊时**：不要自行猜测文档，使用 Top 2 候选让用户确认
- **纠错冲突处理**：conflicted 状态的纠错必须展示所有版本让用户选择，不能自行裁决
- **跨文档对比**：确保各文档分别独立执行路由和定位，不要混用
- **路由偏好**：仅存储用户明确表达的偏好，不要从对话历史中推断
- **{kb_path} 占位符**：执行时替换为实际知识库路径，默认为 `knowledge_repo`（可配置）