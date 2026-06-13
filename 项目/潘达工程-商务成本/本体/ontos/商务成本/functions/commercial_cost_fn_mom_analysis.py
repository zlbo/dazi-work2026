# 商务成本环比分析函数

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2024-01-01",
        "end_date": "2026-06-30",
        "project_key": None,
        "region_key": None,
    },
    "object_type_code": "Project",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    
    start_date = params.get("start_date", "2024-01-01")
    end_date = params.get("end_date", "2026-06-30")
    project_key = params.get("project_key")
    region_key = params.get("region_key")
    
    filters = []
    if project_key:
        filters.append(f"p.project_key = '{project_key}'")
    if region_key:
        filters.append(f"p.region_key = '{region_key}'")
    filter_str = " AND ".join(filters) if filters else "1=1"
    
    cost_sql = f"""
    SELECT 
        d.year_month as period,
        SUM(c.cost_amount) as cost_amount
    FROM fact_project_cost c
    JOIN dim_project p ON c.project_key = p.project_key
    JOIN dim_date d ON c.date_key = d.date_key
    WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
        AND {filter_str}
    GROUP BY d.year_month
    ORDER BY d.year_month
    """
    
    cost_results = p.sql.query(cost_sql)
    
    output_sql = f"""
    SELECT 
        d.year_month as period,
        SUM(o.output_amount) as output_amount
    FROM fact_project_output o
    JOIN dim_project p ON o.project_key = p.project_key
    JOIN dim_date d ON o.date_key = d.date_key
    WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
        AND {filter_str}
    GROUP BY d.year_month
    ORDER BY d.year_month
    """
    
    output_results = p.sql.query(output_sql)
    
    cost_dict = {r["period"]: float(r.get("cost_amount", 0) or 0) for r in cost_results}
    output_dict = {r["period"]: float(r.get("output_amount", 0) or 0) for r in output_results}
    
    periods = sorted(set(list(cost_dict.keys()) + list(output_dict.keys())))
    
    result = []
    prev_cost = None
    prev_output = None
    
    for period in periods:
        cost = cost_dict.get(period, 0)
        output = output_dict.get(period, 0)
        
        cost_mom = (cost - prev_cost) / prev_cost * 100 if prev_cost else 0
        output_mom = (output - prev_output) / prev_output * 100 if prev_output else 0
        
        result.append({
            "period": period,
            "cost_amount": cost,
            "cost_mom": round(cost_mom, 2),
            "output_amount": output,
            "output_mom": round(output_mom, 2),
            "profit": output - cost,
        })
        
        prev_cost = cost
        prev_output = output
    
    if result:
        columns = list(result[0].keys())
        data = [list(row.values()) for row in result]
    else:
        columns = ["period", "cost_amount", "cost_mom", "output_amount", "output_mom", "profit"]
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