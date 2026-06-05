# DRAP 常见问题（FAQ）

---

## 环境与命令

### Q：`dazi-app` 找不到或命令无效？

在**应用项目根目录**（须含 `sdk/`、`templates/`；如 `项目/app_<名称>/` 或 `dazi/runtime-apps`）：

```powershell
pnpm install
pnpm run dazi-app -- --version    # 期望 3.0.0
pnpm run dazi-app -- whoami
```

CLI 由启动器解析 **`dazi-vscode/bundled/clis/dazi-app.js`**，日常**不必** `pnpm run cli:build`。若仍失败：

1. 在 `dazi/dazi-vscode` 执行：`pnpm run bundle:clis`
2. 确认搭子扩展已安装，且存在 `dazi-vscode/bundled/clis/dazi-app.js`（CLI 启动器会解析；相对路径因 monorepo 位置而异）
3. 改 CLI 源码：编辑 `dazi/dazi-vscode/cli/dazi-app`，再 `pnpm run bundle:clis`

勿在 `templates/` 子目录裸跑；在应用目录用 `pnpm -C ../.. run dazi-app -- <子命令> --cwd .`。

### Q：`upload` 找错 manifest 目录？

使用 `--cwd` 或在应用目录执行（利用 `INIT_CWD`）：

```powershell
cd apps\my-app
pnpm -C ..\.. run dazi-app -- upload --space space__0519 --activate
```

### Q：`--space` 填什么？

须为库里真实 `ads_dataspaces.id`，如 `space__0519`，勿用虚构 `space__demo`。

---

## 数据与 manifest

### Q：改了 manifest 线上不变？

运行时读 **DB 激活版本的 `manifest_json`**。须：

```powershell
pnpm run dazi-app -- upload --activate
```

或管理端「构建并上传激活」。

### Q：`fetch-data-sources` 报 `kind not allowed`？

空间 policy 未开启对应 kind：

```powershell
cd dazi\backend
python scripts/seed_runtime_app_policies.py space__0519
```

### Q：`sql_template` 报查询不存在？

`template_id` 须与空间「已保存查询」的 id 一致；管理端空间资产面板可复制片段。

### Q：页模式有数据，问数无数据？

问数主区走宿主 `message` 注入，检查：

- manifest `mount.type` 是否为 `chat_result`
- 管理端是否配置聊天绑定（`chat_bindings`）
- 组件是否使用 `useResultDataset()` 而非页模式的 `useDataset`
- Network：`chat-resolve` / `fetch-data-sources` 是否 200 且 `meta.ok`

### Q：`manifest validate` 报 SRC_KEY_UNDECLARED？

源码 `useDataset("foo")` 但 manifest 未声明 `key: "foo"`，补 `data_sources` 或改代码。

---

## 构建与加载

### Q：主站 `/runtime-apps/<appId>` 灰屏或 404 JS？

- 确认已 `upload --activate`
- Network 应请求 `/runtime-apps/<appId>/<semver>/index.html`，而非主站 hash 路由的 `/assets/`
- 改模板/SDK 后须 **重新 build + upload**
- 确认 release 已激活；浏览器 Network 请求路径为 `/runtime-apps/<appId>/<semver>/index.html`
- 勿用主站 hash 路由下的 `/assets/` 加载子应用 JS

### Q：KPI 为 0 或假数据？

开发环境可能对 `profit-analysis` 有 fixture 兜底；生产 ontology 失败会空白。检查 `fetch-data-sources` 的 `meta.ok` 与 `meta.error`。

---

## AI 与文档

### Q：Cursor 不知道 DRAP 约束？

- 打开 `runtime-apps/AGENTS.md` 或应用 `apps/<id>/AGENTS.md`
- 应用内先读 `.ai/overview.md`（通用）再读模板示例 `.ai/page-intent.md`
- 工作区规则：`runtime-apps/.cursor/rules/drap-runtime-apps.mdc`

### Q：如何刷新空间上下文？

```powershell
pnpm run dazi-app -- context refresh --cwd apps/<app_id>
```

同时会更新 `AGENTS.md` 中的空间摘要（若已生成）。

### Q：`doctor` 做什么？

```powershell
pnpm run dazi-app -- doctor --cwd apps/<app_id>
```

检查：登录态、manifest 校验、`.ai/` 文件、`drap-assets` 与 manifest 引用一致性。

---

## VS Code 插件

### Q：片段库为空？

添加 `runtime-apps/space-snippets/<spaceId>.json` 种子，或管理端维护。

### Q：绑定数据源后线上仍旧数据？

VS Code 只写**本地** manifest；须再执行 **构建并上传激活**。

---

## 获取更多帮助

```powershell
pnpm run dazi-app -- help quickstart
pnpm run dazi-app -- help data-source
pnpm run dazi-app -- doctor
```

文档：[quickstart.md](./quickstart.md) · [data-source-cookbook.md](./data-source-cookbook.md) · [inline-data-source.md](./inline-data-source.md) · [env.md](./env.md)
