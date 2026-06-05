import React from "react";

export interface KpiCardProps {
  title: string;
  value: number | string;
  /** 同/环比数值，正负号决定颜色与箭头 */
  trend?: number;
  /** 趋势单位，默认 % */
  trendUnit?: string;
  hint?: string;
}

function formatTrend(t: number, unit: string) {
  const arrow = t > 0 ? "▲" : t < 0 ? "▼" : "•";
  return `${arrow} ${Math.abs(t).toFixed(2)}${unit}`;
}

export function KpiCard(props: KpiCardProps) {
  const { title, value, trend, trendUnit = "%", hint } = props;
  return (
    <div className="drap-kpi">
      <div className="drap-kpi__title">{title}</div>
      <div className="drap-kpi__value">{value}</div>
      {typeof trend === "number" && (
        <div
          className={
            "drap-kpi__trend " +
            (trend > 0
              ? "drap-kpi__trend--up"
              : trend < 0
                ? "drap-kpi__trend--down"
                : "")
          }
        >
          {formatTrend(trend, trendUnit)}
          {hint ? ` · ${hint}` : ""}
        </div>
      )}
    </div>
  );
}
