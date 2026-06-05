/**
 * DRAP P4：iframe 沙箱内子应用宿主桥 shim（postMessage ↔ 父页 DaziAppIframeHost）。
 */

import {
  DRAP_CONTRACT,
  DRAP_HOST_BRIDGE_KEY,
  DRAP_HOST_READY_EVENT,
  type DrapContract,
  type DaziAppDataSourceDecl,
  type DaziAppDataset,
  type DaziAppManifest,
} from "@dazi/app-sdk-core";
import type { DaziAppHostBridge, DaziAppHostEvents } from "./hostBridge";

const DRAP_IFRAME_PROTOCOL = "drap-iframe-v1";

type RpcPending = {
  resolve: (v: unknown) => void;
  reject: (e: Error) => void;
};

const pendingRpc = new Map<string, RpcPending>();

function isInIframe(): boolean {
  try {
    return typeof window !== "undefined" && window.parent !== window;
  } catch {
    return true;
  }
}

function postToParent(msg: Record<string, unknown>) {
  window.parent.postMessage(
    { protocol: DRAP_IFRAME_PROTOCOL, ...msg },
    window.location.origin,
  );
}

function createProxyBridge(
  init: {
    appId: string;
    spaceId: string;
    appearance: "light" | "dark";
    manifest: DaziAppManifest;
    datasets: Record<string, DaziAppDataset>;
  },
): DaziAppHostBridge {
  let datasets = { ...init.datasets };
  let appearance = init.appearance;
  const listeners: Partial<{
    [K in keyof DaziAppHostEvents]: Set<(p: DaziAppHostEvents[K]) => void>;
  }> = {};

  const rpc = (method: string, args?: unknown[]): Promise<unknown> =>
    new Promise((resolve, reject) => {
      const id = `rpc-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
      pendingRpc.set(id, { resolve, reject });
      postToParent({ type: "drap-iframe-rpc", id, method, args });
      window.setTimeout(() => {
        if (pendingRpc.has(id)) {
          pendingRpc.delete(id);
          reject(new Error(`iframe RPC 超时: ${method}`));
        }
      }, 30_000);
    });

  const on: DaziAppHostBridge["on"] = (event, handler) => {
    const set = (listeners[event] ?? new Set()) as Set<typeof handler>;
    set.add(handler);
    listeners[event] = set;
    return () => set.delete(handler);
  };

  const bridge: DaziAppHostBridge = {
    contract: DRAP_CONTRACT as DrapContract,
    appId: init.appId,
    spaceId: init.spaceId,
    appearance,
    manifest: init.manifest,
    getInitialDatasets: () => ({ ...datasets }),
    async invokeDataSource(key, overrides) {
      const ds = (await rpc("invokeDataSource", [key, overrides])) as DaziAppDataset;
      return ds;
    },
    async invokeDynamicDataSource(decl) {
      return (await rpc("invokeDynamicDataSource", [decl])) as DaziAppDataset;
    },
    navigate(path) {
      void rpc("navigate", [path]);
    },
    back() {
      void rpc("back", []);
    },
    reportError(code, detail) {
      void rpc("reportError", [code, detail]);
    },
    on,
  };

  const handler = (ev: MessageEvent) => {
    if (ev.origin !== window.location.origin) return;
    const data = ev.data as Record<string, unknown>;
    if (data?.protocol !== DRAP_IFRAME_PROTOCOL) return;

    if (data.type === "drap-iframe-init") {
      appearance = (data.appearance as typeof appearance) || appearance;
      datasets = (data.datasets as typeof datasets) || datasets;
      if (data.manifest) bridge.manifest = data.manifest as DaziAppManifest;
      window.dispatchEvent(new Event(DRAP_HOST_READY_EVENT));
      return;
    }
    if (data.type === "drap-iframe-rpc-result" && typeof data.id === "string") {
      const p = pendingRpc.get(data.id);
      if (!p) return;
      pendingRpc.delete(data.id);
      if (data.error) p.reject(new Error(String(data.error)));
      else p.resolve(data.result);
      return;
    }
    if (data.type === "drap-iframe-event" && data.event === "appearanceChange") {
      appearance = data.payload as typeof appearance;
      const set = listeners.appearanceChange;
      if (set) for (const fn of set) fn(appearance);
      return;
    }
    if (data.type === "drap-iframe-event" && data.event === "datasetsRefreshed") {
      datasets = data.payload as typeof datasets;
      const set = listeners.datasetsRefreshed;
      if (set) for (const fn of set) fn(datasets);
    }
  };

  window.addEventListener("message", handler);
  return bridge;
}

let shimInstalled = false;

/** 在 iframe 子应用入口最早调用；成功则写入 window.__DAZI_APP_SDK__ */
export function tryInstallIframeBridgeShim(): boolean {
  if (shimInstalled || typeof window === "undefined") return shimInstalled;
  if (!isInIframe()) return false;

  const handler = (ev: MessageEvent) => {
    if (ev.origin !== window.location.origin) return;
    const data = ev.data as Record<string, unknown>;
    if (data?.protocol !== DRAP_IFRAME_PROTOCOL || data.type !== "drap-iframe-init") return;
    window.removeEventListener("message", handler);
    const bridge = createProxyBridge({
      appId: String(data.appId ?? ""),
      spaceId: String(data.spaceId ?? ""),
      appearance: (data.appearance as "light" | "dark") || "light",
      manifest: data.manifest as DaziAppManifest,
      datasets: (data.datasets as Record<string, DaziAppDataset>) || {},
    });
    window[DRAP_HOST_BRIDGE_KEY] = bridge;
    shimInstalled = true;
    window.dispatchEvent(new Event(DRAP_HOST_READY_EVENT));
  };

  window.addEventListener("message", handler);
  postToParent({ type: "drap-iframe-ready" });
  shimInstalled = true;
  return true;
}
