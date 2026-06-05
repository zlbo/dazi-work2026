# 流程运行失败（Run 42）

> 由 dazi-flow 生成。**测试不会自动纠错**：请确认错误后，再把本文件连同 code.* / 节点配置交给 AI 处理。

## 概要

| 字段 | 值 |
| --- | --- |
| flowId | 120 |
| 节点 | — |
| 状态 | failed |
| 错误分类 | **未知** |

## 修复指引

请查看完整 traceback 与日志。

## FailureBundle

```json
{
  "version": 1,
  "run_id": 42,
  "flow_id": 120,
  "run_status": "failed",
  "has_failure": true,
  "failures": [
    {
      "node_id": "n-87be45c2b58a",
      "node_label": "科研项目人员统计分析",
      "status": "failed",
      "error": "(\"Could not convert '-' with type str: tried to convert to int64\", 'Conversion failed for column 排名 with type object')",
      "traceback_excerpt": null,
      "step_order": 7,
      "iteration": 0,
      "source": "execution_log",
      "related_variable_names": []
    }
  ]
}
```
