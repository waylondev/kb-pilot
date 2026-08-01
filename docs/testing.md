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

## 与传统 RAG 的对比测试

为全面评估 kb-pilot 的性能，建议与以下方案对比：

| 方案 | 检索方式 | 部署要求 |
|------|---------|---------|
| Naive RAG | 向量相似度 + Chunk 切分 | Embedding 模型 + 向量数据库 |
| GraphRAG | 实体关系图 | 图数据库 + 实体抽取 |
| kb-pilot | 树索引确定性定位 | 仅文件系统 |

对比维度：
- 路由准确率
- 答案召回率
- 部署成本
- 上下文完整性
- 可追溯性