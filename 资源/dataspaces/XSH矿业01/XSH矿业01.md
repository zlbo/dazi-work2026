# 数据空间：XSH矿业01

## 基本信息

| 项 | 值 |
| --- | --- |
| 空间 ID | `space__xsh_01` |
| 名称 | XSH矿业01 |
| 描述 | — |
| 存储引擎 | clickhouse |
| 语义层 | native |
| 表数量 | 15 |
| 关系数量 | 6 |
| 业务域 | — |
| 状态 | active |
| 导出时间 | 2026-06-02T02:36:57.782Z |

## 流程与开发引用

- **数据空间 ID**：`space__xsh_01`（CLI：`dazi-flow dataspace list` / `dazi data space list`）
- 空间内表可在侧栏展开后「下载表信息」，保存到 `资源/dataspaces/<空间名>/` 下各表 md。
- 流程节点：`dataspace-source` / `dataspace-sink` 使用 **`spaceId`**（本 ID）+ `code.sql`（读取）或 `tableName`（写入）；读外部库用 `database-source` 的 **`connectionId`**。
- 开发时可将本文件 @ 引用给 AI，便于了解可用表与空间上下文。

## 数据表列表

| 显示名 | 物理表名 | 表 ID | 类型 |
| --- | --- | --- | --- |
| 供应商信息表 | `supplier_info` | `054995db28c84a6e` | native |
| 预算计划表 | `budget_plan` | `a50f9bc00e714e7e` | native |
| 期间费用表 | `period_expense` | `35b4c613ee61481f` | native |
| 运输成本表 | `transport_cost` | `06984ba3a49943b5` | native |
| 设备维护成本表 | `equipment_maintenance_cost` | `9fdf30fc605b4622` | native |
| 人工成本表 | `labor_cost` | `7a0dea3ff0a34b70` | native |
| 能源消耗表 | `energy_consumption` | `fba54953093548ab` | native |
| 原材料成本明细表 | `raw_material_cost` | `2d80c368437540a5` | native |
| 成本中心表 | `cost_center_info` | `713eadcde1cf49eb` | native |
| 成本类型表 | `cost_type_info` | `039a5abf859f4d0a` | native |
| 日成本报表 | `daily_cost_report` | `63a74c611e004f4d` | native |
| 设备信息表 | `equipment_info` | `10c060a409e94f00` | native |
| 产品类型表 | `product_type_info` | `ff568686d10a41d9` | native |
| 矿区信息表 | `mine_area_info` | `a7e7e8a994164a55` | native |
| 生产日报表 | `production_daily_report` | `8f715c307a4f48da` | native |
