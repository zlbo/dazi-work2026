"""分公司对标 panda_cost.fn.company_comparison

参数：report_period, metric
返回：rank, company_id, company_name, metric, metric_value, report_period

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划02/functions/panda_cost_fn_company_comparison.py \
    --space space__panda_construction --register-function-id panda_cost.fn.company_comparison
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"report_period": "2025-06", "metric": "profit_rate"},
    "object_type_code": "CostManagementAnalysis",
}


def _calc_metric(row, metric):
    total_output = float(row.get("total_output") or 0)
    confirmed_output = float(row.get("confirmed_output") or 0)
    cost_confirmed = float(row.get("cost_confirmed_acc") or 0)
    target_cost = float(row.get("target_cost") or 0)
    paid_amount = float(row.get("paid_amount") or 0)
    payable_confirmed = float(row.get("payable_confirmed") or 0)
    if metric == "output_total":
        return round(total_output, 2)
    if metric == "cost_confirmed_acc":
        return round(cost_confirmed, 2)
    if metric == "profit_rate":
        val = (total_output - cost_confirmed) / total_output if total_output > 0 else 0.0
        return round(val, 4)
    if metric == "confirmed_ratio":
        val = confirmed_output / total_output if total_output > 0 else 0.0
        return round(val, 4)
    if metric == "payment_rate":
        val = paid_amount / payable_confirmed if payable_confirmed > 0 else 0.0
        return round(val, 4)
    if metric == "cost_variance_ratio":
        val = (cost_confirmed - target_cost) / target_cost if target_cost > 0 else 0.0
        return round(val, 4)
    return 0.0


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    report_period = params.get("report_period", "")
    metric = params.get("metric", "profit_rate")

    sql = f"""
    SELECT
        dp.company_id,
        any(dp.company_name) AS company_name,
        sum(o.total_output) AS total_output,
        sum(o.confirmed_output) AS confirmed_output,
        sum(c.cost_confirmed_acc) AS cost_confirmed_acc,
        sum(c.target_cost) AS target_cost,
        sum(pay.paid_amount) AS paid_amount,
        sum(pay.payable_confirmed) AS payable_confirmed
    FROM fact_project_output o
    JOIN dim_project dp ON o.project_id = dp.project_id
    LEFT JOIN fact_project_cost c
        ON o.project_id = c.project_id AND o.report_period = c.report_period
    LEFT JOIN fact_project_payment pay
        ON o.project_id = pay.project_id AND o.report_period = pay.report_period
    WHERE o.report_period = '{report_period}'
    GROUP BY dp.company_id
    """

    rows = p.sql.query(sql)
    if metric in ("collection_rate", "health_score"):
        ind_sql = f"""
        SELECT company_id, avg(indicator_value) AS metric_value
        FROM fact_project_indicator
        WHERE report_period = '{report_period}' AND indicator_code = '{metric}'
        GROUP BY company_id
        """
        ind_rows = p.sql.query(ind_sql)
        scored = [{
            "company_id": str(r.get("company_id") or ""),
            "company_name": "",
            "metric_value": round(float(r.get("metric_value") or 0), 4),
        } for r in ind_rows]
    else:
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
