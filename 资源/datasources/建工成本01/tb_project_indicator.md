# tb_project_indicator

- 数据连接：`建工成本01`（ID: `duckdb__建工成本01`）
- 表标识：`tb_project_indicator`
- 物理表名：`tb_project_indicator`
- 导出时间：2026-06-05T14:41:45.090Z

## 字段结构

| 显示名 | 字段名 | 类型 | 可空 |
| --- | --- | --- | --- |
| id | `id` | VARCHAR | 是 |
| project_id | `project_id` | VARCHAR | 是 |
| year | `year` | BIGINT | 是 |
| month | `month` | BIGINT | 是 |
| code | `code` | VARCHAR | 是 |
| title | `title` | VARCHAR | 是 |
| value | `value` | VARCHAR | 是 |
| value_type | `value_type` | BIGINT | 是 |
| remark | `remark` | VARCHAR | 是 |
| status | `status` | BIGINT | 是 |
| create_time | `create_time` | TIMESTAMP | 是 |
| create_by | `create_by` | VARCHAR | 是 |
| update_time | `update_time` | TIMESTAMP | 是 |
| update_by | `update_by` | VARCHAR | 是 |

## 数据预览（前 10 行）

| id | project_id | year | month | code | title | value | value_type | remark | status | create_time | create_by | update_time | update_by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 00000ff0821f4eeb9e42596ac317b8c1 | 2910a66f-2c75-4810-9427-41aeb6d5e49a | 2023 | 6 | indicator_cbgxd | 指标_成本刚性度 | 1 | 2 | 表3(6.4) | 1 | 2023-07-14T14:19:57 | 1270 | 2023-07-14T14:19:57 | 1270 |
| 00001bfbf0e34f4494f597551d7d7ca6 | aeff472e-7202-49ba-93c9-bb98d2185aa3 | 2022 | 12 | outcome_guarantee_else | 保证金支出_其它保证金支出 |  | 2 | 表3(8.4.3) | 1 | 2023-01-09T17:46:09 | 5605 | 2023-01-09T17:46:09 | 5605 |
| 00002b8d549e40d5960863e09bc57e45 | 4e801692-2771-4abc-9fac-c971d598fd9b | 2022 | 10 | retention_amount_two | 质保金金额_第二阶段 |  | 2 | 表3.1.2(2.2.1) | 1 | 2022-10-25T20:31:25 | 1317 | 2022-10-25T20:31:25 | 1317 |
| 00003b7ab8f24fdfa3b8c8f1c8f02cae | 81ae6cbc-e4e2-4031-ac8a-f304bb36b78d | 2022 | 4 | outcome_principal_return_internal | 借款本金返回_内部项目资金拆借本金返还支出 |  | 2 | 表3(8.3.1) | 1 | 2022-05-17T18:23:36 | 1317 | 2022-05-17T18:23:36 | 1317 |
| 00003ff140964f0fb03fefa1fe5e312e | cc4217da-243d-4d3f-ae4c-b2006b841c6b | 2022 | 7 | project_name | 项目名称 | 东原金马三期一组团项目部 | 1 |  | 1 | 2022-07-25T09:49:08 | 1317 | 2022-07-25T09:49:08 | 1317 |
| 00005ac65457477282ad4416ce6757c9 | a854999e-fcdd-449b-876c-138a54df94d9 | 2022 | 4 | project_contract_amount | 合同金额(含暂定金/暂估价/甲供材) | 5263053.84 | 2 |  | 1 | 2022-04-25T09:45:37 | 1317 | 2022-04-25T09:45:37 | 1317 |
| 000060204fb14d8fb05e3dca42515f61 | 948e9025-cfd6-427b-a45b-0aa43d3cf96e | 2022 | 5 | full_cost_unconfirmed_cmonth | 全口径成本_本月已发生_待确 |  | 2 | 表3(3.5) | 1 | 2022-05-25T14:01:43 | 1317 | 2022-05-25T14:01:43 | 1317 |
| 00006e7051dc4d5bbc51932447f44471 | f030e0a8-1ae8-4a15-9a18-93f29c89c23b | 2021 | 10 | output_actual_unconfirmed_cmonth | 产值_本月完成_待确认 | -1710419.06 | 2 | 表3.1(1.8) | 1 | 2021-11-11T19:17:43 | 1357 | 2021-11-11T19:17:43 | 1357 |
| 00006ea8edcc455d8f476938d2a0303e | 206bc338-dbc7-4fce-b896-7040a0cb557f | 2022 | 10 | project_actual_completion_date | 实际竣工日期 | 2016-09-15 | 3 |  | 1 | 2022-10-25T20:31:25 | 1317 | 2022-10-25T20:31:25 | 1317 |
| 000071864681465b991a0b039be11968 | 3bdaf591-3e1b-4a14-b4a5-9fb7fb256f11 | 2023 | 10 | income_owner_acc | 业主收款_累计已收工程款 | 111352800.45 | 2 | 表3(7.2)/表3.1.2(4) | 1 | 2023-11-13T14:19:45 | 5605 | 2023-11-13T14:19:45 | 5605 |
