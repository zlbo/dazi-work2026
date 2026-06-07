"""环比分析函数

功能：对比当期与上一期的利润指标变化
参数：start_date, end_date

放置：项目/DAZI_TEST/本体/ontos/利润分析示例/functions/profit_fn_mom_analysis.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润分析示例/functions/profit_fn_mom_analysis.py --space space__misc_01 --register-function-id profit.fn.mom_analysis
"""

from datetime import datetime, timedelta
import calendar
import json


def _ontology_fn_body(p):
    start_date = p.get("start_date", "2025-01-01")
    end_date = p.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    
    days_diff = (end_dt - start_dt).days
    
    prev_start = (start_dt - timedelta(days=days_diff)).strftime("%Y-%m-%d")
    prev_end = (end_dt - timedelta(days=days_diff)).strftime("%Y-%m-%d")
    
    output.print(f"当期: {start_date} ~ {end_date}")
    output.print(f"上期: {prev_start} ~ {prev_end}")
    
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
    previous = get_period_data(prev_start, prev_end)
    
    current_profit = current["revenue"] - current["cost"] - current["expense"]
    previous_profit = previous["revenue"] - previous["cost"] - previous["expense"]
    
    def calc_mom(current, prev):
        if prev == 0:
            return 0 if current == 0 else None
        return (current - prev) / prev
    
    result = {
        "period": f"{start_date} ~ {end_date}",
        "previous_period": f"{prev_start} ~ {prev_end}",
        "current": {
            "revenue": round(current["revenue"], 2),
            "cost": round(current["cost"], 2),
            "expense": round(current["expense"], 2),
            "operating_profit": round(current_profit, 2),
        },
        "previous": {
            "revenue": round(previous["revenue"], 2),
            "cost": round(previous["cost"], 2),
            "expense": round(previous["expense"], 2),
            "operating_profit": round(previous_profit, 2),
        },
        "mom": {
            "revenue": round(calc_mom(current["revenue"], previous["revenue"]), 4) if calc_mom(current["revenue"], previous["revenue"]) is not None else None,
            "cost": round(calc_mom(current["cost"], previous["cost"]), 4) if calc_mom(current["cost"], previous["cost"]) is not None else None,
            "expense": round(calc_mom(current["expense"], previous["expense"]), 4) if calc_mom(current["expense"], previous["expense"]) is not None else None,
            "operating_profit": round(calc_mom(current_profit, previous_profit), 4) if calc_mom(current_profit, previous_profit) is not None else None,
        },
    }
    
    p.function_result(result)


