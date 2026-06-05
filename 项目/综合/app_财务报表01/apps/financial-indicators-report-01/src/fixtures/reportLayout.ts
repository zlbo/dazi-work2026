import type { ReportLayoutIR } from "@dazi/app-sdk-ui";
import layoutJson from "./generated/reportLayout.json";

type RawColumn = (typeof layoutJson.columns)[number];

function mapColumn(c: RawColumn) {
  return {
    id: c.id,
    field: c.field,
    label: c.label,
    align: c.align as "left" | "right" | "center" | undefined,
    parentId: c.parentId,
    visible: c.visible,
    leaf: c.leaf,
    rowMerge: c.field === "category",
    format:
      c.field === "category" || c.field === "indicator" ? undefined : ("number" as const),
  };
}

/**
 * RLIR 中 leaf:false 的分组父列（如 col_2021_monthly）只应出现在 columnGroups，
 * 若保留在 columns 会导致 ComplexReport 将其渲染为独立 rowspan 表头，1 月等子列错位。
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
      rowMerge: c.rowMerge ?? (c.field === "category"),
    })),
    wideTable,
    features: {
      ...layout.features,
      rowEmphasis: layout.features?.rowEmphasis ?? [
        { field: "indicator", includes: "利润总额" },
      ],
      rowDanger: layout.features?.rowDanger ?? [
        { field: "indicator", includes: "万元产值综合能耗" },
      ],
    },
  };
}

/** 来自 `资源/files/单一分析表2026.xlsx_575878bb/报表布局.json` */
export const financialReportLayout: ReportLayoutIR = normalizeReportLayout({
  title: layoutJson.title,
  summary: layoutJson.summary,
  columnGroups: layoutJson.columnGroups,
  wideTable: layoutJson.wideTable,
  columns: layoutJson.columns.map(mapColumn),
  features: {
    rowEmphasis: [{ field: "indicator", includes: "利润总额" }],
    rowDanger: [{ field: "indicator", includes: "万元产值综合能耗" }],
  },
});

/** @deprecated 保留旧示例名，指向财务指标表布局 */
export const demoReportLayout = financialReportLayout;
