# 数据连接： space__xsh_01

## 基本信息

| 项 | 值 |
| --- | --- |
| 连接 ID | `clickhouse__space_xsh_01` |
| 名称 |  space__xsh_01 |
| 类型 | `clickhouse` |
| 描述 | space__xsh_01 |
| 主机 | 43.136.220.149 |
| 端口 | 8123 |
| 数据库 | space__xsh_01 |
| Schema | — |
| 用户名 | default |
| 关联空间 | — |
| 导出时间 | 2026-05-30T14:30:28.871Z |

## 流程节点引用

在 `flow.json` 中，`database-source`、`database-sink`、`sql-query` 等节点使用 **`connectionId`** 指向本连接：

**database-source（读库）**

```json
{
  "type": "database-source",
  "data": {
    "connectionId": "clickhouse__space_xsh_01",
    "output_variable_name": "查询结果",
    "code": { "sql": "SELECT * FROM your_table LIMIT 100" }
  }
}
```

**database-sink（写库，VS-flow0 示例）**

```json
{
  "type": "database-sink",
  "data": {
    "connectionId": "clickhouse__space_xsh_01",
    "tableName": "temp_sales001",
    "display_name": "销售表临时数据001",
    "input_variable_name": "销售明细宽表"
  }
}
```

- `connectionId` 必须为 **`ads_connections` 的字符串 id**（见上文「连接 ID」）。
- 表结构详情可拉取各表的「下载表信息」到 `资源/datasources/<连接名>/` 目录。
- 开发时可将本文件 @ 引用给 AI，便于填写 SQL 与节点配置。

## 数据表列表

| 表名 | 类型 |
| --- | --- |
| `budget_plan` | TABLE |
| `cost_center_info` | TABLE |
| `cost_type_info` | TABLE |
| `daily_cost_report` | TABLE |
| `energy_consumption` | TABLE |
| `equipment_info` | TABLE |
| `equipment_maintenance_cost` | TABLE |
| `labor_cost` | TABLE |
| `mine_area_info` | TABLE |
| `period_expense` | TABLE |
| `product_type_info` | TABLE |
| `production_daily_report` | TABLE |
| `raw_material_cost` | TABLE |
| `supplier_info` | TABLE |
| `temp001` | TABLE |
| `temp_sales001` | TABLE（销售表临时数据001，VS-flow0 写入） |
| `temp005` | TABLE |
| `temp01` | TABLE |
| `transport_cost` | TABLE |

## 连接配置（已脱敏）

```json
{
  "host": "43.136.220.149",
  "port": 8123,
  "user": "default",
  "password": "***",
  "database": " space__xsh_01",
  "interface": "http"
}
```
