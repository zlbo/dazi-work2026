"""运行计划对比 equip_ops.fn.plan_vs_actual

参数：fiscal_year, fiscal_month, plan_version, plant_id（可选）
JOIN fact_equipment_plan 与 fact_equipment_daily_ops
返回：planned vs actual runtime/output/energy, execution_rate

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/设备运营/functions/equip_ops_fn_plan_vs_actual.py \
    --space space_cate_test01 --register-function-id equip_ops.fn.plan_vs_actual
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "fiscal_year": 2026,
        "fiscal_month": 6,
        "plan_version": "2026月度计划",
    },
    "object_type_code": "PlanAnalysis",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    fiscal_year = int(params.get("fiscal_year", 2026))
    fiscal_month = int(params.get("fiscal_month", 1))
    plan_version = params.get("plan_version", "2026月度计划")
    plant_id = params.get("plant_id") or None

    plant_cond = "" if not plant_id else f"AND p.plant_id = '{plant_id}'"

    sql = f"""
    SELECT
        sum(p.planned_runtime_min) AS planned_runtime_min,
        sum(p.planned_output_qty) AS planned_output_qty,
        sum(p.planned_energy) AS planned_energy,
        sum(o.runtime_min) AS actual_runtime_min,
        sum(o.actual_output_qty) AS actual_output_qty,
        sum(o.energy_consumption) AS actual_energy
    FROM fact_equipment_plan AS p
    LEFT JOIN fact_equipment_daily_ops AS o
        ON p.equipment_id = o.equipment_id AND p.date_key = o.date_key
    WHERE p.fiscal_year = {fiscal_year}
        AND p.fiscal_month = {fiscal_month}
        AND p.plan_version = '{plan_version}'
        {plant_cond}
    """

    rows = p.sql.query(sql)
    row = rows[0] if rows else {}

    planned_runtime = float(row.get("planned_runtime_min") or 0)
    planned_output = float(row.get("planned_output_qty") or 0)
    planned_energy = float(row.get("planned_energy") or 0)
    actual_runtime = float(row.get("actual_runtime_min") or 0)
    actual_output = float(row.get("actual_output_qty") or 0)
    actual_energy = float(row.get("actual_energy") or 0)

    runtime_rate = actual_runtime / planned_runtime if planned_runtime > 0 else 0.0
    output_rate = actual_output / planned_output if planned_output > 0 else 0.0
    energy_rate = actual_energy / planned_energy if planned_energy > 0 else 0.0
    execution_rate = (runtime_rate + output_rate + energy_rate) / 3.0

    data = [{
        "fiscal_year": fiscal_year,
        "fiscal_month": fiscal_month,
        "plan_version": plan_version,
        "planned_runtime_hours": round(planned_runtime / 60.0, 2),
        "actual_runtime_hours": round(actual_runtime / 60.0, 2),
        "runtime_execution_rate": round(runtime_rate, 4),
        "planned_output_qty": round(planned_output, 2),
        "actual_output_qty": round(actual_output, 2),
        "output_execution_rate": round(output_rate, 4),
        "planned_energy": round(planned_energy, 2),
        "actual_energy": round(actual_energy, 2),
        "energy_execution_rate": round(energy_rate, 4),
        "execution_rate": round(execution_rate, 4),
    }]

    return p.function_result(
        columns=[
            "fiscal_year", "fiscal_month", "plan_version",
            "planned_runtime_hours", "actual_runtime_hours", "runtime_execution_rate",
            "planned_output_qty", "actual_output_qty", "output_execution_rate",
            "planned_energy", "actual_energy", "energy_execution_rate",
            "execution_rate",
        ],
        data=data,
        row_count=1,
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
