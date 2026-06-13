"""收支科目结构 panda_cost.fn.balance_breakdown（V3）

参数：report_period, project_id（可选）
返回：subject_code, subject_name, project_amount, company_amount, total_amount,
      amount_ratio, report_period

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划03/functions/panda_cost_v3_fn_balance_breakdown.py \
    --space space__panda_construction --register-function-id panda_cost.fn.balance_breakdown
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
        clauses.append(f"b.report_period = '{report_period}'")
    if project_id:
        clauses.append(f"b.project_id = '{project_id}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    report_period = params.get("report_period", "")
    project_id = params.get("project_id") or None
    where_clause = _build_where(report_period, project_id)

    sql = f"""
    SELECT
        b.subject_code,
        any(b.subject_name) AS subject_name,
        sum(b.project_amount) AS project_amount,
        sum(b.company_amount) AS company_amount,
        sum(b.total_amount) AS total_amount
    FROM fact_project_balance b
    {where_clause}
    GROUP BY b.subject_code
    ORDER BY total_amount DESC
    """

    rows = p.sql.query(sql)
    grand_total = sum(_safe_float(r.get("total_amount")) for r in rows)
    data = []
    for row in rows:
        total_amount = _safe_float(row.get("total_amount"))
        amount_ratio = total_amount / grand_total if grand_total > 0 else 0.0
        data.append({
            "subject_code": str(row.get("subject_code") or ""),
            "subject_name": str(row.get("subject_name") or ""),
            "project_amount": _safe_round(row.get("project_amount"), 2),
            "company_amount": _safe_round(row.get("company_amount"), 2),
            "total_amount": _safe_round(total_amount, 2),
            "amount_ratio": _safe_round(amount_ratio, 4),
            "report_period": report_period,
        })

    return p.function_result(
        columns=["subject_code", "subject_name", "project_amount", "company_amount",
                 "total_amount", "amount_ratio", "report_period"],
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
