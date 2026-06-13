/**
 * 模板 dev 入口（仅 `pnpm dev` 用）。
 *
 * 步骤：
 *   1. 读 manifest.json
 *   2. installDevHostBridge() 注入 window.__DAZI_APP_SDK__（mock 宿主）
 *   3. import 生产 lifecycle 并 mount 到 #drap-root
 *
 * 生产打包后由 DaziAppHost 走 micro-app 加载 dist/index.html；本文件仍会被打入，
 * 但宿主桥已由主站注入，dev-shim 会检测到已存在 bridge 而跳过覆盖（见 isAlreadyMounted）。
 */

import { getHostBridge } from "@dazi/app-sdk-runtime";
import { installDevHostBridge } from "@dazi/app-sdk-runtime/dev-shim";
import {
  DRAP_HOST_BRIDGE_KEY,
  type DaziAppManifest,
} from "@dazi/app-sdk-core";
import manifestJson from "../manifest.json";
import { fixtureDatasets } from "./fixtures/datasets";

const manifest = manifestJson as DaziAppManifest;

/**
 * 找 #drap-root 容器：
 *   - 普通 dev / iframe 模式：在主 document 内
 *   - micro-app + shadow-dom 模式：在 <micro-app> 的 shadowRoot 内
 *
 * 因 shadow-dom 模式下 micro-app 不一定 patch 子应用 document，这里加兜底。
 */
function findDrapRoot(appId: string): HTMLElement | null {
  const scopeName = (
    window as unknown as { __MICRO_APP_NAME__?: string }
  ).__MICRO_APP_NAME__?.trim();
  if (scopeName) {
    const scoped = document.querySelector(`micro-app[name="${scopeName}"]`);
    if (scoped) {
      const sr = (scoped as unknown as { shadowRoot?: ShadowRoot | null })
        .shadowRoot;
      if (sr) {
        const el = sr.getElementById("drap-root");
        if (el) return el;
      }
      const light = scoped.querySelector("#drap-root");
      if (light) return light as HTMLElement;
    }
  }
  const direct = document.getElementById("drap-root");
  if (direct) return direct;
  const name = `drap-${appId}`;
  const preferred = document.querySelector(`micro-app[name="${name}"]`);
  const candidates = preferred
    ? [preferred]
    : Array.from(document.querySelectorAll("micro-app"));
  for (const ma of candidates) {
    const sr = (ma as unknown as { shadowRoot?: ShadowRoot | null }).shadowRoot;
    if (sr) {
      const el = sr.getElementById("drap-root");
      if (el) return el;
    }
  }
  return null;
}

async function waitForRoot(appId: string, timeoutMs = 8_000): Promise<HTMLElement> {
  const t0 = Date.now();
  while (Date.now() - t0 < timeoutMs) {
    const el = findDrapRoot(appId);
    if (el) return el;
    await new Promise((r) => setTimeout(r, 30));
  }
  throw new Error("缺少 #drap-root 容器（主 document 与 micro-app shadow root 均未找到）");
}

async function bootstrap() {
  const alreadyHasHost =
    typeof window !== "undefined" &&
    Boolean((window as unknown as Record<string, unknown>)[DRAP_HOST_BRIDGE_KEY]);

  if (!alreadyHasHost) {
    installDevHostBridge({
      appId: manifest.appId,
      spaceId: "space__demo",
      appearance: "light",
      manifest,
      datasets: fixtureDatasets,
    });
  }

  const lifecycle = (await import("./index")).default;
  const container = await waitForRoot(manifest.appId);
  let mountManifest = manifest;
  let mountDatasets = fixtureDatasets;
  let mountSpaceId = "space__demo";
  let mountAppearance: "light" | "dark" = "light";
  if (alreadyHasHost) {
    try {
      const bridge = getHostBridge();
      mountManifest = bridge.manifest ?? manifest;
      mountSpaceId = bridge.spaceId || mountSpaceId;
      mountAppearance = bridge.appearance ?? "light";
      mountDatasets = bridge.getInitialDatasets?.() ?? fixtureDatasets;
    } catch {
      /* keep defaults */
    }
  }
  await lifecycle.mount(container, {
    appId: mountManifest.appId,
    spaceId: mountSpaceId,
    appearance: mountAppearance,
    manifest: mountManifest,
    datasets: mountDatasets,
  });
}

void bootstrap();
