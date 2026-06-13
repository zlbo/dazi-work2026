/**
 * 从 catalog 规划批量生成 DRAP 页模式模板（P5）。
 * 用法：node scripts/scaffold-planned-templates.mjs
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const TEMPLATES_DIR = path.join(ROOT, "templates");
const CATALOG_PATH = path.join(TEMPLATES_DIR, "catalog.json");

const SKIP_IDS = new Set([
  "profit-analysis-dashboard",
  "chat-kpi-skin",
  "chat-trend-skin",
]);

const PLANNED = [
  {
    id: "production-analysis-grid",
    appId: "production-analysis-grid",
    name: "生产明细分析网格",
    port: 5184,
    archetype: "grid",
    datasetKey: "table",
    sceneTag: "production_detail",
    title: "生产明细分析",
    fixture: {
      columns: ["work_order", "line", "qty", "yield_pct", "shift"],
      rows: [
        { work_order: "WO-1001", line: "产线A", qty: 1200, yield_pct: 98.2, shift: "白班" },
        { work_order: "WO-1002", line: "产线B", qty: 980, yield_pct: 96.5, shift: "夜班" },
      ],
    },
  },
  {
    id: "financial-trend-dashboard",
    appId: "financial-trend",
    name: "财务多指标趋势",
    port: 5185,
    archetype: "trend",
    sceneTag: "finance_trend",
    title: "财务趋势看板",
    fixture: {
      kpi: {
        columns: ["revenue", "profit", "margin_pct"],
        rows: [{ revenue: 12500000, profit: 2100000, margin_pct: 16.8 }],
      },
      trend: {
        columns: ["month", "revenue", "profit"],
        rows: [
          { month: "1月", revenue: 980000, profit: 120000 },
          { month: "2月", revenue: 1020000, profit: 135000 },
          { month: "3月", revenue: 1100000, profit: 148000 },
        ],
      },
    },
  },
  {
    id: "equipment-monitor-board",
    appId: "equipment-monitor",
    name: "设备监控大屏",
    port: 5186,
    archetype: "kpi-wall",
    datasetKey: "metrics",
    sceneTag: "equipment_realtime",
    title: "设备监控",
    fixture: {
      columns: ["label", "value", "unit", "status"],
      rows: [
        { label: "OEE", value: 87.3, unit: "%", status: "正常" },
        { label: "运行设备", value: 42, unit: "台", status: "正常" },
        { label: "告警", value: 3, unit: "条", status: "关注" },
      ],
    },
  },
  {
    id: "purchase-order-form",
    appId: "purchase-order",
    name: "采购单维护",
    port: 5187,
    archetype: "form",
    sceneTag: "purchase",
    title: "采购单维护",
    fixture: {},
  },
  {
    id: "workflow-approval-page",
    appId: "workflow-approval",
    name: "审批流挂载页",
    port: 5188,
    archetype: "grid",
    datasetKey: "todos",
    sceneTag: "workflow",
    title: "审批待办",
    fixture: {
      columns: ["id", "title", "applicant", "status", "submitted_at"],
      rows: [
        { id: "AP-001", title: "差旅报销", applicant: "张三", status: "待审", submitted_at: "2026-05-20" },
        { id: "AP-002", title: "采购申请", applicant: "李四", status: "待审", submitted_at: "2026-05-21" },
      ],
    },
  },
  {
    id: "inventory-management-page",
    appId: "inventory-mgmt",
    name: "库存管理",
    port: 5189,
    archetype: "grid",
    datasetKey: "inventory",
    sceneTag: "inventory",
    title: "库存管理",
    fixture: {
      columns: ["sku", "name", "qty", "safety_stock", "warehouse"],
      rows: [
        { sku: "SKU-001", name: "原料A", qty: 520, safety_stock: 200, warehouse: "WH-01" },
        { sku: "SKU-002", name: "成品B", qty: 88, safety_stock: 100, warehouse: "WH-02" },
      ],
    },
  },
  {
    id: "realtime-monitor",
    appId: "realtime-monitor",
    name: "实时监控卡片墙",
    port: 5190,
    archetype: "kpi-wall",
    datasetKey: "metrics",
    sceneTag: "realtime",
    title: "实时监控",
    fixture: {
      columns: ["label", "value", "unit"],
      rows: [
        { label: "在线用户", value: 1284, unit: "人" },
        { label: "TPS", value: 342, unit: "/s" },
        { label: "错误率", value: 0.12, unit: "%" },
      ],
    },
  },
  {
    id: "alarm-center",
    appId: "alarm-center",
    name: "告警中心",
    port: 5191,
    archetype: "grid",
    datasetKey: "alarms",
    sceneTag: "alarm",
    title: "告警中心",
    fixture: {
      columns: ["level", "source", "message", "time", "status"],
      rows: [
        { level: "高", source: "产线A", message: "温度超限", time: "10:02", status: "未确认" },
        { level: "中", source: "仓储", message: "库存低于安全线", time: "09:45", status: "处理中" },
      ],
    },
  },
  {
    id: "production-command-center",
    appId: "production-command",
    name: "生产指挥中心",
    port: 5192,
    archetype: "kpi-wall",
    datasetKey: "kpi",
    sceneTag: "command_center",
    title: "生产指挥中心",
    fixture: {
      columns: ["label", "value", "unit"],
      rows: [
        { label: "今日产量", value: 12500, unit: "件" },
        { label: "计划达成", value: 96.8, unit: "%" },
        { label: "一次合格率", value: 99.1, unit: "%" },
      ],
    },
  },
];

function dirName(id) {
  return `app-template-${id}`;
}

function write(rel, content) {
  const full = path.join(TEMPLATES_DIR, rel);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, content, "utf8");
}

function manifestJson(spec) {
  const dataSources = [];
  if (spec.archetype === "trend") {
    dataSources.push(
      {
        key: "kpi",
        kind: "static",
        data: { columns: spec.fixture.kpi.columns, rows: spec.fixture.kpi.rows },
      },
      {
        key: "trend",
        kind: "static",
        data: { columns: spec.fixture.trend.columns, rows: spec.fixture.trend.rows },
      },
    );
  } else if (spec.archetype === "form") {
    dataSources.push({
      key: "form",
      kind: "static",
      data: { columns: ["field", "value"], rows: [] },
    });
  } else {
    dataSources.push({
      key: spec.datasetKey,
      kind: "static",
      data: { columns: spec.fixture.columns, rows: spec.fixture.rows },
    });
  }
  return (
    JSON.stringify(
      {
        appId: spec.appId,
        name: spec.name,
        description: `${spec.name}（DRAP 页模式演示模板）`,
        version: "0.1.0",
        framework: { react: "^18", ts: true },
        entry: "index.html",
        styles: ["style.css"],
        assets: ["assets/"],
        permissions: ["dataspace:space__0519"],
        data_sources: dataSources,
        sdk: { min_version: "0.1.0", contract: "drap-1" },
        mount: { type: "page", sandbox: "shadow_dom" },
        refresh: { on_mount: true, stale_ms: 60000 },
        ai: {
          scene_tag: spec.sceneTag,
          template_origin: `@dazi/${dirName(spec.id)}@0.1.0`,
        },
      },
      null,
      2,
    ) + "\n"
  );
}

function fixturesTs(spec) {
  if (spec.archetype === "trend") {
    return `import type { DaziAppDataset } from "@dazi/app-sdk-core";

export const fixtureDatasets: Record<string, DaziAppDataset> = {
  kpi: {
    columns: ${JSON.stringify(spec.fixture.kpi.columns)},
    data: ${JSON.stringify(spec.fixture.kpi.rows)},
    row_count: ${spec.fixture.kpi.rows.length},
    meta: { kind: "static", ok: true, fetched_at: new Date().toISOString() },
  },
  trend: {
    columns: ${JSON.stringify(spec.fixture.trend.columns)},
    data: ${JSON.stringify(spec.fixture.trend.rows)},
    row_count: ${spec.fixture.trend.rows.length},
    meta: { kind: "static", ok: true, fetched_at: new Date().toISOString() },
  },
};
`;
  }
  if (spec.archetype === "form") {
    return `import type { DaziAppDataset } from "@dazi/app-sdk-core";

export const fixtureDatasets: Record<string, DaziAppDataset> = {
  form: {
    columns: ["field", "value"],
    data: [],
    row_count: 0,
    meta: { kind: "static", ok: true, fetched_at: new Date().toISOString() },
  },
};
`;
  }
  return `import type { DaziAppDataset } from "@dazi/app-sdk-core";

export const fixtureDatasets: Record<string, DaziAppDataset> = {
  ${spec.datasetKey}: {
    columns: ${JSON.stringify(spec.fixture.columns)},
    data: ${JSON.stringify(spec.fixture.rows)},
    row_count: ${spec.fixture.rows.length},
    meta: { kind: "static", ok: true, fetched_at: new Date().toISOString() },
  },
};
`;
}

function mainPageTsx(spec) {
  if (spec.archetype === "grid") {
    return `import React from "react";
import { useDataset } from "@dazi/app-sdk-data";
import { useAppearance } from "@dazi/app-sdk-runtime";
import { DataGrid, PageLayout } from "@dazi/app-sdk-ui";

export function MainPage() {
  const appearance = useAppearance();
  const ds = useDataset("${spec.datasetKey}");

  return (
    <PageLayout
      title="${spec.title}"
      appearance={appearance}
      toolbar={
        <button
          type="button"
          onClick={() => void ds.refetch()}
          style={{
            padding: "4px 10px",
            border: "1px solid var(--drap-card-border)",
            borderRadius: 6,
            background: "transparent",
            cursor: "pointer",
          }}
        >
          刷新
        </button>
      }
    >
      {ds.loading && <p style={{ color: "#6b7280" }}>加载中…</p>}
      {ds.error && <p style={{ color: "#b91c1c" }}>{ds.error}</p>}
      <DataGrid dataset={ds.data} maxHeight={520} />
    </PageLayout>
  );
}
`;
  }
  if (spec.archetype === "trend") {
    return `import React from "react";
import { useDataset } from "@dazi/app-sdk-data";
import { useAppearance } from "@dazi/app-sdk-runtime";
import { KpiCard, PageLayout, TrendChart } from "@dazi/app-sdk-ui";

function fmt(n: unknown) {
  const v = Number(n);
  return Number.isFinite(v) ? v.toLocaleString("zh-CN") : "—";
}

export function MainPage() {
  const appearance = useAppearance();
  const kpi = useDataset("kpi");
  const trend = useDataset("trend");
  const row = kpi.data?.data?.[0] ?? {};

  return (
    <PageLayout title="${spec.title}" appearance={appearance}>
      <motion className="drap-kpi-row" style={{ marginBottom: 16 }}>
        <KpiCard title="营收" value={fmt(row.revenue)} />
        <KpiCard title="利润" value={fmt(row.profit)} />
        <KpiCard title="利润率" value={\`\${fmt(row.margin_pct)}%\`} />
      </motion>
      <TrendChart
        dataset={trend.data}
        xKey="month"
        yKeys={["revenue", "profit"]}
        appearance={appearance}
        height={320}
        title="月度趋势"
      />
    </PageLayout>
  );
}
`.replace(/<motion/g, "<div").replace(/<\/motion>/g, "</div>");
  }
  if (spec.archetype === "kpi-wall") {
    return `import React from "react";
import { useDataset } from "@dazi/app-sdk-data";
import { useAppearance } from "@dazi/app-sdk-runtime";
import { KpiCard, PageLayout } from "@dazi/app-sdk-ui";

export function MainPage() {
  const appearance = useAppearance();
  const ds = useDataset("${spec.datasetKey}");
  const rows = ds.data?.data ?? [];

  return (
    <PageLayout title="${spec.title}" appearance={appearance}>
      <div className="drap-kpi-row">
        {rows.map((r, i) => (
          <KpiCard
            key={String(r.label ?? i)}
            title={String(r.label ?? "指标")}
            value={String(r.value ?? "—") + (r.unit ? \` \${String(r.unit)}\` : "")}
            hint={r.status ? String(r.status) : undefined}
          />
        ))}
      </div>
      {!rows.length && !ds.loading && (
        <p style={{ color: "#6b7280" }}>暂无指标数据</p>
      )}
    </PageLayout>
  );
}
`;
  }
  return `import React from "react";
import { useAppearance } from "@dazi/app-sdk-runtime";
import { Card, PageLayout } from "@dazi/app-sdk-ui";

export function MainPage() {
  const appearance = useAppearance();

  return (
    <PageLayout title="${spec.title}" appearance={appearance}>
      <Card title="采购单（演示表单）">
        <div style={{ display: "grid", gap: 12, maxWidth: 480 }}>
          <label style={{ display: "grid", gap: 4, fontSize: 13 }}>
            供应商
            <input readOnly value="示例供应商有限公司" style={{ padding: 8, borderRadius: 6, border: "1px solid #e5e7eb" }} />
          </label>
          <label style={{ display: "grid", gap: 4, fontSize: 13 }}>
            物料
            <input readOnly value="原料 A-100" style={{ padding: 8, borderRadius: 6, border: "1px solid #e5e7eb" }} />
          </label>
          <label style={{ display: "grid", gap: 4, fontSize: 13 }}>
            数量
            <input readOnly value="500" style={{ padding: 8, borderRadius: 6, border: "1px solid #e5e7eb" }} />
          </label>
          <p style={{ fontSize: 12, color: "#6b7280" }}>
            演示模板：提交 Action 请在本体函数绑定后扩展（禁止裸 fetch）。
          </p>
        </div>
      </Card>
    </PageLayout>
  );
}
`;
}

function indexTsx() {
  return `import React from "react";
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
    const root = ReactDOM.createRoot(container as Element);
    roots.set(container, root);
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
`;
}

function prodEntry() {
  return `import {
  getHostBridge,
  waitForHostBridge,
  findMicroAppNameFromContainer,
  tryInstallIframeBridgeShim,
  type DaziAppProps,
} from "@dazi/app-sdk-runtime";

tryInstallIframeBridgeShim();
import {
  DRAP_HOST_BRIDGE_KEY,
  DRAP_HOST_BRIDGE_REGISTRY_KEY,
  type DaziAppManifest,
} from "@dazi/app-sdk-core";
import manifestJson from "../manifest.json";
import { fixtureDatasets } from "./fixtures/datasets";
import type { DaziAppLifecycle } from "@dazi/app-sdk-runtime";

const manifest = manifestJson as DaziAppManifest;

declare global {
  interface Window {
    __MICRO_APP_NAME__?: string;
    mount?: (data?: Record<string, unknown>) => void | Promise<void>;
    unmount?: (data?: Record<string, unknown>) => void | Promise<void>;
  }
}

function readMicroAppName(): string | undefined {
  return window.__MICRO_APP_NAME__?.trim() || undefined;
}

function findDrapRoot(): HTMLElement | null {
  const scopeName = readMicroAppName();
  if (scopeName) {
    const ma = document.querySelector(\`micro-app[name="\${scopeName}"]\`);
    if (ma) {
      const sr = (ma as HTMLElement & { shadowRoot?: ShadowRoot | null }).shadowRoot;
      if (sr) {
        const inShadow = sr.getElementById("drap-root");
        if (inShadow) return inShadow;
      }
      const inLight = ma.querySelector("#drap-root");
      if (inLight) return inLight as HTMLElement;
    }
  }
  return document.getElementById("drap-root");
}

async function waitForRoot(timeoutMs = 8_000): Promise<HTMLElement> {
  const t0 = Date.now();
  while (Date.now() - t0 < timeoutMs) {
    const el = findDrapRoot();
    if (el) return el;
    await new Promise((r) => setTimeout(r, 30));
  }
  throw new Error(\`[DRAP] 缺少 #drap-root（micro-app=\${readMicroAppName() ?? "?"}）\`);
}

function hostBridgeReady(): boolean {
  const reg = window[DRAP_HOST_BRIDGE_REGISTRY_KEY];
  const scope = readMicroAppName();
  if (scope && reg?.[scope]) return true;
  return Boolean(window[DRAP_HOST_BRIDGE_KEY]);
}

function buildMountProps(data?: Record<string, unknown>): DaziAppProps {
  const scope = readMicroAppName();
  if (hostBridgeReady()) {
    try {
      const bridge = getHostBridge(scope);
      return {
        appId: bridge.appId,
        spaceId: bridge.spaceId,
        appearance: bridge.appearance,
        manifest: bridge.manifest,
        datasets: bridge.getInitialDatasets(),
      };
    } catch {
      /* fallback */
    }
  }
  return {
    appId: (data?.appId as string) || manifest.appId,
    spaceId: (data?.spaceId as string) || "space__demo",
    appearance: (data?.appearance as DaziAppProps["appearance"]) || "light",
    manifest,
    datasets: fixtureDatasets,
  };
}

let lifecyclePromise: Promise<DaziAppLifecycle> | null = null;

function getLifecycle(): Promise<DaziAppLifecycle> {
  if (!lifecyclePromise) {
    lifecyclePromise = import("./index").then((m) => m.default);
  }
  return lifecyclePromise;
}

window.mount = async (data?: Record<string, unknown>) => {
  const scope = readMicroAppName();
  if (!hostBridgeReady()) {
    await waitForHostBridge(8_000, scope);
  }
  const lc = await getLifecycle();
  const container = await waitForRoot();
  await lc.mount(container, buildMountProps(data));
};

window.unmount = async () => {
  const lc = await getLifecycle();
  const container = findDrapRoot();
  if (!container) return;
  void findMicroAppNameFromContainer(container);
  await lc.unmount(container);
};
`;
}

function devEntry(appId) {
  return `import { getHostBridge } from "@dazi/app-sdk-runtime";
import { installDevHostBridge } from "@dazi/app-sdk-runtime/dev-shim";
import { DRAP_HOST_BRIDGE_KEY, type DaziAppManifest } from "@dazi/app-sdk-core";
import manifestJson from "../manifest.json";
import { fixtureDatasets } from "./fixtures/datasets";

const manifest = manifestJson as DaziAppManifest;
const APP_ID = ${JSON.stringify(appId)};

function findDrapRoot(): HTMLElement | null {
  const scopeName = (window as unknown as { __MICRO_APP_NAME__?: string }).__MICRO_APP_NAME__?.trim();
  if (scopeName) {
    const scoped = document.querySelector(\`micro-app[name="\${scopeName}"]\`);
    if (scoped) {
      const sr = (scoped as unknown as { shadowRoot?: ShadowRoot | null }).shadowRoot;
      if (sr) {
        const el = sr.getElementById("drap-root");
        if (el) return el;
      }
      const light = scoped.querySelector("#drap-root");
      if (light) return light as HTMLElement;
    }
  }
  return document.getElementById("drap-root");
}

async function waitForRoot(timeoutMs = 8_000): Promise<HTMLElement> {
  const t0 = Date.now();
  while (Date.now() - t0 < timeoutMs) {
    const el = findDrapRoot();
    if (el) return el;
    await new Promise((r) => setTimeout(r, 30));
  }
  throw new Error("缺少 #drap-root 容器");
}

async function bootstrap() {
  const alreadyHasHost =
    Boolean(window[DRAP_HOST_BRIDGE_KEY]) ||
    Boolean((window as unknown as { __DAZI_APP_SDK_REGISTRY__?: unknown }).__DAZI_APP_SDK_REGISTRY__);
  if (!alreadyHasHost) {
    installDevHostBridge({
      appId: APP_ID,
      spaceId: "space__0519",
      appearance: "light",
      manifest,
      datasets: fixtureDatasets,
    });
  }
  const lc = await import("./index").then((m) => m.default);
  const container = await waitForRoot();
  const bridge = getHostBridge();
  await lc.mount(container, {
    appId: bridge.appId,
    spaceId: bridge.spaceId,
    appearance: bridge.appearance,
    manifest: bridge.manifest,
    datasets: bridge.getInitialDatasets(),
  });
}

void bootstrap();
`;
}

function writeHtmlFiles(spec, base) {
  write(
    `${base}index.html`,
    `<!doctype html>
<html lang="zh-CN">
  <head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>${spec.name}</title></head>
  <body><div id="drap-root"></div><script type="module" src="/src/dev-entry.tsx"></script></body>
</html>
`,
  );
  write(
    `${base}index.prod.html`,
    `<!doctype html>
<html lang="zh-CN">
  <head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>${spec.name}</title></head>
  <body><div id="drap-root"></div><script type="module" src="/src/prod-entry.tsx"></script></body>
</html>
`,
  );
}

function scaffoldOneFixed(spec) {
  const folder = dirName(spec.id);
  const pkgName = `@dazi/${folder}`;
  const base = `${folder}/`;

  write(`${base}package.json`, `${JSON.stringify(
    {
      name: pkgName,
      version: "0.1.0",
      private: true,
      description: `DRAP 模板：${spec.name}`,
      type: "module",
      scripts: {
        dev: `vite --port ${spec.port} --host`,
        build:
          "vite build && node -e \"require('fs').copyFileSync('dist/index.prod.html','dist/index.html')\"",
        preview: `vite preview --port ${spec.port}`,
      },
      dependencies: {
        "@dazi/app-sdk-core": "workspace:*",
        "@dazi/app-sdk-runtime": "workspace:*",
        "@dazi/app-sdk-data": "workspace:*",
        "@dazi/app-sdk-ui": "workspace:*",
        echarts: "^6.0.0",
        react: "^18.3.1",
        "react-dom": "^18.3.1",
      },
      devDependencies: {
        "@types/react": "^18.3.12",
        "@types/react-dom": "^18.3.1",
        "@vitejs/plugin-react": "^4.3.4",
        typescript: "~5.6.3",
        vite: "^6.0.0",
      },
      drap: { scene_tag: spec.sceneTag, industry: ["通用"] },
    },
    null,
    2,
  )}\n`);

  write(`${base}manifest.json`, manifestJson(spec));
  write(`${base}tsconfig.json`, `{
  "extends": "../../tsconfig.base.json",
  "include": ["src", "manifest.json"],
  "compilerOptions": { "noEmit": true }
}
`);
  write(
    `${base}vite.config.ts`,
    `import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";

export default defineConfig({
  base: process.env.DRAP_ASSET_BASE || "/",
  plugins: [react()],
  server: { port: ${spec.port}, cors: true, headers: { "Access-Control-Allow-Origin": "*" } },
  build: {
    outDir: "dist",
    sourcemap: true,
    target: "es2020",
    rollupOptions: { input: path.resolve(__dirname, "index.prod.html") },
  },
  resolve: { alias: { "@": path.resolve(__dirname, "src") } },
});
`,
  );
  writeHtmlFiles(spec, base);
  write(`${base}.gitignore`, "node_modules\ndist\n*.log\n.DS_Store\n");
  write(
    `${base}README.md`,
    `# ${pkgName}

${spec.name}（DRAP 页模式模板）

\`\`\`powershell
cd dazi/runtime-apps
pnpm install
pnpm --filter ${pkgName} run dev
pnpm --filter ${pkgName} run build
pnpm run dazi-app -- init ${spec.id} --space space__0519
\`\`\`
`,
  );
  write(`${base}src/index.tsx`, indexTsx());
  write(`${base}src/prod-entry.tsx`, prodEntry());
  write(`${base}src/dev-entry.tsx`, devEntry(spec.appId));
  write(`${base}src/fixtures/datasets.ts`, fixturesTs(spec));
  write(`${base}src/pages/MainPage.tsx`, mainPageTsx(spec));
  write(
    `${base}src/styles/template.css`,
    `@import "@dazi/app-sdk-ui/styles.css";

html, body, #drap-root {
  margin: 0;
  padding: 0;
  width: 100%;
  min-height: 100%;
  box-sizing: border-box;
  font-family: "Inter", system-ui, sans-serif;
}

.drap-kpi-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
}
`,
  );
}

function updateCatalog() {
  const catalog = JSON.parse(fs.readFileSync(CATALOG_PATH, "utf8"));
  const readyIds = new Set([
    "profit-analysis-dashboard",
    "chat-kpi-skin",
    "chat-trend-skin",
    ...PLANNED.map((p) => p.id),
  ]);
  for (const t of catalog.templates) {
    if (readyIds.has(t.id)) {
      t.availability = "ready";
      t.source = "local";
      t.source_ref = dirName(t.id);
    }
  }
  catalog.updated_at = new Date().toISOString().slice(0, 10);
  fs.writeFileSync(CATALOG_PATH, JSON.stringify(catalog, null, 2) + "\n", "utf8");
}

function main() {
  const created = [];
  for (const spec of PLANNED) {
    if (SKIP_IDS.has(spec.id)) continue;
    const folder = path.join(TEMPLATES_DIR, dirName(spec.id));
    if (fs.existsSync(folder)) {
      console.log(`skip exists: ${spec.id}`);
      continue;
    }
    scaffoldOneFixed(spec);
    created.push(spec.id);
    console.log(`created: ${spec.id} -> ${dirName(spec.id)} (port ${spec.port})`);
  }
  updateCatalog();
  console.log(`\nDone. Created ${created.length} templates. Updated catalog.json.`);
  console.log("Next: cd dazi/runtime-apps && pnpm install && pnpm -r --filter './templates/*' run build");
}

main();
