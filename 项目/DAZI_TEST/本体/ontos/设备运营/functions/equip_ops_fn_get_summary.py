"""设备运营总览 equip_ops.fn.get_summary

参数：start_date, end_date, plant_id（可选）
返回：equipment_count, avg_availability, avg_oee, total_runtime_hours,
      total_unplanned_downtime_hours, total_output_qty, total_energy,
      energy_per_output, downtime_event_count

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/设备运营/functions/equip_ops_fn_get_summary.py \
    --space space_cate_test01 --register-function-id equip_ops.fn.get_summary
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


def _build_downtime_where(start_date, end_date, plant_id=None):
    clauses = []
    if start_date and end_date:
        clauses.append(
            f"toDate(start_time) >= '{start_date}' AND toDate(start_time) <= '{end_date}'"
        )
    if plant_id:
        clauses.append(f"plant_id = '{plant_id}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _calc_oee_from_sums(row):
    sum_runtime = float(row.get("sum_runtime_min") or 0)
    sum_available = float(row.get("sum_available_min") or 0)
    sum_actual = float(row.get("sum_actual_output") or 0)
    sum_qualified = float(row.get("sum_qualified_output") or 0)
    sum_theoretical = float(row.get("sum_theoretical_output") or 0)
    availability = sum_runtime / sum_available if sum_available > 0 else 0.0
    quality = sum_qualified / sum_actual if sum_actual > 0 else 0.0
    performance = sum_actual / sum_theoretical if sum_theoretical > 0 else 0.0
    oee = availability * performance * quality
    return round(availability, 4), round(oee, 4)


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    plant_id = params.get("plant_id") or None
    where_clause = _build_ops_where(start_date, end_date, plant_id)

    sql = f"""
    SELECT
        uniq(equipment_id) AS equipment_count,
        sum(runtime_min) AS sum_runtime_min,
        sum(calendar_minutes - planned_downtime_min) AS sum_available_min,
        sum(actual_output_qty) AS sum_actual_output,
        sum(qualified_output_qty) AS sum_qualified_output,
        sumIf(runtime_min * ideal_cycle_rate, runtime_min > 0) AS sum_theoretical_output,
        sum(unplanned_downtime_min) AS sum_unplanned_downtime_min,
        sum(energy_consumption) AS sum_energy
    FROM fact_equipment_daily_ops
    {where_clause}
    """

    rows = p.sql.query(sql)
    row = rows[0] if rows else {}
    avg_availability, avg_oee = _calc_oee_from_sums(row)

    sum_runtime = float(row.get("sum_runtime_min") or 0)
    sum_actual = float(row.get("sum_actual_output") or 0)
    sum_energy = float(row.get("sum_energy") or 0)
    energy_per_output = sum_energy / sum_actual if sum_actual > 0 else 0.0

    dt_where = _build_downtime_where(start_date, end_date, plant_id)
    dt_sql = f"SELECT count() AS event_count FROM fact_downtime_event {dt_where}"
    dt_rows = p.sql.query(dt_sql)
    downtime_event_count = int((dt_rows[0] if dt_rows else {}).get("event_count") or 0)

    data = [{
        "equipment_count": int(row.get("equipment_count") or 0),
        "avg_availability": avg_availability,
        "avg_oee": avg_oee,
        "total_runtime_hours": round(sum_runtime / 60.0, 2),
        "total_unplanned_downtime_hours": round(
            float(row.get("sum_unplanned_downtime_min") or 0) / 60.0, 2
        ),
        "total_output_qty": round(sum_actual, 2),
        "total_energy": round(sum_energy, 2),
        "energy_per_output": round(energy_per_output, 4),
        "downtime_event_count": downtime_event_count,
    }]

    return p.function_result(
        columns=[
            "equipment_count", "avg_availability", "avg_oee", "total_runtime_hours",
            "total_unplanned_downtime_hours", "total_output_qty", "total_energy",
            "energy_per_output", "downtime_event_count",
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
