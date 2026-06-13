# 本体引擎测试空间 · 本体函数

空间：`space__onto_engine_test`

## 函数清单

| function_id | 脚本 | 锚定对象 | 用途 |
|---|---|---|---|
| `onto_engine.fn.get_summary` | `onto_engine_fn_get_summary.py` | CostAnalysis | 空间总览（成本/预算/产值/执行率） |
| `onto_engine.fn.project_summary` | `onto_engine_fn_project_summary.py` | Project | 各项目成本+产值+毛利 |
| `onto_engine.fn.region_cost` | `onto_engine_fn_region_cost.py` | Project | 按片区汇总（锚点：按片区看本月开销） |
| `onto_engine.fn.budget_vs_actual` | `onto_engine_fn_budget_vs_actual.py` | CostAnalysis | 项目预实对比/超支筛选 |
| `onto_engine.fn.top_cost_projects` | `onto_engine_fn_top_cost_projects.py` | Project | 成本 Top-N（配合 rank_cost_topn 规则） |
| `onto_engine.fn.cost_extremes` | `onto_engine_fn_cost_extremes.py` | Project | 成本最高/最低项目及差值 |
| `onto_engine.fn.cost_structure` | `onto_engine_fn_cost_structure.py` | CostRecord | 成本科目结构占比 |

## 发布（在 dazi-work 根目录）

```powershell
$SP = "space__onto_engine_test"
$FN = "项目/DAZI_TEST/本体/ontos/引擎测试/functions"

# 使用 dazi-onto（dazi onto 不转发 --register-platform-category）
dazi-onto script publish $FN/onto_engine_fn_get_summary.py --space $SP --register-function-id onto_engine.fn.get_summary --register-platform-category 总览分析
dazi-onto script publish $FN/onto_engine_fn_project_summary.py --space $SP --register-function-id onto_engine.fn.project_summary --register-platform-category 组织分析
dazi-onto script publish $FN/onto_engine_fn_region_cost.py --space $SP --register-function-id onto_engine.fn.region_cost --register-platform-category 组织分析
dazi-onto script publish $FN/onto_engine_fn_budget_vs_actual.py --space $SP --register-function-id onto_engine.fn.budget_vs_actual --register-platform-category 预实分析
dazi-onto script publish $FN/onto_engine_fn_top_cost_projects.py --space $SP --register-function-id onto_engine.fn.top_cost_projects --register-platform-category 结构分析
dazi-onto script publish $FN/onto_engine_fn_cost_extremes.py --space $SP --register-function-id onto_engine.fn.cost_extremes --register-platform-category 结构分析
dazi-onto script publish $FN/onto_engine_fn_cost_structure.py --space $SP --register-function-id onto_engine.fn.cost_structure --register-platform-category 结构分析
```

## 锚定与规则（publish 之后）

```powershell
$BASE = "项目/DAZI_TEST/本体/ontos/引擎测试/setup"

dazi onto script publish $BASE/onto_engine_test_functions_register.py --space $SP --type setup
dazi onto script run --file $BASE/onto_engine_test_functions_register.py --space $SP

dazi onto script publish $BASE/onto_engine_test_function_rules_seed.py --space $SP --type data
dazi onto script run --file $BASE/onto_engine_test_function_rules_seed.py --space $SP
```

`function_rules_seed` 新增 4 条 **annotate** 规则，在问句命中时写入 `suggested_function_id`，与 `meta_seed` 中 rank/超支规则互补。

## 测试参数（test_arguments，已入库）

本地 JSON：`functions/test_arguments/onto_engine.fn.*.json`

```powershell
$TA = "项目/DAZI_TEST/本体/ontos/引擎测试/functions/test_arguments"
dazi-onto function save-test-arguments --function-id onto_engine.fn.region_cost `
  --space $SP --arguments-json-file "$TA/onto_engine.fn.region_cost.json"
# 其余 5 个函数同理
```

侧栏 **Onto → 运行函数** 将预填已保存参数。
