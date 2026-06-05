/**
 * FC02 本体 / Cube 数据集 → 看板 UI 字段映射。
 * B1 函数返回 actual_total / budget_total / achievement_rate；
 * Cube 趋势返回 cube_fin_cockpit02_profit.year_month / .amount。
 */

import type { DaziAppDataset } from "@dazi/app-sdk-core";

function num(v: unknown): number {
  const n = Number(v ?? 0);
  return Number.isFinite(n) ? n : 0;
}

/** 单行 KPI（ontology_function fc02.fn.month_pl_budget_kpi） */
export function parseFc02KpiRow(row: Record<string, unknown>) {
  if (row.revenue != null || row.profit != null) {
    return {
      revenue: num(row.revenue),
      profit: num(row.profit),
      profitRate: num(row.profit_rate),
    };
  }
  const actual = num(row.actual_total);
  const budget = num(row.budget_total);
  const rateRaw = row.achievement_rate;
  const rateNum = rateRaw != null && rateRaw !== "" ? num(rateRaw) : NaN;
  const profitRate = Number.isFinite(rateNum)
    ? Math.abs(rateNum) <= 2
      ? rateNum * 100
      : rateNum
    : budget !== 0
      ? (actual / budget) * 100
      : 0;
  return {
    revenue: Math.abs(budget),
    profit: Math.abs(actual),
    profitRate: Number.isFinite(profitRate) ? profitRate : 0,
  };
}

const PROFIT_YM = "cube_fin_cockpit02_profit.year_month";
const PROFIT_AMT = "cube_fin_cockpit02_profit.amount";
function monthKey(row: Record<string, unknown>): string {
  return String(row.month ?? row.year_month ?? row[PROFIT_YM] ?? "");
}

function amountKey(row: Record<string, unknown>, ...keys: string[]): number {
  for (const k of keys) {
    if (row[k] != null) return Math.abs(num(row[k]));
  }
  return 0;
}

/** Cube 利润按月 → TrendChart（month / profit） */
export function buildTrendChartDataset(
  profitDs: DaziAppDataset | undefined,
): DaziAppDataset | undefined {
  const profitRows = profitDs?.data ?? [];
  if (!profitRows.length) return profitDs;

  const rows = profitRows.map((r) => {
    const m = monthKey(r);
    const profit = amountKey(r, PROFIT_AMT, "amount", "profit");
    return { month: m, profit };
  });

  rows.sort((a, b) => String(a.month).localeCompare(String(b.month)));

  return {
    columns: ["month", "profit"],
    data: rows,
    row_count: rows.length,
    meta: profitDs?.meta ?? { kind: "cube_query", ok: true },
  };
}

/** 由趋势数据生成简易同环比表（仅利润一行有数时其余仍可读） */
export function buildYoyTableFromTrend(
  trend: DaziAppDataset | undefined,
): DaziAppDataset | undefined {
  const rows = trend?.data ?? [];
  if (rows.length < 2) return undefined;
  const sorted = [...rows].sort((a, b) =>
    String(a.month).localeCompare(String(b.month)),
  );
  const cur = sorted[sorted.length - 1];
  const prev = sorted[sorted.length - 2];
  const pct = (c: number, p: number) =>
    p !== 0 ? ((c - p) / Math.abs(p)) * 100 : 0;

  const mk = (dim: string, c: number, p: number) => ({
    维度: dim,
    本期: c,
    上期: p,
    "同比%": Number(pct(c, p).toFixed(2)),
  });

  const data = [
    mk("利润", num(cur.profit), num(prev.profit)),
  ];

  return {
    columns: ["维度", "本期", "上期", "同比%"],
    data,
    row_count: data.length,
    meta: { kind: "derived", ok: true },
  };
}
