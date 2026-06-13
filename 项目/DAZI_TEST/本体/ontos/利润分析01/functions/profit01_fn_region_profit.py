"""profit01.fn.region_profit — 片区利润对比"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31"},
    "object_type_code": "ProfitAnalysis",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", "2025-12-31")
    lo = int(start_date.replace("-", "")[:8])
    hi = int(end_date.replace("-", "")[:8])

    sql = f"""
        SELECT
            region,
            sum(revenue) AS total_revenue,
            sum(cost) AS total_cost,
            sum(gross_profit) AS gross_profit,
            count(DISTINCT project_id) AS project_count
        FROM fact_project_profit
        WHERE region != '' AND date_key >= {lo} AND date_key <= {hi}
        GROUP BY region
        ORDER BY gross_profit DESC
    """
    rows = p.sql.query(sql) or []
    data = []
    for r in rows:
        rev = float(r.get("total_revenue") or 0)
        gp = float(r.get("gross_profit") or 0)
        data.append({
            "region": r.get("region", ""),
            "total_revenue": round(rev, 2),
            "total_cost": round(float(r.get("total_cost") or 0), 2),
            "gross_profit": round(gp, 2),
            "profit_margin": round(gp / rev, 4) if rev > 0 else 0,
            "project_count": int(r.get("project_count") or 0),
        })
    return p.function_result(
        columns=["region", "total_revenue", "total_cost", "gross_profit", "profit_margin", "project_count"],
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
