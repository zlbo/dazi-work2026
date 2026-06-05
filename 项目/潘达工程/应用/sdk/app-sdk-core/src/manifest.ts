/**
 * Manifest 类型（与 305 §4.1 字段对齐）。
 * P0 仅做类型约束，不内置运行时校验；P1 后端落 JSON Schema 校验。
 */

import type { DrapContract } from "./contract";

export type DaziAppMountType = "page" | "chat_result";
export type DaziAppSandbox = "shadow_dom" | "iframe";
export type DaziAppDataSourceKind =
  | "ontology_function"
  | "ontology_semantic"
  | "cube_query"
  | "sql_template"
  | "script_entry"
  | "static";

/** 与 303 §6 `data_sources[]` 同 schema */
export interface DaziAppDataSourceDecl {
  key: string;
  kind: DaziAppDataSourceKind;
  object_type_code?: string;
  function_id?: string;
  arguments?: Record<string, unknown>;
  metric_request?: {
    measures: string[];
    dimensions?: string[];
    filters?: unknown[];
  };
  measures?: string[];
  dimensions?: string[];
  segments?: string[];
  filters?: unknown[];
  template_id?: string;
  script_id?: string;
  entry?: string;
  source?: string;
  data?: { columns: string[]; rows: Record<string, unknown>[] };
  /** 宽表列投影（复杂报表 fetch 时传给 Data Plane） */
  project_columns?: string[];
  offset?: number;
  limit?: number;
}

/** manifest.report_design（337 复杂报表） */
export interface DaziAppReportDesign {
  managed_file_id?: string;
  display_name?: string;
  layout_source?: string;
  report_id?: string;
  layout_snapshot?: Record<string, unknown>;
  binding?: {
    datasets?: Record<
      string,
      {
        manifest_key?: string;
        rowKey?: string[];
        fieldMap?: Record<string, string>;
      }
    >;
    wideTable?: {
      strategy?: string;
      pageSize?: number;
      maxColumnsPerRequest?: number;
    };
  };
}

export interface DaziAppManifest {
  appId: string;
  name: string;
  description?: string;
  version: string;
  framework: { react: string; ts?: boolean };
  entry: string;
  styles?: string[];
  assets?: string[];
  routes?: string[];
  permissions: string[];
  data_sources?: DaziAppDataSourceDecl[];
  sdk: { min_version: string; contract: DrapContract };
  mount: { type: DaziAppMountType; sandbox: DaziAppSandbox };
  refresh?: { on_mount?: boolean; stale_ms?: number };
  ai?: {
    scene_tag?: string;
    industry?: string[];
    template_origin?: string;
  };
  report_design?: DaziAppReportDesign;
}
