# budget_plan

- 数据连接：`space__xsh_01`（ID: `clickhouse__space_xsh_01`）
- 表标识：`budget_plan`
- 物理表名：`budget_plan`
- 导出时间：2026-05-25T17:22:57.169Z

## 字段结构

| 显示名 | 字段名 | 类型 | 可空 |
| --- | --- | --- | --- |
| id | `id` | Nullable(String) | 是 |
| budget_year | `budget_year` | Nullable(Int64) | 是 |
| budget_month | `budget_month` | Nullable(Int64) | 是 |
| cost_center | `cost_center` | Nullable(String) | 是 |
| cost_type | `cost_type` | Nullable(String) | 是 |
| cost_category | `cost_category` | Nullable(String) | 是 |
| budget_amount | `budget_amount` | Nullable(Int64) | 是 |
| product_type | `product_type` | Nullable(String) | 是 |
| mine_area | `mine_area` | Nullable(String) | 是 |

## 数据预览（前 10 行）

| id | budget_year | budget_month | cost_center | cost_type | cost_category | budget_amount | product_type | mine_area |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BUD202512000 | 2025 | 12 | XSH矿业 | 空数据 | 生产成本 | 0 | 铁精矿 | 红星沟 |
