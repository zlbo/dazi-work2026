# 商务成本组织分析函数

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2024-01-01",
        "end_date": "2026-06-30",
        "organization_key": None,
    },
    "object_type_code": "Project",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    
    start_date = params.get("start_date", "2024-01-01")
    end_date = params.get("end_date", "2026-06-30")
    organization_key = params.get("organization_key")
    
    filter_str = f"AND o.organization_key = '{organization_key}'" if organization_key else ""
    
    sql = f"""
    SELECT 
        org.organization_key,
        org.organization_code,
        org.organization_name,
        org.org_level,
        COUNT(DISTINCT p.project_key) as project_count,
        SUM(c.cost_amount) as total_cost,
        SUM(out.output_amount) as total_output,
        SUM(p.contract_amount) as total_contract_amount,
        AVG(p.management_fee_rate) as avg_management_fee_rate
    FROM dim_organization org
    LEFT JOIN dim_project p ON org.organization_key = p.organization_key
    LEFT JOIN fact_project_cost c ON p.project_key = c.project_key
    LEFT JOIN fact_project_output out ON p.project_key = out.project_key
    LEFT JOIN dim_date d ON c.date_key = d.date_key
    WHERE (d.calendar_date BETWEEN '{start_date}' AND '{end_date}' OR d.calendar_date IS NULL)
        {filter_str}
    GROUP BY org.organization_key, org.organization_code, org.organization_name, org.org_level
    ORDER BY org.org_level, org.organization_code
    """
    
    results = p.sql.query(sql)
    
    org_analysis = []
    for row in results:
        total_cost = float(row.get("total_cost", 0) or 0)
        total_output = float(row.get("total_output", 0) or 0)
        total_contract = float(row.get("total_contract_amount", 0) or 0)
        
        org_analysis.append({
            "organization_key": row["organization_key"],
            "organization_code": row["organization_code"],
            "organization_name": row["organization_name"],
            "org_level": row.get("org_level", 0) or 0,
            "project_count": row.get("project_count", 0) or 0,
            "total_cost": total_cost,
            "total_output": total_output,
            "total_contract_amount": total_contract,
            "avg_management_fee_rate": round(float(row.get("avg_management_fee_rate", 0) or 0) * 100, 2),
            "profit": total_output - total_cost,
            "profit_rate": round((total_output - total_cost) / total_output * 100, 2) if total_output > 0 else 0,
            "cost_ratio": round(total_cost / total_contract * 100, 2) if total_contract > 0 else 0,
        })
    
    level_summary = {}
    for org in org_analysis:
        level = org["org_level"]
        if level not in level_summary:
            level_summary[level] = {
                "org_count": 0,
                "project_count": 0,
                "total_cost": 0,
                "total_output": 0,
            }
        level_summary[level]["org_count"] += 1
        level_summary[level]["project_count"] += org["project_count"]
        level_summary[level]["total_cost"] += org["total_cost"]
        level_summary[level]["total_output"] += org["total_output"]
    
    if org_analysis:
        columns = list(org_analysis[0].keys())
        data = [list(row.values()) for row in org_analysis]
    else:
        columns = ["organization_key", "organization_code", "organization_name", "org_level", "project_count", "total_cost", "total_output", "total_contract_amount", "avg_management_fee_rate", "profit", "profit_rate", "cost_ratio"]
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