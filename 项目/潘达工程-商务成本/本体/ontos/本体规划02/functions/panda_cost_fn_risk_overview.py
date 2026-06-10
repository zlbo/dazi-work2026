"""风险预警总览 panda_cost.fn.risk_overview

参数：report_period, warning_level（可选）
返回：risk_type, risk_count, high_risk_count, avg_risk_value, warning_level, report_period

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划02/functions/panda_cost_fn_risk_overview.py \
    --space space__panda_construction --register-function-id panda_cost.fn.risk_overview
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"report_period": "2025-06"},
    "object_type_code": "ProjectRisk",
}


def _build_where(report_period, warning_level=None):
    clauses = []
    if report_period:
        clauses.append(f"report_period = '{report_period}'")
    if warning_level:
        clauses.append(f"warning_level = '{warning_level}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    report_period = params.get("report_period", "")
    warning_level = params.get("warning_level") or None
    where_clause = _build_where(report_period, warning_level)

    sql = f"""
    SELECT
        risk_type,
        count() AS risk_count,
        countIf(warning_level IN ('red', '高')) AS high_risk_count,
        avg(risk_value) AS avg_risk_value,
        any(warning_level) AS warning_level
    FROM fact_project_risk
    {where_clause}
    GROUP BY risk_type
    ORDER BY high_risk_count DESC, risk_count DESC
    """

    rows = p.sql.query(sql)
    data = []
    for row in rows:
        data.append({
            "risk_type": str(row.get("risk_type") or ""),
            "risk_count": int(row.get("risk_count") or 0),
            "high_risk_count": int(row.get("high_risk_count") or 0),
            "avg_risk_value": round(float(row.get("avg_risk_value") or 0), 2),
            "warning_level": str(row.get("warning_level") or ""),
            "report_period": report_period,
        })

    return p.function_result(
        columns=["risk_type", "risk_count", "high_risk_count",
                 "avg_risk_value", "warning_level", "report_period"],
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
