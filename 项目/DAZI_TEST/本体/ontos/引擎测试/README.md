# 本体引擎测试空间

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 数据空间 | 本体引擎测试 |
| 数据空间 ID | `space__onto_engine_test` |
| 规划文档 | `dazi/docs2/规划/018-本体引擎测试场景方案.md` |

## 目录

- `setup/` — 初始化、灌数、元数据（同义词/层级/规则）、函数锚定、引擎验证脚本
- `functions/` — 6 个 `onto_engine.fn.*` 本体函数（见 `functions/README.md`）

## 实施顺序（强制）

在 `dazi-work` 根目录执行：

```powershell
$SP = "space__onto_engine_test"
$BASE = "项目/DAZI_TEST/本体/ontos/引擎测试/setup"

dazi onto script publish $BASE/onto_engine_test_ontology_init.py --space $SP --type setup
dazi onto script run --file $BASE/onto_engine_test_ontology_init.py --space $SP

dazi onto script publish $BASE/onto_engine_test_seed_data.py --space $SP --type data
dazi onto script run --file $BASE/onto_engine_test_seed_data.py --space $SP

dazi onto script publish $BASE/onto_engine_test_meta_seed.py --space $SP --type data
dazi onto script run --file $BASE/onto_engine_test_meta_seed.py --space $SP

dazi onto script publish $BASE/onto_engine_test_category_mount.py --space $SP --type setup
dazi onto script run --file $BASE/onto_engine_test_category_mount.py --space $SP

dazi onto script publish $BASE/onto_engine_test_engine_verify.py --space $SP --type data
dazi onto script run --file $BASE/onto_engine_test_engine_verify.py --space $SP

dazi onto script publish $BASE/onto_engine_test_engine_verify_advanced.py --space $SP --type data
dazi onto script run --file $BASE/onto_engine_test_engine_verify_advanced.py --space $SP

dazi onto script publish $BASE/onto_engine_test_graph_verify.py --space $SP --type data
dazi onto script run --file $BASE/onto_engine_test_graph_verify.py --space $SP
```

**本体函数（可选，增强域赋能与 G3 函数意图规则）**：

```powershell
$FN = "项目/DAZI_TEST/本体/ontos/引擎测试/functions"
# 逐条 publish，见 functions/README.md

dazi onto script publish $BASE/onto_engine_test_functions_register.py --space $SP --type setup
dazi onto script run --file $BASE/onto_engine_test_functions_register.py --space $SP

dazi onto script publish $BASE/onto_engine_test_function_rules_seed.py --space $SP --type data
dazi onto script run --file $BASE/onto_engine_test_function_rules_seed.py --space $SP
```

验收：
- 基础：`onto_engine_test_engine_verify` → `failed=0`（12 项单点能力）
- 高级：`onto_engine_test_engine_verify_advanced` → `failed=0`（10 项多步骤 G2~G5 + 7 项「为什么」可解释推理）
- **图谱**：`onto_engine_test_graph_verify` → `failed=0`（OntologyGraph/networkx 结构不变式）
- **单元**：`pytest tests/test_ontology_engine_graph.py`（fake DB，networkx 结构）
