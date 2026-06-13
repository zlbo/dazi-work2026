# 流程运行失败（Run 51）

> 由 dazi-flow 生成。**测试不会自动纠错**：请确认错误后，再把本文件连同 code.* / 节点配置交给 AI 处理。

## 概要

| 字段 | 值 |
| --- | --- |
| flowId | 63 |
| 节点 | — |
| 状态 | failed |
| 错误分类 | **未知** |

## 修复指引

请查看完整 traceback 与日志。

## FailureBundle

```json
{
  "version": 1,
  "run_id": 51,
  "flow_id": 63,
  "run_status": "failed",
  "has_failure": true,
  "failures": [
    {
      "node_id": "dataspace-sink-output",
      "node_label": "写入产值数据",
      "status": "failed",
      "error": "ClickHouse 追加写入失败: 'str' object has no attribute 'timestamp'",
      "traceback_excerpt": null,
      "step_order": 5,
      "iteration": 0,
      "source": "execution_log",
      "related_variable_names": []
    }
  ]
}
```
