"""成本项详情分析函数

功能：获取各成本项的明细数据
参数：start_date, end_date

放置：项目/DAZI_TEST/本体/ontos/利润成本分析/functions/profit_cost_fn_cost_item_detail.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本分析/functions/profit_cost_fn_cost_item_detail.py --space space_cate_test01 --type ontology_function --register-function-id profit_cost.fn.cost_item_detail
"""

from datetime import datetime
import json


def _ontology_fn_body(p):
    start_date = p.get("start_date", "2025-01-01")
    end_date = p.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    
    output.print(f"查询期间: {start_date} ~ {end_date}")
    
    sql = """
        SELECT 
            c.cost_item_code,
            c.cost_item_name,
            c.cost_item_level,
            sum(f.amount_signed) as total_amount
        FROM fact_gl_journal_entry f
        JOIN dim_cost_item c ON f.cost_item_code = c.cost_item_code
        WHERE f.posting_date >= '{start_date}' AND f.posting_date <= '{end_date}'
        GROUP BY c.cost_item_code, c.cost_item_name, c.cost_item_level
        ORDER BY c.cost_item_code
    """.format(start_date=start_date, end_date=end_date)
    
    result = p.sql.query(sql)
    
    items = []
    total_amount = 0
    for row in result:
        item = {
            "cost_item_code": row.get("cost_item_code", ""),
            "cost_item_name": row.get("cost_item_name", ""),
            "cost_item_level": int(row.get("cost_item_level", 1)),
            "total_amount": round(float(row.get("total_amount", 0) or 0), 2),
        }
        items.append(item)
        total_amount += item["total_amount"]
    
    p.function_result({
        "period": f"{start_date} ~ {end_date}",
        "total_amount": round(total_amount, 2),
        "item_count": len(items),
        "items": items,
    })
