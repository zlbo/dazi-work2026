"""培训总览函数 training.fn.get_summary

参数：start_date, end_date（可选）
返回：培训总人次、参训员工数、开设课程数、平均出勤率、平均完成率、平均考核成绩、平均合格率

发布：
  dazi-onto script publish 项目/onto_本体项目01/脚本/functions/training_fn_get_summary.py \\
    --space space__0519 --register-function-id training.fn.get_summary
"""


def _build_where(start_date, end_date):
    clauses = []
    if start_date and end_date:
        clauses.append(f"training_date >= '{start_date}' AND training_date <= '{end_date}'")
    return "WHERE " + " AND ".join(clauses) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    where_clause = _build_where(start_date, end_date)

    sql = f"""
    SELECT
        count(record_id) AS total_trainings,
        uniq(employee_id) AS total_employees,
        uniq(course_id) AS total_courses,
        sum(attendance = '出勤') * 100.0 / count(record_id) AS attendance_rate,
        sum(completion = '完成') * 100.0 / count(record_id) AS completion_rate,
        avg(score) AS avg_score,
        sum(score >= 60) * 100.0 / count(record_id) AS qualified_rate
    FROM training_record
    {where_clause}
    """

    rows = p.sql.query(sql)
    row = rows[0] if rows else {}
    
    data = [{
        "total_trainings": int(row.get("total_trainings", 0) or 0),
        "total_employees": int(row.get("total_employees", 0) or 0),
        "total_courses": int(row.get("total_courses", 0) or 0),
        "attendance_rate": round(float(row.get("attendance_rate", 0) or 0), 2),
        "completion_rate": round(float(row.get("completion_rate", 0) or 0), 2),
        "avg_score": round(float(row.get("avg_score", 0) or 0), 2),
        "qualified_rate": round(float(row.get("qualified_rate", 0) or 0), 2),
    }]

    return p.function_result(
        columns=["total_trainings", "total_employees", "total_courses", "attendance_rate", "completion_rate", "avg_score", "qualified_rate"],
        data=data,
        row_count=1,
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