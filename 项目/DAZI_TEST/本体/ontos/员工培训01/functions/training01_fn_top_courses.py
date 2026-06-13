"""training01.fn.top_courses — Top 参训/低通过率课程"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31", "limit": 10, "sort_by": "enroll"},
    "object_type_code": "Course",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", "2025-12-31")
    limit = int(params.get("limit") or 10)
    sort_by = (params.get("sort_by") or "enroll").strip()
    lo = int(start_date.replace("-", "")[:8])
    hi = int(end_date.replace("-", "")[:8])
    order_col = "pass_rate ASC" if sort_by == "pass_rate" else "enroll_count DESC"

    sql = f"""
        SELECT
            course_id, course_name, category_type,
            count() AS enroll_count,
            countIf(completion_status = '已完成') AS complete_count,
            countIf(pass_flag = 1) AS pass_count,
            coalesce(avgIf(exam_score, completion_status = '已完成'), 0) AS avg_exam_score
        FROM fact_training_record
        WHERE date_key >= {lo} AND date_key <= {hi}
        GROUP BY course_id, course_name, category_type
        ORDER BY {order_col}
        LIMIT {limit}
    """
    rows = p.sql.query(sql) or []
    data = []
    for r in rows:
        complete = int(r.get("complete_count") or 0)
        passed = int(r.get("pass_count") or 0)
        data.append({
            "course_id": r.get("course_id", ""),
            "course_name": r.get("course_name", ""),
            "category_type": r.get("category_type", ""),
            "enroll_count": int(r.get("enroll_count") or 0),
            "complete_count": complete,
            "pass_count": passed,
            "pass_rate": round(passed / complete, 4) if complete > 0 else 0,
            "avg_exam_score": round(float(r.get("avg_exam_score") or 0), 2),
        })
    return p.function_result(
        columns=["course_id", "course_name", "category_type", "enroll_count", "complete_count",
                 "pass_count", "pass_rate", "avg_exam_score"],
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
