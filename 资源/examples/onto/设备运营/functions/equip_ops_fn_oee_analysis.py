"""OEE 分解分析 equip_ops.fn.oee_analysis

参数：start_date, end_date, equipment_id（可选）, group_by=plant|unit|equipment|equip_type
返回：group_id, group_name, availability, performance, quality, oee, runtime_hours, output_qty

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/设备运营/functions/equip_ops_fn_oee_analysis.py \
    --space space_cate_test01 --register-function-id equip_ops.fn.oee_analysis
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2025-01-01",
        "end_date": "2026-06-30",
        "group_by": "plant",
    },
    "object_type_code": "EquipmentAnalysis",
}

_GROUP_BY_MAP = {
    "plant": ("plant_id", "any(plant_name)"),
    "unit": ("unit_id", "any(unit_name)"),
    "equipment": ("equipment_id", "any(equipment_name)"),
    "equip_type": ("equip_type_id", "any(category)"),
}


def _build_ops_where(start_date, end_date, plant_id=None, equipment_id=None):
    clauses = []
    if start_date and end_date:
        clauses.append(f"calendar_date >= '{start_date}' AND calendar_date <= '{end_date}'")
    if plant_id:
        clauses.append(f"plant_id = '{plant_id}'")
    if equipment_id:
        clauses.append(f"equipment_id = '{equipment_id}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _calc_oee_metrics(row):
    sum_runtime = float(row.get("sum_runtime_min") or 0)
    sum_available = float(row.get("sum_available_min") or 0)
    sum_actual = float(row.get("sum_actual_output") or 0)
    sum_qualified = float(row.get("sum_qualified_output") or 0)
    sum_theoretical = float(row.get("sum_theoretical_output") or 0)
    availability = sum_runtime / sum_available if sum_available > 0 else 0.0
    quality = sum_qualified / sum_actual if sum_actual > 0 else 0.0
    performance = sum_actual / sum_theoretical if sum_theoretical > 0 else 0.0
    oee = availability * performance * quality
    return {
        "availability": round(availability, 4),
        "performance": round(performance, 4),
        "quality": round(quality, 4),
        "oee": round(oee, 4),
        "runtime_hours": round(sum_runtime / 60.0, 2),
        "output_qty": round(sum_actual, 2),
    }


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    equipment_id = params.get("equipment_id") or None
    group_by = params.get("group_by", "plant")
    group_id_col, group_name_expr = _GROUP_BY_MAP.get(group_by, _GROUP_BY_MAP["plant"])
    where_clause = _build_ops_where(start_date, end_date, equipment_id=equipment_id)

    sql = f"""
    SELECT
        {group_id_col} AS group_id,
        {group_name_expr} AS group_name,
        sum(runtime_min) AS sum_runtime_min,
        sum(calendar_minutes - planned_downtime_min) AS sum_available_min,
        sum(actual_output_qty) AS sum_actual_output,
        sum(qualified_output_qty) AS sum_qualified_output,
        sumIf(runtime_min * ideal_cycle_rate, runtime_min > 0) AS sum_theoretical_output
    FROM fact_equipment_daily_ops
    {where_clause}
    GROUP BY {group_id_col}
    ORDER BY group_id
    """

    result = p.sql.query(sql)
    if not result:
        return p.function_result(
            columns=[
                "group_id", "group_name", "availability", "performance",
                "quality", "oee", "runtime_hours", "output_qty",
            ],
            data=[],
            row_count=0,
        )

    data = []
    for row in result:
        metrics = _calc_oee_metrics(row)
        data.append({
            "group_id": str(row.get("group_id") or ""),
            "group_name": str(row.get("group_name") or ""),
            **metrics,
        })

    return p.function_result(
        columns=[
            "group_id", "group_name", "availability", "performance",
            "quality", "oee", "runtime_hours", "output_qty",
        ],
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
