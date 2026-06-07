"""装置成本分析函数

功能：按装置/单元分析成本结构与单位成本
参数：start_date, end_date, plant_id（可选）, unit_id（可选）

放置：项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_unit_cost_analysis.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_unit_cost_analysis.py --space space_cate_test01 --register-function-id profit.fn.unit_cost_analysis --register-platform-category 组织分析
"""

from datetime import datetime

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30", "plant_id": None, "unit_id": None},
    "object_type_code": "ProcessUnit",
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
            plant_id,
            plant_name,
            unit_id,
            unit_name,
            cost_element,
            sum(amount) as total_amount,
            sum(quantity) as total_quantity,
            sum(output_qty) as total_output
        FROM fact_production_cost
        WHERE date_key >= {start_date.replace('-', '')} AND date_key <= {end_date.replace('-', '')}
            {plant_cond}
            {unit_cond}
        GROUP BY plant_id, plant_name, unit_id, unit_name, cost_element
        ORDER BY plant_name, unit_name, total_amount DESC
    """

    rows = p.sql.query(sql)

    data = []
    for row in rows:
        amount = row.get("total_amount", 0) or 0
        output_val = row.get("total_output", 0) or 0

        data.append({
            "plant_name": row.get("plant_name"),
            "unit_name": row.get("unit_name"),
            "cost_element": row.get("cost_element") or "其他",
            "total_amount": round(amount, 2),
            "total_quantity": round(row.get("total_quantity", 0) or 0, 2),
            "total_output": round(output_val, 2),
            "unit_cost": round(amount / output_val, 2) if output_val > 0 else 0,
        })

    return p.function_result(
        columns=["plant_name", "unit_name", "cost_element", "total_amount",
                 "total_quantity", "total_output", "unit_cost"],
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
