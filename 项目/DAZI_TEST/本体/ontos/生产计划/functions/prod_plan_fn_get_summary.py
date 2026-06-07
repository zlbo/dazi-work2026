"""生产计划总览 prod_plan.fn.get_summary

参数：start_date, end_date, plant_id（可选）
发布：dazi onto script publish .../functions/prod_plan_fn_get_summary.py \
  --space space_cate_test01 --register-function-id prod_plan.fn.get_summary
"""

def _safe_float(val, default=0.0):
    try:
        v = float(val or default)
        return default if v != v else v
    except (TypeError, ValueError):
        return default


TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2026-01-01", "end_date": "2026-06-30"},
    "object_type_code": "ProductionAnalysis",
}


def _daily_where(start_date, end_date, plant_id=None):
    clauses = []
    if start_date and end_date:
        clauses.append(f"calendar_date >= '{start_date}' AND calendar_date <= '{end_date}'")
    if plant_id:
        clauses.append(f"plant_id = '{plant_id}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    plant_id = params.get("plant_id") or None
    where_clause = _daily_where(start_date, end_date, plant_id)
    plant_cond = "" if not plant_id else f" AND plant_id = '{plant_id}'"

    daily_sql = f"""
    SELECT
        sum(planned_qty) AS planned_qty,
        sum(actual_qty) AS actual_qty,
        sum(qualified_qty) AS qualified_qty
    FROM fact_production_daily
    {where_clause}
    """
    daily_row = (p.sql.query(daily_sql) or [{}])[0]
    planned_qty = float(daily_row.get("planned_qty") or 0)
    actual_qty = float(daily_row.get("actual_qty") or 0)
    qualified_qty = float(daily_row.get("qualified_qty") or 0)
    achievement_rate = actual_qty / planned_qty if planned_qty > 0 else 0.0

    wo_sql = f"""
    SELECT
        count() AS work_order_count,
        countIf(status = '已完工') AS completed_work_order_count,
        ifNotFinite(avgIf(is_on_schedule, status = '已完工'), 0) AS on_time_rate
    FROM fact_work_order
    WHERE release_date >= '{start_date}' AND release_date <= '{end_date}'{plant_cond}
    """
    wo_row = (p.sql.query(wo_sql) or [{}])[0]

    load_sql = f"""
    SELECT avg(planned_load_hours / nullIf(available_hours, 0)) AS avg_planned_load_rate
    FROM fact_capacity_load
    WHERE calendar_date >= '{start_date}' AND calendar_date <= '{end_date}'{plant_cond}
    """
    load_row = (p.sql.query(load_sql) or [{}])[0]

    mrp_sql = f"""
    SELECT
        countIf(kit_status = '缺料') AS material_shortage_line_count,
        countIf(kit_status = '齐套') / count() AS kit_rate
    FROM fact_material_requirement
    WHERE requirement_date >= '{start_date}' AND requirement_date <= '{end_date}'{plant_cond}
    """
    mrp_row = (p.sql.query(mrp_sql) or [{}])[0]

    data = [{
        "planned_qty": round(planned_qty, 2),
        "actual_qty": round(actual_qty, 2),
        "qualified_qty": round(qualified_qty, 2),
        "achievement_rate": round(achievement_rate, 4),
        "work_order_count": int(wo_row.get("work_order_count") or 0),
        "completed_work_order_count": int(wo_row.get("completed_work_order_count") or 0),
        "on_time_rate": round(_safe_float(wo_row.get("on_time_rate")), 4),
        "avg_planned_load_rate": round(_safe_float(load_row.get("avg_planned_load_rate")), 4),
        "material_shortage_line_count": int(mrp_row.get("material_shortage_line_count") or 0),
        "kit_rate": round(_safe_float(mrp_row.get("kit_rate")), 4),
    }]
    return p.function_result(
        columns=[
            "planned_qty", "actual_qty", "qualified_qty", "achievement_rate",
            "work_order_count", "completed_work_order_count", "on_time_rate",
            "avg_planned_load_rate", "material_shortage_line_count", "kit_rate",
        ],
        data=data,
        row_count=1,
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
