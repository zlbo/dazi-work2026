# 本体函数脚本（从服务端拉取）
# function_id: panda_cost.fn.profit_analysis
# script_id: 314c8353-3541-4ac5-bbe5-5837b8a508b7
# space_id: space__panda_construction

"""毛利率 / 成本率分析 panda_cost.fn.profit_analysis（V3）

参数：report_period, project_id（可选）, group_by=project|company|employer
返回：group_id, group_name, total_output, total_cost, profit_rate, cost_ratio, confirmed_ratio

V3：group_by 支持 project/company/employer（无 region/owner/department）

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划03/functions/panda_cost_v3_fn_profit_analysis.py \
    --space space__panda_construction --register-function-id panda_cost.fn.profit_analysis
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"report_period": "2025-06", "group_by": "project"},
    "object_type_code": "CostManagementAnalysis",
}



import math


def _safe_float(v, default=0.0):
    try:
        x = float(v if v is not None else default)
        return x if math.isfinite(x) else default
    except (TypeError, ValueError):
        return default


def _safe_round(v, ndigits=4, default=0.0):
    return round(_safe_float(v, default), ndigits)
_GROUP_JOINS = {
    "project": ("", "dp.project_id", "dp.project_name"),
    "company": (
        "LEFT JOIN dim_company dc ON dp.company_id = dc.company_id",
        "dp.company_id",
        "dc.company_name",
    ),
    "employer": (
        "LEFT JOIN dim_employer de ON dp.employer_id = de.employer_id",
        "dp.employer_id",
        "de.employer_name",
    ),
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
    join_sql, group_id_col, group_name_col = _GROUP_JOINS.get(
        group_by, _GROUP_JOINS["project"]
    )
    where_clause = _build_where(report_period, project_id)

    sql = f"""
    SELECT
        {group_id_col} AS group_id,
        any({group_name_col}) AS group_name,
        sum(o.total_output) AS total_output,
        sumIf(c.cost_confirmed_acc, c.cost_level IN ('L1', '') OR isNull(c.cost_level)) AS total_cost,
        sum(o.confirmed_output) AS confirmed_output
    FROM fact_project_output o
    JOIN dim_project dp ON o.project_id = dp.project_id
    {join_sql}
    LEFT JOIN fact_project_cost c
        ON o.project_id = c.project_id AND o.report_period = c.report_period
    {where_clause}
    GROUP BY group_id
    ORDER BY total_output DESC
    """

    rows = p.sql.query(sql)
    data = []
    for row in rows:
        total_output = _safe_float(row.get("total_output"))
        total_cost = _safe_float(row.get("total_cost"))
        confirmed_output = _safe_float(row.get("confirmed_output"))
        profit_rate = (total_output - total_cost) / total_output if total_output > 0 else 0.0
        cost_ratio = total_cost / total_output if total_output > 0 else 0.0
        confirmed_ratio = confirmed_output / total_output if total_output > 0 else 0.0
        data.append({
            "group_id": str(row.get("group_id") or ""),
            "group_name": str(row.get("group_name") or ""),
            "total_output": _safe_round(total_output, 2),
            "total_cost": _safe_round(total_cost, 2),
            "profit_rate": _safe_round(profit_rate, 4),
            "cost_ratio": _safe_round(cost_ratio, 4),
            "confirmed_ratio": _safe_round(confirmed_ratio, 4),
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
