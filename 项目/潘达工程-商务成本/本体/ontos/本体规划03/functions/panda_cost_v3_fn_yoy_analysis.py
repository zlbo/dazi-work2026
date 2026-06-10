"""同比分析 panda_cost.fn.yoy_analysis（V3）

参数：report_period, metric, project_id（可选）
metric 枚举：output_total | cost_confirmed_acc | profit_rate | confirmed_ratio |
             payment_rate | collection_rate | health_score | output_growth | cost_variance_ratio
返回：current_value, previous_year_value, growth_rate, growth_amount, metric, report_period

V3：collection_rate 优先 fact_receipt 聚合

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划03/functions/panda_cost_v3_fn_yoy_analysis.py \
    --space space__panda_construction --register-function-id panda_cost.fn.yoy_analysis
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"report_period": "2025-06", "metric": "profit_rate"},
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

def _prev_year_period(report_period):
    year, month = report_period.split("-")
    return f"{int(year) - 1}-{month}"


def _build_project_filter(project_id, alias="o"):
    return f"AND {alias}.project_id = '{project_id}'" if project_id else ""


def _query_collection_rate(p, report_period, project_id=None):
    pf = f"AND o.project_id = '{project_id}'" if project_id else ""
    sql = f"""
    SELECT
        sum(r.receipt_amount) AS received_amount,
        sum(o.confirmed_output) AS confirmed_output
    FROM fact_project_output o
    LEFT JOIN fact_receipt r
        ON o.project_id = r.project_id
        AND formatDateTime(r.receipt_date, '%Y-%m') = '{report_period}'
    WHERE o.report_period = '{report_period}' {pf}
    """
    rows = p.sql.query(sql)
    row = rows[0] if rows else {}
    confirmed = _safe_float(row.get("confirmed_output"))
    received = _safe_float(row.get("received_amount"))
    if confirmed > 0 and received > 0:
        return received / confirmed
    ind_pf = f"AND i.project_id = '{project_id}'" if project_id else ""
    ind_sql = f"""
    SELECT avg(indicator_value) AS val FROM fact_project_indicator i
    WHERE report_period = '{report_period}' AND indicator_code = 'collection_rate' {ind_pf}
    """
    ind_rows = p.sql.query(ind_sql)
    return _safe_float((ind_rows[0] if ind_rows else {}).get("val"))


def _query_metric(p, report_period, metric, project_id=None):
    pf = _build_project_filter(project_id)
    if metric == "output_total":
        sql = f"""
        SELECT sum(total_output) AS val FROM fact_project_output o
        WHERE report_period = '{report_period}' {pf}
        """
    elif metric == "cost_confirmed_acc":
        sql = f"""
        SELECT sumIf(cost_confirmed_acc, cost_level IN ('L1', '') OR isNull(cost_level)) AS val
        FROM fact_project_cost c
        WHERE report_period = '{report_period}'
        {f"AND c.project_id = '{project_id}'" if project_id else ""}
        """
    elif metric == "collection_rate":
        return _query_collection_rate(p, report_period, project_id)
    elif metric == "health_score":
        sql = f"""
        SELECT avg(indicator_value) AS val FROM fact_project_indicator i
        WHERE report_period = '{report_period}' AND indicator_code = 'health_score'
        {f"AND i.project_id = '{project_id}'" if project_id else ""}
        """
    else:
        sql = f"""
        SELECT
            sum(o.total_output) AS total_output,
            sum(o.confirmed_output) AS confirmed_output,
            sumIf(c.cost_confirmed_acc, c.cost_level IN ('L1', '') OR isNull(c.cost_level)) AS cost_confirmed_acc,
            sum(c.target_cost) AS target_cost,
            sum(pay.paid_amount) AS paid_amount,
            sum(pay.payable_confirmed) AS payable_confirmed
        FROM fact_project_output o
        LEFT JOIN fact_project_cost c
            ON o.project_id = c.project_id AND o.report_period = c.report_period
        LEFT JOIN fact_project_payment pay
            ON o.project_id = pay.project_id AND o.report_period = pay.report_period
        WHERE o.report_period = '{report_period}' {pf}
        """
    rows = p.sql.query(sql)
    row = rows[0] if rows else {}
    if metric in ("output_total", "cost_confirmed_acc", "health_score"):
        return _safe_float(row.get("val"))
    total_output = _safe_float(row.get("total_output"))
    confirmed_output = _safe_float(row.get("confirmed_output"))
    cost_confirmed = _safe_float(row.get("cost_confirmed_acc"))
    target_cost = _safe_float(row.get("target_cost"))
    paid_amount = _safe_float(row.get("paid_amount"))
    payable_confirmed = _safe_float(row.get("payable_confirmed"))
    if metric == "profit_rate":
        return (total_output - cost_confirmed) / total_output if total_output > 0 else 0.0
    if metric == "confirmed_ratio":
        return confirmed_output / total_output if total_output > 0 else 0.0
    if metric == "payment_rate":
        return paid_amount / payable_confirmed if payable_confirmed > 0 else 0.0
    if metric == "cost_variance_ratio":
        return (cost_confirmed - target_cost) / target_cost if target_cost > 0 else 0.0
    if metric == "output_growth":
        return total_output
    return 0.0


def _calc_growth(current, previous):
    growth_amount = current - previous
    if previous == 0:
        growth_rate = 0.0
    else:
        growth_rate = round(growth_amount / previous, 4)
    return growth_amount, growth_rate


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    report_period = params.get("report_period", "")
    metric = params.get("metric", "profit_rate")
    project_id = params.get("project_id") or None

    prev_period = _prev_year_period(report_period)
    current_value = _query_metric(p, report_period, metric, project_id)
    previous_value = _query_metric(p, prev_period, metric, project_id)

    if metric == "output_growth":
        growth_amount, growth_rate = _calc_growth(current_value, previous_value)
        current_value = _safe_float(growth_rate)
        previous_value = 0.0
    else:
        growth_amount, growth_rate = _calc_growth(current_value, previous_value)

    data = [{
        "current_value": _safe_round(current_value, 4),
        "previous_year_value": _safe_round(previous_value, 4),
        "growth_rate": _safe_float(growth_rate),
        "growth_amount": _safe_round(growth_amount, 4),
        "metric": metric,
        "report_period": report_period,
    }]

    return p.function_result(
        columns=["current_value", "previous_year_value", "growth_rate",
                 "growth_amount", "metric", "report_period"],
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
