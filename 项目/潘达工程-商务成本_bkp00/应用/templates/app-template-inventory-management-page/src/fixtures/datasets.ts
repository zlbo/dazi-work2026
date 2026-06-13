import type { DaziAppDataset } from "@dazi/app-sdk-core";

export const fixtureDatasets: Record<string, DaziAppDataset> = {
  inventory: {
    columns: ["sku","name","qty","safety_stock","warehouse"],
    data: [{"sku":"SKU-001","name":"原料A","qty":520,"safety_stock":200,"warehouse":"WH-01"},{"sku":"SKU-002","name":"成品B","qty":88,"safety_stock":100,"warehouse":"WH-02"}],
    row_count: 2,
    meta: { kind: "static", ok: true, fetched_at: new Date().toISOString() },
  },
};
