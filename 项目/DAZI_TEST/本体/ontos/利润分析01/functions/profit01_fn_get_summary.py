"""profit01.fn.get_summary — 利润总览

发布：
  dazi onto script publish .../profit01_fn_get_summary.py \\
    --space space__onto_engine_test --register-function-id profit01.fn.get_summary
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31"},
    "object_type_code": "ProfitAnalysis",
}


def _date_clause(start_date, end_date):
    lo = int(str(start_date).replace("-", "")[:8])
    hi = int(str(end_date).replace("-", "")[:8])
    return f" AND date_key >= {lo} AND date_key <= {hi}"


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", "2025-12-31")
    org_id = (params.get("org_id") or "").strip()
    dc = _date_clause(start_date, end_date)
    org_filter = f" AND org_id = '{org_id}'" if org_id else ""

    rev_sql = f"""
        SELECT sum(output_amount) AS total_revenue
        FROM fact_output WHERE 1=1 {dc} {org_filter}
    """
    cost_sql = f"""
        SELECT sum(cost_amount) AS total_cost, count(DISTINCT project_id) AS project_count
        FROM fact_cost WHERE 1=1 {dc} {org_filter}
    """
    rev = float((p.sql.query(rev_sql) or [{}])[0].get("total_revenue") or 0)
    cost_row = (p.sql.query(cost_sql) or [{}])[0]
    cost = float(cost_row.get("total_cost") or 0)
    gp = rev - cost
    margin = gp / rev if rev > 0 else 0

    data = [{
        "period": f"{start_date} ~ {end_date}",
        "total_revenue": round(rev, 2),
        "total_cost": round(cost, 2),
        "gross_profit": round(gp, 2),
        "profit_margin": round(margin, 4),
        "project_count": int(cost_row.get("project_count") or 0),
    }]
    return p.function_result(
        columns=["period", "total_revenue", "total_cost", "gross_profit", "profit_margin", "project_count"],
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
