# 节点代码编写指南

**文档 ID**: `flow/node-code-guide`  
**适用**: `项目/<业务名>/流程/flows/<流程名>/节点/<节点名>/code.*`  
**前置**: **[流程本地文件规范](./local-files-spec.md)**（必读）、[数据流程项目开发指南](./flow-project-guide.md)、[流程变量系统指南](./variables-guide.md)

> 设计器「打开代码」依赖 `flow.meta.json` 中该节点的 `dir`+`codeFile`。若打不开，先 `dazi flow project doctor` → `repair-meta`。

---

## 1. 哪些节点有代码文件

> 完整 **14 种** 可用 `data.type`（含无代码节点）见 [flows-guide §流程节点组件](./flows-guide.md#流程节点组件)。

| 业务类型 `data.type` | 本地文件                       | 平台存储               |
| -------------------- | ------------------------------ | ---------------------- |
| `sql-query`          | `code.sql`                     | `flow_nodes.code_body` |
| `database-source`    | `code.sql`                     | 同上                   |
| `dataspace-source`   | `code.sql`                     | 同上                   |
| `python-script`      | `code.py`                      | 同上                   |
| `excel-python`       | `code.py`                      | 同上                   |
| `condition`          | `code.py`                      | 同上                   |
| `data-quality-check` | `code.py`（键 `dqPythonCode`） | 同上                   |

纯配置节点（如 `database-sink`、`dataspace-sink`、`excel-import`、`delay`、`file-source` 等）**无** `code.*`，只在 `flow.json` 的 `data` 里配置；完整列表见 [flows-guide](./flows-guide.md#流程节点组件)。

**编辑入口**

- 资源管理器：右键 `节点/<名>/` → **打开节点代码**
- 设计器：选中节点 → **打开代码文件**
- 直接打开 `code.sql` / `code.py`

**提交入口**

- 右键 `code.*` → **提交节点** → `flow node push --node <node_uuid>`
- 或 **提交流程**（批量提交所有脏代码节点）

---

## 2. 修改代码的标准流程

```powershell
# 1. 确定流程目录（推荐绝对路径）
$flowDir = "D:\path\to\dazi-work\项目\<业务名>\流程\flows\MyFlow"

# 2. 编辑 节点/SQL查询/code.sql 等

# 3. 查看是否有本地改动
dazi flow project status --dir $flowDir

# 4. 提交代码到平台（必须先于测试；node-exec 跑的是平台已 push 的代码）
dazi flow node push --node <node_uuid> --dir $flowDir

# 5. 单节点测试
dazi flow run node-exec --node <node_uuid> --dir $flowDir

# 6. 若有 output_variable_name：核对输出变量（不能仅凭 node-exec 退出码）
dazi flow variable pull --name <output_variable_name> --dir $flowDir
```

`node_uuid` 在 `flow.meta.json` → `nodes.<uuid>`，或设计器属性面板、 `node.info.json` 中查看。  
**单节点运行 API 使用语义 `nodeId`（画布 `id` 字段）**，CLI 的 `node-exec` 会用 meta 自动翻译。

> **勿先测后 push**：未 `node push` 时 `node-exec` 仍执行平台旧代码，会造成「本地已改但通过/仍报错」的假象。

**成功判据**：`node push` 成功 → `node-exec` 的 JSON `success: true` →（有输出变量时）`variable pull` 后 `变量/<名>.json` 为 ready 且数据合理。

测试失败时阅读 **`_run/<节点名>.last-error.md`**（含错误分类与修复指引），确认后再交给 AI。

---

## 3. `sql-query` / `database-source` / `dataspace-source`（SQL）

**文件**: `code.sql`  
**画布配置**（`flow.json` → 节点 `data`）：

| 类型               | 关键字段                                 |
| ------------------ | ---------------------------------------- |
| `database-source`  | `connectionId`、`output_variable_name`   |
| `dataspace-source` | `spaceId`、`output_variable_name`        |
| `sql-query`        | `output_variable_name`（消费上游表变量） |

> **变量用法**：`sql-query` 在 SQL 里把 **上游 `output_variable_name`** 当作 **表名**；`database-source` / `dataspace-source` 只 **产出** 变量、不消费 Run 内变量。详见 [流程变量系统指南 §6.1–6.2](./variables-guide.md#61-sql-queryduckdb-内存-sql)。

**约定**

- SQL 写在 **`code.sql`**，不要塞进 `flow.json` 的 `data.sql`（pull 后会剥离到文件）。
- `connectionId` 为 **`ads_connections` 的字符串 id**，用 `dazi-flow source list` 核对。
- `spaceId` 为 **`ads_dataspaces` 的 id**，用 `dazi-flow dataspace list` 核对。
- 执行结果以 **`output_variable_name`** 为名写入调试 Run（表变量）。

**模板（database-source：外部库 → 表变量）**

```sql
-- output_variable_name = dim_product
SELECT product_id, product_name, category
FROM dim_product
WHERE is_active = 1
LIMIT 50000;
```

**模板（dataspace-source：数据空间 DuckDB/ClickHouse → 表变量）**

```sql
-- spaceId 在 flow.json；SQL 针对空间内已注册表
-- output_variable_name = sales_raw
SELECT *
FROM sales_fact
WHERE dt >= '2025-01-01'
LIMIT 100000;
```

**模板（sql-query：消费上游表变量 → 新表变量）**

```sql
-- 上游 output_variable_name = excel_raw
-- 本节点 output_variable_name = sales_agg
SELECT
  产品类别,
  SUM(销售金额) AS 合计金额
FROM excel_raw
GROUP BY 产品类别;
```

**多表 JOIN（变量名即表名）**

```sql
-- 上游已产出 orders、customers
SELECT o.order_id, c.customer_name, o.amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;
```

**测试**: 右键 → 测试运行节点；成功后用设计器 📊 或 `flow variable pull --name <output_variable_name>` 查看结果。

---

## 4. `python-script`（表 → 表）

**文件**: `code.py`  
**画布**: 配置 **`output_variable_name`**（主输出表变量名）。

> **变量用法**：单节点测试用 **`get_variable('上游 output_variable_name')`**；整图跑时入边 **`df`** 可能有值。完整说明与多表示例见 [流程变量系统指南 §6.3](./variables-guide.md#63-python-script最常用)。

**运行时注入**

| 符号                         | 说明                                               |
| ---------------------------- | -------------------------------------------------- |
| `pd`                         | pandas                                             |
| `df`                         | 来自入边 Parquet（整图跑时通常非空）               |
| `get_variable("名")`         | 从调试 Run 读上游表（**单节点测试时优先用这个**）  |
| `set_table_output(name, df)` | 多表输出                                           |
| `result_df`                  | 主输出 DataFrame（与 `output_variable_name` 对应） |
| `output.print(...)`          | 运行日志（**勿用裸 `print`**）                     |

**单节点测试要点**

整图运行时 `df` 可能有值；**单节点调试**时常无入边 Parquet，`df` 为空，应：

```python
# -*- coding: utf-8 -*-
# 上游 sql-query 的 output_variable_name = sales_agg
# 本节点 output_variable_name = py_result
import pandas as pd

output.print("[python-script] 开始")

df = get_variable("sales_agg")  # 变量名须与上游画布配置完全一致
output.print(f"输入 shape={df.shape}, columns={list(df.columns)}")

result_df = df.groupby("产品类别", as_index=False)["合计金额"].sum()
output.print(f"输出 shape={result_df.shape}")
```

**多表 + 入边回退**

```python
import pandas as pd

if df is None or df.empty:
    df = get_variable("sales_agg")
ref = get_variable("dim_product")
result_df = df.merge(ref, on="product_id", how="left")
set_table_output("merged_preview", result_df.head(100))  # 可选附加表
```

**日志规范**（与平台约定一致）

- 开始 / 输入信息 / 关键变换 / 输出结果 / 结束 均用 `output.print`
- `except` 里先 `output.print` 再 `raise`

---

## 5. `excel-python`（Excel 开发 · **默认首选**）

> **选型**：文件上传管理中的 **`.xlsx` / `.xls`**（有 `managed_file_id`）**优先本节点**，**禁止**用 `file-source`（不解析 Excel）。仅极简单单 Sheet 零代码时才考虑 `excel-import`。

**文件**: `code.py`  
**画布**（`flow.json` → 节点 `data`，**不是写在 code.py 里**）:

| 字段                       | 说明                                                                                        |
| -------------------------- | ------------------------------------------------------------------------------------------- |
| **`managed_file_id`**      | 平台「文件上传管理」登记的 **UUID**（见 `资源/files/<名>_<id8>/文件信息.json` → `file_id`） |
| **`output_variable_name`** | 主输出表变量名；**必须与** `set_table_output` 第一个参数 **完全一致**                       |

### 分工（AI 必守）

| 谁配置                   | 配什么                              | 禁止                                                           |
| ------------------------ | ----------------------------------- | -------------------------------------------------------------- |
| **`flow.json` / 设计器** | `managed_file_id` = UUID            | 不要用文件名、相对路径、data upload 的 `id`                    |
| **`code.py`**            | 用 **`excel_source_path`** 读 Excel | 不要 `open("xxx.xlsx")`、`pd.read_excel("D:/...")`、不要猜路径 |

引擎根据 `managed_file_id` 查库得到物理路径，执行前注入：

| 变量                          | 说明                                                        |
| ----------------------------- | ----------------------------------------------------------- |
| **`excel_source_path`**       | 服务端 Excel **绝对路径**（代码里唯一正确的读文件方式）     |
| **`excel_original_filename`** | 登记显示名（仅用于 `output.print` 日志）                    |
| `pd`                          | pandas                                                      |
| `set_table_output(name, df)`  | 产出表变量（**必须**调用，主表名 = `output_variable_name`） |
| `output.print(...)`           | 运行日志                                                    |

**获取 `managed_file_id`**

1. 侧栏 **数据资源 → 文件上传管理** → 拉取到 `资源/files/.../文件信息.json`
2. 或 CLI：`dazi flow managed-files list` / `managed-files pull --file-id <uuid>`

**`flow.json` 示例（画布配置）**

```json
{
  "id": "n-excel-1",
  "type": "custom",
  "data": {
    "label": "Excel解析",
    "type": "excel-python",
    "managed_file_id": "51853ede-9e6b-4a3a-aa7a-060cbead0862",
    "output_variable_name": "成本统计报表"
  }
}
```

> `managed_file_id` 是 **UUID 字符串**，与 `Excel成本报表08.xlsx` 等文件名 **无关**；文件名只出现在注释/`excel_original_filename` 日志中。

---

### 示例 A：单 Sheet、复杂表头（推荐模板）

对应真实流程「成本报表数据08」：表头不在第 1 行时用 `header=None` + `skiprows` + `names`。

```python
# -*- coding: utf-8 -*-
# 画布：managed_file_id = <UUID>（见 flow.json，勿在代码里写文件名）
# 画布：output_variable_name = 成本统计报表
import pandas as pd

OUTPUT_VAR = "成本统计报表"  # 必须与 output_variable_name 一致
DATA_START_ROW = 4           # 0-based，Excel 第 5 行起为数据

COLUMN_NAMES = [
    "基本信息_组织", "基本信息_年度", "基本信息_月度", "基本信息_项目",
    "成本项_管理费", "成本项_间接成本", "成本项_税金",
    # ... 按实际列继续
]

output.print("[excel-python] 开始")
output.print(f"source={excel_original_filename or excel_source_path}")

# ✅ 正确：读引擎注入的路径
raw = pd.read_excel(
    excel_source_path,
    sheet_name="Sheet1",
    header=None,
    skiprows=DATA_START_ROW,
    usecols="A:P",
    names=COLUMN_NAMES,
)
table = raw.dropna(how="all")

output.print(f"{OUTPUT_VAR} shape={table.shape}")
set_table_output(OUTPUT_VAR, table)  # 主输出，名称必须与 output_variable_name 一致
output.print("[excel-python] 完成")
```

---

### 示例 B：多 Sheet 产出多张表变量

对应 VS-flow0：一个 Excel 解析出 `销售表`、`产品表`、`规格表`。

```python
# -*- coding: utf-8 -*-
# 画布：managed_file_id = <UUID>
# 画布：output_variable_name = 销售表（主输出，须 set_table_output 同名）
import pandas as pd

SHEETS = {
    "销售表": {"sheet_name": "销售表", "header": 0, "usecols": "A:H"},
    "产品表": {"sheet_name": "产品表", "header": 1, "usecols": "A:C"},
    "规格表": {"sheet_name": "规格表", "header": 1, "usecols": "A:C"},
}

output.print("[excel-python] 开始")
output.print(f"source={excel_original_filename or excel_source_path}")

for var_name, kwargs in SHEETS.items():
    raw = pd.read_excel(excel_source_path, **kwargs)  # ✅ 只用 excel_source_path
    table = raw.dropna(how="all")
    output.print(f"{var_name} shape={table.shape}")
    set_table_output(var_name, table)

output.print("[excel-python] 完成")
```

下游 `sql-query` 可直接 `FROM 销售表 JOIN 产品表 ...`。

---

### 反例（AI 禁止）

```python
# ❌ 错误：臆造本地/相对路径
pd.read_excel("Excel成本报表08.xlsx")
pd.read_excel("./uploads/xxx.xlsx")
pd.read_excel(r"D:\src2025\...\成本报表.xlsx")

# ❌ 错误：在 code.py 里写 managed_file_id 或 open 文件
open(managed_file_id)

# ❌ 错误：主输出未 set_table_output，或名称与 output_variable_name 不一致
result_df = pd.read_excel(excel_source_path)
# 缺少 set_table_output("与画布同名", result_df)
```

---

### 提交与测试

1. 改 **`managed_file_id` / `output_variable_name`** → `project push --canvas`
2. 改 **`code.py`** → `node push` → `node-exec` 或整流程 `flow-exec`
3. 多表时单节点测试可能只有主表；全表变量用 **`flow-exec --type debug`** 后 `variable sync`

详见 [flow-project-guide §6.1 文件上传管理](./flow-project-guide.md#61-文件上传管理excel-等流程数据源)、[流程开发最佳实践 §6.1](./流程开发最佳实践-VS-flow0案例.md#61-excel-多表解析节选)。

---

## 6. `condition`（条件分支）

**文件**: `code.py`  
逻辑脚本决定分支；使用 `output.print` 记录判断依据。测试方式同 `python-script`。

---

## 7. `data-quality-check`（数据质量）

**文件**: `code.py`（平台键 `dqPythonCode`）

**注入**

| 符号                             | 说明                           |
| -------------------------------- | ------------------------------ |
| `df`                             | 入边 Parquet；单节点时可能为空 |
| `get_variable("名")`             | 调试 Run 中的附加表            |
| `quality_config`                 | 与画布 `qualityConfig` 对齐    |
| `set_scalar_output(name, value)` | 综合分等标量                   |
| `result_df`                      | 质检报告表                     |

**推荐**：`df.empty` 时用 `get_variable` 补主表（变量名与 `attached_variables` / 上游输出一致）。

规则从 `quality_config["rules"]` 读取，避免魔法数。端到端质检案例见 [流程开发最佳实践（VS-flow0 案例）](./流程开发最佳实践-VS-flow0案例.md)。

---

## 8. 画布配置 vs 代码分工

| 改什么                                   | 改哪里                   | 怎么提交                |
| ---------------------------------------- | ------------------------ | ----------------------- |
| SQL / Python 正文                        | `code.sql` / `code.py`   | `node push`             |
| 连线、坐标、节点增删                     | `flow.json`（设计器）    | `project push --canvas` |
| connectionId、表名、output_variable_name | 设计器属性 → `flow.json` | `project push --canvas` |

**不要**在 `flow.json` 里硬塞大段 `pythonCode`/`sql`：pull 会剥离到 `code.*`，push 代码走 `flow-nodes` 接口。

---

## 9. 查看输出变量

变量模型、`debug_run_id`、本地 **`变量/<名>.json`** 详见 **[流程变量系统指南](./variables-guide.md)**。

```powershell
# 拉取单个变量（schema + 前 10 行）到 变量/<name>.json
dazi flow variable pull --name sales_df --dir .

# 同步全部调试变量
dazi flow variable sync --dir .
```

设计器：选中节点 → 属性 **`output_variable_name`** → 点击 **📊**。

---

## 10. AI 协作建议

1. 让 AI 阅读 **`code.*`** + **`flow.json` 中该节点 `data`** + 失败时的 **`_run/*.last-error.md`**
2. **Agent 模式**（用户委托改流程）：AI 应主动执行「改 `code.*` → **`node push`** → **`node-exec`** →（有输出变量时）**`variable pull`** → 读 `last-error.md` → 再改」循环（默认最多 3 轮），详见 **`快速启动_<流程名>.md` §AI 自主运行与改错闭环** 或 **`flow/run-fix-loop`**
3. **对话模式**（用户仅粘贴错误）：用户确认后再改代码 → **`node push`** → 测试 → `variable pull`（若适用）
4. 需要查上游表结构时，先 **运行上游** 或 **`variable pull`**，把 `变量/<名>.json` 交给 AI
5. MCP：`dazi-flow mcp serve`（工具含 `flow_run_node`、`flow_node_get_code`、`flow_node_set_code` 等，写操作需 `--allow-write`）
