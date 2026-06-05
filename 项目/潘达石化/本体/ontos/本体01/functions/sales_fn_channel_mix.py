"""渠道销售占比 sales.fn.channel_mix

参数：start_date, end_date
返回：各渠道销售额、订单数及占比

发布：
  dazi-onto script publish 项目/onto_本体项目01/脚本/functions/sales_fn_channel_mix.py \\
    --space space__0519 --register-function-id sales.fn.channel_mix
"""


def _build_where(start_date, end_date):
    clauses = ["f.order_status IN ('已完成', '已发货')"]
    if start_date and end_date:
        clauses.append(f"f.order_date >= '{start_date}' AND f.order_date <= '{end_date}'")
    return "WHERE " + " AND ".join(clauses)


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    where_clause = _build_where(start_date, end_date)

    sql = f"""
    SELECT
        f.channel_id,
        any(c.channel_name) AS channel_name,
        sum(f.sales_amount) AS sales_amount,
        uniq(f.order_id) AS order_count
    FROM sales_order_fact AS f
    LEFT JOIN channel_dimension AS c ON f.channel_id = c.channel_id
    {where_clause}
    GROUP BY f.channel_id
    ORDER BY sales_amount DESC
    """

    result = p.sql.query(sql)
    if not result:
        return p.function_result(
            columns=["channel_id", "channel_name", "sales_amount", "order_count", "share_pct"],
            data=[],
            row_count=0,
        )

    total = sum(float(r.get("sales_amount", 0) or 0) for r in result)
    data = []
    for row in result:
        sales_amount = float(row.get("sales_amount", 0) or 0)
        data.append({
            "channel_id": str(row.get("channel_id", "")),
            "channel_name": str(row.get("channel_name", "")),
            "sales_amount": round(sales_amount, 2),
            "order_count": int(row.get("order_count", 0) or 0),
            "share_pct": round(sales_amount / total if total > 0 else 0.0, 4),
        })

    return p.function_result(
        columns=["channel_id", "channel_name", "sales_amount", "order_count", "share_pct"],
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
