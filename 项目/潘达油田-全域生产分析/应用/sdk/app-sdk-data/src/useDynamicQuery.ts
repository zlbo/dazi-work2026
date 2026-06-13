/**
 * 动态查询 hook：useSemanticQuery / useCubeQuery / useOntologyFunction / useSqlTemplate / useScriptEntry。
 *
 * 与 305 §5.3 / 303 §6 一一对应；
 * 内部统一调 bridge.invokeDynamicDataSource(decl)。
 *
 * P0 阶段宿主仅放通在 manifest.data_sources 已声明的 key；动态查询会被宿主校验拒绝。
 * P3（Phase D）：invokeDynamicDataSource 走 fetch-data-sources dynamic[]，kind 须在 policy 允许集内。
 */

import { useCallback, useEffect, useRef, useState } from "react";
import { useHostBridge } from "@dazi/app-sdk-runtime";
import type {
  DaziAppDataset,
  DaziAppDataSourceDecl,
} from "@dazi/app-sdk-core";
import type { UseDataResult } from "./types";

function useDynamicSource(
  decl: DaziAppDataSourceDecl,
  enabled = true,
): UseDataResult<DaziAppDataset> {
  const bridge = useHostBridge();
  const [data, setData] = useState<DaziAppDataset | undefined>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | undefined>();
  const mounted = useRef(true);
  const declRef = useRef(decl);
  declRef.current = decl;

  const run = useCallback(async () => {
    setLoading(true);
    setError(undefined);
    try {
      const next = await bridge.invokeDynamicDataSource(declRef.current);
      if (!mounted.current) return;
      setData(next);
      if (next.meta && !next.meta.ok) setError(next.meta.error);
    } catch (e) {
      if (!mounted.current) return;
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      if (mounted.current) setLoading(false);
    }
  }, [bridge]);

  useEffect(() => {
    mounted.current = true;
    if (enabled) void run();
    return () => {
      mounted.current = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [JSON.stringify(decl), enabled]);

  return { data, loading, error, refetch: run };
}

export function useOntologyFunction(args: {
  function_id: string;
  object_type_code: string;
  arguments?: Record<string, unknown>;
  key?: string;
  enabled?: boolean;
}): UseDataResult<DaziAppDataset> {
  const { enabled = true, key = args.function_id, ...rest } = args;
  return useDynamicSource(
    { key, kind: "ontology_function", ...rest },
    enabled,
  );
}

export function useSemanticQuery(args: {
  object_type_code: string;
  metric_request: {
    measures: string[];
    dimensions?: string[];
    filters?: unknown[];
  };
  key?: string;
  enabled?: boolean;
}): UseDataResult<DaziAppDataset> {
  const { enabled = true, key = `sem.${args.object_type_code}`, ...rest } = args;
  return useDynamicSource(
    { key, kind: "ontology_semantic", ...rest },
    enabled,
  );
}

export function useCubeQuery(args: {
  measures: string[];
  dimensions?: string[];
  segments?: string[];
  filters?: unknown[];
  limit?: number;
  key?: string;
  enabled?: boolean;
}): UseDataResult<DaziAppDataset> {
  const { enabled = true, key = `cube.${args.measures.join(",")}`, ...rest } =
    args;
  return useDynamicSource({ key, kind: "cube_query", ...rest }, enabled);
}

export function useSqlTemplate(args: {
  template_id: string;
  params?: Record<string, unknown>;
  key?: string;
  enabled?: boolean;
}): UseDataResult<DaziAppDataset> {
  const { enabled = true, key = `sql.${args.template_id}`, ...rest } = args;
  return useDynamicSource(
    { key, kind: "sql_template", arguments: rest.params, template_id: rest.template_id },
    enabled,
  );
}

export function useScriptEntry(args: {
  script_id: string;
  entry: string;
  arguments?: Record<string, unknown>;
  key?: string;
  enabled?: boolean;
}): UseDataResult<DaziAppDataset> {
  const { enabled = true, key = `script.${args.script_id}.${args.entry}`, ...rest } = args;
  return useDynamicSource({ key, kind: "script_entry", ...rest }, enabled);
}
