# 分包商维表

- 数据空间：`space__panda_construction`（ID: `space__panda_construction`）
- 表标识：`abbe83de39e247b0`
- 物理表名：`dim_subcontractor`
- 导出时间：2026-06-10T07:31:35.743Z

## 字段结构

| 显示名 | 字段名 | 类型 | 可空 | 说明 |
| --- | --- | --- | --- | --- |
| 分包商ID | `subcontractor_id` | String | 是 | 主键 |
| 分包商编号 | `subcontractor_code` | String | 是 |  |
| 分包商名称 | `subcontractor_name` | String | 是 |  |
| 资质等级 | `qualification_level` | String | 是 |  |
| 专业类别 | `professional_category` | String | 是 |  |
| 项目经理 | `project_manager` | String | 是 |  |
| 分包类型 | `subcontract_type` | String | 是 | 劳务/专业 |
| 安全许可证 | `safety_license` | String | 是 |  |
| 状态 | `status` | String | 是 |  |
| 创建时间 | `created_at` | DateTime | 是 |  |

## 数据预览（前 10 行）

| 分包商ID | 分包商编号 | 分包商名称 | 资质等级 | 专业类别 | 项目经理 | 分包类型 | 安全许可证 | 状态 | 创建时间 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SC001 | BJGS | 北京钢构 | 一级 | 钢结构 | 赵工 | 专业分包 | SAF-SC-001 | 正常 | 2025-01-01 00:00:00+08:00 |
| SC002 | GDGC | 广东建工机械 | 二级 | 机械租赁 | 王总 | 劳务分包 | SAF-SC-002 | 正常 | 2025-01-01 00:00:00+08:00 |
| SC003 | SHLW | 上海劳务 | 二级 | 劳务 | 李经理 | 劳务分包 | SAF-SC-003 | 正常 | 2025-01-01 00:00:00+08:00 |
