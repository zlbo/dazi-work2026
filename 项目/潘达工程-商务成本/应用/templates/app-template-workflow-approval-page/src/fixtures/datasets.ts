import type { DaziAppDataset } from "@dazi/app-sdk-core";

export const fixtureDatasets: Record<string, DaziAppDataset> = {
  todos: {
    columns: ["id","title","applicant","status","submitted_at"],
    data: [{"id":"AP-001","title":"差旅报销","applicant":"张三","status":"待审","submitted_at":"2026-05-20"},{"id":"AP-002","title":"采购申请","applicant":"李四","status":"待审","submitted_at":"2026-05-21"}],
    row_count: 2,
    meta: { kind: "static", ok: true, fetched_at: new Date().toISOString() },
  },
};
