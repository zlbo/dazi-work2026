# tb_cost_report_view_model_definition_item

- 数据连接：`建工成本01`（ID: `duckdb__建工成本01`）
- 表标识：`tb_cost_report_view_model_definition_item`
- 物理表名：`tb_cost_report_view_model_definition_item`
- 导出时间：2026-06-05T14:41:31.739Z

## 字段结构

| 显示名 | 字段名 | 类型 | 可空 |
| --- | --- | --- | --- |
| id | `id` | VARCHAR | 是 |
| view_model_definition_id | `view_model_definition_id` | VARCHAR | 是 |
| title | `title` | VARCHAR | 是 |
| code | `code` | VARCHAR | 是 |
| binding_type | `binding_type` | BIGINT | 是 |
| meta | `meta` | VARCHAR | 是 |
| editable | `editable` | DOUBLE | 是 |
| role_codes | `role_codes` | VARCHAR | 是 |
| index | `index` | BIGINT | 是 |
| remark | `remark` | VARCHAR | 是 |
| status | `status` | BIGINT | 是 |
| create_time | `create_time` | TIMESTAMP | 是 |
| create_by | `create_by` | VARCHAR | 是 |
| update_time | `update_time` | TIMESTAMP | 是 |
| update_by | `update_by` | VARCHAR | 是 |

## 数据预览（前 10 行）

| id | view_model_definition_id | title | code | binding_type | meta | editable | role_codes | index | remark | status | create_time | create_by | update_time | update_by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 003bdfbcdb904d4dbc1bf9a577e7b314 | 26f45883bab9400f932d5debccdc7419 | 产值_本月完成_待确认 | output_actual_unconfirmed_cmonth | 1 | {"dataType":"number"} | 1 | fgssw,gssw,xmbtb | 383 | 表3.1(1.8) | 1 | 2021-12-16T09:47:34 | 1319 | 2021-12-16T09:47:34 | 1319 |
| 006f6e14e77246989d96b23bf29b22f6 | 26f45883bab9400f932d5debccdc7419 | 合同编号(pkpm) | project_contract_no | 1 | {"dataType":"string"} | 2 | base_user | 26 |  | 1 | 2021-12-16T09:47:34 | 1319 | 2021-12-16T09:47:34 | 1319 |
| 02a54d342112467f9e609b849d8be056 | 26f45883bab9400f932d5debccdc7419 | 欠公司管理费 | management_fee_debt | 1 | {"dataType":"number"} | 1 | fgscw,gscw | 71 | 表2 | 1 | 2021-12-16T09:47:34 | 1319 | 2021-12-16T09:47:34 | 1319 |
| 03f63948a54a443aa13bb7d766c4513d | 0a512e70f5f94e149a157cfa0915e8b8 | 指标_成本资金支出比 | indicator_cbzjzcb | 1 | {"dataType":"number"} | 3 | gscw,fgscw,gssw | 183 | 表3(6.7) | 2 | 2021-05-31T14:17:32 | 1319 | 2021-06-09T10:25:07 | 1319 |
| 042daff3957749d8ac0c124cdd754bf3 | 26f45883bab9400f932d5debccdc7419 | 成本支出_间接成本 | outcome_cost_indirection | 1 | {"dataType":"number"} | 1 | gscw,fgscw | 289 | 表3(8.2.8) | 1 | 2021-12-16T09:47:34 | 1319 | 2021-12-16T09:47:34 | 1319 |
| 049629b291de458e8f6dbc5be7027065 | 26f45883bab9400f932d5debccdc7419 | 应收未收款_合约_质保金扣款原因 | ysws_contract_retention_cut_reason | 1 | {"dataType":"number"} | 1 | xmbtb | 957 | 表3.1.2(5.1.4) | 1 | 2021-12-17T16:41:40 | 1319 | 2022-01-15T10:21:51 | 1319 |
| 0622517d34ab4ee4a25bd3350cee4c6b | 26f45883bab9400f932d5debccdc7419 | sheet_3_1_备注 | sheet_3_1_remark | 1 | {"dataType":"string"} |  | gscw,fgscw | 421 | 表3.1 | 1 | 2021-12-16T09:47:34 | 1319 | 2021-12-16T09:47:34 | 1319 |
| 06a9fb7f1919424e81cd8299c0d55d45 | 0a512e70f5f94e149a157cfa0915e8b8 | 借款本金返回_公司借票据返还（兑付） | outcome_principal_return_bill | 1 | {"dataType":"number"} | 1 | gscw,fgscw | 307 | 表3(8.3.3) | 2 | 2021-05-31T14:17:36 | 1319 | 2021-06-09T10:38:59 | 1319 |
| 07b7da1e7b4c4d06bd5ccb7deaeee0e0 | 26f45883bab9400f932d5debccdc7419 | 质保金到期时间_第二阶段 | retention_due_date_two | 1 | {"dataType":"date"} | 2 | xmbtb,fgssw,gssw | 925 | 表3.1.2(2.2.3) | 1 | 2021-12-17T15:07:41 | 1319 | 2022-04-17T10:37:43 | 1317 |
| 089cf44f013c4e6c82e6c2529c821c0e | 0a512e70f5f94e149a157cfa0915e8b8 | 项目名称 | project_name | 1 | {"dataType":"string"} | 2 | base_user | 3 |  | 2 | 2021-05-31T14:17:29 | 1319 | 2021-05-31T14:17:29 | 1319 |
