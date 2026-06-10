"""商务成本 - 项目风险预警查询 cost.fn.risk_warning

参数：start_date, end_date, project_id（可选）, warning_level（可选：绿色/黄色/红色）
返回：project_id, project_name, report_period, risk_type, risk_name, risk_score, warning_level, warning_reason, risk_description

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/商务成本/functions/cost_fn_risk_warning.py \
    --space space__panda_construction --register-function-id cost.fn.risk_warning
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31"},
    "object_type_code": "ProjectRisk",
}


def _build_where(start_date, end_date, project_id=None, warning_level=None):
    clauses = []
    if start_date and end_date:
        clauses.append(f"report_period >= '{start_date[:7]}' AND report_period <= '{end_date[:7]}'")
    if project_id:
        clauses.append(f"r.project_id = '{project_id}'")
    if warning_level:
        clauses.append(f"warning_level = '{warning_level}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    project_id = params.get("project_id") or None
    warning_level = params.get("warning_level") or None
    where_clause = _build_where(start_date, end_date, project_id, warning_level)

    sql = f"""
    SELECT 
        r.id,
        r.project_id,
        p.project_name,
        r.report_period,
        r.risk_type,
        r.risk_code,
        r.risk_name,
        r.risk_score,
        r.warning_level,
        r.warning_reason,
        r.risk_description,
        r.response_measure
    FROM fact_project_risk r
    JOIN dim_project p ON r.project_id = p.project_id
    {where_clause}
    ORDER BY r.warning_level DESC, r.risk_score DESC, r.report_period DESC
    """

    rows = p.sql.query(sql)
    data = []
    for row in rows:
        data.append({
            "id": row.get("id", ""),
            "project_id": row.get("project_id", ""),
            "project_name": row.get("project_name", ""),
            "report_period": row.get("report_period", ""),
            "risk_type": row.get("risk_type", ""),
            "risk_code": row.get("risk_code", ""),
            "risk_name": row.get("risk_name", ""),
            "risk_score": round(float(row.get("risk_score") or 0), 2),
            "warning_level": row.get("warning_level", ""),
            "warning_reason": row.get("warning_reason", ""),
            "risk_description": row.get("risk_description", ""),
            "response_measure": row.get("response_measure", ""),
        })

    return p.function_result(
        columns=["id", "project_id", "project_name", "report_period", "risk_type", 
                 "risk_code", "risk_name", "risk_score", "warning_level", 
                 "warning_reason", "risk_description", "response_measure"],
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