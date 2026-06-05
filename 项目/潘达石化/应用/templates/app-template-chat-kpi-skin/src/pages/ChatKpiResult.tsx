/**
 * 问数 KPI 展示：message 问数注入优先，页模式回退 manifest 内联/其它数据源预览。
 */

import React, { useMemo } from "react";
import { useResultDataset } from "@dazi/app-sdk-data";
import { KpiCard } from "@dazi/app-sdk-ui";
import { extractKpiCards } from "../lib/kpiFromMessage";

export function ChatKpiResult() {
  const result = useResultDataset();
  const cols = result.data?.columns ?? [];
  const rows = (result.data?.data ?? []) as Record<string, unknown>[];

  const cards = useMemo(() => {
    if (!rows.length) return [];
    return extractKpiCards(rows[0], cols, 4);
  }, [rows, cols]);

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
  if (!cards.length) {
    return (
      <div className="drap-page drap-page--chat" style={{ padding: 12, color: "#6b7280" }}>
        当前结果行无数值列，无法生成 KPI 卡片
      </div>
    );
  }

  return (
    <div className="drap-page drap-page--chat" style={{ padding: "8px 4px 4px" }}>
      {result.isPreview ? (
        <p style={{ margin: "0 0 8px", fontSize: 12, color: "#9ca3af" }}>
          预览数据（数据源：{result.sourceKey}）
        </p>
      ) : null}
      <div className="drap-kpi-row">
        {cards.map((c) => (
          <KpiCard key={c.key} title={c.title} value={c.value} hint={c.hint} />
        ))}
      </div>
    </div>
  );
}
