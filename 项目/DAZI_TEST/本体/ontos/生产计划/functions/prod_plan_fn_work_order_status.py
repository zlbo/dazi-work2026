"""工单状态结构 prod_plan.fn.work_order_status

参数：start_date, end_date, plant_id（可选）
发布：dazi onto script publish .../functions/prod_plan_fn_work_order_status.py \
  --space space_cate_test01 --register-function-id prod_plan.fn.work_order_status
"""

def _safe_float(val, default=0.0):
    try:
        v = float(val or default)
        return default if v != v else v  # NaN → default
    except (TypeError, ValueError):
        return default


TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2026-01-01", "end_date": "2026-06-30"},
    "object_type_code": "WorkOrder",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    plant_id = params.get("plant_id") or None
    plant_cond = "" if not plant_id else f" AND plant_id = '{plant_id}'"

    sql = f"""
    SELECT
        status,
        count() AS order_count,
        sum(order_qty) AS order_qty_total,
        sum(completed_qty) AS completed_qty_total,
        ifNotFinite(avgIf(is_on_schedule, status = '已完工'), 0) AS on_time_rate
    FROM fact_work_order
    WHERE release_date >= '{start_date}' AND release_date <= '{end_date}'{plant_cond}
    GROUP BY status
    ORDER BY order_count DESC
    """
    rows = p.sql.query(sql) or []
    total = sum(int(r.get("order_count") or 0) for r in rows)
    data = []
    for row in rows:
        cnt = int(row.get("order_count") or 0)
        order_qty = float(row.get("order_qty_total") or 0)
        completed = float(row.get("completed_qty_total") or 0)
        data.append({
            "status": str(row.get("status") or ""),
            "order_count": cnt,
            "share_pct": round(cnt / total * 100, 2) if total > 0 else 0.0,
            "order_qty_total": round(order_qty, 2),
            "completed_qty_total": round(completed, 2),
            "completion_rate": round(completed / order_qty, 4) if order_qty > 0 else 0.0,
            "on_time_rate": round(_safe_float(row.get("on_time_rate")), 4),
        })

    return p.function_result(
        columns=[
            "status", "order_count", "share_pct", "order_qty_total",
            "completed_qty_total", "completion_rate", "on_time_rate",
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
