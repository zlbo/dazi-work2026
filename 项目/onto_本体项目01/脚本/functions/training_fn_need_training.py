"""培训需求分析函数 training.fn.need_training

参数：department（可选）, position（可选）, course_category（可选）
返回：各部门/岗位的培训需求分析，包括培训覆盖率、平均成绩、建议培训方向

发布：
  dazi-onto script publish 项目/onto_本体项目01/脚本/functions/training_fn_need_training.py \\
    --space space__0519 --register-function-id training.fn.need_training
"""


def _build_where(department, position, course_category):
    clauses = []
    if department:
        clauses.append(f"em.department = '{department}'")
    if position:
        clauses.append(f"em.position = '{position}'")
    if course_category:
        clauses.append(f"cm.course_category = '{course_category}'")
    return "WHERE " + " AND ".join(clauses) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    department = params.get("department", "")
    position = params.get("position", "")
    course_category = params.get("course_category", "")
    where_clause = _build_where(department, position, course_category)

    sql = f"""
    SELECT
        em.department,
        em.position,
        cm.course_category,
        count(DISTINCT em.employee_id) AS total_employees,
        count(DISTINCT tr.employee_id) AS trained_employees,
        count(DISTINCT tr.employee_id) * 100.0 / count(DISTINCT em.employee_id) AS coverage_rate,
        avg(tr.score) AS avg_score,
        sum(tr.score >= 60) * 100.0 / count(tr.record_id) AS qualified_rate,
        count(tr.record_id) AS training_count
    FROM employee_master em
    LEFT JOIN training_record tr ON em.employee_id = tr.employee_id
    LEFT JOIN course_master cm ON tr.course_id = cm.course_id
    {where_clause}
    GROUP BY em.department, em.position, cm.course_category
    ORDER BY coverage_rate ASC, training_count DESC
    """

    rows = p.sql.query(sql)
    
    data = []
    for row in rows:
        coverage_rate = float(row.get("coverage_rate", 0) or 0)
        avg_score = float(row.get("avg_score", 0) or 0)
        qualified_rate = float(row.get("qualified_rate", 0) or 0)
        
        if coverage_rate < 50:
            priority = "高"
            suggestion = f"培训覆盖率较低（{coverage_rate:.1f}%），建议加强该类别培训"
        elif coverage_rate < 80:
            priority = "中"
            suggestion = f"培训覆盖率中等（{coverage_rate:.1f}%），可适当增加培训频次"
        else:
            priority = "低"
            suggestion = "培训覆盖率较高，维持现状即可"
        
        if avg_score < 70:
            suggestion += f"，平均成绩偏低（{avg_score:.1f}分），建议优化课程内容"
        elif avg_score < 85:
            suggestion += f"，平均成绩中等（{avg_score:.1f}分），可适当提升课程难度"
        
        data.append({
            "department": row.get("department", ""),
            "position": row.get("position", ""),
            "course_category": row.get("course_category", ""),
            "total_employees": int(row.get("total_employees", 0) or 0),
            "trained_employees": int(row.get("trained_employees", 0) or 0),
            "coverage_rate": round(coverage_rate, 2),
            "avg_score": round(avg_score, 2),
            "qualified_rate": round(qualified_rate, 2),
            "training_count": int(row.get("training_count", 0) or 0),
            "priority": priority,
            "suggestion": suggestion,
        })

    return p.function_result(
        columns=["department", "position", "course_category", "total_employees", "trained_employees", "coverage_rate", "avg_score", "qualified_rate", "training_count", "priority", "suggestion"],
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