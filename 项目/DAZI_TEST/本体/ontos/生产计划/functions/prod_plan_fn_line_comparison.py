"""产线产量对标 prod_plan.fn.line_comparison

参数：start_date, end_date, metric=achievement_rate|actual_qty|planned_qty, plant_id（可选）
发布：dazi onto script publish .../functions/prod_plan_fn_line_comparison.py \
  --space space_cate_test01 --register-function-id prod_plan.fn.line_comparison
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2026-01-01",
        "end_date": "2026-06-30",
        "metric": "achievement_rate",
    },
    "object_type_code": "WorkCenter",
}


def _calc_metric(row, metric):
    planned = float(row.get("planned_qty") or 0)
    actual = float(row.get("actual_qty") or 0)
    if metric == "planned_qty":
        return round(planned, 2)
    if metric == "actual_qty":
        return round(actual, 2)
    return round(actual / planned, 4) if planned > 0 else 0.0


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    metric = params.get("metric", "achievement_rate")
    plant_id = params.get("plant_id") or None
    plant_cond = "" if not plant_id else f" AND plant_id = '{plant_id}'"

    sql = f"""
    SELECT
        work_center_id,
        any(work_center_name) AS work_center_name,
        any(plant_name) AS plant_name,
        sum(planned_qty) AS planned_qty,
        sum(actual_qty) AS actual_qty
    FROM fact_production_daily
    WHERE calendar_date >= '{start_date}' AND calendar_date <= '{end_date}'{plant_cond}
    GROUP BY work_center_id
    """

    rows = p.sql.query(sql) or []
    scored = []
    for row in rows:
        scored.append({
            "work_center_id": str(row.get("work_center_id") or ""),
            "work_center_name": str(row.get("work_center_name") or ""),
            "plant_name": str(row.get("plant_name") or ""),
            "metric_value": _calc_metric(row, metric),
        })
    scored.sort(key=lambda x: x["metric_value"], reverse=True)

    data = []
    for rank, item in enumerate(scored, start=1):
        data.append({
            "rank": rank,
            "work_center_id": item["work_center_id"],
            "work_center_name": item["work_center_name"],
            "plant_name": item["plant_name"],
            "metric": metric,
            "metric_value": item["metric_value"],
        })

    return p.function_result(
        columns=["rank", "work_center_id", "work_center_name", "plant_name", "metric", "metric_value"],
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
