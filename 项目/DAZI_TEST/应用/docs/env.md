# 部署环境与访问地址

> **唯一地址表**：其他文档只引用本文，勿在各处硬编码 localhost 或 IP。

---

## 开发环境（仅本地联调）

| 服务 | 地址 | 说明 |
|------|------|------|
| 后端 API | `http://localhost:8001` | uvicorn，与 `dazi-app auth login` 一致 |
| 主站（Vite dev） | `http://localhost:3011` | 前后端分离开发时使用 |

子应用运行时入口：`http://localhost:3011/runtime-apps/<app_id>`

---

## 测试 / 生产环境

| 环境 | 主站地址 | 说明 |
|------|----------|------|
| 测试 | `http://139.186.77.254:9010` | 前后端一体部署；主站静态资源由 backend 提供 |
| 生产 | `http://139.186.77.254:9010` | 与测试同机示例；实际以运维配置为准 |

子应用运行时入口：`<主站地址>/runtime-apps/<app_id>`

例如：`http://139.186.77.254:9010/runtime-apps/my-profit`

---

## VS Code / CLI 配置（搭子 v3）

| 配置项 | 用途 |
|--------|------|
| `dazi.serverUrl` | 平台根地址（无 `/api` 后缀）；开发 `http://127.0.0.1:8001` 或生产 `http://139.186.77.254:9010` |
| `dazi.runtimeAppsRoot` | 应用项目 monorepo 根（含 `sdk/`、`templates/`） |
| `~/.dazi/auth.json` | 登录凭据；`serverUrl` 与发布/upload 应对齐 |

修改后重载窗口或重新登录。勿仅改磁盘 manifest 而不 **upload --activate**。

---

## 平台维护者（monorepo 内，可选）

若需单独起后端与主站前端（非一体部署），在 monorepo 根目录：

```powershell
# 终端 1：后端
cd dazi\backend
# 按项目惯用方式启动 uvicorn

# 终端 2：主站前端
cd dazi\frontend
pnpm run dev
```

业务开发者打开 **搭子工作区**（含 `项目/app_*`），在应用项目根执行 CLI，并以上表主站地址验收 `/runtime-apps/<app_id>`。
