# 商务成本区域分析函数

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2024-01-01",
        "end_date": "2026-06-30",
        "region_key": None,
    },
    "object_type_code": "Project",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    
    start_date = params.get("start_date", "2024-01-01")
    end_date = params.get("end_date", "2026-06-30")
    region_key = params.get("region_key")
    
    filter_str = f"AND r.region_key = '{region_key}'" if region_key else ""
    
    sql = f"""
    SELECT 
        r.region_key,
        r.region_code,
        r.region_name,
        r.region_level,
        r.parent_key,
        COUNT(DISTINCT p.project_key) as project_count,
        SUM(c.cost_amount) as total_cost,
        SUM(out.output_amount) as total_output,
        SUM(p.contract_amount) as total_contract_amount,
        AVG(risk.risk_value) as avg_risk_value
    FROM dim_region r
    LEFT JOIN dim_project p ON r.region_key = p.region_key
    LEFT JOIN fact_project_cost c ON p.project_key = c.project_key
    LEFT JOIN fact_project_output out ON p.project_key = out.project_key
    LEFT JOIN fact_risk risk ON p.project_key = risk.project_key
    LEFT JOIN dim_date d ON c.date_key = d.date_key
    WHERE (d.calendar_date BETWEEN '{start_date}' AND '{end_date}' OR d.calendar_date IS NULL)
        {filter_str}
    GROUP BY r.region_key, r.region_code, r.region_name, r.region_level, r.parent_key
    ORDER BY r.region_level, r.region_code
    """
    
    results = p.sql.query(sql)
    
    region_analysis = []
    for row in results:
        total_cost = float(row.get("total_cost", 0) or 0)
        total_output = float(row.get("total_output", 0) or 0)
        total_contract = float(row.get("total_contract_amount", 0) or 0)
        
        region_analysis.append({
            "region_key": row["region_key"],
            "region_code": row["region_code"],
            "region_name": row["region_name"],
            "region_level": row.get("region_level", 0) or 0,
            "parent_key": row.get("parent_key"),
            "project_count": row.get("project_count", 0) or 0,
            "total_cost": total_cost,
            "total_output": total_output,
            "total_contract_amount": total_contract,
            "avg_risk_value": round(float(row.get("avg_risk_value", 0) or 0), 2),
            "profit": total_output - total_cost,
            "profit_rate": round((total_output - total_cost) / total_output * 100, 2) if total_output > 0 else 0,
            "cost_ratio": round(total_cost / total_contract * 100, 2) if total_contract > 0 else 0,
        })
    
    level_summary = {}
    for region in region_analysis:
        level = region["region_level"]
        if level not in level_summary:
            level_summary[level] = {
                "region_count": 0,
                "project_count": 0,
                "total_cost": 0,
                "total_output": 0,
            }
        level_summary[level]["region_count"] += 1
        level_summary[level]["project_count"] += region["project_count"]
        level_summary[level]["total_cost"] += region["total_cost"]
        level_summary[level]["total_output"] += region["total_output"]
    
    if region_analysis:
        columns = list(region_analysis[0].keys())
        data = [list(row.values()) for row in region_analysis]
    else:
        columns = ["region_key", "region_code", "region_name", "region_level", "parent_key", "project_count", "total_cost", "total_output", "total_contract_amount", "avg_risk_value", "profit", "profit_rate", "cost_ratio"]
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