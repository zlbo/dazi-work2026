import type { DaziAppDataset } from "@dazi/app-sdk-core";

export const fixtureDatasets: Record<string, DaziAppDataset> = {
  metrics: {
    columns: ["label","value","unit"],
    data: [{"label":"在线用户","value":1284,"unit":"人"},{"label":"TPS","value":342,"unit":"/s"},{"label":"错误率","value":0.12,"unit":"%"}],
    row_count: 3,
    meta: { kind: "static", ok: true, fetched_at: new Date().toISOString() },
  },
};
