"""物料缺口与齐套 prod_plan.fn.material_shortage

参数：start_date, end_date, plant_id（可选）, critical_only（可选 bool）
发布：dazi onto script publish .../functions/prod_plan_fn_material_shortage.py \
  --space space_cate_test01 --register-function-id prod_plan.fn.material_shortage
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2026-01-01",
        "end_date": "2026-06-30",
        "critical_only": True,
    },
    "object_type_code": "MaterialRequirement",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    plant_id = params.get("plant_id") or None
    critical_only = params.get("critical_only", False)

    clauses = [f"requirement_date >= '{start_date}'", f"requirement_date <= '{end_date}'"]
    if plant_id:
        clauses.append(f"plant_id = '{plant_id}'")
    if critical_only:
        clauses.append("is_critical = 1")
    where_clause = "WHERE " + " AND ".join(clauses)

    sql = f"""
    SELECT
        component_product_code,
        any(component_product_name) AS component_product_name,
        sum(planned_require_qty) AS planned_require_qty,
        sum(actual_issue_qty) AS actual_issue_qty,
        any(kit_status) AS kit_status,
        max(is_critical) AS is_critical
    FROM fact_material_requirement
    {where_clause}
    GROUP BY component_product_code
    HAVING planned_require_qty > actual_issue_qty
    ORDER BY (planned_require_qty - actual_issue_qty) DESC
    """

    rows = p.sql.query(sql) or []
    data = []
    for row in rows:
        planned = float(row.get("planned_require_qty") or 0)
        issued = float(row.get("actual_issue_qty") or 0)
        shortage = max(planned - issued, 0)
        data.append({
            "component_product_code": str(row.get("component_product_code") or ""),
            "component_product_name": str(row.get("component_product_name") or ""),
            "planned_require_qty": round(planned, 2),
            "actual_issue_qty": round(issued, 2),
            "shortage_qty": round(shortage, 2),
            "issue_rate": round(issued / planned, 4) if planned > 0 else 0.0,
            "kit_status": str(row.get("kit_status") or ""),
            "is_critical": int(row.get("is_critical") or 0),
        })

    return p.function_result(
        columns=[
            "component_product_code", "component_product_name",
            "planned_require_qty", "actual_issue_qty", "shortage_qty",
            "issue_rate", "kit_status", "is_critical",
        ],
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
