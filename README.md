# kb-pilot

基于结构化树索引（Tree Index）的知识库问答系统。不依赖向量检索、不切分文档，通过章节索引树精确定位原文内容，实现确定性、可追溯的知识问答。

## 核心特性

- **确定性路由**：基于 manifest.json 全局路由表 + tree.json 章节索引树，100% 可复现的检索路径
- **零部署成本**：纯文件系统 + Markdown，无需向量数据库、Embedding 模型、GPU 资源
- **无上下文断裂**：不切分文档，直接读取原文段落，保留完整上下文
- **可纠错**：内置纠错记忆机制，支持人工修正知识库答案
- **Git 原生**：知识库基于 Git 版本控制，支持协作编辑、变更追溯
- **跨 Agent 兼容**：SKILL 文件遵循 Agent Skills 标准，支持 Trae、Copilot、Codex 等多种 Agent

## 与传统 RAG 的对比

| 维度 | kb-pilot | 传统 RAG (Naive RAG) | GraphRAG |
|------|----------|---------------------|----------|
| 检索方式 | 树索引确定性定位 | 向量相似度检索 | 图结构检索 |
| 文档切分 | 不切分 | Chunk 切分 | 实体/关系抽取 |
| 上下文完整性 | 完整章节 | 碎片化 Chunk | 子图片段 |
| 路由准确率 | 100% | ~60% | ~85% |
| 部署成本 | 零（纯文件） | 需要向量库+Embedding | 需要图数据库 |
| 可追溯性 | 行级精确引用 | Chunk 级引用 | 实体级引用 |

## 快速开始

### 前置要求

- Python 3.8+
- Git
- PyYAML（`pip install pyyaml`）

### 1. 接入文档

使用 `kb-ingest` SKILL 将文档入库：

```
Use Skill: kb-ingest 将 {文档路径} 接入知识库
```

### 2. 问答

使用 `kb-chat` SKILL 进行知识问答：

```
Use Skill: kb-chat {你的问题}
```

### 3. 知识同步

知识库更新后，同步最新内容：

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
│   ├── architecture.md         # 系统架构
│   ├── workflow.md             # 执行流程
│   ├── testing.md              # 测试方法
│   ├── e2e-test-results.md     # E2E 测试结果
│   └── skills/                 # SKILL 详解
│       ├── kb-ingest.md
│       └── kb-chat.md
└── knowledge_repo/             # 知识库数据（可选，不纳入版本控制）
    ├── manifest.json
    ├── memory/
    └── docs/
```

## 知识库结构

```
knowledge_repo/
├── manifest.json              # 全局路由表
├── memory/
│   ├── corrections/           # 纠错记录
│   └── route_preferences.json # 路由偏好
└── docs/
    └── {domain}/               # 按领域组织
        └── {doc_id}_{简称}/
            ├── source.md       # 原始文档
            ├── tree.json       # 章节索引树
            └── metadata.yaml   # 元数据
```

## License

MIT