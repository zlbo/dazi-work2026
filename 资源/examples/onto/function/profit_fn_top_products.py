"""Top Products Profit Ranking Function

功能：按利润或利润率排序，获取Top N产品
参数：limit, metric, start_date, end_date
返回：产品利润排行数据

放置位置：spaces/space__profit0520/editorial/scripts/ontology_functions/profit_fn_top_products.py
检索关键字：profit top_products ranking
"""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})

    limit = int(params.get("limit", 10) or 10)
    metric = params.get("metric", "profit")
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")

    where_clause = ""
    if start_date and end_date:
        where_clause = f"WHERE order_date >= '{start_date}' AND order_date <= '{end_date}'"

    if metric == "margin":
        order_by = "profit_margin DESC"
    else:
        order_by = "profit DESC"

    sql = f"""
    SELECT
        product_id,
        product_category,
        sum(revenue) as revenue,
        sum(cost) as cost,
        sum(revenue) - sum(cost) as profit,
        if(sum(revenue) > 0, (sum(revenue) - sum(cost)) / sum(revenue), 0) as profit_margin
    FROM profit_analysis_fact
    {where_clause}
    GROUP BY product_id, product_category
    ORDER BY {order_by}
    LIMIT {limit}
    """

    result = p.sql.query(sql)

    if not result:
        return p.function_result(
            columns=["rank", "product_id", "product_category", "revenue", "cost", "profit", "profit_margin"],
            data=[],
            row_count=0
        )

    data = []
    rank = 1
    for row in result:
        data.append({
            "rank": rank,
            "product_id": str(row.get("product_id", "")),
            "product_category": str(row.get("product_category", "")),
            "revenue": round(float(row.get("revenue", 0) or 0), 2),
            "cost": round(float(row.get("cost", 0) or 0), 2),
            "profit": round(float(row.get("profit", 0) or 0), 2),
            "profit_margin": round(float(row.get("profit_margin", 0) or 0), 4),
        })
        rank += 1

    return p.function_result(
        columns=["rank", "product_id", "product_category", "revenue", "cost", "profit", "profit_margin"],
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
