/**
 * 模板生产入口（被宿主 micro-app 加载）。
 *
 * 通过 defineDaziApp 暴露 lifecycle.mount/unmount；
 * mount 把 ProfitDashboard 渲染到宿主提供的容器（shadow_dom 或普通 div）。
 */

import React from "react";
import ReactDOM from "react-dom/client";
import {
  BridgeScopeProvider,
  defineDaziApp,
  findMicroAppNameFromContainer,
  getHostBridge,
  type DaziAppProps,
} from "@dazi/app-sdk-runtime";
import type { DaziAppManifest } from "@dazi/app-sdk-core";
import { ChatProfitResult } from "./pages/ChatProfitResult";
import { ProfitDashboard } from "./pages/ProfitDashboard";
import "./styles/template.css";

const roots = new WeakMap<Element | ShadowRoot, ReactDOM.Root>();

/** 优先用宿主注入的 manifest（Registry resolve），打包内的 manifest 仅作 dev 兜底 */
function effectiveManifest(
  props: DaziAppProps,
  scopeKey?: string,
): DaziAppManifest {
  try {
    const fromHost = getHostBridge(scopeKey).manifest;
    if (fromHost?.appId) return fromHost;
  } catch {
    /* 独立 dev 无宿主桥 */
  }
  return props.manifest;
}

function resolvePage(props: DaziAppProps, scopeKey?: string) {
  return effectiveManifest(props, scopeKey).mount?.type === "chat_result"
    ? ChatProfitResult
    : ProfitDashboard;
}

function applyRootLayoutMode(
  container: Element | ShadowRoot,
  props: DaziAppProps,
  scopeKey?: string,
) {
  const el = container as HTMLElement;
  if (!el?.classList) return;
  const isChat = effectiveManifest(props, scopeKey).mount?.type === "chat_result";
  el.classList.toggle("drap-root--chat", isChat);
  el.classList.toggle("drap-root--page", !isChat);
  if (isChat) {
    el.style.height = "auto";
    el.style.minHeight = "0";
  }
}

const lifecycle = defineDaziApp({
  mount(container, props) {
    const scopeKey = findMicroAppNameFromContainer(container);
    applyRootLayoutMode(container, props, scopeKey);
    const Page = resolvePage(props, scopeKey);
    const root = ReactDOM.createRoot(container as Element);
    roots.set(container, root);
    root.render(
      <React.StrictMode>
        <BridgeScopeProvider scopeKey={scopeKey}>
          <Page />
        </BridgeScopeProvider>
      </React.StrictMode>,
    );
  },
  unmount(container) {
    const root = roots.get(container);
    if (root) {
      root.unmount();
      roots.delete(container);
    }
  },
});

export default lifecycle;
