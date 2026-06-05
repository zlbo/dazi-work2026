/**
 * Hook 通用结果类型。
 */

import type { DaziAppDataset } from "@dazi/app-sdk-core";

export interface UseDataResult<T = DaziAppDataset> {
  data: T | undefined;
  loading: boolean;
  error?: string;
  /** 可选 overrides 走 dynamic fetch（与 manifest 声明 merge） */
  refetch(overrides?: Partial<import("@dazi/app-sdk-core").DaziAppDataSourceDecl>): Promise<void>;
}
