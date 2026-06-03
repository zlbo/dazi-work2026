# 流程变量系统指南

**文档 ID**: `flow/variables-guide`  
**适用**: `dazi-vscode` 流程项目、`python-script` / `sql-query` 等代码节点  
**概念来源**: 搭子数据流程引擎统一变量模型（对齐 devend《011》），详见 `dazi/docs/279-dazi-dataflow数据流程功能总结.md` §3

**相关文档**

- [数据流程项目开发指南](./flow-project-guide.md) — 目录、`debug_run_id`、开发循环
- [节点代码编写指南](./node-code-guide.md) — 各节点 `code.*` 约定
- [Flow 运行与测试](./run-guide.md) — `node-exec`、`variable pull/sync`

---

## 1. 什么是流程变量

流程引擎把 **参数、中间表、最终结果** 统一抽象为 **变量（Variable）**，在一次 Run 内按 **变量名** 读写，而不必处处依赖画布连线传递文件路径。

| 概念           | 说明                                                                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **变量名**     | 字符串标识，如 `sales_raw`、`V1`、`销售表`；由节点配置 **`output_variable_name`** 或脚本 **`set_table_output` / `set_scalar_output`** 登记 |
| **变量作用域** | 绑定到某次 **`flow_runs`**；日常调试对应 **`ads_flows.debug_run_id`**                                                                      |
| **登记时机**   | 节点执行成功后，引擎读取 **`output_variable_name`**，将输出写入当前 Run 的 **`flow_run_variables`**                                        |

**本地开发时**：变量不在 `flow.json` 里，而在调试 Run 中；CLI/扩展通过 API 拉取 schema + 预览到 **`变量/<名>.json`**。

---

## 2. 存储类型

| 类型                | 典型场景                             | 存储                              | `get_variable` 行为                      |
| ------------------- | ------------------------------------ | --------------------------------- | ---------------------------------------- |
| **table（表变量）** | SQL 结果、Python `result_df`、文件源 | Parquet 落盘，库中 `value` 为路径 | 自动 `pd.read_parquet` → **`DataFrame`** |
| **text（标量）**    | 计数、标志位、质检综合分             | 库中 `value` 为字符串             | 返回 Python 原生值（str/int/float 等）   |

表变量是流程开发中最常用的类型；标量多用于质检分数、状态位等。

---

## 3. 产生变量：`output_variable_name`

在 **设计器属性面板** 或 `flow.json` → 节点 `data` 中配置：

```json
{
  "type": "custom",
  "data": {
    "type": "sql-query",
    "output_variable_name": "sales_clean",
    "connectionId": "..."
  }
}
```

**规则**

1. 节点成功执行后，引擎以 **`output_variable_name`** 为键登记变量（表 → Parquet 路径）。
2. 下游节点通过 **同名** 引用该变量（SQL 表名 / Python `get_variable('sales_clean')`）。
3. 变量名须 **全流程内唯一**；建议英文+下划线，中文名也支持（SQL 会自动加双引号）。
4. 未配置 `output_variable_name` 的节点，输出不会进入变量表（仍可能有入边 Parquet，但不便于单节点调试）。

**Python 多表输出**

- 主表：赋值 **`result_df`**（与 `output_variable_name` 对应）。
- 附加表：**`set_table_output('other_table', df)`**（`excel-python` 主输出也须 `set_table_output` 与 `output_variable_name` 同名）。

**标量输出**：**`set_scalar_output('score', 95.5)`**，变量名由画布质检配置或业务约定。

---

## 4. 变量从哪里来、怎么查看

```text
单节点测试 / 整流程运行
        │
        ▼
GET /flows/{id}/debug-run  →  绑定 ads_flows.debug_run_id
        │
        ▼
节点成功 → 写入 flow_run_variables（name = output_variable_name）
        │
        ▼
本地：flow variable pull/sync → 变量/<name>.json
```

```powershell
cd "项目\flow_xxx\流程\MyFlow"

# 先运行产出变量的上游节点，或整流程 debug
dazi flow run node-exec --node <上游uuid> --dir .

# 拉取单个变量（列信息 + 前 10 行）
dazi flow variable pull --name sales_clean --dir .

# 同步调试 Run 中全部变量
dazi flow variable sync --dir .
```

- 设计器：选中节点 → **`output_variable_name`** 旁 **📊**
- 资源管理器：**`变量/<名>.json`**（只读派生，勿手改后当真理源）
- 变量尚未产出时，占位 JSON 会提示：**先运行上游节点**

---

## 5. 管线示例：变量如何串联

典型链路 **Excel → SQL → Python**（变量名需在画布上事先约定）：

```text
[excel-import]     output_variable_name = excel_raw
       │
       ▼
[sql-query]        FROM excel_raw …          →  output_variable_name = sales_agg
       │
       ▼
[python-script]    get_variable('sales_agg') →  result_df → output_variable_name = py_result
       │
       ▼
[database-sink]    input_variable_name = py_result（或依赖入边 Parquet）
```

| 步骤 | 节点            | 画布配置                          | 代码如何读写变量                                  |
| ---- | --------------- | --------------------------------- | ------------------------------------------------- |
| 1    | `excel-import`  | `output_variable_name: excel_raw` | 无代码；导入后自动登记                            |
| 2    | `sql-query`     | `output_variable_name: sales_agg` | SQL 中 **`FROM excel_raw`**                       |
| 3    | `python-script` | `output_variable_name: py_result` | **`get_variable('sales_agg')`** → **`result_df`** |
| 4    | `database-sink` | `input_variable_name: py_result`  | 无代码；从变量或入边读表                          |

---

## 6. 各节点类型：如何使用变量

### 6.1 `sql-query`（DuckDB 内存 SQL）

**消费变量**：把 **已登记在调试 Run 中的表变量名** 当作 SQL **表名** 使用。引擎会将 Parquet 注册为 DuckDB VIEW。

**产生变量**：查询结果写入 **`output_variable_name`**。

```sql
-- 上游节点 output_variable_name = excel_raw
-- 本节点 output_variable_name = sales_agg

SELECT
  产品类别,
  SUM(销售金额) AS 合计金额
FROM excel_raw
GROUP BY 产品类别
```

**多表 JOIN**

```sql
-- 变量名 orders、customers 均由上游节点产出
SELECT o.order_id, c.customer_name, o.amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= '2026-01-01'
```

**注意**

- 变量名含中文或特殊字符时，引擎会自动加双引号（也可手写 `"销售表"`）。
- SQL 末尾不要加分号（引擎会去掉，避免 COPY 语法错误）。
- **单节点测试前**，须先运行产出 `excel_raw` 等上游变量的节点，否则 DuckDB 找不到表。

---

### 6.2 `database-source`（外部库只读）

**产生变量**：`connectionId` + `code.sql` 查外部库，结果登记为 **`output_variable_name`**。  
**不消费** Run 内变量（直连 `ads_connections`）。

```sql
-- output_variable_name = dim_product
SELECT product_id, product_name, category
FROM dim_product
WHERE is_active = 1
LIMIT 50000
```

---

### 6.2b `dataspace-source`（数据空间只读）

**产生变量**：`spaceId` + `code.sql` 在空间存储引擎上查询，结果登记为 **`output_variable_name`**。  
**不消费** Run 内变量（直连 `ads_dataspaces` + `get_storage`）。

| 配置项                 | 说明                                              |
| ---------------------- | ------------------------------------------------- |
| `spaceId`              | `ads_dataspaces.id`（`dazi-flow dataspace list`） |
| `output_variable_name` | 产出表变量名                                      |

```sql
-- output_variable_name = space_sales
SELECT *
FROM sales_fact
WHERE dt >= '2025-01-01'
LIMIT 100000
```

---

### 6.3 `python-script`（最常用）

**运行时注入**

| 符号                             | 说明                                               |
| -------------------------------- | -------------------------------------------------- |
| `pd`                             | pandas                                             |
| `df`                             | 入边 Parquet（**整图跑**时常有值）                 |
| `get_variable("名")`             | 从当前调试 Run 按名读表/标量（**单节点测试首选**） |
| `result_df`                      | 主输出表 → 对应 **`output_variable_name`**         |
| `set_table_output(name, df)`     | 额外表变量                                         |
| `set_scalar_output(name, value)` | 标量变量                                           |
| `output.print(...)`              | 运行日志（勿用裸 `print`）                         |

**示例 A：单节点测试（推荐写法）**

上游 `sql-query` 的 `output_variable_name = sales_agg`；本节点 `output_variable_name = py_result`。

```python
# -*- coding: utf-8 -*-
# 输入：sales_agg（上游 SQL 节点产出）
# 输出：py_result（本节点 output_variable_name）
import pandas as pd

output.print("[python-script] 开始")

# 单节点调试时 df 常为空，务必用 get_variable
df = get_variable("sales_agg")
output.print(f"输入 sales_agg shape={df.shape}, columns={list(df.columns)}")

result_df = (
    df.groupby("产品类别", as_index=False)["合计金额"]
    .sum()
    .sort_values("合计金额", ascending=False)
)
output.print(f"输出 py_result shape={result_df.shape}")
output.print("[python-script] 完成")
```

**示例 B：整图跑 + 入边 + 附加变量**

```python
import pandas as pd

output.print("[python-script] 开始")

# 优先入边 df；若无数据再按变量名补
if df is None or df.empty:
    df = get_variable("sales_agg")
else:
    output.print(f"使用入边 df shape={df.shape}")

# 读取另一张已登记表（无需画布连线）
ref = get_variable("dim_product")
output.print(f"维表 dim_product shape={ref.shape}")

merged = df.merge(ref, on="product_id", how="left")
result_df = merged[merged["category"] == "A"]

# 可选：额外输出一张表
set_table_output("category_a_only", result_df)
output.print("[python-script] 完成")
```

**示例 C：标量变量**

```python
df = get_variable("sales_agg")
row_count = len(df)
set_scalar_output("row_count_flag", row_count)
result_df = df.head(100)
```

---

### 6.4 `excel-python`

**产生变量**：读 `excel_source_path`，用 **`set_table_output`** 登记；主输出名 **必须** 与 **`output_variable_name`** 一致。

```python
import pandas as pd

output.print("[excel-python] 开始")
output.print(f"file={excel_original_filename or excel_source_path}")

df = pd.read_excel(excel_source_path, sheet_name="Sheet1")
output.print(f"读取 shape={df.shape}")

# 与画布 output_variable_name 同名
set_table_output("excel_raw", df)
output.print("[excel-python] 完成")
```

---

### 6.5 `data-quality-check`

**消费变量**：主表可用入边 **`df`**；单节点测试时 **`df` 常为空**，须用 **`get_variable`**。附加表按画布 **`attached_variables`** / 上游 `output_variable_name` 逐个读取。

```python
import pandas as pd

output.print("[DQ] 开始")

if df is None or df.empty:
    df = get_variable("销售表")  # 与上游 output_variable_name 完全一致

orders = get_variable("订单明细")  # attached_variables 中的附加表

output.print(f"主表 shape={df.shape}, 订单 shape={orders.shape}")

# … 按 quality_config["rules"] 执行规则 …

result_df = pd.DataFrame([{"rule": "非空检查", "passed": True}])
set_scalar_output("quality_score", 98.5)
output.print("[DQ] 完成")
```

---

### 6.6 `database-sink`（无代码文件）

**消费变量**：画布配置 **`input_variable_name`**，从调试 Run 取表写入目标库；也可依赖入边 Parquet（未配变量名时）。

| 配置项                | 说明                                             |
| --------------------- | ------------------------------------------------ |
| `connectionId`        | 目标 `ads_connections`                           |
| `tableName`           | 目标表名                                         |
| `input_variable_name` | 可选；显式指定要写入的表变量名（如 `py_result`） |

---

### 6.6b `dataspace-sink`（无代码文件）

**消费变量**：与 `database-sink` 相同，通过 **`input_variable_name`** 或入边 Parquet 取表。

| 配置项                | 说明                            |
| --------------------- | ------------------------------- |
| `spaceId`             | 目标 `ads_dataspaces.id`        |
| `tableName`           | 空间内目标表（物理表名）        |
| `mode`                | `append`（默认）或 `replace`    |
| `syncMetadata`        | 写后是否同步元数据（默认 true） |
| `input_variable_name` | 要写入的表变量名                |

---

### 6.7 `condition`（条件分支）

条件脚本求布尔值，决定 **true/false** 分支。运行时主要注入入边 **`df`**（**不**注入 `get_variable`）。

```python
# code.py：表达式或单行，eval 后决定分支
df.shape[0] > 0 and df["amount"].sum() > 10000
```

单节点测试条件节点前，须保证 **入边上游已运行** 且连线有效；复杂判断可先用 `python-script` 写清逻辑再改为 condition。

---

## 7. `df` 与 `get_variable` 怎么选

| 场景                          | 推荐                                                               |
| ----------------------------- | ------------------------------------------------------------------ |
| **单节点测试**（`node-exec`） | **`get_variable('上游 output_variable_name')`**                    |
| **整流程 debug/preview**      | 入边 **`df`** 通常已有值；仍可用 `get_variable` 读 **未连线** 的表 |
| **多表输入**                  | 一张走 `df` 或主变量，其余 **`get_variable('名')`**                |
| **写 SQL**                    | 直接用 **变量名作表名**，不用 `get_variable`                       |

**常见错误**：单节点测试时只写 `result_df = df.groupby(...)`，但 `df` 为空 → 报错或空结果。  
**修复**：改为 `df = get_variable("上游变量名")`，或先运行上游再测。

---

## 8. 开发调试清单

1. 打开设计器，确认各节点 **`output_variable_name`** 已填且 **不重名**。
2. **自上游向下** 单节点测试，或一次 **`flow run flow-exec --type debug`**。
3. 用 **📊** 或 **`flow variable pull --name <名>`** 核对列名与样例行（交给 AI 时附上 **`变量/<名>.json`**）。
4. 写下游代码时 **变量名与画布完全一致**（区分大小写；中文名含全角字符）。
5. 改 `output_variable_name` → **`project push --canvas`**；改 `code.*` → **`node push`**。

---

## 9. 相关命令速查

```powershell
# 单节点测试（会更新 debug_run_id 对应变量）
dazi flow run node-exec --node <uuid> --dir .

# 整流程调试
dazi flow run flow-exec --dir . --type debug

# 变量
dazi flow variable pull --name sales_agg --dir .
dazi flow variable sync --dir .
```

---

## 10. 延伸阅读

- 搭子功能总览：`dazi/docs/279-dazi-dataflow数据流程功能总结.md` §3
- devend 变量重构：`devend/docs/20251201-009-变量系统重构.md`
- Excel→SQL→Python 端到端案例：[流程开发最佳实践（VS-flow0 案例）](./流程开发最佳实践-VS-flow0案例.md)
