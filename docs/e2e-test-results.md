# kb-pilot E2E 测试报告

> 测试日期: 2026-08-01  
> 测试框架: kb-ingest + kb-chat (SKILL-driven, LLM native)  
> 测试数据集: 自建 5 篇测试文档, 32 个 QA 问题  
> 覆盖格式: 中文表格、英文财务表、代码块、Mermaid 图、数学公式、架构图、业务流程图

---

## 1. 测试概述

### 1.1 测试文档

| # | 文档 | 领域 | 语言 | 格式特征 | 行数 |
|---|------|------|------|----------|------|
| doc_001 | AI大模型对比分析（2024版） | AI | 中文 | 表格、列表 | 88 |
| doc_002 | Q1 2024 Earnings Report - NovaTech Solutions | 财经 | 英文 | 财务表格、列表 | 88 |
| doc_003 | Microservices Architecture Guide | 技术 | 英文 | 代码块、Mermaid图、表格 | 208 |
| doc_004 | 深度学习在NLP中的应用 | AI | 中英混合 | 数学公式、表格 | 145 |
| doc_005 | 银行核心系统架构与业务手册 | 金融 | 中文 | Mermaid架构图、业务流程图、表格 | 234 |

### 1.2 测试维度

| 维度 | 覆盖 |
|------|------|
| 文档数 | 5 |
| 领域数 | 4 (AI、财经、技术、金融) |
| 语言 | 中文 28 题 + 英文 4 题 |
| 问题类型 | 简单问答、聚合统计、对比分析、多跳推理、后处理 |
| 格式覆盖 | 表格、代码块、Mermaid图、数学公式、列表、流程图 |

---

## 2. 测试结果

### 2.1 总体指标

| 指标 | 值 |
|------|-----|
| 总问题数 | 32 |
| 路由正确数 | 32 |
| 路由准确率 | **100.0%** |
| 答案完全匹配 | 32 |
| 答案召回率 | **100.0%** |
| Perfect (完全正确) | 32 (100.0%) |
| Acceptable (可接受) | 0 (0.0%) |
| Mismatch (错误) | 0 (0.0%) |

### 2.2 按文档统计

| 文档 | 问题数 | 路由准确 | 答案匹配 | Perfect |
|------|--------|----------|----------|---------|
| doc_001 AI大模型 | 6 | 6/6 | 6/6 | 100% |
| doc_002 财报 | 6 | 6/6 | 6/6 | 100% |
| doc_003 微服务 | 6 | 6/6 | 6/6 | 100% |
| doc_004 NLP | 6 | 6/6 | 6/6 | 100% |
| doc_005 银行 | 8 | 8/8 | 8/8 | 100% |

### 2.3 按问题类型统计

| 问题类型 | 数量 | 路由准确 | 答案匹配 | Perfect |
|----------|------|----------|----------|---------|
| 简单问答 (simple) | 12 | 12/12 | 12/12 | 100% |
| 聚合统计 (aggregation) | 5 | 5/5 | 5/5 | 100% |
| 对比分析 (comparison) | 5 | 5/5 | 5/5 | 100% |
| 多跳推理 (multi-hop) | 5 | 5/5 | 5/5 | 100% |
| 后处理 (post-processing) | 5 | 5/5 | 5/5 | 100% |

### 2.4 按语言统计

| 语言 | 数量 | 路由准确 | 答案匹配 |
|------|------|----------|----------|
| 中文 | 28 | 28/28 | 28/28 |
| 英文 | 4 | 4/4 | 4/4 |

---

## 3. 详细结果

### 3.1 文档1: AI大模型对比分析 (doc_001)

| # | 问题 | 类型 | 路由 | 答案 | 预期 | 结果 |
|---|------|------|------|------|------|------|
| Q1-1 | 哪个模型的MMLU得分最高？ | simple | ch_2_1 | Claude 3.5 Sonnet (88.7%) | Claude 3.5 Sonnet (88.7%) | Perfect |
| Q1-2 | What is the context window size of Gemini 1.5 Pro? | simple | ch_1 | 1M tokens | 1M tokens | Perfect |
| Q1-3 | 哪些模型支持多模态？ | aggregation | ch_1 | GPT-4 Turbo, Claude 3.5 Sonnet, Gemini 1.5 Pro, Qwen 2.5 Max | 同上 | Perfect |
| Q1-4 | 比较DeepSeek V3和GPT-4 Turbo的API价格 | comparison | ch_1+ch_3_2 | $0.27/$1.1 vs $10/$30 (1/37) | 同上 | Perfect |
| Q1-5 | 中文能力最强的模型是什么？C-Eval得分？ | multi-hop | ch_2_2 | Qwen 2.5 Max (91.5%) | 同上 | Perfect |
| Q1-6 | DeepSeek V3比GPT-4 Turbo每月节省多少成本？ | post-processing | ch_3_2 | ~$19,315/月 | 同上 | Perfect |

### 3.2 文档2: Q1 2024 Earnings Report (doc_002)

| # | 问题 | 类型 | 路由 | 答案 | 预期 | 结果 |
|---|------|------|------|------|------|------|
| Q2-1 | What was NovaTech's total revenue in Q1 2024? | simple | ch_2 | $5,600M | $5,600M | Perfect |
| Q2-2 | 哪个业务板块的YoY增长率最高？ | simple | ch_2 | Cloud Services (35.4%) | 同上 | Perfect |
| Q2-3 | Cloud Services和Enterprise Software占Q1总收入百分比？ | aggregation | ch_2 | 76.2% | 76.2% | Perfect |
| Q2-4 | EMEA和APAC哪个区域收入更高？高多少？ | comparison | ch_4 | EMEA ($1,344M) > APAC ($1,008M), +$336M | 同上 | Perfect |
| Q2-5 | Hardware板块Q1表现？YoY和QoQ增长？ | multi-hop | ch_2+ch_6_3 | $892M, YoY -11.9%, QoQ -5.6% | 同上 | Perfect |
| Q2-6 | Q2 2024 guidance中EPS的中值？ | post-processing | ch_7 | $2.93 | $2.93 | Perfect |

### 3.3 文档3: Microservices Architecture Guide (doc_003)

| # | 问题 | 类型 | 路由 | 答案 | 预期 | 结果 |
|---|------|------|------|------|------|------|
| Q3-1 | What is the Circuit Breaker pattern used for? | simple | ch_3_2 | Prevents cascading failures | 同上 | Perfect |
| Q3-2 | 哪个微服务使用MongoDB数据库？ | simple | ch_4_1 | Inventory Service | 同上 | Perfect |
| Q3-3 | Monolith和Microservices的Scaling方式区别？ | comparison | ch_6 | Whole app vs Per-service granular | 同上 | Perfect |
| Q3-4 | CircuitBreaker类中failure_threshold和recovery_timeout默认值？ | multi-hop | ch_3_2 | failure_threshold=5, recovery_timeout=30 | 同上 | Perfect |
| Q3-5 | 哪些服务使用PostgreSQL数据库？ | aggregation | ch_4_1 | User Service, Order Service | 同上 | Perfect |
| Q3-6 | 微服务推荐的observability工具？ | simple | ch_5_2 | OpenTelemetry, ELK/Loki, Prometheus+Grafana | 同上 | Perfect |

### 3.4 文档4: 深度学习在NLP中的应用 (doc_004)

| # | 问题 | 类型 | 路由 | 答案 | 预期 | 结果 |
|---|------|------|------|------|------|------|
| Q4-1 | Transformer架构是哪一年由谁提出的？ | simple | ch_2_1 | 2017年, Vaswani ("Attention Is All You Need") | 同上 | Perfect |
| Q4-2 | BERT模型的参数量？ | simple | ch_2_2 | 110M/340M | 同上 | Perfect |
| Q4-3 | BERT和GPT-2架构类型本质区别？ | comparison | ch_2_2 | Encoder-only (双向) vs Decoder-only (单向) | 同上 | Perfect |
| Q4-4 | LoRA公式中B和A矩阵维度？r范围？ | multi-hop | ch_4_1 | B∈R^{d×r}, A∈R^{r×k}, r<<min(d,k) | 同上 | Perfect |
| Q4-5 | 列出量化方法及大小缩减比例 | aggregation | ch_4_2 | FP16 50%, INT8 75%, INT4 87.5%, NF4 87.5% | 同上 | Perfect |
| Q4-6 | 中文NLP面临的特殊挑战？ | post-processing | ch_6 | 分词歧义、多音字、繁简转换、领域术语 | 同上 | Perfect |

### 3.5 文档5: 银行核心系统架构与业务手册 (doc_005)

| # | 问题 | 类型 | 路由 | 答案 | 预期 | 结果 |
|---|------|------|------|------|------|------|
| Q5-1 | 借记卡普卡的日累计限额？ | simple | ch_2_2 | 5万元 | 5万元 | Perfect |
| Q5-2 | 信用卡账单日后多久是还款日？ | simple | ch_3_2 | 20-25天 | 同上 | Perfect |
| Q5-3 | 借记卡和信用卡资金来源本质区别？ | comparison | ch_4 | 自有存款 vs 银行授信额度 | 同上 | Perfect |
| Q5-4 | 列出信用卡等级及额度范围 | aggregation | ch_3_3 | 普卡3千-5万, 金卡1万-10万, 白金5万-50万, 钻石20万-200万 | 同上 | Perfect |
| Q5-5 | 信用卡逾期未还计息规则？涉及哪些费用？ | multi-hop | ch_3_5 | 日利率0.05% + 5%违约金 | 同上 | Perfect |
| Q5-6 | 核心账务系统TPS性能要求？ | simple | ch_6_1 | ≥5000笔/秒 | 同上 | Perfect |
| Q5-7 | What is the RPO requirement for core banking? | simple | ch_6_2 | RPO ≤ 0 (zero data loss) | 同上 | Perfect |
| Q5-8 | 大额转账反洗钱上报阈值和时限？ | post-processing | ch_5_2 | 单笔≥50万, T+1 | 同上 | Perfect |

---

## 4. 路由分析

### 4.1 领域路由

| 领域 | 问题数 | 路由准确 | 准确率 |
|------|--------|----------|--------|
| AI | 12 | 12 | 100% |
| 财经 | 6 | 6 | 100% |
| 技术 | 6 | 6 | 100% |
| 金融 | 8 | 8 | 100% |

### 4.2 章节定位

所有 32 题均通过 tree.json keywords 匹配精确定位到正确章节。关键词匹配准确，无跨章节误定位。

### 4.3 多文档领域区分

AI 领域含 2 篇文档 (doc_001 大模型, doc_004 NLP)，文档路由通过 manifest.json tags 精准区分：
- "MMLU"/"API价格"/"模型对比" → doc_001
- "Transformer"/"BERT"/"NLP"/"NER" → doc_004
- 无交叉误路由

---

## 5. 设计验证

本测试验证了 kb-pilot 核心设计假设在 5 篇文档规模下的表现：

| 设计假设 | 验证结果 |
|----------|----------|
| LLM 能通过 manifest.json tags 做文档路由 | 5/5 文档路由准确 |
| LLM 能通过 tree.json keywords 做章节定位 | 32/32 题章节定位准确 |
| 中英文混合不影响路由 | 中文 28 题 + 英文 4 题均正确 |
| 多文档同领域可区分 | AI 领域 2 篇文档零误路由 |

> 注：以上为 5 篇文档、32 题的小规模验证，不代表大规模生产环境表现。与 RAG 方案的设计哲学对比见 [rag-comparison.md](rag-comparison.md)。

---

## 6. 结论

### 6.1 关键发现

1. **路由精度 100%**：5 篇文档 32 题中，LLM 通过 manifest.json tags 和 tree.json keywords 实现了零误路由
2. **答案召回 100%**：所有 32 题答案与预期完全一致，Perfect 率 100%
3. **多格式覆盖**：表格、代码块、Mermaid 图、数学公式、流程图等复杂格式均被正确索引和检索
4. **中英文混合**：中文 28 题 + 英文 4 题均准确路由和回答
5. **多文档领域**：AI 领域含 2 篇文档，manifest.json 的 tags 精确区分了两个文档

### 6.2 设计优势

- 零部署成本：纯 SKILL 文件，无需向量数据库或图数据库
- 确定性路由：LLM 语义匹配 keywords，路由结果可复现
- 精确引用：每个答案可追溯到 source.md 具体行号
- 轻量级：tree.json 索引仅几十 KB，远小于向量索引

### 6.3 架构说明

当前 SKILL 架构已经覆盖了完整的知识库问答链路，无需额外扩展：

- **keywords 填充**：kb-ingest Step 6 由 LLM 分析文档内容自动生成，无需外部脚本
- **文档格式**：专注 Markdown 输入，文档转换由客户自行处理，SKILL 不引入转换工具避免质量风险
- **语义匹配**：kb-chat 的文档路由和章节定位均由 LLM 进行语义理解，无需额外 embedding 层

---

## 7. 记忆系统测试

验证 kb-pilot 的记忆系统（路由偏好 + 纠错功能）是否按 SKILL 规范正确运行。

### 7.1 路由偏好测试

#### 测试流程

| 步骤 | 操作 | 预期 | 实际 |
|------|------|------|------|
| 1 | 表达偏好："我以后主要问金融领域的问题" | route_preferences.json 更新，记录 domain_preferences: ["金融"] | 已更新，包含 domain_preferences 和 updated_at |
| 2 | 提问："信用卡的账单日和还款日是怎样的？" | 路由到金融 → doc_005 | 金融 → doc_005 |
| 3 | 验证问答结果 | 精确匹配 ch_3_2（信用卡核心概念） | 匹配 ch_3_2，答案正确 |

#### 路由详情

**问题**："信用卡的账单日和还款日是怎样的？"

| 步骤 | 操作 | 结果 |
|------|------|------|
| Step 1: 领域路由 | route_preferences.json 偏好"金融" + 关键词"信用卡""账单日""还款日" | 金融 |
| Step 2: 文档路由 | manifest.json 金融域 doc_005，tags 含"信用卡""还款日""账单日" | doc_005 |
| Step 3: 章节定位 | tree.json ch_3_2 keywords ["账单日", "还款日", "免息期", "最低还款额", "循环信用", "日利率", "0.05%"] | ch_3_2 (2 matches) |
| Step 4: 内容截取 | source.md L118-L125 | 账单日/还款日/免息期/最低还款/循环信用 |
| Step 5: 纠错加载 | memory/corrections/doc_005.jsonl 不存在 | 跳过 |
| Step 6: 生成答案 | 账单日每月生成账单，还款日为账单日后20-25天，免息期最长50-56天 | 基于原文 |

**答案**：账单日是银行每月生成账单的日期，还款日是持卡人应还款的最后日期（通常为账单日后20-25天），免息期最长50-56天。

**依据**：docs/04_金融/doc_005_banking/source.md#L118-L125（3.2 信用卡核心概念）

**置信度**：高（原文直接匹配）

#### 偏好验证

| 检查项 | 结果 |
|--------|------|
| route_preferences.json 创建 | 通过 — domain_preferences: ["金融"] |
| 偏好路由生效 | 通过 — 金融领域问题正确路由到 doc_005 |
| 偏好不覆盖明确意图 | 通过 — 即使偏好金融，AI 领域问题仍正确路由到 AI 域 |

### 7.2 纠错功能测试

#### 测试流程

| 步骤 | 操作 | 预期 | 实际 |
|------|------|------|------|
| 1 | 提问："DeepSeek V3 的输入价格是多少？" | 路由到 AI → doc_001，答案 $0.27/1M | AI → doc_001 → ch_1，答案 $0.27/1M |
| 2 | 纠错："不对，应该是 $0.14" | corrections/doc_001.jsonl 追加 active 记录 | 已创建，status=active |
| 3 | 重新提问相同问题 | 使用纠错后答案 $0.14 | 纠错加载后答案 $0.14 |
| 4 | 再次纠错："不对，应该是 $0.20" | 追加 conflicted 记录 | 已追加，status=conflicted |
| 5 | 重新提问相同问题 | 展示两个版本让用户选择 | active($0.14) + conflicted($0.20) |

#### 纠错记录详情

**原始问答**（纠错前）：

| 步骤 | 操作 | 结果 |
|------|------|------|
| Step 1: 领域路由 | 关键词 "DeepSeek""V3""输入价格" | AI（偏好不覆盖明确意图） |
| Step 2: 文档路由 | manifest.json AI 域，doc_001 tags 含 "DeepSeek""API价格" | doc_001 |
| Step 3: 章节定位 | tree.json ch_1 keywords ["DeepSeek", "API价格"] | ch_1 (2 matches) |
| Step 4: 内容截取 | source.md L3-L16，line 12: `$0.27/$1.1` | $0.27/1M tokens |
| Step 5: 纠错加载 | 无 | 跳过 |
| Step 6: 生成答案 | $0.27/1M tokens | 基于原文 |

**第一次纠错**："不对，DeepSeek V3 输入价格应该是 $0.14"

```jsonl
{"timestamp":"2026-08-01T18:05:00+08:00","question":"DeepSeek V3 的输入价格是多少？","correct_answer":"$0.14/1M tokens","doc_id":"doc_001","source_ref":"用户纠正","status":"active"}
```

**重新问答**（纠错后）：

| 步骤 | 操作 | 结果 |
|------|------|------|
| Step 1-4 | 同上 | AI → doc_001 → ch_1 |
| Step 5: 纠错加载 | 读取 corrections/doc_001.jsonl，status=active | 加载纠错：$0.14/1M tokens |
| Step 6: 生成答案 | 优先使用 active 纠错 | **$0.14/1M tokens**（已纠正） |

**第二次纠错**（冲突场景）："不对，应该是 $0.20"

已有 active 记录且答案不同 → 追加为 conflicted：

```jsonl
{"timestamp":"2026-08-01T18:10:00+08:00","question":"DeepSeek V3 的输入价格是多少？","correct_answer":"$0.20/1M tokens","doc_id":"doc_001","source_ref":"用户纠正","status":"conflicted"}
```

**重新问答**（冲突后）：

| 步骤 | 操作 | 结果 |
|------|------|------|
| Step 5: 纠错加载 | 读取 corrections/doc_001.jsonl | active: $0.14 + conflicted: $0.20 |
| Step 6: 生成答案 | 优先使用 active，同时展示 conflicted 版本 | 答案 $0.14，提示存在冲突版本 $0.20 |

#### 纠错验证

| 检查项 | 结果 |
|--------|------|
| 纠错记录创建 | 通过 — corrections/doc_001.jsonl 创建 |
| active 状态生效 | 通过 — 重新问答时使用 $0.14 |
| 冲突检测 | 通过 — 不同答案追加为 conflicted |
| 冲突展示 | 通过 — active + conflicted 两个版本均可见 |
| 文档隔离 | 通过 — 纠错记录按 doc_id 隔离 |
| 原始原文保留 | 通过 — source.md 第 12 行仍为 $0.27 |

---

## 8. 总结

### 8.1 全部测试指标

| 测试类别 | 测试项 | 通过率 |
|----------|--------|--------|
| 问答路由 | 32 题文档路由 | 100% (32/32) |
| 答案召回 | 32 题答案匹配 | 100% (32/32) |
| 路由偏好 | 偏好记录 + 路由验证 | 100% (3/3) |
| 纠错功能 | active + conflicted + 重新问答 | 100% (5/5) |

### 8.2 关键发现

1. **路由精度 100%**：5 篇文档 32 题中，LLM 通过 manifest.json tags 和 tree.json keywords 实现了零误路由
2. **答案召回 100%**：所有 32 题答案与预期完全一致，Perfect 率 100%
3. **多格式覆盖**：表格、代码块、Mermaid 图、数学公式、流程图等复杂格式均被正确索引和检索
4. **中英文混合**：中文 28 题 + 英文 4 题均准确路由和回答
5. **多文档领域**：AI 领域含 2 篇文档，manifest.json 的 tags 精确区分了两个文档
6. **路由偏好生效**：用户表达领域偏好后，route_preferences.json 正确更新，后续问答优先匹配
7. **纠错链路完整**：active/conflicted 状态管理、重新问答自动纠正、冲突版本展示均正常工作

### 8.3 设计优势

- 零部署成本：纯 SKILL 文件，无需向量数据库或图数据库
- 确定性路由：LLM 语义匹配 keywords，路由结果可复现
- 精确引用：每个答案可追溯到 source.md 具体行号
- 轻量级：tree.json 索引仅几十 KB，远小于向量索引
- 对话式纠错：用户纠正答案后自动持久化，active/conflicted 状态管理，知识库越用越准
- 路由偏好记忆：用户表达领域偏好后自动更新，后续问答优先匹配

### 8.4 架构说明

当前 SKILL 架构已经覆盖了完整的知识库问答链路，无需额外扩展：

- **keywords 填充**：kb-ingest Step 6 由 LLM 分析文档内容自动生成，无需外部脚本
- **文档格式**：专注 Markdown 输入，文档转换由客户自行处理，SKILL 不引入转换工具避免质量风险
- **语义匹配**：kb-chat 的文档路由和章节定位均由 LLM 进行语义理解，无需额外 embedding 层
- **记忆系统**：路由偏好（route_preferences.json）+ 纠错记录（corrections/*.jsonl），纯文件系统，零依赖