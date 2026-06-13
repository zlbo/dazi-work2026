"""项目健康度与风险综合分 panda_cost.fn.project_health（V3）

参数：report_period, project_id
返回：profit_rate, collection_rate, confirmed_ratio, cash_balance,
      risk_score, health_score, is_healthy, report_period

V3：回款率优先 fact_receipt 聚合；cash_balance = receivedAmount - paidAmount（030 §2.2）

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划03/functions/panda_cost_v3_fn_project_health.py \
    --space space__panda_construction --register-function-id panda_cost.fn.project_health
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"report_period": "2025-06", "project_id": "P001"},
    "object_type_code": "Project",
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
    project_id = params.get("project_id", "")

    base_sql = f"""
    SELECT
        sum(o.total_output) AS total_output,
        sum(o.confirmed_output) AS confirmed_output,
        sumIf(c.cost_confirmed_acc, c.cost_level IN ('L1', '') OR isNull(c.cost_level)) AS cost_confirmed_acc,
        sum(pay.paid_amount) AS paid_amount
    FROM fact_project_output o
    LEFT JOIN fact_project_cost c
        ON o.project_id = c.project_id AND o.report_period = c.report_period
    LEFT JOIN fact_project_payment pay
        ON o.project_id = pay.project_id AND o.report_period = pay.report_period
    WHERE o.report_period = '{report_period}' AND o.project_id = '{project_id}'
    """
    base_rows = p.sql.query(base_sql)
    base = base_rows[0] if base_rows else {}
    total_output = _safe_float(base.get("total_output"))
    confirmed_output = _safe_float(base.get("confirmed_output"))
    cost_confirmed = _safe_float(base.get("cost_confirmed_acc"))
    paid_amount = _safe_float(base.get("paid_amount"))

    profit_rate = (total_output - cost_confirmed) / total_output if total_output > 0 else 0.0
    confirmed_ratio = confirmed_output / total_output if total_output > 0 else 0.0

    receipt_sql = f"""
    SELECT sum(receipt_amount) AS received_amount
    FROM fact_receipt
    WHERE project_id = '{project_id}'
      AND formatDateTime(receipt_date, '%Y-%m') = '{report_period}'
    """
    receipt_rows = p.sql.query(receipt_sql)
    received_amount = _safe_float((receipt_rows[0] if receipt_rows else {}).get("received_amount"))

    collection_rate = 0.0
    if confirmed_output > 0 and received_amount > 0:
        collection_rate = received_amount / confirmed_output
    else:
        ind_sql = f"""
        SELECT avgIf(indicator_value, indicator_code = 'collection_rate') AS collection_rate
        FROM fact_project_indicator
        WHERE report_period = '{report_period}' AND project_id = '{project_id}'
        """
        ind_rows = p.sql.query(ind_sql)
        collection_rate = _safe_float((ind_rows[0] if ind_rows else {}).get("collection_rate"))

    health_sql = f"""
    SELECT avgIf(indicator_value, indicator_code = 'health_score') AS health_score
    FROM fact_project_indicator
    WHERE report_period = '{report_period}' AND project_id = '{project_id}'
    """
    health_rows = p.sql.query(health_sql)
    health_score = _safe_float((health_rows[0] if health_rows else {}).get("health_score"))

    if health_score == 0 and (profit_rate or collection_rate or confirmed_ratio):
        health_score = (profit_rate / 0.20 + collection_rate + confirmed_ratio) / 3.0

    cash_balance = received_amount - paid_amount if received_amount else confirmed_output - paid_amount

    risk_sql = f"""
    SELECT sum(risk_value) AS risk_score
    FROM fact_project_risk
    WHERE report_period = '{report_period}' AND project_id = '{project_id}'
    """
    risk_rows = p.sql.query(risk_sql)
    risk_score = int((risk_rows[0] if risk_rows else {}).get("risk_score") or 0)

    health_threshold = 0.60 if health_score <= 1 else 60
    is_healthy = 1 if health_score >= health_threshold and risk_score < 50 else 0

    data = [{
        "profit_rate": _safe_round(profit_rate, 4),
        "collection_rate": _safe_round(collection_rate, 4),
        "confirmed_ratio": _safe_round(confirmed_ratio, 4),
        "cash_balance": _safe_round(cash_balance, 2),
        "risk_score": risk_score,
        "health_score": _safe_round(health_score, 4),
        "is_healthy": is_healthy,
        "report_period": report_period,
    }]

    return p.function_result(
        columns=["profit_rate", "collection_rate", "confirmed_ratio", "cash_balance",
                 "risk_score", "health_score", "is_healthy", "report_period"],
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
