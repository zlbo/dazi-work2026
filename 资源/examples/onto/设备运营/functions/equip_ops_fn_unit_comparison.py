"""工艺单元对标 equip_ops.fn.unit_comparison

参数：start_date, end_date, metric=oee|availability|output, plant_id（可选）
按工艺单元对标排名

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/设备运营/functions/equip_ops_fn_unit_comparison.py \
    --space space_cate_test01 --register-function-id equip_ops.fn.unit_comparison
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2025-01-01",
        "end_date": "2026-06-30",
        "metric": "oee",
    },
    "object_type_code": "EquipmentAnalysis",
}


def _build_ops_where(start_date, end_date, plant_id=None):
    clauses = []
    if start_date and end_date:
        clauses.append(f"calendar_date >= '{start_date}' AND calendar_date <= '{end_date}'")
    if plant_id:
        clauses.append(f"plant_id = '{plant_id}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _calc_metric(row, metric):
    sum_runtime = float(row.get("sum_runtime_min") or 0)
    sum_available = float(row.get("sum_available_min") or 0)
    sum_actual = float(row.get("sum_actual_output") or 0)
    sum_qualified = float(row.get("sum_qualified_output") or 0)
    sum_theoretical = float(row.get("sum_theoretical_output") or 0)
    availability = sum_runtime / sum_available if sum_available > 0 else 0.0
    quality = sum_qualified / sum_actual if sum_actual > 0 else 0.0
    performance = sum_actual / sum_theoretical if sum_theoretical > 0 else 0.0
    oee = availability * performance * quality
    if metric == "availability":
        return round(availability, 4)
    if metric == "output":
        return round(sum_actual, 2)
    return round(oee, 4)


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    metric = params.get("metric", "oee")
    plant_id = params.get("plant_id") or None
    where_clause = _build_ops_where(start_date, end_date, plant_id)

    sql = f"""
    SELECT
        unit_id,
        any(unit_name) AS unit_name,
        any(plant_name) AS plant_name,
        sum(runtime_min) AS sum_runtime_min,
        sum(calendar_minutes - planned_downtime_min) AS sum_available_min,
        sum(actual_output_qty) AS sum_actual_output,
        sum(qualified_output_qty) AS sum_qualified_output,
        sumIf(runtime_min * ideal_cycle_rate, runtime_min > 0) AS sum_theoretical_output
    FROM fact_equipment_daily_ops
    {where_clause}
    GROUP BY unit_id
    """

    result = p.sql.query(sql)
    if not result:
        return p.function_result(
            columns=["rank", "unit_id", "unit_name", "plant_name", "metric", "metric_value"],
            data=[],
            row_count=0,
        )

    scored = []
    for row in result:
        scored.append({
            "unit_id": str(row.get("unit_id") or ""),
            "unit_name": str(row.get("unit_name") or ""),
            "plant_name": str(row.get("plant_name") or ""),
            "metric_value": _calc_metric(row, metric),
        })

    scored.sort(key=lambda x: x["metric_value"], reverse=True)

    data = []
    for rank, item in enumerate(scored, start=1):
        data.append({
            "rank": rank,
            "unit_id": item["unit_id"],
            "unit_name": item["unit_name"],
            "plant_name": item["plant_name"],
            "metric": metric,
            "metric_value": item["metric_value"],
        })

    return p.function_result(
        columns=["rank", "unit_id", "unit_name", "plant_name", "metric", "metric_value"],
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
