/**
 * 从 RLIR headerCells 渲染多级表头（与 Excel 合并格一致）。
 */

import React from "react";

export interface ReportHeaderCell {
  row: number;
  col: number;
  rowSpan: number;
  colSpan: number;
  label: string;
}

/** 按行输出 <tr>，仅包含锚点单元格（合并格左上角） */
export function renderHeaderRows(cells: ReportHeaderCell[]): React.ReactNode[] {
  if (!cells.length) return [];

  const byRow = new Map<number, ReportHeaderCell[]>();
  for (const c of cells) {
    const list = byRow.get(c.row) ?? [];
    list.push(c);
    byRow.set(c.row, list);
  }

  return [...byRow.keys()]
    .sort((a, b) => a - b)
    .map((rowIdx) => (
      <tr key={`hr-${rowIdx}`}>
        {[...(byRow.get(rowIdx) ?? [])]
          .sort((a, b) => a.col - b.col)
          .map((cell) => (
            <th
              key={`h-${rowIdx}-${cell.col}`}
              rowSpan={cell.rowSpan > 1 ? cell.rowSpan : undefined}
              colSpan={cell.colSpan > 1 ? cell.colSpan : undefined}
              style={{ textAlign: "center", verticalAlign: "middle", whiteSpace: "nowrap" }}
            >
              {cell.label}
            </th>
          ))}
      </tr>
    ));
}
