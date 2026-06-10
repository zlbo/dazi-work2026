# @dazi/dazi-app-cli（启动器）

本目录**不再包含** CLI 源码与 `dist/`。`pnpm run dazi-app` 通过 `bin/dazi-app.mjs` 调用：

**`dazi/dazi-vscode/bundled/clis/dazi-app.js`**

## 源码与构建

| 项目 | 路径 |
|------|------|
| TypeScript 源码 | `dazi/dazi-vscode/cli/dazi-app/src/` |
| 构建 | `cd dazi/dazi-vscode && pnpm run bundle:clis` |
| 文档 | [dazi-vscode/cli/dazi-app/README.md](../../dazi-vscode/cli/dazi-app/README.md) |

## 修改 CLI 后

```powershell
cd dazi\dazi-vscode
pnpm run bundle:clis
```

然后在 `runtime-apps` 根目录验证：

```powershell
pnpm run dazi-app -- --version
```
