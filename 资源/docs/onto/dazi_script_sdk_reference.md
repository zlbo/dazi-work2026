# DaziScript SDK 参考

**文档 ID**: `onto/dazi-script-sdk-reference`  
**适用**: dazi-vscode v3 + 搭子平台 DaziScript（ClickHouse 数据空间）

> 给 LLM 与开发者提供精简、可执行的 SDK 规范。脚本目录、类型与 **`dazi onto script publish`** 等见 **[本体脚本编写指南](./本体脚本编写指南.md)**。  
> **执行脚本前必读（强制）**：[脚本运行常见错误处理](./脚本运行常见错误处理.md)。

## 1. 工作区与脚本放置（dazi-vscode）

| 用途                 | 路径                                                                                                        |
| -------------------- | ----------------------------------------------------------------------------------------------------------- |
| **日常开发**（推荐） | `<工作区根>/项目/<业务名>/本体/ontos/<实现名>/setup/*.py`（初始化、灌数）                                   |
|                      | `<工作区根>/项目/<业务名>/本体/ontos/<实现名>/functions/*.py`（本体函数、动作）                           |
| **空间 ID**          | `项目/<业务名>/本体/ontos/<实现名>/README.md` 中的数据空间 ID                                              |
| **本体域**           | `快速启动_<实现名>.md` §1 的 **本体域 code / ID**（`dazi onto domain ensure` 或侧栏同步）                  |
| **参考示例**         | **`资源/examples/onto/利润示例/`**、**`资源/examples/onto/销售示例/`**（侧栏 **帮助 → 示例** 或 `dazi examples sync`；总览 `onto/README.md`） |
| **本文档**           | `资源/docs/onto/dazi_script_sdk_reference.md`（`dazi docs sync` 后）                                        |

- **禁止**将 `onto/<space_id>/editorial/` 作为 v3 本地开发约定（历史路径，仅 CLI `script sync` 可能拉回平台副本）。
- 脚本入口仅需定义 **`main()`**；平台执行时自动调用，**不要**写 `if __name__ == "__main__":`。

## 2. 基本约束

- 数据引擎：**ClickHouse**
- 新建空间须显式指定（若脚本内创建空间）：
  - `storage_engine="clickhouse"`
  - `connection_config={"database": "<db_name>"}`
- 执行前确认已登录（`dazi auth whoami`）且 `dazi.serverUrl` 正确。

## 3. 顶层对象与推荐调用

常用对象：

- `space`：空间管理与切换
- `s.sql`：原始 SQL
- `s.tables`：表注册与列同步
- `s.register_cube(...)`：Cube 注册
- `s.onto`：本体定义（对象、属性、链接、函数、活动）
- `s.ontology`：对象中心能力（objects/features）
- `s.ontology_rules`：规则集与规则
- `s.scripts`：脚本记录管理
- `s.domain`：本体域成员挂载（`ontology_domain_members`；与 `s.categories` **不同**，见 §5.7）
- `output`：打印与成功提示（`output.print` / `output.success`）

命名规范（便于 LLM 推断）：

- 读操作：`exists_*`、`get_*`、`require_*`、`list_*`
- 写操作：`create_*`、`ensure_*`、`update_*`、`delete_*`
- 派生/同步：`create_from_*`、`sync_*`

推荐本体落库路径（与 **[本体规划指南](./本体规划指南.md)** 一致）：

1. `s.onto.define_object_type` → `s.onto.bind_source(..., "dazi_cube", config={"cube": ...})`
2. `s.onto.define_property`（`dimension` / `measure` 须带与 Cube 成员一致的 `qualified_name`）
3. `s.onto.define_link_type`（两端为对象类型 **`code`**，非 Cube 名）
4. `s.onto.register_function` / `s.onto.define_action`
5. `s.ontology.features.attach(object_code, feature_type, feature_id)`（`feature_type`: `function | action | rule`）

**关于 `s.ontology.objects.create_from_cubes`**：SDK 仍提供，**易与业务语义脱节**；规划文档、示例包与交付脚本**不应依赖**。仅隔离烟测按需使用。

## 4. 返回结构规范

### 4.1 批量派生返回（ResultBatch）

```json
{
  "ok": true,
  "created": [],
  "updated": [],
  "skipped": [],
  "errors": [],
  "summary": {
    "requested": 0,
    "created": 0,
    "updated": 0,
    "skipped": 0,
    "errors": 0
  }
}
```

### 4.2 特征绑定返回（示例）

```json
{
  "ok": true,
  "id": "xxx",
  "created": true,
  "updated": false,
  "message": ""
}
```

## 5. 模块速查

### 5.1 `space`

- `s = space.create(name, space_id=None, storage_engine="clickhouse", connection_config={"database": ...}, ...)`
- `s = space.get(name_or_id)`
- `space.use(handle_or_name)`

### 5.2 `s.sql`

- `s.sql.query(sql)` / `s.sql.query_one(sql)` / `s.sql.execute(sql)`
- `s.sql.insert_rows(table, rows)`（`rows` 为 `list[dict]`）

**`query_one` 与多列聚合**

- `query_one` 适合 `SELECT count()` 等**单列标量**；对 `SELECT sum(a), count(b) ...` 等多列聚合，**勿**对返回值调用 `.get()`（可能得到 float 而非 dict）。
- **推荐**：`rows = s.sql.query(sql); row = rows[0] if rows else {}`（函数脚本内为 `p.sql.query`）。详见 [脚本运行常见错误处理](./脚本运行常见错误处理.md#2-sql-聚合查询query_one-返回类型)。

### 5.2.1 本体函数输出（`ontology_function`）

与 setup/seed 不同，本体函数运行时平台注入 `ctx`、`space`、`onto`：

| 要点 | 说明 |
| ---- | ---- |
| 入口 | `def main():`（**无** `params` 形参） |
| 入参 | `ctx.params` → `p.get_params()` |
| 出参 | **`return p.function_result(columns=..., data=..., row_count=...)`** |
| 禁止 | `output.print_json()`（`OutputModule` 无此方法）、裸 `return {"k": v}` |

标准模板：`资源/examples/onto/_templates/ontology_function_template.py`。详见 [function-guide](./function-guide.md#函数脚本结构标准模板)、[脚本运行常见错误处理 §3](./脚本运行常见错误处理.md#3-函数输出禁止-outputprint_json)。

**ClickHouse：`INSERT ... VALUES` 与注释**

- **`VALUES` 与各元组之间禁止 SQL 行注释 `--`**，否则易出现 `Code: 27` 等解析错误。
- **推荐**：大批量灌数用 **`s.sql.insert_rows`**；详见 **[dazi_script_seed_data_guide](./dazi_script_seed_data_guide.md)**。

### 5.3 `s.tables`

- `s.tables.register(table_name, display_name=..., description=..., label=..., category_347=...)` — `label` 为 `display_name` 简写别名；已注册时可刷新表显示名与说明；`category_347` 为 平台标准分类中文名（如 `"维度表"`），注册后**即时挂载**平台分类
- `s.tables.sync_columns(table_name)` — 从物理库同步列；未显式传入元数据时仅**推断** `display_name`（token 词典），**不**写入业务 `description`
- `s.tables.set_column_meta(table_name, columns=[{name, display_name, description, business_role}], force=False)` — 批量写入列显示名与说明（须先 register + sync_columns）
- `s.tables.register_with_meta(table_name, display_name=..., description=..., columns=[...], force_column_meta=False, category_347=...)` — 上三者合一（**推荐** setup 脚本使用）
- `s.tables.list()` / `s.tables.discover()`
- `s.tables.add_relationship(from_table, to_table, join_sql, relationship_type="many_to_one", join_keys=None, description=None, category_347=...)` — 注册**数据空间表间关系**（幂等）；`category_347` 如 `"主数据关联"`、`"时间关联"`

### 5.4 Cube

- `s.register_cube(name, table, title, measures, dimensions, category_347=...)` — `category_347` 如 `"流程型"`、`"主体型"`

### 5.5 `s.onto`

- `s.onto.define_object_type(code, name, ..., category_347=...)` — 如 `category_347="主数据"`
- `s.onto.bind_source(object_type_code, "dazi_cube", config={"cube": "CubeName"})`
- `s.onto.define_property(...)`
- `s.onto.define_link_type(code, name, from_object_type_code, to_object_type_code, ..., category_347=...)` — 如 `category_347="归属关系"`
- `s.onto.register_function(function_id, adapter, ..., category_347=...)` — 如 `category_347="总览分析"`
- `s.onto.define_action(action_code, ...)`

**常见误用**（setup 脚本）：不存在 `s.onto.sync_metrics()`、`s.cubes.upsert`；`define_object_type` 第二参数为 `name` 非 `label`；链接类型参数为 `from_object_type_code` / `to_object_type_code`。对照表见 [脚本运行常见错误处理](./脚本运行常见错误处理.md#1-setup-脚本-api-误用)。

### 5.6 `s.categories`（平台分类挂载）

挂载到 `ads_categories` 默认根下的平级目录，桥表关联表/Cube/对象/关系/链接/函数。分类名必须与 [本体命名规范](./本体命名规范_物理表Cube与对象.md) 中的**平台标准分类中文名**一致（如「维度表」「流程型」「总览分析」）。详见 [本体分类规划与SDK扩展方案](./本体分类规划与SDK扩展方案.md)。

> **术语说明**：SDK 参数 `category_347`、`ensure_347` 与 CLI `--register-platform-category` 均表示**平台标准分类**（侧栏分组名），与内部文档编号无关；`category_347` 为历史参数名，请传入标准中文分类名。

- `s.categories` — `CategoryManager` 实例（按空间懒加载）
- `s.categories.ensure_347(kind, category)` — 按平台标准分类名创建平级目录（幂等）；`kind` 支持 `table` / `cube` / `object` / `relation` / `link` / `function`
- `s.categories.assign_table(category, table_name)` — 挂载物理表
- `s.categories.assign_cube(category, cube_name)` — 挂载 Cube
- `s.categories.assign_object(category, object_type_code)` — 挂载对象类型
- `s.categories.assign_relation(category, from_table, to_table)` — 挂载表间关系
- `s.categories.assign_link(category, link_code)` — 挂载链接类型
- `s.categories.assign_function(category, function_id)` — 挂载本体函数（如 `profit.fn.get_summary`）
- `s.categories.auto_assign_tables(table_names)` — 按表名前缀自动推断平台分类并挂载
- `s.categories.apply_registry(CATEGORY_REGISTRY, skip_missing=True, kinds=None)` — 批量应用注册表；`kinds` 可限定资源类（默认六类全挂；推荐在 `*_category_mount.py` 中一次性执行）

**`CATEGORY_REGISTRY` 结构**（与规划附录 B 对齐）：

```python
CATEGORY_REGISTRY = {
    "table": {"维度表": ["dim_account"], "事实表": ["fact_gl_journal_entry"]},
    "cube": {"流程型": ["ActualCube"], "主体型": ["AccountActualCube"]},
    "object": {"主数据": ["Account"], "事务": ["JournalEntry"], "分析": ["ProfitAnalysis"]},
    "relation": {"时间关联": [("fact_x", "dim_date")], "主数据关联": [("fact_x", "dim_y")]},
    "link": {"归属关系": ["entry_belongs_account"], "分析归因": ["analysis_by_account"]},
    "function": {"总览分析": ["profit.fn.get_summary"]},  # 函数未注册时须 skip_missing=True
}
```

**两种用法**（可并存，挂载幂等）：

1. **批量 — `*_category_mount.py`**（推荐）：全量 `CATEGORY_REGISTRY` + `apply_registry`（init + seed + 全部函数 publish **之后**）
2. **内联**（注册时即时挂载，可与 1 并存）：

```python
s.tables.register_with_meta("dim_product", display_name="产品维表", category_347="维度表", ...)
s.register_cube("SalesCube", table=fact, title="...", category_347="流程型", ...)
s.onto.define_object_type("Product", "产品", category_347="主数据")
s.tables.add_relationship(..., category_347="主数据关联")
s.onto.define_link_type("order_contains_product", "...", ..., category_347="归属关系")
```

### 5.7 `s.domain`（本体域成员挂载）

将表/Cube/对象/链接/函数等资源挂入 **本体域**（写入 `ontology_domain_members`），供管理端 **本体域详情树** 展示。与 §5.6 **平台分类**（`ads_categories`）是**两套独立机制**：

| 维度 | `s.categories` | `s.domain` |
| ---- | -------------- | ---------- |
| 存储 | 平台分类桥表 | `ontology_domain_members` |
| 前端 | 空间侧栏分类视图 | **本体域**详情（各 kind 的 count / 树） |
| 脚本时机 | `*_category_mount.py` | **category_mount 之后**（同脚本末尾或独立 `*_domain_mount.py`） |

**域 code / ID**：从实现单元 `快速启动_<名>.md` §1 读取（扩展创建或 `dazi onto domain ensure` 后回写）。`function_id` 前缀建议与 **本体域 code** 一致（如 `profit01.fn.get_summary`）。

- `s.domain.ensure(code, name, ...)` — 幂等创建/更新域（通常扩展已 ensure，脚本内可省略）
- `s.domain.mount(domain_code_or_id, kind, keys, pinned=False, strict=True)` — 按业务键挂成员
- `s.domain.apply_registry(DOMAIN_REGISTRY, strict=False)` — 批量入域（推荐）
- `s.domain.unmount(domain, kind, keys)` — 按业务键移除
- `s.domain.tree(domain)` — 域树（调试）
- `s.domain.list()` — 空间内域列表
- `s.domain.backfill_default(code=..., name=...)` — **存量回填**（整空间资源挂入指定域；共享空间慎用）

**`DOMAIN_REGISTRY` 结构**（members 的 kind 用 SDK 规范名；`object` / `link` 会自动归一为 `object_type` / `link_type`）：

```python
DOMAIN_CODE = "profit01"  # 与快速启动 §1 本体域 code 一致

DOMAIN_REGISTRY = {
    "code": DOMAIN_CODE,
    "name": "利润分析01",
    "members": {
        "table": ["dim_account", "fact_pl_budget"],
        "cube": ["ProjectProfitCube", "BudgetVsActualCube"],
        "object_type": ["Account", "Project", "ProfitAnalysis"],
        "link_type": ["budget_for_project", "profit_analysis_by_project"],
        "function": ["profit01.fn.get_summary", "profit01.fn.project_profit"],
        # "relation"：域成员键为 relationship 主键，非 (from_table, to_table) 元组；可暂省略
    },
}

s.domain.apply_registry(DOMAIN_REGISTRY, strict=False)
```

**从 `CATEGORY_REGISTRY` 生成 members**（附录 B 与域成员资源集一致时，可在 `*_category_mount.py` 末尾追加）：

```python
def _flatten_for_domain(reg):
    kind_map = {"object": "object_type", "link": "link_type"}
    members = {}
    for kind, cats in reg.items():
        if kind == "relation":
            continue
        dk = kind_map.get(kind, kind)
        keys = [x for items in cats.values() for x in items if not isinstance(x, tuple)]
        if keys:
            members[dk] = keys
    return members

s.domain.apply_registry(
    {"code": DOMAIN_CODE, "name": DOMAIN_NAME, "members": _flatten_for_domain(CATEGORY_REGISTRY)},
    strict=False,
)
```

**验收**：管理端打开 §1 的 **本体域 ID** → 表/对象/Cube/函数 kind **count > 0** 且可展开；或 `dazi onto domain show --domain-id <id>`。

### 5.8 `s.ontology` / `s.ontology_rules` / `s.scripts`

见上文；规则：`ensure_rule_set` + `upsert_rule`；脚本记录：`create` / `ensure` / `list` 等。

## 6. 标准初始化流程（建议）

1. 确认 `space_id`（实现单元 README）与 **本体域 code/ID**（快速启动 §1；未同步则 `dazi onto domain ensure`）
2. 建表与灌数（`s.sql`；灌数规范见 seed 指南）
3. `s.tables.register_with_meta`（`TABLE_REGISTRY` 含表/列 `display_name`、`description`）
4. **`s.tables.add_relationship`**（与规划「表间关系」一致；**勿省略**）
5. `s.register_cube`
6. `s.onto` 定义对象、属性、链接
7. 注册函数/动作：`dazi onto script publish ... --register-function-id`（可选 `--register-platform-category`）；**发布后** `save-test-arguments`
8. 函数齐后 run `*_category_mount.py`（全量 **平台分类**；或依赖步骤 7 内联 `--register-platform-category`）
9. **同脚本末尾或独立脚本**：`s.domain.apply_registry(DOMAIN_REGISTRY)`（**本体域成员**；见 §5.7）
10. 配置规则（如需要）

## 7. 在 dazi-vscode 中发布与运行

开发完成后，在工作区根目录：

```bash
# 预检
dazi onto script publish-preview 项目/<业务名>/本体/ontos/<实现名>/setup/my_setup.py --space <space-id>

# 发布（初始化/灌数类脚本）
dazi onto script publish 项目/<业务名>/本体/ontos/<实现名>/setup/my_setup.py --space <space-id>

# 发布并注册为本体函数
dazi onto script publish 项目/<业务名>/本体/ontos/<实现名>/functions/my_func.py \
  --space <space-id> \
  --register-function-id my_func

# 运行已入库函数
dazi onto function run my_func --space <space-id> --params '{}'
```

亦可用侧栏 **Onto 本体** → 发布函数 / 运行函数。

## 8. 回归与 JSON 摘要

- 支持 `--json` 时，输出前缀统一：`__JSON_SUMMARY__`
- 非 0 退出码即失败
- 会改写数据的步骤须提供跳过/禁用开关

**内置参考示例**（在用户工作区：**侧栏 帮助 → 示例 → 下载所有示例**，或执行 `dazi examples sync`，得到 **`资源/examples/`**；可复制到 **`项目/<业务名>/本体/ontos/<实现名>/setup/`** 或 **`functions/`** 再改，勿直接改写同步下来的只读备份）：

- **规划全文**：`资源/examples/onto/<示例>/plans/*.md`（推荐 `销售示例/plans/规划示例_产品销售本体规划方案.md`）
- **常见错误**（，**非**通用模板）：`脚本运行常见错误处理.md` 中的已废弃客户路径 — 使用通用占位符
- **利润示例（GL 域）**：`资源/examples/onto/利润示例/setup/profit_ontology_init.py`、`profit_seed_data.py`、`functions/profit_fn_*.py`、`functions/test_arguments/`
- **销售示例（推荐，含表间关系 + test_arguments）**：`资源/examples/onto/销售示例/setup/sales_ontology_init.py`、`sales_seed_data.py`、`functions/sales_fn_*.py`
- **脚本运行纠错（实录）**：`资源/docs/onto/脚本运行常见错误处理.md` — setup API、`query_one`、CLI test_arguments 踩坑
