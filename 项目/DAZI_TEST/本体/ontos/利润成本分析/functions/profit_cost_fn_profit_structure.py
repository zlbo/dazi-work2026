"""利润结构分析函数

功能：按利润项层级展开利润结构
参数：start_date, end_date, profit_item_level（可选）

放置：项目/DAZI_TEST/本体/ontos/利润成本分析/functions/profit_cost_fn_profit_structure.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本分析/functions/profit_cost_fn_profit_structure.py --space space_cate_test01 --register-function-id profit_cost.fn.profit_structure
"""

from datetime import datetime
import json

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2025-01-01",
        "end_date": "2026-06-30",
        "profit_item_level": 2
    }
}


def _ontology_fn_body(p):
    start_date = p.get("start_date", "2025-01-01")
    end_date = p.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    profit_item_level = p.get("profit_item_level", 2)
    
    output.print(f"查询期间: {start_date} ~ {end_date}, 层级: {profit_item_level}")
    
    # 查询利润项结构
    sql = """
        SELECT 
            pi.profit_item_id,
            pi.profit_item_code,
            pi.profit_item_name,
            pi.profit_item_type,
            pi.profit_item_level,
            sumIf(je.amount_signed, je.account_type='收入') as revenue,
            sumIf(je.amount_signed, je.account_type='成本') as cost,
            sumIf(je.amount_signed, je.account_type='费用') as expense
        FROM fact_gl_journal_entry je
        LEFT JOIN dim_profit_item pi ON je.profit_item_id = pi.profit_item_id
        WHERE je.posting_date >= '{start_date}' AND je.posting_date <= '{end_date}'
          AND pi.profit_item_level <= {level}
        GROUP BY pi.profit_item_id, pi.profit_item_code, pi.profit_item_name, pi.profit_item_type, pi.profit_item_level
        ORDER BY pi.profit_item_code
    """.format(start_date=start_date, end_date=end_date, level=profit_item_level)
    
    rows = p.space.sql.query(sql)
    
    results = []
    total_revenue = 0
    total_cost = 0
    
    for row in rows:
        revenue = row.get("revenue", 0) or 0
        cost = row.get("cost", 0) or 0
        expense = row.get("expense", 0) or 0
        gross_profit = revenue + cost
        
        total_revenue += revenue
        total_cost += abs(cost)
        
        results.append({
            "profit_item_id": row.get("profit_item_id", ""),
            "profit_item_code": row.get("profit_item_code", ""),
            "profit_item_name": row.get("profit_item_name", ""),
            "profit_item_type": row.get("profit_item_type", ""),
            "profit_item_level": row.get("profit_item_level", 0),
            "revenue": round(revenue, 2),
            "cost": round(cost, 2),
            "expense": round(expense, 2),
            "gross_profit": round(gross_profit, 2),
        })
    
    # 计算占比
    for r in results:
        if r["revenue"] != 0:
            r["revenue_share_pct"] = round(r["revenue"] / total_revenue * 100, 2) if total_revenue > 0 else 0
        else:
            r["revenue_share_pct"] = 0
    
    p.function_result({
        "profit_structure": results,
        "total_revenue": round(total_revenue, 2),
        "total_cost": round(total_cost, 2),
        "period": f"{start_date} ~ {end_date}",
    })


def main():
    ctx = space.get_context()
    return _ontology_fn_body(ctx.params)