# Dazi Runtime App Platform (DRAP) · Monorepo

**AI / 开发者入口**：[AGENTS.md](./AGENTS.md) · 快速入门：[docs/quickstart.md](./docs/quickstart.md) · 环境地址：[docs/env.md](./docs/env.md)

> **目录约定（v3.1+）**  
> - **搭子工作区（推荐）**：`项目/app_<名称>/` — 由扩展「新建应用项目」生成的完整 monorepo（本 README 描述的结构）。  
> - **开发仓**：`dazi/runtime-apps` — 与扩展 bundled 骨架同步的源码真源。  
> - **兼容（可选）**：工作区根 `<ws>/runtime-apps/`（与 `项目/app_*` 可并存；扩展侧栏会标注「默认应用项目」）。  
> 下文「应用项目根」「monorepo 根」均指**同时含 `sdk/` 与 `templates/` 的目录**。

## 结构

```
<应用项目根>/                    # 例：dazi-work/项目/app_应用001 或 dazi/runtime-apps
├── sdk/
│   ├── app-sdk-core/            # 协议 / 类型 / 错误码（零运行时）
│   ├── app-sdk-runtime/         # defineDaziApp / lifecycle / host 桥 / dev-shim
│   ├── app-sdk-data/            # useDataset / useSemanticQuery 等 hook
│   └── app-sdk-ui/              # KpiCard / TrendChart / DataGrid / FilterBar / PageLayout
├── templates/                   # 官方脚手架（app-template-*），init 从此拷贝
│   ├── catalog.json
│   └── app-template-*/
├── apps/                        # 业务应用（init / 扩展创建，勿与 templates 混放）
├── docs/                        # 开发指南（help 命令可读）
├── AGENTS.md
├── .cursor/rules/
└── cli/                         # 仅 bin/dazi-app.mjs 启动器 → bundled（无 src/dist）
```

> **v3 说明**：CLI 源码在 `dazi/dazi-vscode/cli/dazi-app`；本目录 `cli/` 仅保留 **启动器** `bin/dazi-app.mjs`，`pnpm run dazi-app` 转发至 `bundled/clis/dazi-app.js`。

## 快速开始（CLI）

在 **应用项目根目录**执行（不要在 `templates/` 子目录裸跑）：

```powershell
cd 项目/app_<名称>       # 搭子工作区示例；或 dazi/runtime-apps
pnpm install

# 版本（应输出 3.0.0）
pnpm run dazi-app -- --version

# 登录（推荐先用搭子扩展或 dazi auth login；亦可）
pnpm run dazi-app -- auth login --username <用户> --password <密码>
# 凭据：~/.dazi/auth.json（兼容 ~/.dazi-app/auth.json）

# 校验应用 manifest
pnpm run dazi-app -- manifest validate --cwd apps/<app_id> --scan-src

# 初始化应用
pnpm run dazi-app -- init production-command-center --space space__0519 --template app-template-production-command-center

# 发布流水线
pnpm run dazi-app -- build --cwd apps/<app_id>
pnpm run dazi-app -- package --cwd apps/<app_id>
pnpm run dazi-app -- upload --cwd apps/<app_id> --space <空间id> --activate --changelog "release"
```

### CLI 如何解析

`cli/bin/dazi-app.mjs` 按顺序查找可执行文件：

1. `DAZI_BUNDLED_DIR/dazi-app.js`
2. `../dazi-vscode/bundled/clis/dazi-app.js`（monorepo 内）
3. `../dazi/dazi-vscode/bundled/clis/dazi-app.js`（工作区应用项目内相对路径）

并自动设置 `DAZI_RUNTIME_APPS_ROOT` 为本目录（须含 `templates/` 与 `sdk/`）。

### 修改 CLI 后

```powershell
# 在 dazi-vscode 重打 bundled（扩展与工作区共用）
cd dazi/dazi-vscode
pnpm run bundle:clis
# 或于 runtime-apps 根：pnpm run bundle:clis
```

### 重打 bundled（CI / 发版前）

```powershell
cd dazi/dazi-vscode
pnpm run bundle:clis
pnpm run vsix
```

## CLI 子命令一览

`build` | `dev` | `package` | `upload` | `release` / `releases` list|activate|revoke | `auth` login|set-token | `whoami` | `init` | `templates` list|info | `manifest` validate|diff-template|merge-template | `asset` / `drap-assets` | `workspace` link | `preview` | `test` | `help` | `doctor` | `context` refresh

**帮助与自检**：

```powershell
pnpm run dazi-app -- help
pnpm run dazi-app -- help quickstart
pnpm run dazi-app -- doctor --cwd apps/<app_id>
```

**manifest 校验**：`pnpm run dazi-app -- manifest validate --cwd apps/<app_id> --scan-src`；`upload` 默认会先校验（可用 `--skip-validate` 跳过）。

**模板市场**：`pnpm run dazi-app -- templates list`（加 `--remote` 拉远端）；主站 `/admin/runtime-apps/templates`。

**内联数据源**：见 [docs/inline-data-source.md](./docs/inline-data-source.md)、[§317 DRAP Inline 联调](../docs/317-DRAP-Inline数据源联调与测试指南.md)。

## VS Code · 搭子 v3（推荐）

使用 **`dazi/dazi-vscode`** 一体化扩展（取代 `dazi-app-vscode`）：

- 侧栏 **App 应用**：应用项目 → 应用组件 → 数据源 / drap-assets；构建/发布/预览
- **新建项目** → 应用项目（新建 monorepo 或在已有项目下新建组件）
- 设置 `dazi.runtimeAppsRoot` 指向本目录（空则自动找 `项目/app_*` monorepo 或兼容的 `<工作区>/runtime-apps`）
- 扩展内 CLI 优先 `bundled/clis/dazi-app.js`，与终端 `pnpm run dazi-app` 同源

文档：搭子扩展内置 `docs/` 或仓库 `dazi/docs/` — §331 多项目架构、§333 本轮优化、§326 v3 总结

## 应用 / SDK 开发

```powershell
cd 项目/app_<名称>    # 应用项目根
pnpm install
pnpm dev:profit-analysis         # 模板 dev server (5180)
pnpm build:profit-analysis       # 模板 build → dist/
pnpm preview:profit-analysis     # vite preview → 5181
```

## P0 端到端验证（305 §15.1）

1. 三个终端：`pnpm dev:profit-analysis`（5180）、`pnpm preview:profit-analysis`（5181）、主站 `frontend` dev（3011）
2. 浏览器 `http://localhost:5180` 确认 mock dashboard
3. 主站 `http://localhost:3011/runtime-apps-test` 加载 5180/5181 子应用

详细协议参见 [305-Dazi-RuntimeAppPlatform方案](../docs/305-Dazi-RuntimeAppPlatform方案.md) §4 / §5 / §8。
