"""ABC 分类 inventory.fn.abc_classification

参数：snapshot_date, metric(amount|qty)
返回：product_id, product_name, value, cumulative_pct, abc_class

发布：
  dazi-onto script publish 项目/onto_本体测试05/脚本/functions/inventory_fn_abc_classification.py \\
    --space space__0519 --register-function-id inventory.fn.abc_classification
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


def _abc_class(cumulative_pct):
    if cumulative_pct <= 0.8:
        return "A"
    if cumulative_pct <= 0.95:
        return "B"
    return "C"


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    metric = params.get("metric", "amount")
    snapshot_date = _resolve_snapshot_date(p, params.get("snapshot_date", ""))
    value_col = "inventory_amount" if metric == "amount" else "on_hand_qty"

    if not snapshot_date:
        return p.function_result(
            columns=["product_id", "product_name", "value", "cumulative_pct", "abc_class"],
            data=[],
            row_count=0,
        )

    sql = f"""
    SELECT
        b.product_id,
        pm.product_name,
        sum(b.{value_col}) AS value
    FROM inventory_balance_snapshot AS b
    LEFT JOIN product_master AS pm ON b.product_id = pm.product_id
    WHERE b.snapshot_date = '{snapshot_date}'
    GROUP BY b.product_id, pm.product_name
    HAVING value > 0
    ORDER BY value DESC
    """

    result = p.sql.query(sql)
    total = sum(float(r.get("value", 0) or 0) for r in result)

    data = []
    cumulative = 0.0
    for row in result:
        val = float(row.get("value", 0) or 0)
        cumulative += val / total if total > 0 else 0.0
        data.append({
            "product_id": str(row.get("product_id", "")),
            "product_name": str(row.get("product_name", "")),
            "value": round(val, 2),
            "cumulative_pct": round(cumulative, 4),
            "abc_class": _abc_class(cumulative),
        })

    return p.function_result(
        columns=["product_id", "product_name", "value", "cumulative_pct", "abc_class"],
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
