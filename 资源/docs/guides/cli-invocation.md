# CLI 调用约定（生产交付）

**文档 ID**: `guides/cli-invocation`  
**适用**: 开发人员仅持有 **`dazi-work/`** + **`dazi-vscode.vsix`**，**无** monorepo 源码

## 原则

默认交付（仅 `dazi-work` + vsix）**不**要求全局 PATH；请用 **`dazi`**。  
开发机可选安装 **`@dazitech/cli`**（pnpm 全局）后直接使用 `dazi` / `dazi-flow`。

## 命令前缀

| 场景                                     | 工作目录                                       | 命令形式                            |
| ---------------------------------------- | ---------------------------------------------- | ----------------------------------- |
| 本体 / 流程 / 鉴权 / 数据 / 文档（默认） | **`dazi-work` 根**                             | `dazi <子命令...>`                  |
| 同上（已 `pnpm add -g @dazitech/cli`）   | **`dazi-work` 根**（自动识别）或任意目录       | `dazi <子命令...>`、`dazi flow ...` |
| DRAP 应用                                | **`dazi-work/项目/app_<名称>/`**（应用项目根） | `pnpm run dazi-app -- <子命令...>`  |
| 环境自检                                 | **`dazi-work` 根**                             | `.\scripts\doctor-cli.ps1`          |

CMD 用户：`scripts\dazi.cmd`、`scripts\doctor-cli.cmd`（转发到同名 `.ps1`）。

## 首次安装后（推荐顺序）

```powershell
# 1) 安装扩展
code --install-extension dazi-vscode-3.x.x.vsix

# 2) 打开 dazi-work 为 VS Code 工作区根

# 3) 自检 CLI（无需源码、无需 pnpm run bundle:clis）
cd D:\path\to\dazi-work
.\scripts\doctor-cli.ps1

# 4) 登录
dazi auth login
# 或
dazi auth set-token --token "<jwt>"

# 5) 验证
dazi auth whoami
dazi onto function list --space <space-id>
```

## 文档中的写法对照

内置帮助文档里的可运行示例统一采用 **`dazi`**，等价关系如下：

| 文档示例                                                         | 含义                                                                    |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `dazi auth whoami`                                               | 原 `dazi auth whoami`                                                   |
| `dazi onto script publish ...`                                   | 原 `dazi onto script publish ...`（**勿用** `dazi-onto`）               |
| `dazi flow project pull --flow 98 --dir 项目\flow_x\流程\MyFlow` | 流程项目拉取                                                            |
| `dazi flow run node-exec --node <uuid> --dir <流程目录>`         | 单节点测试                                                              |
| `pnpm run dazi-app -- upload ...`                                | 原 `dazi-app upload ...`（须在**应用项目根**，含 `sdk/`、`templates/`） |

扩展侧栏、命令面板触发的操作与上述 CLI **同源**（bundled `clis/*.js`）。

### 流程子命令（`flow` → `dazi-flow`）

`dazi flow …` **不会**执行独立的 `dazi-flow.exe`，而是：

1. `dazi.ps1` 设置 `DAZI_BUNDLED_DIR`，在 **dazi-work 根**执行 `node bundled/clis/dazi.js`
2. `dazi.js` 将 `flow` 后所有参数 **转发**给 `node bundled/clis/dazi-flow.js`

因此文档里的 `dazi-flow project pull …` 在 Trae / VS Code 交付环境中应写为：

```powershell
dazi flow project pull --flow 98 --dir "项目\flow_xxx\流程\MyFlow"
```

流程项目开发详见 [flow/flow-project-guide](../flow/flow-project-guide.md)。

## CLI 解析来源（doctor-cli 会检查）

1. 环境变量 `DAZI_BUNDLED_DIR`
2. `dazi-work/tools/dazi-clis/`（可选离线包）
3. 已安装扩展（路径因 IDE 而异）
   - Trae：`%USERPROFILE%\.trae\extensions\dazitech.dazi-vscode-*\bundled\clis`
   - Cursor / VS Code：`.cursor\extensions` 或 `.vscode\extensions`
   - 也可：`%VSCODE_EXTENSIONS%`、`dazi-work\tools\dazi-clis`（`sync-clis-from-extension.ps1`）

## 常见错误

| 现象               | 原因                                      | 处理                                            |
| ------------------ | ----------------------------------------- | ----------------------------------------------- |
| `dazi-onto` 找不到 | v3 无此全局命令                           | 改用 `dazi onto ...`                            |
| `dazi` 找不到      | 未装 vsix / 未用包装脚本 / 未全局安装 CLI | `doctor-cli.ps1` 或 `pnpm add -g @dazitech/cli` |
| `dazi-app` 找不到  | 未在应用项目根或未 pnpm install           | `cd 项目/app_<名> && pnpm install`              |

## 相关文档

- [CLI 命令参考](./cli-reference.md)
- [故障排查](./troubleshooting.md)
- 工作区脚本说明：`dazi-work/scripts/README.md`（交付包内）
