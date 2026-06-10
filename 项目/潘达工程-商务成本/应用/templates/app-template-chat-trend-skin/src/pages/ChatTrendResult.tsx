/**
 * 趋势展示：message 问数注入优先，页模式回退 manifest 内联/其它数据源预览。
 */

import React, { useMemo } from "react";
import { useResultDataset } from "@dazi/app-sdk-data";
import { useAppearance } from "@dazi/app-sdk-runtime";
import { TrendChart } from "@dazi/app-sdk-ui";
import { inferTrendAxes } from "../lib/trendFromMessage";

export function ChatTrendResult() {
  const result = useResultDataset({ fallbackKeys: ["trend"] });
  const appearance = useAppearance();
  const cols = result.data?.columns ?? [];
  const rows = (result.data?.data ?? []) as Record<string, unknown>[];

  const axes = useMemo(() => inferTrendAxes(cols, rows), [cols, rows]);

  const dataset = useMemo(
    () =>
      result.data
        ? {
            columns: cols,
            data: rows,
            row_count: rows.length,
            meta: result.data.meta,
          }
        : undefined,
    [result.data, cols, rows],
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
  if (!axes) {
    return (
      <div className="drap-page drap-page--chat" style={{ padding: 12, color: "#6b7280" }}>
        无法推断趋势图维度（需至少一列分类 + 一列数值）
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
      <TrendChart
        dataset={dataset}
        xKey={axes.xKey}
        yKeys={axes.yKeys}
        appearance={appearance}
        height={result.isPreview ? 320 : 240}
        title={result.isPreview ? "数据趋势（预览）" : "问数趋势"}
      />
    </div>
  );
}
