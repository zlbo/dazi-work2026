# DRAP 快速入门（5 分钟）

> 搭子工作区推荐目录：`dazi-work/项目/app_<名称>/`（扩展 **新建项目 → 应用项目**）。  
> **主站 / API 地址**见 [env.md](./env.md)。  
> **CLI 推荐**：在 **`dazi-work` 根**执行 `.\scripts\dazi.ps1 app …`（自动 bundled，最稳）。

---

## 1. 准备

```powershell
cd D:\path\to\dazi-work
.\scripts\doctor-cli.ps1
.\scripts\dazi.ps1 auth login
.\scripts\dazi.ps1 auth whoami
```

在**应用项目根**安装依赖（含 `sdk/`、`templates/`）：

```powershell
cd 项目\app_<名称>
pnpm install
```

---

## 2. 从模板创建应用

也可用扩展：**新建项目 → 应用项目**，或 **App: 新建应用组件…**（`dazi.app.component.new`）。

```powershell
cd D:\path\to\dazi-work

.\scripts\dazi.ps1 app init profit-analysis-dashboard `
  --space space__0519 `
  --dir 项目/app_<名>/apps/my-profit `
  --name "我的利润分析"
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
cd 项目\app_<名>\apps\my-profit
pnpm run dev
```

---

## 4. 校验与自检

在 **dazi-work 根**：

```powershell
.\scripts\dazi.ps1 app manifest validate --cwd 项目/app_<名>/apps/my-profit --scan-src
.\scripts\dazi.ps1 app doctor --cwd 项目/app_<名>/apps/my-profit
```

若 manifest 使用 `sql_asset` / `script_asset`，可先本地预览（须已登录）：

```powershell
.\scripts\dazi.ps1 app preview sql kpi --cwd 项目/app_<名>/apps/my-profit
.\scripts\dazi.ps1 app test --key kpi --cwd 项目/app_<名>/apps/my-profit
```

---

## 5. 发布到 Registry

```powershell
cd 项目\app_<名>\apps\my-profit
pnpm run build

cd D:\path\to\dazi-work
.\scripts\dazi.ps1 app upload --cwd 项目/app_<名>/apps/my-profit --space space__0519 --activate --changelog "初版"
```

浏览器验收（须登录主站，地址见 [env.md](./env.md)）：

`<主站地址>/runtime-apps/<app_id>`

---

## 相关文档

| 文档 | 说明 |
|------|------|
| [develop-guide.md](./develop-guide.md) | 完整开发流 |
| [data-source-cookbook.md](./data-source-cookbook.md) | 数据源 kind |
| [faq.md](./faq.md) | 常见报错 |
| `../AGENTS.md` | AI 工作指南 |

扩展内：`资源/docs/app/`（先 `dazi docs sync`）。
