# 生产指挥中心KPI

- 数据空间：`space__0519`（ID: `space__0519`）
- 表标识：`d5bafc8076b8423f`
- 物理表名：`pcc_kpi_daily`
- 导出时间：2026-05-25T17:21:52.004Z

## 字段结构

| 显示名 | 字段名 | 类型 | 可空 |
| --- | --- | --- | --- |
| kpi_code | `kpi_code` | String | 是 |
| kpi_label | `kpi_label` | String | 是 |
| kpi_value | `kpi_value` | Float64 | 是 |
| 单价 | `unit` | String | 是 |
| 日期 | `stat_date` | Date | 是 |

## 数据预览（前 10 行）

| kpi_code | kpi_label | kpi_value | 单价 | 日期 |
| --- | --- | --- | --- | --- |
| output_today | 今日产量 | 12800 | 件 | 2026-05-24 |
| pass_rate | 一次合格率 | 99.5 | % | 2026-05-24 |
| plan_rate | 计划达成 | 90.8 | % | 2026-05-24 |
