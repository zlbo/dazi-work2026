"""成本中心利润分析函数

功能：获取各成本中心的利润分析数据
参数：start_date, end_date

放置：项目/DAZI_TEST/本体/ontos/利润成本分析/functions/profit_cost_fn_cost_center_profit.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本分析/functions/profit_cost_fn_cost_center_profit.py --space space_cate_test01 --type ontology_function --register-function-id profit_cost.fn.cost_center_profit
"""

from datetime import datetime
import json


def _ontology_fn_body(p):
    start_date = p.get("start_date", "2025-01-01")
    end_date = p.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    
    output.print(f"查询期间: {start_date} ~ {end_date}")
    
    sql = """
        SELECT 
            c.cost_center_code,
            c.cost_center_name,
            sumIf(f.amount_signed, a.account_type='收入') as revenue,
            sumIf(f.amount_signed, a.account_type='成本') as cost,
            sumIf(f.amount_signed, a.account_type='费用') as expense,
            count(*) as entry_count
        FROM fact_gl_journal_entry f
        JOIN dim_cost_center c ON f.cost_center_code = c.cost_center_code
        JOIN dim_account a ON f.account_code = a.account_code
        WHERE f.posting_date >= '{start_date}' AND f.posting_date <= '{end_date}'
        GROUP BY c.cost_center_code, c.cost_center_name
        ORDER BY c.cost_center_code
    """.format(start_date=start_date, end_date=end_date)
    
    result = p.sql.query(sql)
    
    cost_centers = []
    total_revenue = 0
    total_cost = 0
    total_expense = 0
    
    for row in result:
        revenue = float(row.get("revenue", 0) or 0)
        cost = float(row.get("cost", 0) or 0)
        expense = float(row.get("expense", 0) or 0)
        profit = revenue + cost - expense  # 成本为负数
        
        cc = {
            "cost_center_code": row.get("cost_center_code", ""),
            "cost_center_name": row.get("cost_center_name", ""),
            "revenue": round(revenue, 2),
            "cost": round(cost, 2),
            "expense": round(expense, 2),
            "profit": round(profit, 2),
            "entry_count": int(row.get("entry_count", 0) or 0),
        }
        cost_centers.append(cc)
        total_revenue += revenue
        total_cost += cost
        total_expense += expense
    
    total_profit = total_revenue + total_cost - total_expense
    
    p.function_result({
        "period": f"{start_date} ~ {end_date}",
        "total": {
            "revenue": round(total_revenue, 2),
            "cost": round(total_cost, 2),
            "expense": round(total_expense, 2),
            "profit": round(total_profit, 2),
        },
        "cost_center_count": len(cost_centers),
        "cost_centers": cost_centers,
    })
