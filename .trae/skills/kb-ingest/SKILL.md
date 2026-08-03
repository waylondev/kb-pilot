---
name: kb-ingest
description: 将 Markdown 文档接入知识库。不侵入用户目录，元数据统一存放在 .kb/ 下镜像目录结构。当用户提供 Markdown 文档需要入库时使用。
config:
  repo_url: ""
  kb_path: knowledge_repo
---

> **设计边界**：
> - 专注 Markdown 输入。PDF/Word/HTML 等格式转换由客户自行处理。
> - **不侵入用户目录**：原始 Markdown 留在原位，元数据（metadata.yaml、tree.json）统一存放在 `.kb/index/` 下镜像路径。
> - 删除知识库 = 删除 `.kb/` 目录，用户文件毫发无损。

> **前置条件**：
> - Python 3.10+
> - PyYAML（`pip install pyyaml`）
> - Git

## 知识库目录结构

知识库是一个 Git 仓库，克隆到本地 `{kb_path}` 目录。用户原始文档可以在仓库任意位置，`.kb/` 是 kb-pilot 的元数据目录：

```
{kb_path}/                          # Git 仓库根目录
├── .kb/                            # kb-pilot 元数据（集中存放）
│   ├── manifest.json               # 全局路由表（脚本生成）
│   ├── memory/
│   │   ├── corrections/            # 纠错记录（jsonl）
│   │   └── route_preferences.json  # 路由偏好
│   └── index/                      # 镜像目录结构
│       └── {原文件相对路径}/        # 镜像原文件路径，文件名去掉 .md
│           ├── metadata.yaml
│           └── tree.json
├── docs/                           # 用户原始文档（任意目录结构）
│   └── api/
│       ├── auth.md                 # 源文件不动
│       └── user.md
├── specs/
│   └── architecture.md
└── README.md
```

**路径映射规则**：源文件 `docs/api/auth.md` → 元数据目录 `.kb/index/docs/api/auth/`。即把文件路径中的 `/` 当目录层级，去掉 `.md` 后缀。

## 接入流程（检查清单）

- [ ] **Step 1: 接收用户输入**
  - Markdown 文档路径（相对于 `{kb_path}` 的相对路径，如 `docs/api/auth.md`）
  - 所属领域 domain（如不指定则从一级目录推断）

- [ ] **Step 2: 准备知识库**
  - 若 `{kb_path}` 不存在，从 `repo_url` 克隆：`git clone {repo_url} {kb_path}`
  - 若已存在，执行 `git pull` 同步最新内容
  - 确认 `.kb/` 目录存在（不存在则创建 `.kb/index/`、`.kb/memory/corrections/`）

- [ ] **Step 3: 定位源文件与元数据目录**
  - 源文件路径：`{kb_path}/{source_rel_path}`（如 `{kb_path}/docs/api/auth.md`）
  - 检查源文件是否存在
  - 检查 Markdown 结构：标题层级是否完整（# ~ ######），层级缺失时提示用户完善后重新入库
  - 元数据目录：`{kb_path}/.kb/index/{source_rel_path 去掉 .md}/`（如 `.kb/index/docs/api/auth/`）
  - 自动创建元数据目录

- [ ] **Step 4: 分配 doc_id 并创建 metadata.yaml**
  - 扫描 `.kb/index/` 下所有 metadata.yaml，取最大 doc_id 序号 +1
  - 从源文件 H1 获取 title（无 H1 则用文件名）
  - domain：用户指定或从一级目录推断（如 `docs/api/auth.md` → domain 为 "api"）
  - 在元数据目录创建 metadata.yaml：
    ```yaml
    doc_id: doc_001
    title: "API 认证接口"
    domain: api
    source_path: docs/api/auth.md
    source_format: markdown
    ingested_at: "2026-08-02"
    ```

- [ ] **Step 5: 构建 tree.json 骨架**
  - 运行脚本：
    ```
    python .trae/skills/kb-ingest/scripts/build_tree.py \
      "{kb_path}/{source_rel_path}" \
      "{kb_path}/.kb/index/{source_rel_dir}/tree.json" \
      "{doc_id}" "{title}"
    ```
  - 其中 `{source_rel_dir}` 是 source_rel_path 去掉 `.md` 后缀（如 `docs/api/auth`）
  - 脚本自动在元数据目录生成 tree.json 骨架

- [ ] **Step 6: 填充 summary 和 keywords（LLM 驱动）**
  - 读取源文件原文和 tree.json 骨架
  - 为**每个节点**生成：summary（≤20字，概括该节内容）、keywords（3~8个，含表格字段名/mermaid节点名/关键术语）
  - **必须由 LLM 逐个节点填充**，不能用规则脚本自动生成（规则脚本无法理解内容语义）
  - 将填充结果写入 tree.json（直接编辑 JSON 文件，保留骨架中的 id/level/title/start_line/end_line）

- [ ] **Step 7: 更新 manifest.json**
  - 运行脚本：`python .trae/skills/kb-ingest/scripts/build_manifest.py {kb_path}`
  - 脚本扫描 `.kb/index/` 下所有 metadata.yaml，重新生成 `.kb/manifest.json`

- [ ] **Step 8: 提交到 Git**
  - `cd {kb_path} && git add .kb/ && git add {source_rel_path}`（如果是新文件）
  - `git commit -m "kb: 接入文档 {doc_id} - {title}"`
  - `git push`

- [ ] **Step 9: 确认完成**
  - 告知用户 doc_id、源文件路径、元数据目录、tree.json 节点数

## 批量接入

当用户说"接入整个目录"、"扫描仓库中的所有 md 文件"或"从现有 Git 仓库初始化"时：

1. 若 `{kb_path}` 不存在，先 `git clone {repo_url} {kb_path}`
2. 递归扫描 `{kb_path}` 下所有 `.md` 文件
3. 排除 `.kb/` 目录和 `.git/` 目录
4. 对每个尚无 metadata.yaml 的文件，从 Step 4 开始执行
5. 最后统一执行 Step 7 更新 manifest.json

## 文档重建

用户说"重建 tree.json"或文档有大幅修改时：

1. 读取源文件和对应的 metadata.yaml 获取 doc_id 和 title
2. 对比现有 tree.json 中的 `source_sha256` 与源文件当前 SHA256：
   - 一致 → 跳过（无需重建）
   - 不一致 → 源文件已变更，继续重建
3. 重新运行 Step 5 脚本（会保留原有 summary/keywords，但建议检查布局变化后重新填充）
4. 重新填充 Step 6（结构变化时，旧 summary/keywords 可能不匹配新章节，应重新生成）
5. 执行 Step 7 更新 manifest.json
6. 执行 Step 8 提交到 Git

## 常见陷阱（Gotchas）

- **doc_id 序号**：必须扫描 `.kb/index/` 下已有 metadata.yaml 确认最大序号，不要依赖记忆
- **标题层级**：源文件必须有完整的标题层级（# ~ ######），这是 tree.json 构建的基础
- **source_path 映射**：metadata.yaml 中的 source_path 是相对于仓库根的路径，build_manifest.py 据此生成 manifest 的 path 字段
- **并发协作**：多人同时入库时，`.kb/` 下的文件冲突由 Git 合并机制解决，不在应用层加锁
- **大规模知识库**：单库超过几百篇文档时，按认知边界拆分 Git 仓库，不要在单库内做物理分片
- **{kb_path} 占位符**：执行时替换为实际知识库路径，默认为 `knowledge_repo`
