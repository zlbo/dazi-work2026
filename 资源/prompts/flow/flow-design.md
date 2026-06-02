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

## 命令与环境约束（必须遵守）

- 默认在 **`dazi-work` 根目录**执行，命令前缀统一：`.\scripts\dazi.ps1 flow ...`
- 进入流程目录后可继续带 `--dir .`，不要省略关键参数
- `flow.json` 是画布与配置真理源；`节点/<名>/code.*` 是代码真理源
- 修改拓扑/连线/节点配置后，必须 `flow project push --dir . --canvas`
- 禁止使用裸 `dazi-flow ...` 作为最终交付命令

## 常见节点类型（按业务类型 data.type）

| 节点类型 | 说明 |
|---------|------|
| `database-source` / `dataspace-source` | SQL 读取数据，产出表变量 |
| `sql-query` | 消费上游变量（变量名即 SQL 表名） |
| `python-script` | Python 转换，输出 `result_df` |
| `condition` | 条件分支，出边使用 `true/false` |
| `database-sink` / `dataspace-sink` | 写出目标（通常无 `code.*`） |

## 推荐开发流程（流程项目）

```powershell
# 1) 拉取/同步到本地流程目录
.\scripts\dazi.ps1 flow project pull --flow <flow_id> --dir "项目\flow_xxx\流程\<流程名>"

# 2) 若需新增节点（不要伪造 uuid）
.\scripts\dazi.ps1 flow node new --type <node_type> --dir . --label "<节点名>"

# 3) 修改 flow.json（节点配置与连线）+ 修改 节点/<名>/code.*

# 4) 单节点测试
.\scripts\dazi.ps1 flow run node-exec --node <node_uuid> --dir .

# 5) 提交（代码可用 node push；拓扑/配置变更必须 canvas push）
.\scripts\dazi.ps1 flow node push --node <node_uuid> --dir .
.\scripts\dazi.ps1 flow project push --dir . --canvas
```

## 一致性检查（回答末尾必须自检）

1. 是否同时说明了画布变更与代码变更
2. 是否区分 `node_uuid`（测试/提交）与语义 `nodeId`（画布 id）
3. 是否包含 `output_variable_name` 的来源与去向
4. 是否避免将 SQL/Python 正文嵌入 `flow.json`
