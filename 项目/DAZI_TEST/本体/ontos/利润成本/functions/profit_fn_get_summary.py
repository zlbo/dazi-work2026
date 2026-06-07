"""损益总览函数

功能：获取指定期间的损益汇总数据
参数：start_date, end_date, plant_id（可选）

放置：项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_get_summary.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_get_summary.py --space space_cate_test01 --register-function-id profit.fn.get_summary --register-platform-category 总览分析
"""

from datetime import datetime

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30", "plant_id": None},
    "object_type_code": "CostAnalysis",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    plant_id = params.get("plant_id", None)

    output.print(f"查询期间: {start_date} ~ {end_date}")

    plant_cond = "" if not plant_id else f"AND plant_id = '{plant_id}'"

    # 损益表核心数据 - 来自 GL 日记账
    sql = f"""
        SELECT
            sumIf(amount_signed, account_type='收入') as total_revenue,
            sumIf(amount_signed, account_type='成本') as total_cost,
            sumIf(amount_signed, account_type='费用') as total_expense,
            count(*) as line_count
        FROM fact_gl_journal_entry
        WHERE posting_date >= '{start_date}' AND posting_date <= '{end_date}'
        {plant_cond}
    """

    rows = p.sql.query(sql)
    result = rows[0] if rows else {}

    total_revenue = result.get("total_revenue", 0) or 0
    total_cost = result.get("total_cost", 0) or 0
    total_expense = result.get("total_expense", 0) or 0

    gross_profit = total_revenue - total_cost - total_expense
    profit_margin = gross_profit / total_revenue if total_revenue > 0 else 0

    # 成本要素 breakdown - 来自 fact_production_cost
    cost_sql = f"""
        SELECT
            sumIf(amount, cost_element='原料') as material_cost,
            sumIf(amount, cost_element='能源') as energy_cost,
            sumIf(amount, cost_element='人工') as labor_cost,
            sumIf(amount, cost_element in ('折旧','其他')) as overhead_cost
        FROM fact_production_cost
        WHERE date_key >= {start_date.replace('-', '')} AND date_key <= {end_date.replace('-', '')}
        {plant_cond}
    """
    cost_rows = p.sql.query(cost_sql)
    cost_result = cost_rows[0] if cost_rows else {}
    material_cost = abs(cost_result.get("material_cost", 0) or 0)
    energy_cost = abs(cost_result.get("energy_cost", 0) or 0)
    labor_cost = abs(cost_result.get("labor_cost", 0) or 0)
    overhead_cost = abs(cost_result.get("overhead_cost", 0) or 0)

    # 预算
    budget_sql = f"""
        SELECT sum(budget_amount) as total_budget
        FROM fact_budget_entry
        WHERE fiscal_year = {datetime.now().year} AND budget_version = '2026年度预算'
        {plant_cond}
    """
    budget_rows = p.sql.query(budget_sql)
    total_budget = budget_rows[0].get("total_budget", 0) or 0 if budget_rows else 0

    data = [{
        "period": f"{start_date} ~ {end_date}",
        "total_revenue": round(total_revenue, 2),
        "total_cost": round(total_cost, 2),
        "total_expense": round(total_expense, 2),
        "gross_profit": round(gross_profit, 2),
        "profit_margin": round(profit_margin, 4),
        "material_cost": round(material_cost, 2),
        "energy_cost": round(energy_cost, 2),
        "labor_cost": round(labor_cost, 2),
        "overhead_cost": round(overhead_cost, 2),
        "total_budget": round(total_budget, 2),
        "budget_execution_rate": round(total_revenue / total_budget, 4) if total_budget > 0 else 0,
        "line_count": result.get("line_count", 0),
    }]

    return p.function_result(
        columns=["period", "total_revenue", "total_cost", "total_expense", "gross_profit",
                 "profit_margin", "material_cost", "energy_cost", "labor_cost", "overhead_cost",
                 "total_budget", "budget_execution_rate", "line_count"],
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
