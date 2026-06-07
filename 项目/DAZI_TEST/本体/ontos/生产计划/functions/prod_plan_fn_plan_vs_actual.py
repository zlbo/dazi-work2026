"""MPS 计划 vs 日实绩 prod_plan.fn.plan_vs_actual

参数：start_date, end_date, plan_version_id（可选）, group_by=product|work_center|plant|category
发布：dazi onto script publish .../functions/prod_plan_fn_plan_vs_actual.py \
  --space space_cate_test01 --register-function-id prod_plan.fn.plan_vs_actual
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2026-01-01",
        "end_date": "2026-06-30",
        "group_by": "work_center",
        "plan_version_id": "MPS-2026-06",
    },
    "object_type_code": "PlanAnalysis",
}

_GROUP_MAP = {
    "product": ("product_id", "product_name"),
    "work_center": ("work_center_id", "work_center_name"),
    "plant": ("plant_id", "plant_name"),
    "category": ("product_category", "product_category"),
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    plan_version_id = params.get("plan_version_id") or None
    group_by = params.get("group_by", "work_center")
    gid_col, gname_col = _GROUP_MAP.get(group_by, _GROUP_MAP["work_center"])

    version_cond = ""
    if plan_version_id:
        version_cond = f" AND p.plan_version_code = '{plan_version_id}'"

    sql = f"""
    SELECT
        p.{gid_col} AS group_id,
        any(p.{gname_col}) AS group_name,
        sum(p.planned_qty) AS planned_qty,
        sum(p.planned_hours) AS planned_hours,
        sum(d.actual_qty) AS actual_qty,
        sum(d.actual_hours) AS actual_hours
    FROM fact_production_plan AS p
    LEFT JOIN fact_production_daily AS d
        ON p.work_center_id = d.work_center_id
        AND p.product_id = d.product_id
        AND d.calendar_date >= '{start_date}'
        AND d.calendar_date <= '{end_date}'
    WHERE p.fiscal_year = 2026 AND p.fiscal_month = 6
        {version_cond}
    GROUP BY p.{gid_col}
    ORDER BY planned_qty DESC
    """

    rows = p.sql.query(sql) or []
    data = []
    for row in rows:
        planned_qty = float(row.get("planned_qty") or 0)
        actual_qty = float(row.get("actual_qty") or 0)
        planned_hours = float(row.get("planned_hours") or 0)
        actual_hours = float(row.get("actual_hours") or 0)
        data.append({
            "group_id": str(row.get("group_id") or ""),
            "group_name": str(row.get("group_name") or ""),
            "planned_qty": round(planned_qty, 2),
            "actual_qty": round(actual_qty, 2),
            "qty_variance": round(actual_qty - planned_qty, 2),
            "achievement_rate": round(actual_qty / planned_qty, 4) if planned_qty > 0 else 0.0,
            "planned_hours": round(planned_hours, 2),
            "actual_hours": round(actual_hours, 2),
        })

    return p.function_result(
        columns=[
            "group_id", "group_name", "planned_qty", "actual_qty",
            "qty_variance", "achievement_rate", "planned_hours", "actual_hours",
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
