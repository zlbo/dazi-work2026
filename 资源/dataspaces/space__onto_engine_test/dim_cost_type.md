# 成本科目维表

- 数据空间：`space__onto_engine_test`（ID: `space__onto_engine_test`）
- 表标识：`9c37ea22fdbd4755`
- 物理表名：`dim_cost_type`
- 导出时间：2026-06-12T16:42:22.920Z

## 字段结构

| 显示名 | 字段名 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- | --- |
| 科目 ID | `cost_type_id` | String | 是 | 主键 |
| 科目编码 | `cost_type_code` | String | 是 |  |
| 科目名称 | `cost_type_name` | String | 是 |  |
| 上级科目 | `parent_type_id` | String | 是 | 自关联 |
| 状态 | `status` | String | 是 |  |
| 创建时间 | `created_at` | DateTime | 是 |  |

## 数据预览（前 10 行）

| 科目 ID | 科目编码 | 科目名称 | 上级科目 | 状态 | 创建时间 |
| --- | --- | --- | --- | --- | --- |
| CT_MAT_CONC | CONC | 混凝土 | CT_MAT | 启用 | 2025-01-01 00:00:00+08:00 |
| CT_LAB | LAB | 人工费 |  | 启用 | 2025-01-01 00:00:00+08:00 |
| CT_MAT | MAT | 材料费 |  | 启用 | 2025-01-01 00:00:00+08:00 |
| CT_LAB_OT | OT | 加班费 | CT_LAB | 启用 | 2025-01-01 00:00:00+08:00 |
| CT_MAT_STEEL | STEEL | 钢材 | CT_MAT | 启用 | 2025-01-01 00:00:00+08:00 |
| CT_LAB_WAGE | WAGE | 工资 | CT_LAB | 启用 | 2025-01-01 00:00:00+08:00 |
