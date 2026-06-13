"""商务成本 - 项目成本明细查询 cost.fn.cost_detail

参数：start_date, end_date, project_id（可选）, cost_type（可选）
返回：id, project_id, project_name, report_period, cost_amount, cost_type, labor_cost, material_cost, mechanical_cost, other_cost

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/商务成本/functions/cost_fn_cost_detail.py \
    --space space__panda_construction --register-function-id cost.fn.cost_detail
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31"},
    "object_type_code": "ProjectCost",
}


def _build_where(start_date, end_date, project_id=None, cost_type=None):
    clauses = []
    if start_date and end_date:
        clauses.append(f"report_period >= '{start_date[:7]}' AND report_period <= '{end_date[:7]}'")
    if project_id:
        clauses.append(f"c.project_id = '{project_id}'")
    if cost_type:
        clauses.append(f"cost_type = '{cost_type}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    project_id = params.get("project_id") or None
    cost_type = params.get("cost_type") or None
    where_clause = _build_where(start_date, end_date, project_id, cost_type)

    sql = f"""
    SELECT 
        c.id,
        c.project_id,
        p.project_name,
        c.report_period,
        c.cost_amount,
        c.cost_type,
        c.labor_cost,
        c.material_cost,
        c.mechanical_cost,
        c.other_cost,
        c.target_cost,
        c.variance_amount,
        c.variance_ratio
    FROM fact_project_cost c
    JOIN dim_project p ON c.project_id = p.project_id
    {where_clause}
    ORDER BY c.report_period DESC, c.project_id
    """

    rows = p.sql.query(sql)
    data = []
    for row in rows:
        data.append({
            "id": row.get("id", ""),
            "project_id": row.get("project_id", ""),
            "project_name": row.get("project_name", ""),
            "report_period": row.get("report_period", ""),
            "cost_amount": round(float(row.get("cost_amount") or 0), 2),
            "cost_type": row.get("cost_type", ""),
            "labor_cost": round(float(row.get("labor_cost") or 0), 2),
            "material_cost": round(float(row.get("material_cost") or 0), 2),
            "mechanical_cost": round(float(row.get("mechanical_cost") or 0), 2),
            "other_cost": round(float(row.get("other_cost") or 0), 2),
            "target_cost": round(float(row.get("target_cost") or 0), 2),
            "variance_amount": round(float(row.get("variance_amount") or 0), 2),
            "variance_ratio": round(float(row.get("variance_ratio") or 0), 4),
        })

    return p.function_result(
        columns=["id", "project_id", "project_name", "report_period", "cost_amount", "cost_type", 
                 "labor_cost", "material_cost", "mechanical_cost", "other_cost", 
                 "target_cost", "variance_amount", "variance_ratio"],
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