# 故障排查

**文档 ID**: `guides/troubleshooting`

> 终端命令统一使用 **`dazi-work` 根目录** 下的 `dazi`（见 [CLI 调用约定](./cli-invocation.md)）。

## CLI 命令找不到（优先排查）

```powershell
cd D:\path\to\dazi-work
.\scripts\doctor-cli.ps1
```

常见原因：

| 原因                                 | 处理                                                                                                                              |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| 未安装 `dazi-vscode.vsix`            | 安装扩展后重跑 doctor-cli                                                                                                         |
| **Trae 已装扩展但 doctor 报未安装**  | Trae 扩展在 `%USERPROFILE%\.trae\extensions`；更新 `dazi-work/scripts` 后重跑 doctor，或 `.\scripts\sync-clis-from-extension.ps1` |
| 扩展在但 `bundled/clis/dazi.js` 缺失 | 用完整 `pnpm run vsix` 重打包装；勿用缺 bundled 的旧包                                                                            |
| 直接输入 `dazi` / `dazi-onto`        | 改用 `dazi ...`（无全局 `dazi-onto`）                                                                                             |
| 未安装 Node.js 18+                   | 安装 Node 并加入 PATH                                                                                                             |

环境详情：

```powershell
dazi doctor
dazi env
```

## 401 未授权

```powershell
dazi auth whoami
dazi auth login
dazi auth set-token --token "<new-token>"
```

Token 保存在 `~/.dazi/auth.json`，检查是否过期。

## 扩展侧栏空白

1. 检查 `dazi.serverUrl` 配置是否正确
2. 执行 `dazi auth whoami` 确认登录状态
3. 右键侧栏节点选「刷新」

## 工作区目录找不到

```powershell
dazi doctor --workspace-root D:\path\to\dazi-work
```

或在 VS Code 设置中配置 `dazi.workspaceRoot`。

## 从 v2 迁移后命令不匹配

| 旧命令                          | v3 命令（dazi-work 根目录） |
| ------------------------------- | --------------------------- |
| `dazi-agent snapshot refresh`   | `dazi onto space snapshot`  |
| `dazi-agent function-def list`  | `dazi onto function list`   |
| `dazi-agent flow snapshot pull` | `dazi flow snapshot pull`   |

## MCP 连不上

检查 `.cursor/mcp.json` 配置。MCP 需能调用 bundled CLI，示例：

```powershell
$env:DAZI_BUNDLED_DIR = "$env:USERPROFILE\.cursor\extensions\dazitech.dazi-vscode-3.0.0\bundled\clis"
node "$env:DAZI_BUNDLED_DIR\dazi.js" mcp stdio
```

或使用 `dazi mcp stdio`（在 dazi-work 根目录）。

## DRAP：`dazi-app` 找不到

```powershell
cd D:\path\to\dazi-work\项目\app_<名称>
pnpm install
pnpm run dazi-app -- --version
```

应用 CLI 由 bundled + 启动器提供，**不需要** monorepo 源码。
