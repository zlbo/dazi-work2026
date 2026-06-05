"""部门培训统计函数 training.fn.department_training

参数：department（可选，不传则返回所有部门）, start_date, end_date（可选）
返回：部门培训人次、参训员工数、完成率、平均成绩、合格率

发布：
  dazi-onto script publish 项目/onto_本体项目01/脚本/functions/training_fn_department_training.py \\
    --space space__0519 --register-function-id training.fn.department_training
"""


def _build_where(department, start_date, end_date):
    clauses = []
    if department:
        clauses.append(f"em.department = '{department}'")
    if start_date and end_date:
        clauses.append(f"tr.training_date >= '{start_date}' AND tr.training_date <= '{end_date}'")
    return "WHERE " + " AND ".join(clauses) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    department = params.get("department", "")
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    where_clause = _build_where(department, start_date, end_date)

    sql = f"""
    SELECT
        em.department,
        count(tr.record_id) AS total_trainings,
        uniq(tr.employee_id) AS total_employees,
        sum(tr.completion = '完成') * 100.0 / count(tr.record_id) AS completion_rate,
        avg(tr.score) AS avg_score,
        sum(tr.score >= 60) * 100.0 / count(tr.record_id) AS qualified_rate
    FROM training_record tr
    LEFT JOIN employee_master em ON tr.employee_id = em.employee_id
    {where_clause}
    GROUP BY em.department
    ORDER BY total_trainings DESC
    """

    rows = p.sql.query(sql)
    
    data = []
    for row in rows:
        data.append({
            "department": row.get("department", ""),
            "total_trainings": int(row.get("total_trainings", 0) or 0),
            "total_employees": int(row.get("total_employees", 0) or 0),
            "completion_rate": round(float(row.get("completion_rate", 0) or 0), 2),
            "avg_score": round(float(row.get("avg_score", 0) or 0), 2),
            "qualified_rate": round(float(row.get("qualified_rate", 0) or 0), 2),
        })

    return p.function_result(
        columns=["department", "total_trainings", "total_employees", "completion_rate", "avg_score", "qualified_rate"],
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