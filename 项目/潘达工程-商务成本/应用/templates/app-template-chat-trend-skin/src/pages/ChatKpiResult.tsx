/**
 * 聊天问数 KPI 皮肤：仅展示紧凑 KPI 行，无趋势图/明细表。
 */

import React, { useMemo } from "react";
import { useDataset } from "@dazi/app-sdk-data";
import { KpiCard } from "@dazi/app-sdk-ui";
import { extractKpiCards } from "../lib/kpiFromMessage";

export function ChatKpiResult() {
  const message = useDataset("message");
  const cols = message.data?.columns ?? [];
  const rows = (message.data?.data ?? []) as Record<string, unknown>[];

  const cards = useMemo(() => {
    if (!rows.length) return [];
    return extractKpiCards(rows[0], cols, 4);
  }, [rows, cols]);

  if (message.loading) {
    return (
      <div className="drap-page drap-page--chat" style={{ padding: 12, color: "#6b7280" }}>
        加载问数结果…
      </div>
    );
  }
  if (message.error) {
    return (
      <div className="drap-page drap-page--chat" style={{ padding: 12, color: "#b91c1c" }}>
        {message.error}
      </div>
    );
  }
  if (!rows.length) {
    return (
      <div className="drap-page drap-page--chat" style={{ padding: 12, color: "#6b7280" }}>
        暂无问数数据（宿主未注入 message 数据集）
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
      <div className="drap-kpi-row">
        {cards.map((c) => (
          <KpiCard key={c.key} title={c.title} value={c.value} hint={c.hint} />
        ))}
      </div>
    </div>
  );
}
