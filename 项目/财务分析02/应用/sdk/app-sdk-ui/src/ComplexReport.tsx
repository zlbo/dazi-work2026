/**
 * 中国式复杂报表：优先用 RLIR headerCells（Excel 合并格），否则回退 columnGroups。
 */

import React, { useEffect, useMemo, useRef, useState } from "react";
import type { DaziAppDataset } from "@dazi/app-sdk-core";
import { renderHeaderRows, type ReportHeaderCell } from "./complexReportHeader";

export interface ReportLayoutColumn {
  id: string;
  field: string;
  label?: string;
  colIndex?: number;
  align?: "left" | "right" | "center";
  format?: string | null;
  parentId?: string | null;
  visible?: boolean;
  leaf?: boolean;
}

export interface ReportLayoutGroup {
  id: string;
  label: string;
  children: string[];
}

export interface ReportLayoutIR {
  title?: string;
  summary?: string;
  columns?: ReportLayoutColumn[];
  columnGroups?: ReportLayoutGroup[];
  headerCells?: ReportHeaderCell[];
  headerRowCount?: number;
  wideTable?: {
    defaultVisibleColumns?: number;
    columnPicker?: boolean;
  };
}

export interface ComplexReportProps {
  layout: ReportLayoutIR;
  dataset?: DaziAppDataset;
  emptyText?: string;
  maxHeight?: number;
  onVisibleFieldsChange?: (fields: string[]) => void;
  pagination?: {
    page: number;
    pageSize: number;
    totalRows?: number;
    onPageChange: (page: number) => void;
  };
}

function formatCell(v: unknown, format?: string | null): string {
  if (v == null) return "";
  if (format === "number" && typeof v === "number") {
    return v.toLocaleString("zh-CN");
  }
  const n = Number(v);
  if (format === "number" && !Number.isNaN(n)) {
    return n.toLocaleString("zh-CN");
  }
  return String(v);
}

function sortByColIndex(cols: ReportLayoutColumn[]): ReportLayoutColumn[] {
  return [...cols].sort((a, b) => (a.colIndex ?? 9999) - (b.colIndex ?? 9999));
}

function resolveRowValue(
  row: Record<string, unknown>,
  col: ReportLayoutColumn,
  colPos: number,
  datasetColumns?: string[],
): unknown {
  if (col.field in row) return row[col.field];
  if (col.label && col.label in row) return row[col.label];
  if (datasetColumns && datasetColumns[colPos] !== undefined) {
    const key = datasetColumns[colPos];
    if (key in row) return row[key];
  }
  const keys = Object.keys(row);
  if (keys[colPos] !== undefined) return row[keys[colPos]];
  return undefined;
}

export function ComplexReport(props: ComplexReportProps) {
  const layout = props.layout;
  const allCols = sortByColIndex((layout.columns ?? []).filter((c) => c.field));
  const headerCells = (layout.headerCells ?? []) as ReportHeaderCell[];
  const useMatrixHeader = headerCells.length > 0;

  const defaultVisible = layout.wideTable?.defaultVisibleColumns ?? 24;
  const pickerEnabled =
    layout.wideTable?.columnPicker !== false && allCols.length > defaultVisible;

  const [visibleIds, setVisibleIds] = useState<Set<string>>(() => {
    const init = new Set<string>();
    let n = 0;
    for (const c of allCols) {
      if (c.visible === false) continue;
      init.add(c.id);
      n += 1;
      if (n >= defaultVisible) break;
    }
    if (init.size === 0) {
      allCols.slice(0, defaultVisible).forEach((c) => init.add(c.id));
    }
    return init;
  });

  const visibleColumns = useMemo(
    () => sortByColIndex(allCols.filter((c) => visibleIds.has(c.id))),
    [allCols, visibleIds],
  );

  const lastVisibleFieldsRef = useRef("");
  useEffect(() => {
    const fields = visibleColumns.map((c) => c.field);
    const sig = fields.join("\0");
    if (sig === lastVisibleFieldsRef.current) return;
    lastVisibleFieldsRef.current = sig;
    props.onVisibleFieldsChange?.(fields);
  }, [visibleColumns, props.onVisibleFieldsChange]);

  const groups = layout.columnGroups ?? [];
  const hasGroupRow =
    !useMatrixHeader &&
    groups.some((g) => g.children.some((cid) => visibleIds.has(cid)));

  const rows = props.dataset?.data ?? [];
  const datasetColumns = props.dataset?.columns;

  const toggleColumn = (id: string) => {
    setVisibleIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  if (allCols.length === 0) {
    return <div className="drap-empty">{props.emptyText ?? "未配置报表列"}</div>;
  }

  const theadContent = useMatrixHeader ? (
    renderHeaderRows(headerCells)
  ) : (
    <>
      {hasGroupRow && (
        <tr>
          {groups.map((g) => {
            const childCols = g.children.filter((cid) => visibleIds.has(cid));
            if (childCols.length === 0) return null;
            const label =
              g.label ||
              visibleColumns.find((c) => c.id === childCols[0])?.label ||
              g.id;
            return (
              <th
                key={g.id}
                colSpan={childCols.length}
                style={{ textAlign: "center" }}
              >
                {label}
              </th>
            );
          })}
          {visibleColumns
            .filter(
              (c) =>
                !c.parentId || !groups.some((g) => g.children.includes(c.id)),
            )
            .map((c) => (
              <th key={`solo-${c.id}`} rowSpan={hasGroupRow ? 2 : undefined}>
                {c.label ?? c.field}
              </th>
            ))}
        </tr>
      )}
      <tr>
        {visibleColumns.map((c) => {
          if (hasGroupRow && c.parentId) {
            return (
              <th key={c.id} style={{ textAlign: c.align ?? "left" }}>
                {c.label ?? c.field}
              </th>
            );
          }
          if (
            hasGroupRow &&
            !c.parentId &&
            groups.some((g) => g.children.includes(c.id))
          ) {
            return null;
          }
          if (hasGroupRow) return null;
          return (
            <th key={c.id} style={{ textAlign: c.align ?? "left" }}>
              {c.label ?? c.field}
            </th>
          );
        })}
      </tr>
    </>
  );

  return (
    <div className="drap-complex-report">
      {pickerEnabled && (
        <details className="drap-complex-report__picker" style={{ marginBottom: 8 }}>
          <summary style={{ cursor: "pointer", fontSize: 13 }}>
            列选择（{visibleColumns.length}/{allCols.length}）
          </summary>
          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: 6,
              marginTop: 6,
              maxHeight: 120,
              overflow: "auto",
            }}
          >
            {allCols.map((c) => (
              <label
                key={c.id}
                style={{
                  fontSize: 12,
                  display: "inline-flex",
                  alignItems: "center",
                  gap: 4,
                }}
              >
                <input
                  type="checkbox"
                  checked={visibleIds.has(c.id)}
                  onChange={() => toggleColumn(c.id)}
                />
                {c.label ?? c.field}
              </label>
            ))}
          </div>
        </details>
      )}

      <div
        className="drap-complex-report__scroll"
        style={{ maxHeight: props.maxHeight ?? 560, overflow: "auto" }}
      >
        <table className="drap-table drap-complex-report__table">
          <thead className="drap-complex-report__thead">{theadContent}</thead>
          <tbody>
            {rows.length === 0 ? (
              <tr>
                <td colSpan={visibleColumns.length}>
                  {props.emptyText ?? "暂无数据"}
                </td>
              </tr>
            ) : (
              rows.map((r, i) => (
                <tr key={i}>
                  {visibleColumns.map((c, colPos) => (
                    <td
                      key={c.id}
                      style={{ textAlign: c.align ?? "left", whiteSpace: "nowrap" }}
                    >
                      {formatCell(
                        resolveRowValue(r, c, colPos, datasetColumns),
                        c.format,
                      )}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
      {props.pagination && (
        <div
          className="drap-complex-report__pager"
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            marginTop: 8,
            fontSize: 13,
          }}
        >
          <button
            type="button"
            disabled={props.pagination.page <= 1}
            onClick={() =>
              props.pagination!.onPageChange(props.pagination!.page - 1)
            }
            style={{ padding: "2px 10px" }}
          >
            上一页
          </button>
          <span>
            第 {props.pagination.page} 页
            {props.pagination.totalRows != null
              ? ` · 约 ${props.pagination.totalRows} 行`
              : ` · 本页 ${rows.length} 行`}
          </span>
          <button
            type="button"
            disabled={rows.length < props.pagination.pageSize}
            onClick={() =>
              props.pagination!.onPageChange(props.pagination!.page + 1)
            }
            style={{ padding: "2px 10px" }}
          >
            下一页
          </button>
        </div>
      )}
    </div>
  );
}
