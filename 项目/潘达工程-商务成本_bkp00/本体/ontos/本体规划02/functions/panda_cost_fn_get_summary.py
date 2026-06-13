"""商务成本总览 panda_cost.fn.get_summary

参数：report_period, company_id（可选）
返回：project_count, total_output, confirmed_output, total_cost_confirmed,
      avg_profit_rate, avg_confirmed_ratio, total_paid, total_unpaid,
      high_risk_count, avg_health_score, avg_collection_rate, report_period

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划02/functions/panda_cost_fn_get_summary.py \
    --space space__panda_construction --register-function-id panda_cost.fn.get_summary
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"report_period": "2025-06"},
    "object_type_code": "CostManagementAnalysis",
}


def _build_where(report_period, company_id=None, alias=""):
    prefix = f"{alias}." if alias else ""
    clauses = []
    if report_period:
        clauses.append(f"{prefix}report_period = '{report_period}'")
    if company_id:
        clauses.append(f"{prefix}company_id = '{company_id}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    report_period = params.get("report_period", "")
    company_id = params.get("company_id") or None
    where_o = _build_where(report_period, company_id, "o")

    sql = f"""
    SELECT
        uniq(o.project_id) AS project_count,
        sum(o.total_output) AS total_output,
        sum(o.confirmed_output) AS confirmed_output,
        sum(c.cost_confirmed_acc) AS total_cost_confirmed,
        sum(pay.paid_amount) AS total_paid,
        sum(pay.payable_confirmed - pay.paid_amount) AS total_unpaid
    FROM fact_project_output o
    LEFT JOIN fact_project_cost c
        ON o.project_id = c.project_id AND o.report_period = c.report_period
    LEFT JOIN fact_project_payment pay
        ON o.project_id = pay.project_id AND o.report_period = pay.report_period
    {where_o}
    """

    rows = p.sql.query(sql)
    row = rows[0] if rows else {}
    total_output = float(row.get("total_output") or 0)
    confirmed_output = float(row.get("confirmed_output") or 0)
    total_cost = float(row.get("total_cost_confirmed") or 0)
    avg_profit_rate = (total_output - total_cost) / total_output if total_output > 0 else 0.0
    avg_confirmed_ratio = confirmed_output / total_output if total_output > 0 else 0.0

    ind_where = _build_where(report_period, company_id, "i")
    ind_sql = f"""
    SELECT
        avgIf(indicator_value, indicator_code = 'collection_rate') AS avg_collection_rate,
        avgIf(indicator_value, indicator_code = 'health_score') AS avg_health_score
    FROM fact_project_indicator i
    {ind_where}
    """
    ind_rows = p.sql.query(ind_sql)
    ind_row = ind_rows[0] if ind_rows else {}

    risk_clauses = [f"report_period = '{report_period}'"]
    if company_id:
        risk_clauses.append(
            f"project_id IN (SELECT project_id FROM dim_project WHERE company_id = '{company_id}')"
        )
    risk_sql = f"""
    SELECT count() AS high_risk_count
    FROM fact_project_risk
    WHERE {' AND '.join(risk_clauses)}
      AND warning_level IN ('red', '高', 'yellow', '黄')
    """
    risk_rows = p.sql.query(risk_sql)
    high_risk_count = int((risk_rows[0] if risk_rows else {}).get("high_risk_count") or 0)

    data = [{
        "project_count": int(row.get("project_count") or 0),
        "total_output": round(total_output, 2),
        "confirmed_output": round(confirmed_output, 2),
        "total_cost_confirmed": round(total_cost, 2),
        "avg_profit_rate": round(avg_profit_rate, 4),
        "avg_confirmed_ratio": round(avg_confirmed_ratio, 4),
        "total_paid": round(float(row.get("total_paid") or 0), 2),
        "total_unpaid": round(float(row.get("total_unpaid") or 0), 2),
        "high_risk_count": high_risk_count,
        "avg_health_score": round(float(ind_row.get("avg_health_score") or 0), 4),
        "avg_collection_rate": round(float(ind_row.get("avg_collection_rate") or 0), 4),
        "report_period": report_period,
    }]

    return p.function_result(
        columns=[
            "project_count", "total_output", "confirmed_output", "total_cost_confirmed",
            "avg_profit_rate", "avg_confirmed_ratio", "total_paid", "total_unpaid",
            "high_risk_count", "avg_health_score", "avg_collection_rate", "report_period",
        ],
        data=data,
        row_count=1,
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
