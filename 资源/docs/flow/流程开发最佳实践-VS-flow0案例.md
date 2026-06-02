# 流程开发最佳实践（VS-flow0 案例）

**文档 ID**: `flow/流程开发最佳实践-VS-flow0案例`

> 最佳实践系列文档。以 **VS-flow0**（flowId `103`）为完整案例，总结从 Excel 解析 → 质检分支 → SQL 关联 → 数据库落库的端到端实践。  
> 本文侧重**模式与决策**；目录结构、pull/push、画布规范见 [数据流程项目开发指南](./flow-project-guide.md)。  
> 系列索引见 [Flow 文档索引 · 最佳实践系列](./flows-guide.md#最佳实践系列)。

---

## 一、VS-flow0 案例总结

### 1.1 业务目标

| 项          | 说明                                                                          |
| ----------- | ----------------------------------------------------------------------------- |
| 输入        | `Demo销售表_最简.xlsx`（销售表 / 产品表 / 规格表）                            |
| 处理        | 多 Sheet 解析 → 数据质量检查 → 条件分支 → DuckDB JOIN 宽表                    |
| 输出        | ClickHouse `space__xsh_01.temp_sales001`（销售表临时数据 001，96 行 × 12 列） |
| 平台 flowId | `103`（示例；你的项目以 `flow.meta.json` 为准）                               |

### 1.2 流程拓扑

```text
开始
  ↓
Excel 多表解析          → 产出：销售表、产品表、规格表
  ↓
数据质量检查            → 产出：V_DQ_REPORT、V_DQ_SCORE、quality_passed
  ↓
质检是否通过（condition）
  ├─ True  → SQL 表间关联  → 产出：销售明细宽表
  │            ↓
  │         写入销售临时表（database-sink）→ temp_sales001
  │            ↓
  └─ False → 结束（跳过 SQL 与入库）
            ↓
          结束
```

### 1.3 节点与变量一览

| 序号 | 节点           | 类型                 | 主要配置                                                 | 产出变量                                      |
| ---- | -------------- | -------------------- | -------------------------------------------------------- | --------------------------------------------- |
| 1    | Excel 多表解析 | `excel-python`       | `managed_file_id`、主输出 `销售表`                       | `销售表`、`产品表`、`规格表`                  |
| 2    | 数据质量检查   | `data-quality-check` | `attached_variables`、7 条 rules、`fail_on_error: false` | `V_DQ_REPORT`、`V_DQ_SCORE`、`quality_passed` |
| 3    | 质检是否通过   | `condition`          | 单行表达式 `eval`                                        | （无，仅分支）                                |
| 4    | SQL 表间关联   | `sql-query`          | `attached_variables` 三表                                | `销售明细宽表`                                |
| 5    | 写入销售临时表 | `database-sink`      | `connectionId`、`tableName`、`input_variable_name`       | （写入外部库）                                |

### 1.4 关键设计决策

**（1）一个 excel-python + 一个 sql-query，而非多个 excel-import**

- 三张 Sheet 表头行不一致（销售表 header=0，维表 header=1），用 **单节点 Python** 统一 `read_excel` 参数更可控。
- 多表 JOIN 放在 **DuckDB sql-query**，变量名即表名，SQL 可读性高、易调试。

**（2）质检与分支分离**

- `data-quality-check` 设置 **`fail_on_error: false`**：始终产出报告，不中断流程。
- 下游 **`condition`** 读入边 `df`（即 `V_DQ_REPORT`），按「通过」列决定 True/False。
- 好处：失败路径可观测（报告仍在 Run 中），成功路径才执行重计算与入库。

**（3）条件节点必须是单行表达式**

```python
bool(df is not None and not df.empty and df["通过"].all())
```

多行 Python + `output.print` 会在 `eval` 时报 `Condition Error: invalid syntax`。

**（4）database-sink 显式绑定变量**

- 配置 `input_variable_name: 销售明细宽表`，不依赖隐式入边推断。
- `connectionId` 使用 `ads_connections` 字符串 id（如 `clickhouse__space_xsh_01`），与 `资源/datasources/<连接名>/` 文档一致。

### 1.5 运行验证

整流程 `flow run flow-exec --type debug` 通过后，各节点耗时量级参考：Excel ~700ms、质检 ~600ms、SQL ~50ms、入库 ~620ms（以实际环境为准）。

---

## 二、推荐开发阶段（五步法）

### 阶段 0：规划（动手写代码前）

1. **画拓扑**：明确数据源、中间变量名、终态（表变量 / 标量 / 外部库表）。
2. **变量命名表**：全流程唯一、见名知意；中文名可用，但团队内保持一致。
3. **引用资源**：
   - Excel 表结构 → `资源/files/`（侧栏「文件上传管理」拉取）；
   - 目标库 → `资源/datasources/<连接名>/`（侧栏「数据连接」→ **拉取连接信息**）；
   - 数据空间表清单 → `资源/dataspaces/<空间名>/`（侧栏「数据空间」→ **拉取空间信息**）。
4. **节点选型**：见下文「节点选型速查」。

### 阶段 1：接入与解析

- Excel 多 Sheet、表头不统一 → **`excel-python`** + `set_table_output`。
- 单 Sheet 简单导入 → **`excel-import`** 即可。
- 解析后立即 **`flow variable pull`** 核对列名、行数、类型。

### 阶段 2：质量与分支

- 规则集中在 **`flow.json` → qualityConfig.rules**（行数、非空、外键）。
- 需要「失败仍跑完、再决定是否继续」→ **`fail_on_error: false` + condition**。
- 条件逻辑简单 → **`condition`**；复杂判定 → 先用 **`python-script`** 写清再提炼为单行。

### 阶段 3：转换与关联

- 内存多表 JOIN / 聚合 → **`sql-query`**（`FROM 上游变量名`）。
- 复杂行级逻辑 → **`python-script`**（`get_variable` + `result_df`）。
- SQL 节点配置 **`attached_variables`**，便于单测时注册未连线的维表。

### 阶段 4：落库与收尾

- 写外部库 → **`database-sink`**（`connectionId` + `tableName` + `input_variable_name`）。
- 更新 `资源/datasources/` 下表说明（侧栏连接下各表「下载表信息」）。
- 整流程 **debug run** 通过后，再考虑 preview / 生产调度。

---

## 三、节点选型速查

| 场景                  | 推荐节点             | 避免                              |
| --------------------- | -------------------- | --------------------------------- |
| 多 Sheet、不同 header | `excel-python`       | 多个 `excel-import` 重复配置      |
| 单 Sheet 直读         | `excel-import`       | 不必要的 Python                   |
| 行数/非空/外键        | `data-quality-check` | 在 Python 里散落 if/raise         |
| 通过/不通过两路       | `condition`          | 在 SQL 里写 impossible WHERE      |
| 多表 JOIN 宽表        | `sql-query`          | 全用 pandas merge（大表时难维护） |
| 写 ClickHouse / PG 等 | `database-sink`      | 在 Python 里手写 JDBC/HTTP        |
| 写数据空间表          | `dataspace-sink`     | 先落外部库再回灌空间              |
| 读外部库              | `database-source`    | 与 sql-query 混用职责             |
| 读数据空间            | `dataspace-source`   | 误填 `connectionId`               |

---

## 四、变量约定（必守）

### 4.1 命名

- 全流程 **`output_variable_name` 不重名**。
- 事实表 / 维表 / 宽表 / 报告表语义分离，例如：`销售表` → `销售明细宽表`、`V_DQ_REPORT`。
- 标量用简短名：`quality_passed`、`V_DQ_SCORE`。

### 4.2 读写方式

| 场景              | 做法                                                                            |
| ----------------- | ------------------------------------------------------------------------------- |
| SQL 消费上游表    | `FROM 销售表` / `JOIN 产品表`（变量名即表名）                                   |
| Python 单节点测试 | `get_variable("销售表")`（勿假设 `df` 一定有值）                                |
| Python 整图运行   | 入边 `df` 可用；多表时其余 `get_variable`                                       |
| excel-python 多表 | 每张表 **`set_table_output(变量名, df)`**，主表名与 `output_variable_name` 一致 |
| database-sink     | **`input_variable_name`** 指向要写入的表变量                                    |

### 4.3 调试顺序

```text
自上游向下单节点测试 → 或一次 flow-exec --type debug → variable pull/sync 核对
```

改 **`output_variable_name` / 画布** → `project push --canvas`  
改 **`code.py` / `code.sql`** → `node push` 或 `project push`

---

## 五、画布与 flow.json 规范

1. 节点 **`type: "custom"`**，业务类型在 **`data.type`**。
2. 连线必须写 **`sourceHandle` / `targetHandle`**（`l` `t` `r` `b`；条件用 `true` / `false`）。
3. 相邻节点间距：横向 ≥ 260px，纵向 ≥ 140px。
4. 代码只放在 **`节点/<名>/code.*`**，不要内嵌进 `flow.json`。
5. 新增节点流程：**改 flow.json → `push --canvas` → `pull` 同步 uuid → 再 push 代码**（纯配置节点无 code 则省略最后一步）。

详见 [flow-project-guide §6.2](./flow-project-guide.md#62-画布节点与连线规范ai-创建--编辑-flowjson-必读)。

---

## 六、VS-flow0 代码片段参考

### 6.1 Excel 多表解析（节选）

```python
SHEETS = {
    "销售表": {"sheet_name": "销售表", "header": 0, "usecols": "A:H"},
    "产品表": {"sheet_name": "产品表", "header": 1, "usecols": "A:C"},
    "规格表": {"sheet_name": "规格表", "header": 1, "usecols": "A:C"},
}
for var_name, kwargs in SHEETS.items():
    raw = pd.read_excel(excel_source_path, **kwargs)
    table = _normalize_sales(raw) if var_name == "销售表" else _normalize_dim(raw)
    set_table_output(var_name, table)
```

### 6.2 SQL 三表 JOIN（节选）

```sql
SELECT
    s.ID AS 销售ID,
    s.地区,
    s.产品 AS 产品ID,
    p.名称 AS 产品名称,
    ...
FROM 销售表 s
LEFT JOIN 产品表 p ON CAST(s.产品 AS VARCHAR) = CAST(p.ID AS VARCHAR)
LEFT JOIN 规格表 g ON CAST(s.规格 AS VARCHAR) = CAST(g.ID AS VARCHAR)
```

维表 ID 为字符串、事实表编码混用时，**JOIN 前 CAST** 避免 silent mismatch。

### 6.3 database-sink 配置

```json
{
  "type": "database-sink",
  "data": {
    "connectionId": "clickhouse__space_xsh_01",
    "tableName": "temp_sales001",
    "display_name": "销售表临时数据001",
    "input_variable_name": "销售明细宽表"
  }
}
```

### 6.4 dataspace-source / dataspace-sink 配置（新增）

```json
{
  "type": "dataspace-source",
  "data": {
    "spaceId": "space__0519",
    "output_variable_name": "空间销售明细"
  }
}
```

`节点/<dataspace-source名>/code.sql` 示例：

```sql
SELECT *
FROM sales_fact
WHERE dt >= '2025-01-01'
LIMIT 100000
```

```json
{
  "type": "dataspace-sink",
  "data": {
    "spaceId": "space__0519",
    "tableName": "temp_sales001",
    "mode": "append",
    "syncMetadata": true,
    "input_variable_name": "空间销售明细"
  }
}
```

要点：

- `dataspace-source` / `dataspace-sink` 一律使用 **`spaceId`**，不是 `connectionId`。
- `dataspace-source` 的 SQL 放在 `code.sql`，与 `database-source` 一致。
- `dataspace-sink` 支持 `mode=append|replace`，默认建议 `append`。
- `syncMetadata=true` 时，写入后会触发空间元数据同步（建议保留默认）。

---

## 七、常用命令清单

在 **工作区根目录**（如 `dazi-work`）执行，`<流程目录>` 替换为你的流程项目路径：

```powershell
cd "<流程目录>"

# 同步平台
.\scripts\dazi.ps1 flow project pull --flow <flowId> --dir .
.\scripts\dazi.ps1 flow project push --dir . --canvas

# 测试
.\scripts\dazi.ps1 flow run node-exec --node <node_uuid> --dir .
.\scripts\dazi.ps1 flow run flow-exec --dir . --type debug

# 变量
.\scripts\dazi.ps1 flow variable pull --name 销售明细宽表 --dir .
.\scripts\dazi.ps1 flow variable sync --dir .

# 数据源
.\scripts\dazi.ps1 flow source list

# 数据空间
.\scripts\dazi.ps1 flow dataspace list
.\scripts\dazi.ps1 flow dataspace tables <spaceId>
```

命令前缀与 Trae/VS Code 约定见 [CLI 调用约定](../guides/cli-invocation.md)。

---

## 八、常见问题与对策

| 现象                            | 原因                     | 对策                                  |
| ------------------------------- | ------------------------ | ------------------------------------- |
| SQL 单测找不到表                | 上游变量未写入 debug Run | 先跑 Excel 节点或整流程 debug         |
| excel-python 单测只有主表       | 多表需整图或先跑 Excel   | 用 `flow-exec` 或按序 node-exec       |
| Condition Error: invalid syntax | 条件脚本非单行表达式     | 改为单行 `bool(...)`                  |
| 质检失败流程中断                | `fail_on_error: true`    | 改为 `false` + 下游 condition         |
| 画布 push 失败                  | 未关联 flowId            | 先 `project pull --flow <id>`         |
| sink 写库失败                   | connectionId / 表名错误  | 对照 `资源/datasources/<连接名>/*.md` |
| dataspace-sink 写入失败         | spaceId / tableName 错误 | 先 `flow dataspace list` / `flow dataspace tables` |
| 变量列为空                      | 单测时只用了 `df`        | Python 改用 `get_variable`            |
| AI 不知道 connectionId          | 未拉取连接文档           | 侧栏数据连接 → **拉取连接信息**       |
| AI 不知道 spaceId               | 未拉取空间文档           | 侧栏数据空间 → **拉取空间信息**       |

---

## 九、新流程启动检查表

复制到新项目 `流程/<FlowName>/README.md` 或规划文档中使用：

- [ ] 已创建/拉取流程目录，`flow.meta.json` 含 `flowId`
- [ ] 拓扑图与变量命名表已评审
- [ ] 数据源文档已 @ 引用（Excel / connectionId / 空间表清单）
- [ ] 每个产出表节点配置了 `output_variable_name`
- [ ] SQL / Python 中变量名与画布完全一致
- [ ] 条件节点为单行表达式；出边使用 `true`/`false`
- [ ] 需要入库时配置了 `database-sink` 三要素
- [ ] 读写数据空间时使用 `dataspace-source` / `dataspace-sink` + `spaceId`
- [ ] 自上游单测或整流程 debug 通过
- [ ] `变量/*.json` 已核对 schema 与样例行
- [ ] 项目 README / 快速启动已更新拓扑与命令

---

## 十、相关文档

| 文档                                                          | 用途                          |
| ------------------------------------------------------------- | ----------------------------- |
| [Flow 文档索引 · 最佳实践系列](./flows-guide.md#最佳实践系列) | 系列目录                      |
| [数据流程项目开发指南](./flow-project-guide.md)               | 目录结构、pull/push、画布规范 |
| [流程变量系统指南](./variables-guide.md)                      | 变量模型与各节点读写          |
| [节点代码编写指南](./node-code-guide.md)                      | code.py / code.sql 模板       |
| [Flow 运行与测试](./run-guide.md)                             | Run、debug、错误文件          |
| [数据源管理](./source-guide.md)                               | connectionId、表结构          |
