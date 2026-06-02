# 数据连接：space__panda_construction_005

## 基本信息

| 项 | 值 |
| --- | --- |
| 连接 ID | `clickhouse__space_panda_construction_005` |
| 名称 | space__panda_construction_005 |
| 类型 | `clickhouse` |
| 描述 | — |
| 主机 | 43.136.220.149 |
| 端口 | 8123 |
| 数据库 | space__panda_construction_005 |
| Schema | — |
| 用户名 | default |
| 关联空间 | — |
| 导出时间 | 2026-06-01T13:39:44.764Z |

## 流程节点引用

在 `flow.json` 中，`database-source`、`database-sink`、`sql-query` 等节点使用 **`connectionId`** 指向本连接：

```json
{
  "type": "database-source",
  "data": {
    "connectionId": "clickhouse__space_panda_construction_005",
    "output_variable_name": "查询结果",
    "code": { "sql": "SELECT * FROM your_table LIMIT 100" }
  }
}
```

- `connectionId` 必须为 **`ads_connections` 的字符串 id**（见上文「连接 ID」）。
- 表结构详情可拉取各表的「下载表信息」到 `资源/datasources/<连接名>/` 目录。
- 开发时可将本文件 @ 引用给 AI，便于填写 SQL 与节点配置。

## 数据表列表

| 表名 | 类型 |
| --- | --- |
| （暂无表） | |

## 连接配置（已脱敏）

```json
{
  "host": "43.136.220.149",
  "port": 8123,
  "user": "default",
  "password": "***",
  "database": "space__panda_construction_005",
  "interface": "http"
}
```
