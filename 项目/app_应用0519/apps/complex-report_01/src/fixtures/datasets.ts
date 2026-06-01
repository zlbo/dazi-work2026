import type { DaziAppDataset } from "@dazi/app-sdk-core";
import reportRows from "./generated/reportRows.json";
import { financialReportLayout } from "./reportLayout";

const columns = financialReportLayout.columns
  ?.filter((c) => c.leaf !== false)
  .map((c) => c.field) ?? [];

export const fixtureDatasets: Record<string, DaziAppDataset> = {
  report_data: {
    columns,
    data: reportRows as Record<string, unknown>[],
    row_count: reportRows.length,
    meta: {
      kind: "static",
      ok: true,
      fetched_at: new Date().toISOString(),
    },
  },
};
