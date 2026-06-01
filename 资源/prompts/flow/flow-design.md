# 提示词：Flow 设计

**提示词 ID**: `flow/flow-design`  
**场景**: 设计新的数据流程

---

你是一名搭子平台数据工程师。请根据以下需求设计一个 Flow（数据流程）。

## 需求描述

{{flow_description}}

## 设计要点

1. **输入数据源**：从哪些数据源读取数据
2. **数据转换逻辑**：每个步骤做什么变换
3. **输出目标**：结果写入哪里
4. **触发方式**：定时/事件触发/手动触发

## 常见节点类型

| 节点类型 | 说明 |
|---------|------|
| `source` | 数据读取（数据库/文件/API） |
| `transform` | 数据变换（SQL/Python/聚合） |
| `filter` | 数据过滤 |
| `join` | 数据关联 |
| `sink` | 数据写出 |
| `script` | 自定义脚本节点 |

## 开发流程

```bash
# 1. 创建 Flow
dazi-flow flows create --name "Flow 名称" --space <space-id>

# 2. 拉取快照查看结构
dazi-flow snapshot pull --flow <flow-id>

# 3. 查看数据源
dazi-flow source list --space <space-id>
dazi-flow source tables <source-id>

# 4. 编译执行计划
dazi-flow plan compile <flow-id>

# 5. 启动测试
dazi-flow run start <flow-id> --input '{"test": true}'

# 6. 查看结果
dazi-flow run debug <flow-id>
```
