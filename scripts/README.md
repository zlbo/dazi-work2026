# dazi-work CLI 包装脚本

TRAE、Cursor 终端、CI 等环境**默认没有**全局命令 `dazi` / `dazi-onto`（v3 未安装到 PATH）。请用本目录脚本调用 bundled CLI。

## 解析顺序（适配生产机仅有 dazi-work + vsix）

`dazi.ps1` 会按顺序自动查找 `dazi.js`：

1. 环境变量 `DAZI_BUNDLED_DIR`
2. `dazi-work/tools/dazi-clis`（建议交付包携带）
3. 已安装 **v3** 扩展目录（按 IDE 不同路径不同）  
   - **Trae**：`%USERPROFILE%\.trae\extensions\dazitech.dazi-vscode-*\bundled\clis`  
   - **Cursor**：`%USERPROFILE%\.cursor\extensions\...`  
   - **VS Code**：`%USERPROFILE%\.vscode\extensions\...`  
   - 自定义：`%VSCODE_EXTENSIONS%` 或 `%DAZI_EXTENSIONS_DIR%`

> 这意味着生产机**不需要源码仓库**，只要装了 `dazi-vscode.vsix` 即可运行。

## 自检（推荐安装 vsix 后第一步）

```powershell
cd d:\...\dazi-work
.\scripts\doctor-cli.ps1
# 或 CMD：scripts\doctor-cli.cmd
# JSON 输出（CI）：.\scripts\doctor-cli.ps1 -Json
```

检查项：Node 版本、`bundled/clis` 解析路径、四个 CLI 文件、`auth whoami`、`runtime-apps`、`dazi-app`。

## 用法（在 `dazi-work` 目录下）

```powershell
# PowerShell
.\scripts\dazi.ps1 auth whoami
.\scripts\dazi.ps1 onto script publish 项目/onto_本体项目01/脚本/setup/training_ontology_init.py --space space__0519 --type setup
.\scripts\dazi.ps1 onto script run --file 项目/onto_本体项目01/脚本/setup/training_ontology_init.py --space space__0519
```

```cmd
scripts\dazi.cmd onto function list --space space__0519
```

## 生产交付建议（推荐）

给前端/本体开发人员交付：

- `dazi-work/`（含 `scripts/dazi.ps1`、`scripts/dazi.cmd`）
- **`dazi-work/tools/dazi-clis/*.js`**（4 个 CLI，终端**优先**用此目录，不依赖扩展路径）
- `dazi-vscode-<version>.vsix`（侧栏 UI；终端 CLI 有 `tools/dazi-clis` 即可）

发版前在源码机执行（更新离线 CLI）：

```powershell
cd dazi\dazi-vscode
pnpm run bundle:clis
cd ..\..\dazi-work
.\scripts\populate-clis-from-vscode-build.ps1
```

安装后验证：

```powershell
cd d:\...\dazi-work
.\scripts\doctor-cli.ps1
.\scripts\dazi.ps1 --version
.\scripts\dazi.ps1 auth whoami
.\scripts\dazi.ps1 onto function list --space <space_id>
cd runtime-apps
pnpm run dazi-app -- --version
```

从已装扩展一键同步到工作区（离线包）：

```powershell
.\scripts\sync-clis-from-extension.ps1
```

或手动把 `bundled/clis/*.js` 放入 `dazi-work/tools/dazi-clis/`。

> **注意**：侧栏能显示只说明扩展 UI 已加载；终端 CLI 还要能解析到 `bundled/clis/dazi.js`。  
> 若 `doctor-cli` 报「未找到」但 Trae 里已装扩展，多半是 **Trae 扩展在 `.trae/extensions`**，请更新 `scripts/dazi-cli-common.ps1` 后重跑 doctor。

## TRAE 配置建议

在 TRAE 规则或提示词中写明：

- **不要**使用 `dazi-onto`（独立命令不存在于 PATH）
- **不要**使用旧版 `dazi-agent` 发布 v3 本体脚本（除非显式走 legacy 模式）
- **使用**：`.\scripts\dazi.ps1 onto ...`

登录（一次性）：

```powershell
.\scripts\dazi.ps1 auth login
# 或设置 dazi.serverUrl 后
.\scripts\dazi.ps1 auth set-token <token>
```

详见：

- 扩展内置提示词：**帮助 → 提示词 →「本体脚本发布与运行（TRAE/智能体）」**（`onto/script-publish-run`，需 `dazi prompt sync`）
- 文档：`dazi/docs/327-本体项目创建与发布总结.md`
