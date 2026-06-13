"""profit01.fn.account_breakdown — 损益科目结构"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31", "account_level": 2},
    "object_type_code": "Account",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", "2025-12-31")
    account_level = int(params.get("account_level") or 0)
    pl_category = (params.get("pl_category") or "").strip()
    lo = int(start_date.replace("-", "")[:8])
    hi = int(end_date.replace("-", "")[:8])
    level_cond = f" AND a.account_level = {account_level}" if account_level else ""
    cat_cond = f" AND a.pl_category = '{pl_category}'" if pl_category else ""

    sql = f"""
        SELECT
            a.account_code, a.account_name, a.account_level, a.pl_category, a.account_type,
            coalesce(sum(c.cost_amount), 0) AS cost_amount,
            coalesce(sum(b.budget_amount), 0) AS budget_amount
        FROM dim_account a
        LEFT JOIN bridge_cost_type_account br ON a.account_id = br.account_id
        LEFT JOIN fact_cost c ON c.cost_type_id = br.cost_type_id
            AND c.date_key >= {lo} AND c.date_key <= {hi}
        LEFT JOIN fact_pl_budget b ON b.account_id = a.account_id AND b.fiscal_year = 2025
        WHERE a.is_leaf = 1 {level_cond} {cat_cond}
        GROUP BY a.account_code, a.account_name, a.account_level, a.pl_category, a.account_type
        ORDER BY a.pl_category, a.account_code
    """
    rows = p.sql.query(sql) or []
    total_cost = sum(float(r.get("cost_amount") or 0) for r in rows)
    data = []
    for r in rows:
        cost_amt = float(r.get("cost_amount") or 0)
        data.append({
            "account_code": r.get("account_code", ""),
            "account_name": r.get("account_name", ""),
            "account_level": int(r.get("account_level") or 0),
            "pl_category": r.get("pl_category", ""),
            "account_type": r.get("account_type", ""),
            "cost_amount": round(cost_amt, 2),
            "budget_amount": round(float(r.get("budget_amount") or 0), 2),
            "share_pct": round(cost_amt / total_cost, 4) if total_cost > 0 else 0,
        })
    return p.function_result(
        columns=["account_code", "account_name", "account_level", "pl_category", "account_type",
                 "cost_amount", "budget_amount", "share_pct"],
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
