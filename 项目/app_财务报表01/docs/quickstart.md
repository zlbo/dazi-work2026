# DRAP 快速入门（5 分钟）

> 在**应用项目根目录**执行下列命令（须含 `sdk/`、`templates/`、`apps/`）。  
> - 搭子工作区推荐：`项目/app_<名称>/`（扩展 **新建项目 → 应用项目**）  
> - 开发仓：`dazi/runtime-apps`  
> **主站 / API 地址**见 [env.md](./env.md)。CLI 由搭子 v3 **bundled** 提供，日常 **无需** `pnpm run cli:build`。

---

## 1. 准备应用项目

```powershell
cd 项目\app_<名称>        # 搭子工作区；或 cd dazi\runtime-apps
pnpm install
pnpm run dazi-app -- --version    # 应输出 3.0.0

# 登录（API 见 env.md；凭据 ~/.dazi/auth.json，兼容 ~/.dazi-app/auth.json）
pnpm run dazi-app -- auth login --username <用户> --password <密码>
# 或先在 VS Code 用「搭子 v3」扩展登录，再执行 whoami
pnpm run dazi-app -- whoami
```

若 `dazi-app` 不可用：确认已 `pnpm install`，且在 `dazi/dazi-vscode` 执行过 `pnpm run bundle:clis`（见 [../README.md](../README.md)）。

---

## 2. 从模板创建应用

也可用扩展：**新建项目 → 应用项目**（生成 monorepo + 首个组件），或 **在已有项目下新建组件**（`dazi.app.component.new`）。

```powershell
pnpm run dazi-app -- init profit-analysis-dashboard `
  --space space__0519 `
  --dir apps/my-profit `
  --name "我的利润分析"

cd apps\my-profit
```

`init` 会自动生成：

- `manifest.json`（默认 static 演示数据）
- `.ai/overview.md`（通用开发指引）
- `.ai/data-binding.md`、`page-intent.md`、`component-rules.md`（模板**初始示例**，可改）
- `AGENTS.md`（本应用 AI 上下文）
- `drap-assets/README.md`（SQL/Python 资产说明）

---

## 3. 本地开发

```powershell
# 在应用目录
pnpm run dev
# 浏览器打开模板 dev 端口（如 5180），可看 mock / static 布局
```

---

## 4. 校验与自检

在**应用目录**执行（`--cwd .` 指向当前应用；亦可用 `INIT_CWD` 自动识别）：

```powershell
pnpm -C ..\.. run dazi-app -- manifest validate --cwd . --scan-src
pnpm -C ..\.. run dazi-app -- doctor --cwd .
```

若 manifest 使用 `sql_asset` / `script_asset`，可先本地预览（须已登录）：

```powershell
pnpm -C ..\.. run dazi-app -- preview sql kpi --cwd .
pnpm -C ..\.. run dazi-app -- test --cwd .
```

---

## 5. 发布到 Registry

```powershell
pnpm run build
pnpm -C ..\.. run dazi-app -- upload --cwd . --space space__0519 --activate --changelog "初版"
```

浏览器验收（须登录主站，地址见 [env.md](./env.md)）：

`<主站地址>/runtime-apps/<app_id>`

---

## 6. 绑定真实数据（可选）

| 目标 | 做法 |
|------|------|
| 空间已保存查询 | manifest 改 `sql_template` + `template_id`；或 VS Code「配置 manifest 数据源」 |
| 已发布脚本 | manifest 改 `script_entry` + `script_id` |
| 应用内联 SQL/Python | `sql_asset` / `script_asset` + `drap-assets/`（推荐，见 [inline-data-source.md](./inline-data-source.md)） |
| 本体函数 | 使用 `manifest.ontology.json` 档或手改 `ontology_function` |

详见 [data-source-cookbook.md](./data-source-cookbook.md)。

---

## 下一步

- 完整流程：[develop-guide.md](./develop-guide.md)
- 常见报错：[faq.md](./faq.md)
- 界面规范：[ui-style-guide.md](./ui-style-guide.md)
- **VS Code**：`dazi/dazi-vscode`（搭子 v3，侧栏 App 应用；取代 `dazi-app-vscode`）
