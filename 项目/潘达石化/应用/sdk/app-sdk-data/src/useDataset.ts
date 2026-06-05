/**
 * useDataset：按 manifest.data_sources[].key 取宿主预拉好的数据集，并提供 refetch。
 *
 * P0 实现：
 *   - 初始值直接从 bridge.getInitialDatasets() 拿
 *   - refetch 调 bridge.invokeDataSource(key)
 */

import { useCallback, useEffect, useRef, useState } from "react";
import { useHostBridge } from "@dazi/app-sdk-runtime";
import type { DaziAppDataset } from "@dazi/app-sdk-core";
import { applyDatasetProjection } from "./applyDatasetProjection";
import type { UseDataResult } from "./types";

export function useDataset(key: string): UseDataResult<DaziAppDataset> {
  const bridge = useHostBridge();
  const initial = bridge.getInitialDatasets()[key];
  const [data, setData] = useState<DaziAppDataset | undefined>(initial);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | undefined>(
    initial?.meta && !initial.meta.ok ? initial.meta.error : undefined,
  );
  const mounted = useRef(true);

  const refetch = useCallback(async (overrides?: Partial<import("@dazi/app-sdk-core").DaziAppDataSourceDecl>) => {
    const decl = bridge.manifest.data_sources?.find((d) => d.key === key);
    const hasOverrides = overrides && Object.keys(overrides).length > 0;
    if (decl?.kind === "static" && hasOverrides) {
      const raw = bridge.getInitialDatasets()[key] ?? data;
      if (raw?.data?.length) {
        setData(
          applyDatasetProjection(raw, {
            ...(decl ?? { key, kind: "static" as const }),
            ...overrides,
            key,
          }),
        );
        return;
      }
    }

    setLoading(true);
    setError(undefined);
    try {
      const next = await bridge.invokeDataSource(key, overrides);
      if (!mounted.current) return;
      setData(next);
      if (next.meta && !next.meta.ok) setError(next.meta.error);
    } catch (e) {
      if (!mounted.current) return;
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      if (mounted.current) setLoading(false);
    }
  }, [bridge, key]);

  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);

  useEffect(() => {
    const off = bridge.on("datasetsRefreshed", (all) => {
      const next = all[key];
      if (next) {
        setData(next);
        setError(next.meta && !next.meta.ok ? next.meta.error : undefined);
      }
    });
    return off;
  }, [bridge, key]);

  useEffect(() => {
    if (bridge.manifest.refresh?.on_mount === false) return;
    // 宿主已注入且含行数据时（如 chat_result 的 message），不再 on_mount 重复拉取
    const pre = bridge.getInitialDatasets()[key];
    if (pre?.data?.length) return;
    const decl = bridge.manifest.data_sources?.find((d) => d.key === key);
    // static 复杂报表由 useReportDataset 本地投影，避免 on_mount 再拉一次
    if (decl?.kind === "static" && bridge.manifest.report_design) return;
    void refetch();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key]);

  return { data, loading, error, refetch };
}
