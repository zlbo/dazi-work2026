# 本体命名规范 · 物理表、Cube 与对象

**文档 ID**: `onto/naming-conventions`

> **类型**：规范（物理层 · Cube 层 · 本体层 · 三层对照）  
> **适用版本**：`dazi-vscode` v3.0.9+  
> **前置阅读**：[本体规划指南](./本体规划指南.md)

---

## 目录

1. [总则：三层各有一套命名语言](#1-总则三层各有一套命名语言)
2. [物理表：类别与前缀](#2-物理表类别与前缀)
3. [时间维 dim_date（强制）](#3-时间维-dim_date强制)
4. [Cube：类别与命名](#4-cube类别与命名)
5. [本体对象：Palantir 思想与分类](#5-本体对象palantir-思想与分类)
6. [链接类型命名](#6-链接类型命名)
7. [三层对照与迁移示例（销售域）](#7-三层对照与迁移示例销售域)
8. [规划文档写法与自检清单](#8-规划文档写法与自检清单)
9. [相关文档索引](#9-相关文档索引)

---

## 1. 总则：三层各有一套命名语言

本体规划须同时设计 **物理表、Cube、本体对象** 三层；三者 **刻意区分命名**，避免「一张表一个对象一个 Cube 同名」的一一复制。

| 层级 | 面向谁 | 命名风格 | 核心原则 |
| ---- | ------ | -------- | -------- |
| **物理表** | DBA / ETL / ClickHouse | **`{前缀}_{实体}`** snake_case | 从表名即可判断存储角色（事实/维/桥/配置…） |
| **Cube** | 分析 / 报表 / 语义层 | **`{主题}{Analytics\|Cube}`** PascalCase | 表达**分析主题与粒度**，可共享同一 fact 表 |
| **本体对象** | 业务 / 产品 / 智能体 | **`{业务名词}`** PascalCase，**无前缀** | 贴近 **业务世界**（Palantir Object Type 思想），用**分类**而非前缀区分角色 |

```text
  业务世界（本体）          分析语义（Cube）           存储落地（物理表）
  ─────────────────        ─────────────────         ─────────────────
  Product          ←──    ProductSalesCube    ←──   dim_product
  SalesOrder       ←──    SalesCube           ←──   fact_sales_order_line
  (时间分析)        ←──    (SalesCube 时间维)   ←──   dim_date + date_key
```

**规划顺序（推荐）**：

1. 列出 **本体对象类型** 与 **链接**（业务语言）
2. 反推需要的 **Cube**（读模型 / 度量白名单）
3. 再落 **物理表**（fact / dim / dim_date / bridge…）

---

## 2. 物理表：类别与前缀

### 2.1 命名格式

```text
{类别前缀}_{业务域}_{实体}[_{粒度}]
```

- 全小写 **snake_case**
- **类别前缀必填**；禁止 `product_master`、`customer_dimension` 等混用后缀
- 单域实现可省略业务域：`dim_product`；多域共空间时用 `dim_sales_product`

### 2.2 表类别（7 类 + 强制时间维）

| 前缀 | 角色 | 典型粒度 | 本体读模型 | 规划必写 |
| ---- | ---- | -------- | ---------- | -------- |
| **`dim_`** | 维度 / 主数据 | 一行一实体 | 是（或经 JOIN 进 Cube） | 业务维表必写 |
| **`fact_`** | 事实 / 明细 / 事件 | 一行一业务事件 | **是（Cube 主源）** | 核心必写 |
| **`bridge_`** | 桥表（多对多） | 关系对 | 视场景 | 有多对多时必写 |
| **`map_`** | 映射 / 对照 / 码表 | 源→目标 | 辅助 | 有码表转换时写 |
| **`cfg_`** | 配置 / 参数 / 版本 | 配置行 | 一般不作分析对象 | 有预算版本等时写 |
| **`agg_`** | 预聚合 / 主题汇总 | 维组合汇总 | 可选（性能层） | 有固定汇总口径时写 |
| **`tmp_`** | 临时 / 中间 | 不限 | **否** | 仅 ETL 说明，不进核心表清单 |

### 2.3 各类约束摘要

**`fact_*`**

- 含可加性度量或事件计数
- **必须**含 **`date_key`** → `dim_date`（见 §3）
- 可保留业务日期列（如 `order_date`）作展示；**分析 JOIN 优先 `date_key`**
- 外键与维表 PK **同名**：`product_id`、`customer_id`

**`dim_*`**

- PK：`{entity}_id`（或与事实表 FK 统一的 `{entity}_key`）
- 规划注明 SCD 策略（Type 1 / Type 2）

**`bridge_*` / `map_*` / `cfg_*` / `agg_*` / `tmp_*`**

- 见 §2.2；`tmp_*` 不得作为 `bind_source` 或 Cube 唯一事实源

### 2.4 主键 / 外键约定

| 对象 | 约定 | 示例 |
| ---- | ---- | ---- |
| 时间维 PK | **`date_key`** Int32 | `20250605`（YYYYMMDD） |
| 业务维 PK | `{entity}_id` | `product_id` |
| 事实表 FK | 与维表 PK **同名** | `date_key`, `product_id` |

---

## 3. 时间维 dim_date（强制）

### 3.1 何时必须

| 场景 | 要求 |
| ---- | ---- |
| 任意含日期的 **`fact_*`** | **必须** `dim_date` + 事实表 **`date_key`** |
| 仅时点快照、无趋势 | 可豁免，规划 **显式说明理由** |
| 公历 + 会计期间 | **一张** `dim_date`，用列扩展（`fiscal_year`, `fiscal_period`） |

### 3.2 最小字段集

**表名**：`dim_date`（**全空间通常唯一一张**）

| 字段 | 类型 | 说明 |
| ---- | ---- | ---- |
| **`date_key`** | **Int32** | **PK**，推荐 `YYYYMMDD` |
| `calendar_date` | Date | 自然日 |
| `year` / `quarter` / `month` | Int | 公历层次 |
| `week_of_year` / `day_of_week` | Int | 周、星期 |
| `is_weekend` | UInt8 | 0/1 |
| `year_month` | String | 如 `2025-06` |
| `fiscal_year` / `fiscal_period` | Int | 会计日历（可选） |

**排序键**：`ORDER BY (date_key)`

### 3.3 事实表关联

```text
fact_*.date_key  →  dim_date.date_key
```

灌数：`date_key = toYYYYMMDD(order_date)`。YoY/MoM 函数优先通过 **`dim_date`** 做 period shift，而非硬编码 `toYear(order_date)`。

---

## 4. Cube：类别与命名

Cube 是 **物理表 → 分析语义 → 本体读模型** 的中间层；命名应体现 **分析主题**，而非复制表名或对象名。

### 4.1 命名格式

```text
{主题域}{分析焦点}{Cube|Analytics}
```

| 规则 | 说明 |
| ---- | ---- |
| **PascalCase** | `SalesCube`、`ProductSalesCube` |
| **后缀** | 推荐 **`Cube`**（与平台 `register_cube` 一致）；可选 `Analytics`（如 `SalesAnalytics`），**同一实现单元内统一一种** |
| **禁止** | 与对象 `code` 完全相同（`Product` ≠ Cube 名）；与物理表名相同（`dim_product`） |
| **qualified_name** | 成员为 `CubeName.member`（如 `SalesCube.sales_amount`） |

### 4.2 Cube 类别

| 类别 | 用途 | 事实源 | 命名示例 |
| ---- | ---- | ------ | -------- |
| **流程型 Process** | 以事务/事件为主线，多维度切片 | 主 `fact_*` | `SalesCube`、`GlJournalCube` |
| **主体型 Subject** | 以单一业务主体聚合（产品/客户/科目） | 同一 fact 或 subject 切片 | `ProductSalesCube`、`CustomerSalesCube` |
| **对比型 Comparison** | 预实、同比口径、A/B 版本 | 多个 fact 或带 version 维 | `BudgetVsActualCube` |
| **快照型 Snapshot** | 时点库存、余额（非可加事件） | 快照 fact 或 agg | `InventorySnapshotCube` |
| **时间增强** | 时间智能（通常 **不单独建 Cube**） | 通过 **`dim_date`** JOIN 进 Process/Subject Cube | 优先在 `SalesCube` 上挂 `year`/`month`/`fiscal_period` 维，而非孤立 `TimeSalesCube` |

> **建议**：旧示例中的 `TimeSalesCube` 在新规范下 **合并进 Process Cube** + **`dim_date`**；仅当时间主题完全独立（如专用日历配置分析）才保留独立 Cube。

### 4.3 每个 Cube 规划必写

| 列 | 说明 |
| -- | ---- |
| Cube 名 | 符合 §4.1 |
| **类别** | Process / Subject / Comparison / Snapshot |
| 事实源表 | 主 `fact_*` 表名 |
| 时间维 | 是否 JOIN `dim_date`；时间成员来自哪些列 |
| 维度 | GROUP BY / 筛选字段 |
| 度量 | 列名、聚合、业务含义 |
| 派生度量 | 表达式与口径 |
| **支撑的对象类型** | 哪些对象 `bind_source` 绑定本 Cube |

### 4.4 Cube 与多对象

- **多对象可绑同一 Cube**（如 `SalesOrder` 与 `SalesAnalysis` 均绑 `SalesCube`，属性映射不同）
- **一对象只绑一个主 Cube**（读模型）；明细补全可在函数 SQL 中 JOIN `dim_*`
- 同一 `fact_*` 可注册 **多个 Cube**（不同维度切片）

---

## 5. 本体对象：Palantir 思想与分类

### 5.1 与 Palantir Foundry Ontology 的对照

| Palantir 概念 | 搭子平台 | 命名要点 |
| ------------- | -------- | -------- |
| **Object Type** | `define_object_type(code, name, ...)` | **`code` 无前缀**，PascalCase 单数业务名 |
| **Property** | `define_property` | 业务属性名；度量/维度带 Cube `qualified_name` |
| **Link Type** | `define_link_type` | 业务关系语义，非表 FK 名 |
| **Action Type** | `define_action` | 动词短语 code |
| **Function** | `register_function` / 函数脚本 | `domain.fn.name`（带点号命名空间） |

**核心思想**（规划阶段强制）：

- 对象类型描述 **业务世界中「是什么」**，不是「哪张表」
- **先对象与链接，后表与 Cube**；允许多表/多 Cube 支撑一对象，也允许多对象视角看同一 fact
- 对象 **`code` 不加 `dim_` / `fact_` / `Obj` 前缀**；分类用 **文档标签 + 规划表格**，不写入 `code`

### 5.2 对象类型 code 格式

```text
{BusinessNoun}           # PascalCase，英文单数为主
{BusinessNoun}{Role}     # 必要时消歧，如 BudgetLine、SalesOrderLine
```

| 规则 | 正确 | 错误 |
| ---- | ---- | ---- |
| 业务名词 | `Product`, `Customer`, `SalesOrder` | `dim_product`, `ProductObject` |
| 稳定标识 | `JournalEntry`, `Account` | `TblAccount`, `FactSales` |
| 与表/Cube 区分 | `Product` + `ProductSalesCube` + `dim_product` | 三者同名 |

**中文 `name`**：面向业务用户（产品、客户、销售订单）；**`code`**：面向 API / 脚本 / 链接引用。

### 5.3 对象分类（无 code 前缀）

规划文档中为每个对象类型标注 **以下一类**（可多标签，但须有一个主分类）：

| 分类 | 英文标签 | 业务含义 | 典型对象 | 读模型来源 |
| ---- | -------- | -------- | -------- | ---------- |
| **主数据** | `Master` | 长期存在、可被多次引用 | `Product`, `Customer`, `Account`, `CostCenter` | Subject Cube 或 `dim_*` + 函数补全 |
| **事务/事件** | `Transaction` | 一次业务发生、有时间性 | `SalesOrder`, `JournalEntry`, `BudgetLine` | Process Cube / 主 `fact_*` |
| **分析上下文** | `Analytical` | 分析会话/切片上的「上下文对象」，非 ERP 主数据 | `SalesAnalysis`, `ProfitAnalysis` | Process Cube（常无独立 `dim_*`） |
| **参考** | `Reference` | 枚举型、码表级、体量小 | `Channel`, `Currency`, `OrderStatus` | `dim_*` 或 Cube 维度 |
| **配置** | `Configuration` | 版本、日历、口径规则 | `BudgetVersion`, `FiscalCalendar` | `cfg_*` 或专用 dim |

**Palantir 式自检**：

- 能否用 **一句业务话** 向非技术人员解释该对象？（「销售订单是一次成交记录」✓）
- 链接是否表达 **业务关系** 而非「表 A 的 id 等于表 B 的 id」？
- Action/Function 是否挂在 **对象** 上，而非挂在表名上？

### 5.4 bind_source 约定

| 对象分类 | 典型 bind_source |
| -------- | ---------------- |
| Master / Reference | Subject Cube 或 Process Cube 的子集 |
| Transaction | Process Cube |
| Analytical | Process Cube（同一 fact，属性偏度量/筛选） |
| Configuration | 可无 Cube；函数直读 `cfg_*` / `dim_*` |

规划须有 **对象 → Cube → 主 fact/dim** 对照表（见 §7）。

### 5.5 本体函数 function_id（补充）

对象 **`code` 无前缀**；函数仍用 **命名空间**（与 Palantir Function 类似）：

```text
{domain}.fn.{action_name}     # 如 sales.fn.get_summary, profit.fn.yoy_analysis
{domain}.action.{code}        # Action 脚本注册
```

---

## 6. 链接类型命名

链接描述 **对象之间** 的有向业务关系；与物理表 `add_relationship` **分层**，但应 **可对照**。

### 6.1 格式

```text
{from_role}_{verb}_{to_role}     # snake_case
{verb}_{to_role}                 # 简式（from 在 define_link_type 参数中已体现）
```

| 规则 | 示例 |
| ---- | ---- |
| 业务动词/介词 | `order_contains_product`, `entry_posts_to_account` |
| 基数在 API 参数中声明 | `define_link_type(..., cardinality=...)` |
| 禁止 | `product_id_fk`, `rel_sales_product`（物理层命名） |

### 6.2 与表间关系对照

| 物理关系 | 本体链接（示例） |
| -------- | ---------------- |
| `fact_sales_order_line` → `dim_product` | `SalesOrder` —*contains*→ `Product` |
| `fact_sales_order_line` → `dim_customer` | `SalesOrder` —*sold_to*→ `Customer` |
| `fact_gl_journal_entry` → `dim_account` | `JournalEntry` —*posts_to*→ `Account` |

---

## 7. 三层对照与迁移示例（销售域）

### 7.1 旧名 → 新名（物理表）

| 现名（不规范） | 新名 | 类别 |
| -------------- | ---- | ---- |
| — | **`dim_date`** | 时间维（**新增**） |
| `product_master` | `dim_product` | 维 |
| `customer_dimension` | `dim_customer` | 维 |
| `channel_dimension` | `dim_channel` | 维 |
| `sales_order_fact` | `fact_sales_order_line` | 事实（订单行粒度） |

**`fact_sales_order_line` 增补**：`date_key Int32` → `dim_date.date_key`

### 7.2 Cube（建议）

| 现 Cube | 类别 | 建议调整 |
| ------- | ---- | -------- |
| `SalesCube` | Process | 保留；事实源改为 `fact_sales_order_line`；时间维来自 **`dim_date`** |
| `ProductSalesCube` | Subject | 保留 |
| `CustomerSalesCube` | Subject | 保留 |
| `ChannelSalesCube` | Subject | 保留 |
| `TimeSalesCube` | — | **合并**进 `SalesCube`（`dim_date` 列），或标注 deprecated |

### 7.3 本体对象（基本不变，补分类）

| code | 分类 | bind_source | 主物理支撑 |
| ---- | ---- | ----------- | ---------- |
| `Product` | Master | `ProductSalesCube` | `dim_product` |
| `Customer` | Master | `CustomerSalesCube` | `dim_customer` |
| `Channel` | Reference | `ChannelSalesCube` | `dim_channel` |
| `SalesOrder` | Transaction | `SalesCube` | `fact_sales_order_line` |
| `SalesAnalysis` | Analytical | `SalesCube` | 同 fact |

### 7.4 利润域（摘要）

| 物理（新） | Cube（示例） | 对象（示例） |
| ---------- | ------------ | ------------ |
| `dim_date`, `dim_account`, `dim_cost_center` | `GlJournalCube`, `BudgetCube` | `Account`, `CostCenter` |
| `fact_gl_journal_entry`, `fact_budget_entry` | `ActualCube`, `BudgetVsActualCube` | `JournalEntry`, `BudgetLine` |

---

## 8. 规划文档写法与自检清单

### 8.1 物理层章节结构（建议）

```markdown
### 3.0 时间维（强制）
### 3.1 事实表（fact_*）
### 3.2 维度表（dim_*）
### 3.3 桥表 / 映射 / 配置 / 汇总（按需）
### 3.x 表间关系（含 fact → dim_date）
```

### 8.2 Cube 层章节结构（建议）

```markdown
## 四、Cube 层设计
### 4.0 Cube 清单与类别
| Cube | 类别 | 事实源 | 支撑对象 |
### 4.1 SalesCube（Process）…
```

### 8.3 本体层章节结构（建议）

```markdown
## 五、本体层设计
### 5.1 对象类型清单
| code | 分类 | name | bind_source |
### 5.2 对象属性 …
### 5.3 链接类型 …
### 5.4 三层对照总表
| 对象 code | 分类 | Cube | 主 fact/dim |
```

### 8.4 自检清单（在 [本体规划指南](./本体规划指南.md) 原 10 项基础上扩展）

| # | 检查项 | 通过标准 |
| - | ------ | -------- |
| 2a | **dim_date** | 含 `dim_date`，PK 为 **`date_key`** |
| 2b | **fact 时间键** | 每张 `fact_*` 含 **`date_key`** 并关联 `dim_date` |
| 2c | **表前缀** | 使用 `fact_`/`dim_`/…，无 `_master`、`_dimension` 混用 |
| 4a | **Cube 类别** | 每个 Cube 标注 Process/Subject/Comparison/Snapshot |
| 4b | **Cube 命名** | PascalCase + `Cube` 后缀；不与对象 code 同名 |
| 5a | **对象分类** | 每个对象类型标注 Master/Transaction/Analytical/Reference/Configuration |
| 5b | **对象 code** | PascalCase **无前缀**；与表名/Cube 名区分 |
| 5c | **三层对照** | 附录含 对象↔Cube↔表 对照 |
| 6a | **CATEGORY_REGISTRY** | 规划附录 B 与 `*_category_mount.py` 顶部字典一致（见 [本体分类规划与SDK扩展方案](./本体分类规划与SDK扩展方案.md)） |
| 6b | **表平台分类** | 每张表标注 平台标准分类中文名（时间维/维度表/事实表等） |
| 6c | **Cube 平台分类** | 每个 Cube 标注 流程型/主体型/对比型/快照型 |
| 6d | **对象/链接/关系分类** | 对象标 主数据/事务/分析/参考；链接与关系标扩展类别 |
| 6e | **分类挂载** | 已 run `*_category_mount.py` 或注册时 `category_347=`；侧栏与平台标准分类一致 |

---

## 9. 相关文档索引

| 文档 | 说明 |
| ---- | ---- |
| [本体规划指南](./本体规划指南.md) | 规划章节、Cube 强制、自检 |
| [销售示例 plans](../../examples/onto/销售示例/plans/规划示例_产品销售本体规划方案.md) | 完整示例 |
| [利润示例 plans](../../examples/onto/利润示例/plans/规划示例_利润分析本体方案.md) | GL 域 |
| [设备运营 plans](../../examples/onto/设备运营/plans/化工设备运营分析本体方案.md) | 设备/OEE |
| [DaziScript SDK 参考](./dazi_script_sdk_reference.md) | `register_cube`、`define_object_type` API |
| [本体脚本编写指南](./本体脚本编写指南.md) | init / seed / 表间关系实施 |
| [本体分类规划与 SDK 扩展方案](./本体分类规划与SDK扩展方案.md) | 平台分类与 CATEGORY_REGISTRY |

---

**变更记录**

| 日期 | 说明 |
| ---- | ---- |
| 2026-06-05 | 首版：物理表 7 类 + dim_date；Cube 4+1 类；本体对象 Palantir 式 5 分类；三层对照与自检扩展 |
