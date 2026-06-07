/**
 * 运行时辅助 hook（appearance / router）。
 *
 * 注意：导入 react 仅作为 peerDependency，由模板 / 宿主提供；
 * 不在 bundle 内打包 react。
 */

import { useEffect, useState, useCallback, useMemo } from "react";
import { useBridgeScopeKey } from "./bridgeScope";
import { getHostBridge } from "./hostBridge";
import type { Appearance, DaziAppHostBridge } from "./hostBridge";

/** 按 BridgeScopeProvider 的 micro-app name 解析宿主桥 */
export function useHostBridge(): DaziAppHostBridge {
  const scope = useBridgeScopeKey();
  return useMemo(() => getHostBridge(scope), [scope]);
}

export function useAppearance(): Appearance {
  const bridge = useHostBridge();
  const [appearance, setAppearance] = useState<Appearance>(bridge.appearance);
  useEffect(() => {
    return bridge.on("appearanceChange", (a) => setAppearance(a));
  }, [bridge]);
  return appearance;
}

export interface AppRouter {
  navigate(path: string): void;
  back(): void;
}

export function useAppRouter(): AppRouter {
  const bridge = useHostBridge();
  return {
    navigate: useCallback((p: string) => bridge.navigate(p), [bridge]),
    back: useCallback(() => bridge.back(), [bridge]),
  };
}
