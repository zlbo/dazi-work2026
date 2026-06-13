import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";

export default defineConfig({
  base: process.env.DRAP_ASSET_BASE || "/",
  plugins: [react()],
  server: {
    port: 5182,
    cors: true,
    headers: {
      "Access-Control-Allow-Origin": "*",
    },
  },
  build: {
    outDir: "dist",
    sourcemap: true,
    target: "es2020",
    rollupOptions: {
      input: path.resolve(__dirname, "index.prod.html"),
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
});
