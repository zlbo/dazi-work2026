"""科目结构分析函数

功能：按科目层级展开损益结构
参数：start_date, end_date, account_level（可选，默认显示全部层级）, pl_category（可选）

放置：项目/DAZI_TEST/本体/ontos/利润分析示例/functions/profit_fn_account_breakdown.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润分析示例/functions/profit_fn_account_breakdown.py --space space__misc_01 --register-function-id profit.fn.account_breakdown
"""

from datetime import datetime
import json


def _ontology_fn_body(p):
    start_date = p.get("start_date", "2025-01-01")
    end_date = p.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    account_level = int(p.get("account_level", 0))
    pl_category = p.get("pl_category", None)
    
    output.print(f"期间: {start_date} ~ {end_date}, 层级: {'全部' if account_level == 0 else account_level}")
    
    level_cond = "" if account_level == 0 else f"AND account_level = {account_level}"
    cat_cond = "" if not pl_category else f"AND pl_category = '{pl_category}'"
    
    sql = f"""
        SELECT 
            account_code,
            account_name,
            account_level,
            pl_category,
            account_type,
            SUM(amount_signed) as net_impact
        FROM fact_gl_journal_entry
        WHERE posting_date >= '{start_date}' AND posting_date <= '{end_date}'
            {level_cond}
            {cat_cond}
        GROUP BY account_code, account_name, account_level, pl_category, account_type
        ORDER BY pl_category, account_level, account_code
    """
    
    rows = p.space.sql.query(sql)
    
    total = sum(row.get("net_impact", 0) or 0 for row in rows)
    
    result = []
    for row in rows:
        net_impact = row.get("net_impact", 0) or 0
        share_pct = net_impact / total if total != 0 else 0
        
        result.append({
            "account_code": row.get("account_code"),
            "account_name": row.get("account_name"),
            "account_level": row.get("account_level"),
            "pl_category": row.get("pl_category"),
            "account_type": row.get("account_type"),
            "net_impact": round(net_impact, 2),
            "share_pct": round(share_pct, 4),
        })
    
    p.function_result(result)


