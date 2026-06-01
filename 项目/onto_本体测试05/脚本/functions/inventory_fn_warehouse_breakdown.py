"""分仓库存结构 inventory.fn.warehouse_breakdown

参数：snapshot_date, metric(qty|amount)
返回：warehouse_id, warehouse_name, value, share_pct

发布：
  dazi-onto script publish 项目/onto_本体测试05/脚本/functions/inventory_fn_warehouse_breakdown.py \\
    --space space__0519 --register-function-id inventory.fn.warehouse_breakdown
"""


def _resolve_snapshot_date(p, snapshot_date):
    if snapshot_date:
        return snapshot_date
    row = p.sql.query_one("SELECT max(snapshot_date) AS d FROM inventory_balance_snapshot")
    if not row:
        return ""
    if isinstance(row, dict):
        return str(row.get("d", "") or "")
    return str(row)


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    metric = params.get("metric", "qty")
    snapshot_date = _resolve_snapshot_date(p, params.get("snapshot_date", ""))
    value_col = "inventory_amount" if metric == "amount" else "on_hand_qty"

    if not snapshot_date:
        return p.function_result(
            columns=["warehouse_id", "warehouse_name", "value", "share_pct"],
            data=[],
            row_count=0,
        )

    sql = f"""
    SELECT
        b.warehouse_id,
        any(w.warehouse_name) AS warehouse_name,
        sum(b.{value_col}) AS value
    FROM inventory_balance_snapshot AS b
    LEFT JOIN warehouse_dimension AS w ON b.warehouse_id = w.warehouse_id
    WHERE b.snapshot_date = '{snapshot_date}'
    GROUP BY b.warehouse_id
    ORDER BY value DESC
    """

    result = p.sql.query(sql)
    total = sum(float(r.get("value", 0) or 0) for r in result)

    data = []
    for row in result:
        val = float(row.get("value", 0) or 0)
        share_pct = val / total if total > 0 else 0.0
        data.append({
            "warehouse_id": str(row.get("warehouse_id", "")),
            "warehouse_name": str(row.get("warehouse_name", "")),
            "value": round(val, 2),
            "share_pct": round(share_pct, 4),
        })

    return p.function_result(
        columns=["warehouse_id", "warehouse_name", "value", "share_pct"],
        data=data,
        row_count=len(data),
    )


def main():
    s = space.get(ctx.space_id or "")
    _Ports = type(
        "_Ports",
        (),
        {
            "get_params": lambda self: dict(ctx.params or {}),
            "function_result": lambda self, **kw: onto.function_result(**kw),
        },
    )
    p = _Ports()
    p.sql = s.sql
    return _ontology_fn_body(p)
