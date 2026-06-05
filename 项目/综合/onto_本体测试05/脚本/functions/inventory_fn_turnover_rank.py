"""周转排行 inventory.fn.turnover_rank

参数：window_days, limit, direction(slow|fast)
返回：rank, product_id, product_name, turnover_days, avg_inventory,
      daily_outbound, tag

发布：
  dazi-onto script publish 项目/onto_本体测试05/脚本/functions/inventory_fn_turnover_rank.py \\
    --space space__0519 --register-function-id inventory.fn.turnover_rank
"""


def _tag(turnover_days, daily_out):
    if daily_out <= 0:
        return "dead"
    if turnover_days <= 15:
        return "fast"
    if turnover_days <= 45:
        return "normal"
    if turnover_days <= 90:
        return "slow"
    return "dead"


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    window_days = int(params.get("window_days", 30) or 30)
    limit = int(params.get("limit", 10) or 10)
    direction = params.get("direction", "slow")
    order = "turnover_days ASC" if direction == "fast" else "turnover_days DESC"

    sql = f"""
    WITH
        outbound AS (
            SELECT
                product_id,
                sumIf(abs(quantity), transaction_type = 'OUT') / {window_days} AS daily_outbound
            FROM inventory_transaction
            WHERE transaction_date >= today() - {window_days}
            GROUP BY product_id
        ),
        avg_inv AS (
            SELECT
                product_id,
                avg(on_hand_qty) AS avg_inventory
            FROM inventory_balance_snapshot
            WHERE snapshot_date >= today() - {window_days}
            GROUP BY product_id
        )
    SELECT
        o.product_id,
        pm.product_name,
        o.daily_outbound,
        a.avg_inventory,
        if(o.daily_outbound > 0, a.avg_inventory / o.daily_outbound, 9999) AS turnover_days
    FROM outbound AS o
    LEFT JOIN avg_inv AS a ON o.product_id = a.product_id
    LEFT JOIN product_master AS pm ON o.product_id = pm.product_id
    ORDER BY {order}
    LIMIT {limit}
    """

    result = p.sql.query(sql)
    data = []
    for rank, row in enumerate(result, start=1):
        daily_out = float(row.get("daily_outbound", 0) or 0)
        turnover_days = float(row.get("turnover_days", 0) or 0)
        if turnover_days >= 9999:
            turnover_days = 0.0
        data.append({
            "rank": rank,
            "product_id": str(row.get("product_id", "")),
            "product_name": str(row.get("product_name", "")),
            "turnover_days": round(turnover_days, 2),
            "avg_inventory": round(float(row.get("avg_inventory", 0) or 0), 2),
            "daily_outbound": round(daily_out, 4),
            "tag": _tag(turnover_days, daily_out),
        })

    return p.function_result(
        columns=[
            "rank", "product_id", "product_name", "turnover_days",
            "avg_inventory", "daily_outbound", "tag",
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
