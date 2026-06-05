# 页面意图：主要财务指标复杂报表

## 业务目标

渲染**主要财务指标表**：左侧为类别、指标名称；中部为 2017–2022 年度列；右侧为分月列（2021/2022/2023 等），支持横向滚动与左侧冻结。

## UI 组件

- `PageLayout`：标题、刷新工具栏
- `ComplexReport`：多级表头、类别 `rowMerge`、行强调/警示色

## 数据

- 数据集 key：`report_data`
- 开发：`src/fixtures/generated/reportRows.json`
- 生产：`manifest.report_design.binding` + SQL/ontology（`drap-assets/`）

## 禁止

- 禁止 `fetch` / 裸 axios
- 禁止忽略 `normalizeReportLayout`
- 禁止将 `leaf:false` 父列保留在 `columns`
