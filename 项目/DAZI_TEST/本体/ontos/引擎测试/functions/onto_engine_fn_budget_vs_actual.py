"""本体引擎测试 — 项目预实对比 onto_engine.fn.budget_vs_actual

参数：start_date, end_date, region（可选）, overrun_only（可选 bool，仅超支项目）
返回：project_id, project_name, region, budget_amount, actual_amount, variance, execution_rate, is_overrun

与决策规则 cost_overrun_alert（budget_exec_rate > 1）互补。

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/引擎测试/functions/onto_engine_fn_budget_vs_actual.py \\
    --space space__onto_engine_test --register-function-id onto_engine.fn.budget_vs_actual \\
    --register-platform-category 预实分析
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2026-04-01", "end_date": "2026-06-30", "overrun_only": True},
    "object_type_code": "CostAnalysis",
}


def _date_clause(start_date, end_date):
    if not start_date or not end_date:
        return ""
    lo = int(str(start_date).replace("-", "")[:8])
    hi = int(str(end_date).replace("-", "")[:8])
    return f" AND date_key >= {lo} AND date_key <= {hi}"


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2026-04-01")
    end_date = params.get("end_date", "2026-06-30")
    region = (params.get("region") or "").strip() or None
    overrun_only = bool(params.get("overrun_only", False))
    dc = _date_clause(start_date, end_date)

    region_cond = f" AND region = '{region}'" if region else ""
    sql = f"""
        SELECT
            project_id,
            any(project_name) AS project_name,
            any(region) AS region,
            sum(budget_amount) AS budget_amount,
            sum(cost_amount) AS actual_amount
        FROM fact_cost
        WHERE 1=1 {dc} {region_cond}
        GROUP BY project_id
        ORDER BY actual_amount / greatest(budget_amount, 0.01) DESC
    """
    rows = p.sql.query(sql)
    data = []
    for row in rows:
        budget = float(row.get("budget_amount") or 0)
        actual = float(row.get("actual_amount") or 0)
        rate = actual / budget if budget > 0 else 0
        is_overrun = rate > 1.0
        if overrun_only and not is_overrun:
            continue
        data.append({
            "project_id": row.get("project_id", ""),
            "project_name": row.get("project_name", ""),
            "region": row.get("region", ""),
            "budget_amount": round(budget, 2),
            "actual_amount": round(actual, 2),
            "variance": round(actual - budget, 2),
            "execution_rate": round(rate, 4),
            "is_overrun": 1 if is_overrun else 0,
        })
    return p.function_result(
        columns=[
            "project_id", "project_name", "region", "budget_amount", "actual_amount",
            "variance", "execution_rate", "is_overrun",
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
