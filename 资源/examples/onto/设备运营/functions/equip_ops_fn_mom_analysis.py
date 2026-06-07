"""环比分析 equip_ops.fn.mom_analysis

参数：start_date, end_date, metric=oee|availability|output, unit_id（可选）
对比上一同等长度期间，返回 current / previous / mom

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/设备运营/functions/equip_ops_fn_mom_analysis.py \
    --space space_cate_test01 --register-function-id equip_ops.fn.mom_analysis
"""

from datetime import datetime, timedelta

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2025-01-01",
        "end_date": "2026-06-30",
        "metric": "availability",
    },
    "object_type_code": "EquipmentAnalysis",
}


def _build_ops_where(start_date, end_date, unit_id=None):
    clauses = []
    if start_date and end_date:
        clauses.append(f"calendar_date >= '{start_date}' AND calendar_date <= '{end_date}'")
    if unit_id:
        clauses.append(f"unit_id = '{unit_id}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _query_period_metrics(p, start_date, end_date, unit_id):
    where_clause = _build_ops_where(start_date, end_date, unit_id)
    sql = f"""
    SELECT
        sum(runtime_min) AS sum_runtime_min,
        sum(calendar_minutes - planned_downtime_min) AS sum_available_min,
        sum(actual_output_qty) AS sum_actual_output,
        sum(qualified_output_qty) AS sum_qualified_output,
        sumIf(runtime_min * ideal_cycle_rate, runtime_min > 0) AS sum_theoretical_output
    FROM fact_equipment_daily_ops
    {where_clause}
    """
    rows = p.sql.query(sql)
    row = rows[0] if rows else {}
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
        "oee": round(oee, 4),
        "availability": round(availability, 4),
        "output": round(sum_actual, 2),
    }


def _calc_mom(current, previous):
    if previous == 0:
        return 0.0 if current == 0 else None
    return round((current - previous) / previous, 4)


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date") or "2025-01-01"
    end_date = params.get("end_date") or "2026-06-30"
    metric = params.get("metric", "oee")
    unit_id = params.get("unit_id") or None

    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    period_days = (end_dt - start_dt).days + 1
    prev_end_dt = start_dt - timedelta(days=1)
    prev_start_dt = prev_end_dt - timedelta(days=period_days - 1)
    prev_start = prev_start_dt.strftime("%Y-%m-%d")
    prev_end = prev_end_dt.strftime("%Y-%m-%d")

    current_metrics = _query_period_metrics(p, start_date, end_date, unit_id)
    previous_metrics = _query_period_metrics(p, prev_start, prev_end, unit_id)

    current_value = current_metrics.get(metric, 0)
    previous_value = previous_metrics.get(metric, 0)
    mom = _calc_mom(current_value, previous_value)

    result = {
        "metric": metric,
        "period": f"{start_date} ~ {end_date}",
        "previous_period": f"{prev_start} ~ {prev_end}",
        "current": current_value,
        "previous": previous_value,
        "mom": mom,
    }
    return p.function_result(
        columns=["metric", "period", "previous_period", "current", "previous", "mom"],
        data=[result],
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
