# DaziScript SDK 参考

**文档 ID**: `onto/dazi-script-sdk-reference`  
**适用**: dazi-vscode v3 + 搭子平台 DaziScript（ClickHouse 数据空间）

> 给 LLM 与开发者提供精简、可执行的 SDK 规范。脚本目录、类型与 **`dazi onto script publish`** 等见 **[本体脚本编写指南](./本体脚本编写指南.md)**。

## 1. 工作区与脚本放置（dazi-vscode）

| 用途                 | 路径                                                                                                        |
| -------------------- | ----------------------------------------------------------------------------------------------------------- |
| **日常开发**（推荐） | `<工作区根>/项目/onto_<项目名>/脚本/*.py`                                                                   |
| **空间 ID**          | `项目/onto_<项目名>/README.md` 中的数据空间 ID                                                              |
| **参考示例**         | `资源/examples/onto/setup/`、`资源/examples/onto/function/`（侧栏 **帮助 → 示例** 或 `dazi examples sync`） |
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

**ClickHouse：`INSERT ... VALUES` 与注释**

- **`VALUES` 与各元组之间禁止 SQL 行注释 `--`**，否则易出现 `Code: 27` 等解析错误。
- **推荐**：大批量灌数用 **`s.sql.insert_rows`**；详见 **[dazi_script_seed_data_guide](./dazi_script_seed_data_guide.md)**。

### 5.3 `s.tables`

- `s.tables.register(table_name, label=...)`
- `s.tables.sync_columns(table_name)`
- `s.tables.list()` / `s.tables.discover()`
- `s.tables.add_relationship(...)`

### 5.4 Cube

- `s.register_cube(name, table, title, measures, dimensions)`

### 5.5 `s.onto`

- `s.onto.define_object_type(code, name, ...)`
- `s.onto.bind_source(object_type_code, "dazi_cube", config={"cube": "CubeName"})`
- `s.onto.define_property(...)`
- `s.onto.define_link_type(code, name, from_object_type_code, to_object_type_code, ...)`
- `s.onto.register_function(function_id, adapter, ...)`
- `s.onto.define_action(action_code, ...)`

### 5.6 `s.ontology` / `s.ontology_rules` / `s.scripts`

见上文；规则：`ensure_rule_set` + `upsert_rule`；脚本记录：`create` / `ensure` / `list` 等。

## 6. 标准初始化流程（建议）

1. 确认 `space_id`（项目 README）
2. 建表与灌数（`s.sql`；灌数规范见 seed 指南）
3. `s.tables.register` + `sync_columns`
4. `s.register_cube`
5. `s.onto` 定义对象、属性、链接
6. 注册函数/动作并 `features.attach`
7. 配置规则（如需要）

## 7. 在 dazi-vscode 中发布与运行

开发完成后，在工作区根目录：

```bash
# 预检
dazi onto script publish-preview 项目/onto_<项目名>/脚本/my_setup.py --space <space-id>

# 发布（初始化/灌数类脚本）
dazi onto script publish 项目/onto_<项目名>/脚本/my_setup.py --space <space-id>

# 发布并注册为本体函数
dazi onto script publish 项目/onto_<项目名>/脚本/my_func.py \
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

**内置参考示例**（在用户工作区：**侧栏 帮助 → 示例 → 下载所有示例**，或执行 `dazi examples sync`，得到 **`资源/examples/`**；可复制到 **`项目/<onto_项目名>/脚本/`** 再改，勿直接改写同步下来的只读备份）：

- 初始化：**`<工作区根>/资源/examples/onto/setup/profit_ontology_init.py`**
- 函数样例：**`<工作区根>/资源/examples/onto/function/profit_fn_*.py`**
