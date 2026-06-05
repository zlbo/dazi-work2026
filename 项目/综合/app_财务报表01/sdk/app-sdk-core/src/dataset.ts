/**
 * 子应用与宿主之间的数据集统一封装。
 * 与 303 ExtensionDataset 形态一致，便于 DRAP 直接消费 Data Plane。
 */

export interface DaziAppDataset {
  columns: string[];
  data: Record<string, unknown>[];
  row_count?: number;
  meta?: {
    kind: string;
    ok: boolean;
    error?: string;
    fetched_at?: string;
  };
}

export interface DaziAppDatasetMap {
  [key: string]: DaziAppDataset;
}
