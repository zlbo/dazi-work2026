"""本体引擎测试 — 片区成本汇总 onto_engine.fn.region_cost

参数：start_date, end_date
返回：region, total_cost, total_budget, budget_exec_rate, project_count

锚点问句：「按片区看本月开销」

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/引擎测试/functions/onto_engine_fn_region_cost.py \\
    --space space__onto_engine_test --register-function-id onto_engine.fn.region_cost \\
    --register-platform-category 地域分析
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2026-06-01", "end_date": "2026-06-30"},
    "object_type_code": "Project",
}


def _date_clause(start_date, end_date):
    if not start_date or not end_date:
        return ""
    lo = int(str(start_date).replace("-", "")[:8])
    hi = int(str(end_date).replace("-", "")[:8])
    return f" AND date_key >= {lo} AND date_key <= {hi}"


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2026-06-01")
    end_date = params.get("end_date", "2026-06-30")
    dc = _date_clause(start_date, end_date)

    sql = f"""
        SELECT
            region,
            sum(cost_amount) AS total_cost,
            sum(budget_amount) AS total_budget,
            count(DISTINCT project_id) AS project_count
        FROM fact_cost
        WHERE region != '' {dc}
        GROUP BY region
        ORDER BY total_cost DESC
    """
    rows = p.sql.query(sql)
    data = []
    for row in rows:
        cost = float(row.get("total_cost") or 0)
        budget = float(row.get("total_budget") or 0)
        data.append({
            "region": row.get("region", ""),
            "total_cost": round(cost, 2),
            "total_budget": round(budget, 2),
            "budget_exec_rate": round(cost / budget, 4) if budget > 0 else 0,
            "project_count": int(row.get("project_count") or 0),
        })
    return p.function_result(
        columns=["region", "total_cost", "total_budget", "budget_exec_rate", "project_count"],
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
