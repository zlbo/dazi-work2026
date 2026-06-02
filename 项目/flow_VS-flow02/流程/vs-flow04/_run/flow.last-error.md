# 流程运行失败（Run 34）

> 由 dazi-flow 生成。**测试不会自动纠错**：请确认错误后，再把本文件连同 code.* / 节点配置交给 AI 处理。

## 概要

| 字段 | 值 |
| --- | --- |
| flowId | 112 |
| 节点 | — |
| 状态 | failed |
| 错误分类 | **未知** |

## 修复指引

请查看完整 traceback 与日志。

## FailureBundle

```json
{
  "version": 1,
  "run_id": 34,
  "flow_id": 112,
  "run_status": "failed",
  "has_failure": true,
  "failures": [
    {
      "node_id": "n-b35f0f30cdf4",
      "node_label": "SQL 销售产品关联",
      "status": "failed",
      "error": "Catalog Error: Table with name 销售表1 does not exist!\nDid you mean \"销售表\"?\n\nLINE 15: FROM 销售表1 s\n              ^",
      "traceback_excerpt": null,
      "step_order": 4,
      "iteration": 0,
      "source": "execution_log",
      "related_variable_names": [
        "销售产品宽表"
      ]
    }
  ]
}
```
