"""低库存/缺货预警 inventory.fn.low_stock_alerts

参数：warehouse_id, category, limit, snapshot_date
返回：rank, product_id, product_name, warehouse_id, warehouse_name,
      available_qty, safety_stock, gap_qty, severity

发布：
  dazi-onto script publish 项目/onto_本体测试05/脚本/functions/inventory_fn_low_stock_alerts.py \\
    --space space__0519 --register-function-id inventory.fn.low_stock_alerts
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


def _severity(available_qty, safety_stock):
    if available_qty <= 0:
        return "critical"
    if available_qty < safety_stock:
        return "warning"
    return "normal"


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    warehouse_id = params.get("warehouse_id", "")
    category = params.get("category", "")
    limit = int(params.get("limit", 50) or 50)
    snapshot_date = _resolve_snapshot_date(p, params.get("snapshot_date", ""))

    if not snapshot_date:
        return p.function_result(
            columns=[
                "rank", "product_id", "product_name", "warehouse_id", "warehouse_name",
                "available_qty", "safety_stock", "gap_qty", "severity",
            ],
            data=[],
            row_count=0,
        )

    filters = [
        f"b.snapshot_date = '{snapshot_date}'",
        "b.available_qty < b.safety_stock",
        "pm.status = '在用'",
    ]
    if warehouse_id:
        filters.append(f"b.warehouse_id = '{warehouse_id}'")
    if category:
        filters.append(f"pm.product_category = '{category}'")
    where_clause = "WHERE " + " AND ".join(filters)

    sql = f"""
    SELECT
        b.product_id,
        pm.product_name,
        b.warehouse_id,
        w.warehouse_name,
        b.available_qty,
        b.safety_stock,
        b.safety_stock - b.available_qty AS gap_qty
    FROM inventory_balance_snapshot AS b
    LEFT JOIN product_master AS pm ON b.product_id = pm.product_id
    LEFT JOIN warehouse_dimension AS w ON b.warehouse_id = w.warehouse_id
    {where_clause}
    ORDER BY gap_qty DESC, b.available_qty ASC
    LIMIT {limit}
    """

    result = p.sql.query(sql)
    data = []
    for rank, row in enumerate(result, start=1):
        available = float(row.get("available_qty", 0) or 0)
        safety = float(row.get("safety_stock", 0) or 0)
        data.append({
            "rank": rank,
            "product_id": str(row.get("product_id", "")),
            "product_name": str(row.get("product_name", "")),
            "warehouse_id": str(row.get("warehouse_id", "")),
            "warehouse_name": str(row.get("warehouse_name", "")),
            "available_qty": round(available, 2),
            "safety_stock": round(safety, 2),
            "gap_qty": round(float(row.get("gap_qty", 0) or 0), 2),
            "severity": _severity(available, safety),
        })

    return p.function_result(
        columns=[
            "rank", "product_id", "product_name", "warehouse_id", "warehouse_name",
            "available_qty", "safety_stock", "gap_qty", "severity",
        ],
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
