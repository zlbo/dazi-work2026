"""故障 TOP 设备 equip_ops.fn.top_fault_equipment

参数：start_date, end_date, limit=10, plant_id（可选）
按非计划停机时长 TOP 设备

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/设备运营/functions/equip_ops_fn_top_fault_equipment.py \
    --space space_cate_test01 --register-function-id equip_ops.fn.top_fault_equipment
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2025-01-01",
        "end_date": "2026-06-30",
        "limit": 10,
    },
    "object_type_code": "EquipmentAnalysis",
}


def _build_where(start_date, end_date, plant_id=None):
    clauses = ["e.is_planned = 0"]
    if start_date and end_date:
        clauses.append(
            f"e.start_time >= '{start_date} 00:00:00' AND e.start_time <= '{end_date} 23:59:59'"
        )
    if plant_id:
        clauses.append(f"e.plant_id = '{plant_id}'")
    return "WHERE " + " AND ".join(clauses)


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    limit = int(params.get("limit", 10) or 10)
    plant_id = params.get("plant_id") or None
    where_clause = _build_where(start_date, end_date, plant_id)

    sql = f"""
    SELECT
        e.equipment_id,
        any(e.equipment_code) AS equipment_code,
        any(e.equipment_name) AS equipment_name,
        any(eq.plant_name) AS plant_name,
        any(eq.unit_name) AS unit_name,
        sum(e.duration_min) AS downtime_min,
        count() AS event_count
    FROM fact_downtime_event AS e
    LEFT JOIN dim_equipment AS eq ON e.equipment_id = eq.equipment_id
    {where_clause}
    GROUP BY e.equipment_id
    ORDER BY downtime_min DESC
    LIMIT {limit}
    """

    result = p.sql.query(sql)
    if not result:
        return p.function_result(
            columns=[
                "rank", "equipment_id", "equipment_code", "equipment_name",
                "plant_name", "unit_name", "downtime_hours", "event_count",
            ],
            data=[],
            row_count=0,
        )

    data = []
    for rank, row in enumerate(result, start=1):
        data.append({
            "rank": rank,
            "equipment_id": str(row.get("equipment_id") or ""),
            "equipment_code": str(row.get("equipment_code") or ""),
            "equipment_name": str(row.get("equipment_name") or ""),
            "plant_name": str(row.get("plant_name") or ""),
            "unit_name": str(row.get("unit_name") or ""),
            "downtime_hours": round(float(row.get("downtime_min") or 0) / 60.0, 2),
            "event_count": int(row.get("event_count") or 0),
        })

    return p.function_result(
        columns=[
            "rank", "equipment_id", "equipment_code", "equipment_name",
            "plant_name", "unit_name", "downtime_hours", "event_count",
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
