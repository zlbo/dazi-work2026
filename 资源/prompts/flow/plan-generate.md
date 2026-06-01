# 提示词：执行计划生成

**提示词 ID**: `flow/plan-generate`  
**场景**: 根据需求生成 Flow 执行计划

---

请根据以下 Flow LLM 引导文档和输入参数，分析执行计划：

## Flow 结构

```
{{llm_guide_content}}
```

## 输入参数

```json
{{input_params}}
```

## 要求

1. 分析每个节点的执行顺序
2. 预估数据量和执行时间
3. 识别潜在的瓶颈节点
4. 给出优化建议

获取 LLM 引导文档：
```bash
dazi-flow plan llm-guide <flow-id>
cat flows/<flow-id>/plans/llm-guide.md
```
