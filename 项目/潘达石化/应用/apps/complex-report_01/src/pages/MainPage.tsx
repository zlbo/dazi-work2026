import React, { useMemo, useState } from "react";
import { useReportDataset } from "@dazi/app-sdk-data";
import { useAppearance, useHostBridge } from "@dazi/app-sdk-runtime";
import { ComplexReport, PageLayout, type ReportLayoutIR } from "@dazi/app-sdk-ui";
import { financialReportLayout } from "../fixtures/reportLayout";

export function MainPage() {
  const appearance = useAppearance();
  const bridge = useHostBridge();
  const [visibleFields, setVisibleFields] = useState<string[]>([]);

  const layout = useMemo((): ReportLayoutIR => {
    const manifest = bridge?.manifest as Record<string, unknown> | undefined;
    const rd = manifest?.report_design as Record<string, unknown> | undefined;
    const snap = rd?.layout_snapshot as ReportLayoutIR | undefined;
    return snap ?? financialReportLayout;
  }, [bridge?.manifest]);

  const ds = useReportDataset({
    visibleFields,
  });

  return (
    <PageLayout
      title={layout.title ?? "中国式复杂报表"}
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
      {layout.summary && (
        <p style={{ color: "#6b7280", fontSize: 13, marginBottom: 12 }}>{layout.summary}</p>
      )}
      {ds.loading && <p style={{ color: "#6b7280" }}>加载中…</p>}
      {ds.error && <p style={{ color: "#b91c1c" }}>{ds.error}</p>}
      <ComplexReport
        layout={layout}
        dataset={ds.data}
        maxHeight={640}
        onVisibleFieldsChange={(fields) => {
          setVisibleFields(fields);
          ds.setPage(1);
        }}
        pagination={{
          page: ds.page,
          pageSize: ds.pageSize,
          onPageChange: (p) => ds.setPage(p),
        }}
      />
    </PageLayout>
  );
}
