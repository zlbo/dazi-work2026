# 商务成本计划vs实际分析函数

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
        p.project_key,
        p.project_code,
        p.project_name,
        ct.cost_type_key,
        ct.cost_type_code,
        ct.cost_type_name,
        SUM(CASE WHEN c.cost_source = '计划' THEN c.cost_amount ELSE 0 END) as plan_cost,
        SUM(CASE WHEN c.cost_source = '实际' THEN c.cost_amount ELSE 0 END) as actual_cost,
        COUNT(DISTINCT CASE WHEN c.cost_source = '实际' THEN c.project_key END) as actual_project_count
    FROM fact_project_cost c
    JOIN dim_project p ON c.project_key = p.project_key
    JOIN dim_cost_type ct ON c.cost_type_key = ct.cost_type_key
    JOIN dim_date d ON c.date_key = d.date_key
    WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
        AND {filter_str}
    GROUP BY p.project_key, p.project_code, p.project_name, ct.cost_type_key, ct.cost_type_code, ct.cost_type_name
    ORDER BY p.project_code, ct.cost_type_code
    """
    
    results = p.sql.query(sql)
    
    plan_vs_actual = []
    total_plan = 0
    total_actual = 0
    
    for row in results:
        plan_cost = float(row.get("plan_cost", 0) or 0)
        actual_cost = float(row.get("actual_cost", 0) or 0)
        variance = actual_cost - plan_cost
        variance_rate = (variance / plan_cost * 100) if plan_cost > 0 else 0
        
        total_plan += plan_cost
        total_actual += actual_cost
        
        plan_vs_actual.append({
            "project_key": row["project_key"],
            "project_code": row["project_code"],
            "project_name": row["project_name"],
            "cost_type_key": row["cost_type_key"],
            "cost_type_code": row["cost_type_code"],
            "cost_type_name": row["cost_type_name"],
            "plan_cost": plan_cost,
            "actual_cost": actual_cost,
            "variance": variance,
            "variance_rate": round(variance_rate, 2),
        })
    
    if plan_vs_actual:
        columns = list(plan_vs_actual[0].keys())
        data = [list(row.values()) for row in plan_vs_actual]
    else:
        columns = ["project_key", "project_code", "project_name", "cost_type_key", "cost_type_code", "cost_type_name", "plan_cost", "actual_cost", "variance", "variance_rate"]
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