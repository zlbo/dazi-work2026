/**
 * 从问数 message 数据集首行抽取 KPI 卡片（通用数值列，最多 4 项）。
 */

const SKIP_KEYS = new Set([
  "id",
  "uuid",
  "row_id",
  "created_at",
  "updated_at",
  "year_month",
  "version_id",
]);

export interface KpiCardItem {
  key: string;
  title: string;
  value: string;
  hint?: string;
}

function humanizeColumn(key: string): string {
  const known: Record<string, string> = {
    actual_total: "实际",
    budget_total: "预算",
    achievement_rate: "达成率",
    revenue: "营收",
    profit: "利润",
    profit_rate: "利润率",
    amount: "金额",
    total: "合计",
    count: "数量",
  };
  if (known[key]) return known[key];
  return key.replace(/_/g, " ");
}

function isNumericValue(v: unknown): boolean {
  if (typeof v === "number" && Number.isFinite(v)) return true;
  if (typeof v === "string" && v.trim() !== "" && !Number.isNaN(Number(v))) return true;
  return false;
}

function toNumber(v: unknown): number {
  return typeof v === "number" ? v : Number(v);
}

export function fmtKpiValue(key: string, raw: unknown): string {
  const n = toNumber(raw);
  if (!Number.isFinite(n)) return "—";
  const lk = key.toLowerCase();
  if (lk.includes("rate") || lk.includes("ratio") || lk.endsWith("_pct") || key.includes("率")) {
    const pct = Math.abs(n) <= 1 ? n * 100 : n;
    return `${pct.toFixed(1)}%`;
  }
  if (Math.abs(n) >= 10_000) return `${(n / 10_000).toFixed(1)} 万`;
  if (Math.abs(n) >= 1_000) return n.toLocaleString("zh-CN", { maximumFractionDigits: 0 });
  return n.toLocaleString("zh-CN", { maximumFractionDigits: 2 });
}

export function extractKpiCards(
  row: Record<string, unknown>,
  columns: string[],
  maxCards = 4,
): KpiCardItem[] {
  const ordered =
    columns.length > 0
      ? columns
      : Object.keys(row).filter((k) => !SKIP_KEYS.has(k));

  const items: KpiCardItem[] = [];
  for (const key of ordered) {
    if (SKIP_KEYS.has(key)) continue;
    const v = row[key];
    if (!isNumericValue(v)) continue;
    items.push({
      key,
      title: humanizeColumn(key),
      value: fmtKpiValue(key, v),
      hint: key,
    });
    if (items.length >= maxCards) break;
  }
  return items;
}
