"""科目结构分析函数

功能：按科目层级展开损益结构
参数：start_date, end_date, account_level（可选，默认显示全部层级）, pl_category（可选）

放置：项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_account_breakdown.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_account_breakdown.py --space space_cate_test01 --register-function-id profit.fn.account_breakdown --register-platform-category 结构分析
"""

from datetime import datetime

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30", "account_level": 0, "pl_category": None},
    "object_type_code": "Account",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    account_level = int(params.get("account_level", 0))
    pl_category = params.get("pl_category", None)

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
            sum(amount_signed) as net_impact
        FROM fact_gl_journal_entry
        WHERE posting_date >= '{start_date}' AND posting_date <= '{end_date}'
            {level_cond}
            {cat_cond}
        GROUP BY account_code, account_name, account_level, pl_category, account_type
        ORDER BY pl_category, account_level, account_code
    """

    rows = p.sql.query(sql)

    total = sum(row.get("net_impact", 0) or 0 for row in rows)

    data = []
    for row in rows:
        net_impact = row.get("net_impact", 0) or 0
        share_pct = net_impact / total if total != 0 else 0

        data.append({
            "account_code": row.get("account_code"),
            "account_name": row.get("account_name"),
            "account_level": row.get("account_level"),
            "pl_category": row.get("pl_category"),
            "account_type": row.get("account_type"),
            "net_impact": round(net_impact, 2),
            "share_pct": round(share_pct, 4),
        })

    return p.function_result(
        columns=["account_code", "account_name", "account_level", "pl_category",
                 "account_type", "net_impact", "share_pct"],
        data=data,
        row_count=len(data),
    )


def main():
    s = space.get(ctx.space_id or "")
    _Ports = type(
        "_Ports",
        (),
        {
            "get_params": lambda self: dict(ctx.params or {}),
            "function_result": lambda self, **kw: onto.function_result(**kw),
        },
    )
    p = _Ports()
    p.sql = s.sql
    return _ontology_fn_body(p)
