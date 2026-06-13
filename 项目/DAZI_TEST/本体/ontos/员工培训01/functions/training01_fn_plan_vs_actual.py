"""training01.fn.plan_vs_actual — 计划 vs 实际"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "fiscal_year": 2025,
        "fiscal_period": 0,
        "plan_version": "2025年度培训计划",
    },
    "object_type_code": "TrainingPlan",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    fiscal_year = int(params.get("fiscal_year") or 2025)
    fiscal_period = int(params.get("fiscal_period") or 0)
    plan_version = params.get("plan_version") or "2025年度培训计划"
    org_id = (params.get("org_id") or "").strip()
    period_cond = "" if fiscal_period == 0 else f" AND p.fiscal_period = {fiscal_period}"
    org_cond = f" AND p.org_id = '{org_id}'" if org_id else ""

    sql = f"""
        SELECT
            p.org_name, p.category_type,
            sum(p.plan_headcount) AS plan_headcount,
            sum(p.plan_hours) AS plan_hours,
            sum(p.plan_cost) AS plan_cost,
            coalesce(a.actual_headcount, 0) AS actual_headcount,
            coalesce(a.actual_hours, 0) AS actual_hours,
            coalesce(a.actual_cost, 0) AS actual_cost
        FROM fact_training_plan p
        LEFT JOIN (
            SELECT org_id, category_type, fiscal_year, fiscal_period,
                   countIf(completion_status = '已完成') AS actual_headcount,
                   sum(training_hours) AS actual_hours,
                   sum(training_cost) AS actual_cost
            FROM fact_training_record
            WHERE fiscal_year = {fiscal_year}
            GROUP BY org_id, category_type, fiscal_year, fiscal_period
        ) a ON a.org_id = p.org_id AND a.category_type = p.category_type
            AND a.fiscal_year = p.fiscal_year AND a.fiscal_period = p.fiscal_period
        WHERE p.fiscal_year = {fiscal_year}
          AND p.plan_version = '{plan_version}'
          {period_cond} {org_cond}
        GROUP BY p.org_name, p.category_type, a.actual_headcount, a.actual_hours, a.actual_cost
        ORDER BY p.org_name, p.category_type
    """
    rows = p.sql.query(sql) or []
    data = []
    for r in rows:
        plan_hc = int(r.get("plan_headcount") or 0)
        plan_hrs = float(r.get("plan_hours") or 0)
        plan_cost = float(r.get("plan_cost") or 0)
        actual_hc = int(r.get("actual_headcount") or 0)
        actual_hrs = float(r.get("actual_hours") or 0)
        actual_cost = float(r.get("actual_cost") or 0)
        data.append({
            "org_name": r.get("org_name", ""),
            "category_type": r.get("category_type", ""),
            "plan_headcount": plan_hc,
            "actual_headcount": actual_hc,
            "plan_hours": round(plan_hrs, 2),
            "actual_hours": round(actual_hrs, 2),
            "plan_cost": round(plan_cost, 2),
            "actual_cost": round(actual_cost, 2),
            "headcount_exec_rate": round(actual_hc / plan_hc, 4) if plan_hc > 0 else 0,
            "hours_exec_rate": round(actual_hrs / plan_hrs, 4) if plan_hrs > 0 else 0,
        })
    return p.function_result(
        columns=["org_name", "category_type", "plan_headcount", "actual_headcount",
                 "plan_hours", "actual_hours", "plan_cost", "actual_cost",
                 "headcount_exec_rate", "hours_exec_rate"],
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
