# Flow 文档索引

**文档 ID**: `flow/flows-guide`

> v3.1 起，日常流程开发请优先阅读 **[数据流程项目开发指南](./flow-project-guide.md)**。  
> 本文保留平台级 Flow 操作速查，并链到各专题文档。

---

## 推荐阅读顺序

1. [数据流程项目开发指南](./flow-project-guide.md) — 目录结构、`dazi.ps1 flow`、菜单、pull/push 循环
2. **[画布节点与连线规范](./flow-project-guide.md#62-画布节点与连线规范ai-创建--编辑-flowjson-必读)** — **AI 创建流程必读**：节点尺寸 200px、锚点 `l/t/r/b/true/false`、条件分支
3. [流程开发最佳实践（VS-flow0 案例）](./流程开发最佳实践-VS-flow0案例.md) — **端到端案例**：Excel → 质检 → SQL → 落库、五阶段开发法、检查表
4. [流程变量系统指南](./variables-guide.md) — 变量模型、`output_variable_name`、代码节点如何用变量
5. [节点代码编写指南](./node-code-guide.md) — `python-script`、`sql-query` 等单节点代码
6. [Flow 运行与测试](./run-guide.md) — 单节点/整流程运行、变量
7. [CLI 调用约定](../guides/cli-invocation.md) — `.\scripts\dazi.ps1` 在 Trae/VS Code 中的用法

---

## 终端命令前缀

在 **`dazi-work` 根目录**（Trae、VS Code、Cursor 交付环境）：

```powershell
.\scripts\dazi.ps1 flow <子命令...>
```

等价于开发时的 `dazi-flow <子命令...>`。示例：

```powershell
.\scripts\dazi.ps1 flow flows list
.\scripts\dazi.ps1 flow project pull --flow 98 --dir "项目\flow_xxx\流程\MyFlow"
```

---

## 流程项目（`项目/flow_*`）常用命令

| 任务               | 命令                                                |
| ------------------ | --------------------------------------------------- |
| 拉取平台流程到本地 | `flow project pull --flow <id> --dir <流程目录>`    |
| 提交代码 + 画布    | `flow project push --dir <流程目录> --canvas`       |
| 查看本地改动       | `flow project status --dir <流程目录>`              |
| 提交单个节点代码   | `flow node push --node <uuid> --dir <流程目录>`     |
| 单节点测试         | `flow run node-exec --node <uuid> --dir <流程目录>` |
| 整流程运行         | `flow run flow-exec --dir <流程目录> --type debug`  |
| 拉取变量           | `flow variable pull --name <名> --dir <流程目录>`   |

扩展侧栏/资源管理器右键与上表 **同源**，见 [flow-project-guide](./flow-project-guide.md#6-资源管理器菜单主交互)。

---

## 平台级 Flow 操作

| 任务 | 命令                              |
| ---- | --------------------------------- |
| 列表 | `flow flows list`                 |
| 详情 | `flow flows get <flow-id>`        |
| 新建 | `flow flows create --name "名称"` |
| 校验 | `flow flows validate <flow-id>`   |

---

## AI 创建流程速查

| 主题                                            | 文档章节                                                                            |
| ----------------------------------------------- | ----------------------------------------------------------------------------------- |
| **节点尺寸与布局**（200px 宽、260×140 间距）    | [flow-project-guide §6.2.1](./flow-project-guide.md#621-节点尺寸与布局)             |
| **连线锚点**（`sourceHandle` / `targetHandle`） | [flow-project-guide §6.2.2](./flow-project-guide.md#622-锚点连线端点约定)           |
| **条件节点 True/False 分支**                    | [flow-project-guide §6.2.4](./flow-project-guide.md#624-条件节点condition)          |
| **`flow.json` 边与完整示例**                    | [flow-project-guide §6.2.5–6.2.6](./flow-project-guide.md#625-flowjson-边edges字段) |
| **提交前自检清单**                              | [flow-project-guide §6.2.7](./flow-project-guide.md#627-ai-自检清单)                |
| **端到端案例与启动检查表**                      | [流程开发最佳实践-VS-flow0案例](./流程开发最佳实践-VS-flow0案例.md)                 |
| 变量串联与 `output_variable_name`               | [variables-guide](./variables-guide.md)                                             |
| 节点 `code.py` / `code.sql`                     | [node-code-guide](./node-code-guide.md)                                             |

---

## 最佳实践系列

按 **`NN-主题-案例标识.md`** 编号发布，每篇对应一个可复用的端到端模式。新增篇章请递增编号并在此登记。

| 编号 | 文档                                                                    | 说明                                                  |
| ---- | ----------------------------------------------------------------------- | ----------------------------------------------------- |
| 01   | [流程开发最佳实践（VS-flow0 案例）](./流程开发最佳实践-VS-flow0案例.md) | Excel 多表 → 质检分支 → SQL 宽表 → database-sink 落库 |

---

## 其他专题

| 文档                                       | 说明                                        |
| ------------------------------------------ | ------------------------------------------- |
| [流程变量系统指南](./variables-guide.md)   | 变量产生/消费、`get_variable`、SQL 表名约定 |
| [Flow 运行与测试](./run-guide.md)          | Run、debug、变量、流程项目测试              |
| [Flow 快照管理](./snapshot-guide.md)       | 平台级 `flows/<id>/snapshot.json` 分离快照  |
| [数据源管理](./source-guide.md)            | connectionId、表结构                        |
| [Flow 执行计划](./plan-guide.md)           | FlowPlan / markdown 规划                    |
| [CLI 命令速查](../guides/cli-reference.md) | 完整命令表                                  |

---
