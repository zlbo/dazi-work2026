/**
 * 复杂报表数据集：按可见列 + 分页取数。
 * - static：仅在子应用内对宿主注入数据做本地投影，不 POST fetch-data-sources
 * - 其他 kind：invokeDataSource + project_columns/offset/limit
 */

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useHostBridge } from "@dazi/app-sdk-runtime";
import type { DaziAppDataset, DaziAppReportDesign } from "@dazi/app-sdk-core";
import { applyDatasetProjection } from "./applyDatasetProjection";
import { resolveStaticDatasetFromManifest } from "./resolveStaticDataset";
import { useDataset } from "./useDataset";
import type { UseDataResult } from "./types";

export interface UseReportDatasetOptions {
  dataKey?: string;
  visibleFields: string[];
  page?: number;
  pageSize?: number;
  wideTable?: { pageSize?: number; maxColumnsPerRequest?: number };
}

function fieldsSignature(fields: string[]): string {
  return fields.filter(Boolean).join("\0");
}

export function useReportDataset(
  opts: UseReportDatasetOptions,
): UseDataResult<DaziAppDataset> & { page: number; setPage: (p: number) => void; pageSize: number } {
  const key = opts.dataKey ?? "report_data";
  const bridge = useHostBridge();
  const base = useDataset(key);
  const [page, setPage] = useState(opts.page ?? 1);
  const [projected, setProjected] = useState<DaziAppDataset | undefined>();
  const prevFieldsKey = useRef("");

  const binding = useMemo(() => {
    const rd = bridge.manifest.report_design as DaziAppReportDesign | undefined;
    return rd?.binding;
  }, [bridge.manifest]);

  const pageSize = useMemo(() => {
    const wt = binding?.wideTable ?? opts.wideTable;
    return opts.pageSize ?? wt?.pageSize ?? 200;
  }, [binding, opts.wideTable, opts.pageSize]);

  const maxCols = binding?.wideTable?.maxColumnsPerRequest ?? 40;

  const fieldsKey = useMemo(
    () => fieldsSignature(opts.visibleFields),
    [opts.visibleFields],
  );

  const projectColumns = useMemo(() => {
    const fields = fieldsKey ? fieldsKey.split("\0") : [];
    if (!fields.length) return undefined;
    return fields.slice(0, maxCols);
  }, [fieldsKey, maxCols]);

  const isStatic = useMemo(() => {
    const decl = bridge.manifest.data_sources?.find((d) => d.key === key);
    return decl?.kind === "static";
  }, [bridge.manifest, key]);

  const runFetch = useCallback(
    async (force = false) => {
      const offset = (page - 1) * pageSize;
      const overrides = {
        project_columns: projectColumns,
        offset,
        limit: pageSize,
      };

      if (isStatic) {
        let raw = bridge.getInitialDatasets()[key] ?? base.data;
        if (!raw?.data?.length) {
          raw = resolveStaticDatasetFromManifest(bridge.manifest, key);
        }
        if (!raw?.data?.length) return;
        setProjected(
          applyDatasetProjection(raw, { key, kind: "static", ...overrides }),
        );
        return;
      }

      if (!force) return;
      await base.refetch(overrides as Parameters<typeof base.refetch>[0]);
      setProjected(undefined);
    },
    [base.refetch, base.data, bridge, isStatic, key, page, pageSize, projectColumns],
  );

  useEffect(() => {
    if (prevFieldsKey.current !== fieldsKey && prevFieldsKey.current !== "") {
      setPage(1);
    }
    prevFieldsKey.current = fieldsKey;
  }, [fieldsKey]);

  useEffect(() => {
    void runFetch(true);
  }, [fieldsKey, page, pageSize, isStatic, key, projectColumns]);

  const data =
    isStatic && projected
      ? projected
      : base.data ?? resolveStaticDatasetFromManifest(bridge.manifest, key);

  return {
    data,
    loading: isStatic ? false : base.loading,
    error: base.error,
    refetch: () => runFetch(true),
    page,
    setPage,
    pageSize,
  };
}
