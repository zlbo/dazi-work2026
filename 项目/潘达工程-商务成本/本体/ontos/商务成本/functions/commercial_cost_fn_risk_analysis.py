# 商务成本风险分析函数

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2024-01-01",
        "end_date": "2026-06-30",
        "risk_level": None,
        "project_key": None,
        "region_key": None,
    },
    "object_type_code": "Project",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    
    start_date = params.get("start_date", "2024-01-01")
    end_date = params.get("end_date", "2026-06-30")
    risk_level = params.get("risk_level")
    project_key = params.get("project_key")
    region_key = params.get("region_key")
    
    filters = []
    if project_key:
        filters.append(f"p.project_key = '{project_key}'")
    if region_key:
        filters.append(f"p.region_key = '{region_key}'")
    if risk_level:
        risk_level_key_map = {"G": "RL001", "Z": "RL002", "D": "RL003"}
        filters.append(f"risk.risk_level_key = '{risk_level_key_map.get(risk_level, risk_level)}'")
    
    filter_str = " AND ".join(filters) if filters else "1=1"
    
    risk_sql = f"""
    SELECT 
        risk.risk_id,
        risk.risk_type,
        risk.risk_value,
        rl.risk_level_name,
        p.project_key,
        p.project_code,
        p.project_name,
        p.contract_amount,
        r.region_name,
        org.organization_name,
        risk.calendar_date as risk_date
    FROM fact_risk risk
    JOIN dim_project p ON risk.project_key = p.project_key
    JOIN dim_risk_level rl ON risk.risk_level_key = rl.risk_level_key
    JOIN dim_region r ON p.region_key = r.region_key
    JOIN dim_organization org ON p.organization_key = org.organization_key
    JOIN dim_date d ON risk.date_key = d.date_key
    WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
        AND {filter_str}
    ORDER BY risk.risk_value DESC
    """
    
    risk_results = p.sql.query(risk_sql)
    
    summary_sql = f"""
    SELECT 
        COUNT(DISTINCT risk.project_key) as risk_project_count,
        COUNT(*) as risk_count,
        AVG(risk.risk_value) as avg_risk_value,
        MAX(risk.risk_value) as max_risk_value,
        MIN(risk.risk_value) as min_risk_value,
        SUM(CASE WHEN risk.risk_level_key = 'RL001' THEN 1 ELSE 0 END) as high_risk_count,
        SUM(CASE WHEN risk.risk_level_key = 'RL002' THEN 1 ELSE 0 END) as medium_risk_count,
        SUM(CASE WHEN risk.risk_level_key = 'RL003' THEN 1 ELSE 0 END) as low_risk_count
    FROM fact_risk risk
    JOIN dim_project p ON risk.project_key = p.project_key
    JOIN dim_date d ON risk.date_key = d.date_key
    WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
        AND {filter_str}
    """
    
    summary_result = p.sql.query_one(summary_sql)
    
    type_sql = f"""
    SELECT 
        risk.risk_type,
        COUNT(*) as risk_count,
        AVG(risk.risk_value) as avg_risk_value,
        SUM(p.contract_amount) as affected_contract_amount
    FROM fact_risk risk
    JOIN dim_project p ON risk.project_key = p.project_key
    JOIN dim_date d ON risk.date_key = d.date_key
    WHERE d.calendar_date BETWEEN '{start_date}' AND '{end_date}'
        AND {filter_str}
    GROUP BY risk.risk_type
    ORDER BY risk_count DESC
    """
    
    type_results = p.sql.query(type_sql)
    
    risk_details = []
    for row in risk_results:
        risk_details.append({
            "risk_id": row["risk_id"],
            "risk_type": row["risk_type"],
            "risk_value": float(row.get("risk_value", 0) or 0),
            "risk_level_name": row["risk_level_name"],
            "project_key": row["project_key"],
            "project_code": row["project_code"],
            "project_name": row["project_name"],
            "contract_amount": float(row.get("contract_amount", 0) or 0),
            "region_name": row["region_name"],
            "organization_name": row["organization_name"],
            "risk_date": str(row.get("risk_date")),
        })
    
    type_distribution = []
    for row in type_results:
        type_distribution.append({
            "risk_type": row["risk_type"],
            "risk_count": row.get("risk_count", 0) or 0,
            "avg_risk_value": round(float(row.get("avg_risk_value", 0) or 0), 2),
            "affected_contract_amount": float(row.get("affected_contract_amount", 0) or 0),
        })
    
    if risk_details:
        columns = list(risk_details[0].keys())
        data = [list(row.values()) for row in risk_details]
    else:
        columns = ["risk_id", "risk_type", "risk_value", "risk_level_name", "project_key", "project_code", "project_name", "contract_amount", "region_name", "organization_name", "risk_date"]
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