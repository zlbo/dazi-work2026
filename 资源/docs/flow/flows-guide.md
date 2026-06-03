# Flow 文档索引

**文档 ID**: `flow/flows-guide`

> v3.1 起，日常流程开发请优先阅读 **[数据流程项目开发指南](./flow-project-guide.md)**。  
> 本文保留平台级 Flow 操作速查，并链到各专题文档。

---

## 推荐阅读顺序

1. [数据流程项目开发指南](./flow-project-guide.md) — 目录结构、`dazi.ps1 flow`、菜单、pull/push 循环
2. **[画布节点与连线规范](./flow-project-guide.md#62-画布节点与连线规范ai-创建--编辑-flowjson-必读)** — **AI 创建流程必读**：节点尺寸 200px、锚点 `l/t/r/b/true/false`、条件分支
3. [流程开发最佳实践（VS-flow0 案例）](./流程开发最佳实践-VS-flow0案例.md) — **端到端案例**：Excel → 质检 → SQL → 落库、五阶段开发法、检查表
4. [流程变量系统指南](./variables-guide.md) — 变量模型、`output_variable_name`、代码节点如何用变量
5. [节点代码编写指南](./node-code-guide.md) — `python-script`、`sql-query` 等单节点代码
6. [Flow 运行与测试](./run-guide.md) — 单节点/整流程运行、变量
7. [CLI 调用约定](../guides/cli-invocation.md) — `dazi` 在 Trae/VS Code 中的用法

---

## 终端命令前缀

在 **`dazi-work` 根目录**（Trae、VS Code、Cursor 交付环境）：

```powershell
dazi flow <子命令...>
```

等价于开发时的 `dazi-flow <子命令...>`。示例：

```powershell
dazi flow flows list
dazi flow project pull --flow 98 --dir "项目\flow_xxx\流程\MyFlow"
```

---

## 流程项目（`项目/flow_*`）常用命令

| 任务               | 命令                                                |
| ------------------ | --------------------------------------------------- |
| 拉取平台流程到本地 | `flow project pull --flow <id> --dir <流程目录>`    |
| 提交代码 + 画布    | `flow project push --dir <流程目录> --canvas`       |
| 查看本地改动       | `flow project status --dir <流程目录>`              |
| 提交单个节点代码   | `flow node push --node <uuid> --dir <流程目录>`     |
| 单节点测试         | `flow run node-exec --node <uuid> --dir <流程目录>` |
| 整流程运行         | `flow run flow-exec --dir <流程目录> --type debug`  |
| 拉取变量           | `flow variable pull --name <名> --dir <流程目录>`   |

扩展侧栏/资源管理器右键与上表 **同源**，见 [flow-project-guide](./flow-project-guide.md#6-资源管理器菜单主交互)。

---

## 平台级 Flow 操作

| 任务 | 命令                              |
| ---- | --------------------------------- |
| 列表 | `flow flows list`                 |
| 详情 | `flow flows get <flow-id>`        |
| 新建 | `flow flows create --name "名称"` |
| 校验 | `flow flows validate <flow-id>`   |

---

## AI 创建流程速查

| 主题                                            | 文档章节                                                                            |
| ----------------------------------------------- | ----------------------------------------------------------------------------------- |
| **可用节点类型一览（AI 必读）**                 | [§流程节点组件](#流程节点组件)                                                      |
| **节点尺寸与布局**（200px 宽、260×140 间距）    | [flow-project-guide §6.2.1](./flow-project-guide.md#621-节点尺寸与布局)             |
| **连线锚点**（`sourceHandle` / `targetHandle`） | [flow-project-guide §6.2.2](./flow-project-guide.md#622-锚点连线端点约定)           |
| **条件节点 True/False 分支**                    | [flow-project-guide §6.2.4](./flow-project-guide.md#624-条件节点condition)          |
| **`flow.json` 边与完整示例**                    | [flow-project-guide §6.2.5–6.2.6](./flow-project-guide.md#625-flowjson-边edges字段) |
| **提交前自检清单**                              | [flow-project-guide §6.2.7](./flow-project-guide.md#627-ai-自检清单)                |
| **端到端案例与启动检查表**                      | [流程开发最佳实践-VS-flow0案例](./流程开发最佳实践-VS-flow0案例.md)                 |
| 变量串联与 `output_variable_name`               | [variables-guide](./variables-guide.md)                                             |
| 节点 `code.py` / `code.sql`                     | [node-code-guide](./node-code-guide.md)                                             |

---

## 流程节点组件

> **AI 设计/改流程时只能使用下表中的 `data.type`**，与 Web 设计器「组件」Tab、CLI `flow node new --type` 一致。  
> 画布 JSON 中节点 **`type` 恒为 `"custom"`**，业务类型写在 **`data.type`**。

新建节点（在流程目录）：

```powershell
dazi flow node new --type <data.type> --dir . --label "<显示名>"
```

### 总览

| 分组     | `data.type`                | 名称           | 代码文件   | 典型用途                        |
| -------- | -------------------------- | -------------- | ---------- | ------------------------------- |
| 流程控制 | `condition`                | 条件判断       | `code.py`  | 布尔分支，出边 `true`/`false`   |
| 流程控制 | `delay`                    | 延时等待       | —          | 暂停 N 秒                       |
| 数据处理 | `file-source`              | 文件输入       | —          | 托管/上传文件 → 表变量          |
| 数据处理 | `excel-import`             | Excel 导入     | —          | 单 Sheet 简单导入               |
| 数据处理 | `excel-python`             | Excel 开发     | `code.py`  | 多 Sheet、复杂表头              |
| 数据处理 | `sql-query`                | SQL 查询       | `code.sql` | DuckDB 内存 SQL，上游变量作表名 |
| 数据处理 | `python-script`            | Python 脚本    | `code.py`  | pandas 转换（最常用）           |
| 数据处理 | `database-source`          | 数据库读取     | `code.sql` | 外部库只读（`connectionId`）    |
| 数据处理 | `database-sink`            | 数据库写入     | —          | 表变量 → 外部库表               |
| 数据处理 | `dataspace-source`         | 数据空间读取   | `code.sql` | 空间只读（`spaceId`）           |
| 数据处理 | `dataspace-sink`           | 数据空间写入   | —          | 表变量 → 空间表                 |
| 数据处理 | `data-quality-check`       | 数据质量检查   | `code.py`  | 规则或自定义质检脚本            |
| 数据处理 | `folder-resource-import`   | 文件夹资源导入 | —          | 文件夹批量导入                  |
| 数据处理 | `folder-resource-register` | 资源注册       | —          | 注册到连接/目录                 |

### 流程控制

#### `condition` — 条件判断

| 项   | 说明                                                                       |
| ---- | -------------------------------------------------------------------------- |
| 代码 | `节点/<名>/code.py`（布尔表达式，运行时 eval）                             |
| 入边 | 至少一条；上游表注入为 **`df`**                                            |
| 出边 | **`sourceHandle: "true"`** / **`"false"`**（禁止用 `r`/`b`）               |
| 变量 | 不产生新表，仅路由                                                         |
| 详见 | [flow-project-guide §6.2.4](./flow-project-guide.md#624-条件节点condition) |

#### `delay` — 延时等待

| 项   | 说明                                 |
| ---- | ------------------------------------ |
| 配置 | `data.delaySeconds` 或 `delay`（秒） |
| 变量 | 无                                   |

### 数据输入 / 读取

#### Excel 文件选型（AI 必读）

数据源来自 **文件上传管理**（有 `file_id` / `managed_file_id`）且文件为 **`.xlsx` / `.xls`** 时：

|    优先级     | 节点               | 说明                                                                                          |
| :-----------: | ------------------ | --------------------------------------------------------------------------------------------- |
| **1（默认）** | **`excel-python`** | **优先使用**。可控制 Sheet、表头行、列范围、多表 `set_table_output`；画布配 `managed_file_id` |
|       2       | `excel-import`     | 仅当 **单 Sheet、第 1 行即标准表头、无需任何解析逻辑** 时                                     |
|   **禁止**    | `file-source`      | **不要**用 file-source 读 Excel——它只做原始文件透传，**不会**解析为表变量                     |

```text
有 managed_file_id + Excel  →  excel-python（默认）
极简单单 Sheet、零代码       →  excel-import（例外）
CSV / Parquet / 非 Excel     →  file-source 或其他专用节点
```

> 不确定表头/Sheet 结构时，**一律选 `excel-python`**，在 `code.py` 里用 `excel_source_path` 解析。

#### `file-source` — 文件输入

| 项         | 说明                                                     |
| ---------- | -------------------------------------------------------- |
| 何时用     | **非 Excel** 的原始文件透传（CSV、Parquet 等已登记文件） |
| **勿用于** | **`.xlsx` / `.xls`** → 改用 **`excel-python`**（见上表） |
| 配置       | `file_id` / `managed_file_id`、`output_variable_name`    |
| 产出       | 原始文件路径对应的表变量（**不解析 Excel**）             |

#### `excel-import` — Excel 导入（简单）

| 项       | 说明                                                                         |
| -------- | ---------------------------------------------------------------------------- |
| 何时用   | **单 Sheet、第 1 行标准表头、零自定义逻辑** 的极少数场景                     |
| 默认建议 | 有 `managed_file_id` 的 Excel **优先 `excel-python`**，便于后续改 Sheet/表头 |
| 配置     | `file_id` / `source_excel_id`、`sheetName`（可选）、`output_variable_name`   |
| 产出     | 表变量（如 `excel_raw`）                                                     |

#### `excel-python` — Excel 开发（Excel 默认首选）

| 项       | 说明                                                                                                 |
| -------- | ---------------------------------------------------------------------------------------------------- |
| 何时用   | **凡 `.xlsx`/`.xls` 且已有 `managed_file_id` 时优先本节点**；多 Sheet、非标准表头、需清洗/拆表       |
| 画布配置 | **`managed_file_id`**（UUID，来自文件上传管理 / `文件信息.json` 的 `file_id`）                       |
| 代码     | `code.py` 内 **只读 `excel_source_path`**（引擎注入），**禁止**写文件名或本地路径                    |
| 产出     | **`set_table_output(变量名, df)`**；主表名 **= `output_variable_name`**                              |
| 详见     | [node-code-guide §5 excel-python](./node-code-guide.md#5-excel-pythonexcel-开发)（含完整示例与反例） |

#### `database-source` — 数据库读取

| 项   | 说明                                                                                                         |
| ---- | ------------------------------------------------------------------------------------------------------------ |
| 代码 | `code.sql`（SELECT，直连外部库）                                                                             |
| 配置 | **`connectionId`**（`ads_connections.id`）、`output_variable_name`                                           |
| 消费 | **不**消费 Run 内变量                                                                                        |
| 详见 | [source-guide](./source-guide.md)、[variables-guide §6.2](./variables-guide.md#62-database-source外部库只读) |

#### `dataspace-source` — 数据空间读取

| 项   | 说明                                                                           |
| ---- | ------------------------------------------------------------------------------ |
| 代码 | `code.sql`                                                                     |
| 配置 | **`spaceId`**、`output_variable_name`、`limit`（可选）                         |
| 消费 | **不**消费 Run 内变量                                                          |
| 详见 | [variables-guide §6.2b](./variables-guide.md#62b-dataspace-source数据空间只读) |

### 数据加工

#### `sql-query` — SQL 查询

| 项   | 说明                                                                     |
| ---- | ------------------------------------------------------------------------ |
| 代码 | `code.sql`                                                               |
| 消费 | 上游 **`output_variable_name` 作 SQL 表名**（`FROM 上游变量名`）         |
| 产出 | `output_variable_name`                                                   |
| 注意 | 单节点测试前须先跑上游；SQL 末尾勿加分号                                 |
| 详见 | [variables-guide §6.1](./variables-guide.md#61-sql-queryduckdb-内存-sql) |

#### `python-script` — Python 脚本

| 项   | 说明                                                                                                         |
| ---- | ------------------------------------------------------------------------------------------------------------ |
| 代码 | `code.py`                                                                                                    |
| 消费 | **`get_variable("上游变量名")`**（单节点测试首选）或入边 `df`                                                |
| 产出 | **`result_df`** → `output_variable_name`                                                                     |
| 详见 | [variables-guide §6.3](./variables-guide.md#63-python-script最常用)、[node-code-guide](./node-code-guide.md) |

#### `data-quality-check` — 数据质量检查

| 项   | 说明                                                 |
| ---- | ---------------------------------------------------- |
| 代码 | `code.py`（平台键 `dqPythonCode`；非空时优先于规则） |
| 配置 | `qualityConfig`、`output_variable_name`              |
| 消费 | 上游表 / `get_variable`                              |
| 典型 | 与 **`condition`** 组合做合格/不合格分支             |

### 数据输出 / 写入

#### `database-sink` — 数据库写入

| 项   | 说明                                                                    |
| ---- | ----------------------------------------------------------------------- |
| 代码 | 无                                                                      |
| 配置 | **`connectionId`**、**`tableName`**、**`input_variable_name`**、`mode`  |
| 消费 | 指定变量或入边 Parquet                                                  |
| 详见 | [variables-guide §6.6](./variables-guide.md#66-database-sink无代码文件) |

#### `dataspace-sink` — 数据空间写入

| 项   | 说明                                                                      |
| ---- | ------------------------------------------------------------------------- |
| 代码 | 无                                                                        |
| 配置 | **`spaceId`**、**`tableName`**、**`input_variable_name`**、`syncMetadata` |
| 消费 | 同 database-sink                                                          |

### 资源与文件夹

#### `folder-resource-import` — 文件夹资源导入

| 项   | 说明                                                         |
| ---- | ------------------------------------------------------------ |
| 配置 | `folderId`、`resourceId`、`pageSize`、`output_variable_name` |
| 产出 | 表变量                                                       |

#### `folder-resource-register` — 资源注册

| 项   | 说明                                  |
| ---- | ------------------------------------- |
| 配置 | `connectionName`、`targetFolderId` 等 |
| 用途 | 将导入结果注册到连接/资源目录         |

### 选型速查（AI 常用）

```text
Excel（有 managed_file_id）→ excel-python（默认，勿用 file-source）
Excel 极简单单 Sheet 零代码 → excel-import（例外）
非 Excel 原始文件           → file-source
读外部数据库               → database-source + connectionId + code.sql
读数据空间         → dataspace-source + spaceId + code.sql
内存 SQL 关联      → sql-query（上游变量名作表名）
pandas 清洗/聚合   → python-script
合格/不合格分支    → data-quality-check → condition
写外部库           → database-sink
写数据空间         → dataspace-sink
```

典型链路示例见 [variables-guide §5](./variables-guide.md#5-管线示例变量如何串联) 与 [流程开发最佳实践-VS-flow0案例](./流程开发最佳实践-VS-flow0案例.md)。

---

## 最佳实践系列

按 **`NN-主题-案例标识.md`** 编号发布，每篇对应一个可复用的端到端模式。新增篇章请递增编号并在此登记。

| 编号 | 文档                                                                    | 说明                                                  |
| ---- | ----------------------------------------------------------------------- | ----------------------------------------------------- |
| 01   | [流程开发最佳实践（VS-flow0 案例）](./流程开发最佳实践-VS-flow0案例.md) | Excel 多表 → 质检分支 → SQL 宽表 → database-sink 落库 |

---

## 其他专题

| 文档                                       | 说明                                        |
| ------------------------------------------ | ------------------------------------------- |
| [流程变量系统指南](./variables-guide.md)   | 变量产生/消费、`get_variable`、SQL 表名约定 |
| [Flow 运行与测试](./run-guide.md)          | Run、debug、变量、流程项目测试              |
| [Flow 快照管理](./snapshot-guide.md)       | 平台级 `flows/<id>/snapshot.json` 分离快照  |
| [数据源管理](./source-guide.md)            | connectionId、表结构                        |
| [Flow 执行计划](./plan-guide.md)           | FlowPlan / markdown 规划                    |
| [CLI 命令速查](../guides/cli-reference.md) | 完整命令表                                  |

---
