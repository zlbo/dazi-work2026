import type { DaziAppDataset } from "@dazi/app-sdk-core";

export const fixtureDatasets: Record<string, DaziAppDataset> = {
  metrics: {
    columns: ["label","value","unit","status"],
    data: [{"label":"OEE","value":87.3,"unit":"%","status":"正常"},{"label":"运行设备","value":42,"unit":"台","status":"正常"},{"label":"告警","value":3,"unit":"条","status":"关注"}],
    row_count: 3,
    meta: { kind: "static", ok: true, fetched_at: new Date().toISOString() },
  },
};
