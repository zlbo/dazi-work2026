# 页面用途（模板示例）

【聊天问数趋势皮肤】，`mount.type=chat_result`，紧凑趋势/折线展示。

## 适合（示例）

- 问数结果中的时间序列、少量维度对比

## 禁止

- 全页复杂看板、裸 HTTP、直接 `echarts`

## 必须

- `useResultDataset()`
- SDK 图表组件；`useAppearance()` 适配主题
