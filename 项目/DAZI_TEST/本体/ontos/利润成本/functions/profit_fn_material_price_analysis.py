"""原料价格分析函数（化工特色）

功能：分析原料采购/消耗价格与标准价差
参数：start_date, end_date, material_id（可选）, plant_id（可选）

放置：项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_material_price_analysis.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本/functions/profit_fn_material_price_analysis.py --space space_cate_test01 --register-function-id profit.fn.material_price_analysis --register-platform-category 结构分析
"""

from datetime import datetime

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30", "material_id": None, "plant_id": None},
    "object_type_code": "Material",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    material_id = params.get("material_id", None)
    plant_id = params.get("plant_id", None)

    output.print(f"期间: {start_date} ~ {end_date}")

    material_cond = "" if not material_id else f"AND pc.material_id = '{material_id}'"
    plant_cond = "" if not plant_id else f"AND pc.plant_id = '{plant_id}'"

    sql = f"""
        SELECT
            pc.material_id,
            pc.material_name,
            pc.plant_id,
            pc.plant_name,
            pc.unit_id,
            pc.unit_name,
            sum(pc.quantity) as total_quantity,
            sum(pc.amount) as total_amount,
            avg(pc.unit_price) as avg_price,
            avg(m.unit_price_standard) as standard_price
        FROM fact_production_cost pc
        LEFT JOIN dim_material m ON pc.material_id = m.material_id
        WHERE pc.date_key >= {start_date.replace('-', '')} AND pc.date_key <= {end_date.replace('-', '')}
            AND pc.material_id IS NOT NULL
            {material_cond}
            {plant_cond}
        GROUP BY pc.material_id, pc.material_name, pc.plant_id, pc.plant_name, pc.unit_id, pc.unit_name
        ORDER BY total_amount DESC
    """

    rows = p.sql.query(sql)

    data = []
    for row in rows:
        avg_price = row.get("avg_price", 0) or 0
        standard_price = row.get("standard_price", 0) or 0
        price_diff = avg_price - standard_price
        price_diff_pct = price_diff / standard_price if standard_price > 0 else 0

        data.append({
            "material_id": row.get("material_id"),
            "material_name": row.get("material_name"),
            "plant_name": row.get("plant_name"),
            "unit_name": row.get("unit_name"),
            "total_quantity": round(row.get("total_quantity", 0) or 0, 2),
            "total_amount": round(row.get("total_amount", 0) or 0, 2),
            "avg_price": round(avg_price, 2),
            "standard_price": round(standard_price, 2),
            "price_diff": round(price_diff, 2),
            "price_diff_pct": round(price_diff_pct, 4),
        })

    return p.function_result(
        columns=["material_id", "material_name", "plant_name", "unit_name",
                 "total_quantity", "total_amount", "avg_price", "standard_price",
                 "price_diff", "price_diff_pct"],
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
