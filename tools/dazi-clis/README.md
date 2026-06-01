# 离线 CLI（生产交付）

本目录存放 v3 bundled CLI 的 4 个单文件（与扩展内 `bundled/clis` 相同）：

- `dazi.js`、`dazi-onto.js`、`dazi-flow.js`、`dazi-app.js`

`dazi-work/scripts/dazi.ps1` **优先**使用此目录，因此终端 CLI **不依赖** Trae/Cursor 是否已扫描到扩展路径。

## 发版时更新

在搭子源码仓库执行：

```powershell
cd dazi\dazi-vscode
pnpm run bundle:clis
Copy-Item bundled\clis\*.js ..\..\dazi-work\tools\dazi-clis\ -Force
```

或在工作区根：

```powershell
.\dazi-work\scripts\sync-clis-from-extension.ps1
```

## 验证

```powershell
cd dazi-work
.\scripts\dazi.ps1 --version
.\scripts\doctor-cli.ps1
```
