# tb_project_income_outcome_summary

- 数据连接：`建工成本01`（ID: `duckdb__建工成本01`）
- 表标识：`tb_project_income_outcome_summary`
- 物理表名：`tb_project_income_outcome_summary`
- 导出时间：2026-06-05T14:41:41.602Z

## 字段结构

| 显示名 | 字段名 | 类型 | 可空 |
| --- | --- | --- | --- |
| id | `id` | VARCHAR | 是 |
| project_id | `project_id` | VARCHAR | 是 |
| year | `year` | BIGINT | 是 |
| month | `month` | BIGINT | 是 |
| code | `code` | VARCHAR | 是 |
| name | `name` | VARCHAR | 是 |
| project_amount | `project_amount` | DOUBLE | 是 |
| company_amount | `company_amount` | DOUBLE | 是 |
| total | `total` | DOUBLE | 是 |
| remark | `remark` | INTEGER | 是 |
| status | `status` | BIGINT | 是 |
| create_time | `create_time` | TIMESTAMP | 是 |
| create_by | `create_by` | VARCHAR | 是 |
| update_time | `update_time` | TIMESTAMP | 是 |
| update_by | `update_by` | VARCHAR | 是 |

## 数据预览（前 10 行）

| id | project_id | year | month | code | name | project_amount | company_amount | total | remark | status | create_time | create_by | update_time | update_by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 000008ae81c747159260b7038b2e422f | 4fa8152c-1cc9-4d2b-b7f9-f2ebebd61a80 | 2022 | 12 | 4.2.2.14 | 其他手续费 | 1991111.11 | 0 | 1991111.11 |  | 1 | 2023-01-07T11:28:34 | 5002 | 2023-01-07T11:28:34 | 5002 |
| 00000b795e26418d945d639aad2943f6 | eeba143e-3c83-4f8e-a776-05452a5b7536 | 2022 | 8 | 4.2.1.20 | 劳动保护费 | 0 | 0 | 0 |  | 1 | 2022-08-26T09:23:15 | 1317 | 2022-08-26T09:23:15 | 1317 |
| 00001703031a42a7abad8586e9370f05 | 97b78498-8c97-47c7-93ed-d1edb08008ed | 2022 | 1 | 4.2.1.2 | 绩效 | 0 |  | 0 |  | 1 | 2022-02-23T16:57:56 | 5889 | 2022-02-23T16:57:56 | 5889 |
| 000040ec9822423c95682281b0556ecf | c6807d6f-5f33-4375-a065-13d740d2fe1c | 2023 | 8 | 2.3 | 工程款（回款差额） | 0 |  |  |  | 1 | 2023-09-26T17:11:58 | 1791 | 2023-09-26T17:11:58 | 1791 |
| 000045ba7e1c4bdd823242e446947e2f | 846e38b2-4192-4838-944d-02f9d12ee3fb | 2021 | 12 | 3.3.1 | 其中：资金占用利息 | 0 |  |  |  | 1 | 2022-01-19T09:41:36 | 5700 | 2022-01-19T09:41:36 | 5700 |
| 000049ed6ebf11ed8d61286ed488c884 | 5a73b85e-e3d9-4d87-8b51-5b04c089542c | 2022 | 11 | 2.8 | 其他业主收入 | 0 |  |  |  | 1 | 2022-11-28T09:51:32 | 1317 | 2022-11-28T09:51:32 | 1317 |
| 00004b256ebf11ed8d61286ed488c884 | 5a73b85e-e3d9-4d87-8b51-5b04c089542c | 2022 | 11 | 4.2.2.1 | 设计费 | 0 | 0 | 0 |  | 1 | 2022-11-28T09:51:32 | 1317 | 2022-11-28T09:51:32 | 1317 |
| 00004be16ebf11ed8d61286ed488c884 | 5a73b85e-e3d9-4d87-8b51-5b04c089542c | 2022 | 11 | 2.3 | 工程款（回款差额） | 0 |  |  |  | 1 | 2022-11-28T09:51:32 | 1317 | 2022-11-28T09:51:32 | 1317 |
| 00004f2113954a25a371036ee4d95d21 | f160fcbf-32d7-4fdb-a362-0b7f11efad36 | 2024 | 2 | 4.3.5 | 预提费用 | 0 | 0 | 0 |  | 1 | 2024-03-15T09:20:21 | 5889 | 2024-03-15T09:20:21 | 5889 |
| 00005fdaacd6418e970154f671fba2ed | 17721e11-96fa-48c4-8c45-f1f3368526ff | 2022 | 9 | 4.2.1.8 | 工会经费 | 0 | 0 | 0 |  | 1 | 2022-10-13T10:19:27 | 1254 | 2022-10-13T10:19:27 | 1254 |
