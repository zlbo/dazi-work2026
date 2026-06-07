"""预实对比分析函数

功能：按科目/成本中心对比预算与实际，输出差异与执行率
参数：fiscal_year, fiscal_period（可选0=全年）, budget_version, cost_center_id（可选）

放置：项目/DAZI_TEST/本体/ontos/利润成本分析/functions/profit_cost_fn_budget_vs_actual.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本分析/functions/profit_cost_fn_budget_vs_actual.py --space space_cate_test01 --register-function-id profit_cost.fn.budget_vs_actual
"""

import json

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "fiscal_year": 2026,
        "fiscal_period": 0,
        "budget_version": "2026年度预算",
        "cost_center_id": ""
    }
}


def _ontology_fn_body(p):
    fiscal_year = p.get("fiscal_year", 2026)
    fiscal_period = p.get("fiscal_period", 0)  # 0表示全年
    budget_version = p.get("budget_version", "2026年度预算")
    cost_center_id = p.get("cost_center_id", "")
    
    output.print(f"预实对比: 年度={fiscal_year}, 期间={fiscal_period}, 版本={budget_version}")
    
    # 构建查询条件
    period_filter = f"fiscal_year = {fiscal_year}" if fiscal_period == 0 else f"fiscal_year = {fiscal_year} AND fiscal_period = {fiscal_period}"
    cc_filter = "" if not cost_center_id else f"AND cost_center_id = '{cost_center_id}'"
    
    # 查询预算数据
    budget_sql = """
        SELECT 
            account_id,
            account_code,
            account_name,
            pl_category,
            cost_center_id,
            cost_center_name,
            sum(budget_amount) as budget_amount
        FROM fact_budget_entry
        WHERE {period_filter} AND budget_version = '{version}' {cc_filter}
        GROUP BY account_id, account_code, account_name, pl_category, cost_center_id, cost_center_name
    """.format(period_filter=period_filter, version=budget_version, cc_filter=cc_filter)
    
    budget_rows = p.space.sql.query(budget_sql)
    
    # 查询实际数据
    actual_sql = """
        SELECT 
            account_id,
            account_code,
            account_name,
            pl_category,
            cost_center_id,
            cost_center_name,
            sum(amount_signed) as actual_amount
        FROM fact_gl_journal_entry
        WHERE {period_filter} {cc_filter}
        GROUP BY account_id, account_code, account_name, pl_category, cost_center_id, cost_center_name
    """.format(period_filter=period_filter, cc_filter=cc_filter)
    
    actual_rows = p.space.sql.query(actual_sql)
    
    # 合并预实数据
    budget_dict = {}
    for row in budget_rows:
        key = f"{row['account_id']}_{row['cost_center_id']}"
        budget_dict[key] = row
    
    actual_dict = {}
    for row in actual_rows:
        key = f"{row['account_id']}_{row['cost_center_id']}"
        actual_dict[key] = row
    
    results = []
    for key, budget_row in budget_dict.items():
        actual_row = actual_dict.get(key, {})
        
        budget_amount = budget_row.get("budget_amount", 0) or 0
        actual_amount = actual_row.get("actual_amount", 0) or 0
        
        variance = actual_amount - budget_amount
        execution_rate = abs(actual_amount) / abs(budget_amount) * 100 if budget_amount != 0 else 0
        
        results.append({
            "account_code": budget_row.get("account_code", ""),
            "account_name": budget_row.get("account_name", ""),
            "pl_category": budget_row.get("pl_category", ""),
            "cost_center_name": budget_row.get("cost_center_name", ""),
            "budget_amount": round(abs(budget_amount), 2),
            "actual_amount": round(abs(actual_amount), 2),
            "variance": round(variance, 2),
            "execution_rate": round(execution_rate, 2),
        })
    
    # 按执行率排序
    results.sort(key=lambda x: x["execution_rate"], reverse=True)
    
    p.function_result({
        "budget_vs_actual": results,
        "fiscal_year": fiscal_year,
        "fiscal_period": fiscal_period,
        "budget_version": budget_version,
        "total_items": len(results),
    })


def main():
    ctx = space.get_context()
    return _ontology_fn_body(ctx.params)