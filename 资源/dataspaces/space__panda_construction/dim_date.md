# 日期维表

- 数据空间：`space__panda_construction`（ID: `space__panda_construction`）
- 表标识：`ff52ca8b82e143c8`
- 物理表名：`dim_date`
- 导出时间：2026-06-10T07:32:13.550Z

## 字段结构

| 显示名 | 字段名 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- | --- |
| 日期键 | `date_key` | Int32 | 是 | YYYYMMDD，主键 |
| 自然日 | `calendar_date` | Date | 是 |  |
| 公历年 | `year` | Int16 | 是 |  |
| 季度 | `quarter` | Int8 | 是 | 1-4 |
| 月 | `month` | Int8 | 是 | 1-12 |
| 周 | `week_of_year` | Int8 | 是 |  |
| 星期 | `day_of_week` | Int8 | 是 |  |
| 是否周末 | `is_weekend` | UInt8 | 是 | 0/1 |
| 年月 | `year_month` | String | 是 | 如 2025-06 |

## 数据预览（前 10 行）

（暂无样例数据）
