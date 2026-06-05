"""客户销售分层 sales.fn.customer_segmentation

参数：metric(sales_amount|quantity), method(quartile|percentile), start_date, end_date
返回：客户销售额及分层（VIP/High/Medium/Low）

发布：
  dazi-onto script publish 项目/onto_本体项目01/脚本/functions/sales_fn_customer_segmentation.py \\
    --space space__0519 --register-function-id sales.fn.customer_segmentation
"""


def _build_where(start_date, end_date):
    clauses = ["order_status IN ('已完成', '已发货')"]
    if start_date and end_date:
        clauses.append(f"order_date >= '{start_date}' AND order_date <= '{end_date}'")
    return "WHERE " + " AND ".join(clauses)


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    metric = params.get("metric", "sales_amount")
    method = params.get("method", "quartile")
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    where_clause = _build_where(start_date, end_date)
    order_col = "quantity" if metric == "quantity" else "sales_amount"

    sql = f"""
    SELECT
        customer_id,
        customer_region,
        sum(sales_amount) AS sales_amount,
        sum(quantity) AS quantity
    FROM sales_order_fact
    {where_clause}
    GROUP BY customer_id, customer_region
    ORDER BY {order_col} DESC
    """

    result = p.sql.query(sql)
    if not result:
        return p.function_result(
            columns=["customer_id", "customer_region", "sales_amount", "quantity", "segment"],
            data=[],
            row_count=0,
        )

    values = [float(row.get(order_col, 0) or 0) for row in result]
    total = len(values)
    if total == 0:
        return p.function_result(
            columns=["customer_id", "customer_region", "sales_amount", "quantity", "segment"],
            data=[],
            row_count=0,
        )

    sorted_vals = sorted(values, reverse=True)
    if method == "percentile":
        p80_idx = min(int(total * 0.8), total - 1)
        p50_idx = min(int(total * 0.5), total - 1)
        p20_idx = min(int(total * 0.2), total - 1)
    else:
        p80_idx = min(int(total * 0.25), total - 1)
        p50_idx = min(int(total * 0.5), total - 1)
        p20_idx = min(int(total * 0.75), total - 1)
    p80 = sorted_vals[p80_idx]
    p50 = sorted_vals[p50_idx]
    p20 = sorted_vals[p20_idx]

    def get_segment(val):
        if val >= p80:
            return "VIP"
        if val >= p50:
            return "High"
        if val >= p20:
            return "Medium"
        return "Low"

    data = []
    for row in result:
        val = float(row.get(order_col, 0) or 0)
        data.append({
            "customer_id": str(row.get("customer_id", "")),
            "customer_region": str(row.get("customer_region", "")),
            "sales_amount": round(float(row.get("sales_amount", 0) or 0), 2),
            "quantity": int(row.get("quantity", 0) or 0),
            "segment": get_segment(val),
        })

    return p.function_result(
        columns=["customer_id", "customer_region", "sales_amount", "quantity", "segment"],
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
