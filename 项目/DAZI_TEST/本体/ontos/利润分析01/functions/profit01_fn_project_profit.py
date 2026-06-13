"""profit01.fn.project_profit — 项目利润排行"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31", "limit": 10},
    "object_type_code": "Project",
}



def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", "2025-12-31")
    limit = int(params.get("limit") or 10)
    region = (params.get("region") or "").strip()
    lo = int(start_date.replace("-", "")[:8])
    hi = int(end_date.replace("-", "")[:8])
    region_filter = f" AND p.region = '{region}'" if region else ""

    sql = f"""
        SELECT
            p.project_id, p.project_name, p.region,
            coalesce(sum(f.revenue), 0) AS total_revenue,
            coalesce(sum(f.cost), 0) AS total_cost,
            coalesce(sum(f.gross_profit), 0) AS gross_profit,
            if(coalesce(sum(f.revenue), 0) > 0,
               coalesce(sum(f.gross_profit), 0) / coalesce(sum(f.revenue), 0), 0) AS profit_margin
        FROM dim_project p
        LEFT JOIN fact_project_profit f ON p.project_id = f.project_id
            AND f.date_key >= {lo} AND f.date_key <= {hi}
        WHERE 1=1 {region_filter}
        GROUP BY p.project_id, p.project_name, p.region
        ORDER BY gross_profit DESC
        LIMIT {limit}
    """
    rows = p.sql.query(sql) or []
    data = [{
        "project_id": r.get("project_id", ""),
        "project_name": r.get("project_name", ""),
        "region": r.get("region", ""),
        "total_revenue": round(float(r.get("total_revenue") or 0), 2),
        "total_cost": round(float(r.get("total_cost") or 0), 2),
        "gross_profit": round(float(r.get("gross_profit") or 0), 2),
        "profit_margin": round(float(r.get("profit_margin") or 0), 4),
    } for r in rows]
    return p.function_result(
        columns=["project_id", "project_name", "region", "total_revenue", "total_cost", "gross_profit", "profit_margin"],
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
