# 流程运行失败（Run 57）

> 由 dazi-flow 生成。**测试不会自动纠错**：请确认错误后，再把本文件连同 code.* / 节点配置交给 AI 处理。

## 概要

| 字段 | 值 |
| --- | --- |
| flowId | 135 |
| 节点 | — |
| 状态 | failed |
| 错误分类 | **未知** |

## 修复指引

请查看完整 traceback 与日志。

## FailureBundle

```json
{
  "version": 1,
  "run_id": 57,
  "flow_id": 135,
  "run_status": "failed",
  "has_failure": true,
  "failures": [
    {
      "node_id": "dataspace-sink-risk",
      "node_label": "写入风险数据",
      "status": "failed",
      "error": "ClickHouse 追加写入失败: Unrecognized column 'risk_level' in table fact_project_risk",
      "traceback_excerpt": null,
      "step_order": 5,
      "iteration": 0,
      "source": "execution_log",
      "related_variable_names": []
    }
  ]
}
```
