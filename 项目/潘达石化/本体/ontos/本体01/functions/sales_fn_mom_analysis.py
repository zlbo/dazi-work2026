"""月度环比分析 sales.fn.mom_analysis

参数：start_date, end_date
返回：月度销售额、销量、订单数及环比增长率

发布：
  dazi-onto script publish 项目/onto_本体项目01/脚本/functions/sales_fn_mom_analysis.py \\
    --space space__0519 --register-function-id sales.fn.mom_analysis
"""


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
        formatDateTime(order_date, '%Y-%m') AS year_month,
        sum(sales_amount) AS sales_amount,
        sum(quantity) AS quantity,
        uniq(order_id) AS order_count
    FROM sales_order_fact
    {where_clause}
    GROUP BY formatDateTime(order_date, '%Y-%m')
    ORDER BY year_month
    """

    result = p.sql.query(sql)
    if not result:
        return p.function_result(
            columns=["year_month", "sales_amount", "quantity", "order_count", "mom_growth"],
            data=[],
            row_count=0,
        )

    data = []
    prev_sales = None
    for row in result:
        sales_amount = float(row.get("sales_amount", 0) or 0)
        if prev_sales is not None and prev_sales != 0:
            mom_growth = (sales_amount - prev_sales) / prev_sales
        else:
            mom_growth = 0.0
        data.append({
            "year_month": str(row.get("year_month", "")),
            "sales_amount": round(sales_amount, 2),
            "quantity": int(row.get("quantity", 0) or 0),
            "order_count": int(row.get("order_count", 0) or 0),
            "mom_growth": round(mom_growth, 4),
        })
        prev_sales = sales_amount

    return p.function_result(
        columns=["year_month", "sales_amount", "quantity", "order_count", "mom_growth"],
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
