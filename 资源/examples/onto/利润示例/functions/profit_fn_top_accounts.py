"""科目Top N分析函数

功能：获取损益影响最大的前N个科目
参数：limit（默认10）, metric（net_impact/revenue/cost/expense）, start_date, end_date, account_type（可选）

放置：项目/DAZI_TEST/本体/ontos/利润分析示例/functions/profit_fn_top_accounts.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润分析示例/functions/profit_fn_top_accounts.py --space space__misc_01 --register-function-id profit.fn.top_accounts
"""

from datetime import datetime
import json


def _ontology_fn_body(p):
    limit = int(p.get("limit", 10))
    metric = p.get("metric", "net_impact")
    start_date = p.get("start_date", "2025-01-01")
    end_date = p.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    account_type = p.get("account_type", None)
    
    output.print(f"期间: {start_date} ~ {end_date}, 取前{limit}个, 指标: {metric}")
    
    type_cond = "" if not account_type else f"AND account_type = '{account_type}'"
    
    metric_expr = {
        "net_impact": "SUM(amount_signed)",
        "revenue": "SUM(if(account_type='收入', amount_signed, 0))",
        "cost": "SUM(if(account_type='成本', amount_signed, 0))",
        "expense": "SUM(if(account_type='费用', amount_signed, 0))",
    }.get(metric, "SUM(amount_signed)")
    
    sql = f"""
        SELECT 
            account_code,
            account_name,
            account_type,
            pl_category,
            {metric_expr} as metric_value
        FROM fact_gl_journal_entry
        WHERE posting_date >= '{start_date}' AND posting_date <= '{end_date}'
            {type_cond}
        GROUP BY account_code, account_name, account_type, pl_category
        ORDER BY metric_value DESC
        LIMIT {limit}
    """
    
    rows = p.space.sql.query(sql)
    
    result = []
    for row in rows:
        result.append({
            "account_code": row.get("account_code"),
            "account_name": row.get("account_name"),
            "account_type": row.get("account_type"),
            "pl_category": row.get("pl_category"),
            "metric_value": round(row.get("metric_value", 0) or 0, 2),
        })
    
    p.function_result(result)


