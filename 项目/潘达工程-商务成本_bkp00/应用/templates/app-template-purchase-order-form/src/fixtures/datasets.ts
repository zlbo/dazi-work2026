import type { DaziAppDataset } from "@dazi/app-sdk-core";

export const fixtureDatasets: Record<string, DaziAppDataset> = {
  form: {
    columns: ["field", "value"],
    data: [],
    row_count: 0,
    meta: { kind: "static", ok: true, fetched_at: new Date().toISOString() },
  },
};
