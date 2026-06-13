"""毛利率 / 成本率分析 panda_cost.fn.profit_analysis

参数：report_period, project_id（可选）, group_by=project|company|region|owner|department
返回：group_id, group_name, total_output, total_cost, profit_rate, cost_ratio, confirmed_ratio

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划02/functions/panda_cost_fn_profit_analysis.py \
    --space space__panda_construction --register-function-id panda_cost.fn.profit_analysis
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"report_period": "2025-06", "group_by": "project"},
    "object_type_code": "CostManagementAnalysis",
}

_GROUP_FIELDS = {
    "project": ("dp.project_id", "dp.project_name"),
    "company": ("dp.company_id", "dp.company_name"),
    "region": ("dp.region_id", "dp.region_name"),
    "owner": ("dp.owner_id", "dp.owner_name"),
    "department": ("dp.department_id", "dp.department_name"),
}


def _build_where(report_period, project_id=None):
    clauses = []
    if report_period:
        clauses.append(f"o.report_period = '{report_period}'")
    if project_id:
        clauses.append(f"o.project_id = '{project_id}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    report_period = params.get("report_period", "")
    project_id = params.get("project_id") or None
    group_by = params.get("group_by", "project")
    group_id_col, group_name_col = _GROUP_FIELDS.get(group_by, _GROUP_FIELDS["project"])
    where_clause = _build_where(report_period, project_id)

    sql = f"""
    SELECT
        {group_id_col} AS group_id,
        any({group_name_col}) AS group_name,
        sum(o.total_output) AS total_output,
        sum(c.cost_confirmed_acc) AS total_cost,
        sum(o.confirmed_output) AS confirmed_output
    FROM fact_project_output o
    JOIN dim_project dp ON o.project_id = dp.project_id
    LEFT JOIN fact_project_cost c
        ON o.project_id = c.project_id AND o.report_period = c.report_period
    {where_clause}
    GROUP BY group_id
    ORDER BY total_output DESC
    """

    rows = p.sql.query(sql)
    data = []
    for row in rows:
        total_output = float(row.get("total_output") or 0)
        total_cost = float(row.get("total_cost") or 0)
        confirmed_output = float(row.get("confirmed_output") or 0)
        profit_rate = (total_output - total_cost) / total_output if total_output > 0 else 0.0
        cost_ratio = total_cost / total_output if total_output > 0 else 0.0
        confirmed_ratio = confirmed_output / total_output if total_output > 0 else 0.0
        data.append({
            "group_id": str(row.get("group_id") or ""),
            "group_name": str(row.get("group_name") or ""),
            "total_output": round(total_output, 2),
            "total_cost": round(total_cost, 2),
            "profit_rate": round(profit_rate, 4),
            "cost_ratio": round(cost_ratio, 4),
            "confirmed_ratio": round(confirmed_ratio, 4),
        })

    return p.function_result(
        columns=["group_id", "group_name", "total_output", "total_cost",
                 "profit_rate", "cost_ratio", "confirmed_ratio"],
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
