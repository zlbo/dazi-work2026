import type { DaziAppDataset } from "@dazi/app-sdk-core";

/** dev / 无宿主桥时的 message mock */
export const fixtureDatasets: Record<string, DaziAppDataset> = {
  message: {
    columns: ["budget_total", "actual_total", "achievement_rate"],
    data: [
      {
        budget_total: 12_500_000,
        actual_total: 10_625_000,
        achievement_rate: 85.0,
      },
    ],
    row_count: 1,
    meta: { kind: "static", ok: true, fetched_at: new Date().toISOString() },
  },
};
