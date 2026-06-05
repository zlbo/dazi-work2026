/**
 * 问数/利润结果展示：message 问数注入优先，页模式回退 manifest 内联预览。
 */

import React, { useMemo } from "react";
import { useResultDataset } from "@dazi/app-sdk-data";
import { useAppearance } from "@dazi/app-sdk-runtime";
import { Card, DataGrid, KpiCard, TrendChart } from "@dazi/app-sdk-ui";
import type { DaziAppDataset } from "@dazi/app-sdk-core";
import { parseFc02KpiRow } from "../lib/fc02Dataset";

const FC02_LABELS: Record<string, string> = {
  year_month: "分析年月",
  version_id: "预算版本",
  actual_total: "实际利润",
  budget_total: "月预算",
  achievement_rate: "达成率",
};

function fmtMoney(n: number | string | undefined) {
  const v = Number(n ?? 0);
  if (!Number.isFinite(v)) return "—";
  if (Math.abs(v) >= 10_000) return `${(v / 10_000).toFixed(1)} 万`;
  return Math.abs(v).toLocaleString("zh-CN");
}

function colLabel(key: string): string {
  return FC02_LABELS[key] ?? key;
}

function buildBudgetVsActualChart(kpi: {
  revenue: number;
  profit: number;
}): DaziAppDataset {
  return {
    columns: ["item", "amount"],
    data: [
      { item: "月预算", amount: kpi.revenue },
      { item: "实际利润", amount: kpi.profit },
    ],
    row_count: 2,
    meta: { kind: "static", ok: true },
  };
}

export function ChatProfitResult() {
  const appearance = useAppearance();
  const result = useResultDataset();
  const cols = result.data?.columns ?? [];
  const rows = (result.data?.data ?? []) as Record<string, unknown>[];

  const fc02Kpi = useMemo(() => {
    if (!rows.length) return null;
    return parseFc02KpiRow(rows[0]);
  }, [rows]);

  const compareChart = useMemo(
    () => (fc02Kpi ? buildBudgetVsActualChart(fc02Kpi) : null),
    [fc02Kpi],
  );

  if (result.loading) {
    return (
      <div className="drap-page drap-page--chat" style={{ padding: 12, color: "#6b7280" }}>
        加载数据…
      </div>
    );
  }
  if (result.error) {
    return (
      <div className="drap-page drap-page--chat" style={{ padding: 12, color: "#b91c1c" }}>
        {result.error}
      </div>
    );
  }
  if (!rows.length) {
    return (
      <div className="drap-page drap-page--chat" style={{ padding: 12, color: "#6b7280" }}>
        暂无展示数据（可在 manifest 的 message 或其它 data_sources 中配置 static 预览行）
      </div>
    );
  }

  return (
    <div
      className="drap-page drap-page--chat"
      style={{ display: "flex", flexDirection: "column", gap: 12, paddingBottom: 4 }}
    >
      {result.isPreview ? (
        <p style={{ margin: 0, fontSize: 12, color: "#9ca3af" }}>
          预览数据（数据源：{result.sourceKey}）
        </p>
      ) : null}
      {fc02Kpi ? (
        <div
          className="drap-grid"
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
            gap: 12,
          }}
        >
          <KpiCard title="月预算" value={fmtMoney(fc02Kpi.revenue)} hint="FC02" />
          <KpiCard title="实际利润" value={fmtMoney(fc02Kpi.profit)} hint="当月" />
          <KpiCard title="达成率" value={`${fc02Kpi.profitRate.toFixed(1)}%`} hint="实际/预算" />
        </div>
      ) : null}
      {compareChart ? (
        <Card title="预算 vs 实际（当月）">
          <TrendChart
            dataset={compareChart}
            xKey="item"
            yKeys={["amount"]}
            appearance={appearance}
            height={200}
          />
        </Card>
      ) : null}
      <Card title={result.isPreview ? "数据明细（预览）" : "问数明细"}>
        <DataGrid
          dataset={result.data}
          columns={cols.map((c) => ({ key: c, label: colLabel(c) }))}
        />
      </Card>
    </div>
  );
}
