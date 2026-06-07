"""同比分析函数

功能：对比当期与去年同期的利润指标变化
参数：start_date, end_date

放置：项目/DAZI_TEST/本体/ontos/利润分析示例/functions/profit_fn_yoy_analysis.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润分析示例/functions/profit_fn_yoy_analysis.py --space space__misc_01 --register-function-id profit.fn.yoy_analysis
"""

from datetime import datetime, timedelta
import json


def _ontology_fn_body(p):
    start_date = p.get("start_date", "2025-01-01")
    end_date = p.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    
    last_year_start = (start_dt - timedelta(days=365)).strftime("%Y-%m-%d")
    last_year_end = (end_dt - timedelta(days=365)).strftime("%Y-%m-%d")
    
    output.print(f"当期: {start_date} ~ {end_date}")
    output.print(f"去年同期: {last_year_start} ~ {last_year_end}")
    
    def get_period_data(sd, ed):
        sql = """
            SELECT 
                sumIf(amount_signed, account_type='收入') as revenue,
                sumIf(amount_signed, account_type='成本') as cost,
                sumIf(amount_signed, account_type='费用') as expense
            FROM fact_gl_journal_entry
            WHERE posting_date >= '{sd}' AND posting_date <= '{ed}'
        """.format(sd=sd, ed=ed)
        result = p.space.sql.query_one(sql)
        return {
            "revenue": result.get("revenue", 0) or 0,
            "cost": result.get("cost", 0) or 0,
            "expense": result.get("expense", 0) or 0,
        }
    
    current = get_period_data(start_date, end_date)
    last_year = get_period_data(last_year_start, last_year_end)
    
    current_profit = current["revenue"] - current["cost"] - current["expense"]
    last_year_profit = last_year["revenue"] - last_year["cost"] - last_year["expense"]
    
    def calc_yoy(current, last):
        if last == 0:
            return 0 if current == 0 else None
        return (current - last) / last
    
    result = {
        "period": f"{start_date} ~ {end_date}",
        "last_year_period": f"{last_year_start} ~ {last_year_end}",
        "current": {
            "revenue": round(current["revenue"], 2),
            "cost": round(current["cost"], 2),
            "expense": round(current["expense"], 2),
            "operating_profit": round(current_profit, 2),
        },
        "last_year": {
            "revenue": round(last_year["revenue"], 2),
            "cost": round(last_year["cost"], 2),
            "expense": round(last_year["expense"], 2),
            "operating_profit": round(last_year_profit, 2),
        },
        "yoy": {
            "revenue": round(calc_yoy(current["revenue"], last_year["revenue"]), 4) if calc_yoy(current["revenue"], last_year["revenue"]) is not None else None,
            "cost": round(calc_yoy(current["cost"], last_year["cost"]), 4) if calc_yoy(current["cost"], last_year["cost"]) is not None else None,
            "expense": round(calc_yoy(current["expense"], last_year["expense"]), 4) if calc_yoy(current["expense"], last_year["expense"]) is not None else None,
            "operating_profit": round(calc_yoy(current_profit, last_year_profit), 4) if calc_yoy(current_profit, last_year_profit) is not None else None,
        },
    }
    
    p.function_result(result)


