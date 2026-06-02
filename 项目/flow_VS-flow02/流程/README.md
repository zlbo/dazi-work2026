<!-- dazi-flow-scaffold -->
# 流程

每个子目录是一个流程（含 `flow.json`、`flow.meta.json`）。

## 操作

| 操作 | 方式 |
|------|------|
| 新建流程 | 右键本目录 → **新建流程**（表单：名称、说明、路径预览） |
| 拉取平台流程 | 右键 → **拉取平台流程**（表单：平台列表 / Flow ID、本地目录名） |
| 打开设计器 | 右键 `flow.json` → **打开流程设计器** |

```powershell
# 命令行拉取（dazi-work 根）
.\scripts\dazi.ps1 flow project pull --flow <id> --dir "项目\flow_VS-flow02\流程\<流程名>"
```

拉取完成后请阅读各流程子目录下的 **`快速启动_<流程名>.md`**。

## 帮助文档

工作区文档位于 **`资源/docs/`**（扩展侧栏 **帮助 → 下载所有文档**，或在工作区根执行 `dazi docs sync`）：

| 文档 | 链接 |
|------|------|
| Flow 文档索引（从这里开始） | [flows-guide.md](../../../资源/docs/flow/flows-guide.md) |
| 数据流程项目开发指南 | [flow-project-guide.md](../../../资源/docs/flow/flow-project-guide.md) |
| 流程变量系统指南 | [variables-guide.md](../../../资源/docs/flow/variables-guide.md) |
| 节点代码编写指南（含 SQL/Python 示例） | [node-code-guide.md](../../../资源/docs/flow/node-code-guide.md) |
| Flow 运行与测试 | [run-guide.md](../../../资源/docs/flow/run-guide.md) |
| 数据源与 connectionId | [source-guide.md](../../../资源/docs/flow/source-guide.md) |
| CLI 调用约定（`dazi.ps1`） | [cli-invocation.md](../../../资源/docs/guides/cli-invocation.md) |

终端打开文档（在 **dazi-work 根**）：

```powershell
.\scripts\dazi.ps1 docs open flow/flow-project-guide
.\scripts\dazi.ps1 docs open flow/variables-guide
.\scripts\dazi.ps1 docs open flow/node-code-guide
```

**代码示例**：变量读写、`python-script` / `sql-query` 模板见 [节点代码编写指南](../../../资源/docs/flow/node-code-guide.md) 与 [流程变量系统指南](../../../资源/docs/flow/variables-guide.md)。
