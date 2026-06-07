"""能耗强度分析 equip_ops.fn.energy_intensity

参数：start_date, end_date, group_by=plant|unit|equipment, plant_id（可选）
返回：group_id, group_name, energy_total, output_qty, energy_per_output

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/设备运营/functions/equip_ops_fn_energy_intensity.py \
    --space space_cate_test01 --register-function-id equip_ops.fn.energy_intensity
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
    group_by = params.get("group_by", "plant")
    plant_id = params.get("plant_id") or None
    group_id_col, group_name_expr = _GROUP_BY_MAP.get(group_by, _GROUP_BY_MAP["plant"])
    where_clause = _build_ops_where(start_date, end_date, plant_id)

    sql = f"""
    SELECT
        {group_id_col} AS group_id,
        {group_name_expr} AS group_name,
        sum(energy_consumption) AS energy_total,
        sum(actual_output_qty) AS output_qty
    FROM fact_equipment_daily_ops
    {where_clause}
    GROUP BY {group_id_col}
    ORDER BY energy_total DESC
    """

    result = p.sql.query(sql)
    if not result:
        return p.function_result(
            columns=["group_id", "group_name", "energy_total", "output_qty", "energy_per_output"],
            data=[],
            row_count=0,
        )

    data = []
    for row in result:
        energy_total = float(row.get("energy_total") or 0)
        output_qty = float(row.get("output_qty") or 0)
        energy_per_output = energy_total / output_qty if output_qty > 0 else 0.0
        data.append({
            "group_id": str(row.get("group_id") or ""),
            "group_name": str(row.get("group_name") or ""),
            "energy_total": round(energy_total, 2),
            "output_qty": round(output_qty, 2),
            "energy_per_output": round(energy_per_output, 4),
        })

    return p.function_result(
        columns=["group_id", "group_name", "energy_total", "output_qty", "energy_per_output"],
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
