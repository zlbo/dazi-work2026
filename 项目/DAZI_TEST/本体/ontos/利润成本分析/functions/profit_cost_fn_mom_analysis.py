"""利润成本环比分析函数

功能：获取指定期间与上一月的对比分析数据
参数：year, month

放置：项目/DAZI_TEST/本体/ontos/利润成本分析/functions/profit_cost_fn_mom_analysis.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本分析/functions/profit_cost_fn_mom_analysis.py --space space_cate_test01 --type ontology_function --register-function-id profit_cost.fn.mom_analysis
"""

from datetime import datetime
import calendar
import json


def _ontology_fn_body(p):
    year = int(p.get("year", datetime.now().year))
    month = int(p.get("month", datetime.now().month))
    
    # 当前月份的起止日期
    _, last_day = calendar.monthrange(year, month)
    start_date = f"{year}-{month:02d}-01"
    end_date = f"{year}-{month:02d}-{last_day}"
    
    # 上一月的起止日期
    if month == 1:
        prev_year = year - 1
        prev_month = 12
    else:
        prev_year = year
        prev_month = month - 1
    _, prev_last_day = calendar.monthrange(prev_year, prev_month)
    prev_start_date = f"{prev_year}-{prev_month:02d}-01"
    prev_end_date = f"{prev_year}-{prev_month:02d}-{prev_last_day}"
    
    output.print(f"查询期间: {start_date} ~ {end_date}")
    
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
        WHERE posting_date >= '{prev_start_date}' AND posting_date <= '{prev_end_date}'
    """.format(prev_start_date=prev_start_date, prev_end_date=prev_end_date)
    
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
    
    revenue_mom = (current_revenue - prev_revenue) / prev_revenue if prev_revenue > 0 else 0
    cost_mom = (current_cost - prev_cost) / prev_cost if prev_cost != 0 else 0
    expense_mom = (current_expense - prev_expense) / prev_expense if prev_expense > 0 else 0
    profit_mom = (current_profit - prev_profit) / prev_profit if prev_profit != 0 else 0
    
    p.function_result({
        "current_period": f"{year}年{month}月 ({start_date} ~ {end_date})",
        "previous_period": f"{prev_year}年{prev_month}月 ({prev_start_date} ~ {prev_end_date})",
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
        "mom": {
            "revenue": round(revenue_mom, 4),
            "cost": round(cost_mom, 4),
            "expense": round(expense_mom, 4),
            "profit": round(profit_mom, 4),
        },
    })
