# 流程运行失败（Run 39）

> 由 dazi-flow 生成。**测试不会自动纠错**：请确认错误后，再把本文件连同 code.* / 节点配置交给 AI 处理。

## 概要

| 字段 | 值 |
| --- | --- |
| flowId | 117 |
| 节点 | — |
| 状态 | failed |
| 错误分类 | **未知** |

## 修复指引

请查看完整 traceback 与日志。

## FailureBundle

```json
{
  "version": 1,
  "run_id": 39,
  "flow_id": 117,
  "run_status": "failed",
  "has_failure": true,
  "failures": [
    {
      "node_id": "n-a1b2c3d4e5f6",
      "node_label": "Excel读取",
      "status": "failed",
      "error": "Excel-python script must call set_table_output('excel_data', df) to produce main output",
      "traceback_excerpt": null,
      "step_order": 2,
      "iteration": 0,
      "source": "execution_log",
      "related_variable_names": []
    }
  ]
}
```
