# 主要财务指标复杂报表（DRAP 模板）

基于实践应用 `complex-report-003` 沉淀的**集团财务宽表**模板：多级表头、类别纵向合并、条件行样式、左侧列冻结。

| 项 | 值 |
|----|-----|
| 模板 ID | `financial-indicators-complex-report` |
| 场景标签 | `financial_indicators_complex_report` |
| 参考应用 | `complex-report-003` |
| 开发文档 | [`dazi/docs/app/主要财务指标复杂报表开发实践.md`](../../../docs/app/主要财务指标复杂报表开发实践.md) |

## 快速开始

```powershell
cd ..  # 应用项目根（本 README 在 templates/ 子目录时）
pnpm install

# 本地预览模板
pnpm --filter @dazi/app-template-financial-indicators-complex-report run dev

# 从模板初始化新应用（在 dazi-work 根；路径按实际项目名调整）
cd D:\path\to\dazi-work
.\scripts\dazi.ps1 app init financial-indicators-complex-report --space space__0519 --dir 项目/app_<名>/apps/my-fin-report-001
```

## 目录要点

- `src/fixtures/generated/reportLayout.json` — RLIR（仅叶子列）
- `src/fixtures/generated/reportRows.json` — 28 行样例数据
- `src/fixtures/reportLayout.ts` — `normalizeReportLayout()`（过滤 `leaf:false` 父列）
- `src/pages/MainPage.tsx` — `ComplexReport` + `useReportDataset`

## 发布前

1. 管理端上传 Excel → 报表布局解析 → VS Code 拉取 `报表布局.json`
2. 绑定 `manifest.report_design.managed_file_id`，发布时写入 `layout_snapshot`
3. `pnpm run build` → `.\scripts\dazi.ps1 app upload --cwd 项目/app_<名>/apps/<app_id> --activate`（在 dazi-work 根）
