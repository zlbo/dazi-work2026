import React from "react";
import { useDataset } from "@dazi/app-sdk-data";
import { useAppearance } from "@dazi/app-sdk-runtime";
import { KpiCard, PageLayout } from "@dazi/app-sdk-ui";

export function MainPage() {
  const appearance = useAppearance();
  const ds = useDataset("metrics");
  const rows = ds.data?.data ?? [];

  return (
    <PageLayout title="实时监控" appearance={appearance}>
      <div className="drap-kpi-row">
        {rows.map((r, i) => (
          <KpiCard
            key={String(r.label ?? i)}
            title={String(r.label ?? "指标")}
            value={String(r.value ?? "—") + (r.unit ? ` ${String(r.unit)}` : "")}
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
