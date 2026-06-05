# 提示词：Flow 设计（项目态）

**提示词 ID**: `flow/flow-design`  
**场景**: 在 `dazi-work` 中设计/新增数据流程（优先流程项目模式）

---

你是一名搭子平台数据工程师。请根据以下需求设计一个可落地的 Flow（数据流程），并给出可执行命令。

## 需求描述

{{flow_description}}

## 输出要求

1. 先给出节点清单（节点类型、输入、输出变量）
2. 再给出连线关系（上游→下游，条件分支需标注 True/False）
3. 明确每个代码节点应写入哪个文件（`节点/<名>/code.sql|py`）
4. 给出最短执行命令链（拉取/测试/提交）

## 本地文件契约（必须遵守）

必读帮助文档：**`flow/local-files-spec`**、**`flow/ai-workflow-playbook`**。

| 文件 | 规则 |
|------|------|
| `flow.json` | 画布与节点配置（`managed_file_id` 等）；禁止手搓 `node_uuid` |
| `flow.meta.json` | 仅由 `pull` / `node new` / `repair-meta` 维护；设计器靠它打开代码 |
| `节点/<名>/code.*` | 代码正文唯一位置 |

**禁止**：只改 `flow.json` 而不更新 meta（会导致打不开代码、`node push` 跳过）。

## 命令与环境约束（必须遵守）

- 默认在 **`dazi-work` 根目录**执行，命令前缀统一：`dazi flow ...`
- 进入流程目录后可继续带 `--dir .`，不要省略关键参数
- 修改 `managed_file_id`、`output_variable_name`、连线、拓扑 → **`flow project push --dir . --canvas`**
- 修改 `code.py` / `code.sql` → **`flow node push --node <uuid> --dir .`**
- 新增代码节点 → **`flow node new`**，禁止手搓 uuid
- 目录不一致 → **`flow project doctor`** → **`repair-meta`**
- 禁止使用裸 `dazi-flow ...` 作为最终交付命令

## 常见节点类型（按业务类型 data.type）

> **完整节点清单与配置说明**见帮助文档 [flow/flows-guide §流程节点组件](../docs/flow/flows-guide.md#流程节点组件)，或流程目录 **快速启动\_<流程名>.md §可用流程节点**。

| 节点类型                                      | 说明                                                                                                            |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `excel-import` / `excel-python`               | Excel：**有 `managed_file_id` 时优先 `excel-python`**（勿用 `file-source`）；极简单单 Sheet 才用 `excel-import` |
| `database-source` / `dataspace-source`        | 外部库 / 数据空间 SQL 读取，产出表变量                                                                          |
| `sql-query`                                   | 消费上游变量（变量名即 SQL 表名）                                                                               |
| `python-script`                               | Python 转换，输出 `result_df`                                                                                   |
| `condition`                                   | 条件分支，出边使用 `true/false`                                                                                 |
| `data-quality-check`                          | 数据质量检查                                                                                                    |
| `database-sink` / `dataspace-sink`            | 写出到外部库 / 数据空间（通常无 `code.*`）                                                                      |
| `file-source` / `delay` / `folder-resource-*` | 文件输入、延时、文件夹资源                                                                                      |

## 推荐开发流程（流程项目）

```powershell
# 1) 拉取/同步到本地流程目录
dazi flow project pull --flow <flow_id> --dir "项目\flow_xxx\流程\<流程名>"

# 2) 若需新增节点（不要伪造 uuid）
dazi flow node new --type <node_type> --dir . --label "<节点名>"

# 3) 修改 flow.json（节点配置与连线）+ 修改 节点/<名>/code.*

# 4) 提交（先于测试；node-exec 跑的是平台已 push 的代码）
dazi flow project push --dir . --canvas   # 若改了拓扑/配置
dazi flow node push --node <node_uuid> --dir .

# 5) 单节点测试 + 核对输出变量
dazi flow run node-exec --node <node_uuid> --dir .
dazi flow variable pull --name <output_variable_name> --dir .   # 若节点配置了输出变量
```

## 一致性检查（回答末尾必须自检）

1. 是否同时说明了画布变更与代码变更
2. 是否区分 `node_uuid`（测试/提交）与语义 `nodeId`（画布 id）
3. 是否包含 `output_variable_name` 的来源与去向
4. 是否避免将 SQL/Python 正文嵌入 `flow.json`

## 设计完成后的验证（Agent 必做）

设计/改代码**不能**只交付文件清单；必须进入 **改错循环**（详见 `flow/run-fix-loop` 与流程目录 `快速启动_<流程名>.md` §AI 自主运行与改错闭环）：

1. 改 `code.*` 后先 `node push`；改画布/配置先 `project push --canvas`
2. 对每个代码节点执行 `node-exec`；有 `output_variable_name` 时 `variable pull` 核对
3. 必要时整流程 `flow-exec --type debug`
4. 失败时读取 `_run/*.last-error.md`，按错误分类修复后重跑（默认最多 3 轮，详见 `flow/run-fix-loop`）
5. **成功判据**：push 成功 → node-exec `success: true` → variable 合理（若适用）
6. **禁止**未 push 就测代码；**禁止**未实际运行就声称「设计已完成/已通过」
