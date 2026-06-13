import React from "react";
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
    <PageLayout title="财务趋势看板" appearance={appearance}>
      <div className="drap-kpi-row" style={{ marginBottom: 16 }}>
        <KpiCard title="营收" value={fmt(row.revenue)} />
        <KpiCard title="利润" value={fmt(row.profit)} />
        <KpiCard title="利润率" value={`${fmt(row.margin_pct)}%`} />
      </div>
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
