"""员工培训档案函数 training.fn.employee_training

参数：employee_id, start_date, end_date（可选）
返回：员工培训记录明细，包括课程信息、培训日期、出勤状态、完成状态、成绩、证书编号

发布：
  dazi-onto script publish 项目/onto_本体项目01/脚本/functions/training_fn_employee_training.py \\
    --space space__0519 --register-function-id training.fn.employee_training
"""


def _build_where(employee_id, start_date, end_date):
    clauses = []
    if employee_id:
        clauses.append(f"tr.employee_id = '{employee_id}'")
    if start_date and end_date:
        clauses.append(f"tr.training_date >= '{start_date}' AND tr.training_date <= '{end_date}'")
    return "WHERE " + " AND ".join(clauses) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    employee_id = params.get("employee_id", "")
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    where_clause = _build_where(employee_id, start_date, end_date)

    sql = f"""
    SELECT
        tr.employee_id,
        em.employee_name,
        em.department,
        em.position,
        tr.course_id,
        cm.course_name,
        cm.course_category,
        cm.course_level,
        tr.training_date,
        tr.attendance,
        tr.completion,
        tr.score,
        tr.certificate_no
    FROM training_record tr
    LEFT JOIN employee_master em ON tr.employee_id = em.employee_id
    LEFT JOIN course_master cm ON tr.course_id = cm.course_id
    {where_clause}
    ORDER BY tr.training_date DESC, tr.record_id
    """

    rows = p.sql.query(sql)
    
    data = []
    for row in rows:
        data.append({
            "employee_id": row.get("employee_id", ""),
            "employee_name": row.get("employee_name", ""),
            "department": row.get("department", ""),
            "position": row.get("position", ""),
            "course_id": row.get("course_id", ""),
            "course_name": row.get("course_name", ""),
            "course_category": row.get("course_category", ""),
            "course_level": row.get("course_level", ""),
            "training_date": str(row.get("training_date", "")),
            "attendance": row.get("attendance", ""),
            "completion": row.get("completion", ""),
            "score": float(row.get("score", 0) or 0) if row.get("score") else None,
            "certificate_no": row.get("certificate_no", ""),
        })

    return p.function_result(
        columns=["employee_id", "employee_name", "department", "position", "course_id", "course_name", "course_category", "course_level", "training_date", "attendance", "completion", "score", "certificate_no"],
        data=data,
        row_count=len(data),
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