"""预算执行分析函数

功能：按科目/成本中心对比预算与实际，输出差异与执行率
参数：fiscal_year, fiscal_period（可选，0=全年）, budget_version, cost_center_id（可选）, plant_id（可选）

放置：项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_budget_vs_actual.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_budget_vs_actual.py --space space_cate_test01 --register-function-id profit.fn.budget_vs_actual --register-platform-category 预实分析
"""

from datetime import datetime

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"fiscal_year": 2026, "fiscal_period": 6, "budget_version": "2026年度预算", "cost_center_id": None, "plant_id": None},
    "object_type_code": "BudgetAnalysis",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    fiscal_year = int(params.get("fiscal_year", datetime.now().year))
    fiscal_period = int(params.get("fiscal_period", 0))
    budget_version = params.get("budget_version", "2026年度预算")
    cost_center_id = params.get("cost_center_id", None)
    plant_id = params.get("plant_id", None)

    output.print(f"预算年度: {fiscal_year}, 期间: {'全年' if fiscal_period == 0 else fiscal_period}月, 版本: {budget_version}")

    period_cond = "" if fiscal_period == 0 else f"AND be.fiscal_period = {fiscal_period}"
    cc_cond = "" if not cost_center_id else f"AND be.cost_center_id = '{cost_center_id}'"

    sql = f"""
        SELECT
            be.account_code,
            be.account_name,
            be.pl_category,
            be.cost_center_name,
            sum(be.budget_amount) as budget_amount,
            coalesce(sum(fe.amount_signed), 0) as actual_amount
        FROM fact_budget_entry be
        LEFT JOIN fact_gl_journal_entry fe
            ON be.account_id = fe.account_id
            AND be.cost_center_id = fe.cost_center_id
            AND be.fiscal_year = fe.fiscal_year
            AND be.fiscal_period = fe.fiscal_period
        WHERE be.fiscal_year = {fiscal_year}
            AND be.budget_version = '{budget_version}'
            {period_cond}
            {cc_cond}
        GROUP BY be.account_code, be.account_name, be.pl_category, be.cost_center_name
        ORDER BY be.pl_category, be.account_code
    """

    rows = p.sql.query(sql)

    data = []
    for row in rows:
        budget = row.get("budget_amount", 0) or 0
        actual = row.get("actual_amount", 0) or 0
        variance = actual - budget
        execution_rate = actual / budget if budget != 0 else 0

        data.append({
            "account_code": row.get("account_code"),
            "account_name": row.get("account_name"),
            "pl_category": row.get("pl_category"),
            "cost_center_name": row.get("cost_center_name"),
            "budget_amount": round(budget, 2),
            "actual_amount": round(actual, 2),
            "variance": round(variance, 2),
            "execution_rate": round(execution_rate, 4),
        })

    return p.function_result(
        columns=["account_code", "account_name", "pl_category", "cost_center_name",
                 "budget_amount", "actual_amount", "variance", "execution_rate"],
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
