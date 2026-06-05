# complex-report-003

基于 `单一分析表2026.xlsx`（`575878bb-0e11-4b76-bd22-24623b6ddd8a`）的**主要财务指标表**复杂报表。

- 布局：`资源/files/单一分析表2026.xlsx_575878bb/报表布局.json` → `manifest.report_design.layout_snapshot`
- 静态数据：从 `原生解析.md` 解析 → `src/fixtures/generated/reportRows.json`（28 行 × 36 列）
- **开发实践文档**：[复杂报表开发003开发实践.md](./复杂报表开发003开发实践.md)（后续中国式复杂报表参考）

```powershell
cd "项目/app_应用0519/apps/complex-report-003"
pnpm run dev
```

重新生成 fixtures（更新 Excel 拉取后）：

```powershell
node -e "/* 见 .ai/implement-from-managed-file.md 或 复杂报表开发003开发实践.md §4.3 */"
```
