# 快速开始

**文档 ID**: `guides/quickstart`  
**适用版本**: dazi-vscode v3.0+

> CLI 调用约定见 **[CLI 调用约定](./cli-invocation.md)**。生产环境在 `dazi-work` 根目录使用 `.\scripts\dazi.ps1`。

## 5 分钟完成首次配置

### 1. 安装扩展

在 VS Code / Cursor 中安装 **搭子** 扩展，或通过 `.vsix`：

```powershell
code --install-extension dazi-vscode-3.x.x.vsix
```

### 2. 打开工作区

将 **`dazi-work`** 文件夹作为 VS Code 工作区根目录打开（含 `项目/`、`资源/`、`scripts/`）。  
DRAP 应用项目位于 **`项目/app_<名称>/`**（完整 monorepo，见 [§331](../../docs/331-应用项目多项目与组件重构.md)）；不再要求根目录必须有 `runtime-apps/`。

### 3. 自检 CLI

```powershell
cd D:\path\to\dazi-work
.\scripts\doctor-cli.ps1
```

应解析到已安装扩展内的 `bundled/clis/dazi.js`（无需 monorepo 源码）。

### 4. 配置服务地址

在 VS Code 设置中搜索 `dazi.serverUrl`，填入搭子平台地址：

```
https://your-dazi-server.example.com
```

### 5. 登录

在命令面板（`Ctrl+Shift+P`）搜索 **搭子: 登录**，或终端：

```powershell
.\scripts\dazi.ps1 auth login
# 或直接绑定 Token
.\scripts\dazi.ps1 auth set-token --token "your-jwt-token"
```

### 6. 初始化工作区

```powershell
# 新项目（本体空间）
.\scripts\dazi.ps1 onto space init --space-id <your-space-id>

# 已有 v2 项目迁移
.\scripts\dazi.ps1 migrate workspace
```

### 7. 验证环境

```powershell
.\scripts\dazi.ps1 doctor
.\scripts\dazi.ps1 env
.\scripts\dazi.ps1 auth whoami
```

侧栏「搭子」图标应显示 6 个节点：帮助、数据资源、本体、流程、应用、工作区。

## 下一步

- [CLI 调用约定](./cli-invocation.md)
- [认证管理](../auth/auth-login.md)
- [本体开发入门](../onto/space-management.md)
- [数据流程项目开发](../flow/flow-project-guide.md) — **推荐**：`项目/flow_*`、菜单、pull/push
- [节点代码编写](../flow/node-code-guide.md) — python-script、sql-query 等
- [流程开发索引](../flow/flows-guide.md) — Flow 文档入口
