"""可用率与停机结构分析 equip_ops.fn.availability_analysis

参数：start_date, end_date, plant_id（可选）
返回：planned_downtime_hours, unplanned_downtime_hours, runtime_hours, availability, load_rate

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/设备运营/functions/equip_ops_fn_availability_analysis.py \
    --space space_cate_test01 --register-function-id equip_ops.fn.availability_analysis
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30"},
    "object_type_code": "EquipmentAnalysis",
}


def _build_ops_where(start_date, end_date, plant_id=None):
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
    where_clause = _build_ops_where(start_date, end_date, plant_id)

    sql = f"""
    SELECT
        sum(planned_downtime_min) AS sum_planned_downtime_min,
        sum(unplanned_downtime_min) AS sum_unplanned_downtime_min,
        sum(runtime_min) AS sum_runtime_min,
        sum(calendar_minutes - planned_downtime_min) AS sum_available_min
    FROM fact_equipment_daily_ops
    {where_clause}
    """

    rows = p.sql.query(sql)
    row = rows[0] if rows else {}

    sum_runtime = float(row.get("sum_runtime_min") or 0)
    sum_available = float(row.get("sum_available_min") or 0)
    availability = sum_runtime / sum_available if sum_available > 0 else 0.0
    load_rate = availability

    data = [{
        "planned_downtime_hours": round(float(row.get("sum_planned_downtime_min") or 0) / 60.0, 2),
        "unplanned_downtime_hours": round(
            float(row.get("sum_unplanned_downtime_min") or 0) / 60.0, 2
        ),
        "runtime_hours": round(sum_runtime / 60.0, 2),
        "availability": round(availability, 4),
        "load_rate": round(load_rate, 4),
    }]

    return p.function_result(
        columns=[
            "planned_downtime_hours", "unplanned_downtime_hours",
            "runtime_hours", "availability", "load_rate",
        ],
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
