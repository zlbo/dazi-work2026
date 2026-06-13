import type { DaziAppDataset } from "@dazi/app-sdk-core";

export const fixtureDatasets: Record<string, DaziAppDataset> = {
  kpi: {
    columns: ["label","value","unit"],
    data: [{"label":"今日产量","value":12500,"unit":"件"},{"label":"计划达成","value":96.8,"unit":"%"},{"label":"一次合格率","value":99.1,"unit":"%"}],
    row_count: 3,
    meta: { kind: "static", ok: true, fetched_at: new Date().toISOString() },
  },
};
