# tb_project_major_cost

- 数据连接：`建工成本01`（ID: `duckdb__建工成本01`）
- 表标识：`tb_project_major_cost`
- 物理表名：`tb_project_major_cost`
- 导出时间：2026-06-05T14:41:48.079Z

## 字段结构

| 显示名 | 字段名 | 类型 | 可空 |
| --- | --- | --- | --- |
| id | `id` | VARCHAR | 是 |
| project_id | `project_id` | VARCHAR | 是 |
| year | `year` | BIGINT | 是 |
| month | `month` | BIGINT | 是 |
| code | `code` | VARCHAR | 是 |
| name | `name` | VARCHAR | 是 |
| scope | `scope` | VARCHAR | 是 |
| target_cost_amount | `target_cost_amount` | DOUBLE | 是 |
| target_cost_of_m3 | `target_cost_of_m3` | DOUBLE | 是 |
| contract_amount | `contract_amount` | DOUBLE | 是 |
| contract_amount_of_m3 | `contract_amount_of_m3` | DOUBLE | 是 |
| incurred_cost_amount | `incurred_cost_amount` | DOUBLE | 是 |
| incurred_cost_amount_of_m3 | `incurred_cost_amount_of_m3` | DOUBLE | 是 |
| incurred_cost_confirmed | `incurred_cost_confirmed` | DOUBLE | 是 |
| incurred_cost_confirmed_of_m3 | `incurred_cost_confirmed_of_m3` | DOUBLE | 是 |
| warning | `warning` | BIGINT | 是 |
| analyse_reason | `analyse_reason` | VARCHAR | 是 |
| remark | `remark` | VARCHAR | 是 |
| status | `status` | BIGINT | 是 |
| create_time | `create_time` | TIMESTAMP | 是 |
| create_by | `create_by` | VARCHAR | 是 |
| update_time | `update_time` | TIMESTAMP | 是 |
| update_by | `update_by` | VARCHAR | 是 |

## 数据预览（前 10 行）

| id | project_id | year | month | code | name | scope | target_cost_amount | target_cost_of_m3 | contract_amount | contract_amount_of_m3 | incurred_cost_amount | incurred_cost_amount_of_m3 | incurred_cost_confirmed | incurred_cost_confirmed_of_m3 | warning | analyse_reason | remark | status | create_time | create_by | update_time | update_by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 00032f4c98e6493ba4b849b8cb9aaf3a | 3501290c-e094-4fba-9002-d856545ae77d | 2022 | 7 | 50 | 水电费用 |  |  | 0 |  | 0 |  | 0 |  | 0 | 3 | 1.存在问题： 2.改进措施： |  | 1 | 2022-08-22T09:48:48 | 3382 | 2022-08-22T09:48:48 | 3382 |
| 0003539061a14c808efb5ebcc9441a53 | eb695f69-4b81-4501-b4a5-b582e153ca83 | 2022 | 4 | 40 | 安全文明费用 | 临时设施、安全、文明、环境保护 |  | 0 |  | 0 |  | 0 |  | 0 | 3 | 1.存在问题： 2.改进措施： |  | 1 | 2022-05-11T12:14:34 | 3637 | 2022-05-11T12:14:34 | 3637 |
| 0005773d4066477aaa9cebf6b97708c9 | 97b78498-8c97-47c7-93ed-d1edb08008ed | 2023 | 8 | 50 | 水电费用 |  |  | 0 |  | 0 |  | 0 |  | 0 | 3 | 1.存在问题： 2.改进措施： |  | 1 | 2023-09-13T10:54:27 | 5889 | 2023-09-13T10:54:27 | 5889 |
| 00073fd57a3d491b8df4776ca044c2d0 | 01cbd0f4-2e8a-43f9-96f6-44e298795db5 | 2022 | 4 | 30 | 土建劳务费用 |  |  | 0 |  | 0 |  | 0 |  | 0 | 3 | 1.存在问题： 2.改进措施： |  | 1 | 2022-05-07T16:00:54 | 3797 | 2022-05-07T16:00:54 | 3797 |
| 00089d36f1ea47b9bf1c649e3f2a927d | 722fbfb4-bf77-4ccc-80e1-633f125a42a5 | 2022 | 4 | 10 | 周转材费用 | 模板、木枋、架管、扣件、矩管、铝模、爬架等 |  | 0 |  | 0 |  | 0 |  | 0 | 3 | 1.存在问题： 2.改进措施： |  | 1 | 2022-06-06T15:18:31 | 2404 | 2022-06-06T15:18:31 | 2404 |
| 000a0e493e8c4855b549432833b2cf90 | abcfc933-2eef-48fb-a55f-c829b699169a | 2023 | 12 | 30 | 土建劳务费用 |  |  | 0 |  | 0 |  | 0 |  | 0 | 3 | 1.存在问题： 2.改进措施： |  | 1 | 2024-01-19T08:42:50 | 4975 | 2024-01-19T08:42:50 | 4975 |
| 000e423ec0e848a5b49f4550a37d69e7 | 7f331521-6c75-4bc5-b448-1c352244fb43 | 2021 | 7 | 60 | 间接费用 |  |  | 0 |  | 0 |  | 0 |  | 0 | 3 | 1.存在问题： 2.改进措施： |  | 1 | 2021-08-19T14:35:17 | 3755 | 2021-08-19T14:35:17 | 3755 |
| 001548f97d5b4ce59defb77adc54c0c1 | 18235636-337e-43e9-a4be-4cca94e5f48a | 2022 | 10 | 60 | 间接费用 |  |  |  |  |  |  |  |  |  | 3 | 1.存在问题： 2.改进措施： |  | 1 | 2022-11-09T15:58:15 | 1297 | 2022-11-09T15:58:15 | 1297 |
| 001669aace5c401e91bc74dfde94b1a1 | 10daa78d-ada6-4123-87a2-94981d7708aa | 2023 | 4 | 10 | 周转材费用 | 模板、木枋、架管、扣件、矩管、铝模、爬架等 |  | 0 |  | 0 |  | 0 |  | 0 | 3 | 1.存在问题： 2.改进措施： |  | 1 | 2023-05-08T16:48:56 | 3159 | 2023-05-08T16:48:56 | 3159 |
| 001875158f2d4559837e3fb5b0af8669 | 3bdaf591-3e1b-4a14-b4a5-9fb7fb256f11 | 2023 | 11 | 60 | 间接费用 |  |  | 0 |  | 0 |  | 0 |  | 0 | 3 | 1.存在问题： 2.改进措施： |  | 1 | 2023-12-20T14:22:55 | 5257 | 2023-12-20T14:22:55 | 5257 |
