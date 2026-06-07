"""渠道结构分析 sales.fn.channel_mix

参数：start_date, end_date
返回：各渠道销售额、销量、订单数及占比

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/销售本体示例/functions/sales_fn_channel_mix.py \
    --space space__misc_01 --register-function-id sales.fn.channel_mix
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30"},
    "object_type_code": "SalesAnalysis",
}


def _build_where(start_date, end_date):
    clauses = ["order_status IN ('已完成', '已发货')"]
    if start_date and end_date:
        clauses.append(f"order_date >= '{start_date}' AND order_date <= '{end_date}'")
    return "WHERE " + " AND ".join(clauses)


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    where_clause = _build_where(start_date, end_date)

    sql = f"""
    SELECT
        f.channel_id,
        any(dch.channel_name) AS channel_name,
        any(dch.channel_type) AS channel_type,
        sum(f.sales_amount) AS sales_amount,
        sum(f.quantity) AS quantity,
        uniq(f.order_id) AS order_count
    FROM fact_sales_order_line AS f
    LEFT JOIN dim_channel AS dch ON f.channel_id = dch.channel_id
    {where_clause}
    GROUP BY f.channel_id
    ORDER BY sales_amount DESC
    """

    result = p.sql.query(sql)
    if not result:
        return p.function_result(
            columns=["channel_id", "channel_name", "channel_type", "sales_amount", "quantity", "order_count", "share_pct"],
            data=[],
            row_count=0,
        )

    total = sum(float(r.get("sales_amount", 0) or 0) for r in result)

    data = []
    for row in result:
        sales_amount = float(row.get("sales_amount", 0) or 0)
        share_pct = sales_amount / total if total > 0 else 0.0
        data.append({
            "channel_id": str(row.get("channel_id", "")),
            "channel_name": str(row.get("channel_name", "")),
            "channel_type": str(row.get("channel_type", "")),
            "sales_amount": round(sales_amount, 2),
            "quantity": int(row.get("quantity", 0) or 0),
            "order_count": int(row.get("order_count", 0) or 0),
            "share_pct": round(share_pct, 4),
        })

    return p.function_result(
        columns=["channel_id", "channel_name", "channel_type", "sales_amount", "quantity", "order_count", "share_pct"],
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
