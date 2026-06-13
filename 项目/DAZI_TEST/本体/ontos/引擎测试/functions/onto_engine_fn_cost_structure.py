"""本体引擎测试 — 成本科目结构 onto_engine.fn.cost_structure

参数：start_date, end_date, project_id（可选）, parent_cost_type_id（可选，大类过滤）
返回：cost_type_id, cost_type_name, parent_cost_type_name, total_cost, cost_share

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/引擎测试/functions/onto_engine_fn_cost_structure.py \\
    --space space__onto_engine_test --register-function-id onto_engine.fn.cost_structure \\
    --register-platform-category 结构分析
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30"},
    "object_type_code": "CostRecord",
}


def _date_clause(start_date, end_date):
    if not start_date or not end_date:
        return ""
    lo = int(str(start_date).replace("-", "")[:8])
    hi = int(str(end_date).replace("-", "")[:8])
    return f" AND f.date_key >= {lo} AND f.date_key <= {hi}"


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", "2026-06-30")
    project_id = (params.get("project_id") or "").strip() or None
    parent_type = (params.get("parent_cost_type_id") or "").strip() or None
    dc = _date_clause(start_date, end_date)
    proj_cond = f" AND f.project_id = '{project_id}'" if project_id else ""
    parent_cond = f" AND f.parent_cost_type_id = '{parent_type}'" if parent_type else ""

    sql = f"""
        WITH base AS (
            SELECT
                f.cost_type_id,
                any(f.cost_type_name) AS cost_type_name,
                any(f.parent_cost_type_id) AS parent_cost_type_id,
                sum(f.cost_amount) AS total_cost
            FROM fact_cost f
            WHERE 1=1 {dc} {proj_cond} {parent_cond}
            GROUP BY f.cost_type_id
        ),
        tot AS (SELECT sum(total_cost) AS grand FROM base)
        SELECT
            b.cost_type_id,
            b.cost_type_name,
            coalesce(p.cost_type_name, '') AS parent_cost_type_name,
            b.total_cost,
            if(t.grand > 0, b.total_cost / t.grand, 0) AS cost_share
        FROM base b
        LEFT JOIN dim_cost_type p ON b.parent_cost_type_id = p.cost_type_id
        CROSS JOIN tot t
        ORDER BY b.total_cost DESC
    """
    rows = p.sql.query(sql)
    data = []
    for row in rows:
        data.append({
            "cost_type_id": row.get("cost_type_id", ""),
            "cost_type_name": row.get("cost_type_name", ""),
            "parent_cost_type_name": row.get("parent_cost_type_name", ""),
            "total_cost": round(float(row.get("total_cost") or 0), 2),
            "cost_share": round(float(row.get("cost_share") or 0), 4),
        })
    return p.function_result(
        columns=["cost_type_id", "cost_type_name", "parent_cost_type_name", "total_cost", "cost_share"],
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
