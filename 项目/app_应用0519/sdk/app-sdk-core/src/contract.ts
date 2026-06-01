/**
 * DRAP 协议版本与全局常量。
 * 协议号不可随意更改：主站宿主据此选注入器版本，子应用据此校验自身可用性。
 */

export type DrapContract = "drap-1";
export const DRAP_CONTRACT: DrapContract = "drap-1";

export const DRAP_HOST_BRIDGE_KEY = "__DAZI_APP_SDK__" as const;
/** 聊天多消息并存：按 bridgeInstanceId 索引多个宿主桥（disable-sandbox 共享 window） */
export const DRAP_HOST_BRIDGE_REGISTRY_KEY = "__DAZI_APP_SDK_REGISTRY__" as const;
export const DRAP_HOST_READY_EVENT = "dazi-app-sdk-ready" as const;
export const DRAP_MIN_HOST_SHELL_VERSION = "0.1.0" as const;
