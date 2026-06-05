"""培训趋势分析函数 training.fn.training_trend

参数：start_date, end_date, period_type（可选，默认为'month'，可选'month'或'quarter'）
返回：按时间维度的培训人次、参训员工数、完成率、平均成绩、合格率趋势

发布：
  dazi-onto script publish 项目/onto_本体项目01/脚本/functions/training_fn_training_trend.py \\
    --space space__0519 --register-function-id training.fn.training_trend
"""


def _build_time_group(period_type):
    if period_type == "quarter":
        return "toYearMonth(training_date) AS year_month, toQuarter(training_date) AS quarter, toYear(training_date) AS year, 'Q' || toString(toQuarter(training_date)) || ' ' || toString(toYear(training_date)) AS period"
    else:
        return "toYearMonth(training_date) AS year_month, toQuarter(training_date) AS quarter, toYear(training_date) AS year, toString(toYear(training_date)) || '-' || lpad(toString(toMonth(training_date)), 2, '0') AS period"


def _build_order_by(period_type):
    if period_type == "quarter":
        return "ORDER BY year, quarter"
    else:
        return "ORDER BY year_month"


def _build_where(start_date, end_date):
    clauses = []
    if start_date and end_date:
        clauses.append(f"training_date >= '{start_date}' AND training_date <= '{end_date}'")
    return "WHERE " + " AND ".join(clauses) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    period_type = params.get("period_type", "month")
    
    where_clause = _build_where(start_date, end_date)
    time_group = _build_time_group(period_type)
    order_by = _build_order_by(period_type)

    sql = f"""
    SELECT
        {time_group},
        count(record_id) AS total_trainings,
        uniq(employee_id) AS total_employees,
        sum(completion = '完成') * 100.0 / count(record_id) AS completion_rate,
        avg(score) AS avg_score,
        sum(score >= 60) * 100.0 / count(record_id) AS qualified_rate
    FROM training_record
    {where_clause}
    GROUP BY year_month, quarter, year, period
    {order_by}
    """

    rows = p.sql.query(sql)
    
    data = []
    for row in rows:
        data.append({
            "year_month": row.get("year_month", ""),
            "quarter": row.get("quarter", ""),
            "year": str(row.get("year", "")),
            "period": row.get("period", ""),
            "total_trainings": int(row.get("total_trainings", 0) or 0),
            "total_employees": int(row.get("total_employees", 0) or 0),
            "completion_rate": round(float(row.get("completion_rate", 0) or 0), 2),
            "avg_score": round(float(row.get("avg_score", 0) or 0), 2),
            "qualified_rate": round(float(row.get("qualified_rate", 0) or 0), 2),
        })

    return p.function_result(
        columns=["year_month", "quarter", "year", "period", "total_trainings", "total_employees", "completion_rate", "avg_score", "qualified_rate"],
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