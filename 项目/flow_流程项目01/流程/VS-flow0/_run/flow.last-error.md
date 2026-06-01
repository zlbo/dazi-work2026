# 流程运行失败（Run 25）

> 由 dazi-flow 生成。**测试不会自动纠错**：请确认错误后，再把本文件连同 code.* / 节点配置交给 AI 处理。

## 概要

| 字段 | 值 |
| --- | --- |
| flowId | 103 |
| 节点 | — |
| 状态 | failed |
| 错误分类 | **未知** |

## 修复指引

请查看完整 traceback 与日志。

## FailureBundle

```json
{
  "version": 1,
  "run_id": 25,
  "flow_id": 103,
  "run_status": "failed",
  "has_failure": true,
  "failures": [
    {
      "node_id": "n-c8d9e0f12a3b",
      "node_label": "质检是否通过",
      "status": "failed",
      "error": "Condition Error: invalid syntax (<string>, line 20)",
      "traceback_excerpt": null,
      "step_order": 4,
      "iteration": 0,
      "source": "execution_log",
      "related_variable_names": []
    }
  ]
}
```
