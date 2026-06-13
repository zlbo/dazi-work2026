"""本体引擎测试 — 成本 Top-N 项目 onto_engine.fn.top_cost_projects

参数：start_date, end_date, limit（默认 5）, region（可选）
返回：rank_no, project_id, project_name, region, total_cost

与决策规则 rank_cost_topn 互补。

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/引擎测试/functions/onto_engine_fn_top_cost_projects.py \\
    --space space__onto_engine_test --register-function-id onto_engine.fn.top_cost_projects \\
    --register-platform-category 排名分析
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30", "limit": 5},
    "object_type_code": "Project",
}


def _date_clause(start_date, end_date):
    if not start_date or not end_date:
        return ""
    lo = int(str(start_date).replace("-", "")[:8])
    hi = int(str(end_date).replace("-", "")[:8])
    return f" AND date_key >= {lo} AND date_key <= {hi}"


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", "2026-06-30")
    limit = int(params.get("limit") or 5)
    region = (params.get("region") or "").strip() or None
    dc = _date_clause(start_date, end_date)
    region_cond = f" AND region = '{region}'" if region else ""

    sql = f"""
        SELECT
            project_id,
            any(project_name) AS project_name,
            any(region) AS region,
            sum(cost_amount) AS total_cost
        FROM fact_cost
        WHERE 1=1 {dc} {region_cond}
        GROUP BY project_id
        ORDER BY total_cost DESC
        LIMIT {max(1, min(limit, 50))}
    """
    rows = p.sql.query(sql)
    data = []
    for i, row in enumerate(rows, start=1):
        data.append({
            "rank_no": i,
            "project_id": row.get("project_id", ""),
            "project_name": row.get("project_name", ""),
            "region": row.get("region", ""),
            "total_cost": round(float(row.get("total_cost") or 0), 2),
        })
    return p.function_result(
        columns=["rank_no", "project_id", "project_name", "region", "total_cost"],
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
