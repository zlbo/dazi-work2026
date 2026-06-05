import React from "react";
import ReactDOM from "react-dom/client";
import {
  BridgeScopeProvider,
  defineDaziApp,
  findMicroAppNameFromContainer,
} from "@dazi/app-sdk-runtime";
import { MainPage } from "./pages/MainPage";
import "./styles/template.css";

const roots = new WeakMap<Element | ShadowRoot, ReactDOM.Root>();

const lifecycle = defineDaziApp({
  mount(container) {
    const scopeKey = findMicroAppNameFromContainer(container);
    const el = container as HTMLElement;
    el?.classList?.add("drap-root--page");
    let root = roots.get(container);
    if (!root) {
      root = ReactDOM.createRoot(container as Element);
      roots.set(container, root);
    }
    root.render(
      <React.StrictMode>
        <BridgeScopeProvider scopeKey={scopeKey}>
          <MainPage />
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
