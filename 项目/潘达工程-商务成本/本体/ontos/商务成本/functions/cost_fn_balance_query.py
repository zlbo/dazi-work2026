"""商务成本 - 项目收支查询 cost.fn.balance_query

参数：start_date, end_date, project_id（可选）, balance_type（可选：收入/支出）
返回：id, project_id, project_name, report_period, subject_code, subject_name, project_amount, company_amount, total_amount, balance_type

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/商务成本/functions/cost_fn_balance_query.py \
    --space space__panda_construction --register-function-id cost.fn.balance_query
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31"},
    "object_type_code": "ProjectBalance",
}


def _build_where(start_date, end_date, project_id=None, balance_type=None):
    clauses = []
    if start_date and end_date:
        clauses.append(f"report_period >= '{start_date[:7]}' AND report_period <= '{end_date[:7]}'")
    if project_id:
        clauses.append(f"b.project_id = '{project_id}'")
    if balance_type:
        clauses.append(f"balance_type = '{balance_type}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    project_id = params.get("project_id") or None
    balance_type = params.get("balance_type") or None
    where_clause = _build_where(start_date, end_date, project_id, balance_type)

    sql = f"""
    SELECT 
        b.id,
        b.project_id,
        p.project_name,
        b.report_period,
        b.subject_code,
        b.subject_name,
        b.project_amount,
        b.company_amount,
        b.total_amount,
        b.balance_type
    FROM fact_project_balance b
    JOIN dim_project p ON b.project_id = p.project_id
    {where_clause}
    ORDER BY b.report_period DESC, b.balance_type, b.project_id
    """

    rows = p.sql.query(sql)
    data = []
    for row in rows:
        data.append({
            "id": row.get("id", ""),
            "project_id": row.get("project_id", ""),
            "project_name": row.get("project_name", ""),
            "report_period": row.get("report_period", ""),
            "subject_code": row.get("subject_code", ""),
            "subject_name": row.get("subject_name", ""),
            "project_amount": round(float(row.get("project_amount") or 0), 2),
            "company_amount": round(float(row.get("company_amount") or 0), 2),
            "total_amount": round(float(row.get("total_amount") or 0), 2),
            "balance_type": row.get("balance_type", ""),
        })

    return p.function_result(
        columns=["id", "project_id", "project_name", "report_period", "subject_code", 
                 "subject_name", "project_amount", "company_amount", "total_amount", "balance_type"],
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