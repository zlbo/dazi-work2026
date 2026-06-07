"""延期工单 TOP N prod_plan.fn.top_delayed_orders

参数：start_date, end_date, limit=10, plant_id（可选）
发布：dazi onto script publish .../functions/prod_plan_fn_top_delayed_orders.py \
  --space space_cate_test01 --register-function-id prod_plan.fn.top_delayed_orders
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2026-01-01",
        "end_date": "2026-06-30",
        "limit": 10,
    },
    "object_type_code": "WorkOrder",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    limit = int(params.get("limit", 10))
    plant_id = params.get("plant_id") or None
    plant_cond = "" if not plant_id else f" AND plant_id = '{plant_id}'"

    sql = f"""
    SELECT
        work_order_id,
        product_code,
        product_name,
        work_center_name,
        status,
        order_qty,
        completed_qty,
        planned_end_date,
        delay_days,
        is_on_schedule
    FROM fact_work_order
    WHERE release_date >= '{start_date}' AND release_date <= '{end_date}'
        AND delay_days > 0{plant_cond}
    ORDER BY delay_days DESC, order_qty DESC
    LIMIT {limit}
    """

    rows = p.sql.query(sql) or []
    data = []
    for rank, row in enumerate(rows, start=1):
        order_qty = float(row.get("order_qty") or 0)
        completed = float(row.get("completed_qty") or 0)
        data.append({
            "rank": rank,
            "work_order_id": str(row.get("work_order_id") or ""),
            "product_code": str(row.get("product_code") or ""),
            "product_name": str(row.get("product_name") or ""),
            "work_center_name": str(row.get("work_center_name") or ""),
            "status": str(row.get("status") or ""),
            "order_qty": round(order_qty, 2),
            "completed_qty": round(completed, 2),
            "completion_rate": round(completed / order_qty, 4) if order_qty > 0 else 0.0,
            "planned_end_date": str(row.get("planned_end_date") or ""),
            "delay_days": int(row.get("delay_days") or 0),
            "is_on_schedule": int(row.get("is_on_schedule") or 0),
        })

    return p.function_result(
        columns=[
            "rank", "work_order_id", "product_code", "product_name",
            "work_center_name", "status", "order_qty", "completed_qty",
            "completion_rate", "planned_end_date", "delay_days", "is_on_schedule",
        ],
        data=data,
        row_count=len(data),
    )


def main():
    s = space.get(ctx.space_id or "")
    _Ports = type("_Ports", (), {
        "get_params": lambda self: dict(ctx.params or {}),
        "function_result": lambda self, **kw: onto.function_result(**kw),
    })
    p = _Ports()
    p.sql = s.sql
    return _ontology_fn_body(p)
