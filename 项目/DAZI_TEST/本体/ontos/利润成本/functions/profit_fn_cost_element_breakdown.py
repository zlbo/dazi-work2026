"""成本要素分析函数（化工特色）

功能：按成本要素展开成本结构（原料/人工/能源/折旧/其他）
参数：start_date, end_date, plant_id（可选）, unit_id（可选）

放置：项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_cost_element_breakdown.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_cost_element_breakdown.py --space space_cate_test01 --register-function-id profit.fn.cost_element_breakdown --register-platform-category 结构分析
"""

from datetime import datetime

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30", "plant_id": None, "unit_id": None},
    "object_type_code": "ProductionCost",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    plant_id = params.get("plant_id", None)
    unit_id = params.get("unit_id", None)

    output.print(f"期间: {start_date} ~ {end_date}")

    plant_cond = "" if not plant_id else f"AND plant_id = '{plant_id}'"
    unit_cond = "" if not unit_id else f"AND unit_id = '{unit_id}'"

    sql = f"""
        SELECT
            cost_element,
            sum(amount) as total_amount,
            sum(quantity) as total_quantity,
            sum(output_qty) as total_output
        FROM fact_production_cost
        WHERE date_key >= {start_date.replace('-', '')} AND date_key <= {end_date.replace('-', '')}
            {plant_cond}
            {unit_cond}
        GROUP BY cost_element
        ORDER BY total_amount DESC
    """

    rows = p.sql.query(sql)

    total = sum(row.get("total_amount", 0) or 0 for row in rows)

    data = []
    for row in rows:
        total_amount = row.get("total_amount", 0) or 0
        total_quantity = row.get("total_quantity", 0) or 0
        total_output = row.get("total_output", 0) or 0
        share_pct = total_amount / total if total != 0 else 0
        unit_cost = total_amount / total_output if total_output > 0 else 0

        data.append({
            "cost_element": row.get("cost_element") or "其他",
            "total_amount": round(total_amount, 2),
            "total_quantity": round(total_quantity, 2),
            "total_output": round(total_output, 2),
            "share_pct": round(share_pct, 4),
            "unit_cost": round(unit_cost, 2),
        })

    return p.function_result(
        columns=["cost_element", "total_amount", "total_quantity", "total_output",
                 "share_pct", "unit_cost"],
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
