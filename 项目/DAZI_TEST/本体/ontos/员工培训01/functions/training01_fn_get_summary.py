"""training01.fn.get_summary — 培训总览"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31"},
    "object_type_code": "TrainingAnalysis",
}


def _date_clause(start_date, end_date):
    lo = int(str(start_date).replace("-", "")[:8])
    hi = int(str(end_date).replace("-", "")[:8])
    return lo, hi


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", "2025-12-31")
    org_id = (params.get("org_id") or "").strip()
    lo, hi = _date_clause(start_date, end_date)
    org_filter = f" AND org_id = '{org_id}'" if org_id else ""

    sql = f"""
        SELECT
            count() AS enroll_count,
            countIf(completion_status = '已完成') AS complete_count,
            countIf(pass_flag = 1) AS pass_count,
            coalesce(sum(training_hours), 0) AS total_hours,
            coalesce(sum(training_cost), 0) AS total_cost,
            coalesce(avgIf(exam_score, completion_status = '已完成'), 0) AS avg_exam_score
        FROM fact_training_record
        WHERE date_key >= {lo} AND date_key <= {hi} {org_filter}
    """
    row = (p.sql.query(sql) or [{}])[0]
    enroll = int(row.get("enroll_count") or 0)
    complete = int(row.get("complete_count") or 0)
    passed = int(row.get("pass_count") or 0)
    data = [{
        "period": f"{start_date} ~ {end_date}",
        "enroll_count": enroll,
        "complete_count": complete,
        "pass_count": passed,
        "total_hours": round(float(row.get("total_hours") or 0), 2),
        "total_cost": round(float(row.get("total_cost") or 0), 2),
        "completion_rate": round(complete / enroll, 4) if enroll > 0 else 0,
        "pass_rate": round(passed / complete, 4) if complete > 0 else 0,
        "avg_exam_score": round(float(row.get("avg_exam_score") or 0), 2),
    }]
    return p.function_result(
        columns=["period", "enroll_count", "complete_count", "pass_count", "total_hours",
                 "total_cost", "completion_rate", "pass_rate", "avg_exam_score"],
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
