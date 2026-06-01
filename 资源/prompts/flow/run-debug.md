# 提示词：Run 调试分析

**提示词 ID**: `flow/run-debug`  
**场景**: 分析 Flow Run 失败原因

---

以下是搭子 Flow 运行的调试信息，请分析失败原因并给出修复建议。

## 调试输出

```
{{debug_output}}
```

## 分析要求

1. 找出**失败节点**及其错误信息
2. 分析**根本原因**（数据问题/配置问题/代码问题）
3. 给出**具体的修复步骤**
4. 如果是脚本错误，提供修复后的代码

## 常见问题类型

| 症状 | 可能原因 |
|------|---------|
| `KeyError` | 字段名不一致，检查 `source table-structure` |
| `TypeError` | 数据类型不符，检查字段类型 |
| `ConnectionError` | 数据源连接失败，检查数据源配置 |
| `PermissionError` | 缺少权限，检查 Token 和空间权限 |
| 节点超时 | 数据量过大或查询未优化 |

## 重新运行

```bash
dazi-flow run start <flow-id> --input '{{input_params}}'
dazi-flow run debug <flow-id>
```
