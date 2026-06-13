"""training01.fn.org_breakdown — 组织培训对比"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31", "org_level": 3},
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
            o.org_id, o.org_code, o.org_name, o.org_level,
            count(r.record_id) AS enroll_count,
            countIf(r.completion_status = '已完成') AS complete_count,
            coalesce(sum(r.training_hours), 0) AS total_hours,
            coalesce(sum(r.training_cost), 0) AS total_cost,
            uniq(r.employee_id) AS trained_employees
        FROM dim_org o
        LEFT JOIN fact_training_record r ON r.org_id = o.org_id
            AND r.date_key >= {lo} AND r.date_key <= {hi}
        WHERE 1=1 {level_cond}
        GROUP BY o.org_id, o.org_code, o.org_name, o.org_level
        HAVING enroll_count > 0
        ORDER BY total_hours DESC
    """
    rows = p.sql.query(sql) or []
    data = []
    for r in rows:
        enroll = int(r.get("enroll_count") or 0)
        complete = int(r.get("complete_count") or 0)
        trained = int(r.get("trained_employees") or 0)
        hours = float(r.get("total_hours") or 0)
        data.append({
            "org_id": r.get("org_id", ""),
            "org_code": r.get("org_code", ""),
            "org_name": r.get("org_name", ""),
            "org_level": int(r.get("org_level") or 0),
            "enroll_count": enroll,
            "complete_count": complete,
            "completion_rate": round(complete / enroll, 4) if enroll > 0 else 0,
            "total_hours": round(hours, 2),
            "total_cost": round(float(r.get("total_cost") or 0), 2),
            "avg_hours_per_person": round(hours / trained, 2) if trained > 0 else 0,
        })
    return p.function_result(
        columns=["org_id", "org_code", "org_name", "org_level", "enroll_count", "complete_count",
                 "completion_rate", "total_hours", "total_cost", "avg_hours_per_person"],
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
