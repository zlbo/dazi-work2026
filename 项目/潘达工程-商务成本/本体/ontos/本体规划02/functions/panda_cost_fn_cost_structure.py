"""成本结构（人工 / 材料 / 设备） panda_cost.fn.cost_structure

参数：report_period, project_id（可选）
返回：project_id, project_name, cost_confirmed_acc, labor_cost_acc, material_cost_acc,
      equipment_cost_acc, labor_ratio, material_ratio, equipment_ratio, report_period

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划02/functions/panda_cost_fn_cost_structure.py \
    --space space__panda_construction --register-function-id panda_cost.fn.cost_structure
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"report_period": "2025-06"},
    "object_type_code": "CostManagementAnalysis",
}


def _build_where(report_period, project_id=None):
    clauses = []
    if report_period:
        clauses.append(f"c.report_period = '{report_period}'")
    if project_id:
        clauses.append(f"c.project_id = '{project_id}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    report_period = params.get("report_period", "")
    project_id = params.get("project_id") or None
    where_clause = _build_where(report_period, project_id)

    sql = f"""
    SELECT
        c.project_id,
        any(c.project_name) AS project_name,
        sum(c.cost_confirmed_acc) AS cost_confirmed_acc,
        sum(c.labor_cost_acc) AS labor_cost_acc,
        sum(c.material_cost_acc) AS material_cost_acc,
        sum(c.equipment_cost_acc) AS equipment_cost_acc
    FROM fact_project_cost c
    {where_clause}
    GROUP BY c.project_id
    ORDER BY cost_confirmed_acc DESC
    """

    rows = p.sql.query(sql)
    data = []
    for row in rows:
        cost_total = float(row.get("cost_confirmed_acc") or 0)
        labor = float(row.get("labor_cost_acc") or 0)
        material = float(row.get("material_cost_acc") or 0)
        equipment = float(row.get("equipment_cost_acc") or 0)
        data.append({
            "project_id": str(row.get("project_id") or ""),
            "project_name": str(row.get("project_name") or ""),
            "cost_confirmed_acc": round(cost_total, 2),
            "labor_cost_acc": round(labor, 2),
            "material_cost_acc": round(material, 2),
            "equipment_cost_acc": round(equipment, 2),
            "labor_ratio": round(labor / cost_total, 4) if cost_total > 0 else 0.0,
            "material_ratio": round(material / cost_total, 4) if cost_total > 0 else 0.0,
            "equipment_ratio": round(equipment / cost_total, 4) if cost_total > 0 else 0.0,
            "report_period": report_period,
        })

    return p.function_result(
        columns=["project_id", "project_name", "cost_confirmed_acc", "labor_cost_acc",
                 "material_cost_acc", "equipment_cost_acc", "labor_ratio",
                 "material_ratio", "equipment_ratio", "report_period"],
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
