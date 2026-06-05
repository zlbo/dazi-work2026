/**
 * 批量 upload 新建的 9 个页模式模板到 Registry。
 * 用法（在 dazi/runtime-apps 根目录）：
 *   node scripts/upload-planned-templates.mjs [--space space__0519]
 */

import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const spaceId = process.argv.includes("--space")
  ? process.argv[process.argv.indexOf("--space") + 1]
  : "space__0519";

const TEMPLATE_DIRS = process.argv.includes("--skip-first")
  ? [
      "app-template-financial-trend-dashboard",
      "app-template-equipment-monitor-board",
      "app-template-purchase-order-form",
      "app-template-workflow-approval-page",
      "app-template-inventory-management-page",
      "app-template-realtime-monitor",
      "app-template-alarm-center",
      "app-template-production-command-center",
    ]
  : [
  "app-template-production-analysis-grid",
  "app-template-financial-trend-dashboard",
  "app-template-equipment-monitor-board",
  "app-template-purchase-order-form",
  "app-template-workflow-approval-page",
  "app-template-inventory-management-page",
  "app-template-realtime-monitor",
  "app-template-alarm-center",
  "app-template-production-command-center",
  ];

const results = [];

for (const dir of TEMPLATE_DIRS) {
  const cwd = path.join(ROOT, "templates", dir);
  console.log(`\n=== upload: ${dir} (space=${spaceId}) ===`);
  const r = spawnSync(
    "pnpm",
    [
      "run",
      "dazi-app",
      "upload",
      "--cwd",
      path.relative(ROOT, cwd).replace(/\\/g, "/"),
      "--space",
      spaceId,
      "--activate",
      "--changelog",
      `P5-${dir}-0.1.0`,
    ],
    {
      cwd: ROOT,
      stdio: "inherit",
      shell: process.platform === "win32",
    },
  );
  results.push({ dir, ok: r.status === 0, code: r.status ?? 1 });
  if (r.status !== 0) {
    console.error(`FAILED: ${dir} exit=${r.status}`);
  }
}

const ok = results.filter((x) => x.ok).length;
const fail = results.length - ok;
console.log(`\nDone: ${ok} ok, ${fail} failed`);
if (fail > 0) process.exit(1);
