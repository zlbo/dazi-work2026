# 快速开始

**文档 ID**: `guides/quickstart`  
**适用版本**: dazi-vscode v3.0+

> CLI 调用约定见 **[CLI 调用约定](./cli-invocation.md)**。生产环境在 `dazi-work` 根目录使用 `dazi`。

## 5 分钟完成首次配置

### 1. 安装扩展

在 VS Code / Cursor 中安装 **搭子** 扩展，或通过 `.vsix`：

```powershell
code --install-extension dazi-vscode-3.x.x.vsix
```

### 2. 打开工作区

将 **`dazi-work`** 文件夹作为 VS Code 工作区根目录打开（含 `项目/`、`资源/`、`scripts/`）。

业务项目位于 **`项目/<业务名>/`**，内含固定子目录 `本体/`、`流程/`、`应用/`。  
本体开发入口为 **`项目/<业务名>/本体/ontos/<实现名>/`**（含 `plans/`、`setup/`、`functions/`；`space_id` 写在 `README.md`）。  
应用组件位于 **`项目/<业务名>/应用/apps/<app_id>/`**（见 [§331](../../docs/331-应用项目多项目与组件重构.md)）。

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
dazi auth login
# 或直接绑定 Token
dazi auth set-token --token "your-jwt-token"
```

### 6. 初始化工作区

**推荐（v3 业务项目 + per-item 本体）**：

1. 命令面板执行 **搭子: 新建业务项目**，创建 `项目/<业务名>/`
2. 命令面板执行 **搭子: 新建本体实现**，在 `本体/ontos/<实现名>/` 下生成 `plans/`、`setup/`、`functions/` 及 `快速启动_<实现名>.md`
3. 在 `ontos/<实现名>/README.md` 中确认或填写数据空间 ID

**兼容（历史 CLI 布局，非日常开发入口）**：

```powershell
dazi onto space init --space-id <your-space-id>
```

已有 v2 项目迁移：

```powershell
dazi migrate workspace
```

### 7. 验证环境

```powershell
dazi doctor
dazi env
dazi auth whoami
```

侧栏「搭子」图标应显示 6 个节点：帮助、数据资源、本体、流程、应用、工作区。

## 下一步

- [CLI 调用约定](./cli-invocation.md)
- [认证管理](../auth/auth-login.md)
- [本体开发入门](../onto/space-management.md)
- [工作区 v3 规范](./workspace-v3.md) — 业务项目目录树与 per-item 本体结构
- [数据流程项目开发](../flow/flow-project-guide.md) — **推荐**：`项目/<业务名>/流程/flows/`、菜单、pull/push
- [节点代码编写](../flow/node-code-guide.md) — python-script、sql-query 等
- [流程开发索引](../flow/flows-guide.md) — Flow 文档入口
