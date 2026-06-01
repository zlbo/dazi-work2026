"""讲师绩效评估函数 training.fn.trainer_performance

参数：trainer_id（可选，不传则返回所有讲师）, start_date, end_date（可选）
返回：讲师授课次数、平均讲师评分、平均内容评分、平均环境评分、平均综合评分

发布：
  dazi-onto script publish 项目/onto_本体项目01/脚本/functions/training_fn_trainer_performance.py \\
    --space space__0519 --register-function-id training.fn.trainer_performance
"""


def _build_where(trainer_id, start_date, end_date):
    clauses = []
    if trainer_id:
        clauses.append(f"cm.trainer_id = '{trainer_id}'")
    if start_date and end_date:
        clauses.append(f"tr.training_date >= '{start_date}' AND tr.training_date <= '{end_date}'")
    return "WHERE " + " AND ".join(clauses) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    trainer_id = params.get("trainer_id", "")
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    where_clause = _build_where(trainer_id, start_date, end_date)

    sql = f"""
    SELECT
        tm.trainer_id,
        tm.trainer_name,
        tm.department,
        tm.expertise,
        tm.qualification,
        count(DISTINCT tr.record_id) AS training_count,
        avg(te.trainer_score) AS avg_trainer_score,
        avg(te.content_score) AS avg_content_score,
        avg(te.environment_score) AS avg_environment_score,
        avg(te.overall_score) AS avg_overall_score
    FROM training_record tr
    LEFT JOIN course_master cm ON tr.course_id = cm.course_id
    LEFT JOIN trainer_master tm ON cm.trainer_id = tm.trainer_id
    LEFT JOIN training_evaluation te ON tr.record_id = te.record_id
    {where_clause}
    GROUP BY tm.trainer_id, tm.trainer_name, tm.department, tm.expertise, tm.qualification
    ORDER BY training_count DESC
    """

    rows = p.sql.query(sql)
    
    data = []
    for row in rows:
        data.append({
            "trainer_id": row.get("trainer_id", ""),
            "trainer_name": row.get("trainer_name", ""),
            "department": row.get("department", ""),
            "expertise": row.get("expertise", ""),
            "qualification": row.get("qualification", ""),
            "training_count": int(row.get("training_count", 0) or 0),
            "avg_trainer_score": round(float(row.get("avg_trainer_score", 0) or 0), 2),
            "avg_content_score": round(float(row.get("avg_content_score", 0) or 0), 2),
            "avg_environment_score": round(float(row.get("avg_environment_score", 0) or 0), 2),
            "avg_overall_score": round(float(row.get("avg_overall_score", 0) or 0), 2),
        })

    return p.function_result(
        columns=["trainer_id", "trainer_name", "department", "expertise", "qualification", "training_count", "avg_trainer_score", "avg_content_score", "avg_environment_score", "avg_overall_score"],
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