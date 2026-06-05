import type { DaziAppDataSourceDecl, DaziAppDataset } from "@dazi/app-sdk-core";

/** 与后端 data_plane._apply_dataset_projection 对齐的前端裁剪（static 等本地数据用） */
export function applyDatasetProjection(
  ds: DaziAppDataset,
  decl: Partial<DaziAppDataSourceDecl>,
): DaziAppDataset {
  const meta = ds.meta ?? { kind: "unknown", ok: true };
  if (meta.ok === false) return ds;

  let columns = [...(ds.columns ?? [])];
  let rows = (ds.data ?? []).map((r) => ({ ...r }));

  const rawProj = decl.project_columns;
  let wanted: string[] = [];
  if (Array.isArray(rawProj) && rawProj.length) {
    wanted = rawProj.map((c) => String(c).trim()).filter(Boolean);
    if (wanted.length) {
      columns = wanted;
      rows = rows.map((r) => {
        const row = r as Record<string, unknown>;
        const out: Record<string, unknown> = {};
        for (const k of wanted) out[k] = row[k];
        return out;
      });
    }
  }

  const off = Math.max(0, Number(decl.offset) || 0);
  if (off > 0) rows = rows.slice(off);

  const lim = decl.limit;
  if (lim != null) {
    const n = Number(lim);
    if (n > 0) rows = rows.slice(0, n);
  }

  const extra: Record<string, unknown> = {};
  if (rawProj || decl.offset != null || decl.limit != null) {
    extra.projected = true;
    if (wanted.length) extra.project_columns = wanted;
  }

  return {
    columns,
    data: rows,
    row_count: rows.length,
    meta: { ...meta, ...extra },
  };
}
