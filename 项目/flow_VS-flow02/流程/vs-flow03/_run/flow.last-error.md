# 流程运行失败（Run 32）

> 由 dazi-flow 生成。**测试不会自动纠错**：请确认错误后，再把本文件连同 code.* / 节点配置交给 AI 处理。

## 概要

| 字段 | 值 |
| --- | --- |
| flowId | 111 |
| 节点 | — |
| 状态 | failed |
| 错误分类 | **未知** |

## 修复指引

请查看完整 traceback 与日志。

## FailureBundle

```json
{
  "version": 1,
  "run_id": 32,
  "flow_id": 111,
  "run_status": "failed",
  "has_failure": true,
  "failures": [
    {
      "node_id": "n-sql-join",
      "node_label": "SQL 成本关联",
      "status": "failed",
      "error": "Invalid Input Error: Failed to read Parquet file 'D:/dazi/dazi-backend/storage/uploads/1c458509-fdd1-4b6a-8fe1-487b273f0c9e.parquet': Need at least one non-root column in the file",
      "traceback_excerpt": null,
      "step_order": 4,
      "iteration": 0,
      "source": "execution_log",
      "related_variable_names": []
    }
  ]
}
```
