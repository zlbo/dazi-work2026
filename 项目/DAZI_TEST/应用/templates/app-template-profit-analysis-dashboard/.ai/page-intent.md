# 页面用途（模板示例）

【利润分析】页模式应用（`mount.type=page`）。

## 适合（示例场景）

- KPI 卡片：营收 / 净利润 / 利润率（**数量与指标名可改**）
- 趋势图、对比表、多维切片（增 manifest key 即可）

## 禁止

- 裸 `fetch` / `axios`、直接 `import echarts`、篡改 `window` / 存储

## 必须

- `useDataset` / `useSemanticQuery` 等 SDK 数据 hook
- `@dazi/app-sdk-ui`：`PageLayout`、`KpiCard`、`TrendChart`、`DataGrid` 等
- `useAppearance()` 适配主题
