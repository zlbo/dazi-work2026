/**
 * disable-sandbox 多实例共享 window，子应用须用 micro-app name 解析对应宿主桥。
 */

import React, { createContext, useContext } from "react";

export type BridgeScopeKey = string | null;

const BridgeScopeContext = createContext<BridgeScopeKey>(null);

export function BridgeScopeProvider({
  scopeKey,
  children,
}: {
  scopeKey?: string | null;
  children: React.ReactNode;
}) {
  const key = scopeKey?.trim() || null;
  return (
    <BridgeScopeContext.Provider value={key}>
      {children}
    </BridgeScopeContext.Provider>
  );
}

export function useBridgeScopeKey(): BridgeScopeKey {
  return useContext(BridgeScopeContext);
}

/** 从 mount 容器向上找到 <micro-app name="..."> */
export function findMicroAppNameFromContainer(
  container: Element | ShadowRoot,
): string | undefined {
  if (container instanceof ShadowRoot) {
    const host = container.host;
    if (
      host instanceof HTMLElement &&
      host.tagName?.toLowerCase() === "micro-app"
    ) {
      return host.getAttribute("name") ?? undefined;
    }
    return undefined;
  }
  let node: Element | null = container instanceof Element ? container : null;
  while (node) {
    if (node.tagName?.toLowerCase() === "micro-app") {
      return node.getAttribute("name") ?? undefined;
    }
    node = node.parentElement;
  }
  const microAppName = (
    window as unknown as { __MICRO_APP_NAME__?: string }
  ).__MICRO_APP_NAME__?.trim();
  return microAppName || undefined;
}
