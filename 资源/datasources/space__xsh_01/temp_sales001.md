# 表：temp_sales001（销售表临时数据001）

## 基本信息

| 项 | 值 |
| --- | --- |
| 连接 | `clickhouse__space_xsh_01` |
| 表名 | `temp_sales001` |
| 中文名 | 销售表临时数据001 |
| 来源流程 | VS-flow0（flowId `103`） |
| 写入节点 | `写入销售临时表`（database-sink） |
| 输入变量 | `销售明细宽表`（96 行 JOIN 宽表） |

## 列结构（与流程变量一致）

| 列名 | 类型（Parquet/变量） | 说明 |
| --- | --- | --- |
| 销售ID | int64 | 销售记录主键 |
| 地区 | string | 销售区域 |
| 产品ID | string | 产品编码 |
| 产品名称 | string | 产品维表名称 |
| 产品说明 | string | 产品维表说明 |
| 规格ID | string | 规格编码 |
| 规格名称 | string | 规格维表名称 |
| 规格说明 | string | 规格维表说明 |
| 颜色 | string | 颜色编码 |
| 数量 | int64 | 销售数量 |
| 金额 | double | 销售金额 |
| 日期 | timestamp | 销售日期 |

## 流程节点配置示例

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
