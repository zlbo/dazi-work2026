/**
 * dev-shim：模板独立 `pnpm dev` 时使用，向 window 注入一个本地宿主桥 mock。
 *
 * 与生产 DaziAppHost 注入的真桥行为对齐：
 *   - 提供 manifest / spaceId / appearance
 *   - getInitialDatasets() / invokeDataSource() 直接从 fixtures 取数
 *   - 不接入真实后端
 *
 * 模板的 dev-entry 第一步必须调 installDevHostBridge()，再 import lifecycle 并调 mount。
 */

import {
  DRAP_CONTRACT,
  DRAP_HOST_BRIDGE_KEY,
  DRAP_HOST_READY_EVENT,
  type DaziAppDataSourceDecl,
  type DaziAppDataset,
  type DaziAppManifest,
} from "@dazi/app-sdk-core";
import type {
  Appearance,
  DaziAppHostBridge,
  DaziAppHostEvents,
} from "./hostBridge";

export interface DevHostBridgeOptions {
  appId: string;
  spaceId: string;
  appearance?: Appearance;
  manifest: DaziAppManifest;
  datasets: Record<string, DaziAppDataset>;
  onNavigate?: (path: string) => void;
}

type Listener<K extends keyof DaziAppHostEvents> = (
  payload: DaziAppHostEvents[K],
) => void;

export function installDevHostBridge(opts: DevHostBridgeOptions): void {
  if (typeof window === "undefined") return;
  const listeners: { [K in keyof DaziAppHostEvents]?: Set<Listener<K>> } = {};

  const on: DaziAppHostBridge["on"] = (event, handler) => {
    const set = (listeners[event] ?? new Set()) as Set<typeof handler>;
    set.add(handler);
    (listeners as Record<string, Set<unknown>>)[event] = set;
    return () => set.delete(handler);
  };

  const bridge: DaziAppHostBridge = {
    contract: DRAP_CONTRACT,
    appId: opts.appId,
    spaceId: opts.spaceId,
    appearance: opts.appearance ?? "light",
    manifest: opts.manifest,
    getInitialDatasets: () => ({ ...opts.datasets }),
    async invokeDataSource(key, _overrides) {
      const ds = opts.datasets[key];
      if (!ds) {
        return {
          columns: [],
          data: [],
          meta: { kind: "unknown", ok: false, error: `dev fixture 缺少 key=${key}` },
        };
      }
      return ds;
    },
    async invokeDynamicDataSource(decl: DaziAppDataSourceDecl) {
      console.warn("[dev-shim] invokeDynamicDataSource called", decl);
      return {
        columns: [],
        data: [],
        meta: {
          kind: decl.kind,
          ok: false,
          error: "dev-shim 不支持动态数据源；请在 fixtures 中提供 mock",
        },
      };
    },
    navigate: (path) => {
      console.info("[dev-shim] navigate ->", path);
      opts.onNavigate?.(path);
    },
    back: () => {
      console.info("[dev-shim] back()");
      history.back();
    },
    reportError: (code, detail) => {
      console.error("[dev-shim] reportError", code, detail);
    },
    on,
  };

  window[DRAP_HOST_BRIDGE_KEY] = bridge;
  window.dispatchEvent(new Event(DRAP_HOST_READY_EVENT));
}
