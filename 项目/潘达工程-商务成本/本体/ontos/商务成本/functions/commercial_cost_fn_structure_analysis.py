# 商务成本结构分析函数

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2024-01-01",
        "end_date": "2026-06-30",
        "project_key": None,
        "cost_type_key": None,
    },
    "object_type_code": "Project",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    
    start_date = params.get("start_date", "2024-01-01")
    end_date = params.get("end_date", "2026-06-30")
    project_key = params.get("project_key")
    cost_type_key = params.get("cost_type_key")
    
    filters = []
    if project_key:
        filters.append(f"p.project_key = '{project_key}'")
    if cost_type_key:
        filters.append(f"ct.cost_type_key = '{cost_type_key}'")
    filter_str = " AND ".join(filters) if filters else "1=1"
    
    sql = f"""
    SELECT 
        ct.cost_type_key,
        ct.cost_type_code,
        ct.cost_type_name,
        ct.cost_category,
        SUM(c.cost_amount) as total_cost,
        COUNT(DISTINCT c.project_key) as project_count
    FROM fact_project_cost c
    JOIN dim_project p ON c.project_key = p.project_key
    JOIN dim_cost_type ct ON c.cost_type_key = ct.cost_type_key
    JOIN dim_date d ON c.date_key = d.date_key
    WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
        AND {filter_str}
    GROUP BY ct.cost_type_key, ct.cost_type_code, ct.cost_type_name, ct.cost_category
    ORDER BY total_cost DESC
    """
    
    results = p.sql.query(sql)
    
    category_summary = {}
    total_all = 0
    
    for row in results:
        total_cost = float(row.get("total_cost", 0) or 0)
        total_all += total_cost
        category = row.get("cost_category", "其他")
        
        if category not in category_summary:
            category_summary[category] = {
                "total_cost": 0,
                "count": 0,
            }
        category_summary[category]["total_cost"] += total_cost
        category_summary[category]["count"] += 1
    
    cost_structure = []
    for row in results:
        total_cost = float(row.get("total_cost", 0) or 0)
        cost_structure.append({
            "cost_type_key": row["cost_type_key"],
            "cost_type_code": row["cost_type_code"],
            "cost_type_name": row["cost_type_name"],
            "cost_category": row.get("cost_category", "其他"),
            "total_cost": total_cost,
            "proportion": round(total_cost / total_all * 100, 2) if total_all > 0 else 0,
            "project_count": int(row.get("project_count", 0) or 0),
        })
    
    category_list = []
    for category, data in category_summary.items():
        category_list.append({
            "cost_category": category,
            "total_cost": data["total_cost"],
            "proportion": round(data["total_cost"] / total_all * 100, 2) if total_all > 0 else 0,
            "type_count": data["count"],
        })
    
    if cost_structure:
        columns = list(cost_structure[0].keys())
        data = [list(row.values()) for row in cost_structure]
    else:
        columns = ["cost_type_key", "cost_type_code", "cost_type_name", "cost_category", "total_cost", "proportion", "project_count"]
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