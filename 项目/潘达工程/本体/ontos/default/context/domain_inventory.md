# 域环境清单 · 本体引擎测试

> 由 **materialize / snapshotPull** 自平台域树生成 · `2026-06-13T12:22:27.211Z`

| 域 code | 域名称 | domainId |
| --- | --- | --- |
| `default` | 本体引擎测试 | `3dc87cac8ba94dad9d4b6b5460bf1494` |

## 数据表 (table)

- `产值事实表`
- `成本科目维表`
- `成本科目映射表`
- `成本事实表`
- `利润预算明细`
- `日期维表`
- `损益科目维表`
- `项目利润快照`
- `项目维表`
- `组织维表`

## Cube

- `产值分析Cube`
- `成本分析Cube`
- `利润预算Cube`
- `损益科目成本Cube`
- `项目利润Cube`
- `预实对比Cube`

## 对象类型 (object_type)

- `产值记录`
- `成本分析`
- `成本记录`
- `成本科目`
- `利润分析`
- `损益科目`
- `项目`
- `营收记录`
- `预算分析`
- `预算行`
- `组织`

## 链接 (link_type)

- `产值归属项目`
- `成本归属科目`
- `成本归属项目`
- `成本映射损益科目`
- `分析归因项目`
- `科目上级`
- `利润归因科目`
- `利润归因项目`
- `项目归属组织`
- `营收归属项目`
- `预算对比实际`
- `预算对应科目`
- `预算对应项目`
- `组织上级`

## 函数 (function)

- `成本 Top-N 项目`
- `成本极值与差值`
- `成本科目结构`
- `空间总览汇总`
- `片区成本汇总`
- `项目成本产值汇总`
- `项目预实对比`
- `profit01.fn.account_breakdown`
- `profit01.fn.budget_vs_actual`
- `profit01.fn.cost_type_breakdown`
- `profit01.fn.get_summary`
- `profit01.fn.org_profit`
- `profit01.fn.project_profit`
- `profit01.fn.region_profit`
- `semantic.query_aggregate`

## 表间关系 (relation)

- `142a9528d4744e00`
- `16dc44913e624df0`
- `18136dfde8c441f7`
- `486232c65a324a52`
- `5f82a3a6df37490f`
- `66ef982497c84fa6`
- `6b794f2db79d43f6`
- `8544ad0bcdae444f`
- `8807aaefae304af0`
- `8fadbf1d5f4f4528`
- `a103174bb0d9404c`
- `a2e7ca1ecd11428e`
- `ad25ee5c2aa64ad4`
- `b4d365af8cb74ad8`
- `c0a822401ce74c45`
- `c0bd3324a8354706`
- `d2170c4941a047be`
- `d3201f3ad71d45fd`
- `ebe7301d6adc45f2`
- `edccb8ca632f467b`

## 脚本 (script)

- `onto_engine_fn_budget_vs_actual`
- `onto_engine_fn_cost_extremes`
- `onto_engine_fn_cost_structure`
- `onto_engine_fn_get_summary`
- `onto_engine_fn_project_summary`
- `onto_engine_fn_region_cost`
- `onto_engine_fn_top_cost_projects`
- `onto_engine_test_category_mount`
- `onto_engine_test_engine_verify`
- `onto_engine_test_engine_verify_advanced`
- `onto_engine_test_function_rules_seed`
- `onto_engine_test_functions_register`
- `onto_engine_test_graph_verify`
- `onto_engine_test_meta_seed`
- `onto_engine_test_ontology_init`
- `onto_engine_test_seed_data`
- `profit01_category_mount`
- `profit01_fn_account_breakdown`
- `profit01_fn_budget_vs_actual`
- `profit01_fn_cost_type_breakdown`
- `profit01_fn_get_summary`
- `profit01_fn_org_profit`
- `profit01_fn_project_profit`
- `profit01_fn_region_profit`
- `profit01_ontology_init`
- `profit01_seed_data`

## 流程 (workflow)

（无域成员或未挂载）

## 应用组件 (component)

（无域成员或未挂载）

## 智能体必读

1. 本文件为 **当前平台环境真源**；写 gap 补丁前须对照此处与 `plans/training/gap_*.md`。
2. **禁止**无 gap 理由重写整域 init；优先最小补丁（函数 / category_mount / 单表）。
3. 刷新：`dazi onto domain snapshot-pull --onto-dir <本实现>` 或侧栏 **🔄 刷新域快照**。
