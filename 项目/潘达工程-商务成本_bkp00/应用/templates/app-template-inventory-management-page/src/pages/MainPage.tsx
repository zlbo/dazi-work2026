import React from "react";
import { useDataset } from "@dazi/app-sdk-data";
import { useAppearance } from "@dazi/app-sdk-runtime";
import { DataGrid, PageLayout } from "@dazi/app-sdk-ui";

export function MainPage() {
  const appearance = useAppearance();
  const ds = useDataset("inventory");

  return (
    <PageLayout
      title="库存管理"
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
