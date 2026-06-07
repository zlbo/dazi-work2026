"""成本中心利润分析函数

功能：按成本中心/部门分析利润贡献
参数：start_date, end_date, department（可选）

放置：项目/DAZI_TEST/本体/ontos/利润分析示例/functions/profit_fn_cost_center_profit.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润分析示例/functions/profit_fn_cost_center_profit.py --space space__misc_01 --register-function-id profit.fn.cost_center_profit
"""

from datetime import datetime
import json


def _ontology_fn_body(p):
    start_date = p.get("start_date", "2025-01-01")
    end_date = p.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    department = p.get("department", None)
    
    output.print(f"期间: {start_date} ~ {end_date}, 部门: {'全部' if not department else department}")
    
    dept_cond = "" if not department else f"AND department = '{department}'"
    
    sql = f"""
        SELECT 
            cost_center_id,
            cost_center_name,
            department,
            profit_center,
            SUM(amount_signed) as total_amount,
            SUM(if(account_type='收入', amount_signed, 0)) as revenue,
            SUM(if(account_type='成本', amount_signed, 0)) as cost,
            SUM(if(account_type='费用', amount_signed, 0)) as expense
        FROM fact_gl_journal_entry
        WHERE posting_date >= '{start_date}' AND posting_date <= '{end_date}'
            {dept_cond}
        GROUP BY cost_center_id, cost_center_name, department, profit_center
        ORDER BY department, cost_center_name
    """
    
    rows = p.space.sql.query(sql)
    
    result = []
    for row in rows:
        revenue = row.get("revenue", 0) or 0
        cost = row.get("cost", 0) or 0
        expense = row.get("expense", 0) or 0
        operating_profit = revenue - cost - expense
        profit_margin = operating_profit / revenue if revenue > 0 else 0
        
        result.append({
            "cost_center_id": row.get("cost_center_id"),
            "cost_center_name": row.get("cost_center_name"),
            "department": row.get("department"),
            "profit_center": row.get("profit_center"),
            "revenue": round(revenue, 2),
            "cost": round(cost, 2),
            "expense": round(expense, 2),
            "operating_profit": round(operating_profit, 2),
            "profit_margin": round(profit_margin, 4),
        })
    
    p.function_result(result)


