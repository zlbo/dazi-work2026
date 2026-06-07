# CLI 命令速查

**文档 ID**: `guides/cli-reference`

> **生产环境**：在 `dazi-work` 根目录，所有 `dazi` / `dazi onto` / `dazi flow` 命令写作  
> **`dazi <子命令>`**；DRAP 在**应用项目根**（`项目/app_<名称>/`，含 `sdk/`）用 **`pnpm run dazi-app -- <子命令>`**。  
> 详见 [CLI 调用约定](./cli-invocation.md)。首次安装后运行 **`.\scripts\doctor-cli.ps1`**。

## 主 CLI（`dazi`）

| 命令                      | 说明                                               |
| ------------------------- | -------------------------------------------------- |
| `dazi auth login`         | 用户名密码登录                                     |
| `dazi auth set-token`     | 绑定 JWT Token                                     |
| `dazi auth whoami`        | 显示当前账号                                       |
| `dazi auth migrate`       | 迁移旧版认证                                       |
| `dazi doctor`             | 环境诊断                                           |
| `dazi env`                | 显示环境信息                                       |
| `dazi docs list`          | 列出文档                                           |
| `dazi docs open <id>`     | 打开文档                                           |
| `dazi docs sync`          | 同步内置文档到 `资源/docs/`                        |
| `dazi prompt list`        | 列出提示词                                         |
| `dazi prompt show <id>`   | 显示提示词                                         |
| `dazi prompt sync`        | 同步内置提示词到 `资源/prompts/`                   |
| `dazi examples list`      | 列出示例脚本（`--category onto` 过滤本体类）     |
| `dazi examples show <id>` | 显示示例内容（如 `onto/sales/plan`）               |
| `dazi examples sync`      | 同步内置示例到 `资源/examples/`（含完整 `onto/` 树） |
| `dazi examples onto list` | 列出本体完整示例注册表（读 `onto/index.json`）     |
| `dazi examples onto suggest [关键词]` | 按业务域推荐对照示例（规划前选用）   |
| `dazi examples onto show <id>` | 显示示例路径；`--plan` / `--readme` 输出全文  |
| `dazi migrate workspace`  | 迁移工作区                                         |
| `dazi migrate config`     | 迁移旧配置                                         |
| `dazi onto <args>`        | 本体 CLI（**勿用** `dazi-onto`）                   |
| `dazi flow <args>`        | 流程 CLI                                           |
| `dazi app <args>`         | 应用 CLI（亦可在应用项目根用 `pnpm run dazi-app`） |

**本体规划阶段常用**：

```powershell
dazi examples sync
dazi examples onto suggest 设备 OEE
dazi examples onto show equip-ops --plan
```

索引真源：`examples/onto/index.yaml`（人工维护）→ `index.json`（`copy:bundled` 时生成）。详见 [本体规划指南](../onto/本体规划指南.md)。

## 本体（`dazi onto ...`）

| 命令                                                       | 说明             |
| ---------------------------------------------------------- | ---------------- |
| `dazi onto space list`                                     | 空间列表         |
| `dazi onto space snapshot`                                 | 拉取空间快照     |
| `dazi onto space init`                                     | 初始化空间工作区 |
| `dazi onto function list`                                  | 函数定义列表     |
| `dazi onto function run`                                   | 执行函数         |
| `dazi onto function publish`                               | 发布函数         |
| `dazi onto function update-code`                           | 更新函数代码     |
| `dazi onto action list/update-code/delete`                 | 动作管理         |
| `dazi onto rule list/run-seed/delete`                      | 规则管理         |
| `dazi onto script sync/publish/publish-preview/run/dedupe` | 脚本管理         |
| `dazi onto mcp serve`                                      | 启动本体 MCP     |

## 流程（`dazi flow ...`）

> **流程项目日常开发**见 [flow/flow-project-guide](../flow/flow-project-guide.md)。

### 流程项目（`项目/<业务名>/流程/flows/<流程名>/`）

> `--dir` 须含 `flow.json`，推荐绝对路径；禁止在 `dazi-work` 工作区根 `--dir .`。

| 命令                                                  | 说明                                        |
| ----------------------------------------------------- | ------------------------------------------- |
| `dazi flow project pull --flow <id> --dir <流程目录>` | 拉取 snapshot 并拆分为 flow.json + 节点代码 |
| `dazi flow project push --dir <dir> [--canvas]`       | 提交脏代码节点；**配置变更必须** `--canvas`   |
| `dazi flow project doctor --dir <dir>`                | 检查 flow.json / meta / 节点/ 一致性        |
| `dazi flow project repair-meta --dir <dir>`           | 修复 flow.meta.json 索引                    |
| `dazi flow project status --dir <dir>`                | 本地代码改动                                |
| `dazi flow node push --node <uuid> --dir <dir>`       | 提交单节点代码                              |
| `dazi flow node pull --node <uuid> --dir <dir>`       | 拉取单节点代码                              |
| `dazi flow run node-exec --node <uuid> --dir <dir>`   | 单节点测试                                  |
| `dazi flow run flow-exec --dir <dir> --type debug`    | 整流程运行                                  |
| `dazi flow variable pull --name <名> --dir <dir>`     | 拉取变量到 `变量/<名>.json`                 |
| `dazi flow variable sync --dir <dir>`                 | 同步全部调试变量                            |

### 平台级 / 旧式

| 命令                                           | 说明                     |
| ---------------------------------------------- | ------------------------ |
| `dazi flow flows list`                         | Flow 列表                |
| `dazi flow flows get <id>`                     | Flow 详情                |
| `dazi flow flows create`                       | 新建 Flow                |
| `dazi flow snapshot pull --flow <id>`          | 拉取快照到 `flows/<id>/` |
| `dazi flow snapshot push-graph`                | 推送图快照               |
| `dazi flow run start <id>` / `run debug <id>`  | 启动 / 调试 Run          |
| `dazi flow run variables-list`                 | 查看变量                 |
| `dazi flow source list/tables/table-structure` | 数据源                   |
| `dazi flow plan compile/apply/markdown`        | 执行计划                 |
| `dazi flow file list/upload/pull`              | 文件管理                 |
| `dazi flow mcp serve`                          | Flow MCP                 |

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

等价写法（仍在 `dazi-work` 根）：`dazi app <子命令>`。
