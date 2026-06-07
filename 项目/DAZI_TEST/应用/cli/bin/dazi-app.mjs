#!/usr/bin/env node
/**
 * dazi-app 启动器：优先使用 dazi-vscode bundled CLI，回退 workspace cli/dist。
 * 自动注入 DAZI_RUNTIME_APPS_ROOT（含 templates/、sdk/ 的 runtime-apps 根）。
 */
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CLI_PKG_ROOT = path.resolve(__dirname, "..");

function isRuntimeAppsRoot(dir) {
  return (
    fs.existsSync(path.join(dir, "templates")) &&
    fs.existsSync(path.join(dir, "sdk"))
  );
}

function resolveRuntimeAppsRoot() {
  const env = process.env.DAZI_RUNTIME_APPS_ROOT?.trim();
  if (env && isRuntimeAppsRoot(env)) {
    return path.resolve(env);
  }
  let cur = CLI_PKG_ROOT;
  for (let i = 0; i < 6; i++) {
    if (isRuntimeAppsRoot(cur)) return cur;
    const parent = path.dirname(cur);
    if (parent === cur) break;
    cur = parent;
  }
  return path.resolve(CLI_PKG_ROOT, "..");
}

function resolveDaziAppEntry() {
  const raRoot = resolveRuntimeAppsRoot();
  const candidates = [
    process.env.DAZI_BUNDLED_DIR
      ? path.join(process.env.DAZI_BUNDLED_DIR, "dazi-app.js")
      : null,
    path.join(raRoot, "..", "dazi-vscode", "bundled", "clis", "dazi-app.js"),
    path.join(raRoot, "..", "dazi", "dazi-vscode", "bundled", "clis", "dazi-app.js"),
    path.join(raRoot, "..", "..", "dazi", "dazi-vscode", "bundled", "clis", "dazi-app.js"),
  ].filter(Boolean);

  for (const p of candidates) {
    if (fs.existsSync(p)) {
      return { entry: p, raRoot, source: "bundled" };
    }
  }
  return null;
}

const resolved = resolveDaziAppEntry();
if (!resolved) {
  console.error(
    "[dazi-app] 未找到 bundled CLI。请执行：\n" +
      "  cd dazi/dazi-vscode && pnpm run bundle:clis\n" +
      "（源码：dazi-vscode/cli/dazi-app，产物：bundled/clis/dazi-app.js）",
  );
  process.exit(1);
}

const env = {
  ...process.env,
  DAZI_RUNTIME_APPS_ROOT: resolved.raRoot,
};

if (resolved.source === "bundled" && process.env.DAZI_APP_CLI_SOURCE !== "quiet") {
  process.stderr.write(
    `[dazi-app] 使用 bundled CLI（${resolved.entry}）\n`,
  );
}

const result = spawnSync(process.execPath, [resolved.entry, ...process.argv.slice(2)], {
  stdio: "inherit",
  env,
  cwd: process.cwd(),
});

process.exit(result.status ?? 1);
