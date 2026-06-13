"""profit01.fn.cost_type_breakdown — 成本科目结构"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31"},
    "object_type_code": "CostType",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", "2025-12-31")
    project_id = (params.get("project_id") or "").strip()
    lo = int(start_date.replace("-", "")[:8])
    hi = int(end_date.replace("-", "")[:8])
    proj_filter = f" AND c.project_id = '{project_id}'" if project_id else ""

    sql = f"""
        SELECT
            t.cost_type_id, t.cost_type_code, t.cost_type_name,
            t.parent_type_id,
            coalesce(sum(c.cost_amount), 0) AS cost_amount,
            coalesce(sum(c.budget_amount), 0) AS budget_amount
        FROM dim_cost_type t
        LEFT JOIN fact_cost c ON c.cost_type_id = t.cost_type_id
            AND c.date_key >= {lo} AND c.date_key <= {hi} {proj_filter}
        GROUP BY t.cost_type_id, t.cost_type_code, t.cost_type_name, t.parent_type_id
        HAVING cost_amount > 0 OR budget_amount > 0
        ORDER BY cost_amount DESC
    """
    rows = p.sql.query(sql) or []
    total = sum(float(r.get("cost_amount") or 0) for r in rows)
    data = [{
        "cost_type_code": r.get("cost_type_code", ""),
        "cost_type_name": r.get("cost_type_name", ""),
        "parent_type_id": r.get("parent_type_id", ""),
        "cost_amount": round(float(r.get("cost_amount") or 0), 2),
        "budget_amount": round(float(r.get("budget_amount") or 0), 2),
        "share_pct": round(float(r.get("cost_amount") or 0) / total, 4) if total > 0 else 0,
    } for r in rows]
    return p.function_result(
        columns=["cost_type_code", "cost_type_name", "parent_type_id", "cost_amount", "budget_amount", "share_pct"],
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
