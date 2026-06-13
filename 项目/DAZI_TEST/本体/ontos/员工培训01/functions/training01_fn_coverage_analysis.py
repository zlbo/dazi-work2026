"""training01.fn.coverage_analysis — 人员培训覆盖度"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31"},
    "object_type_code": "Employee",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", "2025-12-31")
    org_id = (params.get("org_id") or "").strip()
    lo = int(start_date.replace("-", "")[:8])
    hi = int(end_date.replace("-", "")[:8])
    org_cond = f" AND e.org_id = '{org_id}'" if org_id else ""

    sql = f"""
        SELECT
            e.org_id, e.org_name,
            count(DISTINCT e.employee_id) AS total_employees,
            count(DISTINCT r.employee_id) AS trained_employees,
            coalesce(sum(r.training_hours), 0) AS total_hours
        FROM dim_employee e
        LEFT JOIN fact_training_record r ON r.employee_id = e.employee_id
            AND r.date_key >= {lo} AND r.date_key <= {hi}
            AND r.completion_status = '已完成'
        WHERE e.employment_status = '在职' {org_cond}
        GROUP BY e.org_id, e.org_name
        ORDER BY trained_employees DESC
    """
    rows = p.sql.query(sql) or []
    data = []
    for r in rows:
        total = int(r.get("total_employees") or 0)
        trained = int(r.get("trained_employees") or 0)
        data.append({
            "org_id": r.get("org_id", ""),
            "org_name": r.get("org_name", ""),
            "total_employees": total,
            "trained_employees": trained,
            "coverage_rate": round(trained / total, 4) if total > 0 else 0,
            "total_hours": round(float(r.get("total_hours") or 0), 2),
            "avg_hours_per_trained": round(float(r.get("total_hours") or 0) / trained, 2) if trained > 0 else 0,
        })
    return p.function_result(
        columns=["org_id", "org_name", "total_employees", "trained_employees",
                 "coverage_rate", "total_hours", "avg_hours_per_trained"],
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
