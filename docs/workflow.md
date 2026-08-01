# 执行流程

## 全链路总览

```mermaid
flowchart TD
    subgraph INGEST["Phase 1: kb-ingest（文档入库）"]
        direction TB
        S1["Step 1-2<br/>接收输入 + 准备知识库"]
        S2["Step 3<br/>放置 source.md"]
        S3["Step 4<br/>创建 metadata.yaml"]
        S4["Step 5<br/>build_tree.py 生成骨架"]
        S5["Step 6<br/>LLM 填充 summary + keywords"]
        S6["Step 7<br/>build_manifest.py 更新路由表"]
        S7["Step 8-9<br/>Git 提交 + 确认"]
        S1 --> S2 --> S3 --> S4 --> S5 --> S6 --> S7
    end

    S7 -.->|"知识库就绪"| CHAT

    subgraph CHAT["Phase 2: kb-chat（知识问答）"]
        direction TB
        C0["Step 0<br/>git pull 同步"]
        C1["Step 1<br/>领域路由<br/>route_preferences.json"]
        C2["Step 2<br/>文档路由<br/>manifest.json"]
        C3["Step 3<br/>章节定位<br/>tree.json"]
        C4["Step 4<br/>内容截取<br/>source.md"]
        C5["Step 5<br/>纠错加载<br/>corrections/"]
        C6["Step 6<br/>生成答案<br/>答案 + 依据 + 置信度"]
        C0 --> C1 --> C2 --> C3 --> C4 --> C5 --> C6
    end
```

---

## Phase 1: 文档入库（kb-ingest）

### 流程详解

```mermaid
sequenceDiagram
    actor User as 用户
    participant LLM as LLM
    participant Script as 脚本
    participant FS as 文件系统

    User->>LLM: 接入文档 {path}
    LLM->>FS: 创建 docs/{domain}/{doc_id}_{简称}/
    LLM->>FS: 复制 source.md
    LLM->>FS: 创建 metadata.yaml
    LLM->>Script: 调用 build_tree.py
    Script->>FS: 读取 source.md
    Script->>FS: 生成 tree.json 骨架
    Script-->>LLM: 骨架就绪
    LLM->>FS: 读取 source.md + tree.json
    LLM->>LLM: 为每个节点生成 summary + keywords
    LLM->>FS: 写入 tree.json
    LLM->>Script: 调用 build_manifest.py
    Script->>FS: 扫描 docs/ 目录
    Script->>FS: 生成 manifest.json
    Script-->>LLM: 路由表更新完成
    LLM->>FS: git add + commit + push
    LLM-->>User: doc_id + 节点数 + 路径
```

### 脚本 vs LLM 分工

| 步骤 | 执行者 | 原因 |
|------|--------|------|
| Step 5: 生成 tree.json 骨架 | `build_tree.py` | 确定性操作，解析 Markdown 标题 |
| Step 6: 填充 summary/keywords | LLM | 语义理解，脚本无法替代 |
| Step 7: 生成 manifest.json | `build_manifest.py` | 确定性操作，扫描文件系统 |

---

## Phase 2: 知识问答（kb-chat）

### 6 步流程详解

```mermaid
flowchart LR
    subgraph 路由["确定性路由"]
        C1["Step 1<br/>领域路由"]
        C2["Step 2<br/>文档路由"]
    end

    subgraph 定位["精确定位"]
        C3["Step 3<br/>章节定位"]
        C4["Step 4<br/>内容截取"]
    end

    subgraph 增强["上下文增强"]
        C5["Step 5<br/>纠错加载"]
    end

    subgraph 输出["输出"]
        C6["Step 6<br/>生成答案"]
    end

    C1 --> C2 --> C3 --> C4 --> C5 --> C6
```

### 具体示例：以"量子力学核心概念"为例

```mermaid
sequenceDiagram
    actor User as 用户
    participant LLM as LLM
    participant FS as 文件系统

    User->>LLM: 量子力学有哪些核心概念？

    Note over LLM,FS: Step 1: 领域路由
    LLM->>FS: 读取 route_preferences.json
    LLM->>LLM: 关键词"量子力学" → 物理领域

    Note over LLM,FS: Step 2: 文档路由
    LLM->>FS: 读取 manifest.json
    LLM->>LLM: title 匹配 → doc_106 "量子力学基础"

    Note over LLM,FS: Step 3: 章节定位
    LLM->>FS: 读取 docs/30_物理/doc_106_量子力学基础/tree.json
    LLM->>LLM: keywords 匹配 → ch_1_1 "量子力学核心概念"

    Note over LLM,FS: Step 4: 内容截取
    LLM->>FS: 读取 source.md lines 5-14
    FS-->>LLM: 波粒二象性、不确定性原理、量子叠加、量子纠缠、量子隧穿

    Note over LLM,FS: Step 5: 纠错加载
    LLM->>FS: 读取 corrections/doc_106.jsonl
    FS-->>LLM: 无纠错记录

    Note over LLM,FS: Step 6: 生成答案
    LLM-->>User: 5 大概念：...[详细答案]<br/>依据：source.md#L5-L14<br/>置信度：高
```

---

## 特殊流程

### 纠错流程

```mermaid
flowchart TD
    U["用户: 不对，应该是..."] --> C["检查 corrections/{doc_id}.jsonl"]
    C -->|"无相似记录"| A["追加 active<br/>用新答案回答"]
    C -->|"有记录且答案相同"| SKIP["跳过"]
    C -->|"有记录且答案不同"| CF["追加 conflicted<br/>展示所有版本"]
```

### 跨文档对比流程

```mermaid
flowchart TD
    Q["用户: 比较 A 和 B"] --> SPLIT["LLM 识别两个目标文档"]
    SPLIT --> DA["对文档 A 执行 Step 1-6"]
    SPLIT --> DB["对文档 B 执行 Step 1-6"]
    DA --> MERGE["并列展示<br/>生成对比分析"]
    DB --> MERGE
    MERGE --> OUT["答案 + 多文档依据 + 置信度"]
```

### 模糊匹配流程

```mermaid
flowchart TD
    Q["用户问题"] --> M["manifest.json<br/>title → summary → tags 匹配"]
    M -->|"唯一匹配"| SINGLE["直接定位"]
    M -->|"多个候选"| TOP2["返回 Top 2<br/>用户确认"]
    TOP2 --> SINGLE
```

---

## 数据依赖关系

```mermaid
flowchart LR
    S["source.md"] --> BT["build_tree.py"]
    S --> META["metadata.yaml"]
    BT --> T_SKEL["tree.json 骨架"]
    T_SKEL --> LLM["LLM 填充"]
    LLM --> T_FULL["tree.json<br/>含 summary + keywords"]
    METADATA --> BM["build_manifest.py"]
    T_FULL --> BM
    BM --> MF["manifest.json"]
    MF --> CHAT["kb-chat"]
    T_FULL --> CHAT
    S --> CHAT
```

---

## 关键约束

- **脚本只做确定性操作**：`build_tree.py` 和 `build_manifest.py` 是仅有的两个脚本，其余全部由 LLM 执行
- **纠错按 doc_id 隔离**：不同文档的纠错互不影响
- **偏好仅存储显式表达**：不从对话历史推断用户偏好
- **每次回答必须引用行号**：`source.md#L{start}-L{end}`