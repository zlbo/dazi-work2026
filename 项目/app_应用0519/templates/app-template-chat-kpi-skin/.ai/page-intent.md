# 页面用途（模板示例）

【聊天问数 KPI 皮肤】，`mount.type=chat_result`，用于 AI 聊天主区紧凑展示。

## 适合（示例）

- 问数结果 1–4 个核心数值（**个数可改**）
- 轻量 KPI 横排

## 禁止

- 当作全页看板（页模式请用 profit-analysis 等模板）
- 裸 HTTP、`fetch`、直接 `echarts`

## 必须

- `useResultDataset()`（主数据来自宿主 `message`）
- `@dazi/app-sdk-ui` 的 `KpiCard`；高度随内容收缩
