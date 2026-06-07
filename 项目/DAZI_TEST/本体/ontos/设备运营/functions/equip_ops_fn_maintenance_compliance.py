"""维保达成分析 equip_ops.fn.maintenance_compliance

参数：start_date, end_date, plant_id（可选）
返回：schedule_rate, total_maint, on_schedule_count, overdue_count, total_cost

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/设备运营/functions/equip_ops_fn_maintenance_compliance.py \
    --space space_cate_test01 --register-function-id equip_ops.fn.maintenance_compliance
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30"},
    "object_type_code": "EquipmentAnalysis",
}


def _build_where(start_date, end_date, plant_id=None):
    clauses = []
    if start_date and end_date:
        clauses.append(f"plan_date >= '{start_date}' AND plan_date <= '{end_date}'")
    if plant_id:
        clauses.append(f"plant_id = '{plant_id}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    plant_id = params.get("plant_id") or None
    where_clause = _build_where(start_date, end_date, plant_id)

    sql = f"""
    SELECT
        count() AS total_maint,
        sum(is_on_schedule) AS on_schedule_count,
        countIf(status = '逾期') AS overdue_count,
        sum(actual_cost) AS total_cost
    FROM fact_maintenance_record
    {where_clause}
    """

    rows = p.sql.query(sql)
    row = rows[0] if rows else {}
    total_maint = int(row.get("total_maint") or 0)
    on_schedule_count = int(row.get("on_schedule_count") or 0)
    schedule_rate = on_schedule_count / total_maint if total_maint > 0 else 0.0

    data = [{
        "schedule_rate": round(schedule_rate, 4),
        "total_maint": total_maint,
        "on_schedule_count": on_schedule_count,
        "overdue_count": int(row.get("overdue_count") or 0),
        "total_cost": round(float(row.get("total_cost") or 0), 2),
    }]

    return p.function_result(
        columns=["schedule_rate", "total_maint", "on_schedule_count", "overdue_count", "total_cost"],
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
