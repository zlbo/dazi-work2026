import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";

/**
 * DRAP 模板 Vite 配置。
 *
 * P0 构建策略（折中）：
 *   - dev: index.html + dev-entry.tsx 自带宿主桥 mock，可单独 pnpm dev 调试
 *   - build: 同样输出完整 SPA（含 index.html），由 micro-app 拉取 URL 解析挂载
 *     - 入口仍走 dev-entry.tsx；但生产模式自动跳过 dev-shim 注入（见 dev-entry 内的 if 判断）
 *
 * P1 起将切换为：library 模式 + manifest.json + entry chunk，由 DaziAppHost 直读 manifest.entry。
 * P0 用 SPA 形态先打通 micro-app 链路（micro-app 接受 url 指向任意 HTML，故无需 library 模式）。
 */
export default defineConfig({
  // 发布构建由 dazi-app build/upload 注入 DRAP_ASSET_BASE=/runtime-apps/<appId>/<ver>/
  // 本地 pnpm dev 仍用根路径 /
  base: process.env.DRAP_ASSET_BASE || "/",
  plugins: [react()],
  server: {
    port: 5180,
    cors: true,
    headers: {
      // micro-app 跨源加载子应用 HTML 需要 CORS；P0 dev 简化放通
      "Access-Control-Allow-Origin": "*",
    },
  },
  build: {
    outDir: "dist",
    sourcemap: true,
    target: "es2020",
    rollupOptions: {
      // 生产走 prod-entry，避免 dev-entry 自动挂到第一个 micro-app
      input: path.resolve(__dirname, "index.prod.html"),
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
});
