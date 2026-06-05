import React from "react";
import ReactDOM from "react-dom/client";
import {
  BridgeScopeProvider,
  defineDaziApp,
  findMicroAppNameFromContainer,
} from "@dazi/app-sdk-runtime";
import { ChatKpiResult } from "./pages/ChatKpiResult";
import "./styles/template.css";

const roots = new WeakMap<Element | ShadowRoot, ReactDOM.Root>();

function applyChatRootLayout(container: Element | ShadowRoot) {
  const el = container as HTMLElement;
  if (!el?.classList) return;
  el.classList.add("drap-root--chat");
  el.style.height = "auto";
  el.style.minHeight = "0";
}

const lifecycle = defineDaziApp({
  mount(container) {
    const scopeKey = findMicroAppNameFromContainer(container);
    applyChatRootLayout(container);
    const root = ReactDOM.createRoot(container as Element);
    roots.set(container, root);
    root.render(
      <React.StrictMode>
        <BridgeScopeProvider scopeKey={scopeKey}>
          <ChatKpiResult />
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
