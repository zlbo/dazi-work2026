"""商务成本 - 项目产值查询 cost.fn.output_query

参数：start_date, end_date, project_id（可选）, output_type（可选）
返回：id, project_id, project_name, report_period, output_value, output_tax, output_without_tax, output_type, output_ratio, confirm_type

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/商务成本/functions/cost_fn_output_query.py \
    --space space__panda_construction --register-function-id cost.fn.output_query
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31"},
    "object_type_code": "ProjectOutput",
}


def _build_where(start_date, end_date, project_id=None, output_type=None):
    clauses = []
    if start_date and end_date:
        clauses.append(f"report_period >= '{start_date[:7]}' AND report_period <= '{end_date[:7]}'")
    if project_id:
        clauses.append(f"o.project_id = '{project_id}'")
    if output_type:
        clauses.append(f"output_type = '{output_type}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    project_id = params.get("project_id") or None
    output_type = params.get("output_type") or None
    where_clause = _build_where(start_date, end_date, project_id, output_type)

    sql = f"""
    SELECT 
        o.id,
        o.project_id,
        p.project_name,
        o.report_period,
        o.output_value,
        o.output_tax,
        o.output_without_tax,
        o.output_type,
        o.output_ratio,
        o.confirm_type,
        o.confirmed_output,
        o.pending_output
    FROM fact_project_output o
    JOIN dim_project p ON o.project_id = p.project_id
    {where_clause}
    ORDER BY o.report_period DESC, o.project_id
    """

    rows = p.sql.query(sql)
    data = []
    for row in rows:
        data.append({
            "id": row.get("id", ""),
            "project_id": row.get("project_id", ""),
            "project_name": row.get("project_name", ""),
            "report_period": row.get("report_period", ""),
            "output_value": round(float(row.get("output_value") or 0), 2),
            "output_tax": round(float(row.get("output_tax") or 0), 2),
            "output_without_tax": round(float(row.get("output_without_tax") or 0), 2),
            "output_type": row.get("output_type", ""),
            "output_ratio": round(float(row.get("output_ratio") or 0), 4),
            "confirm_type": row.get("confirm_type", ""),
            "confirmed_output": round(float(row.get("confirmed_output") or 0), 2),
            "pending_output": round(float(row.get("pending_output") or 0), 2),
        })

    return p.function_result(
        columns=["id", "project_id", "project_name", "report_period", "output_value", 
                 "output_tax", "output_without_tax", "output_type", "output_ratio", 
                 "confirm_type", "confirmed_output", "pending_output"],
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