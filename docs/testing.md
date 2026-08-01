# 测试方法

## 测试原则

kb-pilot 的 E2E 测试严格遵循 SKILL 流程，**不使用 Python 脚本替代 LLM 执行**。测试的核心是验证 LLM 驱动的 SKILL 流程能否正确完成文档入库和知识问答。

## 测试类型

### 1. 单元测试

#### build_tree.py 测试

验证脚本对 Markdown 标题的解析准确性：

- 输入：包含各种标题层级（#、##、###）的 Markdown 文件
- 验证：节点数、层级、行号范围是否正确
- 方法：`python .trae/skills/kb-ingest/scripts/build_tree.py <source.md>`

#### build_manifest.py 测试

验证 manifest.json 生成准确性：

- 输入：包含多个文档的 docs/ 目录
- 验证：条目数、字段完整性、路径正确性
- 方法：`python .trae/skills/kb-ingest/scripts/build_manifest.py <kb_path>`

### 2. E2E 测试（LLM 驱动）

完整的端到端测试，验证 kb-ingest → kb-chat 全链路。

#### 测试流程

```
Phase 1: kb-ingest
  1. 选择测试文档（source.md）
  2. 执行 kb-ingest SKILL 9 步流程
  3. 验证产物：metadata.yaml, tree.json, manifest.json

Phase 2: kb-chat
  1. 准备 QA 测试集（问题 + 标准答案）
  2. 逐题执行 kb-chat SKILL 6 步流程
  3. 记录 LLM 答案与标准答案
  4. 评估路由准确率、答案召回率、置信度
```

#### 测试数据集

推荐使用 CRAG（Comprehensive RAG Benchmark）数据集：

- 来源：Meta CRAG Benchmark
- 规模：~4409 个 QA 对，覆盖 5 个领域
- 题型：8 种问题类型（simple, simple_w_condition, multi-hop, comparison, aggregation, set, post-processing, false_premise）
- 格式：JSONL，每行包含 query、answer、page_content（HTML 文档）

#### 测试样本选择

选择 5-10 个样本，覆盖：
- 多领域（finance, sports, music, movie, open）
- 多题型（simple, simple_w_condition, multi-hop, comparison, aggregation, post-processing）
- 不同文档长度（短/中/长）

#### 答案评估标准

| 等级 | 标准 | 说明 |
|------|------|------|
| Perfect | 答案与标准答案完全一致 | 关键信息完全匹配 |
| Acceptable | 答案包含关键信息但表述不同 | 语义等价 |
| Partial | 答案部分正确 | 缺少部分关键信息 |
| Incorrect | 答案错误 | 关键信息不匹配 |
| Not Found | 知识库中未找到 | 路由或定位失败 |

## 评估指标

### 路由准确率

文档定位是否正确（是否定位到了正确的文档和章节）：

```
路由准确率 = 正确路由的题目数 / 总题目数 × 100%
```

### 答案召回率

答案是否包含标准答案中的关键信息：

```
答案召回率 = Acceptable 及以上题目数 / 总题目数 × 100%
```

### 置信度分布

统计高/中/低置信度的分布，评估系统对自身回答的认知能力。

## 测试报告格式

测试报告应包含：

1. **测试概述**：测试时间、数据集、样本数
2. **Phase 1 结果**：ingest 产物验证
3. **Phase 2 结果**：逐题答案对比
4. **汇总指标**：路由准确率、答案召回率、置信度分布
5. **问题分析**：失败案例及原因
6. **改进建议**：SKILL 流程优化建议

### 3. 纠错功能测试

验证对话式纠错的完整链路：

#### 测试步骤

1. **正常问答**：先问一个问题，记录原始答案
2. **触发纠错**：说"不对，正确应该是 XXX"
3. **验证持久化**：检查 `memory/corrections/{doc_id}.jsonl` 是否追加了新记录
4. **重新问答**：再次问相同问题，验证是否使用了纠正后的答案
5. **冲突处理**：再次说"不对，应该是 YYY"，验证是否追加 `conflicted` 状态并展示所有版本

#### 验证标准

| 检查项 | 预期结果 |
|--------|---------|
| 纠错记录创建 | jsonl 文件追加新行，含 timestamp、status=active |
| 答案修正 | 重新问答时使用纠正后的答案 |
| 冲突检测 | 不同答案追加为 conflicted，展示所有版本 |
| 文档隔离 | 不同 doc_id 的纠错记录互不影响 |

### 4. 路由偏好测试

1. 表达偏好："我以后主要问 X 领域"
2. 验证 `route_preferences.json` 更新
3. 问一个模糊问题，验证是否优先匹配偏好领域

## 与传统 RAG 的对比测试

详见 [rag-comparison.md](rag-comparison.md) — 与 8 种主流方案的架构对比。

| 方案 | 检索方式 | 部署要求 |
|------|---------|---------|
| Naive RAG | 向量相似度 + Chunk 切分 | Embedding 模型 + 向量数据库 |
| GraphRAG | 实体关系图 | 图数据库 + 实体抽取 |
| HyDE | 假设文档嵌入 | Embedding 模型 + 向量数据库 |
| RAPTOR | 层级摘要树 | Embedding 模型 + 向量数据库 |
| kb-pilot | 树索引确定性定位 | 仅文件系统 |

对比维度：
- 路由准确率
- 答案召回率
- 部署成本
- 上下文完整性
- 可追溯性
- 纠错能力
- 文档更新成本