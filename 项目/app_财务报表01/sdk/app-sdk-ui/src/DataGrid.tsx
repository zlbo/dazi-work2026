/**
 * P0 极简网格：仅展示。
 * 列定义可选，未传时自动从 dataset.columns 推断；可定义 align / format。
 */

import React from "react";
import type { DaziAppDataset } from "@dazi/app-sdk-core";

export interface DataGridColumn {
  key: string;
  label?: string;
  align?: "left" | "right" | "center";
  format?: (v: unknown, row: Record<string, unknown>) => React.ReactNode;
}

export interface DataGridProps {
  dataset?: DaziAppDataset;
  columns?: DataGridColumn[];
  emptyText?: string;
  maxHeight?: number;
}

export function DataGrid(props: DataGridProps) {
  const rows = props.dataset?.data ?? [];
  const cols: DataGridColumn[] =
    props.columns && props.columns.length > 0
      ? props.columns
      : (props.dataset?.columns ?? []).map((k) => ({ key: k, label: k }));

  if (rows.length === 0) {
    return <div className="drap-empty">{props.emptyText ?? "暂无数据"}</div>;
  }
  return (
    <div style={{ maxHeight: props.maxHeight, overflow: "auto" }}>
      <table className="drap-table">
        <thead>
          <tr>
            {cols.map((c) => (
              <th key={c.key} style={{ textAlign: c.align ?? "left" }}>
                {c.label ?? c.key}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i}>
              {cols.map((c) => (
                <td key={c.key} style={{ textAlign: c.align ?? "left" }}>
                  {c.format ? c.format(r[c.key], r) : String(r[c.key] ?? "")}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
