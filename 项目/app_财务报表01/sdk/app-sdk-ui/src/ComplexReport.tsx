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
  /** 同列相邻相同值纵向合并（空值沿用上一行） */
  rowMerge?: boolean;
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

function findGroupForColumn(
  col: ReportLayoutColumn,
  groups: ReportLayoutGroup[],
): ReportLayoutGroup | undefined {
  return groups.find((g) => g.children.includes(col.id));
}

function colCellClass(col: ReportLayoutColumn, extra?: string): string {
  const parts = ["drap-complex-report__cell", `drap-complex-report__cell--${col.id}`];
  if (extra) parts.push(extra);
  return parts.join(" ");
}

type HeaderZone = "dim" | "year" | "monthly";

function headerZone(col: ReportLayoutColumn): HeaderZone {
  if (col.field === "category" || col.field === "indicator") return "dim";
  if (col.parentId) return "monthly";
  return "year";
}

function monthlyGroupId(
  col: ReportLayoutColumn,
  groups: ReportLayoutGroup[],
): string | undefined {
  return findGroupForColumn(col, groups)?.id;
}

function isMonthlyGroupLead(
  col: ReportLayoutColumn,
  groups: ReportLayoutGroup[],
): boolean {
  const g = findGroupForColumn(col, groups);
  return g?.children[0] === col.id;
}

function isMonthlyGroupTail(
  col: ReportLayoutColumn,
  groups: ReportLayoutGroup[],
): boolean {
  const g = findGroupForColumn(col, groups);
  if (!g) return false;
  return g.children[g.children.length - 1] === col.id;
}

function headerCellClass(
  col: ReportLayoutColumn,
  groups: ReportLayoutGroup[],
  opts?: {
    zoneStart?: boolean;
    groupStart?: boolean;
    groupEnd?: boolean;
    rowMerge?: boolean;
  },
): string {
  const zone = headerZone(col);
  const parts = [
    colCellClass(col, opts?.rowMerge ? "drap-complex-report__cell--row-merge" : undefined),
    "drap-complex-report__head",
    `drap-complex-report__head--${zone}`,
  ];
  const bandId = monthlyGroupId(col, groups);
  if (bandId) parts.push(`drap-complex-report__monthly-band--${bandId}`);
  if (opts?.zoneStart) parts.push("drap-complex-report__head--zone-start");
  if (opts?.groupStart) parts.push("drap-complex-report__head--group-start");
  if (opts?.groupEnd) parts.push("drap-complex-report__head--group-end");
  return parts.join(" ");
}

function bodyCellClass(
  col: ReportLayoutColumn,
  groups: ReportLayoutGroup[],
  opts?: {
    zoneStart?: boolean;
    groupStart?: boolean;
    groupEnd?: boolean;
    rowMerge?: boolean;
  },
): string {
  const zone = headerZone(col);
  const parts = [
    colCellClass(col, opts?.rowMerge ? "drap-complex-report__cell--row-merge" : undefined),
    "drap-complex-report__body",
    `drap-complex-report__body--${zone}`,
  ];
  const bandId = monthlyGroupId(col, groups);
  if (bandId) parts.push(`drap-complex-report__monthly-band--${bandId}`);
  if (opts?.zoneStart) parts.push("drap-complex-report__body--zone-start");
  if (opts?.groupStart) parts.push("drap-complex-report__body--group-start");
  if (opts?.groupEnd) parts.push("drap-complex-report__body--group-end");
  return parts.join(" ");
}

function isHeaderZoneStart(
  col: ReportLayoutColumn,
  prev: ReportLayoutColumn | null,
): boolean {
  if (!prev) return false;
  return headerZone(prev) !== headerZone(col);
}

/** 分月区第一组的第一个子列（用于表体竖向分隔） */
function isFirstMonthlyColumn(
  col: ReportLayoutColumn,
  visibleColumns: ReportLayoutColumn[],
): boolean {
  if (headerZone(col) !== "monthly") return false;
  const firstMonthly = visibleColumns.find((c) => headerZone(c) === "monthly");
  return firstMonthly?.id === col.id;
}

/** 按 visibleColumns 顺序渲染多级表头，避免分组列排在独立列之前导致错位 */
function renderGroupHeaderRows(
  visibleColumns: ReportLayoutColumn[],
  groups: ReportLayoutGroup[],
  visibleIds: Set<string>,
): React.ReactNode {
  const emittedGroupIds = new Set<string>();
  const topRow: React.ReactNode[] = [];
  let prevSolo: ReportLayoutColumn | null = null;

  for (const c of visibleColumns) {
    if (c.parentId) {
      const g = findGroupForColumn(c, groups);
      if (!g || emittedGroupIds.has(g.id)) continue;
      const childCount = g.children.filter((cid) => visibleIds.has(cid)).length;
      if (childCount === 0) continue;
      const isFirstMonthlyGroup = emittedGroupIds.size === 0;
      emittedGroupIds.add(g.id);
      const label =
        g.label ||
        visibleColumns.find((col) => col.id === g.children[0])?.label ||
        g.id;
      const zoneStart = prevSolo == null || headerZone(prevSolo) !== "monthly";
      topRow.push(
        <th
          key={g.id}
          colSpan={childCount}
          className={[
            "drap-complex-report__head",
            "drap-complex-report__head--monthly-group",
            `drap-complex-report__monthly-band--${g.id}`,
            zoneStart ? "drap-complex-report__head--zone-start" : "",
            !isFirstMonthlyGroup ? "drap-complex-report__head--group-start" : "",
          ]
            .filter(Boolean)
            .join(" ")}
          style={{ textAlign: "center" }}
        >
          {label}
        </th>,
      );
      prevSolo = c;
      continue;
    }
    topRow.push(
      <th
        key={`solo-${c.id}`}
        className={headerCellClass(c, groups, {
          zoneStart: isHeaderZoneStart(c, prevSolo),
        })}
        rowSpan={2}
      >
        {c.label ?? c.field}
      </th>,
    );
    prevSolo = c;
  }

  let prevSub: ReportLayoutColumn | null = null;
  const subRow = visibleColumns
    .filter((c) => c.parentId)
    .map((c) => {
      const isGroupLead = isMonthlyGroupLead(c, groups);
      const isGroupTail = isMonthlyGroupTail(c, groups);
      const zoneStart =
        isHeaderZoneStart(c, prevSub) || isFirstMonthlyColumn(c, visibleColumns);
      const groupStart = isGroupLead && !isFirstMonthlyColumn(c, visibleColumns);
      prevSub = c;
      return (
        <th
          key={c.id}
          className={headerCellClass(c, groups, {
            zoneStart,
            groupStart,
            groupEnd: isGroupTail,
          })}
          style={{ textAlign: c.align ?? "center" }}
        >
          {c.label ?? c.field}
        </th>
      );
    });

  return (
    <>
      <tr className="drap-complex-report__head-row drap-complex-report__head-row--top">
        {topRow}
      </tr>
      <tr className="drap-complex-report__head-row drap-complex-report__head-row--sub">
        {subRow}
      </tr>
    </>
  );
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

/** 每行：>0 表示该行起始 rowspan；0 表示被上方合并格覆盖，跳过渲染 */
function computeRowMergeSpans(
  rows: Record<string, unknown>[],
  col: ReportLayoutColumn,
  colPos: number,
  datasetColumns?: string[],
): number[] {
  if (rows.length === 0) return [];

  const effective: unknown[] = [];
  let carry: unknown = undefined;
  for (let i = 0; i < rows.length; i++) {
    const raw = resolveRowValue(rows[i], col, colPos, datasetColumns);
    if (raw != null && raw !== "") {
      carry = raw;
    }
    effective.push(carry);
  }

  const spans = new Array<number>(rows.length).fill(0);
  let i = 0;
  while (i < rows.length) {
    const current = effective[i];
    let run = 1;
    while (i + run < rows.length && effective[i + run] === current) {
      run += 1;
    }
    spans[i] = run;
    i += run;
  }
  return spans;
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

  const rowMergeSpansByColId = useMemo(() => {
    const map = new Map<string, number[]>();
    visibleColumns.forEach((col, colPos) => {
      if (col.rowMerge) {
        map.set(col.id, computeRowMergeSpans(rows, col, colPos, datasetColumns));
      }
    });
    return map;
  }, [visibleColumns, rows, datasetColumns]);

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
  ) : hasGroupRow ? (
    renderGroupHeaderRows(visibleColumns, groups, visibleIds)
  ) : (
    <tr className="drap-complex-report__head-row">
      {visibleColumns.map((c, i) => (
        <th
          key={c.id}
          className={headerCellClass(c, groups, {
            zoneStart: isHeaderZoneStart(c, visibleColumns[i - 1] ?? null),
          })}
          style={{ textAlign: c.align ?? "left" }}
        >
          {c.label ?? c.field}
        </th>
      ))}
    </tr>
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
                  {visibleColumns.map((c, colPos) => {
                    const zoneStart =
                      isHeaderZoneStart(c, visibleColumns[colPos - 1] ?? null) ||
                      isFirstMonthlyColumn(c, visibleColumns);
                    const groupStart =
                      isMonthlyGroupLead(c, groups) &&
                      !isFirstMonthlyColumn(c, visibleColumns);
                    const groupEnd = isMonthlyGroupTail(c, groups);
                    const mergeSpans = rowMergeSpansByColId.get(c.id);
                    if (mergeSpans) {
                      const span = mergeSpans[i];
                      if (span === 0) return null;
                      const value = resolveRowValue(r, c, colPos, datasetColumns);
                      return (
                        <td
                          key={c.id}
                          rowSpan={span > 1 ? span : undefined}
                          className={bodyCellClass(c, groups, {
                            zoneStart,
                            groupStart,
                            groupEnd,
                            rowMerge: true,
                          })}
                          style={{
                            textAlign: c.align ?? "left",
                            whiteSpace: "nowrap",
                            verticalAlign: "middle",
                          }}
                        >
                          {formatCell(value, c.format)}
                        </td>
                      );
                    }
                    return (
                      <td
                        key={c.id}
                        className={bodyCellClass(c, groups, {
                          zoneStart,
                          groupStart,
                          groupEnd,
                        })}
                        style={{ textAlign: c.align ?? "left", whiteSpace: "nowrap" }}
                      >
                        {formatCell(
                          resolveRowValue(r, c, colPos, datasetColumns),
                          c.format,
                        )}
                      </td>
                    );
                  })}
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
