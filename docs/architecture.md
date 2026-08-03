# kb-pilot 架构设计

## 设计哲学

**目录 + 原文 = 知识库**

LLM 足够聪明，你不需要把书切碎、向量化、建图谱。你只需要给它一本有目录的完整书，它就能精准定位、阅读、回答。

### 核心原则

| 原则 | 说明 |
|------|------|
| LLM 是路由引擎 | 语义理解 title/summary/keywords，不是 keyword 匹配 |
| 零侵入 | 用户原文留在原位，元数据集中在 `.kb/`，删除即卸载 |
| 确定性 | tree.json 是脚本确定性生成，不依赖概率模型 |
| 完整上下文 | 读取原文片段而非 Chunk，避免断章取义 |
| Git 原生 | 所有元数据是文本文件，版本管理、协作、同步都靠 Git |
| 少即是多 | 不做向量、不做图谱、不做分片、不做加权 |

### 不做什么

- ❌ 不做 PDF/Word/HTML → Markdown 转换（客户自行处理）
- ❌ 不做 Embedding 向量检索
- ❌ 不做 Chunk 切分
- ❌ 不做知识图谱/实体关系
- ❌ 不在应用层做并发锁（Git 解决）
- ❌ 不做 manifest 分片（超过规模就分仓库）
- ❌ 不往用户目录放元数据文件（全部在 `.kb/`）

---

## 核心组件

```
┌─────────────────────────────────────────────┐
│                Git 仓库                      │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ .kb/          元数据（集中存放）      │    │
│  │  ├── manifest.json   全局路由表      │    │
│  │  ├── memory/         纠错+偏好       │    │
│  │  └── index/          镜像目录树      │    │
│  │      └── docs/api/auth/             │    │
│  │          ├── metadata.yaml          │    │
│  │          └── tree.json              │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ 用户文档（任意结构，不动）            │    │
│  │  └── docs/api/auth.md              │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

### manifest.json — 全局路由表

全局文档索引，每条记录代表一个文档：

```json
{
  "doc_id": "doc_001",
  "title": "API 认证接口",
  "domain": "api",
  "summary": "OAuth2认证流程;Token有效期管理;权限分级",
  "tags": ["OAuth2", "JWT", "Token", "认证", "权限"],
  "updated_at": "2026-08-02",
  "path": "docs/api/auth.md"
}
```

- `path`：源文件相对仓库根的路径（**关键**，kb-chat 据此定位原文）
- `summary`：从 tree.json 顶层节点 summary 自动拼接（前 3 个，分号连接）
- `tags`：从 tree.json 所有节点 keywords 自动收集
- 由 `build_manifest.py` 脚本自动生成，不人工维护

### metadata.yaml — 文档元数据

每个 Markdown 文件对应一份，存放在 `.kb/index/` 镜像路径下：

```yaml
doc_id: doc_001
title: "API 认证接口"
domain: api
source_path: docs/api/auth.md
source_format: markdown
ingested_at: "2026-08-02"
```

- `source_path`：源文件相对于仓库根的路径
- `domain`：领域分类，从一级目录推断或用户指定

### tree.json — 章节目录

每个 Markdown 文件的章节索引树，存放在 `.kb/index/` 镜像路径下：

```json
{
  "doc_id": "doc_001",
  "title": "API 认证接口",
  "source_sha256": "abc123...",
  "total_lines": 256,
  "nodes": [
    {
      "id": "ch_1",
      "level": 2,
      "title": "OAuth2 认证流程",
      "summary": "授权码模式完整流程",
      "keywords": ["OAuth2", "授权码", "access_token"],
      "start_line": 15,
      "end_line": 48,
      "children": [...]
    }
  ]
}
```

- 骨架由 `build_tree.py` 脚本确定性生成（解析 Markdown 标题层级）
- `summary` 和 `keywords` 由 LLM 填充
- `source_sha256`：源文件哈希，用于检测变更
- 节点数上限 50，超过时自动展平所有子节点（保留顶层结构，丢弃嵌套层级）

### corrections/ — 纠错记录

对话中用户纠正的答案，以 jsonl 格式按 doc_id 存储：

```json
{"question": "Token有效期", "correct_answer": "2小时", "ch_id": "ch_2", "session_id": "xxx", "timestamp": "2026-08-02T10:00:00", "status": "active"}
```

- 重复记录 = 多人共识，不去重
- conflicted = 多人答案冲突，并列展示
- 并发冲突由 Git merge 解决

---

## 目录结构

### 路径映射规则

源文件路径 → 元数据目录：把 `/` 当目录层级，去掉 `.md` 后缀。

| 源文件路径 | 元数据目录 |
|---|---|
| `docs/api/auth.md` | `.kb/index/docs/api/auth/` |
| `specs/architecture.md` | `.kb/index/specs/architecture/` |
| `README.md` | `.kb/index/README/` |

### 完整结构

```
{repo_root}/
├── .kb/
│   ├── manifest.json               # 全局路由表（脚本生成）
│   ├── memory/
│   │   ├── corrections/            # {doc_id}.jsonl
│   │   └── route_preferences.json
│   └── index/
│       └── docs/
│           └── api/
│               └── auth/
│                   ├── metadata.yaml
│                   └── tree.json
├── docs/                           # 用户文档（任意结构）
│   └── api/
│       └── auth.md
├── specs/
│   └── architecture.md
└── README.md
```

---

## 两个 SKILL

### kb-ingest：文档入库

1. 接收源文件路径和 domain
2. 在 `.kb/index/` 镜像路径创建 metadata.yaml
3. 运行 build_tree.py 生成 tree.json 骨架（输出到镜像路径）
4. LLM 逐节点填充 summary 和 keywords（不可用规则脚本替代）
5. 运行 build_manifest.py 更新 `.kb/manifest.json`
6. Git commit + push

文档大幅修改时，通过 `source_sha256` 漂移检测判断是否需要重建 tree.json。

### kb-chat：知识问答

1. 读 `.kb/memory/route_preferences.json`
2. 读 `.kb/manifest.json` → 语义匹配定位 doc_id
3. 读 `.kb/index/.../tree.json` → 语义匹配定位 ch_id
4. 按 manifest path 读源文件行范围
5. 读 `.kb/memory/corrections/{doc_id}.jsonl`
6. 生成答案 + 标注行号引用

---

## 与传统 RAG 的本质区别

| 维度 | 传统 RAG | kb-pilot |
|------|---------|---------|
| 检索模型 | 向量相似度（概率） | LLM 语义路由（认知） |
| 上下文单位 | Chunk（几百 token 碎片） | 章节（完整语义单元） |
| 答案精度 | "某个附近" | 文件路径 + 行号 |
| 基础设施 | GPU + 向量库 | 文件系统 |
| 部署成本 | 高 | 零 |
| 纠错 | 需重建索引 | 对话即纠错 |
| 用户目录 | 需迁移重组 | 零侵入 |
| 协作 | 需同步服务状态 | Git 原生 |
