# 本体函数脚本（从服务端拉取）
# function_id: panda_cost.fn.output_analysis
# script_id: 073c020f-7164-4fa6-8731-b71a04d06a3c
# space_id: space__panda_construction

"""产值确权结构 panda_cost.fn.output_analysis（V3）

参数：report_period, project_id（可选）
返回：project_id, project_name, total_output, confirmed_output, unconfirmed_output,
      confirmed_ratio, unconfirmed_ratio, report_period

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划03/functions/panda_cost_v3_fn_output_analysis.py \
    --space space__panda_construction --register-function-id panda_cost.fn.output_analysis
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"report_period": "2025-06"},
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
    where_clause = _build_where(report_period, project_id)

    sql = f"""
    SELECT
        o.project_id,
        any(dp.project_name) AS project_name,
        sum(o.total_output) AS total_output,
        sum(o.confirmed_output) AS confirmed_output,
        sum(o.unconfirmed_output) AS unconfirmed_output
    FROM fact_project_output o
    JOIN dim_project dp ON o.project_id = dp.project_id
    {where_clause}
    GROUP BY o.project_id
    ORDER BY total_output DESC
    """

    rows = p.sql.query(sql)
    data = []
    for row in rows:
        total_output = _safe_float(row.get("total_output"))
        confirmed_output = _safe_float(row.get("confirmed_output"))
        unconfirmed_output = _safe_float(row.get("unconfirmed_output"))
        confirmed_ratio = confirmed_output / total_output if total_output > 0 else 0.0
        unconfirmed_ratio = unconfirmed_output / total_output if total_output > 0 else 0.0
        data.append({
            "project_id": str(row.get("project_id") or ""),
            "project_name": str(row.get("project_name") or ""),
            "total_output": _safe_round(total_output, 2),
            "confirmed_output": _safe_round(confirmed_output, 2),
            "unconfirmed_output": _safe_round(unconfirmed_output, 2),
            "confirmed_ratio": _safe_round(confirmed_ratio, 4),
            "unconfirmed_ratio": _safe_round(unconfirmed_ratio, 4),
            "report_period": report_period,
        })

    return p.function_result(
        columns=["project_id", "project_name", "total_output", "confirmed_output",
                 "unconfirmed_output", "confirmed_ratio", "unconfirmed_ratio", "report_period"],
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
