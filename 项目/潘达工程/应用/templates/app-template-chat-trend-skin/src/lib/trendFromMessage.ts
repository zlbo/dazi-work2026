/** 从问数 message 表推断趋势图 x 轴与 y 序列 */

function isNumeric(v: unknown): boolean {
  if (v == null || v === "") return false;
  const n = Number(v);
  return Number.isFinite(n);
}

function looksLikeCategory(col: string, sample: unknown): boolean {
  if (typeof sample === "string" && sample.length > 0 && !isNumeric(sample)) {
    return true;
  }
  const lower = col.toLowerCase();
  return (
    lower.includes("month") ||
    lower.includes("date") ||
    lower.includes("year") ||
    lower.includes("period") ||
    lower.includes("name") ||
    lower.includes("label") ||
    lower === "id"
  );
}

export function inferTrendAxes(
  columns: string[],
  rows: Record<string, unknown>[],
): { xKey: string; yKeys: string[] } | null {
  if (!columns.length || !rows.length) return null;

  const sample = rows[0];
  let xKey = columns.find((c) => looksLikeCategory(c, sample[c]));
  if (!xKey) xKey = columns[0];

  const yKeys = columns.filter(
    (c) => c !== xKey && rows.some((r) => isNumeric(r[c])),
  );
  if (!yKeys.length) return null;

  return { xKey, yKeys: yKeys.slice(0, 3) };
}
