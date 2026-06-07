"""销售总览函数 sales.fn.get_summary

参数：start_date, end_date（可选）
返回：总销售额、总销量、订单数、客单价、动销 SKU 数

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/销售本体示例/functions/sales_fn_get_summary.py \
    --space space__misc_01 --register-function-id sales.fn.get_summary
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30"},
    "object_type_code": "SalesAnalysis",
}


def _valid_order_clause():
    return "order_status IN ('已完成', '已发货')"


def _build_where(start_date, end_date):
    clauses = [_valid_order_clause()]
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
        sum(sales_amount) AS total_sales,
        sum(quantity) AS total_quantity,
        uniq(order_id) AS order_count,
        uniq(product_id) AS product_count
    FROM fact_sales_order_line
    {where_clause}
    """

    rows = p.sql.query(sql)
    row = rows[0] if rows else {}
    total_sales = float(row.get("total_sales", 0) or 0)
    order_count = int(row.get("order_count", 0) or 0)
    avg_order_value = total_sales / order_count if order_count > 0 else 0.0

    data = [{
        "total_sales": round(total_sales, 2),
        "total_quantity": int(row.get("total_quantity", 0) or 0),
        "order_count": order_count,
        "avg_order_value": round(avg_order_value, 2),
        "product_count": int(row.get("product_count", 0) or 0),
    }]

    return p.function_result(
        columns=["total_sales", "total_quantity", "order_count", "avg_order_value", "product_count"],
        data=data,
        row_count=1,
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
