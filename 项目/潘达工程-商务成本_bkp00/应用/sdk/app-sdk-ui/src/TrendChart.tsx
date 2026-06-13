/**
 * 基础趋势图：基于 ECharts。echarts 作为 peerDependency。
 *
 * SDK Boundary 提醒：模板代码禁止直接 import 'echarts'；统一通过该组件使用。
 */

import React, { useEffect, useRef } from "react";
import * as echarts from "echarts";
import type { DaziAppDataset } from "@dazi/app-sdk-core";

export interface TrendChartProps {
  dataset?: DaziAppDataset;
  xKey: string;
  yKeys: string[];
  appearance?: "light" | "dark";
  height?: number;
  title?: string;
}

export function TrendChart(props: TrendChartProps) {
  const ref = useRef<HTMLDivElement>(null);
  const instRef = useRef<echarts.ECharts | null>(null);

  useEffect(() => {
    if (!ref.current) return;
    const inst = echarts.init(
      ref.current,
      props.appearance === "dark" ? "dark" : undefined,
    );
    instRef.current = inst;
    const onResize = () => inst.resize();
    window.addEventListener("resize", onResize);
    const ro =
      typeof ResizeObserver !== "undefined" && ref.current
        ? new ResizeObserver(() => inst.resize())
        : null;
    ro?.observe(ref.current);
    return () => {
      window.removeEventListener("resize", onResize);
      ro?.disconnect();
      inst.dispose();
      instRef.current = null;
    };
  }, [props.appearance]);

  useEffect(() => {
    const inst = instRef.current;
    if (!inst) return;
    const rows = props.dataset?.data ?? [];
    const xData = rows.map((r) => String(r[props.xKey] ?? ""));
    const series = props.yKeys.map((k) => ({
      name: k,
      type: "line" as const,
      smooth: true,
      data: rows.map((r) => Number(r[k] ?? 0)),
    }));
    inst.setOption({
      title: props.title ? { text: props.title, left: 0, top: 0 } : undefined,
      tooltip: { trigger: "axis" },
      legend: { data: props.yKeys, top: props.title ? 24 : 0 },
      grid: { left: 40, right: 16, top: props.title ? 56 : 32, bottom: 28 },
      xAxis: { type: "category", data: xData, boundaryGap: false },
      yAxis: { type: "value" },
      series,
    });
  }, [props.dataset, props.xKey, props.yKeys, props.title]);

  if (!props.dataset || props.dataset.data.length === 0) {
    return <div className="drap-empty">暂无数据</div>;
  }
  return (
    <div
      ref={ref}
      className="drap-chart"
      style={{ height: props.height ?? 320 }}
    />
  );
}
