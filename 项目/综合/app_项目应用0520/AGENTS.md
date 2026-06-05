# DRAP runtime-apps · AI Agent 工作指南

> **读者**：Cursor / Codex / Claude Code 等 AI 助手，以及 DRAP 业务开发者。  
> 本文档与 `docs/` 目录为**自包含**分发包，不依赖 monorepo 外路径。

---

## 你是谁

你正在 **Dazi Runtime App Platform（DRAP）** 的**应用项目 monorepo** 中协助开发**子应用**（micro-app 制品）：模板在 `templates/`，业务应用在 `apps/`，CLI 在 `cli/`。  
本目录通常是搭子工作区下的 `项目/app_<名称>/`（扩展「新建应用项目」生成），或开发仓 `dazi/runtime-apps`。

---

## 铁律（不可违反）

1. **禁止裸 `fetch` / `axios`**：数据只走 `@dazi/app-sdk-data`（`useDataset` / `useResultDataset` 等）。
2. **改 manifest 后必须 `upload --activate`**：运行时读的是 Registry **DB `manifest_json`**，不是仅磁盘文件。
3. **`data_sources[].key` 与 `useDataset("key")` 必须一一对应**。
4. **manifest `kind` 使用 canonical 名**：`sql_template`、`script_entry`、`ontology_function`、`ontology_semantic`、`cube_query`、`static`、`sql_asset`、`script_asset`。
5. **视觉**：遵循 [docs/ui-style-guide.md](./docs/ui-style-guide.md)；`useAppearance()`，禁止硬编码深浅色。
6. **模板 `.ai/*` 仅为初始示例**：业务以 `apps/<id>/.ai/overview.md` 与 manifest 为准，可完全替换布局与数据源。

---

## 五步法（任何新应用）

```powershell
# 推荐：在 dazi-work 根（dazi 自动设置 bundled CLI）
cd D:\path\to\dazi-work

# 1. 脚手架（亦可用扩展「新建项目 / 新建应用组件」）
dazi app init <template_id> --space <spaceId> --dir 项目/app_<名>/apps/<app_id>

# 2. 改 manifest.data_sources（VS Code 绑定面板或手改 manifest.json）
dazi app manifest validate --cwd 项目/app_<名>/apps/<app_id> --scan-src

# 3. 本地 dev（在应用组件目录）
cd 项目\app_<名>\apps\<app_id>
pnpm run dev

# 4. 自检（回到 dazi-work 根）
cd D:\path\to\dazi-work
dazi app doctor --cwd 项目/app_<名>/apps/<app_id>

# 5. 发布
dazi app upload --cwd 项目/app_<名>/apps/<app_id> --space <spaceId> --activate
```

**备选**：在应用项目 monorepo 根使用 `pnpm run dazi-app -- …`（须配置 `DAZI_BUNDLED_DIR`，否则易报「未找到 bundled CLI」）。

主站验收地址见 [docs/env.md](./docs/env.md)。

---

## 目录约定

| 路径                            | 说明                                                                |
| ------------------------------- | ------------------------------------------------------------------- |
| `templates/app-template-*`      | 官方场景模板（勿与 `apps/` 混放）                                   |
| `apps/<app_id>/`                | 业务应用（`init` 生成）                                             |
| `apps/<app_id>/manifest.json`   | 数据源与权限声明                                                    |
| `apps/<app_id>/.ai/overview.md` | **通用**开发指引（所有应用相同结构）                                |
| `apps/<app_id>/.ai/`            | `CONTEXT.md`、`data-binding.md`、`page-intent.md`（模板示例，可改） |
| `apps/<app_id>/AGENTS.md`       | **本应用**专用 AI 指南                                              |
| `apps/<app_id>/drap-assets/`    | SQL / Python 资产                                                   |
| `sdk/app-sdk-*`                 | 子应用 SDK（源码直引）                                              |
| `docs/`                         | 人类可读开发指南                                                    |

---

## 文档索引

| 文档                                                           | 用途                                   |
| -------------------------------------------------------------- | -------------------------------------- |
| [docs/quickstart.md](./docs/quickstart.md)                     | 5 分钟开机                             |
| [docs/env.md](./docs/env.md)                                   | 开发/生产主站与 API 地址（唯一真值源） |
| [docs/develop-guide.md](./docs/develop-guide.md)               | 完整开发流                             |
| [docs/data-source-cookbook.md](./docs/data-source-cookbook.md) | 数据源 kind 与示例                     |
| [docs/inline-data-source.md](./docs/inline-data-source.md)     | sql_asset / script_asset               |
| [docs/ui-style-guide.md](./docs/ui-style-guide.md)             | 子应用 UI 规范                         |
| [docs/faq.md](./docs/faq.md)                                   | 常见报错                               |

---

## CLI 速查

```powershell
# dazi-work 根
dazi app help [quickstart|manifest|data-source|upload|doctor]
dazi app doctor --cwd 项目/app_<名>/apps/<app_id>
dazi app manifest validate --cwd 项目/app_<名>/apps/<app_id> --scan-src
dazi app templates list --remote
dazi app context refresh --cwd 项目/app_<名>/apps/<app_id>
```

---

## 给 AI 的修改检查清单

- [ ] 每个 `useDataset("x")` 在 `manifest.data_sources` 中有 `key: "x"`
- [ ] Chat 组件用 `useResultDataset`；问数主数据来自宿主 `message`
- [ ] `permissions` 含 `dataspace:<spaceId>` 及所用 ontology/cube 声明
- [ ] 改 manifest 后提醒用户 **upload --activate**
- [ ] 不将模板示例（如「三块 KPI」）当作不可变更的硬约束
- [ ] 不删除、不扩大 scope 修改无关文件
