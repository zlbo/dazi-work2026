"""能源分析函数（化工特色）

功能：按能源类型分析消耗与成本结构
参数：start_date, end_date, energy_type_id（可选）, plant_id（可选）

放置：项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_energy_analysis.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_energy_analysis.py --space space_cate_test01 --register-function-id profit.fn.energy_analysis --register-platform-category 结构分析
"""

from datetime import datetime

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30", "energy_type_id": None, "plant_id": None},
    "object_type_code": "EnergyConsumption",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    energy_type_id = params.get("energy_type_id", None)
    plant_id = params.get("plant_id", None)

    output.print(f"期间: {start_date} ~ {end_date}")

    energy_cond = "" if not energy_type_id else f"AND energy_type_id = '{energy_type_id}'"
    plant_cond = "" if not plant_id else f"AND plant_id = '{plant_id}'"

    sql = f"""
        SELECT
            energy_type_id,
            energy_type_name,
            sum(consumption_qty) as total_consumption,
            sum(amount) as total_amount,
            sum(output_qty) as total_output,
            avg(intensity) as avg_intensity
        FROM fact_energy_consumption
        WHERE date_key >= {start_date.replace('-', '')} AND date_key <= {end_date.replace('-', '')}
            {energy_cond}
            {plant_cond}
        GROUP BY energy_type_id, energy_type_name
        ORDER BY total_amount DESC
    """

    rows = p.sql.query(sql)

    total_consumption = sum(row.get("total_consumption", 0) or 0 for row in rows)
    total_amount = sum(row.get("total_amount", 0) or 0 for row in rows)
    total_output = sum(row.get("total_output", 0) or 0 for row in rows)

    data = []
    for row in rows:
        consumption = row.get("total_consumption", 0) or 0
        amount = row.get("total_amount", 0) or 0
        output_val = row.get("total_output", 0) or 0

        data.append({
            "energy_type_id": row.get("energy_type_id"),
            "energy_type_name": row.get("energy_type_name"),
            "consumption_qty": round(consumption, 2),
            "amount": round(amount, 2),
            "consumption_share": round(consumption / total_consumption, 4) if total_consumption > 0 else 0,
            "cost_share": round(amount / total_amount, 4) if total_amount > 0 else 0,
            "avg_intensity": round(row.get("avg_intensity", 0) or 0, 4),
            "cost_per_unit": round(amount / consumption, 2) if consumption > 0 else 0,
            "output_qty": round(output_val, 2),
        })

    return p.function_result(
        columns=["energy_type_id", "energy_type_name", "consumption_qty", "amount",
                 "consumption_share", "cost_share", "avg_intensity", "cost_per_unit", "output_qty"],
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
