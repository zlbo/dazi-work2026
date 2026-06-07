"""环比分析函数

功能：指定指标环比变化分析
参数：start_date, end_date, metric, plant_id（可选）

放置：项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_mom_analysis.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_mom_analysis.py --space space_cate_test01 --register-function-id profit.fn.mom_analysis --register-platform-category 趋势分析
"""

from datetime import datetime

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30", "metric": "gross_profit", "plant_id": None},
    "object_type_code": "CostAnalysis",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    metric = params.get("metric", "gross_profit")
    plant_id = params.get("plant_id", None)

    output.print(f"期间: {start_date} ~ {end_date}, 指标: {metric}")

    plant_cond = "" if not plant_id else f"AND plant_id = '{plant_id}'"

    metric_expr = {
        "revenue": "sumIf(amount_signed, account_type='收入')",
        "total_cost": "sumIf(amount_signed, account_type in ('成本','费用'))",
        "gross_profit": "sumIf(amount_signed, account_type='收入') + sumIf(amount_signed, account_type in ('成本','费用'))",
        "profit_margin": f"(sumIf(amount_signed, account_type='收入') + sumIf(amount_signed, account_type in ('成本','费用'))) / nullIf(sumIf(amount_signed, account_type='收入'), 0)",
    }

    expr = metric_expr.get(metric, metric_expr["gross_profit"])

    sql = f"""
        SELECT
            toYear(posting_date) as year,
            toMonth(posting_date) as month,
            {expr} as metric_value
        FROM fact_gl_journal_entry
        WHERE posting_date >= '{start_date}' AND posting_date <= '{end_date}'
            {plant_cond}
        GROUP BY toYear(posting_date), toMonth(posting_date)
        ORDER BY year, month
    """

    rows = p.sql.query(sql)

    data = []
    for i, row in enumerate(rows):
        current = row.get("metric_value", 0) or 0
        prev = rows[i-1].get("metric_value", 0) or 0 if i > 0 else 0
        mom_change = current - prev
        mom_pct = mom_change / abs(prev) if prev != 0 else 0

        data.append({
            "year": row["year"],
            "month": row["month"],
            "current_value": round(current, 2),
            "prev_value": round(prev, 2),
            "mom_change": round(mom_change, 2),
            "mom_pct": round(mom_pct, 4),
        })

    return p.function_result(
        columns=["year", "month", "current_value", "prev_value", "mom_change", "mom_pct"],
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
