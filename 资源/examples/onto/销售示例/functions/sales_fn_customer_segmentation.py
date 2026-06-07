"""客户分层分析 sales.fn.customer_segmentation

参数：metric(sales_amount|quantity), method(quartile|total), start_date, end_date
返回：客户分层结果（VIP/战略/普通）

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/销售本体示例/functions/sales_fn_customer_segmentation.py \
    --space space__misc_01 --register-function-id sales.fn.customer_segmentation
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "metric": "sales_amount",
        "method": "quartile",
        "start_date": "2025-01-01",
        "end_date": "2026-06-30",
    },
    "object_type_code": "Customer",
}


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

    sql = f"""
    SELECT
        f.customer_id,
        any(dc.customer_name) AS customer_name,
        f.customer_type,
        sum(f.sales_amount) AS sales_amount,
        sum(f.quantity) AS quantity,
        uniq(f.order_id) AS order_count
    FROM fact_sales_order_line AS f
    LEFT JOIN dim_customer AS dc ON f.customer_id = dc.customer_id
    {where_clause}
    GROUP BY f.customer_id, f.customer_type
    ORDER BY sales_amount DESC
    """

    result = p.sql.query(sql)
    if not result:
        return p.function_result(
            columns=["customer_id", "customer_name", "customer_type", "sales_amount", "quantity", "order_count", "segment"],
            data=[],
            row_count=0,
        )

    total_key = "quantity" if metric == "quantity" else "sales_amount"
    total = sum(float(r.get(total_key, 0) or 0) for r in result)

    if method == "quartile":
        values = sorted([float(r.get(total_key, 0) or 0) for r in result], reverse=True)
        n = len(values)
        p75 = values[min(int(n * 0.25), n - 1)]
        p50 = values[min(int(n * 0.50), n - 1)]
        p25 = values[min(int(n * 0.75), n - 1)]

    data = []
    for row in result:
        val = float(row.get(total_key, 0) or 0)
        if method == "quartile":
            if val >= p75:
                segment = "VIP"
            elif val >= p50:
                segment = "战略"
            elif val >= p25:
                segment = "普通"
            else:
                segment = "低价值"
        else:
            share = val / total if total > 0 else 0
            if share >= 0.6:
                segment = "核心"
            elif share >= 0.3:
                segment = "重要"
            else:
                segment = "普通"

        data.append({
            "customer_id": str(row.get("customer_id", "")),
            "customer_name": str(row.get("customer_name", "")),
            "customer_type": str(row.get("customer_type", "")),
            "sales_amount": round(float(row.get("sales_amount", 0) or 0), 2),
            "quantity": int(row.get("quantity", 0) or 0),
            "order_count": int(row.get("order_count", 0) or 0),
            "segment": segment,
        })

    return p.function_result(
        columns=["customer_id", "customer_name", "customer_type", "sales_amount", "quantity", "order_count", "segment"],
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
