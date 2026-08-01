# 执行流程

## 全链路流程

```
┌──────────────────────────────────────────────────────────────┐
│                      Phase 1: kb-ingest                       │
│                                                              │
│  原始文档 → source.md → metadata.yaml → tree.json → manifest │
│                                                              │
│  Step 1-2: 接收输入 + 准备知识库                                │
│  Step 3:   转换文档 (source.md)                                │
│  Step 4:   创建元数据 (metadata.yaml)                          │
│  Step 5:   构建骨架 (tree.json, 脚本)                          │
│  Step 6:   填充语义 (tree.json, LLM)                          │
│  Step 7:   更新路由表 (manifest.json, 脚本)                     │
│  Step 8-9: Git 提交 + 确认                                    │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                      Phase 2: kb-chat                         │
│                                                              │
│  用户问题 → 领域路由 → 文档路由 → 章节定位 → 内容截取 → 答案    │
│                                                              │
│  Step 0: 准备知识库 (git pull)                                │
│  Step 1: 领域路由 (route_preferences.json)                   │
│  Step 2: 文档路由 (manifest.json)                             │
│  Step 3: 章节定位 (tree.json keywords 匹配)                   │
│  Step 4: 内容截取 (source.md start_line → end_line)          │
│  Step 5: 纠错加载 (corrections/*.jsonl)                      │
│  Step 6: 生成答案 (答案 + 依据 + 置信度)                       │
└──────────────────────────────────────────────────────────────┘
```

## 数据依赖关系

```
source.md ──────────────────────────────────────┐
    │                                             │
    ├──► build_tree.py ──► tree.json (骨架) ──┤   │
    │                                         │   │
    │    LLM 填充 ◄────────────────────────────┘   │
    │         │                                    │
    │         ▼                                    │
    │    tree.json (含 summary/keywords) ─────────┤
    │                                             │
    ├──► metadata.yaml ──────────────────────────┤
    │                                             │
    └──► build_manifest.py ◄─────────────────────┘
              │
              ▼
         manifest.json
              │
              ▼
         kb-chat 文档路由
```

## 问答流程示例

以 "DeepSeek V3 的参数量是多少？" 为例：

```
Step 1: 领域路由
  关键词 "DeepSeek"、"V3"、"参数量" → 领域: 技术

Step 2: 文档路由
  manifest.json tags 匹配 "DeepSeek"、"参数量" → doc_001

Step 3: 章节定位
  tree.json 节点匹配:
    ch_2_1 (模型参数概览): keywords 含 "参数量" → 1 match ✓
    ch_2 (模型能力对比):   keywords 含 "DeepSeek" → 1 match
  
  选中 ch_2_1 (start_line=9, end_line=18)

Step 4: 内容截取
  读取 source.md L9-L18:
  | DeepSeek V3 | 671B (MoE) | 128K tokens | 2024年10月 | 文本 |

Step 5: 纠错加载
  memory/corrections/doc_001.jsonl 不存在 → 跳过

Step 6: 生成答案
  答案: DeepSeek V3 总参数量 671B (MoE)，激活 37B
  依据: source.md#L16-L16 (模型参数概览)
  置信度: 高
```

## E2E 测试流程

完整的端到端测试包含两个阶段：

### Phase 1: 文档入库测试

1. 准备 source.md 原始文档
2. 执行 kb-ingest 9 步流程
3. 验证产物：
   - metadata.yaml 字段完整
   - tree.json 骨架正确（节点数、行号范围）
   - tree.json summary/keywords 语义合理
   - manifest.json 条目正确

### Phase 2: 问答测试

1. 读取 QA 测试集
2. 逐题执行 kb-chat 6 步流程
3. 对比 LLM 答案与标准答案
4. 评估指标：
   - 路由准确率（文档定位是否正确）
   - 答案召回率（答案是否包含关键信息）
   - 置信度分布

## 纠错流程

当知识库原文存在过时或错误信息时，用户可以通过对话纠正：

```
User: 不对，DeepSeek V3 输入价格应该是 $0.14，不是 $0.27
    │
    ▼
检查 memory/corrections/doc_001.jsonl
    │
    ├── 无相似记录
    │   └── 追加: {"question":"DeepSeek V3 输入价格","correct_answer":"$0.14","status":"active"}
    │
    ├── 有记录且答案相同
    │   └── 跳过（已存在）
    │
    └── 有记录且答案不同
        └── 追加: {"correct_answer":"$0.14","status":"conflicted"}
    │
    ▼
重新回答（使用纠正后的信息）
```

**后续问答时**，kb-chat Step 5 自动加载纠错记录，优先使用 `active` 状态的答案。`conflicted` 状态时展示所有版本让用户选择。

## 路由偏好流程

```
User: 我以后主要问技术领域的问题
    │
    ▼
更新 memory/route_preferences.json
    │
    ▼
后续 kb-chat Step 1:
  读取 route_preferences.json
  偏好领域 "01_技术" 在匹配时给予更高权重
```

## 注意事项

- **LLM 驱动**：Step 6（填充 summary/keywords）和 kb-chat 全流程由 LLM 执行，不编写 Python 脚本替代
- **脚本边界**：仅 build_tree.py（Step 5）和 build_manifest.py（Step 7）使用脚本，因为它们是确定性操作
- **Git 同步**：多用户协作时，每次问答前先 git pull 确保知识库最新
- **纠错隔离**：纠错记录按 doc_id 隔离，不同文档的纠错互不影响
- **偏好约束**：仅存储用户明确表达的偏好，不从对话历史推断