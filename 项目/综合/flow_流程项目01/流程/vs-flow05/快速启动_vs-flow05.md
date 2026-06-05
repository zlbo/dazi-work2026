<!-- dazi-flow-scaffold -->

# 快速启动

**流程**：vs-flow05 · 平台 flowId `115`

## 流程信息

| 字段     | 值                       |
| -------- | ------------------------ |
| flowId   | `115`                    |
| 本地目录 | `流程/vs-flow05/`        |
| 节点数   | 2（代码节点 0）          |
| 上次拉取 | 2026-06-03T02:46:01.303Z |

## 常用命令

在 **dazi-work 根**（或将 `--dir` 指向本目录）：

```powershell
cd "项目\flow_流程项目01\流程\vs-flow05"

# 状态 / 拉取 / 提交
dazi flow project status --dir .
dazi flow project pull --flow 115 --dir .
dazi flow project push --dir . --canvas

# 单节点测试（uuid 见 flow.meta.json 或 node.info.json）
dazi flow run node-exec --node <node_uuid> --dir .

# 整流程调试 + 变量
dazi flow run flow-exec --dir . --type debug
dazi flow variable sync --dir .
dazi flow variable pull --name <output_variable_name> --dir .
```

## AI 修改现有流程（单文件入口）

> 推荐只把本文件附加给 AI；若信息不足，再按需打开「帮助文档」中的专题。

### 场景 A：新增节点（已有流程继续改）

1. 先读 `flow.json` 与 `flow.meta.json`，确认当前节点与连线
2. 新建节点（避免伪造 uuid）：`.scriptsdazi.ps1 flow node new --type <node_type> --dir . --label "<节点名>"`
3. 在 `flow.json` 里补 `nodes/edges`（遵守锚点：`sourceHandle` 仅 `r/b/true/false`，`targetHandle` 仅 `l/t`）
4. 若是代码节点，补 `节点/<名>/code.sql|py`
5. 单节点测试：`.scriptsdazi.ps1 flow run node-exec --node <node_uuid> --dir .`
6. 提交画布（含连线/配置）：`.scriptsdazi.ps1 flow project push --dir . --canvas`

### 场景 B：仅改节点代码

1. 编辑 `节点/<名>/code.sql|py`（不要把正文写回 `flow.json`）
2. 运行节点：`.scriptsdazi.ps1 flow run node-exec --node <node_uuid> --dir .`
3. 提交代码：`.scriptsdazi.ps1 flow node push --node <node_uuid> --dir .`

### 场景 C：画布和代码不同步

1. 先 `.scriptsdazi.ps1 flow project status --dir .` 看本地脏改动
2. 若改了拓扑/连线/配置：执行 `.scriptsdazi.ps1 flow project push --dir . --canvas`
3. 若只改了代码：执行 `.scriptsdazi.ps1 flow node push --node <node_uuid> --dir .`
4. 必要时重新拉取校对：`.scriptsdazi.ps1 flow project pull --flow <flowId> --dir .`

## AI 自检清单（提交前）

- 命令前缀是否统一为 `.scriptsdazi.ps1 flow ...`（而不是裸 `dazi-flow`）
- `flow.json` 是否只承载画布拓扑与节点配置（不嵌入大段 SQL/Python）
- `code.*` 是否与节点业务类型一致（SQL 节点 `code.sql`，Python 节点 `code.py`）
- 条件节点出边是否仅使用 `true/false`，未误用 `r/b`
- 若改动画布，是否执行了 `flow project push --canvas`

## 常见错误与修复

| 现象                     | 常见原因                          | 修复                                                        |
| ------------------------ | --------------------------------- | ----------------------------------------------------------- |
| 命令找不到               | 在 dazi-work 外执行，或用了旧前缀 | 切到 dazi-work 根，使用 `.scriptsdazi.ps1 flow ...`         |
| 节点测试报上游变量不存在 | 未先运行上游节点产出变量          | 先跑上游，或整流程 `flow run flow-exec --type debug` 后再测 |
| 画布显示对但平台不生效   | 只 push 了代码，未 push 画布      | 执行 `flow project push --dir . --canvas`                   |
| 代码改了但平台还是旧代码 | 改了本地 `code.*` 但未 node push  | 执行 `flow node push --node <node_uuid> --dir .`            |

## AI 自主运行与改错闭环（Agent 必读）

> **扩展/菜单不会自动改代码**（平台 D6）；用户委托你改流程时，你**必须主动**执行「改 → 跑 → 读错 → 再改 → 再跑」，直到通过或达到重试上限。

### 错误落在哪里（跑完必查）

| 运行方式               | 失败时读                      | 成功/步骤摘要                        |
| ---------------------- | ----------------------------- | ------------------------------------ |
| 单节点 `run node-exec` | `_run/<节点名>.last-error.md` | 无 error 文件即通过                  |
| 整流程 `run flow-exec` | `_run/flow.last-error.md`     | `_run/flow.last-run.md`（步骤+日志） |

CLI 带 `--json` 时：看返回 `success: false` 或 `errorFile` 字段，**再打开对应 md 文件**，不要只看终端一行报错。

### 标准改错循环（默认最多 3 轮）

1. **定位**：读 `flow.json` + 目标 `节点/<名>/code.*` + `flow.meta.json`（取 `node_uuid`）
2. **修改**：只改必要文件（代码 → `code.*`；连线/配置 → `flow.json`）
3. **验证**（先小后大）：
   - 单节点：`.scriptsdazi.ps1 flow run node-exec --node <node_uuid> --dir .`
   - 整流程：`.scriptsdazi.ps1 flow run flow-exec --dir . --type debug`
4. **判错**：退出码非 0 / JSON `success:false` → 打开 `_run/*.last-error.md`，按其中**错误分类**与 traceback 修复
5. **重试**：回到步骤 2；若 3 轮仍失败，汇总已尝试修复点并请求用户介入
6. **提交**（仅通过后）：代码 `node push`；画布 `project push --canvas`

### 常见失败 → 优先动作

| last-error 分类 | 优先检查                                                            |
| --------------- | ------------------------------------------------------------------- |
| 缺上游变量      | 先跑上游节点或整流程 debug，再 `variable pull` 看 schema            |
| 配置缺失        | `flow.json` 该节点 `data`（connectionId / output_variable_name 等） |
| 代码错误        | `code.*` 与 traceback；改后只 `node push`                           |
| 连接/数据源     | connectionId / spaceId 是否有效                                     |

### Agent 禁止项

- **禁止**未实际运行就声称「已修复/已通过」
- **禁止**不读 `_run/*.last-error.md` 就猜测原因
- **禁止**修复后跳过验证直接 `push`
- **禁止**把 SQL/Python 正文写回 `flow.json`

侧栏提示词可选用 **`flow/run-fix-loop`**（自主改错专用）。

扩展：右键 **`flow.json`** / **节点/** / **`code.*`** 可测试、提交、打开设计器。

## 编写节点代码

- **SQL 节点**（`sql-query` / `database-source`）：编辑 `节点/<名>/code.sql`；`sql-query` 中用 **上游变量名作表名**（`FROM 上游变量名`）
- **Python 节点**（`python-script`）：编辑 `code.py`；单节点测试用 **`get_variable("上游变量名")`**，输出赋值 **`result_df`**
- 变量约定与完整示例 → [流程变量系统指南](../../../../资源/docs/flow/variables-guide.md) · [节点代码编写指南](../../../../资源/docs/flow/node-code-guide.md)

## 帮助文档

工作区文档位于 **`资源/docs/`**（扩展侧栏 **帮助 → 下载所有文档**，或在工作区根执行 `dazi docs sync`）：

| 文档                                   | 链接                                                                      |
| -------------------------------------- | ------------------------------------------------------------------------- |
| Flow 文档索引（从这里开始）            | [flows-guide.md](../../../../资源/docs/flow/flows-guide.md)               |
| 数据流程项目开发指南                   | [flow-project-guide.md](../../../../资源/docs/flow/flow-project-guide.md) |
| 流程变量系统指南                       | [variables-guide.md](../../../../资源/docs/flow/variables-guide.md)       |
| 节点代码编写指南（含 SQL/Python 示例） | [node-code-guide.md](../../../../资源/docs/flow/node-code-guide.md)       |
| Flow 运行与测试                        | [run-guide.md](../../../../资源/docs/flow/run-guide.md)                   |
| 数据源与 connectionId                  | [source-guide.md](../../../../资源/docs/flow/source-guide.md)             |
| CLI 调用约定（`dazi.ps1`）             | [cli-invocation.md](../../../../资源/docs/guides/cli-invocation.md)       |

终端打开文档（在 **dazi-work 根**）：

```powershell
dazi docs open flow/flow-project-guide
dazi docs open flow/variables-guide
dazi docs open flow/node-code-guide
```

**代码示例**：变量读写、`python-script` / `sql-query` 模板见 [节点代码编写指南](../../../../资源/docs/flow/node-code-guide.md) 与 [流程变量系统指南](../../../../资源/docs/flow/variables-guide.md)。
