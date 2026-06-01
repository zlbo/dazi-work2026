"""课程效果分析函数 training.fn.course_effectiveness

参数：course_id（可选，不传则返回所有课程）, start_date, end_date（可选）
返回：课程培训人次、完成率、平均成绩、合格率、讲师评分、内容评分、综合评分

发布：
  dazi-onto script publish 项目/onto_本体项目01/脚本/functions/training_fn_course_effectiveness.py \\
    --space space__0519 --register-function-id training.fn.course_effectiveness
"""


def _build_where(course_id, start_date, end_date):
    clauses = []
    if course_id:
        clauses.append(f"tr.course_id = '{course_id}'")
    if start_date and end_date:
        clauses.append(f"tr.training_date >= '{start_date}' AND tr.training_date <= '{end_date}'")
    return "WHERE " + " AND ".join(clauses) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    course_id = params.get("course_id", "")
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    where_clause = _build_where(course_id, start_date, end_date)

    sql = f"""
    SELECT
        tr.course_id,
        cm.course_name,
        cm.course_category,
        cm.course_level,
        count(tr.record_id) AS trained_count,
        sum(tr.completion = '完成') * 100.0 / count(tr.record_id) AS completion_rate,
        avg(tr.score) AS avg_score,
        sum(tr.score >= 60) * 100.0 / count(tr.record_id) AS qualified_rate,
        avg(te.trainer_score) AS avg_trainer_score,
        avg(te.content_score) AS avg_content_score,
        avg(te.overall_score) AS avg_overall_score
    FROM training_record tr
    LEFT JOIN course_master cm ON tr.course_id = cm.course_id
    LEFT JOIN training_evaluation te ON tr.record_id = te.record_id
    {where_clause}
    GROUP BY tr.course_id, cm.course_name, cm.course_category, cm.course_level
    ORDER BY trained_count DESC
    """

    rows = p.sql.query(sql)
    
    data = []
    for row in rows:
        data.append({
            "course_id": row.get("course_id", ""),
            "course_name": row.get("course_name", ""),
            "course_category": row.get("course_category", ""),
            "course_level": row.get("course_level", ""),
            "trained_count": int(row.get("trained_count", 0) or 0),
            "completion_rate": round(float(row.get("completion_rate", 0) or 0), 2),
            "avg_score": round(float(row.get("avg_score", 0) or 0), 2),
            "qualified_rate": round(float(row.get("qualified_rate", 0) or 0), 2),
            "avg_trainer_score": round(float(row.get("avg_trainer_score", 0) or 0), 2),
            "avg_content_score": round(float(row.get("avg_content_score", 0) or 0), 2),
            "avg_overall_score": round(float(row.get("avg_overall_score", 0) or 0), 2),
        })

    return p.function_result(
        columns=["course_id", "course_name", "course_category", "course_level", "trained_count", "completion_rate", "avg_score", "qualified_rate", "avg_trainer_score", "avg_content_score", "avg_overall_score"],
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