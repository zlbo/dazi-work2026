# fact_actual

- 数据连接：`decysion`（ID: `postgres__decysion`）
- 表标识：`fact_actual`
- 物理表名：`fact_actual`
- 导出时间：2026-05-30T13:40:12.226Z

## 字段结构

| 显示名 | 字段名 | 类型 | 可空 |
| --- | --- | --- | --- |
| id | `id` | bigint | 否 |
| date_key | `date_key` | integer | 否 |
| actual_account_code | `actual_account_code` | character varying | 否 |
| amount | `amount` | numeric | 否 |
| quantity | `quantity` | numeric | 是 |
| department | `department` | character varying | 是 |
| product_line | `product_line` | character varying | 是 |
| region | `region` | character varying | 是 |
| voucher_no | `voucher_no` | character varying | 是 |
| created_at | `created_at` | timestamp without time zone | 是 |

## 数据预览（前 10 行）

| id | date_key | actual_account_code | amount | quantity | department | product_line | region | voucher_no | created_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 20240131 | REV_MAIN_01 | 8500000 | 8500 | 销售部 | A产品 | 华东 | VOUCH-202401-001 | 2026-04-17T10:05:02.429061 |
| 2 | 20240131 | REV_MAIN_02 | 4200000 | 4200 | 销售部 | B产品 | 华南 | VOUCH-202401-002 | 2026-04-17T10:05:02.429061 |
| 3 | 20240131 | REV_OTHER_01 | 350000 |  | 销售部 | 材料 | 华东 | VOUCH-202401-003 | 2026-04-17T10:05:02.429061 |
| 4 | 20240131 | REV_OTHER_02 | 280000 |  | 技术部 | 服务 | 全国 | VOUCH-202401-004 | 2026-04-17T10:05:02.429061 |
| 5 | 20240131 | COST_DIRECT_01 | 3200000 | 8000 | 生产部 | A产品 | 华东 | VOUCH-202401-005 | 2026-04-17T10:05:02.429061 |
| 6 | 20240131 | COST_DIRECT_02 | 1800000 | 4000 | 生产部 | B产品 | 华南 | VOUCH-202401-006 | 2026-04-17T10:05:02.429061 |
| 7 | 20240131 | COST_LABOR | 1500000 |  | 生产部 |  | 全国 | VOUCH-202401-007 | 2026-04-17T10:05:02.429061 |
| 8 | 20240131 | ADV_BAIDU | 450000 |  | 市场部 |  | 全国 | VOUCH-202401-008 | 2026-04-17T10:05:02.429061 |
| 9 | 20240131 | ADV_TENCENT | 320000 |  | 市场部 |  | 全国 | VOUCH-202401-009 | 2026-04-17T10:05:02.429061 |
| 10 | 20240131 | ADV_TOUTIAO | 280000 |  | 市场部 |  | 全国 | VOUCH-202401-010 | 2026-04-17T10:05:02.429061 |
