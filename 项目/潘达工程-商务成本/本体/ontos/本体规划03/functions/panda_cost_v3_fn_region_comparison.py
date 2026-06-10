"""分公司对标（原地区对标） panda_cost.fn.region_comparison（V3）

参数：report_period, metric, company_id（可选，筛选指定分公司）
返回：rank, company_id, company_name, metric, metric_value, report_period

V3：保留 function id region_comparison，按 dim_company 分组对标（无 dim_region）

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划03/functions/panda_cost_v3_fn_region_comparison.py \
    --space space__panda_construction --register-function-id panda_cost.fn.region_comparison
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

def _calc_metric(row, metric):
    total_output = _safe_float(row.get("total_output"))
    confirmed_output = _safe_float(row.get("confirmed_output"))
    cost_confirmed = _safe_float(row.get("cost_confirmed_acc"))
    target_cost = _safe_float(row.get("target_cost"))
    paid_amount = _safe_float(row.get("paid_amount"))
    payable_confirmed = _safe_float(row.get("payable_confirmed"))
    received_amount = _safe_float(row.get("received_amount"))
    if metric == "output_total":
        return _safe_round(total_output, 2)
    if metric == "cost_confirmed_acc":
        return _safe_round(cost_confirmed, 2)
    if metric == "profit_rate":
        val = (total_output - cost_confirmed) / total_output if total_output > 0 else 0.0
        return _safe_round(val, 4)
    if metric == "confirmed_ratio":
        val = confirmed_output / total_output if total_output > 0 else 0.0
        return _safe_round(val, 4)
    if metric == "payment_rate":
        val = paid_amount / payable_confirmed if payable_confirmed > 0 else 0.0
        return _safe_round(val, 4)
    if metric == "collection_rate":
        val = received_amount / confirmed_output if confirmed_output > 0 else 0.0
        return _safe_round(val, 4)
    if metric == "cost_variance_ratio":
        val = (cost_confirmed - target_cost) / target_cost if target_cost > 0 else 0.0
        return _safe_round(val, 4)
    return 0.0


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    report_period = params.get("report_period", "")
    metric = params.get("metric", "profit_rate")
    company_id = params.get("company_id") or None

    company_filter = f"AND dc.company_id = '{company_id}'" if company_id else ""

    sql = f"""
    SELECT
        dc.company_id,
        any(dc.company_name) AS company_name,
        sum(o.total_output) AS total_output,
        sum(o.confirmed_output) AS confirmed_output,
        sumIf(c.cost_confirmed_acc, c.cost_level IN ('L1', '') OR isNull(c.cost_level)) AS cost_confirmed_acc,
        sum(c.target_cost) AS target_cost,
        sum(pay.paid_amount) AS paid_amount,
        sum(pay.payable_confirmed) AS payable_confirmed,
        sum(r.receipt_amount) AS received_amount
    FROM fact_project_output o
    JOIN dim_project dp ON o.project_id = dp.project_id
    JOIN dim_company dc ON dp.company_id = dc.company_id
    LEFT JOIN fact_project_cost c
        ON o.project_id = c.project_id AND o.report_period = c.report_period
    LEFT JOIN fact_project_payment pay
        ON o.project_id = pay.project_id AND o.report_period = pay.report_period
    LEFT JOIN (
        SELECT project_id, sum(receipt_amount) AS receipt_amount
        FROM fact_receipt
        WHERE formatDateTime(receipt_date, '%Y-%m') = '{report_period}'
        GROUP BY project_id
    ) r ON o.project_id = r.project_id
    WHERE o.report_period = '{report_period}' {company_filter}
    GROUP BY dc.company_id
    """

    rows = p.sql.query(sql)
    scored = []
    for row in rows:
        scored.append({
            "company_id": str(row.get("company_id") or ""),
            "company_name": str(row.get("company_name") or ""),
            "metric_value": _calc_metric(row, metric),
        })

    scored.sort(key=lambda x: x["metric_value"], reverse=True)
    data = []
    for rank, item in enumerate(scored, start=1):
        data.append({
            "rank": rank,
            "company_id": item["company_id"],
            "company_name": item["company_name"],
            "metric": metric,
            "metric_value": item["metric_value"],
            "report_period": report_period,
        })

    return p.function_result(
        columns=["rank", "company_id", "company_name", "metric", "metric_value", "report_period"],
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
