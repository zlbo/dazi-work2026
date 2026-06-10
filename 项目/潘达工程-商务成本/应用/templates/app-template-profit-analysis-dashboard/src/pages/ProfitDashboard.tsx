/**
 * 利润分析看板页面。
 *
 * 数据来源：
 *   - `kpi`     →  KPI 卡片
 *   - `trend`   →  TrendChart（月度营收/利润趋势）
 *   - `yoy_table` → DataGrid（同比对比表）
 *
 * 数据访问统一通过 `useDataset` / `useSemanticQuery`，禁止裸 fetch；
 * 视觉统一用 `@dazi/app-sdk-ui` 组件，禁止直接 import 'echarts'。
 */

import React from "react";
import { useDataset } from "@dazi/app-sdk-data";
import { useAppearance } from "@dazi/app-sdk-runtime";
import {
  Card,
  DataGrid,
  KpiCard,
  PageLayout,
  TrendChart,
} from "@dazi/app-sdk-ui";
import {
  buildTrendChartDataset,
  buildYoyTableFromTrend,
  parseFc02KpiRow,
} from "../lib/fc02Dataset";

function fmtMoney(n: number | string | undefined) {
  const v = Number(n ?? 0);
  if (!Number.isFinite(v)) return "—";
  if (Math.abs(v) >= 10_000) {
    return `${(v / 10_000).toFixed(1)} 万`;
  }
  return v.toLocaleString("zh-CN");
}

/** 从 yoy_table 数据集读取「同比%」（维度列名：营收 / 利润 / 利润率） */
function yoyTrend(
  rows: Record<string, unknown>[] | undefined,
  dimension: string,
): number | undefined {
  if (!rows?.length) return undefined;
  const row = rows.find((r) => String(r["维度"] ?? r.dimension ?? "") === dimension);
  if (!row) return undefined;
  const v = Number(row["同比%"] ?? row.yoy_pct ?? row.trend);
  return Number.isFinite(v) ? v : undefined;
}

export function ProfitDashboard() {
  const appearance = useAppearance();
  const kpi = useDataset("kpi");
  const trend = useDataset("trend");
  const yoy = useDataset("yoy_table");

  const k = parseFc02KpiRow((kpi.data?.data?.[0] ?? {}) as Record<string, unknown>);
  const { revenue, profit, profitRate } = k;
  const trendChart = buildTrendChartDataset(trend.data);
  const yoyDerived = buildYoyTableFromTrend(trendChart);
  const yoyDisplay = yoyDerived ?? yoy.data;
  const yoyRows = yoyDisplay?.data;

  return (
    <PageLayout
      title="利润分析"
      appearance={appearance}
      toolbar={
        <button
          onClick={() => {
            void kpi.refetch();
            void trend.refetch();
            void yoy.refetch();
          }}
          style={{
            padding: "4px 10px",
            border: "1px solid var(--drap-card-border)",
            borderRadius: 6,
            background: "transparent",
            color: "inherit",
            cursor: "pointer",
            fontSize: 12,
          }}
        >
          刷新
        </button>
      }
    >
      <div className="drap-grid">
        <KpiCard
          title="营业收入"
          value={fmtMoney(revenue)}
          hint="月预算口径"
        />
        <KpiCard
          title="净利润"
          value={fmtMoney(profit)}
          trend={yoyTrend(yoyRows, "利润")}
          hint="实际利润"
        />
        <KpiCard
          title="利润率"
          value={`${profitRate.toFixed(1)}%`}
          hint="预算达成率"
        />
      </div>

      <Card title="月度利润趋势（FC02）">
        <TrendChart
          dataset={trendChart}
          xKey="month"
          yKeys={["profit"]}
          appearance={appearance}
        />
      </Card>

      <Card title="同环比对比">
        <DataGrid
          dataset={yoyDisplay}
          columns={[
            { key: "维度", label: "维度" },
            { key: "本期", label: "本期", align: "right", format: (v) => fmtMoney(v as number) },
            { key: "上期", label: "上期", align: "right", format: (v) => fmtMoney(v as number) },
            { key: "同比%", label: "同比%", align: "right", format: (v) => `${Number(v ?? 0).toFixed(2)}%` },
          ]}
        />
      </Card>
    </PageLayout>
  );
}
