"""profit01.fn.org_profit — 组织利润树"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31", "org_level": 2},
    "object_type_code": "Org",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", "2025-12-31")
    org_level = int(params.get("org_level") or 0)
    lo = int(start_date.replace("-", "")[:8])
    hi = int(end_date.replace("-", "")[:8])
    level_cond = f" AND o.org_level = {org_level}" if org_level else ""

    sql = f"""
        SELECT
            o.org_id, o.org_code, o.org_name, o.org_level, o.parent_org_id,
            coalesce(sum(f.revenue), 0) AS total_revenue,
            coalesce(sum(f.cost), 0) AS total_cost,
            coalesce(sum(f.gross_profit), 0) AS gross_profit
        FROM dim_org o
        LEFT JOIN fact_project_profit f ON f.org_id = o.org_id
            AND f.date_key >= {lo} AND f.date_key <= {hi}
        WHERE 1=1 {level_cond}
        GROUP BY o.org_id, o.org_code, o.org_name, o.org_level, o.parent_org_id
        ORDER BY gross_profit DESC
    """
    rows = p.sql.query(sql) or []
    data = []
    for r in rows:
        rev = float(r.get("total_revenue") or 0)
        gp = float(r.get("gross_profit") or 0)
        data.append({
            "org_id": r.get("org_id", ""),
            "org_code": r.get("org_code", ""),
            "org_name": r.get("org_name", ""),
            "org_level": int(r.get("org_level") or 0),
            "total_revenue": round(rev, 2),
            "total_cost": round(float(r.get("total_cost") or 0), 2),
            "gross_profit": round(gp, 2),
            "profit_margin": round(gp / rev, 4) if rev > 0 else 0,
        })
    return p.function_result(
        columns=["org_id", "org_code", "org_name", "org_level", "total_revenue", "total_cost", "gross_profit", "profit_margin"],
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
