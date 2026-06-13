"""本体引擎测试 — 成本极值与差值 onto_engine.fn.cost_extremes

参数：start_date, end_date, region（可选）
返回：extreme_type, rank_no, project_id, project_name, region, total_cost, cost_gap

锚点问句：「本月成本中，排最前和最后的是哪两个，中间的差值有多大」

发布：
  dazi-onto script publish 项目/DAZI_TEST/本体/ontos/引擎测试/functions/onto_engine_fn_cost_extremes.py \\
    --space space__onto_engine_test --register-function-id onto_engine.fn.cost_extremes \\
    --register-platform-category 结构分析
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2026-06-01", "end_date": "2026-06-30"},
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
    start_date = params.get("start_date", "2026-06-01")
    end_date = params.get("end_date", "2026-06-30")
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
    """
    rows = p.sql.query(sql)
    if not rows:
        return p.function_result(
            columns=[
                "extreme_type",
                "rank_no",
                "project_id",
                "project_name",
                "region",
                "total_cost",
                "cost_gap",
            ],
            data=[],
            row_count=0,
        )

    ranked = []
    for i, row in enumerate(rows, start=1):
        ranked.append({
            "rank_no": i,
            "project_id": row.get("project_id", ""),
            "project_name": row.get("project_name", ""),
            "region": row.get("region", ""),
            "total_cost": round(float(row.get("total_cost") or 0), 2),
        })

    top = ranked[0]
    bottom = ranked[-1] if len(ranked) > 1 else ranked[0]
    cost_gap = round(top["total_cost"] - bottom["total_cost"], 2)

    data = [
        {**top, "extreme_type": "最高", "cost_gap": cost_gap},
        {**bottom, "extreme_type": "最低", "cost_gap": cost_gap},
    ]

    return p.function_result(
        columns=[
            "extreme_type",
            "rank_no",
            "project_id",
            "project_name",
            "region",
            "total_cost",
            "cost_gap",
        ],
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
