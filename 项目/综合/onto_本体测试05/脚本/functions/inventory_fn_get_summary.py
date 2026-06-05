"""库存总览 inventory.fn.get_summary

参数：snapshot_date（可选，默认最新快照日）
返回：总现存量、总可用量、总库存金额、SKU数、预警数、零库存数、快照日期

发布：
  dazi-onto script publish 项目/onto_本体测试05/脚本/functions/inventory_fn_get_summary.py \\
    --space space__0519 --register-function-id inventory.fn.get_summary
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
    snapshot_date = _resolve_snapshot_date(p, params.get("snapshot_date", ""))
    if not snapshot_date:
        return p.function_result(
            columns=[
                "total_on_hand_qty", "total_available", "total_amount",
                "sku_count", "alert_sku_count", "stockout_count", "snapshot_date",
            ],
            data=[],
            row_count=0,
        )

    sql = f"""
    SELECT
        sum(on_hand_qty) AS total_on_hand_qty,
        sum(available_qty) AS total_available,
        sum(inventory_amount) AS total_amount,
        uniq(product_id) AS sku_count,
        countIf(available_qty < safety_stock) AS alert_sku_count,
        countIf(on_hand_qty <= 0) AS stockout_count
    FROM inventory_balance_snapshot
    WHERE snapshot_date = '{snapshot_date}'
    """

    rows = p.sql.query(sql)
    row = rows[0] if rows else {}

    data = [{
        "total_on_hand_qty": round(float(row.get("total_on_hand_qty", 0) or 0), 2),
        "total_available": round(float(row.get("total_available", 0) or 0), 2),
        "total_amount": round(float(row.get("total_amount", 0) or 0), 2),
        "sku_count": int(row.get("sku_count", 0) or 0),
        "alert_sku_count": int(row.get("alert_sku_count", 0) or 0),
        "stockout_count": int(row.get("stockout_count", 0) or 0),
        "snapshot_date": snapshot_date,
    }]

    return p.function_result(
        columns=[
            "total_on_hand_qty", "total_available", "total_amount",
            "sku_count", "alert_sku_count", "stockout_count", "snapshot_date",
        ],
        data=data,
        row_count=1,
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
