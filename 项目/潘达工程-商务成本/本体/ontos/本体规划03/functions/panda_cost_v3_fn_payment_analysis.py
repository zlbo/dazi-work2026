"""付款与未付款分析 panda_cost.fn.payment_analysis（V3）

参数：report_period, project_id（可选）
返回：project_id, project_name, payable_confirmed, payable_unconfirmed, paid_amount,
      unpaid_amount, payment_rate, labor_payable, report_period

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划03/functions/panda_cost_v3_fn_payment_analysis.py \
    --space space__panda_construction --register-function-id panda_cost.fn.payment_analysis
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
        clauses.append(f"pay.report_period = '{report_period}'")
    if project_id:
        clauses.append(f"pay.project_id = '{project_id}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    report_period = params.get("report_period", "")
    project_id = params.get("project_id") or None
    where_clause = _build_where(report_period, project_id)

    sql = f"""
    SELECT
        pay.project_id,
        any(dp.project_name) AS project_name,
        sum(pay.payable_confirmed) AS payable_confirmed,
        sum(pay.payable_unconfirmed) AS payable_unconfirmed,
        sum(pay.paid_amount) AS paid_amount,
        sum(pay.labor_payable) AS labor_payable
    FROM fact_project_payment pay
    JOIN dim_project dp ON pay.project_id = dp.project_id
    {where_clause}
    GROUP BY pay.project_id
    ORDER BY payable_confirmed DESC
    """

    rows = p.sql.query(sql)
    data = []
    for row in rows:
        payable_confirmed = _safe_float(row.get("payable_confirmed"))
        paid_amount = _safe_float(row.get("paid_amount"))
        unpaid_amount = payable_confirmed - paid_amount
        payment_rate = paid_amount / payable_confirmed if payable_confirmed > 0 else 0.0
        data.append({
            "project_id": str(row.get("project_id") or ""),
            "project_name": str(row.get("project_name") or ""),
            "payable_confirmed": _safe_round(payable_confirmed, 2),
            "payable_unconfirmed": _safe_round(row.get("payable_unconfirmed"), 2),
            "paid_amount": _safe_round(paid_amount, 2),
            "unpaid_amount": _safe_round(unpaid_amount, 2),
            "payment_rate": _safe_round(payment_rate, 4),
            "labor_payable": _safe_round(row.get("labor_payable"), 2),
            "report_period": report_period,
        })

    return p.function_result(
        columns=["project_id", "project_name", "payable_confirmed", "payable_unconfirmed",
                 "paid_amount", "unpaid_amount", "payment_rate", "labor_payable", "report_period"],
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
