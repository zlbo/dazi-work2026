# 页面意图：成本报表测试01

## 业务目标

渲染**成本报表测试01**：左侧为组织、年度、月度、项目；中部为成本项（含直接成本子分组）；右侧为成本比较（实际/目标/实目比）。支持横向滚动与左侧四列冻结。

## UI 组件

- `PageLayout`：标题、刷新工具栏
- `ComplexReport`：三级表头（headerCells）、组织/年度 `rowMerge`、总计行强调

## 数据

- 数据集 key：`report_data`
- 设计稿：`Excel成本报表08.xlsx`（`managed_file_id: 51853ede-9e6b-4a3a-aa7a-060cbead0862`）
- 开发：`src/fixtures/generated/reportRows.json`（15 行样例）
- 生产：`manifest.report_design.binding` + SQL/ontology（`drap-assets/`）

## 禁止

- 禁止 `fetch` / 裸 axios
- 禁止忽略 `normalizeReportLayout`
- 禁止将 `leaf:false` 父列保留在 `columns`
