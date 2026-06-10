/**
 * defineDaziApp：标准化子应用生命周期导出。
 *
 * 子应用 entry 必须 default export 一个由 defineDaziApp() 创建的对象。
 * micro-app 加载后，宿主调 lifecycle.mount(container, props)；
 * 路由离开时调 lifecycle.unmount(container)。
 */

import type {
  DaziAppDataset,
  DaziAppManifest,
} from "@dazi/app-sdk-core";
import type { Appearance } from "./hostBridge";

export interface DaziAppProps {
  appId: string;
  spaceId: string;
  appearance: Appearance;
  manifest: DaziAppManifest;
  datasets?: Record<string, DaziAppDataset>;
}

export interface DaziAppLifecycle {
  mount(
    container: Element | ShadowRoot,
    props: DaziAppProps,
  ): void | Promise<void>;
  unmount(container: Element | ShadowRoot): void | Promise<void>;
}

export function defineDaziApp(impl: DaziAppLifecycle): DaziAppLifecycle {
  if (typeof impl?.mount !== "function" || typeof impl?.unmount !== "function") {
    throw new Error("[DRAP] defineDaziApp: mount/unmount 必须为函数");
  }
  return impl;
}
