"""成本结构分析函数

功能：按成本项层级展开成本结构
参数：start_date, end_date, cost_item_level（可选）

放置：项目/DAZI_TEST/本体/ontos/利润成本分析/functions/profit_cost_fn_cost_structure.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本分析/functions/profit_cost_fn_cost_structure.py --space space_cate_test01 --register-function-id profit_cost.fn.cost_structure
"""

from datetime import datetime
import json

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2025-01-01",
        "end_date": "2026-06-30",
        "cost_item_level": 2
    }
}


def _ontology_fn_body(p):
    start_date = p.get("start_date", "2025-01-01")
    end_date = p.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    cost_item_level = p.get("cost_item_level", 2)
    
    output.print(f"查询期间: {start_date} ~ {end_date}, 层级: {cost_item_level}")
    
    # 查询成本项结构
    sql = """
        SELECT 
            ci.cost_item_id,
            ci.cost_item_code,
            ci.cost_item_name,
            ci.cost_item_type,
            ci.cost_category,
            ci.cost_item_level,
            sumIf(je.amount_signed, je.account_type='成本') as cost_amount,
            sumIf(je.amount_signed, je.account_type='费用') as expense_amount
        FROM fact_gl_journal_entry je
        LEFT JOIN dim_cost_item ci ON je.cost_item_id = ci.cost_item_id
        WHERE je.posting_date >= '{start_date}' AND je.posting_date <= '{end_date}'
          AND ci.cost_item_level <= {level}
        GROUP BY ci.cost_item_id, ci.cost_item_code, ci.cost_item_name, ci.cost_item_type, ci.cost_category, ci.cost_item_level
        ORDER BY ci.cost_item_code
    """.format(start_date=start_date, end_date=end_date, level=cost_item_level)
    
    rows = p.space.sql.query(sql)
    
    results = []
    total_cost = 0
    
    for row in rows:
        cost_amount = row.get("cost_amount", 0) or 0
        expense_amount = row.get("expense_amount", 0) or 0
        total_amount = abs(cost_amount) + abs(expense_amount)
        
        total_cost += total_amount
        
        results.append({
            "cost_item_id": row.get("cost_item_id", ""),
            "cost_item_code": row.get("cost_item_code", ""),
            "cost_item_name": row.get("cost_item_name", ""),
            "cost_item_type": row.get("cost_item_type", ""),
            "cost_category": row.get("cost_category", ""),
            "cost_item_level": row.get("cost_item_level", 0),
            "cost_amount": round(abs(cost_amount), 2),
            "expense_amount": round(abs(expense_amount), 2),
            "total_amount": round(total_amount, 2),
        })
    
    # 计算占比
    for r in results:
        r["share_pct"] = round(r["total_amount"] / total_cost * 100, 2) if total_cost > 0 else 0
    
    p.function_result({
        "cost_structure": results,
        "total_cost": round(total_cost, 2),
        "period": f"{start_date} ~ {end_date}",
    })


def main():
    ctx = space.get_context()
    return _ontology_fn_body(ctx.params)