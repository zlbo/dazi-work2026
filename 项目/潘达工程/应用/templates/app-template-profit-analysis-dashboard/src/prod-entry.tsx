/**
 * 生产入口（micro-app 加载 dist/index.html 时执行）。
 *
 * 禁止自动 bootstrap：多消息同时存在多个 <micro-app name="drap-profit-analysis-xxx">，
 * 若脚本加载时自行 mount 到「第一个」容器，其余消息永远空白。
 *
 * 仅向 window 注册 mount/unmount，由 micro-app 在 umd 模式下按实例调用；
 * 容器与宿主桥均按 window.__MICRO_APP_NAME__ 精确匹配。
 */

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
  const n = window.__MICRO_APP_NAME__?.trim();
  return n || undefined;
}

/** 当前 micro-app 实例内的 #drap-root */
function findDrapRoot(): HTMLElement | null {
  const scopeName = readMicroAppName();
  if (scopeName) {
    const ma = document.querySelector(`micro-app[name="${scopeName}"]`);
    if (ma) {
      const sr = (ma as HTMLElement & { shadowRoot?: ShadowRoot | null })
        .shadowRoot;
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
  throw new Error(
    `[DRAP] 缺少 #drap-root（micro-app=${readMicroAppName() ?? "?"}）`,
  );
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
    spaceId: (data?.spaceId as string) || "space__demo",
    appearance: (data?.appearance as DaziAppProps["appearance"]) || "light",
    manifest: manifest,
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
  const props = buildMountProps(data);
  await lc.mount(container, props);
};

window.unmount = async () => {
  const lc = await getLifecycle();
  const container = findDrapRoot();
  if (!container) return;
  const scope = findMicroAppNameFromContainer(container) ?? readMicroAppName();
  await lc.unmount(container);
  void scope;
};
