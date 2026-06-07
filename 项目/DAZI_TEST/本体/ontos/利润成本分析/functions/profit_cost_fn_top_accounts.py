"""科目排行分析函数

功能：获取金额最大的前N个科目
参数：start_date, end_date, limit

放置：项目/DAZI_TEST/本体/ontos/利润成本分析/functions/profit_cost_fn_top_accounts.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本分析/functions/profit_cost_fn_top_accounts.py --space space_cate_test01 --type ontology_function --register-function-id profit_cost.fn.top_accounts
"""

from datetime import datetime
import json


def _ontology_fn_body(p):
    start_date = p.get("start_date", "2025-01-01")
    end_date = p.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    limit = int(p.get("limit", 10))
    
    output.print(f"查询期间: {start_date} ~ {end_date}")
    
    sql = """
        SELECT 
            a.account_code,
            a.account_name,
            a.account_type,
            sum(f.amount_signed) as total_amount,
            abs(sum(f.amount_signed)) as abs_amount
        FROM fact_gl_journal_entry f
        JOIN dim_account a ON f.account_code = a.account_code
        WHERE f.posting_date >= '{start_date}' AND f.posting_date <= '{end_date}'
        GROUP BY a.account_code, a.account_name, a.account_type
        ORDER BY abs_amount DESC
        LIMIT {limit}
    """.format(start_date=start_date, end_date=end_date, limit=limit)
    
    result = p.sql.query(sql)
    
    top_accounts = []
    for row in result:
        account = {
            "account_code": row.get("account_code", ""),
            "account_name": row.get("account_name", ""),
            "account_type": row.get("account_type", ""),
            "total_amount": round(float(row.get("total_amount", 0) or 0), 2),
            "abs_amount": round(float(row.get("abs_amount", 0) or 0), 2),
        }
        top_accounts.append(account)
    
    p.function_result({
        "period": f"{start_date} ~ {end_date}",
        "limit": limit,
        "top_accounts": top_accounts,
    })
