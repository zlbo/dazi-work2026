import {
  getHostBridge,
  waitForHostBridge,
  findMicroAppNameFromContainer,
  tryInstallIframeBridgeShim,
  type DaziAppProps,
} from "@dazi/app-sdk-runtime";

tryInstallIframeBridgeShim();
import {
  DRAP_HOST_BRIDGE_KEY,
  DRAP_HOST_BRIDGE_REGISTRY_KEY,
  type DaziAppManifest,
} from "@dazi/app-sdk-core";
import manifestJson from "../manifest.json";
import { fixtureDatasets } from "./fixtures/datasets";
import type { DaziAppLifecycle } from "@dazi/app-sdk-runtime";

const manifest = manifestJson as DaziAppManifest;

declare global {
  interface Window {
    __MICRO_APP_NAME__?: string;
    mount?: (data?: Record<string, unknown>) => void | Promise<void>;
    unmount?: (data?: Record<string, unknown>) => void | Promise<void>;
  }
}

function readMicroAppName(): string | undefined {
  return window.__MICRO_APP_NAME__?.trim() || undefined;
}

function findDrapRoot(): HTMLElement | null {
  const scopeName = readMicroAppName();
  if (scopeName) {
    const ma = document.querySelector(`micro-app[name="${scopeName}"]`);
    if (ma) {
      const sr = (ma as HTMLElement & { shadowRoot?: ShadowRoot | null }).shadowRoot;
      if (sr) {
        const inShadow = sr.getElementById("drap-root");
        if (inShadow) return inShadow;
      }
      const inLight = ma.querySelector("#drap-root");
      if (inLight) return inLight as HTMLElement;
    }
  }
  return document.getElementById("drap-root");
}

async function waitForRoot(timeoutMs = 8_000): Promise<HTMLElement> {
  const t0 = Date.now();
  while (Date.now() - t0 < timeoutMs) {
    const el = findDrapRoot();
    if (el) return el;
    await new Promise((r) => setTimeout(r, 30));
  }
  throw new Error(`[DRAP] 缺少 #drap-root（micro-app=${readMicroAppName() ?? "?"}）`);
}

function hostBridgeReady(): boolean {
  const reg = window[DRAP_HOST_BRIDGE_REGISTRY_KEY];
  const scope = readMicroAppName();
  if (scope && reg?.[scope]) return true;
  return Boolean(window[DRAP_HOST_BRIDGE_KEY]);
}

function buildMountProps(data?: Record<string, unknown>): DaziAppProps {
  const scope = readMicroAppName();
  if (hostBridgeReady()) {
    try {
      const bridge = getHostBridge(scope);
      return {
        appId: bridge.appId,
        spaceId: bridge.spaceId,
        appearance: bridge.appearance,
        manifest: bridge.manifest,
        datasets: bridge.getInitialDatasets(),
      };
    } catch {
      /* fallback */
    }
  }
  return {
    appId: (data?.appId as string) || manifest.appId,
    spaceId: (data?.spaceId as string) || "space__panda_construction",
    appearance: (data?.appearance as DaziAppProps["appearance"]) || "light",
    manifest,
    datasets: fixtureDatasets,
  };
}

let lifecyclePromise: Promise<DaziAppLifecycle> | null = null;

function getLifecycle(): Promise<DaziAppLifecycle> {
  if (!lifecyclePromise) {
    lifecyclePromise = import("./index").then((m) => m.default);
  }
  return lifecyclePromise;
}

window.mount = async (data?: Record<string, unknown>) => {
  const scope = readMicroAppName();
  if (!hostBridgeReady()) {
    await waitForHostBridge(8_000, scope);
  }
  const lc = await getLifecycle();
  const container = await waitForRoot();
  await lc.mount(container, buildMountProps(data));
};

window.unmount = async () => {
  const lc = await getLifecycle();
  const container = findDrapRoot();
  if (!container) return;
  void findMicroAppNameFromContainer(container);
  await lc.unmount(container);
};
