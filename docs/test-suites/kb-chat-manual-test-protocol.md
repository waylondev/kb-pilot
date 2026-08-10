# kb-chat 手动测试规程

本文档定义 `kb-chat` Skill 的手动测试标准，用于后续新增数据集时保持一致的执行步骤、证据记录和判定口径。

该测试不是自动化 benchmark。测试目标是人工审计模型是否真正按 `kb-chat` 的 6 个步骤完成知识库问答，并确认最终答案能回到源文档行号。

## 适用范围

本规程适用于小型到中型、结构化 Markdown 知识库的数据集测试。知识库应已完成 `kb-ingest`，并包含：

- `.kb/manifest.json`
- `.kb/index/<source-stem>/tree.json`
- 源 Markdown 文件
- 可选的 `.kb/memory/corrections/`

每个测试数据集建议包含两类文件：

- 题集文件，例如 `qa-xxx.md`
- 执行报告，例如 `kb-chat-strict-execution-report.md`

## 测试原则

- 每题必须按 `kb-chat` 的 6 个步骤记录。
- 最终答案只能基于已读取源文档和已加载 correction。
- 标准答案或证据锚点只用于最后自检，不应提前用于路由、定位或作答。
- 如果题目或测试任务明确给出 `domain_preference`，应在 Step 1 作为强路由提示记录；如果没有明确给出，不应事后补造。
- 如果源文未说明，答案应写明“文档未提及”，不能补充常识或猜测。
- 引用必须能定位到真实源文件和真实行号。
- 复杂题允许扩展读取父级、同级或跨文档内容，但必须记录实际读取范围。

## 测试前准备

### 1. 确认知识库

记录测试对象路径，例如：

```md
测试对象：`../../../fixtures/<kb-name>/`
```

确认以下文件存在：

- `../../../fixtures/<kb-name>/.kb/manifest.json`
- `../../../fixtures/<kb-name>/.kb/index/`
- `../../../fixtures/<kb-name>/*.md` 或对应源文目录

### 2. 确认题集

题集应至少包含：

- 题号
- 问题
- 标准答案
- 证据锚点
- 可选的难度说明

标准答案和证据锚点只在 `Step 6 Self-verify` 后用于对比，不参与前 5 步。

### 3. 创建报告

报告顶部应包含：

```md
# kb-chat 严格执行追踪报告

测试对象：`../../../fixtures/<kb-name>/`

测试题集：`<question-file>.md`

执行目标：按 `kb-chat` Skill 的 6 个步骤，对知识库问题逐题作答，并记录每题的路由、章节定位、实际读取范围、correction 状态、答案、自检与标准答案对比。

执行时间：YYYY-MM-DD。
```

## 单题执行步骤

每道题必须独立执行以下 6 步。

### Step 1 Document routing

读取并使用目标知识库的 `.kb/manifest.json`。如果存在 `.kb/memory/route_preferences.json`，可作为弱先验记录，但不得替代语义判断。

如果测试题或用户指令明确给出 `domain_preference`，应作为强路由提示；如果只是上一次测试留下的偏好，只能作为弱先验。

根据问题语义匹配 manifest 中的：

- `domain`
- `title`
- `summary`
- `tags`

同时核对 `path` 字段是否存在，因为后续读取源文和计算 `tree.json` 路径都依赖该字段。

报告中必须记录：

```md
| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `<source>.md` | `doc_xxx` | 标题、摘要或 tags 中的匹配点 | 该文档用于判断的问题部分 |
```

如果明确排除了容易误命中的文档，应记录排除理由。  
如果路由不确定，应列出候选文档并让用户选择，不应自行猜测。

### Step 2 Section localization

对 Step 1 命中的每个文档，读取对应的 `tree.json`。

根据问题语义匹配节点中的：

- `title`
- `summary`
- `keywords`
- `start_line`
- `end_line`

报告中必须记录：

```md
| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `<source>.md` | `ch_x` | Lx-Ly | 该章节用于判断的问题部分 |
```

如果题目需要跨文档推理，应分别对每个文档执行章节定位。

### Step 3 Content extraction

按 Step 2 的 `start_line/end_line` 读取源 Markdown。读取范围可以扩展，但扩展必须有理由，例如：

- 父级章节包含必要定义
- 同级章节包含例外规则
- 题目涉及跨文档规则组合
- 原行段不足以支撑完整答案

报告中必须记录实际读取的源文行段：

```md
| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `<source>.md` | Lx-Ly | 从该行段提取到的事实 |
```

最终答案中的每个关键断言都必须能回到这些已读取行段。  
如果后续自检发现证据不足，应回到 Step 3 扩展读取，再重新作答和自检。

### Step 4 Correction loading

检查 `.kb/memory/corrections/` 下与命中文档对应的 correction 文件。

至少检查：

- `.kb/memory/corrections/` 是否存在
- `doc_id.jsonl` 是否存在
- correction 是否与当前问题相关

报告中必须记录：

```md
| 检查位置 | 结果 |
|---|---|
| `.kb/memory/corrections/` | 是否存在 correction 目录 |
| `doc_xxx.jsonl` | 不存在 / 存在但无关 / 存在且相关 |
```

如果存在相关 correction：

- 重复 correction 可作为一致性信号。
- 冲突 correction 应并列展示。
- 如果 correction 与当前源文冲突，应优先说明冲突，不应静默覆盖源文。

### Step 5 Generate answer

只基于 Step 3 已读取内容和 Step 4 correction 作答。

报告中建议先记录判断表，再写最终答案：

```md
| 判断项 | 结论 | 判断依据 |
|---|---|---|
| 条件或问点 | 结论 | 对应源文依据 |
```

最终答案应满足：

- 直接回答用户所有问点。
- 不引入未读取源文中的事实。
- 对条件、例外、未提及内容保留边界。
- 引用文件和行号应与 Step 3 实际读取范围一致。

### Step 6 Self-verify

逐条核对最终答案中的关键断言。

报告中必须记录：

```md
| 断言 | 核验 | 来源 |
|---|---|---|
| 答案中的事实断言 | 通过 / 不通过 | `<source>.md#Lx-Ly` |
```

自检要求：

- 每个关键断言都有源文行号。
- 引用行号真实存在。
- 引用内容确实支撑断言。
- 已回答题目中的所有问点。
- 与标准答案和证据锚点对比，记录是否一致。

如果发现断言无证据，应回到 Step 3 重新读取，不得只修改引用。

## 单题报告模板

```md
## 本次单题执行更新：Qx

更新时间：YYYY-MM-DD。

问题：<原始问题>

结论：

| 问点 | 答案 |
|---|---|
| <问点 1> | <答案> |
| <问点 2> | <答案> |

### Step 1 Document routing

执行说明：本题使用 `../../../fixtures/<kb-name>/.kb/manifest.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|

路由判断：<说明命中文档和排除文档的理由>。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|

结论：<是否存在相关 correction>。

### Step 5 Generate answer

| 判断项 | 结论 | 判断依据 |
|---|---|---|

最终答案：<仅基于源文和 correction 的答案>

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|

自检结论：<是否回答所有问点；是否每个断言都有源文支撑；是否与标准答案一致>。
```

## 总体结果记录

报告顶部应维护总体结果表：

```md
| 题号 | 主要能力 | 事实答案 | 引用精度 | 备注 |
|---|---|---:|---:|---|
| Q1 | <能力类型> | 通过 / 不通过 | 通过 / 不通过 | <简要说明> |
```

统计口径：

- `事实答案`：最终答案是否覆盖标准答案的关键事实。
- `引用精度`：引用文件和行号是否真实、准确、能支撑答案。
- 如果答案正确但流程跳步，应在备注中说明，不应计为完整通过。
- 如果引用真实但不能支撑断言，引用精度不通过。
- 如果源文未提及而答案正确写出“未提及”，事实答案可通过。

## 通过标准

单题通过需要同时满足：

- 完成并记录 Step 1 到 Step 6。
- 路由文档与问题语义匹配。
- 章节定位能支撑后续读取。
- 实际读取行段覆盖答案所需证据。
- correction 检查有记录。
- 最终答案回答所有问点。
- 每个关键断言都有源文行号。
- 自检没有发现未支撑断言。

以下情况应判为不通过或部分通过：

- 直接作答，没有记录完整步骤。
- 使用标准答案反推路由或证据。
- 引用了未读取的源文行段。
- 引用行号不存在或不支撑断言。
- 对源文未提及内容进行猜测。
- 忽略相关 correction。
- 多文档问题只读取了其中一部分必要文档。

## 异常处理

异常情况应按 `kb-chat` Skill 的失败处理口径记录，不应为了完成题目而猜测。

| 异常 | 处理方式 | 报告记录 |
|---|---|---|
| `.kb/manifest.json` 缺失 | 停止测试该知识库，报告“knowledge base not initialized; run kb-ingest first” | 记录缺失路径和无法继续的原因 |
| 路由后无相关文档 | 答案只写“not mentioned in the documents”或对应中文表述 | 记录已检查的 manifest 范围 |
| 多个候选文档难以判断 | 列出候选文档并让用户选择 | 不自行猜测命中文档 |
| 源文引用缺失或行号错误 | 回到 Step 3 重新读取并修正 | 不得只改最终答案或只改引用 |
| `path` 字段与源文件不匹配 | 判为该文档不可回答，记录路径问题 | 不手动猜测替代路径，除非用户确认 |

## README 摘要口径

如果测试结果写入项目 README，只能作为手工可审计结果描述：

```md
These are hand-auditable execution records on small, structured Markdown knowledge bases. They are not an automated benchmark or a claim of general performance across open-domain RAG workloads.
```

不要将手动测试结果描述为自动化 benchmark，也不要泛化为任意 RAG 场景的性能结论。
