"""产能负荷分析 prod_plan.fn.capacity_load

参数：start_date, end_date, work_center_id（可选）, plan_version_id（可选）
发布：dazi onto script publish .../functions/prod_plan_fn_capacity_load.py \
  --space space_cate_test01 --register-function-id prod_plan.fn.capacity_load
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2026-01-01",
        "end_date": "2026-06-30",
        "plan_version_id": "PV_MPS_202606",
    },
    "object_type_code": "CapacitySnapshot",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    work_center_id = params.get("work_center_id") or None
    plan_version_id = params.get("plan_version_id") or None

    extra = []
    if work_center_id:
        extra.append(f"work_center_id = '{work_center_id}'")
    if plan_version_id:
        extra.append(f"plan_version_id = '{plan_version_id}'")
    extra_clause = (" AND " + " AND ".join(extra)) if extra else ""

    sql = f"""
    SELECT
        work_center_id,
        any(work_center_name) AS work_center_name,
        sum(available_hours) AS available_hours,
        sum(planned_load_hours) AS planned_load_hours,
        sum(actual_load_hours) AS actual_load_hours
    FROM fact_capacity_load
    WHERE calendar_date >= '{start_date}' AND calendar_date <= '{end_date}'{extra_clause}
    GROUP BY work_center_id
    ORDER BY planned_load_hours DESC
    """

    rows = p.sql.query(sql) or []
    data = []
    for row in rows:
        avail = float(row.get("available_hours") or 0)
        planned = float(row.get("planned_load_hours") or 0)
        actual = float(row.get("actual_load_hours") or 0)
        planned_rate = planned / avail if avail > 0 else 0.0
        actual_rate = actual / avail if avail > 0 else 0.0
        data.append({
            "work_center_id": str(row.get("work_center_id") or ""),
            "work_center_name": str(row.get("work_center_name") or ""),
            "available_hours": round(avail, 2),
            "planned_load_hours": round(planned, 2),
            "actual_load_hours": round(actual, 2),
            "planned_load_rate": round(planned_rate, 4),
            "actual_load_rate": round(actual_rate, 4),
            "is_overloaded": 1 if planned_rate > 1.0 else 0,
        })

    return p.function_result(
        columns=[
            "work_center_id", "work_center_name", "available_hours",
            "planned_load_hours", "actual_load_hours",
            "planned_load_rate", "actual_load_rate", "is_overloaded",
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
