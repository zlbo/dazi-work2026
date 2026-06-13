"""商务成本 - 项目指标分析查询 cost.fn.indicator_analysis

参数：start_date, end_date, project_id（可选）
返回：project_id, project_name, report_period, gross_profit_rate, collection_rate, receivable_recovery_rate, cost_variance_rate, payment_ratio

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/商务成本/functions/cost_fn_indicator_analysis.py \
    --space space__panda_construction --register-function-id cost.fn.indicator_analysis
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31"},
    "object_type_code": "ProjectIndicator",
}


def _build_where(start_date, end_date, project_id=None):
    clauses = []
    if start_date and end_date:
        clauses.append(f"report_period >= '{start_date[:7]}' AND report_period <= '{end_date[:7]}'")
    if project_id:
        clauses.append(f"project_id = '{project_id}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    project_id = params.get("project_id") or None
    where_clause = _build_where(start_date, end_date, project_id)

    sql = f"""
    SELECT 
        i.project_id,
        p.project_name,
        i.report_period,
        i.gross_profit_rate,
        i.collection_rate,
        i.receivable_recovery_rate,
        i.cost_variance_rate,
        i.payment_ratio,
        i.indicator_value,
        i.target_value,
        i.actual_value,
        i.variance_value,
        i.variance_ratio
    FROM fact_project_indicator i
    JOIN dim_project p ON i.project_id = p.project_id
    {where_clause}
    ORDER BY i.report_period DESC, i.project_id
    """

    rows = p.sql.query(sql)
    data = []
    for row in rows:
        data.append({
            "project_id": row.get("project_id", ""),
            "project_name": row.get("project_name", ""),
            "report_period": row.get("report_period", ""),
            "gross_profit_rate": round(float(row.get("gross_profit_rate") or 0), 4),
            "collection_rate": round(float(row.get("collection_rate") or 0), 4),
            "receivable_recovery_rate": round(float(row.get("receivable_recovery_rate") or 0), 4),
            "cost_variance_rate": round(float(row.get("cost_variance_rate") or 0), 4),
            "payment_ratio": round(float(row.get("payment_ratio") or 0), 4),
            "indicator_value": round(float(row.get("indicator_value") or 0), 2),
            "target_value": round(float(row.get("target_value") or 0), 2),
            "actual_value": round(float(row.get("actual_value") or 0), 2),
            "variance_value": round(float(row.get("variance_value") or 0), 2),
            "variance_ratio": round(float(row.get("variance_ratio") or 0), 4),
        })

    return p.function_result(
        columns=["project_id", "project_name", "report_period", "gross_profit_rate", 
                 "collection_rate", "receivable_recovery_rate", "cost_variance_rate", 
                 "payment_ratio", "indicator_value", "target_value", "actual_value", 
                 "variance_value", "variance_ratio"],
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