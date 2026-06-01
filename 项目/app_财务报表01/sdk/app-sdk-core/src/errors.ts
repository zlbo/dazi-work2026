/**
 * 跨 SDK / 宿主 / 后端 统一错误码（305 §5.1）。
 */

export type DaziAppErrorCode =
  | "PERMISSION_DENIED"
  | "DATA_SOURCE_FAILED"
  | "DATA_SOURCE_OUT_OF_SCOPE"
  | "HOST_INCOMPATIBLE"
  | "HOST_BRIDGE_MISSING"
  | "MANIFEST_INVALID"
  | "SDK_BOUNDARY_VIOLATION"
  | "UNKNOWN";

export class DaziAppError extends Error {
  code: DaziAppErrorCode;
  detail?: unknown;
  constructor(code: DaziAppErrorCode, message: string, detail?: unknown) {
    super(message);
    this.name = "DaziAppError";
    this.code = code;
    this.detail = detail;
  }
}
