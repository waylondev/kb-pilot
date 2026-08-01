# kb-ingest SKILL

## 概述

将 Markdown 文档接入知识库系统。创建元数据，构建章节索引树，更新全局路由表。

> **设计边界**：kb-pilot 专注 Markdown 输入。PDF/Word/Excel/HTML 等格式的转换由客户自行处理，本 SKILL 不负责格式转换。

## 配置

```yaml
config:
  repo_url: ""          # Git 仓库地址（可选）
  kb_path: knowledge_repo  # 本地知识库路径（可配置默认值）
```

## 执行流程

```
Step 1: 接收用户输入
  ├── Markdown 文档路径
  ├── 所属领域
  ├── 文档简称
  └── 维护人
    │
    ▼
Step 2: 准备知识库
  ├── 不存在 → git clone {repo_url} {kb_path}
  └── 已存在 → git pull 同步
    │
    ▼
Step 3: 放置文档
  ├── 直接使用用户提供的 Markdown 文件（约定命名为 source.md，文件名不限）
  └── 检查 Markdown 结构：标题层级、表格/代码块正确性
    │
    ▼
Step 4: 创建 metadata.yaml
  ├── doc_id 序号：遍历 docs/ 取最大序号+1
  └── 字段：doc_id, title, domain, maintainer, source_format, converted_at, conversion_quality, manual_edit
    │
    ▼
Step 5: 构建 tree.json 骨架
  ├── 运行 build_tree.py 脚本（传入文档文件名，脚本不依赖文件名）
  └── 生成骨架：id, level, title, anchor, start_line, end_line, children
    │
    ▼
Step 6: 填充 summary 和 keywords （LLM 执行）
  ├── 读取文档原文和 tree.json 骨架
  ├── LLM 为每个节点生成 summary（≤20字）和 keywords（3-8个）
  └── 将填充结果写入 tree.json
    │
    ▼
Step 7: 更新 manifest.json
  └── 运行 build_manifest.py 脚本
    │
    ▼
Step 8: 提交到 Git
  └── git add + commit + push
    │
    ▼
Step 9: 确认完成
  └── 告知用户 doc_id、文档路径、节点数
```

## 关键步骤详解

### Step 5: build_tree.py

单遍扫描 Markdown 文件，遇 `#` 标题即创建节点，累积行号。纯正则解析，确定性输出，不调用 LLM。**文件名不限**，脚本接受任意路径参数。

输入：Markdown 文件路径
输出：`tree.json`（骨架，summary 和 keywords 为空）

### Step 6: LLM 填充语义信息

这是唯一需要 LLM 参与的步骤。LLM 逐节点读取文档对应行内容，生成：
- **summary**：章节摘要，≤20 字，概括该章节核心内容
- **keywords**：3-8 个关键词，用于后续问答时的章节匹配

### Step 7: build_manifest.py

扫描 `docs/` 下所有 `metadata.yaml` 和 `tree.json`，自动生成 `manifest.json`。不人工维护。

## 质量检查

- 检查文档标题层级完整性（#、##、###）
- tree.json 节点数合理范围：10-30 个节点
- 标题层级缺失时，提示用户完善 Markdown 结构后重新入库

## 文档重建

文档大幅修改时，从 Step 5 重新执行（覆盖已有 tree.json）。注意：重建会覆盖已填充的 summary 和 keywords，需重新执行 Step 6。

## 常见陷阱

- **doc_id 序号**：必须遍历 docs/ 目录确认最大序号，不能依赖记忆
- **标题层级**：文档必须有完整的标题层级，这是 tree.json 构建的基础
- **tree.json 覆盖**：重建会丢失 summary 和 keywords
- **manifest.json**：必须用脚本生成，不要手动编辑