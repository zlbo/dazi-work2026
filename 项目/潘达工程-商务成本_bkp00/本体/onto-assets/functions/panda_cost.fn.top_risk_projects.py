# 本体函数脚本（从服务端拉取）
# function_id: panda_cost.fn.top_risk_projects
# script_id: e8248e7f-245f-41cc-af00-f390d672b925
# space_id: space__panda_construction

"""高风险项目 Top N panda_cost.fn.top_risk_projects（V3）

参数：report_period, limit
返回：rank, project_id, project_name, risk_score, high_risk_count, warning_level, report_period

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划03/functions/panda_cost_v3_fn_top_risk_projects.py \
    --space space__panda_construction --register-function-id panda_cost.fn.top_risk_projects
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"report_period": "2025-06", "limit": 10},
    "object_type_code": "ProjectRisk",
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

def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    report_period = params.get("report_period", "")
    limit = int(params.get("limit") or 10)

    sql = f"""
    SELECT
        r.project_id,
        any(dp.project_name) AS project_name,
        sum(r.risk_value) AS risk_score,
        countIf(r.warning_level IN ('red', '高', '红')) AS high_risk_count,
        max(r.warning_level) AS warning_level
    FROM fact_project_risk r
    JOIN dim_project dp ON r.project_id = dp.project_id
    WHERE r.report_period = '{report_period}'
    GROUP BY r.project_id
    ORDER BY risk_score DESC, high_risk_count DESC
    LIMIT {limit}
    """

    rows = p.sql.query(sql)
    data = []
    for rank, row in enumerate(rows, start=1):
        data.append({
            "rank": rank,
            "project_id": str(row.get("project_id") or ""),
            "project_name": str(row.get("project_name") or ""),
            "risk_score": int(row.get("risk_score") or 0),
            "high_risk_count": int(row.get("high_risk_count") or 0),
            "warning_level": str(row.get("warning_level") or ""),
            "report_period": report_period,
        })

    return p.function_result(
        columns=["rank", "project_id", "project_name", "risk_score",
                 "high_risk_count", "warning_level", "report_period"],
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
