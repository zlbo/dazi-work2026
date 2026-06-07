"""利润总览函数

功能：获取指定期间的损益汇总数据
参数：start_date, end_date（可选，默认2025-01-01至当前）

放置：项目/DAZI_TEST/本体/ontos/利润分析示例/functions/profit_fn_get_summary.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润分析示例/functions/profit_fn_get_summary.py --space space__misc_01 --register-function-id profit.fn.get_summary
"""

from datetime import datetime
import json


def _ontology_fn_body(p):
    start_date = p.get("start_date", "2025-01-01")
    end_date = p.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    
    output.print(f"查询期间: {start_date} ~ {end_date}")
    
    sql = """
        SELECT 
            sumIf(amount_signed, account_type='收入') as total_revenue,
            sumIf(amount_signed, account_type='成本') as total_cost,
            sumIf(amount_signed, account_type='费用') as total_expense,
            count(*) as line_count
        FROM fact_gl_journal_entry
        WHERE posting_date >= '{start_date}' AND posting_date <= '{end_date}'
    """.format(start_date=start_date, end_date=end_date)
    
    result = p.space.sql.query_one(sql)
    
    if result:
        total_revenue = result.get("total_revenue", 0) or 0
        total_cost = result.get("total_cost", 0) or 0
        total_expense = result.get("total_expense", 0) or 0
        line_count = result.get("line_count", 0) or 0
        
        operating_profit = total_revenue - total_cost - total_expense
        profit_margin = operating_profit / total_revenue if total_revenue > 0 else 0
        
        p.function_result({
            "total_revenue": round(total_revenue, 2),
            "total_cost": round(total_cost, 2),
            "total_expense": round(total_expense, 2),
            "operating_profit": round(operating_profit, 2),
            "profit_margin": round(profit_margin, 4),
            "line_count": line_count,
            "period": f"{start_date} ~ {end_date}",
        })
    else:
        p.function_result({
            "total_revenue": 0,
            "total_cost": 0,
            "total_expense": 0,
            "operating_profit": 0,
            "profit_margin": 0,
            "line_count": 0,
            "period": f"{start_date} ~ {end_date}",
        })


