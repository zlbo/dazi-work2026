import type { ReportLayoutIR } from "@dazi/app-sdk-ui";
import layoutJson from "./generated/reportLayout.json";

type RawColumn = (typeof layoutJson.columns)[number];

const DIM_FIELDS = new Set(["organization", "year", "month", "project"]);

function mapColumn(c: RawColumn) {
  return {
    id: c.id,
    field: c.field,
    label: c.label,
    colIndex: c.colIndex,
    align: (DIM_FIELDS.has(c.field) ? "left" : "right") as "left" | "right" | "center",
    parentId: c.parentId,
    visible: c.visible,
    leaf: c.leaf,
    rowMerge: c.field === "organization" || c.field === "year",
    format: DIM_FIELDS.has(c.field) ? undefined : ("number" as const),
  };
}

/**
 * RLIR 中 leaf:false 的分组父列只应出现在 columnGroups；
 * 若保留在 columns 会导致 ComplexReport 表头错位。
 */
export function normalizeReportLayout(layout: ReportLayoutIR): ReportLayoutIR {
  const columns = (layout.columns ?? []).filter((c) => c.leaf !== false);
  const leafCount = columns.length;
  const wideTable = layout.wideTable
    ? {
        ...layout.wideTable,
        totalFields: leafCount,
        defaultVisibleColumns: Math.min(
          layout.wideTable.defaultVisibleColumns ?? leafCount,
          leafCount,
        ),
      }
    : undefined;
  return {
    ...layout,
    columns: columns.map((c) => ({
      ...c,
      rowMerge:
        c.rowMerge ??
        (c.field === "organization" || c.field === "year"),
    })),
    wideTable,
    features: {
      ...layout.features,
      rowEmphasis: layout.features?.rowEmphasis ?? [
        { field: "project", includes: "总计" },
        { field: "organization", includes: "总计" },
        { field: "month", includes: "总计" },
      ],
    },
  };
}

/** 来自 `资源/files/Excel成本报表08.xlsx_51853ede/报表布局.json` */
export const costReportLayout: ReportLayoutIR = normalizeReportLayout({
  title: layoutJson.title,
  summary: layoutJson.summary,
  columnGroups: layoutJson.columnGroups,
  headerCells: layoutJson.headerCells,
  headerRowCount: layoutJson.headerRowCount,
  wideTable: layoutJson.wideTable,
  columns: layoutJson.columns.map(mapColumn),
  features: layoutJson.features,
});

/** @deprecated 保留旧导出名 */
export const financialReportLayout = costReportLayout;
export const demoReportLayout = costReportLayout;
