/**
 * dev / 兜底用 mock 数据，与 manifest.data_sources[].key 对齐。
 */

import type { DaziAppDataset } from "@dazi/app-sdk-core";

export const fixtureDatasets: Record<string, DaziAppDataset> = {
  kpi: {
    columns: ["revenue", "profit", "profit_rate"],
    data: [{ revenue: 12_500_000, profit: 2_300_000, profit_rate: 18.4 }],
    row_count: 1,
    meta: { kind: "ontology_semantic", ok: true, fetched_at: new Date().toISOString() },
  },
  trend: {
    columns: ["month", "revenue", "profit"],
    data: [
      { month: "2026-01", revenue: 9_800_000, profit: 1_650_000 },
      { month: "2026-02", revenue: 10_300_000, profit: 1_780_000 },
      { month: "2026-03", revenue: 11_100_000, profit: 1_920_000 },
      { month: "2026-04", revenue: 11_700_000, profit: 2_050_000 },
      { month: "2026-05", revenue: 12_500_000, profit: 2_300_000 },
    ],
    row_count: 5,
    meta: { kind: "ontology_function", ok: true, fetched_at: new Date().toISOString() },
  },
  yoy_table: {
    columns: ["维度", "本期", "上期", "同比%"],
    data: [
      { 维度: "营收", 本期: 12_500_000, 上期: 10_900_000, "同比%": 14.7 },
      { 维度: "利润", 本期: 2_300_000, 上期: 1_870_000, "同比%": 23.0 },
      { 维度: "利润率", 本期: 18.4, 上期: 17.2, "同比%": 7.0 },
    ],
    row_count: 3,
    meta: { kind: "static", ok: true },
  },
};
