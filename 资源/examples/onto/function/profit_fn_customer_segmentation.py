"""Customer Segmentation Function

功能：基于利润贡献对客户进行分层
参数：metric, method, start_date, end_date
返回：客户分层数据（VIP/High/Medium/Low）

放置位置：spaces/space__profit0520/editorial/scripts/ontology_functions/profit_fn_customer_segmentation.py
检索关键字：profit customer_segmentation
"""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})

    metric = params.get("metric", "profit")
    method = params.get("method", "quartile")
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")

    where_clause = ""
    if start_date and end_date:
        where_clause = f"WHERE order_date >= '{start_date}' AND order_date <= '{end_date}'"

    sql = f"""
    SELECT
        customer_id,
        customer_region,
        sum(revenue) as revenue,
        sum(cost) as cost,
        sum(revenue) - sum(cost) as profit
    FROM profit_analysis_fact
    {where_clause}
    GROUP BY customer_id, customer_region
    ORDER BY profit DESC
    """

    result = p.sql.query(sql)

    if not result:
        return p.function_result(
            columns=["customer_id", "customer_region", "revenue", "cost", "profit", "segment"],
            data=[],
            row_count=0
        )

    profits = [float(row.get("profit", 0) or 0) for row in result]
    total = len(profits)

    if total == 0:
        return p.function_result(
            columns=["customer_id", "customer_region", "revenue", "cost", "profit", "segment"],
            data=[],
            row_count=0
        )

    if method == "percentile":
        sorted_profits = sorted(profits, reverse=True)
        p80_idx = min(int(total * 0.8), total - 1)
        p50_idx = min(int(total * 0.5), total - 1)
        p20_idx = min(int(total * 0.2), total - 1)
        p80 = sorted_profits[p80_idx]
        p50 = sorted_profits[p50_idx]
        p20 = sorted_profits[p20_idx]
    else:
        sorted_profits = sorted(profits, reverse=True)
        q1_idx = min(int(total * 0.25), total - 1)
        q2_idx = min(int(total * 0.5), total - 1)
        q3_idx = min(int(total * 0.75), total - 1)
        p80 = sorted_profits[q1_idx]
        p50 = sorted_profits[q2_idx]
        p20 = sorted_profits[q3_idx]

    def get_segment(profit_val):
        if profit_val >= p80:
            return "VIP"
        elif profit_val >= p50:
            return "High"
        elif profit_val >= p20:
            return "Medium"
        else:
            return "Low"

    data = []
    for row in result:
        profit = float(row.get("profit", 0) or 0)
        data.append({
            "customer_id": str(row.get("customer_id", "")),
            "customer_region": str(row.get("customer_region", "")),
            "revenue": round(float(row.get("revenue", 0) or 0), 2),
            "cost": round(float(row.get("cost", 0) or 0), 2),
            "profit": round(profit, 2),
            "segment": get_segment(profit),
        })

    return p.function_result(
        columns=["customer_id", "customer_region", "revenue", "cost", "profit", "segment"],
        data=data,
        row_count=len(data)
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
    p.space_id = str(ctx.space_id or "")
    p.sql = s.sql

    return _ontology_fn_body(p)
