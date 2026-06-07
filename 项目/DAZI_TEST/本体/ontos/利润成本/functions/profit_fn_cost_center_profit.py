"""成本中心利润分析函数

功能：按成本中心汇总利润与预算执行
参数：start_date, end_date, cost_center_id（可选）, plant_id（可选）

放置：项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_cost_center_profit.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_cost_center_profit.py --space space_cate_test01 --register-function-id profit.fn.cost_center_profit --register-platform-category 组织分析
"""

from datetime import datetime

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30", "cost_center_id": None, "plant_id": None},
    "object_type_code": "CostCenter",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    cost_center_id = params.get("cost_center_id", None)
    plant_id = params.get("plant_id", None)

    output.print(f"期间: {start_date} ~ {end_date}")

    cc_cond = "" if not cost_center_id else f"AND cost_center_id = '{cost_center_id}'"
    plant_cond = "" if not plant_id else f"AND plant_id = '{plant_id}'"

    sql = f"""
        SELECT
            cost_center_id,
            cost_center_name,
            department,
            sumIf(amount_signed, account_type='收入') as revenue,
            sumIf(amount_signed, account_type='成本') as total_cost,
            sumIf(amount_signed, account_type='费用') as total_expense
        FROM fact_gl_journal_entry
        WHERE posting_date >= '{start_date}' AND posting_date <= '{end_date}'
            {cc_cond}
            {plant_cond}
        GROUP BY cost_center_id, cost_center_name, department
        ORDER BY revenue DESC
    """

    rows = p.sql.query(sql)

    data = []
    for row in rows:
        revenue = row.get("revenue", 0) or 0
        total_cost = row.get("total_cost", 0) or 0
        total_expense = row.get("total_expense", 0) or 0
        gross_profit = revenue - abs(total_cost) - abs(total_expense)
        profit_margin = gross_profit / revenue if revenue > 0 else 0

        data.append({
            "cost_center_id": row.get("cost_center_id"),
            "cost_center_name": row.get("cost_center_name"),
            "department": row.get("department"),
            "revenue": round(revenue, 2),
            "total_cost": round(abs(total_cost), 2),
            "total_expense": round(abs(total_expense), 2),
            "gross_profit": round(gross_profit, 2),
            "profit_margin": round(profit_margin, 4),
        })

    return p.function_result(
        columns=["cost_center_id", "cost_center_name", "department", "revenue",
                 "total_cost", "total_expense", "gross_profit", "profit_margin"],
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
