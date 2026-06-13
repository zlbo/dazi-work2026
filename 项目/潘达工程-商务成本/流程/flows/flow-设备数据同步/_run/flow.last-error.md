# 流程运行失败（Run 63）

> 由 dazi-flow 生成。**测试不会自动纠错**：请确认错误后，再把本文件连同 code.* / 节点配置交给 AI 处理。

## 概要

| 字段 | 值 |
| --- | --- |
| flowId | 145 |
| 节点 | — |
| 状态 | failed |
| 错误分类 | **未知** |

## 修复指引

请查看完整 traceback 与日志。

## FailureBundle

```json
{
  "version": 1,
  "run_id": 63,
  "flow_id": 145,
  "run_status": "failed",
  "has_failure": true,
  "failures": [
    {
      "node_id": "database-source-equipment",
      "node_label": "读取设备数据",
      "status": "failed",
      "error": "Catalog Error: Table with name tb_project_cost_equipment_detail does not exist!\nDid you mean \"tb_project_cost_pay_detail\"?\n\nLINE 16: FROM \"tb_project_cost_equipment_detail\"\n              ^",
      "traceback_excerpt": null,
      "step_order": 2,
      "iteration": 0,
      "source": "execution_log",
      "related_variable_names": []
    }
  ]
}
```
