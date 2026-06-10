# tb_project_cost_unconfirmed_analyse

- 数据连接：`建工成本01`（ID: `duckdb__建工成本01`）
- 表标识：`tb_project_cost_unconfirmed_analyse`
- 物理表名：`tb_project_cost_unconfirmed_analyse`
- 导出时间：2026-06-10T10:40:15.105Z

## 字段结构

| 显示名 | 字段名 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- | --- |
| id | `id` | VARCHAR | 是 |  |
| project_id | `project_id` | VARCHAR | 是 |  |
| year | `year` | BIGINT | 是 |  |
| month | `month` | BIGINT | 是 |  |
| contract_code | `contract_code` | VARCHAR | 是 |  |
| contract_name | `contract_name` | VARCHAR | 是 |  |
| contract_content | `contract_content` | VARCHAR | 是 |  |
| contract_unit | `contract_unit` | VARCHAR | 是 |  |
| contract_amount | `contract_amount` | DOUBLE | 是 |  |
| pay_ratio | `pay_ratio` | DOUBLE | 是 |  |
| tax_rate | `tax_rate` | DOUBLE | 是 |  |
| is_settlement | `is_settlement` | DOUBLE | 是 |  |
| estimate_amount | `estimate_amount` | DOUBLE | 是 |  |
| reason | `reason` | VARCHAR | 是 |  |
| remark | `remark` | VARCHAR | 是 |  |
| status | `status` | BIGINT | 是 |  |
| create_time | `create_time` | TIMESTAMP | 是 |  |
| create_by | `create_by` | VARCHAR | 是 |  |
| update_time | `update_time` | TIMESTAMP | 是 |  |
| update_by | `update_by` | VARCHAR | 是 |  |

## 数据预览（前 10 行）

| id | project_id | year | month | contract_code | contract_name | contract_content | contract_unit | contract_amount | pay_ratio | tax_rate | is_settlement | estimate_amount | reason | remark | status | create_time | create_by | update_time | update_by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 00000df3ece240379fdd98d2dcfc66f7 | cb03c9e1-d1ef-4f5c-af37-be16093c0609 | 2021 | 8 |  |  |  |  |  |  |  |  |  |  |  | 1 | 2021-09-18T17:19:02 | 3797 | 2021-09-18T17:19:02 | 3797 |
| 000014047ec74506a1a10ea7397466cf | 2331b7f3-59da-46f9-832c-17582553a853 | 2022 | 5 |  |  |  |  |  |  |  |  |  |  |  | 1 | 2022-05-25T14:01:43 | 1317 | 2022-05-25T14:01:43 | 1317 |
| 00003013fc024e338dc131ed9c269501 | 49ca9c4f-8ace-48cd-a56e-751b8d61944e | 2021 | 11 |  |  |  |  |  |  |  |  |  |  |  | 1 | 2021-12-13T15:05:30 | 3878 | 2021-12-13T15:05:30 | 3878 |
| 00004cd8ae224d50b2d34c357c04d6d3 | 7b00bfd7-9cdf-4e0f-a696-abf2546fdf03 | 2022 | 7 |  |  |  |  |  |  |  |  |  |  |  | 1 | 2022-07-25T09:49:08 | 1317 | 2022-07-25T09:49:08 | 1317 |
| 0000cd2d83684c43923a56414afe6433 | 638f42d5-8e87-458a-8bea-1f3f18d80544 | 2022 | 8 |  |  |  |  |  |  |  |  |  |  |  | 1 | 2022-08-26T09:23:15 | 1317 | 2022-08-26T09:23:15 | 1317 |
| 0000faecee574bb9a4508866782c377f | 526cdc7a-63c7-4f4a-9d4e-022ecdb1f2cc | 2023 | 8 |  |  |  |  |  |  |  |  |  |  |  | 1 | 2023-09-27T13:58:16 | 1791 | 2023-09-27T13:58:16 | 1791 |
| 00012be35f794f178919904c5289f3c2 | 854dfb3d-e62c-4e4a-8599-059ad95fc6f8 | 2022 | 7 |  |  |  |  |  |  |  |  |  |  |  | 1 | 2022-08-27T16:59:08 | 1357 | 2022-08-27T16:59:08 | 1357 |
| 000195c0de1646a981b4ff0a5d354e0c | b97f34ef-9beb-412c-8e77-d150214cae5c | 2021 | 11 |  |  |  |  |  |  |  |  |  |  |  | 1 | 2021-12-14T10:53:55 | 1317 | 2021-12-14T10:53:55 | 1317 |
| 00020e56f4024115b853fe2d129451d6 | 3bdaf591-3e1b-4a14-b4a5-9fb7fb256f11 | 2022 | 7 |  |  |  |  |  |  |  |  |  |  |  | 1 | 2022-08-19T08:47:44 | 5257 | 2022-08-19T08:47:44 | 5257 |
| 00022d67e9d14753bacb5748b7fa9c24 | b003d33c-ac0a-4f2e-87a2-2608aec7a1e5 | 2023 | 9 | ZX_WHT_998 | 未签合同安全文明施工费 |  |  | 0 | 0 | 0 | 2 | 121540 | 结算金额确定后，一起签补充协议 |  | 1 | 2023-10-19T08:28:51 | 1791 | 2023-10-19T08:28:51 | 1791 |
