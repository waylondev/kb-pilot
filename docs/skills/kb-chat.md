# kb-chat SKILL

## 概述

基于结构化树索引（tree.json）和全文（source.md）的知识库问答。处理知识问答、自我纠错、跨文档对比、知识同步、路由偏好记忆。

## 配置

```yaml
config:
  repo_url: ""          # Git 仓库地址（可选）
  kb_path: knowledge_repo  # 本地知识库路径
```

## 核心流程（6 步法）

```
Step 0: 准备知识库
  ├── 不存在 → git clone
  └── 已存在 → git pull 同步
    │
    ▼
Step 1: 领域路由
  ├── 读取 memory/route_preferences.json
  └── 结合问题关键词判断目标领域
    │
    ▼
Step 2: 文档路由
  ├── 读取 manifest.json
  ├── 按 title → summary → tags 顺序匹配
  ├── 返回 Top 2 候选
  └── 模糊时让用户确认
    │
    ▼
Step 3: 章节定位
  ├── 读取 tree.json，遍历 nodes
  ├── 按 keywords 匹配问题关键词
  └── 取匹配数最多的节点
    │
    ▼
Step 4: 内容截取
  ├── 按 start_line / end_line 读取 source.md
  └── 超过 2000 字时二次精确定位
    │
    ▼
Step 5: 纠错加载
  └── 读取 memory/corrections/{doc_id}.jsonl
    │
    ▼
Step 6: 生成答案
  └── 答案 + 依据（行号） + 置信度
```

## 各步骤详解

### Step 1: 领域路由

从用户问题中提取关键词，结合 `route_preferences.json` 中的用户偏好，判断目标领域。例如：
- "股票" → 金融
- "NBA" → 体育
- "专辑" → 音乐

### Step 2: 文档路由

在 `manifest.json` 中按三层匹配：
1. **title**：标题直接匹配
2. **summary**：摘要关键词匹配
3. **tags**：标签集合匹配

返回 Top 2 候选文档。用户问题明确指向某文档时直接定位。

### Step 3: 章节定位

在 `tree.json` 中遍历所有节点，将用户问题关键词与每个节点的 `keywords` 列表做匹配，取匹配数最多的节点。如果多个节点匹配数相同，取第一个。

### Step 4: 内容截取

根据选中节点的 `start_line` 和 `end_line`，从 `source.md` 中精确截取对应行。内容超过 2000 字时，启用二次定位（在截取范围内进一步搜索关键词）。

### Step 5: 纠错加载

读取 `memory/corrections/{doc_id}.jsonl`，将所有纠错记录附加到上下文。LLM 自行判断相关性：
- `active`：生效中的纠错，优先使用
- `conflicted`：存在冲突的纠错，展示所有版本

### Step 6: 生成答案

三段式输出：
- **答案**：直接回答
- **依据**：`source.md#L{start}-L{end}（章节名）`
- **置信度**：高/中/低 + 原因说明

## 特殊意图处理

### 自我纠错

用户指出答案错误时：
1. 确认纠错信息
2. 检查已有纠错记录
3. 追加新记录（active/conflicted）
4. 用纠错后信息重新回答

### 跨文档对比

用户要求对比多个文档时：
1. 分别对每个文档执行 Step 2-5
2. 并列展示各文档内容
3. 生成对比分析，突出差异

### 路由偏好

用户表达领域偏好时，更新 `memory/route_preferences.json`。

### 知识同步

用户要求同步知识库时，执行 `git pull` 并报告变更。

## 回答格式

```
**答案**：[直接回答]

**依据**：docs/{domain}/{doc_dir}/source.md#L{start}-L{end}（{章节名}）

**置信度**：[高/中/低]（[原因说明]）
```

## 重要约束

- 答案必须基于 source.md 原文，不能凭空编造
- 找不到相关信息时明确告知
- 每次回答必须引用具体行号范围
- 不向用户暴露 tree.json、manifest.json 等内部实现

## 常见陷阱

- **模糊表达**：使用 Top 2 候选让用户确认，不要自行猜测
- **纠错冲突**：conflicted 纠错展示所有版本，让用户选择
- **跨文档对比**：各文档独立路由和定位，不混用
- **路由偏好**：仅存储用户明确表达的偏好