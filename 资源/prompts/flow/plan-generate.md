# 提示词：执行计划生成（项目态）

**提示词 ID**: `flow/plan-generate`  
**场景**: 基于流程项目上下文生成可执行的运行/改造计划

---

请根据以下 Flow 引导信息和输入参数，分析执行计划，并输出“能直接落地”的操作步骤。

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
4. 给出优化建议（拆成：画布改造 / 代码改造 / 运行策略）
5. 若包含节点新增或连线调整，给出具体修改位置与命令

## 命令约束（必须遵守）

- 命令前缀统一：`dazi flow ...`（在 `dazi-work` 根）
- 在流程目录执行时，命令建议显式带 `--dir .`
- 禁止输出裸 `dazi-flow ...` 作为最终交付命令

## 计划落地命令模板（按需引用）

```powershell
# 查看当前状态
dazi flow project status --dir .

# 新增节点（若需要）
dazi flow node new --type <node_type> --dir . --label "<节点名>"

# 单节点验证
dazi flow run node-exec --node <node_uuid> --dir .

# 整流程验证
dazi flow run flow-exec --dir . --type debug

# 提交（改画布/配置时必须 canvas）
dazi flow node push --node <node_uuid> --dir .
dazi flow project push --dir . --canvas
```

## 回答格式要求

1. **执行顺序图**：节点顺序与关键输入输出变量
2. **风险点**：数据量、连接、字段一致性、上游依赖
3. **改造步骤**：每步写清“改文件 + 跑命令 + 验证点”
4. **一致性检查**：是否同时覆盖 `flow.json` 与 `节点/<名>/code.*`
