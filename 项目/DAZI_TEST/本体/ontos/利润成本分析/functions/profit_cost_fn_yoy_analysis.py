"""利润成本同比分析函数

功能：获取指定期间与去年同期的对比分析数据
参数：start_date, end_date

放置：项目/DAZI_TEST/本体/ontos/利润成本分析/functions/profit_cost_fn_yoy_analysis.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本分析/functions/profit_cost_fn_yoy_analysis.py --space space_cate_test01 --type ontology_function --register-function-id profit_cost.fn.yoy_analysis
"""

from datetime import datetime, timedelta
import json


def _ontology_fn_body(p):
    end_date = p.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    start_date = p.get("start_date", (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"))
    
    output.print(f"查询期间: {start_date} ~ {end_date}")
    
    # 计算去年同期
    start_date_prev = str(int(start_date[:4])-1) + start_date[4:]
    end_date_prev = str(int(end_date[:4])-1) + end_date[4:]
    
    sql = """
        SELECT 
            sumIf(amount_signed, account_type='收入') as total_revenue,
            sumIf(amount_signed, account_type='成本') as total_cost,
            sumIf(amount_signed, account_type='费用') as total_expense
        FROM fact_gl_journal_entry
        WHERE posting_date >= '{start_date}' AND posting_date <= '{end_date}'
    """.format(start_date=start_date, end_date=end_date)
    
    result = p.sql.query(sql)
    current_data = result[0] if result else {}
    
    sql_prev = """
        SELECT 
            sumIf(amount_signed, account_type='收入') as total_revenue,
            sumIf(amount_signed, account_type='成本') as total_cost,
            sumIf(amount_signed, account_type='费用') as total_expense
        FROM fact_gl_journal_entry
        WHERE posting_date >= '{start_date_prev}' AND posting_date <= '{end_date_prev}'
    """.format(start_date_prev=start_date_prev, end_date_prev=end_date_prev)
    
    result_prev = p.sql.query(sql_prev)
    prev_data = result_prev[0] if result_prev else {}
    
    current_revenue = float(current_data.get("total_revenue", 0) or 0)
    current_cost = float(current_data.get("total_cost", 0) or 0)
    current_expense = float(current_data.get("total_expense", 0) or 0)
    
    prev_revenue = float(prev_data.get("total_revenue", 0) or 0)
    prev_cost = float(prev_data.get("total_cost", 0) or 0)
    prev_expense = float(prev_data.get("total_expense", 0) or 0)
    
    current_profit = current_revenue + current_cost - current_expense
    prev_profit = prev_revenue + prev_cost - prev_expense
    
    revenue_yoy = (current_revenue - prev_revenue) / prev_revenue if prev_revenue > 0 else 0
    cost_yoy = (current_cost - prev_cost) / prev_cost if prev_cost != 0 else 0
    expense_yoy = (current_expense - prev_expense) / prev_expense if prev_expense > 0 else 0
    profit_yoy = (current_profit - prev_profit) / prev_profit if prev_profit != 0 else 0
    
    p.function_result({
        "current_period": f"{start_date} ~ {end_date}",
        "previous_period": f"{start_date_prev} ~ {end_date_prev}",
        "current": {
            "revenue": round(current_revenue, 2),
            "cost": round(current_cost, 2),
            "expense": round(current_expense, 2),
            "profit": round(current_profit, 2),
        },
        "previous": {
            "revenue": round(prev_revenue, 2),
            "cost": round(prev_cost, 2),
            "expense": round(prev_expense, 2),
            "profit": round(prev_profit, 2),
        },
        "yoy": {
            "revenue": round(revenue_yoy, 4),
            "cost": round(cost_yoy, 4),
            "expense": round(expense_yoy, 4),
            "profit": round(profit_yoy, 4),
        },
    })
