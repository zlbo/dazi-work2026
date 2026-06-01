"""YoY (Year-over-Year) Analysis Function

功能：计算指定时间范围内的年度同比分析
参数：start_date, end_date
返回：年度利润数据及同比增长率

放置位置：spaces/space__profit0520/editorial/scripts/ontology_functions/profit_fn_yoy_analysis.py
检索关键字：profit yoy year-over-year
"""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})

    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")

    where_clause = ""
    if start_date and end_date:
        where_clause = f"WHERE order_date >= '{start_date}' AND order_date <= '{end_date}'"

    sql = f"""
    SELECT
        toYear(order_date) as year,
        sum(revenue) as revenue,
        sum(cost) as cost,
        sum(revenue) - sum(cost) as profit,
        if(sum(revenue) > 0, (sum(revenue) - sum(cost)) / sum(revenue), 0) as profit_margin
    FROM profit_analysis_fact
    {where_clause}
    GROUP BY toYear(order_date)
    ORDER BY year
    """

    result = p.sql.query(sql)

    if not result:
        return p.function_result(
            columns=["year", "revenue", "cost", "profit", "profit_margin", "yoy_growth"],
            data=[],
            row_count=0
        )

    data = []
    prev_profit = None

    for row in result:
        year = int(row.get("year", 0))
        profit = float(row.get("profit", 0) or 0)

        if prev_profit is not None and prev_profit != 0:
            yoy_growth = (profit - prev_profit) / prev_profit
        else:
            yoy_growth = 0.0

        data.append({
            "year": year,
            "revenue": round(float(row.get("revenue", 0) or 0), 2),
            "cost": round(float(row.get("cost", 0) or 0), 2),
            "profit": round(profit, 2),
            "profit_margin": round(float(row.get("profit_margin", 0) or 0), 4),
            "yoy_growth": round(yoy_growth, 4),
        })

        prev_profit = profit

    return p.function_result(
        columns=["year", "revenue", "cost", "profit", "profit_margin", "yoy_growth"],
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
