# 本体规划03（阶段二 V3.0 对齐版）

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 数据空间 | 潘达工程 |
| 数据空间 ID | `space__panda_construction`（重建后沿用或新建空间后改脚本内 space_id） |
| 规划真理源 | 阶段二 V3.0：`020-本体规划文档.md`、`010-物理表设计文档.md`、`030-派生属性定义.md` |
| 与本体规划02 关系 | **独立实现单元**；V3 采用 20 对象 / 20 表，替代 region/owner 维，新增 bond/receipt 等 |

## 目录

- `plans/` — V3 标准本体方案
- `setup/` — `panda_cost_v3_ontology_init.py` / `panda_cost_v3_seed_data.py` / `panda_cost_v3_category_mount.py`
- `functions/` — `panda_cost_v3_fn_*.py`（function id 仍为 `panda_cost.fn.*`）

## 实施顺序

```
重建数据空间 → init → seed → 发布全部函数 → save_test_arguments → category_mount
```

## 发布命令（在 dazi-work 根目录）

```powershell
# 1. 初始化
dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划03/setup/panda_cost_v3_ontology_init.py --space space__panda_construction --type setup
dazi onto script run --file 项目/潘达工程-商务成本/本体/ontos/本体规划03/setup/panda_cost_v3_ontology_init.py --space space__panda_construction

# 2. 灌数
dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划03/setup/panda_cost_v3_seed_data.py --space space__panda_construction --type data
dazi onto script run --file 项目/潘达工程-商务成本/本体/ontos/本体规划03/setup/panda_cost_v3_seed_data.py --space space__panda_construction

# 3. 函数（示例）
dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划03/functions/panda_cost_v3_fn_get_summary.py --space space__panda_construction --register-function-id panda_cost.fn.get_summary

# 4. 测试参数
.\项目\潘达工程-商务成本\本体\ontos\本体规划03\functions\save_test_arguments.ps1

# 5. 分类挂载（最后）
dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划03/setup/panda_cost_v3_category_mount.py --space space__panda_construction --type setup
dazi onto script run --file 项目/潘达工程-商务成本/本体/ontos/本体规划03/setup/panda_cost_v3_category_mount.py --space space__panda_construction
```
