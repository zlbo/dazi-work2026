# 页面用途（模板示例）

【生产指挥中心】页模式应用（`mount.type=page`），`scene_tag=command_center`。

## 适合（示例场景）

- 制造 KPI 一屏总览（产量、达成率、合格率等；**默认示例为横排 KPI，数量可改**）
- 指挥中心 / 投屏场景
- 可扩展：趋势、告警列表、产线状态（新增 manifest key + 组件）

## 禁止

- 裸 HTTP、全局对象篡改、未经 SDK 的数据访问

## 必须

- `useDataset` + `@dazi/app-sdk-ui`（`PageLayout`、`KpiCard` 等）
- `useAppearance()` 适配主题
