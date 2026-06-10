# tb_cost_report_cell

- 数据连接：`建工成本01`（ID: `duckdb__建工成本01`）
- 表标识：`tb_cost_report_cell`
- 物理表名：`tb_cost_report_cell`
- 导出时间：2026-06-10T10:39:49.135Z

## 字段结构

| 显示名 | 字段名 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- | --- |
| id | `id` | VARCHAR | 是 |  |
| row_id | `row_id` | VARCHAR | 是 |  |
| row_num | `row_num` | BIGINT | 是 |  |
| column_num | `column_num` | BIGINT | 是 |  |
| colspan | `colspan` | DOUBLE | 是 |  |
| rowspan | `rowspan` | DOUBLE | 是 |  |
| style | `style` | VARCHAR | 是 |  |
| format | `format` | VARCHAR | 是 |  |
| value | `value` | VARCHAR | 是 |  |
| type | `type` | VARCHAR | 是 |  |
| data_type | `data_type` | BIGINT | 是 |  |
| locked | `locked` | BIGINT | 是 |  |
| meta | `meta` | VARCHAR | 是 |  |
| formula | `formula` | VARCHAR | 是 |  |
| formula_disabled | `formula_disabled` | BIGINT | 是 |  |
| status | `status` | BIGINT | 是 |  |
| create_by | `create_by` | VARCHAR | 是 |  |
| create_time | `create_time` | INTEGER | 是 |  |
| update_by | `update_by` | VARCHAR | 是 |  |
| update_time | `update_time` | TIMESTAMP | 是 |  |

## 数据预览（前 10 行）

| id | row_id | row_num | column_num | colspan | rowspan | style | format | value | type | data_type | locked | meta | formula | formula_disabled | status | create_by | create_time | update_by | update_time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0000121e8b6843b08d0ee5e37db411d6 | 26753ed797794be8ba1960e28b6eabc9 | 36 | 13 | 1 | 1 | {} | {"decimalLength":2,"zeroValue":true} | 0 | numeric | 5 | 2 |  | sumChildren() | 2 | 1 |  |  |  | 2021-01-20T11:36:33 |
| 000180db14fe41a185f48aa4c28a5b34 | ac9d74d64854423aaa3c327d555b34a2 | 5 | 7 | 1 | 1 | {} |  |  | text | 6 | 2 |  |  | 2 | 1 |  |  |  | 2021-02-06T10:07:07 |
| 000212287d22418cbb42ba48444e4cf9 | 09d8950273ea49ef817dd0599ef8fdba | 84 | 18 | 1 | 1 | {} | {"decimalLength":2} | 0 | numeric | 5 | 2 |  |  | 2 | 1 |  |  |  | 2021-01-21T11:36:27 |
| 0002281be9944a0c802590c94ac4b161 | c7a48c64746247119a8a6f1e27e1a942 | 90 | 22 | 1 | 1 | {} | {"decimalLength":2,"zeroValue":true,"showThousandsSeparator":true} | 0 | numeric | 5 | 2 |  | sumChildren() | 2 | 1 |  |  |  | 2021-03-05T08:44:32 |
| 0006ce199d4d4118bcc2d947dec3f646 | d392464ff2cb42c28cbbd51c110a96a2 | 99 | 1 | 1 | 1 | {} |  | 附加税费支出 | text | 6 | 2 |  |  | 2 | 1 |  |  |  | 2021-03-02T14:00:40 |
| 00075ce51fd44bc4864ee66cd32cb5d2 | 1e06f1f75a0744d4b899ff180e7a1d2d | 97 | 15 | 1 | 1 | {} | {"decimalLength":2,"zeroValue":true,"showThousandsSeparator":true} | 0 | numeric | 5 | 2 |  | sumChildren() | 2 | 1 |  |  |  | 2021-01-29T09:35:10 |
| 0007892bb6d24c29859a5d678389bb38 | 0a5fc8693db34e578eb82e5a84482da5 | 8 | 21 | 1 | 1 | {} | {"decimalLength":2,"zeroValue":true,"showThousandsSeparator":true} | 8874645.392499998 | numeric | 5 | 2 |  | {{idf07999bdf7cd4abca11d92b689fd0a81}} | 2 | 1 |  |  |  | 2021-02-01T11:02:59 |
| 00078aede5f642f782c577d78f245710 | 0f0e7976ba4a48d3b012be61d1ebe01e | 4 | 27 | 1 | 1 | {"textAlign":"center"} |  | 计划累计付款比例 | text | 6 | 2 |  |  | 2 | 1 |  |  |  | 2021-01-20T11:35:04 |
| 000820d97b874d18874f696b545bc2b5 | 15461f0842f54d7fbf7e8b461819da0b | 68 | 30 | 1 | 1 | {} |  |  | text | 6 | 2 |  |  | 2 | 1 |  |  |  | 2021-01-20T10:01:46 |
| 00091cad5f8f47159bcba4fadc5ce6a5 | 5c33b3c9ea0647fbabdff714efe824ec | 112 | 24 |  |  | {"fontWeight":600} |  |  | contract-theWay | 6 | 2 |  |  | 2 | 1 |  |  |  | 2021-01-28T11:52:24 |
