# MCP 配置指南

**文档 ID**: `guides/mcp-setup`

## 在 Cursor 中配置搭子 MCP

在项目根目录创建 `.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "dazi": {
      "command": "node",
      "args": ["<dazi-vscode>/bundled/clis/dazi.js", "mcp", "stdio"],
      "env": {
        "DAZI_BUNDLED_DIR": "<dazi-vscode>/bundled/clis"
      }
    }
  }
}
```

生产交付（`dazi-work`）可将 `command` 改为包装脚本，或设置 `DAZI_BUNDLED_DIR` 指向 `tools/dazi-clis` / 扩展内 `bundled/clis`（见 [CLI 调用约定](./cli-invocation.md)）。

## 聚合 MCP 工具总览（`mcp stdio`）

运行 `dazi mcp tools` 查看完整列表，共 **28 个工具**：

### 📖 文档与提示词（4 个）

| 工具           | 说明                         |
| -------------- | ---------------------------- |
| `list_docs`    | 列出文档目录（可按分类过滤） |
| `get_doc`      | 获取文档完整内容             |
| `list_prompts` | 列出提示词目录               |
| `get_prompt`   | 获取提示词完整内容           |

### 🧠 本体 onto（8 个）

| 工具                  | 说明             |
| --------------------- | ---------------- |
| `onto_list_spaces`    | 列出所有本体空间 |
| `onto_list_functions` | 列出空间函数定义 |
| `onto_get_function`   | 查看函数详情     |
| `onto_run_function`   | 执行函数         |
| `onto_list_actions`   | 列出动作定义     |
| `onto_list_rules`     | 列出规则         |
| `onto_list_scripts`   | 列出脚本         |
| `onto_space_snapshot` | 拉取空间快照     |

### 🔄 流程 flow（9 个）

| 工具                   | 说明              |
| ---------------------- | ----------------- |
| `flow_list_flows`      | 列出 Flow         |
| `flow_get_flow`        | 查看 Flow 详情    |
| `flow_list_runs`       | 列出运行记录      |
| `flow_start_run`       | 启动 Flow         |
| `flow_debug_run`       | 调试最近 Run      |
| `flow_list_sources`    | 列出数据源        |
| `flow_source_tables`   | 列出数据源中的表  |
| `flow_table_structure` | 查看表列结构      |
| `flow_snapshot_pull`   | 拉取快照          |
| `flow_plan_llm_guide`  | 生成 LLM 引导文档 |

### 🗂 数据 data（4 个）

| 工具                | 说明                |
| ------------------- | ------------------- |
| `data_list_spaces`  | 列出数据空间        |
| `data_list_tables`  | 列出数据表          |
| `data_table_schema` | 查看表字段结构      |
| `data_table_sample` | 采样数据（前 N 行） |

## Cursor 使用示例

```
给我 onto/function-guide 文档
→ get_doc({"id": "onto/function-guide"})

列出 space-001 的所有函数
→ onto_list_functions({"space_id": "space-001"})

调试最近一次 Flow 运行失败原因
→ flow_debug_run({"flow_id": "flow-abc123"})

查看 orders 表的字段结构
→ flow_table_structure({"source_id": "ch-main", "table_name": "orders"})
```
