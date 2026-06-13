# 商务成本构成分析函数

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2024-01-01",
        "end_date": "2026-06-30",
        "project_key": None,
    },
    "object_type_code": "Project",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    
    start_date = params.get("start_date", "2024-01-01")
    end_date = params.get("end_date", "2026-06-30")
    project_key = params.get("project_key")
    
    filter_str = f"AND p.project_key = '{project_key}'" if project_key else ""
    
    sql = f"""
    SELECT 
        c.cost_item_key,
        ci.cost_item_code,
        ci.cost_item_name,
        ci.cost_item_level,
        ci.parent_cost_item_key,
        ct.cost_type_name,
        SUM(c.cost_amount) as total_cost,
        COUNT(DISTINCT c.project_key) as project_count
    FROM fact_project_cost c
    JOIN dim_project p ON c.project_key = p.project_key
    JOIN dim_cost_item ci ON c.cost_item_key = ci.cost_item_key
    JOIN dim_cost_type ct ON ci.cost_type_key = ct.cost_type_key
    JOIN dim_date d ON c.date_key = d.date_key
    WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
        {filter_str}
    GROUP BY c.cost_item_key, ci.cost_item_code, ci.cost_item_name, ci.cost_item_level, ci.parent_cost_item_key, ct.cost_type_name
    ORDER BY ci.cost_item_level, ci.cost_item_code
    """
    
    results = p.sql.query(sql)
    
    total_all = sum(float(row.get("total_cost", 0) or 0) for row in results)
    
    cost_items = []
    for row in results:
        total_cost = float(row.get("total_cost", 0) or 0)
        cost_items.append({
            "cost_item_key": row["cost_item_key"],
            "cost_item_code": row["cost_item_code"],
            "cost_item_name": row["cost_item_name"],
            "cost_item_level": int(row.get("cost_item_level", 1) or 1),
            "parent_cost_item_key": row.get("parent_cost_item_key"),
            "cost_type_name": row["cost_type_name"],
            "total_cost": total_cost,
            "proportion": round(total_cost / total_all * 100, 2) if total_all > 0 else 0,
            "project_count": int(row.get("project_count", 0) or 0),
        })
    
    level_summary = {}
    for item in cost_items:
        level = item["cost_item_level"]
        if level not in level_summary:
            level_summary[level] = {
                "total_cost": 0,
                "item_count": 0,
            }
        level_summary[level]["total_cost"] += item["total_cost"]
        level_summary[level]["item_count"] += 1
    
    if cost_items:
        columns = list(cost_items[0].keys())
        data = [list(row.values()) for row in cost_items]
    else:
        columns = ["cost_item_key", "cost_item_code", "cost_item_name", "cost_item_level", "parent_cost_item_key", "cost_type_name", "total_cost", "proportion", "project_count"]
        data = []
    
    return p.function_result(
        columns=columns,
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