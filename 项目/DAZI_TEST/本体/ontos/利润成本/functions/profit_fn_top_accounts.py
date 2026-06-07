"""重点科目TopN函数

功能：按指定科目类型输出金额Top N
参数：start_date, end_date, account_type（收入/成本/费用）, limit（默认10）, plant_id（可选）

放置：项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_top_accounts.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_top_accounts.py --space space_cate_test01 --register-function-id profit.fn.top_accounts --register-platform-category 结构分析
"""

from datetime import datetime

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30", "account_type": "成本", "limit": 10, "plant_id": None},
    "object_type_code": "Account",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    account_type = params.get("account_type", "成本")
    limit = int(params.get("limit", 10))
    plant_id = params.get("plant_id", None)

    output.print(f"期间: {start_date} ~ {end_date}, 科目类型: {account_type}")

    plant_cond = "" if not plant_id else f"AND plant_id = '{plant_id}'"

    sql = f"""
        SELECT
            account_code,
            account_name,
            account_type,
            pl_category,
            sum(amount_signed) as total_amount
        FROM fact_gl_journal_entry
        WHERE posting_date >= '{start_date}' AND posting_date <= '{end_date}'
            AND account_type = '{account_type}'
            {plant_cond}
        GROUP BY account_code, account_name, account_type, pl_category
        ORDER BY total_amount DESC
        LIMIT {limit}
    """

    rows = p.sql.query(sql)

    total = sum(abs(row.get("total_amount", 0) or 0) for row in rows)

    data = []
    for i, row in enumerate(rows):
        amount = row.get("total_amount", 0) or 0
        data.append({
            "rank": i + 1,
            "account_code": row.get("account_code"),
            "account_name": row.get("account_name"),
            "account_type": row.get("account_type"),
            "pl_category": row.get("pl_category"),
            "total_amount": round(amount, 2),
            "share_pct": round(abs(amount) / total, 4) if total > 0 else 0,
        })

    return p.function_result(
        columns=["rank", "account_code", "account_name", "account_type", "pl_category",
                 "total_amount", "share_pct"],
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
