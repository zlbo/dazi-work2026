"""产量环比 prod_plan.fn.mom_analysis

参数：start_date, end_date, metric=actual_qty|achievement_rate, work_center_id（可选）
发布：dazi onto script publish .../functions/prod_plan_fn_mom_analysis.py \
  --space space_cate_test01 --register-function-id prod_plan.fn.mom_analysis
"""

from datetime import datetime, timedelta

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2026-01-01",
        "end_date": "2026-06-30",
        "metric": "achievement_rate",
    },
    "object_type_code": "ProductionAnalysis",
}


def _query_metrics(p, start_date, end_date, work_center_id):
    extra = "" if not work_center_id else f" AND work_center_id = '{work_center_id}'"
    sql = f"""
    SELECT sum(planned_qty) AS planned_qty, sum(actual_qty) AS actual_qty
    FROM fact_production_daily
    WHERE calendar_date >= '{start_date}' AND calendar_date <= '{end_date}'{extra}
    """
    row = (p.sql.query(sql) or [{}])[0]
    planned = float(row.get("planned_qty") or 0)
    actual = float(row.get("actual_qty") or 0)
    return {
        "actual_qty": round(actual, 2),
        "achievement_rate": round(actual / planned, 4) if planned > 0 else 0.0,
    }


def _calc_mom(current, previous):
    if previous == 0:
        return 0.0 if current == 0 else None
    return round((current - previous) / previous, 4)


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date") or "2026-01-01"
    end_date = params.get("end_date") or "2026-06-30"
    metric = params.get("metric", "achievement_rate")
    work_center_id = params.get("work_center_id") or None

    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    period_days = (end_dt - start_dt).days + 1
    prev_end_dt = start_dt - timedelta(days=1)
    prev_start_dt = prev_end_dt - timedelta(days=period_days - 1)
    prev_start = prev_start_dt.strftime("%Y-%m-%d")
    prev_end = prev_end_dt.strftime("%Y-%m-%d")

    current = _query_metrics(p, start_date, end_date, work_center_id)
    previous = _query_metrics(p, prev_start, prev_end, work_center_id)

    return p.function_result(
        columns=["metric", "period", "previous_period", "current", "previous", "mom"],
        data=[{
            "metric": metric,
            "period": f"{start_date} ~ {end_date}",
            "previous_period": f"{prev_start} ~ {prev_end}",
            "current": current.get(metric, 0),
            "previous": previous.get(metric, 0),
            "mom": _calc_mom(current.get(metric, 0), previous.get(metric, 0)),
        }],
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
