# Flow 执行计划

**文档 ID**: `flow/plan-guide`

## 编译计划

```bash
dazi-flow plan compile <flow-id>

# 带输入参数
dazi-flow plan compile <flow-id> --input '{"date": "2026-01-01"}'
```

计划保存到 `flows/<flow-id>/plans/plan.json`。

## 应用计划

```bash
# 验证（dry-run）
dazi-flow plan apply <flow-id> --dry-run

# 执行应用
dazi-flow plan apply <flow-id>
```

## 导出 Markdown 文档

```bash
# 摘要文档
dazi-flow plan markdown <flow-id> --type summary

# 详细文档
dazi-flow plan markdown <flow-id> --type detail

# 流程图（Mermaid）
dazi-flow plan markdown <flow-id> --type diagram
```

## 生成 LLM 引导文档

生成供 Cursor/LLM 理解 Flow 结构的文档：

```bash
dazi-flow plan llm-guide <flow-id>
```

保存到 `flows/<flow-id>/plans/llm-guide.md`，内容包括：
- Flow 目的说明
- 节点功能描述
- 数据流向
- 关键配置项

## 生成数据库脚手架

根据 Flow 的数据模型生成建表 DDL：

```bash
dazi-flow plan scaffold-database <flow-id> --dialect clickhouse
```
