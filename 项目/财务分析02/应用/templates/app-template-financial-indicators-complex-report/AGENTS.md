# 主要财务指标复杂报表（模板）· AI 上下文

> 模板：`financial-indicators-complex-report`  
> 实践来源：`complex-report-003`  
> 用户文档：[`dazi/docs/app/主要财务指标复杂报表开发实践.md`](../../../docs/app/主要财务指标复杂报表开发实践.md)

## 必须遵守

1. 页面只用 `ComplexReport` + `useReportDataset`，禁止手写百列表格。
2. RLIR 中 **`leaf: false` 分组父列不得进入 `columns`**，须经 `normalizeReportLayout()` 过滤。
3. `static` 数据源分页/列投影在本地完成，禁止循环 `fetch-data-sources`。
4. `onVisibleFieldsChange` 须稳定回调并做内容比较。

## 数据源

| key | kind | 说明 |
|-----|------|------|
| `report_data` | `static`（开发）/ `sql_template`（上线） | 宽表指标数据 |

## 关键文件

| 文件 | 职责 |
|------|------|
| `src/fixtures/reportLayout.ts` | RLIR 规范化 + 行样式默认规则 |
| `src/pages/MainPage.tsx` | 页面入口 |
| `manifest.json` | `report_design.layout_snapshot` + binding |
