# tb_project_cost_pay_detail

- 数据连接：`建工成本01`（ID: `duckdb__建工成本01`）
- 表标识：`tb_project_cost_pay_detail`
- 物理表名：`tb_project_cost_pay_detail`
- 导出时间：2026-06-05T14:41:36.003Z

## 字段结构

| 显示名 | 字段名 | 类型 | 可空 |
| --- | --- | --- | --- |
| id | `id` | VARCHAR | 是 |
| project_id | `project_id` | VARCHAR | 是 |
| contract_id | `contract_id` | VARCHAR | 是 |
| year | `year` | BIGINT | 是 |
| month | `month` | BIGINT | 是 |
| no | `no` | VARCHAR | 是 |
| sort_no | `sort_no` | BIGINT | 是 |
| name | `name` | VARCHAR | 是 |
| cost_code | `cost_code` | VARCHAR | 是 |
| cost_attr | `cost_attr` | VARCHAR | 是 |
| level | `level` | BIGINT | 是 |
| base_contract_code | `base_contract_code` | VARCHAR | 是 |
| base_contract_name | `base_contract_name` | VARCHAR | 是 |
| base_contract_content | `base_contract_content` | VARCHAR | 是 |
| base_contract_unit | `base_contract_unit` | VARCHAR | 是 |
| base_contract_amount | `base_contract_amount` | DOUBLE | 是 |
| base_contract_pay_ratio | `base_contract_pay_ratio` | DOUBLE | 是 |
| base_contract_tax_rate | `base_contract_tax_rate` | DOUBLE | 是 |
| base_contract_is_settlement | `base_contract_is_settlement` | DOUBLE | 是 |
| cost_actual_confirmed_acc | `cost_actual_confirmed_acc` | DOUBLE | 是 |
| cost_actual_unconfirmed_acc | `cost_actual_unconfirmed_acc` | DOUBLE | 是 |
| cost_actual_acc | `cost_actual_acc` | DOUBLE | 是 |
| cost_actual_confirmed_cmonth | `cost_actual_confirmed_cmonth` | DOUBLE | 是 |
| cost_actual_unconfirmed_cmonth | `cost_actual_unconfirmed_cmonth` | DOUBLE | 是 |
| cost_actual_cmonth | `cost_actual_cmonth` | DOUBLE | 是 |
| cost_rigidity | `cost_rigidity` | DOUBLE | 是 |
| pay_due_confirmed_contract_acc | `pay_due_confirmed_contract_acc` | DOUBLE | 是 |
| pay_amount_acc | `pay_amount_acc` | DOUBLE | 是 |
| pay_ratio_acc | `pay_ratio_acc` | DOUBLE | 是 |
| unpaid_contract_acc | `unpaid_contract_acc` | DOUBLE | 是 |
| unpaid_exclude_unconfirmed_acc | `unpaid_exclude_unconfirmed_acc` | DOUBLE | 是 |
| unpaid_unconfirmed_acc | `unpaid_unconfirmed_acc` | DOUBLE | 是 |
| unpaid_acc | `unpaid_acc` | DOUBLE | 是 |
| fund_plan_pay_mode | `fund_plan_pay_mode` | DOUBLE | 是 |
| fund_plan_pay_type | `fund_plan_pay_type` | DOUBLE | 是 |
| fund_plan_outcome_plan | `fund_plan_outcome_plan` | DOUBLE | 是 |
| fund_plan_pay_ratio_acc | `fund_plan_pay_ratio_acc` | DOUBLE | 是 |
| fund_plan_approve_amount | `fund_plan_approve_amount` | DOUBLE | 是 |
| fund_plan_approve_ratio_acc | `fund_plan_approve_ratio_acc` | DOUBLE | 是 |
| last_month_plan_execute_approve_amount | `last_month_plan_execute_approve_amount` | DOUBLE | 是 |
| last_month_plan_execute_actual_amount | `last_month_plan_execute_actual_amount` | DOUBLE | 是 |
| retention_due_date | `retention_due_date` | VARCHAR | 是 |
| retention_amount | `retention_amount` | DOUBLE | 是 |
| has_retention | `has_retention` | DOUBLE | 是 |
| cost_actual_labor_acc | `cost_actual_labor_acc` | DOUBLE | 是 |
| pay_due_confirmed_contract_labor_acc | `pay_due_confirmed_contract_labor_acc` | DOUBLE | 是 |
| unpaid_contract_labor_acc | `unpaid_contract_labor_acc` | DOUBLE | 是 |
| unpaid_exclude_unconfirmed_acc_amend | `unpaid_exclude_unconfirmed_acc_amend` | DOUBLE | 是 |
| remark | `remark` | VARCHAR | 是 |
| status | `status` | BIGINT | 是 |
| create_time | `create_time` | TIMESTAMP | 是 |
| create_by | `create_by` | VARCHAR | 是 |
| update_time | `update_time` | TIMESTAMP | 是 |
| update_by | `update_by` | VARCHAR | 是 |

## 数据预览（前 10 行）

| id | project_id | contract_id | year | month | no | sort_no | name | cost_code | cost_attr | level | base_contract_code | base_contract_name | base_contract_content | base_contract_unit | base_contract_amount | base_contract_pay_ratio | base_contract_tax_rate | base_contract_is_settlement | cost_actual_confirmed_acc | cost_actual_unconfirmed_acc | cost_actual_acc | cost_actual_confirmed_cmonth | cost_actual_unconfirmed_cmonth | cost_actual_cmonth | cost_rigidity | pay_due_confirmed_contract_acc | pay_amount_acc | pay_ratio_acc | unpaid_contract_acc | unpaid_exclude_unconfirmed_acc | unpaid_unconfirmed_acc | unpaid_acc | fund_plan_pay_mode | fund_plan_pay_type | fund_plan_outcome_plan | fund_plan_pay_ratio_acc | fund_plan_approve_amount | fund_plan_approve_ratio_acc | last_month_plan_execute_approve_amount | last_month_plan_execute_actual_amount | retention_due_date | retention_amount | has_retention | cost_actual_labor_acc | pay_due_confirmed_contract_labor_acc | unpaid_contract_labor_acc | unpaid_exclude_unconfirmed_acc_amend | remark | status | create_time | create_by | update_time | update_by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 00001590546e45608f187f1ccc37f06f | 217c4ec8-45f5-4ef5-ad05-8a954063ba5f | 74b10090-8e16-4bb0-8106-00afc24881af | 2022 | 10 | 4.4 | 60 |  | 54010104:1 | 机械设备租赁 | 3 | A01201123100052019005000 | 施工升降机租赁合同（重庆同涞） | 施工升降机租赁合同（重庆同涞） | 重庆同涞建筑设备租赁有限公司 | 104000 | 1 | 0.03 | 1 | 134323.56 |  | 134323.56 | 0 |  | 0 | 1 | 134323.56 | 92680.2 | 0.69 | 41643.36 | 41643.36 | 0 | 41643.36 |  |  |  | 0.69 |  | 0.69 |  |  |  |  |  |  |  | 0 | 41643.36 |  | 1 | 2022-11-09T09:54:28 | 2380 | 2022-11-09T09:54:28 | 2380 |
| 00002d1145cc499386b20bbf9b052c3f | 7b00bfd7-9cdf-4e0f-a696-abf2546fdf03 |  | 2022 | 1 | 7.1 | 23 | 其它直接费(报销) | 54010107:1 | 其他直接费 | 3 | ZX_WHT_7_BX | 其它直接费(报销) |  |  |  |  |  |  | 0 |  | 0 |  |  | 0 |  | 0 | 0 |  | 0 | 0 | 0 | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0 |  | 1 | 2022-02-22T10:21:27 | 5686 | 2022-02-22T10:21:27 | 5686 |
| 0000a6cd50d64db6a0aea7431430e4b9 | bd118165-2c0d-4d7e-b325-2be4c1d171fc |  | 2022 | 8 | 2.3 | 56 | 业务招待费 | 54010203 | 间接费 | 2 |  |  |  |  |  |  |  |  | 0 |  | 0 |  |  | 0 |  | 0 | 0 |  | 0 | 0 | 0 | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 |  | 1 | 2022-08-26T09:23:15 | 1317 | 2022-08-26T09:23:15 | 1317 |
| 0000b78b11604bd2831bae3113b939f1 | 56e04b6b-e960-4466-9582-e9347fcf68eb |  | 2022 | 5 | 2.2.11 | 38 | 租赁费 | 5401020211 | 间接费 | 3 |  |  |  |  |  |  |  |  | 0 |  | 0 |  |  | 0 |  | 0 | 0 |  | 0 | 0 | 0 | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0 |  | 1 | 2022-05-25T14:01:43 | 1317 | 2022-05-25T14:01:43 | 1317 |
| 0000d94f0dd04b8193da2818bf98dc5e | c8939a12-8617-478b-9b0a-0f9dafa70f2d |  | 2022 | 5 | 2.2.2 | 65 | 工会经费 | 5401020202 | 间接费 | 3 |  |  |  |  |  |  |  |  | 0 |  | 0 |  | 0 | 0 |  | 0 | 0 |  | 0 | 0 | 0 | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 |  | 1 | 2022-05-25T14:01:43 | 1317 | 2022-05-25T14:01:43 | 1317 |
| 0000e4dd8d9d4232a80944d48e2bf50c | 80a57e77-b682-45fe-824c-5a1e52745ef1 |  | 2022 | 4 | 9.2 | 70 | 保证金支出 | 54012002 |  | 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 |  | 0 |  |  |  |  |  | 0 |  | 0 |  | 0 | 0 |  |  |  |  | 0 | 0 |  |  | 1 | 2022-05-13T16:51:19 | 1791 | 2022-05-13T16:51:19 | 1791 |
| 00015bc7772942b5b767ee016fc7fa05 | 06af29e8-38f9-4961-a4c9-dfc3fd4732db |  | 2022 | 8 | 9.1.4 | 71 | 自筹往来款返还支出 | 5401200104 |  | 3 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0 |  | 1 | 2022-08-26T09:23:15 | 1317 | 2022-08-26T09:23:15 | 1317 |
| 00015e474c7c4680a2a78ec9f012c135 | 7732f58d-9da9-4836-936b-d5f65cf60b4e | ZX_WHT_999 | 2022 | 2 | 7.6 | 68 | 运输费 | 54010107:1 | 其他直接费 | 3 | ZX_WHT_999 | 未签合同其它直接费 |  |  | 0 | 0 | 0 | 2 | 0 |  | 0 | 0 |  | 0 |  | 0 | 0 |  | 0 | 0 | 0 | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0 |  | 1 | 2022-03-14T10:20:13 | 1358 | 2022-03-14T10:20:13 | 1358 |
| 00017d33d7754b1da9d9d77b76c25024 | 35ff9c3a-2b40-461e-b59d-f404183626ee |  | 2022 | 10 | 2.2.6 | 34 | 摊销费 | 5401020206 | 间接费 | 3 |  |  |  |  |  |  |  |  | 0 |  | 0 |  | 0 | 0 |  | 0 | 0 |  | 0 | 0 | 0 | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | 0 | 0 |  | 1 | 2022-10-25T20:31:25 | 1317 | 2022-10-25T20:31:25 | 1317 |
| 0001cbeaf5fa47a5a82b99fe8d4edfbd | c9804473-2560-403e-b88f-32d5be383208 | f67fc130-49b1-46e6-8268-39e34d733dbf | 2022 | 5 | 2.5 | 14 |  | 54010102:1 | 专业分包 | 3 | A01101139000022019007000 | 空调及防排烟工程劳务分包合同（天润） | 空调及防排烟工程劳务分包合同（天润） | 四川天润建筑劳务有限公司 | 30926260.6 | 0.8 | 0.03 | 2 | 2841621.29 |  | 2841621.29 | 0 |  | 0 | 1 | 2273297.032 | 1900000 | 0.6686 | 373297.032 | 941621.29 | 0 | 941621.29 |  |  |  | 0.6686 |  | 0.6686 |  |  |  |  |  |  |  | 0 | 941621.29 |  | 1 | 2022-06-13T10:26:55 | 3797 | 2022-06-13T10:26:55 | 3797 |
