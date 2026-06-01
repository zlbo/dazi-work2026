# CLI 命令速查

**文档 ID**: `guides/cli-reference`

> **生产环境**：在 `dazi-work` 根目录，所有 `dazi` / `dazi onto` / `dazi flow` 命令写作  
> **`.\scripts\dazi.ps1 <子命令>`**；DRAP 在**应用项目根**（`项目/app_<名称>/`，含 `sdk/`）用 **`pnpm run dazi-app -- <子命令>`**。  
> 详见 [CLI 调用约定](./cli-invocation.md)。首次安装后运行 **`.\scripts\doctor-cli.ps1`**。

## 主 CLI（`.\scripts\dazi.ps1`）

| 命令                                    | 说明                                    |
| --------------------------------------- | --------------------------------------- |
| `.\scripts\dazi.ps1 auth login`         | 用户名密码登录                          |
| `.\scripts\dazi.ps1 auth set-token`     | 绑定 JWT Token                          |
| `.\scripts\dazi.ps1 auth whoami`        | 显示当前账号                            |
| `.\scripts\dazi.ps1 auth migrate`       | 迁移旧版认证                            |
| `.\scripts\dazi.ps1 doctor`             | 环境诊断                                |
| `.\scripts\dazi.ps1 env`                | 显示环境信息                            |
| `.\scripts\dazi.ps1 docs list`          | 列出文档                                |
| `.\scripts\dazi.ps1 docs open <id>`     | 打开文档                                |
| `.\scripts\dazi.ps1 docs sync`          | 同步内置文档到 `资源/docs/`             |
| `.\scripts\dazi.ps1 prompt list`        | 列出提示词                              |
| `.\scripts\dazi.ps1 prompt show <id>`   | 显示提示词                              |
| `.\scripts\dazi.ps1 prompt sync`        | 同步内置提示词到 `资源/prompts/`        |
| `.\scripts\dazi.ps1 examples list`      | 列出示例脚本                            |
| `.\scripts\dazi.ps1 examples open <id>` | 显示示例内容                            |
| `.\scripts\dazi.ps1 examples sync`      | 同步内置示例到 `资源/examples/`         |
| `.\scripts\dazi.ps1 migrate workspace`  | 迁移工作区                              |
| `.\scripts\dazi.ps1 migrate config`     | 迁移旧配置                              |
| `.\scripts\dazi.ps1 onto <args>`        | 本体 CLI（**勿用** `dazi-onto`）        |
| `.\scripts\dazi.ps1 flow <args>`        | 流程 CLI                                |
| `.\scripts\dazi.ps1 app <args>`         | 应用 CLI（亦可在应用项目根用 `pnpm run dazi-app`） |

## 本体（`.\scripts\dazi.ps1 onto ...`）

| 命令                                                                     | 说明             |
| ------------------------------------------------------------------------ | ---------------- |
| `.\scripts\dazi.ps1 onto space list`                                     | 空间列表         |
| `.\scripts\dazi.ps1 onto space snapshot`                                 | 拉取空间快照     |
| `.\scripts\dazi.ps1 onto space init`                                     | 初始化空间工作区 |
| `.\scripts\dazi.ps1 onto function list`                                  | 函数定义列表     |
| `.\scripts\dazi.ps1 onto function run`                                   | 执行函数         |
| `.\scripts\dazi.ps1 onto function publish`                               | 发布函数         |
| `.\scripts\dazi.ps1 onto function update-code`                           | 更新函数代码     |
| `.\scripts\dazi.ps1 onto action list/update-code/delete`                 | 动作管理         |
| `.\scripts\dazi.ps1 onto rule list/run-seed/delete`                      | 规则管理         |
| `.\scripts\dazi.ps1 onto script sync/publish/publish-preview/run/dedupe` | 脚本管理         |
| `.\scripts\dazi.ps1 onto mcp serve`                                      | 启动本体 MCP     |

## 流程（`.\scripts\dazi.ps1 flow ...`）

> **流程项目日常开发**见 [flow/flow-project-guide](../flow/flow-project-guide.md)。  
> 下列 `flow` 子命令均写作 `.\scripts\dazi.ps1 flow <...>`。

### 流程项目（`项目/flow_*/流程/<名>/`）

| 命令 | 说明 |
|------|------|
| `flow project pull --flow <id> --dir <流程目录>` | 拉取 snapshot 并拆分为 flow.json + 节点代码 |
| `flow project push --dir <dir> [--canvas]` | 提交脏代码节点；`--canvas` 含画布 |
| `flow project status --dir <dir>` | 本地代码改动 |
| `flow node push --node <uuid> --dir <dir>` | 提交单节点代码 |
| `flow node pull --node <uuid> --dir <dir>` | 拉取单节点代码 |
| `flow run node-exec --node <uuid> --dir <dir>` | 单节点测试 |
| `flow run flow-exec --dir <dir> --type debug` | 整流程运行 |
| `flow variable pull --name <名> --dir <dir>` | 拉取变量到 `变量/<名>.json` |
| `flow variable sync --dir <dir>` | 同步全部调试变量 |

### 平台级 / 旧式

| 命令 | 说明 |
|------|------|
| `flow flows list` | Flow 列表 |
| `flow flows get <id>` | Flow 详情 |
| `flow flows create` | 新建 Flow |
| `flow snapshot pull --flow <id>` | 拉取快照到 `flows/<id>/` |
| `flow snapshot push-graph` | 推送图快照 |
| `flow run start <id>` / `run debug <id>` | 启动 / 调试 Run |
| `flow run variables-list` | 查看变量 |
| `flow source list/tables/table-structure` | 数据源 |
| `flow plan compile/apply/markdown` | 执行计划 |
| `flow file list/upload/pull` | 文件管理 |
| `flow mcp serve` | Flow MCP |

## 应用（`项目/app_<名称>/` 应用项目根）

在 `dazi-work/项目/app_<名称>/` 下（须含 `sdk/`、`templates/`）：

| 命令                                                                 | 说明             |
| -------------------------------------------------------------------- | ---------------- |
| `pnpm run dazi-app -- init ...`                                      | 初始化应用       |
| `pnpm run dazi-app -- build`                                         | 构建应用         |
| `pnpm run dazi-app -- upload --space <id>`                           | 上传应用         |
| `pnpm run dazi-app -- release list`                                  | 发布管理         |
| `pnpm run dazi-app -- asset list`                                    | drap-assets 列表 |
| `pnpm run dazi-app -- manifest validate --cwd apps/<app> --scan-src` | 校验 manifest    |

等价写法（仍在 `dazi-work` 根）：`.\scripts\dazi.ps1 app <子命令>`。
