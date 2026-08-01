# kb-pilot

基于**结构化树索引（Tree Index）** 的知识库问答系统。不依赖向量检索、不切分文档，通过章节索引树精确定位原文内容，实现确定性、可追溯、可纠错的知识问答。

## 为什么选择 kb-pilot？

传统 RAG 的三大痛点：Chunk 切分导致上下文断裂、向量检索结果不可控、答案错误无法修正。kb-pilot 从根本解决这些问题：

| 痛点 | 传统 RAG | kb-pilot |
|------|---------|----------|
| 上下文断裂 | 固定大小 Chunk 切分，语义被截断 | 完整章节读取，零切分 |
| 检索黑盒 | 向量相似度，结果不可解释 | 树索引关键词匹配，确定性可复现 |
| 答案错误 | 无法修正，只能重跑 | 对话式纠错，持久化记忆 |

## 核心创新

- **树索引替代向量检索**：不依赖 Embedding 模型，用 tree.json 章节索引树实现确定性定位，路由结果可复现
- **完整上下文不切分**：直接读取 source.md 原文段落，保持文档完整语义，杜绝上下文断裂
- **对话式纠错记忆**：用户纠正答案后自动持久化为 JSONL 纠错记录，active/conflicted 状态管理，让知识库越用越准
- **路由偏好记忆**：用户表达"主要关注 X 领域"后自动更新 route_preferences.json，后续问答自动优先匹配
- **脚本骨架 + LLM 语义**：build_tree.py 生成确定性结构骨架，LLM 仅填充 summary 和 keywords，检索可控、语义可扩展
- **行级精确引用**：每次回答精确到 `source.md#L{行号}`，可审计、可追溯、可复现
- **Git 原生协作**：知识库基于 Git 版本控制，支持多人协作编辑、变更追溯、版本回滚
- **零部署成本**：纯文件系统 + Markdown，无需向量数据库、Embedding 模型、GPU 资源
- **跨 Agent 兼容**：SKILL 文件遵循 Agent Skills 标准，支持 Trae、Copilot、Codex 等多种 Agent

## 快速开始

### 前置要求

- Python 3.8+
- Git
- PyYAML（`pip install pyyaml`）

### 1. 接入文档

```
Use Skill: kb-ingest 将 {文档路径} 接入知识库
```

### 2. 知识问答

```
Use Skill: kb-chat DeepSeek V3 的参数量是多少？
```

**答案**：DeepSeek V3 总参数量 671B (MoE)，激活 37B
**依据**：source.md#L16-L16（模型参数概览）
**置信度**：高

### 3. 纠错纠正

当知识库原文存在过时或错误信息时，直接对话纠正：

```
User: 不对，DeepSeek V3 输入价格应该是 $0.14，不是 $0.27
```

系统自动检查已有纠错记录，追加为 active 状态，后续相同问题会优先使用纠正后的答案。

### 4. 路由偏好

表达领域偏好，后续问答自动优先检索：

```
User: 我以后主要问技术领域的问题
```

系统更新 `route_preferences.json`，后续问答优先匹配技术领域。

### 5. 知识同步

```
Use Skill: kb-chat 同步一下知识库
```

## 项目结构

```
kb-pilot/
├── .trae/skills/               # Agent SKILL 定义
│   ├── kb-ingest/
│   │   ├── SKILL.md            # 文档接入 SKILL
│   │   └── scripts/
│   │       ├── build_tree.py   # 章节索引树生成器
│   │       └── build_manifest.py # 全局路由表生成器
│   └── kb-chat/
│       └── SKILL.md            # 知识问答 SKILL
├── docs/                       # 项目文档
│   ├── architecture.md         # 系统架构（含纠错/记忆系统详解）
│   ├── workflow.md             # 执行流程
│   ├── testing.md              # 测试方法
│   ├── e2e-test-results.md     # E2E 测试结果
│   ├── rag-comparison.md       # 与主流 RAG 方案详细对比
│   └── skills/                 # SKILL 详解
│       ├── kb-ingest.md
│       └── kb-chat.md
└── knowledge_repo/             # 知识库数据（不纳入版本控制）
```

## 知识库结构

```
knowledge_repo/
├── manifest.json               # 全局路由表
├── memory/
│   ├── corrections/            # 纠错记录（JSONL）
│   │   └── {doc_id}.jsonl      # 按文档隔离的纠错记录
│   └── route_preferences.json  # 用户路由偏好
└── docs/
    └── {domain}/
        └── {doc_id}_{简称}/
            ├── source.md       # 原始文档
            ├── tree.json       # 章节索引树
            └── metadata.yaml   # 元数据
```

## 对比报告

详见 [docs/rag-comparison.md](docs/rag-comparison.md) — 与 Naive RAG、GraphRAG、LightRAG、LlamaIndex、FastGPT、Dify 等主流方案的架构对比。

## License

MIT