# tb_project_risk_list_analyse

- 数据连接：`建工成本01`（ID: `duckdb__建工成本01`）
- 表标识：`tb_project_risk_list_analyse`
- 物理表名：`tb_project_risk_list_analyse`
- 导出时间：2026-06-10T10:40:50.139Z

## 字段结构

| 显示名 | 字段名 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- | --- |
| id | `id` | VARCHAR | 是 |  |
| project_id | `project_id` | VARCHAR | 是 |  |
| year | `year` | BIGINT | 是 |  |
| month | `month` | BIGINT | 是 |  |
| risk_type | `risk_type` | BIGINT | 是 |  |
| code | `code` | VARCHAR | 是 |  |
| name | `name` | VARCHAR | 是 |  |
| value | `value` | VARCHAR | 是 |  |
| value_type | `value_type` | BIGINT | 是 |  |
| value_remark | `value_remark` | VARCHAR | 是 |  |
| warning | `warning` | BIGINT | 是 |  |
| analyse_reason | `analyse_reason` | VARCHAR | 是 |  |
| analyse_correction | `analyse_correction` | VARCHAR | 是 |  |
| remark | `remark` | VARCHAR | 是 |  |
| status | `status` | BIGINT | 是 |  |
| create_time | `create_time` | TIMESTAMP | 是 |  |
| create_by | `create_by` | VARCHAR | 是 |  |
| update_time | `update_time` | TIMESTAMP | 是 |  |
| update_by | `update_by` | VARCHAR | 是 |  |

## 数据预览（前 10 行）

| id | project_id | year | month | risk_type | code | name | value | value_type | value_remark | warning | analyse_reason | analyse_correction | remark | status | create_time | create_by | update_time | update_by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0000c0655598426f8fb77dc668a92e32 | 5a69e6be-a2f1-4987-bf4c-80b71f05b487 | 2022 | 7 | 2 | 223 | 利润额 已确产值-(已确成本+待确成本) | 9619311.49983528 | 2 | ≥±100万元（在建项目）；≥目标利润额（完工项目） 受确权产值影响，需根据合同约定具体分析 | 3 |  |  |  | 1 | 2022-08-25T15:33:48 | 2372 | 2022-08-25T15:33:48 | 2372 |
| 0003b67f5d694b99b6bee5b512e25a0e | 3d8f17f7-3436-4106-a2e0-9f78e37f5f0c | 2021 | 10 | 1 | 110 | 开累产值完成额 | 195959121.5 | 2 |  | 3 |  |  |  | 1 | 2021-11-11T18:29:45 | 1317 | 2021-11-11T18:29:45 | 1317 |
| 0005465ff5204c92b34dc9e25fa39ab2 | 1f2051bd-8193-4aab-b591-f7905d729189 | 2023 | 4 | 1 | 110 | 开累产值完成额 | 60574944.68 | 2 |  | 3 |  |  |  | 1 | 2023-05-16T09:25:49 | 3547 | 2023-05-16T09:25:49 | 3547 |
| 00057d9489364361948811c3cafc8040 | d03529b0-0fab-4c7b-96dd-e2bf97c83e08 | 2022 | 7 | 3 | 310 | 施工图预算 |  | 1 | 1.是否按要求时间办理； 2.是否存在重大争议项 | 3 |  |  |  | 1 | 2022-08-16T14:25:26 | 5028 | 2022-08-16T14:25:26 | 5028 |
| 0006675634b04e75a6aa34f6aba1afd9 | aa3bf73d-0458-4bf3-964c-44d0f18e6554 | 2021 | 12 | 3 | 320 | 签证、索赔办理情况 |  | 1 | 描述办理情况及完成率； | 3 |  |  |  | 1 | 2022-01-13T18:44:20 | 3792 | 2022-01-13T18:44:20 | 3792 |
| 0007465ecaf743fa987c17468adca2f9 | be3b8072-d680-468e-881c-3bac9f7a4cd7 | 2023 | 5 | 3 | 340 | 业主结算 |  | 1 | 1.是否按要求时间办理； 2.是否存在重大争议项 | 3 |  |  |  | 1 | 2023-06-08T14:26:05 | 1317 | 2023-06-08T14:26:05 | 1317 |
| 0007c801b9144940bd3c5cd3835e5824 | 4fa8152c-1cc9-4d2b-b7f9-f2ebebd61a80 | 2021 | 12 | 2 | 220 | 利润率（%） （已确+待确） | 0.0540186737066361 | 2 | ≥±5%（在建项目）；≥目标利润率（完工项目） | 3 |  |  |  | 1 | 2022-01-14T13:48:16 | 4028 | 2022-01-14T13:48:16 | 4028 |
| 000876cdafb94c7fa80b86a46437b059 | b97f34ef-9beb-412c-8e77-d150214cae5c | 2022 | 1 | 3 | 350 | 目标成本 |  | 1 | 1.是否完成； 2.是否在目标管理范围内 | 3 |  |  |  | 1 | 2022-02-23T16:58:38 | 5889 | 2022-02-23T16:58:38 | 5889 |
| 00088e76188a4e7299551d348729e016 | 68215977-bce2-4cc6-9f7e-cb6e11a4de92 | 2021 | 11 | 3 | 310 | 施工图预算 |  | 1 | 1.是否按要求时间办理； 2.是否存在重大争议项 | 3 |  |  | 一期已结算，二期施工图预算未293737184.57元 | 1 | 2021-12-14T11:22:32 | 1297 | 2021-12-14T11:22:32 | 1297 |
| 000aef1b34174beb97e79961e806b032 | 45bbb495-fb63-427f-8073-c340fa7e421d | 2023 | 6 | 1 | 110 | 开累产值完成额 | 202377165.4 | 2 |  | 3 |  |  |  | 1 | 2023-07-11T08:50:07 | 5889 | 2023-07-11T08:50:07 | 5889 |
