"""预算对比实际分析函数

功能：按科目/成本中心对比预算与实际，输出差异与执行率
参数：fiscal_year, fiscal_period（可选，0=全年）, budget_version, cost_center_id（可选）

放置：项目/DAZI_TEST/本体/ontos/利润分析示例/functions/profit_fn_budget_vs_actual.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润分析示例/functions/profit_fn_budget_vs_actual.py --space space__misc_01 --register-function-id profit.fn.budget_vs_actual
"""

from datetime import datetime
import json


def _ontology_fn_body(p):
    fiscal_year = int(p.get("fiscal_year", datetime.now().year))
    fiscal_period = int(p.get("fiscal_period", 0))
    budget_version = p.get("budget_version", "2026年度预算")
    cost_center_id = p.get("cost_center_id", None)
    
    output.print(f"预算年度: {fiscal_year}, 期间: {'全年' if fiscal_period == 0 else fiscal_period}月, 版本: {budget_version}")
    
    period_cond = "" if fiscal_period == 0 else f"AND be.fiscal_period = {fiscal_period}"
    cc_cond = "" if not cost_center_id else f"AND be.cost_center_id = '{cost_center_id}'"
    
    sql = f"""
        SELECT 
            be.account_code,
            be.account_name,
            be.pl_category,
            be.cost_center_name,
            SUM(be.budget_amount) as budget_amount,
            COALESCE(SUM(fe.amount_signed), 0) as actual_amount
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
    
    rows = p.space.sql.query(sql)
    
    result = []
    for row in rows:
        budget = row.get("budget_amount", 0) or 0
        actual = row.get("actual_amount", 0) or 0
        variance = actual - budget
        execution_rate = actual / budget if budget != 0 else 0
        
        result.append({
            "account_code": row.get("account_code"),
            "account_name": row.get("account_name"),
            "pl_category": row.get("pl_category"),
            "cost_center_name": row.get("cost_center_name"),
            "budget_amount": round(budget, 2),
            "actual_amount": round(actual, 2),
            "variance": round(variance, 2),
            "execution_rate": round(execution_rate, 4),
        })
    
    p.function_result(result)


