# 商务成本总览分析函数

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2024-01-01",
        "end_date": "2026-06-30",
        "project_key": None,
        "region_key": None,
        "organization_key": None,
    },
    "object_type_code": "Project",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    
    start_date = params.get("start_date", "2024-01-01")
    end_date = params.get("end_date", "2026-06-30")
    project_key = params.get("project_key")
    region_key = params.get("region_key")
    organization_key = params.get("organization_key")
    
    filters = []
    if project_key:
        filters.append(f"p.project_key = '{project_key}'")
    if region_key:
        filters.append(f"p.region_key = '{region_key}'")
    if organization_key:
        filters.append(f"p.organization_key = '{organization_key}'")
    
    filter_str = " AND ".join(filters) if filters else "1=1"
    
    cost_sql = f"""
    SELECT 
        SUM(c.cost_amount) as total_cost,
        COUNT(DISTINCT c.project_key) as project_count
    FROM fact_project_cost c
    JOIN dim_project p ON c.project_key = p.project_key
    JOIN dim_date d ON c.date_key = d.date_key
    WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
        AND {filter_str}
    """
    cost_result = p.sql.query_one(cost_sql)
    
    output_sql = f"""
    SELECT 
        SUM(o.output_amount) as total_output,
        SUM(CASE WHEN o.confirmation_status = '已确认' THEN o.output_amount ELSE 0 END) as confirmed_output
    FROM fact_project_output o
    JOIN dim_project p ON o.project_key = p.project_key
    JOIN dim_date d ON o.date_key = d.date_key
    WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
        AND {filter_str}
    """
    output_result = p.sql.query_one(output_sql)
    
    payment_sql = f"""
    SELECT 
        SUM(p.payment_amount) as total_payment
    FROM fact_payment p
    JOIN dim_project pr ON p.project_key = pr.project_key
    JOIN dim_date d ON p.date_key = d.date_key
    WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
        AND {filter_str}
    """
    payment_result = p.sql.query_one(payment_sql)
    
    receivable_sql = f"""
    SELECT 
        SUM(r.receivable_amount) as total_receivable,
        SUM(r.received_amount) as total_received,
        SUM(r.outstanding_amount) as total_outstanding
    FROM fact_receivable r
    JOIN dim_project p ON r.project_key = p.project_key
    JOIN dim_date d ON r.date_key = d.date_key
    WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
        AND {filter_str}
    """
    receivable_result = p.sql.query_one(receivable_sql)
    
    risk_sql = f"""
    SELECT 
        COUNT(*) as risk_count,
        AVG(r.risk_value) as avg_risk_value,
        SUM(CASE WHEN r.risk_level_key = 'RL001' THEN 1 ELSE 0 END) as high_risk_count,
        SUM(CASE WHEN r.risk_level_key = 'RL002' THEN 1 ELSE 0 END) as medium_risk_count,
        SUM(CASE WHEN r.risk_level_key = 'RL003' THEN 1 ELSE 0 END) as low_risk_count
    FROM fact_risk r
    JOIN dim_project p ON r.project_key = p.project_key
    JOIN dim_date d ON r.date_key = d.date_key
    WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
        AND {filter_str}
    """
    risk_result = p.sql.query_one(risk_sql)
    
    total_cost = float(cost_result.get("total_cost", 0) or 0)
    total_output = float(output_result.get("total_output", 0) or 0)
    profit = total_output - total_cost
    profit_rate = (profit / total_output * 100) if total_output > 0 else 0
    
    total_receivable = float(receivable_result.get("total_receivable", 0) or 0)
    total_received = float(receivable_result.get("total_received", 0) or 0)
    collection_rate = (total_received / total_receivable * 100) if total_receivable > 0 else 0
    
    data = [{
        "period": f"{start_date} 至 {end_date}",
        "project_count": int(cost_result.get("project_count", 0) or 0),
        "total_cost": total_cost,
        "total_output": total_output,
        "confirmed_output": float(output_result.get("confirmed_output", 0) or 0),
        "confirmation_rate": round(((output_result.get("confirmed_output", 0) or 0) / total_output * 100) if total_output > 0 else 0, 2),
        "profit_amount": profit,
        "profit_rate": round(profit_rate, 2),
        "total_payment": float(payment_result.get("total_payment", 0) or 0),
        "total_receivable": total_receivable,
        "total_received": total_received,
        "total_outstanding": float(receivable_result.get("total_outstanding", 0) or 0),
        "collection_rate": round(collection_rate, 2),
        "risk_count": int(risk_result.get("risk_count", 0) or 0),
        "avg_risk_value": round(float(risk_result.get("avg_risk_value", 0) or 0), 2),
        "high_risk_count": int(risk_result.get("high_risk_count", 0) or 0),
        "medium_risk_count": int(risk_result.get("medium_risk_count", 0) or 0),
        "low_risk_count": int(risk_result.get("low_risk_count", 0) or 0),
    }]
    
    columns = list(data[0].keys())
    
    return p.function_result(
        columns=columns,
        data=[list(row.values()) for row in data],
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