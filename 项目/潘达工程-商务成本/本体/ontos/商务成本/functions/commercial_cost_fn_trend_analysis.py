# 商务成本趋势分析函数

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2024-01-01",
        "end_date": "2026-06-30",
        "indicator_type": "cost",
        "project_key": None,
    },
    "object_type_code": "Project",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    
    start_date = params.get("start_date", "2024-01-01")
    end_date = params.get("end_date", "2026-06-30")
    indicator_type = params.get("indicator_type", "cost")
    project_key = params.get("project_key")
    
    filter_str = f"AND p.project_key = '{project_key}'" if project_key else ""
    
    if indicator_type == "cost":
        sql = f"""
        SELECT 
            d.year_month as period,
            SUM(c.cost_amount) as value,
            COUNT(DISTINCT c.project_key) as project_count
        FROM fact_project_cost c
        JOIN dim_project p ON c.project_key = p.project_key
        JOIN dim_date d ON c.date_key = d.date_key
        WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
            {filter_str}
        GROUP BY d.year_month
        ORDER BY d.year_month
        """
    elif indicator_type == "output":
        sql = f"""
        SELECT 
            d.year_month as period,
            SUM(o.output_amount) as value,
            COUNT(DISTINCT o.project_key) as project_count
        FROM fact_project_output o
        JOIN dim_project p ON o.project_key = p.project_key
        JOIN dim_date d ON o.date_key = d.date_key
        WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
            {filter_str}
        GROUP BY d.year_month
        ORDER BY d.year_month
        """
    elif indicator_type == "profit":
        sql = f"""
        SELECT 
            d.year_month as period,
            SUM(o.output_amount) - SUM(c.cost_amount) as value,
            COUNT(DISTINCT p.project_key) as project_count
        FROM dim_project p
        LEFT JOIN fact_project_output o ON p.project_key = o.project_key
        LEFT JOIN fact_project_cost c ON p.project_key = c.project_key
        LEFT JOIN dim_date d ON o.date_key = d.date_key
        WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
            {filter_str}
        GROUP BY d.year_month
        ORDER BY d.year_month
        """
    elif indicator_type == "receivable":
        sql = f"""
        SELECT 
            d.year_month as period,
            SUM(r.outstanding_amount) as value,
            COUNT(DISTINCT r.project_key) as project_count
        FROM fact_receivable r
        JOIN dim_project p ON r.project_key = p.project_key
        JOIN dim_date d ON r.date_key = d.date_key
        WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
            {filter_str}
        GROUP BY d.year_month
        ORDER BY d.year_month
        """
    else:
        return p.function_result(
            columns=["error"],
            data=[{"error": "Unknown indicator_type"}],
            row_count=1,
        )
    
    results = p.sql.query(sql)
    
    trend_data = []
    prev_value = None
    for row in results:
        value = float(row.get("value", 0) or 0)
        change = (value - prev_value) / prev_value * 100 if prev_value else 0
        trend_data.append({
            "period": row["period"],
            "value": value,
            "project_count": int(row.get("project_count", 0) or 0),
            "change_rate": round(change, 2),
        })
        prev_value = value
    
    if trend_data:
        columns = list(trend_data[0].keys())
        data = [list(row.values()) for row in trend_data]
    else:
        columns = ["period", "value", "project_count", "change_rate"]
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