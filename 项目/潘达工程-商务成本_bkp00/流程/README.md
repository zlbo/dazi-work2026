<!-- dazi-flow-scaffold -->
# 流程

本目录为业务项目 **`潘达工程-商务成本`** 的数据流程工作区。

## 1. 目录结构

| 路径 | 说明 |
|------|------|
| `plans/` | 流程设计文档（数据源、拓扑草案等） |
| `flows/` | 各流程实例目录（`flow.json`、`节点/`、`变量/`） |

单个流程位于 `flows/<流程名>/`：

| 路径 | 说明 |
|------|------|
| `flow.json` | 画布真理源（节点配置 + 连线，代码已剥离） |
| `flow.meta.json` | flowId、node_uuid 映射（CLI 维护，勿手改） |
| `节点/<名>/code.*` | SQL / Python 节点代码 |
| `变量/<名>.json` | 调试 Run 变量预览（只读，pull/sync 生成） |
| `_run/` | 测试/运行产物（`*.last-error.md` 等） |

> 流程**不绑定数据空间**；`connectionId` 仅为数据库节点的配置字段。

## 2. 新建 / 拉取流程

资源管理器（推荐 **表单**）：

| 操作 | 菜单 |
|------|------|
| 新建流程 | 右键 **`流程/flows/`**（或其子目录）→ **新建流程** |
| 拉取平台流程 | 右键 **`流程/flows/`**（或其子目录）→ **拉取平台流程** |

拉取表单可从平台 Flow 列表选择，或手动填写 Flow ID；新建表单填写名称与说明后自动创建并拉取。

> **禁止**在 `dazi-work` 工作区根对流程命令使用 `--dir .`；`--dir` 须指向 `flows/<流程名>/`（推荐绝对路径）。

命令行（`--dir` 使用绝对路径或相对 `dazi-work` 根）：

```powershell
dazi flow project pull --flow <flowId> --dir "D:\path\to\dazi-work\项目\潘达工程-商务成本\流程\flows\<流程名>"
```

拉取后每个流程目录会生成 **`快速启动_<流程名>.md`**（含 flowId 与本流程常用命令，便于 @ 附加给 AI）。

## 3. 开发与提交

1. 编辑 `节点/<名>/code.sql` 或 `code.py`
2. 右键 **提交节点** 或 `flow node push`（**先于测试**；`node-exec` 跑平台已 push 的代码）
3. 右键 **测试运行节点** / 设计器 **搭子执行**，或 `flow run node-exec --node <uuid>`
4. 查看表变量：设计器 **output_variable_name** 旁 📊，或 `flow variable pull --name <名>`（有输出变量时建议必做）
5. 改连线/配置：右键 **提交流程** 或 `flow project push --canvas`

命令前缀：`dazi flow`（全局 CLI；`--dir` 指向 **流程目录绝对路径**；未装全局时可用 `.scriptsdazi.ps1 flow`）

## 4. 推荐开发循环

详见 [数据流程项目开发指南](../../资源/docs/flow/flow-project-guide.md) §4。

## 5. AI 提示词推荐

| 场景 | 提示词 ID |
|------|-----------|
| 设计/新增流程 | `flow/flow-design` |
| **运行失败、自主改错** | **`flow/run-fix-loop`**（⭐ 首选） |
| 分析用户粘贴的错误 | `flow/run-debug` |

侧栏 **帮助 → 🤖 提示词** 中 ⭐ 为流程推荐。右键 **`flow.json`** → **打开 AI 改错提示词**。
给 AI 的任务示例：「改 XX 节点，**先 node push 再测**，失败按 last-error 改到满足成功判据（含 variable pull）」。

## 帮助文档

工作区文档位于 **`资源/docs/`**（扩展侧栏 **帮助 → 下载所有文档**，或在工作区根执行 `dazi docs sync`）：

| 文档 | 链接 |
|------|------|
| Flow 文档索引（从这里开始） | [flows-guide.md](../../资源/docs/flow/flows-guide.md) |
| 数据流程项目开发指南 | [flow-project-guide.md](../../资源/docs/flow/flow-project-guide.md) |
| 流程变量系统指南 | [variables-guide.md](../../资源/docs/flow/variables-guide.md) |
| 节点代码编写指南（含 SQL/Python 示例） | [node-code-guide.md](../../资源/docs/flow/node-code-guide.md) |
| Flow 运行与测试 | [run-guide.md](../../资源/docs/flow/run-guide.md) |
| 数据源与 connectionId | [source-guide.md](../../资源/docs/flow/source-guide.md) |
| **流程本地文件规范（AI 必读）** | [local-files-spec.md](../../资源/docs/flow/local-files-spec.md) |
| 流程 AI 工作手册 | [ai-workflow-playbook.md](../../资源/docs/flow/ai-workflow-playbook.md) |
| CLI 调用约定（`dazi` / `dazi.ps1`） | [cli-invocation.md](../../资源/docs/guides/cli-invocation.md) |

终端打开文档（**dazi-work 根**或已 `cd` 到流程目录）：

```powershell
dazi docs open flow/flow-project-guide
dazi docs open flow/variables-guide
dazi docs open flow/node-code-guide
dazi docs open flow/flows-guide
```

**代码示例**：变量读写、`python-script` / `sql-query` 模板见 [节点代码编写指南](../../资源/docs/flow/node-code-guide.md) 与 [流程变量系统指南](../../资源/docs/flow/variables-guide.md)。
