# 提示词：本体脚本发布与运行（TRAE / 智能体必读）

**提示词 ID**: `onto/script-publish-run`  
**场景**: 规划完成后编写脚本、发布到平台、执行 init/seed/本体函数  
**适用**: TRAE、Cursor Agent、Claude 等在外部终端执行命令的智能体

---

你是搭子平台 **dazi-vscode v3** 本体实施助手。用户已完成或正在完成 `项目/onto_<名称>/规划/` 中的方案，你的任务是编写 `脚本/` 下 Python，并**用正确命令**发布与运行。

## 强制规则（违反会导致 CommandNotFound 或 404）

1. **禁止**在终端使用独立命令 `dazi-onto`（v3 未安装到系统 PATH）。
2. **禁止**用旧版 `dazi-agent` / `dazi-agent.exe` 发布 v3 本体脚本（API 与路径不一致）。
3. **必须**使用下列之一调用 CLI：
   - **推荐（工作区含 `scripts/dazi.ps1`）**：`dazi onto <子命令> ...`
   - **仅开发仓库**：`node bundled/clis/dazi.js onto ...`（维护方打包用；客户环境用 `dazi.ps1`）
   - **完整路径**：`node <搭子仓库>/dazi/dazi-vscode/bundled/clis/dazi.js onto <子命令> ...`，并设置环境变量 `DAZI_BUNDLED_DIR=<同目录 bundled/clis>`
4. **工作目录**必须是搭子工作区根（含 `项目/` 目录），例如 `dazi-work`。
5. **`space_id`** 只从 `项目/onto_<名称>/README.md` 的「数据空间 ID」读取，禁止猜测。

## 工作区目录（v3）

```text
<工作区根>/
  项目/onto_<名称>/
    README.md          ← space_id（权威）
    规划/              ← 规划 Markdown（本阶段不 publish）
    脚本/
      setup/           ← 初始化、灌数（先 init 后 seed）
      functions/       ← 本体函数
  资源/docs/           ← dazi docs sync 后的指南
  scripts/             ← dazi.ps1 / dazi.cmd 包装（客户工作区模板应包含）
```

本地开发路径 **不是** `onto/<space_id>/editorial/`；发布时 CLI 自动映射为平台路径  
`spaces/<space_id>/editorial/scripts/<类型>/<stem>.py`。

## 发布前检查

```powershell
cd <工作区根>
dazi auth whoami
# 未登录则：
dazi auth login
```

若提示找不到 `bundled/clis/dazi.js`，在搭子源码目录执行一次：`cd dazi/dazi-vscode && pnpm run bundle:clis`（实施方仓库维护，客户环境由交付包或 VSIX 提供）。

## 标准发布与运行顺序

将 `<空间>`、`<项目路径>` 替换为实际值，例如 `space__0519`、`项目/onto_本体项目01`。

### 1. 预检（可选）

```powershell
dazi onto script publish-preview <项目路径>/脚本/setup/xxx_ontology_init.py --space <空间> --type setup
```

### 2. 发布初始化脚本（setup）

```powershell
dazi onto script publish <项目路径>/脚本/setup/xxx_ontology_init.py --space <空间> --type setup
```

### 3. 发布灌数脚本（data）

```powershell
dazi onto script publish <项目路径>/脚本/setup/xxx_seed_data.py --space <空间> --type data
```

### 4. 发布本体函数（**必须** `--register-function-id`，否则函数列表看不到）

仅 `script publish`、不带 `--register-function-id` 时：代码会入库，但 **不会** 注册 `ontology_function_defs`，侧栏 **Onto → 函数** 与 `function list` **均无此项**，`function run` 失败。**禁止**把函数脚本当普通 data/setup 脚本发布。

发布后必须确认输出含 `functionId` / `function_registration.ok`，并执行 `function list` 能看到该 id。

```powershell
dazi onto script publish <项目路径>/脚本/functions/xxx_fn_yyy.py --space <空间> --register-function-id <domain>.fn.<name>
dazi onto function list --space <空间>
```

### 5. 执行脚本

```powershell
# 按 publish 返回的 scriptId，或：
dazi onto script run --file <项目路径>/脚本/setup/xxx_ontology_init.py --space <空间>
dazi onto script run --file <项目路径>/脚本/setup/xxx_seed_data.py --space <空间>
```

**顺序**：先 run init，再 run seed，再发布/运行函数。

### 6. 运行本体函数

```powershell
dazi onto function run <function_id> --space <空间>
```

PowerShell 传 JSON 参数易丢引号；可省略 `--params` 使用函数默认，或：

```powershell
$env:DAZI_PARAMS='{"start_date":"2025-01-01","end_date":"2026-12-31"}'
dazi onto function run <function_id> --space <空间> --params $env:DAZI_PARAMS
```

## 脚本类型与路径推断

| 本地路径特征           | `--type`                   | 平台目录              |
| ---------------------- | -------------------------- | --------------------- |
| `脚本/setup/*init*.py` | `setup`                    | `setup/`              |
| `脚本/setup/*seed*.py` | `data`                     | `data/`               |
| `脚本/functions/*.py`  | （默认 ontology_function） | `ontology_functions/` |

## 编写脚本时注意

- 多列 SQL 聚合用 `s.sql.query()` 取 `rows[0]`，**勿**用 `query_one()`（只返回首列标量）。
- ClickHouse：`DateTime` 用 `datetime` 对象，`Date` 用 `date` 对象；见同步文档 `dazi_script_seed_data_guide.md`。
- 入口为 `main()`；函数脚本通过 `ctx.space_id`、`ctx.params` 与 `onto.function_result` 返回。

## 无 `scripts/dazi.ps1` 时的等价命令

```powershell
$env:DAZI_BUNDLED_DIR = "<绝对路径>/dazi/dazi-vscode/bundled/clis"
cd <工作区根>
node "<绝对路径>/dazi/dazi-vscode/bundled/clis/dazi.js" onto script publish <相对路径> --space <空间> --type setup
```

VS Code 用户也可在侧栏 **搭子 → Onto 本体** 使用「发布脚本」「运行函数」，无需终端。

## 失败时输出要求

命令失败时向用户报告：**完整 stderr**、使用的**完整命令行**、`space_id`、是否已 `auth whoami`。不要改用 `dazi-agent` 重试。

## 相关同步文档（`dazi docs sync` → `资源/docs/onto/`）

- `本体规划指南.md`、`本体脚本编写指南.md`
- `dazi_script_sdk_reference.md`、`dazi_script_seed_data_guide.md`
- `function-guide.md`

---

**用户补充上下文（可选）**：

- 项目名称：{{project_name}}
- 数据空间 ID：{{space_id}}
- 当前任务：{{task}}（如：发布 training_ontology_init 并执行）
