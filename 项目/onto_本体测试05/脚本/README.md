# 脚本

库存本体 Python 脚本（`space__0519`）。

## 目录结构

```text
脚本/
├── main.py
├── setup/
│   ├── inventory_ontology_init.py   # 建表 + Cube + 本体定义
│   └── inventory_seed_data.py         # 演示数据灌入
└── functions/
    ├── inventory_fn_get_summary.py
    ├── inventory_fn_low_stock_alerts.py
    ├── inventory_fn_warehouse_breakdown.py
    ├── inventory_fn_movement_trace.py
    ├── inventory_fn_turnover_rank.py
    ├── inventory_fn_abc_classification.py
    └── inventory_fn_compare_production_kpi.py
```

## 执行顺序

> **重要**：`script publish` 只上传脚本代码；**表、Cube、本体对象** 须再执行 **`script run`**（或侧栏「运行脚本」）才会落库。仅发布函数时侧栏只能看到函数，看不到表与对象类型。

在工作区根目录终端执行（需已 `dazi auth login`，推荐用 `.\scripts\dazi.ps1`）：

```powershell
# 1a. 发布初始化脚本
.\scripts\dazi.ps1 onto script publish 项目/onto_本体测试05/脚本/setup/inventory_ontology_init.py --space space__0519

# 1b. 执行初始化（建表 + 注册表 + Cube + 6 种对象类型 + 10 条链接）— 必做
.\scripts\dazi.ps1 onto script run --script-id <init 的 scriptId> --space space__0519

# 2a. 发布灌数脚本
.\scripts\dazi.ps1 onto script publish 项目/onto_本体测试05/脚本/setup/inventory_seed_data.py --space space__0519

# 2b. 执行灌数 — 必做
.\scripts\dazi.ps1 onto script run --script-id <seed 的 scriptId> --space space__0519

# 3. 发布并注册分析函数（示例）
.\scripts\dazi.ps1 onto script publish 项目/onto_本体测试05/脚本/functions/inventory_fn_get_summary.py `
  --space space__0519 --register-function-id inventory.fn.get_summary

.\scripts\dazi.ps1 onto function run inventory.fn.get_summary --space space__0519 --params '{}'
```

**当前环境已执行的 scriptId（2026-05-26）**：

| 步骤 | scriptId |
| --- | --- |
| 初始化 | `00efcf01-8089-47b3-8db9-32381929dc76` |
| 灌数 | `4fc85139-c2e8-4b4b-9884-1edf13d92941` |

侧栏刷新：在 **数据资源 → 数据空间0519** 上右键刷新；本体对象在 **Onto 本体** 视图中查看 `InventoryItem`、`Warehouse` 等。

亦可在侧栏 **Onto 本体** 选择脚本发布/运行。

## 函数 ID 一览

| 函数 ID | 脚本文件 |
| --- | --- |
| `inventory.fn.get_summary` | `functions/inventory_fn_get_summary.py` |
| `inventory.fn.low_stock_alerts` | `functions/inventory_fn_low_stock_alerts.py` |
| `inventory.fn.warehouse_breakdown` | `functions/inventory_fn_warehouse_breakdown.py` |
| `inventory.fn.movement_trace` | `functions/inventory_fn_movement_trace.py` |
| `inventory.fn.turnover_rank` | `functions/inventory_fn_turnover_rank.py` |
| `inventory.fn.abc_classification` | `functions/inventory_fn_abc_classification.py` |
| `inventory.fn.compare_production_kpi` | `functions/inventory_fn_compare_production_kpi.py` |

## 参考

- [本体脚本编写指南](../../资源/docs/onto/本体脚本编写指南.md)
- [库存本体分析方案](../规划/库存本体分析方案.md)
