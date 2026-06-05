import type { ReportLayoutIR } from "@dazi/app-sdk-ui";

/** 开发预览用 RLIR（生产环境来自 manifest.report_design.layout_snapshot 或平台侧车） */
export const demoReportLayout: ReportLayoutIR = {
  title: "复杂报表示例",
  summary: "演示多级列分组与宽表列选择",
  columns: [
    { id: "col_dept", field: "dept", label: "部门", visible: true, leaf: true },
    { id: "col_qty", field: "qty", label: "产量", align: "right", format: "number", parentId: "grp_output", visible: true, leaf: true },
    { id: "col_yield", field: "yield_pct", label: "良品率%", align: "right", parentId: "grp_output", visible: true, leaf: true },
    { id: "col_cost", field: "unit_cost", label: "单位成本", align: "right", format: "number", parentId: "grp_fin", visible: true, leaf: true },
  ],
  columnGroups: [
    { id: "grp_output", label: "产出指标", children: ["col_qty", "col_yield"] },
    { id: "grp_fin", label: "成本", children: ["col_cost"] },
  ],
  wideTable: { defaultVisibleColumns: 8, columnPicker: true },
};
