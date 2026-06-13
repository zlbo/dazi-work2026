"""本体引擎测试 — 空间总览汇总 onto_engine.fn.get_summary

参数：start_date, end_date（YYYY-MM-DD）
返回：total_cost, total_budget, total_output, gross_profit, budget_exec_rate, project_count

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/引擎测试/functions/onto_engine_fn_get_summary.py \\
    --space space__onto_engine_test --register-function-id onto_engine.fn.get_summary \\
    --register-platform-category 总览分析
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30"},
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
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", "2026-06-30")
    dc = _date_clause(start_date, end_date)

    cost_sql = f"""
        SELECT
            sum(cost_amount) AS total_cost,
            sum(budget_amount) AS total_budget,
            count(DISTINCT project_id) AS project_count
        FROM fact_cost
        WHERE 1=1 {dc}
    """
    out_sql = f"""
        SELECT sum(output_amount) AS total_output
        FROM fact_output
        WHERE 1=1 {dc}
    """
    cost_row = (p.sql.query(cost_sql) or [{}])[0]
    out_row = (p.sql.query(out_sql) or [{}])[0]

    total_cost = float(cost_row.get("total_cost") or 0)
    total_budget = float(cost_row.get("total_budget") or 0)
    total_output = float(out_row.get("total_output") or 0)
    gross_profit = total_output - total_cost
    exec_rate = total_cost / total_budget if total_budget > 0 else 0

    data = [{
        "period": f"{start_date} ~ {end_date}",
        "total_cost": round(total_cost, 2),
        "total_budget": round(total_budget, 2),
        "total_output": round(total_output, 2),
        "gross_profit": round(gross_profit, 2),
        "budget_exec_rate": round(exec_rate, 4),
        "project_count": int(cost_row.get("project_count") or 0),
    }]
    return p.function_result(
        columns=[
            "period", "total_cost", "total_budget", "total_output",
            "gross_profit", "budget_exec_rate", "project_count",
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
