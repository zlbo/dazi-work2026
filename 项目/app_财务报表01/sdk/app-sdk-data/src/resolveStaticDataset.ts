import type { DaziAppDataset, DaziAppManifest } from "@dazi/app-sdk-core";

/** manifest.data_sources 内联 static 数据 → 标准 Dataset */
export function resolveStaticDatasetFromManifest(
  manifest: DaziAppManifest,
  key: string,
): DaziAppDataset | undefined {
  const decl = manifest.data_sources?.find((d) => d.key === key);
  if (!decl || decl.kind !== "static" || !decl.data) return undefined;
  const rows = decl.data.rows ?? [];
  if (!rows.length) return undefined;
  const columns =
    decl.data.columns?.length
      ? decl.data.columns
      : rows[0]
        ? Object.keys(rows[0] as object)
        : [];
  return {
    columns,
    data: rows,
    row_count: rows.length,
    meta: { kind: "static", ok: true },
  };
}

export function datasetHasRows(ds?: DaziAppDataset): boolean {
  return Boolean(ds?.data?.length);
}
