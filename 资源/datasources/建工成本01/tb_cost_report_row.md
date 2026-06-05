# tb_cost_report_row

- 数据连接：`建工成本01`（ID: `duckdb__建工成本01`）
- 表标识：`tb_cost_report_row`
- 物理表名：`tb_cost_report_row`
- 导出时间：2026-06-05T14:41:28.352Z

## 字段结构

| 显示名 | 字段名 | 类型 | 可空 |
| --- | --- | --- | --- |
| id | `id` | VARCHAR | 是 |
| parent_id | `parent_id` | VARCHAR | 是 |
| area | `area` | DOUBLE | 是 |
| report_id | `report_id` | VARCHAR | 是 |
| sheet_id | `sheet_id` | VARCHAR | 是 |
| type | `type` | BIGINT | 是 |
| meta | `meta` | VARCHAR | 是 |
| removable | `removable` | BIGINT | 是 |
| num | `num` | BIGINT | 是 |
| level | `level` | BIGINT | 是 |
| style | `style` | VARCHAR | 是 |
| additions | `additions` | INTEGER | 是 |
| remark | `remark` | INTEGER | 是 |
| status | `status` | BIGINT | 是 |
| create_by | `create_by` | VARCHAR | 是 |
| create_time | `create_time` | INTEGER | 是 |
| update_by | `update_by` | VARCHAR | 是 |
| update_time | `update_time` | TIMESTAMP | 是 |

## 数据预览（前 10 行）

| id | parent_id | area | report_id | sheet_id | type | meta | removable | num | level | style | additions | remark | status | create_by | create_time | update_by | update_time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 00013a5f0aba4d08817c89108c826304 | 0 | 2 | d5986a3693854d5c99f8b92e7357aac7 | 5b1a659621664c569753f2e42f41502a | 2 |  | 1 | 94 | 1 | {} |  |  | 1 |  |  |  | 2021-03-17T09:26:56 |
| 005d0b6833fb40f1a6208ad4c223ff0a | 0 | 1 | 93828997774a4d829d0f4b558e7ef92f | 52a1b04356b44762befac1b010280e5f | 1 |  | 1 | 47 | 1 | {} |  |  | 1 |  |  |  | 2021-01-21T14:16:31 |
| 0067fde4701e43f7b34322f1d8c8ac84 | e5d55bd25b0645e19895dc530932a787 | 2 | f2270cffabd541b6afb4323c384164e1 | a10cae3070eb4118a0761ddf14bad968 | 2 | d6e650cc-860f-49a5-a87b-a3b65a933b9b | 1 | 65 | 3 |  |  |  | 1 |  |  |  | 2021-01-29T09:35:10 |
| 007daa42323d4c89ba63ae311178aa66 | c1cf21551b9a4609bb88947b25d9a29b | 2 | dac2a514022f4cbf9ad473b030e080a0 | 20b09d72126a46debafe8c54139b3038 | 2 | 45f7c434-80c0-4b05-91c7-52039a2ce751 | 1 | 46 | 3 | {} |  |  | 1 |  |  |  | 2021-02-01T11:02:59 |
| 00adc30fce9e42539a6cd2296f8deade | 0 | 1 | a32fb07f54c3497992e7d5337c6bd0bc | da8f9cf00d4f4bdaa105c44028460d43 | 2 |  | 1 | 9 | 1 | {} |  |  | 1 |  |  |  | 2021-01-20T11:36:33 |
| 00b8fc6f4cf74d95bde53ceec777f1c4 | 0 | 1 | d5986a3693854d5c99f8b92e7357aac7 | 810889ffe93245d48200adcea23d21b7 | 1 | r[2] | 2 | 55 | 1 | {} |  |  | 1 |  |  |  | 2021-03-03T14:14:56 |
| 00c5459728d54ebdb8e234966fe57599 | 8e0ec1b9f90f4404b031edba25b9fe17 | 2 | db22fa0bca6e476593373c7b09663dc9 | b90b18734f8a45199d1b7242b7210184 | 2 |  | 1 | 24 | 3 | {} |  |  | 1 |  |  |  | 2021-01-21T16:14:34 |
| 00d3738649d5458d8a000a85e21be402 | 0 | 2 | 7d4fea490edc4d959e5acd9b76e8b64d | 682e0395f74e4deab0b2d053acfac25a | 2 | r项目收支汇总表[2] | 2 | 0 | 1 | {} |  |  | 1 |  |  |  | 2021-01-19T18:05:11 |
| 00deb37627264ad98dc4d6158cdce1ee | 71b632f0f263447a954642209e8b2528 | 2 | ff3f098d949347009ee26161fe69785d | 501a69234da1472ca0acf9ae196f37a0 | 2 |  | 1 | 44 | 2 | {} |  |  | 1 |  |  |  | 2021-01-25T18:23:58 |
| 00e08a8a3549494a98bdadfd04792d08 | 0 | 1 | 4598d5dfed92448b800295f6943459dc | 296effb9224d42a1ab2e30e343e5646c | 1 |  | 1 | 4 | 1 | {} |  |  | 1 |  |  |  | 2021-01-29T08:49:02 |
