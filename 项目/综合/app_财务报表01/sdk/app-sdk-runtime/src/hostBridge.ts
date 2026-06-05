/**
 * 宿主桥：子应用通过 window.__DAZI_APP_SDK__ 或注册表访问宿主能力。
 *
 * 聊天区 disable-sandbox 下多实例共享同一 window，须用 microApp.getData().bridgeInstanceId
 * 从 __DAZI_APP_SDK_REGISTRY__ 取对应 bridge，避免后挂载消息覆盖先挂载消息的 datasets。
 */

import {
  DRAP_HOST_BRIDGE_KEY,
  DRAP_HOST_BRIDGE_REGISTRY_KEY,
  DRAP_HOST_READY_EVENT,
  DRAP_CONTRACT,
  type DrapContract,
} from "@dazi/app-sdk-core";
import type {
  DaziAppDataSourceDecl,
  DaziAppDataset,
  DaziAppManifest,
} from "@dazi/app-sdk-core";
import { DaziAppError } from "@dazi/app-sdk-core";

export type Appearance = "light" | "dark";

export interface DaziAppHostBridge {
  contract: DrapContract;
  appId: string;
  spaceId: string;
  appearance: Appearance;
  manifest: DaziAppManifest;

  getInitialDatasets(): Record<string, DaziAppDataset>;

  invokeDataSource(
    key: string,
    overrides?: Partial<DaziAppDataSourceDecl>,
  ): Promise<DaziAppDataset>;

  invokeDynamicDataSource(decl: DaziAppDataSourceDecl): Promise<DaziAppDataset>;

  navigate(path: string): void;
  back(): void;

  reportError(code: string, detail?: unknown): void;

  on<K extends keyof DaziAppHostEvents>(
    event: K,
    handler: (payload: DaziAppHostEvents[K]) => void,
  ): () => void;
}

export interface DaziAppHostEvents {
  appearanceChange: Appearance;
  datasetsRefreshed: Record<string, DaziAppDataset>;
}

type BridgeRegistry = Record<string, DaziAppHostBridge>;

declare global {
  interface Window {
    [DRAP_HOST_BRIDGE_KEY]?: DaziAppHostBridge;
    [DRAP_HOST_BRIDGE_REGISTRY_KEY]?: BridgeRegistry;
    microApp?: {
      getData?: () => Record<string, unknown>;
    };
  }
}

function readBridgeScopeFromMicroApp(): string | undefined {
  try {
    const data = window.microApp?.getData?.();
    const scope = data?.bridgeScope;
    if (typeof scope === "string" && scope.trim()) return scope.trim();
    const id = data?.bridgeInstanceId;
    return typeof id === "string" && id.trim() ? id.trim() : undefined;
  } catch {
    return undefined;
  }
}

function resolveBridgeFromRegistry(
  scopeKey?: string,
): DaziAppHostBridge | undefined {
  const reg = window[DRAP_HOST_BRIDGE_REGISTRY_KEY];
  if (!reg || typeof reg !== "object") return undefined;

  const key = scopeKey?.trim();
  if (key && reg[key]) return reg[key];

  const fromData = readBridgeScopeFromMicroApp();
  if (fromData && reg[fromData]) return reg[fromData];

  return undefined;
}

function assertContract(bridge: DaziAppHostBridge): DaziAppHostBridge {
  if (bridge.contract !== DRAP_CONTRACT) {
    throw new DaziAppError(
      "HOST_INCOMPATIBLE",
      `宿主桥协议版本不匹配：期望 ${DRAP_CONTRACT}，实际 ${bridge.contract}`,
    );
  }
  return bridge;
}

/**
 * @param scopeKey 通常为 <micro-app name>（如 drap-profit-analysis-fd8868fb7eee），
 *   由 BridgeScopeProvider 注入；disable-sandbox 下比 microApp.getData 更可靠。
 */
export function getHostBridge(scopeKey?: string | null): DaziAppHostBridge {
  const fromRegistry = resolveBridgeFromRegistry(
    scopeKey?.trim() || undefined,
  );
  if (fromRegistry) return assertContract(fromRegistry);

  const bridge = window[DRAP_HOST_BRIDGE_KEY];
  if (!bridge) {
    throw new DaziAppError(
      "HOST_BRIDGE_MISSING",
      "DRAP host bridge 未注入；请确认 DaziAppHost 已挂载或 dev 模式下调用了 installDevHostBridge()。",
    );
  }
  return assertContract(bridge);
}

export function waitForHostBridge(
  timeoutMs = 5_000,
  scopeKey?: string | null,
): Promise<DaziAppHostBridge> {
  return new Promise((resolve, reject) => {
    if (typeof window === "undefined") {
      reject(new DaziAppError("HOST_BRIDGE_MISSING", "非浏览器环境"));
      return;
    }
    try {
      const b = getHostBridge(scopeKey);
      resolve(b);
      return;
    } catch {
      /* 继续等待 ready */
    }
    const timer = window.setTimeout(() => {
      window.removeEventListener(DRAP_HOST_READY_EVENT, onReady);
      reject(
        new DaziAppError(
          "HOST_BRIDGE_MISSING",
          `等待宿主桥超时（${timeoutMs}ms）`,
        ),
      );
    }, timeoutMs);
    const onReady = () => {
      window.clearTimeout(timer);
      window.removeEventListener(DRAP_HOST_READY_EVENT, onReady);
      try {
        resolve(getHostBridge(scopeKey));
      } catch (e) {
        reject(
          e instanceof DaziAppError
            ? e
            : new DaziAppError("HOST_BRIDGE_MISSING", "ready 后仍无法解析 bridge"),
        );
      }
    };
    window.addEventListener(DRAP_HOST_READY_EVENT, onReady);
  });
}
