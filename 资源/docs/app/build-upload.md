# 应用构建与上传

**文档 ID**: `app/build-upload`  
**适用**：搭子 v3 · DRAP 应用项目位于 `项目/app_<名称>/apps/<app_id>/`

## 工作目录

| 操作                                     | 目录                                                                                                     |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `dazi app …`（init、upload、release 等） | **`dazi-work` 根**；路径用 `--cwd 项目/app_<名>/apps/<app_id>`（相对工作区根）                           |
| `pnpm run dazi-app`（可选）              | **应用项目根**（含 `sdk/`、`templates/`）；需正确设置 `DAZI_BUNDLED_DIR`，否则易报「未找到 bundled CLI」 |
| `pnpm run dev` / `build`                 | **应用组件目录** `apps/<app_id>/`                                                                        |
| 扩展「构建并发布」                       | 在侧栏选中**应用组件**节点，无需手填路径                                                                 |

发布前确认扩展登录与 **发布目标 API**（`dazi.serverUrl` / `~/.dazi/auth.json`）一致。

## 开发

在 `apps/<app_id>/`：

```bash
pnpm run dev
# 或（在 dazi-work 根）：dazi app dev --cwd 项目/app_<名>/apps/<app_id>
```

## 构建

```bash
pnpm run build
```

输出到 `dist/`（由 `dazi.app.buildOutputDir` 配置）。

## 上传

在 **`dazi-work` 根**执行（`--cwd` 为相对工作区根的应用组件目录）：

```powershell
cd D:\path\to\dazi-work

# 上传到指定空间
dazi app upload --cwd 项目/app_<名>/apps/<app_id> --space <space-id>

# 上传并立即激活
dazi app upload --cwd 项目/app_<名>/apps/<app_id> --space <space-id> --activate

# 带更新日志
dazi app upload --cwd 项目/app_<名>/apps/<app_id> --space <space-id> --changelog "修复了 #123 问题"
```

等价写法（须在应用项目根且已配置 `DAZI_BUNDLED_DIR`）：`pnpm run dazi-app -- upload --cwd apps/<app_id> --space <space-id>`。

浏览器验收：`<主站>/runtime-apps/<app_id>`（地址见应用项目内 `docs/env.md` 或扩展设置 `dazi.serverUrl`）。

## 本地预览（上传前）

```powershell
dazi app preview all --cwd 项目/app_<名>/apps/<app_id>
dazi app preview sql --cwd 项目/app_<名>/apps/<app_id>
dazi app preview script --cwd 项目/app_<名>/apps/<app_id>
```

## 相关文档

- [app-init](./app-init.md)
- [release-guide](./release-guide.md)
- [§331 多项目架构](../../docs/331-应用项目多项目与组件重构.md)

## 收尾与发版检查

在扩展仓 `dazi-vscode` 根目录执行：

```bash
pnpm run build
```

该命令会执行 `copy:bundled`，并在复制 `runtime-apps` 骨架后自动修正文档路径（模板 README/FAQ），确保新建应用项目拿到的是最新说明。
