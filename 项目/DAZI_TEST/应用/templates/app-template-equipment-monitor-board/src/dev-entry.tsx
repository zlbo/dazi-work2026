import { getHostBridge } from "@dazi/app-sdk-runtime";
import { installDevHostBridge } from "@dazi/app-sdk-runtime/dev-shim";
import { DRAP_HOST_BRIDGE_KEY, type DaziAppManifest } from "@dazi/app-sdk-core";
import manifestJson from "../manifest.json";
import { fixtureDatasets } from "./fixtures/datasets";

const manifest = manifestJson as DaziAppManifest;
const APP_ID = "equipment-monitor";

function findDrapRoot(): HTMLElement | null {
  const scopeName = (window as unknown as { __MICRO_APP_NAME__?: string }).__MICRO_APP_NAME__?.trim();
  if (scopeName) {
    const scoped = document.querySelector(`micro-app[name="${scopeName}"]`);
    if (scoped) {
      const sr = (scoped as unknown as { shadowRoot?: ShadowRoot | null }).shadowRoot;
      if (sr) {
        const el = sr.getElementById("drap-root");
        if (el) return el;
      }
      const light = scoped.querySelector("#drap-root");
      if (light) return light as HTMLElement;
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
  throw new Error("缺少 #drap-root 容器");
}

async function bootstrap() {
  const alreadyHasHost =
    Boolean(window[DRAP_HOST_BRIDGE_KEY]) ||
    Boolean((window as unknown as { __DAZI_APP_SDK_REGISTRY__?: unknown }).__DAZI_APP_SDK_REGISTRY__);
  if (!alreadyHasHost) {
    installDevHostBridge({
      appId: APP_ID,
      spaceId: "space__0519",
      appearance: "light",
      manifest,
      datasets: fixtureDatasets,
    });
  }
  const lc = await import("./index").then((m) => m.default);
  const container = await waitForRoot();
  const bridge = getHostBridge();
  await lc.mount(container, {
    appId: bridge.appId,
    spaceId: bridge.spaceId,
    appearance: bridge.appearance,
    manifest: bridge.manifest,
    datasets: bridge.getInitialDatasets(),
  });
}

void bootstrap();
