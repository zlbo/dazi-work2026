# DRAP 开发指南

> 面向在 `apps/<app_id>/` 中维护业务子应用的开发者。应用项目位于搭子工作区 `项目/app_<名称>/`（推荐）或开发仓 `dazi/runtime-apps`。

---

## 1. Monorepo 结构

```text
<应用项目根>/              # 例：dazi-work/项目/app_应用001
├── sdk/                   # @dazi/app-sdk-*（子应用依赖，源码直引）
├── templates/             # app-template-*（init 拷贝源）
├── apps/                  # 业务应用（勿放模板）
├── cli/                   # dazi-app 启动器 → bundled/clis/dazi-app.js
├── docs/                  # 本目录
├── space-snippets/        # 空间推荐 data_sources 片段种子
└── AGENTS.md              # AI 助手入口
```

**原则**：模板在 `templates/`，应用在 `apps/`；**推荐**在 **`dazi-work` 根**执行 `.\scripts\dazi.ps1 app <子命令> --cwd 项目/app_<名>/apps/<app_id>`（自动 bundled CLI）。备选：在 monorepo 根 `pnpm run dazi-app`（须 `DAZI_BUNDLED_DIR`）。

CLI 源码真源：`dazi/dazi-vscode/cli/dazi-app`（见 [../../dazi-vscode/cli/dazi-app/README.md](../../dazi-vscode/cli/dazi-app/README.md)）。

---

## 2. 应用目录标准布局

```text
apps/<app_id>/
├── manifest.json           # 权威声明（upload 后进 DB）
├── manifest.ontology.json  # 可选 profile 档
├── manifest.chat-result.json
├── manifest.sql-script.json
├── src/                    # React 页面
├── drap-assets/            # SQL / Python 资产（Phase E）
│   ├── sql/
│   ├── python/
│   ├── tests/
│   └── README.md
├── .ai/
│   ├── overview.md         # 通用开发指引（init 生成，所有应用）
│   ├── CONTEXT.md          # 空间元数据（context refresh）
│   ├── data-binding.md     # key ↔ 组件（模板示例，可改）
│   ├── page-intent.md      # 场景示例 + 业务目标待填
│   └── component-rules.md  # 布局示例 + SDK 约束
├── AGENTS.md               # 应用级 AI 指南
├── package.json
└── vite.config.ts
```

---

## 3. manifest 要点

| 字段 | 说明 |
|------|------|
| `appId` | 全局唯一，与 Registry 一致 |
| `permissions[]` | 至少 `dataspace:<spaceId>` |
| `data_sources[]` | 数据集 key + kind + 参数 |
| `mount.type` | `page` 或 `chat_result`（布局提示，不互斥） |
| `sdk.contract` | 固定 `drap-1` |

**运行时**：`DaziAppRegistryHost` → `POST .../fetch-data-sources` → `useDataset(key)`。

---

## 4. 开发循环

```text
改 src / manifest
  → manifest validate --cwd <app> --scan-src
  → pnpm run dev（布局）
  → doctor --cwd <app>（自检）
  → pnpm run build
  → upload --cwd <app> --activate
  → 主站 `<主站地址>/runtime-apps/<appId>` 验收（见 env.md）
```

### 4.1 init 与 profile

在 **dazi-work 根**（推荐）：

```powershell
.\scripts\dazi.ps1 app init production-command-center `
  --space space__0519 `
  --dir 项目/app_<名>/apps/my-pcc `
  --name "我的生产指挥中心" `
  --profile static          # 默认；可选 ontology | chat-result | sql-script | sql-asset | script-asset
```

`template_id` 为目录短名（对应 `templates/app-template-production-command-center/`）。

### 4.2 空间上下文

```powershell
.\scripts\dazi.ps1 app context refresh --cwd 项目/app_<名>/apps/my-pcc
# 写入 .ai/CONTEXT.md，并刷新 AGENTS.md 摘要
```

### 4.3 与模板 manifest 对比

```powershell
.\scripts\dazi.ps1 app manifest diff-template production-command-center --cwd 项目/app_<名>/apps/my-pcc
.\scripts\dazi.ps1 app manifest merge-template production-command-center --cwd 项目/app_<名>/apps/my-pcc --profile sql-script --write
```

### 4.4 校验与发布（dazi-work 根）

```powershell
.\scripts\dazi.ps1 app manifest validate --cwd 项目/app_<名>/apps/my-pcc --scan-src
.\scripts\dazi.ps1 app upload --cwd 项目/app_<名>/apps/my-pcc --space space__0519 --activate
```

---

## 5. 数据源选型

| 场景 | 推荐 kind |
|------|-----------|
| 模板演示 / 离线布局 | `static` |
| 生产明细 / 自定义 SQL（空间已保存查询） | `sql_template` |
| 复杂计算（空间已发布脚本） | `script_entry` |
| 标准 KPI / 问数脊骨 | `ontology_function` / `ontology_semantic` |
| Cube 报表 | `cube_query` |
| 单应用专属、随 zip 迁移（Phase E） | `sql_asset` / `script_asset` + `drap-assets/` |

详见 [data-source-cookbook.md](./data-source-cookbook.md) 与 [inline-data-source.md](./inline-data-source.md)。

---

## 6. VS Code · 搭子 v3（dazi-vscode）

使用 **`dazi/dazi-vscode`** 一体化扩展（**取代** `dazi-app-vscode`）：

- 侧栏 **App 应用**：**应用项目** → **应用组件** → 数据源 / drap-assets
- **新建项目** → 应用项目（monorepo）/ 在已有项目下新建组件
- **配置 manifest 数据源**（`dazi.app.editDataSources`）/ **构建并发布**
- **刷新 AI 上下文**（等价 `context refresh`）
- CLI 与终端 `pnpm run dazi-app` **同源**（bundled `dazi-app.js`）

配置（扩展）：

| 设置 | 说明 |
|------|------|
| `dazi.runtimeAppsRoot` | 应用项目根（含 `templates/`、`sdk/`）；空则扫描 `项目/app_*` 或兼容 `<工作区>/runtime-apps` |
| `dazi.serverUrl` | 平台 API 根（无 `/api` 后缀）；与 `~/.dazi/auth.json` 的 `serverUrl` 应对齐 |
| `dazi.spaceId` | 当前数据空间 |

鉴权：`dazi auth login` 或侧栏登录 → `~/.dazi/auth.json`。发布前在发布面板确认 **发布目标 API**。

扩展文档见搭子 `docs/`：§331 多项目、§333 本轮优化、§326 v3 总结。

---

## 7. 问数场景（chat_result）

- 主数据由宿主注入 `datasets.message`，用 `useResultDataset()`
- 页模式预览：manifest 内 static 回退
- 绑定：`/admin/runtime-apps` → 聊天绑定，或 `chat_bindings` API

---

## 8. 生产入口与构建

- **开发**：`src/dev-entry.tsx`（仅 `pnpm dev`）
- **生产**：`src/prod-entry.tsx` + `index.prod.html` → build 后 `dist/index.html`
- 改 SDK/模板后须 **重新 build + upload**

---

## 9. 文档索引（runtime-apps 内）

| 文档 | 内容 |
|------|------|
| [quickstart.md](./quickstart.md) | 5 分钟开机 |
| [env.md](./env.md) | 开发/生产主站与 API 地址 |
| [data-source-cookbook.md](./data-source-cookbook.md) | 数据源 kind |
| [inline-data-source.md](./inline-data-source.md) | sql_asset / script_asset |
| [ui-style-guide.md](./ui-style-guide.md) | 子应用 UI 规范 |
| [faq.md](./faq.md) | 常见报错 |
| [../README.md](../README.md) | monorepo、bundled CLI |
| [AGENTS.md](../AGENTS.md) | AI 助手入口 |
