"""本体引擎测试 — 项目成本产值汇总 onto_engine.fn.project_summary

参数：start_date, end_date, project_id（可选）, region（可选）
返回：project_id, project_name, region, total_cost, total_budget, total_output, gross_profit, profit_rate

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/引擎测试/functions/onto_engine_fn_project_summary.py \\
    --space space__onto_engine_test --register-function-id onto_engine.fn.project_summary \\
    --register-platform-category 项目分析
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30"},
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
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", "2026-06-30")
    project_id = (params.get("project_id") or "").strip() or None
    region = (params.get("region") or "").strip() or None
    dc = _date_clause(start_date, end_date)

    proj_filter = ""
    if project_id:
        proj_filter += f" AND p.project_id = '{project_id}'"
    if region:
        proj_filter += f" AND p.region = '{region}'"

    sql = f"""
        SELECT
            p.project_id,
            p.project_name,
            p.region,
            coalesce(c.total_cost, 0) AS total_cost,
            coalesce(c.total_budget, 0) AS total_budget,
            coalesce(o.total_output, 0) AS total_output,
            coalesce(o.total_output, 0) - coalesce(c.total_cost, 0) AS gross_profit,
            if(coalesce(o.total_output, 0) > 0,
               (coalesce(o.total_output, 0) - coalesce(c.total_cost, 0)) / coalesce(o.total_output, 0),
               0) AS profit_rate
        FROM dim_project p
        LEFT JOIN (
            SELECT project_id,
                   sum(cost_amount) AS total_cost,
                   sum(budget_amount) AS total_budget
            FROM fact_cost
            WHERE 1=1 {dc}
            GROUP BY project_id
        ) c ON p.project_id = c.project_id
        LEFT JOIN (
            SELECT project_id, sum(output_amount) AS total_output
            FROM fact_output
            WHERE 1=1 {dc}
            GROUP BY project_id
        ) o ON p.project_id = o.project_id
        WHERE 1=1 {proj_filter}
        ORDER BY total_cost DESC
    """
    rows = p.sql.query(sql)
    data = []
    for row in rows:
        data.append({
            "project_id": row.get("project_id", ""),
            "project_name": row.get("project_name", ""),
            "region": row.get("region", ""),
            "total_cost": round(float(row.get("total_cost") or 0), 2),
            "total_budget": round(float(row.get("total_budget") or 0), 2),
            "total_output": round(float(row.get("total_output") or 0), 2),
            "gross_profit": round(float(row.get("gross_profit") or 0), 2),
            "profit_rate": round(float(row.get("profit_rate") or 0), 4),
        })
    return p.function_result(
        columns=[
            "project_id", "project_name", "region", "total_cost", "total_budget",
            "total_output", "gross_profit", "profit_rate",
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
