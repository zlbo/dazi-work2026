import type { ReportLayoutIR } from "@dazi/app-sdk-ui";
import layoutJson from "./generated/reportLayout.json";

/** 来自 `资源/files/单一分析表2026.xlsx_575878bb/报表布局.json` */
export const financialReportLayout: ReportLayoutIR = {
  title: layoutJson.title,
  summary: layoutJson.summary,
  columnGroups: layoutJson.columnGroups,
  wideTable: layoutJson.wideTable,
  columns: layoutJson.columns.map((c) => ({
    id: c.id,
    field: c.field,
    label: c.label,
    align: c.align as "left" | "right" | "center" | undefined,
    parentId: c.parentId,
    visible: c.visible,
    leaf: c.leaf,
    format:
      c.field === "category" || c.field === "indicator" ? undefined : "number",
  })),
};

/** @deprecated 保留旧示例名，指向财务指标表布局 */
export const demoReportLayout = financialReportLayout;
