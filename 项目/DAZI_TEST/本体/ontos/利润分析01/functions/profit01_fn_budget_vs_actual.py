"""profit01.fn.budget_vs_actual — 预实对比"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "fiscal_year": 2025,
        "fiscal_period": 0,
        "budget_version": "2025年度预算",
    },
    "object_type_code": "BudgetAnalysis",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    fiscal_year = int(params.get("fiscal_year") or 2025)
    fiscal_period = int(params.get("fiscal_period") or 0)
    budget_version = params.get("budget_version") or "2025年度预算"
    project_id = (params.get("project_id") or "").strip()
    period_cond = "" if fiscal_period == 0 else f" AND fiscal_period = {fiscal_period}"
    proj_cond = f" AND project_id = '{project_id}'" if project_id else ""

    sql = f"""
        SELECT
            project_name, account_code, account_name, pl_category,
            sum(budget_amount) AS budget_amount,
            sum(actual_amount) AS actual_amount
        FROM fact_pl_budget
        WHERE fiscal_year = {fiscal_year}
          AND budget_version = '{budget_version}'
          {period_cond} {proj_cond}
        GROUP BY project_name, account_code, account_name, pl_category
        ORDER BY project_name, pl_category, account_code
    """
    rows = p.sql.query(sql) or []
    data = []
    for r in rows:
        budget = float(r.get("budget_amount") or 0)
        actual = float(r.get("actual_amount") or 0)
        data.append({
            "project_name": r.get("project_name", ""),
            "account_code": r.get("account_code", ""),
            "account_name": r.get("account_name", ""),
            "pl_category": r.get("pl_category", ""),
            "budget_amount": round(budget, 2),
            "actual_amount": round(actual, 2),
            "variance": round(actual - budget, 2),
            "execution_rate": round(actual / budget, 4) if budget != 0 else 0,
        })
    return p.function_result(
        columns=["project_name", "account_code", "account_name", "pl_category",
                 "budget_amount", "actual_amount", "variance", "execution_rate"],
        data=data,
        row_count=len(data),
    )


def main():
    s = space.get(ctx.space_id or "")
    _Ports = type("_Ports", (), {
        "get_params": lambda self: dict(ctx.params or {}),
        "function_result": lambda self, **kw: onto.function_result(**kw),
    })
    p = _Ports()
    p.sql = s.sql
    return _ontology_fn_body(p)
