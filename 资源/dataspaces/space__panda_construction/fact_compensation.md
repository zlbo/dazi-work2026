# 赔偿事实表

- 数据空间：`space__panda_construction`（ID: `space__panda_construction`）
- 表标识：`ebf71d2cebb34973`
- 物理表名：`fact_compensation`
- 导出时间：2026-06-10T07:30:01.435Z

## 字段结构

| 显示名 | 字段名 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- | --- |
| 赔偿记录ID | `compensation_id` | String | 是 | 主键 |
| 日期键 | `date_key` | Int32 | 是 | FK→dim_date |
| 项目ID | `project_id` | String | 是 |  |
| 报告期间 | `report_period` | String | 是 |  |
| 赔偿类型 | `compensation_type` | String | 是 |  |
| 赔偿金额 | `compensation_amount` | Float64 | 是 |  |
| 赔偿原因 | `compensation_reason` | String | 是 |  |
| 责任方 | `responsible_party` | String | 是 |  |
| 赔偿日期 | `compensation_date` | Date | 是 |  |
| 支付状态 | `payment_status` | String | 是 |  |
| 创建时间 | `created_at` | DateTime | 是 |  |

## 数据预览（前 10 行）

| 赔偿记录ID | 日期键 | 项目ID | 报告期间 | 赔偿类型 | 赔偿金额 | 赔偿原因 | 责任方 | 赔偿日期 | 支付状态 | 创建时间 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMP000003 | 20250430 | P002 | 2025-04 | 合同赔偿 | 412967.23 | 北京望京SOHO第三方损失 | 潘达北京分公司 | 2025-04-30 | 已支付 | 2025-04-30 12:00:00+08:00 |
| CMP000001 | 20250430 | P003 | 2025-04 | 合同赔偿 | 518213.76 | 上海浦东住宅项目第三方损失 | 潘达建工集团 | 2025-04-30 | 已支付 | 2025-04-30 12:00:00+08:00 |
| CMP000002 | 20250430 | P004 | 2025-04 | 侵权赔偿 | 584508.15 | 广州白云机场配套第三方损失 | 潘达广东分公司 | 2025-04-30 | 待支付 | 2025-04-30 12:00:00+08:00 |
