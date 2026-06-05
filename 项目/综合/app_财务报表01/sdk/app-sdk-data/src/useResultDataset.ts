/**
 * 问数/页模式通用结果集：优先宿主注入的 `message`，否则回退 manifest 其它数据源或内联 static 预览数据。
 */

import { useEffect, useMemo, useState } from "react";
import { useHostBridge } from "@dazi/app-sdk-runtime";
import type { DaziAppDataset } from "@dazi/app-sdk-core";
import type { UseDataResult } from "./types";
import {
  datasetHasRows,
  resolveStaticDatasetFromManifest,
} from "./resolveStaticDataset";
import { useDataset } from "./useDataset";

export interface UseResultDatasetOptions {
  /** 优先尝试的回退 key（在 manifest 其它 data_sources 之前） */
  fallbackKeys?: string[];
  /** 主键，默认 message */
  primaryKey?: string;
}

export interface UseResultDatasetResult extends UseDataResult<DaziAppDataset> {
  /** 实际使用的 data_sources key */
  sourceKey: string;
  /** true 表示来自 message 以外的预览/声明数据源 */
  isPreview: boolean;
}

export function useResultDataset(
  options: UseResultDatasetOptions = {},
): UseResultDatasetResult {
  const primaryKey = options.primaryKey ?? "message";
  const bridge = useHostBridge();
  const primary = useDataset(primaryKey);
  const [fallbackMap, setFallbackMap] = useState<
    Record<string, DaziAppDataset>
  >({});

  const candidateKeys = useMemo(() => {
    const fromManifest = (bridge.manifest.data_sources ?? [])
      .map((d) => d.key)
      .filter((k): k is string => Boolean(k && k !== primaryKey));
    return [...new Set([...(options.fallbackKeys ?? []), ...fromManifest])];
  }, [bridge.manifest, options.fallbackKeys, primaryKey]);

  const inlinePrimary = useMemo(
    () => resolveStaticDatasetFromManifest(bridge.manifest, primaryKey),
    [bridge.manifest, primaryKey],
  );

  useEffect(() => {
    if (primary.loading) return;
    if (datasetHasRows(primary.data)) return;

    let cancelled = false;
    (async () => {
      const next: Record<string, DaziAppDataset> = {};
      for (const k of candidateKeys) {
        const initial = bridge.getInitialDatasets()[k];
        if (datasetHasRows(initial)) {
          next[k] = initial!;
          continue;
        }
        const inline = resolveStaticDatasetFromManifest(bridge.manifest, k);
        if (inline) {
          next[k] = inline;
          continue;
        }
        try {
          const ds = await bridge.invokeDataSource(k);
          if (datasetHasRows(ds)) next[k] = ds;
        } catch {
          /* 单 key 失败不影响其它回退 */
        }
      }
      if (!cancelled && Object.keys(next).length) {
        setFallbackMap((prev) => ({ ...prev, ...next }));
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [
    primary.loading,
    primary.data,
    candidateKeys,
    bridge,
    primaryKey,
  ]);

  const resolved = useMemo(() => {
    if (datasetHasRows(primary.data)) {
      return {
        data: primary.data,
        loading: primary.loading,
        error: primary.error,
        sourceKey: primaryKey,
        isPreview: false,
      };
    }
    if (datasetHasRows(inlinePrimary)) {
      return {
        data: inlinePrimary,
        loading: primary.loading,
        error: undefined,
        sourceKey: primaryKey,
        isPreview: true,
      };
    }
    for (const k of candidateKeys) {
      const ds = fallbackMap[k] ?? bridge.getInitialDatasets()[k];
      if (datasetHasRows(ds)) {
        return {
          data: ds,
          loading: primary.loading,
          error: undefined,
          sourceKey: k,
          isPreview: true,
        };
      }
    }
    return {
      data: primary.data,
      loading: primary.loading,
      error: primary.error,
      sourceKey: primaryKey,
      isPreview: false,
    };
  }, [
    primary.data,
    primary.loading,
    primary.error,
    inlinePrimary,
    candidateKeys,
    fallbackMap,
    bridge,
    primaryKey,
  ]);

  return {
    ...resolved,
    refetch: primary.refetch,
  };
}
