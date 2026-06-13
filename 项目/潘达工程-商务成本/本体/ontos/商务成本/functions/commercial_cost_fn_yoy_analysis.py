# 商务成本同比分析函数

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
        d.year as year,
        d.month as month,
        d.year_month as period,
        SUM(c.cost_amount) as cost_amount
    FROM fact_project_cost c
    JOIN dim_project p ON c.project_key = p.project_key
    JOIN dim_date d ON c.date_key = d.date_key
    WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
        AND {filter_str}
    GROUP BY d.year, d.month, d.year_month
    ORDER BY d.year, d.month
    """
    
    cost_results = p.sql.query(cost_sql)
    
    output_sql = f"""
    SELECT 
        d.year as year,
        d.month as month,
        d.year_month as period,
        SUM(o.output_amount) as output_amount
    FROM fact_project_output o
    JOIN dim_project p ON o.project_key = p.project_key
    JOIN dim_date d ON o.date_key = d.date_key
    WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
        AND {filter_str}
    GROUP BY d.year, d.month, d.year_month
    ORDER BY d.year, d.month
    """
    
    output_results = p.sql.query(output_sql)
    
    cost_dict = {(r["year"], r["month"]): float(r.get("cost_amount", 0) or 0) for r in cost_results}
    output_dict = {(r["year"], r["month"]): float(r.get("output_amount", 0) or 0) for r in output_results}
    
    result = []
    
    for (year, month), cost in cost_dict.items():
        period = f"{year}-{str(month).zfill(2)}"
        output = output_dict.get((year, month), 0)
        
        prev_year_cost = cost_dict.get((year - 1, month), 0)
        prev_year_output = output_dict.get((year - 1, month), 0)
        
        cost_yoy = (cost - prev_year_cost) / prev_year_cost * 100 if prev_year_cost else 0
        output_yoy = (output - prev_year_output) / prev_year_output * 100 if prev_year_output else 0
        
        result.append({
            "year": year,
            "month": month,
            "period": period,
            "cost_amount": cost,
            "cost_yoy": round(cost_yoy, 2),
            "output_amount": output,
            "output_yoy": round(output_yoy, 2),
            "profit": output - cost,
        })
    
    result.sort(key=lambda x: (x["year"], x["month"]))
    
    if result:
        columns = list(result[0].keys())
        data = [list(row.values()) for row in result]
    else:
        columns = ["year", "month", "period", "cost_amount", "cost_yoy", "output_amount", "output_yoy", "profit"]
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