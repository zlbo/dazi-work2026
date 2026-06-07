"""产品销量/销售额排行 sales.fn.top_products

参数：limit, metric(sales_amount|quantity), start_date, end_date
返回：产品排行及销售占比

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/销售本体示例/functions/sales_fn_top_products.py \
    --space space__misc_01 --register-function-id sales.fn.top_products
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "limit": 5,
        "metric": "sales_amount",
        "start_date": "2025-01-01",
        "end_date": "2026-06-30",
    },
    "object_type_code": "Product",
}


def _build_where(start_date, end_date):
    clauses = ["f.order_status IN ('已完成', '已发货')"]
    if start_date and end_date:
        clauses.append(f"f.order_date >= '{start_date}' AND f.order_date <= '{end_date}'")
    return "WHERE " + " AND ".join(clauses)


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    limit = int(params.get("limit", 10) or 10)
    metric = params.get("metric", "sales_amount")
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    where_clause = _build_where(start_date, end_date)
    order_by = "quantity DESC" if metric == "quantity" else "sales_amount DESC"

    sql = f"""
    SELECT
        f.product_id,
        any(dp.product_name) AS product_name,
        f.product_category,
        sum(f.sales_amount) AS sales_amount,
        sum(f.quantity) AS quantity
    FROM fact_sales_order_line AS f
    LEFT JOIN dim_product AS dp ON f.product_id = dp.product_id
    {where_clause}
    GROUP BY f.product_id, f.product_category
    ORDER BY {order_by}
    LIMIT {limit}
    """

    result = p.sql.query(sql)
    if not result:
        return p.function_result(
            columns=["rank", "product_id", "product_name", "product_category", "sales_amount", "quantity", "share_pct"],
            data=[],
            row_count=0,
        )

    total_key = "quantity" if metric == "quantity" else "sales_amount"
    total = sum(float(r.get(total_key, 0) or 0) for r in result)

    data = []
    for rank, row in enumerate(result, start=1):
        val = float(row.get(total_key, 0) or 0)
        share_pct = val / total if total > 0 else 0.0
        data.append({
            "rank": rank,
            "product_id": str(row.get("product_id", "")),
            "product_name": str(row.get("product_name", "")),
            "product_category": str(row.get("product_category", "")),
            "sales_amount": round(float(row.get("sales_amount", 0) or 0), 2),
            "quantity": int(row.get("quantity", 0) or 0),
            "share_pct": round(share_pct, 4),
        })

    return p.function_result(
        columns=["rank", "product_id", "product_name", "product_category", "sales_amount", "quantity", "share_pct"],
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
