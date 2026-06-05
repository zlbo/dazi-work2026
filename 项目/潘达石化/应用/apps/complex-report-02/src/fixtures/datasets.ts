import type { DaziAppDataset } from "@dazi/app-sdk-core";

export const fixtureDatasets: Record<string, DaziAppDataset> = {
  table: {
    columns: ["work_order","line","qty","yield_pct","shift"],
    data: [{"work_order":"WO-1001","line":"产线A","qty":1200,"yield_pct":98.2,"shift":"白班"},{"work_order":"WO-1002","line":"产线B","qty":980,"yield_pct":96.5,"shift":"夜班"}],
    row_count: 2,
    meta: { kind: "static", ok: true, fetched_at: new Date().toISOString() },
  },
};
