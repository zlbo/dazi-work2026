import type { DaziAppDataset } from "@dazi/app-sdk-core";

export const fixtureDatasets: Record<string, DaziAppDataset> = {
  alarms: {
    columns: ["level","source","message","time","status"],
    data: [{"level":"高","source":"产线A","message":"温度超限","time":"10:02","status":"未确认"},{"level":"中","source":"仓储","message":"库存低于安全线","time":"09:45","status":"处理中"}],
    row_count: 2,
    meta: { kind: "static", ok: true, fetched_at: new Date().toISOString() },
  },
};
