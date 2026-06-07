"""产品产量结构 prod_plan.fn.product_mix

参数：start_date, end_date, group_level=category|product, plant_id（可选）
发布：dazi onto script publish .../functions/prod_plan_fn_product_mix.py \
  --space space_cate_test01 --register-function-id prod_plan.fn.product_mix
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2026-01-01",
        "end_date": "2026-06-30",
        "group_level": "category",
    },
    "object_type_code": "ProductionAnalysis",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    group_level = params.get("group_level", "category")
    plant_id = params.get("plant_id") or None

    if group_level == "product":
        gid, gname = "product_id", "product_name"
    else:
        gid, gname = "product_category", "product_category"

    plant_cond = "" if not plant_id else f" AND plant_id = '{plant_id}'"

    sql = f"""
    SELECT
        {gid} AS group_id,
        any({gname}) AS group_name,
        sum(actual_qty) AS actual_qty,
        sum(qualified_qty) AS qualified_qty
    FROM fact_production_daily
    WHERE calendar_date >= '{start_date}' AND calendar_date <= '{end_date}'{plant_cond}
    GROUP BY {gid}
    ORDER BY actual_qty DESC
    """

    rows = p.sql.query(sql) or []
    total = sum(float(r.get("actual_qty") or 0) for r in rows)
    data = []
    for row in rows:
        actual = float(row.get("actual_qty") or 0)
        qualified = float(row.get("qualified_qty") or 0)
        data.append({
            "group_id": str(row.get("group_id") or ""),
            "group_name": str(row.get("group_name") or ""),
            "actual_qty": round(actual, 2),
            "qualified_qty": round(qualified, 2),
            "share_pct": round(actual / total * 100, 2) if total > 0 else 0.0,
            "first_pass_yield": round(qualified / actual, 4) if actual > 0 else 0.0,
        })

    return p.function_result(
        columns=["group_id", "group_name", "actual_qty", "qualified_qty", "share_pct", "first_pass_yield"],
        data=data,
        row_count=len(data),
    )


def main():
    s = space.get(ctx.space_id or "")
    _Ports = type("_Ports", (), {
        "get_params": lambda self: dict(ctx.params or {}),
        "function_result": lambda self, **kw: onto.function_result(**kw),
    })
    p = _Ports()
    p.sql = s.sql
    return _ontology_fn_body(p)
