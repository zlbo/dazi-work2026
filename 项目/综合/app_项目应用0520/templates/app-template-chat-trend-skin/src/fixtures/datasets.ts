import type { DaziAppDataset } from "@dazi/app-sdk-core";

/** dev / 页模式预览 mock */
export const fixtureDatasets: Record<string, DaziAppDataset> = {
  message: {
    columns: ["month", "revenue", "profit"],
    data: [
      { month: "1月", revenue: 980000, profit: 120000 },
      { month: "2月", revenue: 1020000, profit: 135000 },
      { month: "3月", revenue: 1100000, profit: 148000 },
    ],
    row_count: 3,
    meta: { kind: "static", ok: true, fetched_at: new Date().toISOString() },
  },
  trend: {
    columns: ["month", "revenue", "profit"],
    data: [
      { month: "1月", revenue: 980000, profit: 120000 },
      { month: "2月", revenue: 1020000, profit: 135000 },
      { month: "3月", revenue: 1100000, profit: 148000 },
    ],
    row_count: 3,
    meta: { kind: "static", ok: true, fetched_at: new Date().toISOString() },
  },
};
