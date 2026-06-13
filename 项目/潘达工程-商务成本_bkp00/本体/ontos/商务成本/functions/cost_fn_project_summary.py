"""商务成本 - 项目成本汇总查询 cost.fn.project_summary

参数：start_date, end_date, project_id（可选）
返回：project_id, project_name, total_output, total_cost, gross_profit, gross_profit_rate

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/商务成本/functions/cost_fn_project_summary.py \
    --space space__panda_construction --register-function-id cost.fn.project_summary
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31"},
    "object_type_code": "ProjectAnalysis",
}


def _build_where(start_date, end_date, project_id=None):
    clauses = []
    if start_date and end_date:
        clauses.append(f"report_period >= '{start_date[:7]}' AND report_period <= '{end_date[:7]}'")
    if project_id:
        clauses.append(f"project_id = '{project_id}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    project_id = params.get("project_id") or None
    where_clause = _build_where(start_date, end_date, project_id)

    sql = f"""
    SELECT 
        p.project_id,
        p.project_name,
        COALESCE(SUM(o.output_value), 0) AS total_output,
        COALESCE(SUM(c.cost_amount), 0) AS total_cost,
        COALESCE(SUM(o.output_value), 0) - COALESCE(SUM(c.cost_amount), 0) AS gross_profit,
        CASE WHEN COALESCE(SUM(o.output_value), 0) > 0 
             THEN (COALESCE(SUM(o.output_value), 0) - COALESCE(SUM(c.cost_amount), 0)) / COALESCE(SUM(o.output_value), 0)
             ELSE 0 END AS gross_profit_rate
    FROM dim_project p
    LEFT JOIN fact_project_output o ON p.project_id = o.project_id {where_clause}
    LEFT JOIN fact_project_cost c ON p.project_id = c.project_id {where_clause}
    GROUP BY p.project_id, p.project_name
    ORDER BY total_output DESC
    """

    rows = p.sql.query(sql)
    data = []
    for row in rows:
        data.append({
            "project_id": row.get("project_id", ""),
            "project_name": row.get("project_name", ""),
            "total_output": round(float(row.get("total_output") or 0), 2),
            "total_cost": round(float(row.get("total_cost") or 0), 2),
            "gross_profit": round(float(row.get("gross_profit") or 0), 2),
            "gross_profit_rate": round(float(row.get("gross_profit_rate") or 0), 4),
        })

    return p.function_result(
        columns=["project_id", "project_name", "total_output", "total_cost", "gross_profit", "gross_profit_rate"],
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