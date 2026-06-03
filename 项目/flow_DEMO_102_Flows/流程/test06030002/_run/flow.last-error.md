# 流程运行失败（Run 36）

> 由 dazi-flow 生成。**测试不会自动纠错**：请确认错误后，再把本文件连同 code.* / 节点配置交给 AI 处理。

## 概要

| 字段 | 值 |
| --- | --- |
| flowId | 114 |
| 节点 | — |
| 状态 | failed |
| 错误分类 | **未知** |

## 修复指引

请查看完整 traceback 与日志。

## FailureBundle

```json
{
  "version": 1,
  "run_id": 36,
  "flow_id": 114,
  "run_status": "failed",
  "has_failure": true,
  "failures": [
    {
      "node_id": "excel-parser-node",
      "node_label": "Excel解析器",
      "status": "failed",
      "error": "[Errno 2] No such file or directory: 'D:\\\\GitHub\\\\dazi-work\\\\资源\\\\files\\\\科研项目_模拟人员混杂数据.xlsx_72326a69\\\\原文件.xlsx'",
      "traceback_excerpt": null,
      "step_order": 2,
      "iteration": 0,
      "source": "execution_log",
      "related_variable_names": []
    }
  ]
}
```
