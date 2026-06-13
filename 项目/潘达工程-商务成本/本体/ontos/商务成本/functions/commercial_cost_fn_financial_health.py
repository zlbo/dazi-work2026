# 商务成本财务健康度分析函数

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
    
    sql = f"""
    SELECT 
        p.project_key,
        p.project_code,
        p.project_name,
        p.contract_amount,
        SUM(c.cost_amount) as total_cost,
        SUM(o.output_amount) as total_output,
        SUM(r.receivable_amount) as total_receivable,
        SUM(r.received_amount) as total_received,
        SUM(r.outstanding_amount) as total_outstanding,
        SUM(pay.payment_amount) as total_payment,
        SUM(cash.cash_flow_amount) as net_cash_flow
    FROM dim_project p
    LEFT JOIN fact_project_cost c ON p.project_key = c.project_key
    LEFT JOIN fact_project_output o ON p.project_key = o.project_key
    LEFT JOIN fact_receivable r ON p.project_key = r.project_key
    LEFT JOIN fact_payment pay ON p.project_key = pay.project_key
    LEFT JOIN fact_cash_flow cash ON p.project_key = cash.project_key
    LEFT JOIN dim_date d ON c.date_key = d.date_key
    WHERE (d.calendar_date BETWEEN '{start_date}' AND '{end_date}' OR d.calendar_date IS NULL)
        AND {filter_str}
    GROUP BY p.project_key, p.project_code, p.project_name, p.contract_amount
    ORDER BY p.project_code
    """
    
    results = p.sql.query(sql)
    
    health_analysis = []
    for row in results:
        contract_amount = float(row.get("contract_amount", 0) or 0)
        total_cost = float(row.get("total_cost", 0) or 0)
        total_output = float(row.get("total_output", 0) or 0)
        total_receivable = float(row.get("total_receivable", 0) or 0)
        total_received = float(row.get("total_received", 0) or 0)
        total_outstanding = float(row.get("total_outstanding", 0) or 0)
        total_payment = float(row.get("total_payment", 0) or 0)
        net_cash_flow = float(row.get("net_cash_flow", 0) or 0)
        
        profit = total_output - total_cost
        profit_rate = profit / total_output * 100 if total_output > 0 else 0
        collection_rate = total_received / total_receivable * 100 if total_receivable > 0 else 0
        outstanding_ratio = total_outstanding / contract_amount * 100 if contract_amount > 0 else 0
        cost_ratio = total_cost / contract_amount * 100 if contract_amount > 0 else 0
        
        score = 0
        if profit_rate >= 15:
            score += 30
        elif profit_rate >= 5:
            score += 20
        else:
            score += 5
        
        if collection_rate >= 80:
            score += 25
        elif collection_rate >= 60:
            score += 15
        else:
            score += 5
        
        if outstanding_ratio <= 20:
            score += 20
        elif outstanding_ratio <= 40:
            score += 10
        else:
            score += 0
        
        if cost_ratio <= 85:
            score += 25
        elif cost_ratio <= 95:
            score += 15
        else:
            score += 5
        
        if score >= 80:
            health_level = "健康"
        elif score >= 60:
            health_level = "一般"
        elif score >= 40:
            health_level = "警告"
        else:
            health_level = "危险"
        
        health_analysis.append({
            "project_key": row["project_key"],
            "project_code": row["project_code"],
            "project_name": row["project_name"],
            "contract_amount": contract_amount,
            "total_cost": total_cost,
            "total_output": total_output,
            "profit": profit,
            "profit_rate": round(profit_rate, 2),
            "total_receivable": total_receivable,
            "total_received": total_received,
            "total_outstanding": total_outstanding,
            "collection_rate": round(collection_rate, 2),
            "outstanding_ratio": round(outstanding_ratio, 2),
            "total_payment": total_payment,
            "net_cash_flow": net_cash_flow,
            "cost_ratio": round(cost_ratio, 2),
            "health_score": score,
            "health_level": health_level,
        })
    
    total_projects = len(health_analysis)
    healthy_count = sum(1 for h in health_analysis if h["health_level"] == "健康")
    normal_count = sum(1 for h in health_analysis if h["health_level"] == "一般")
    warning_count = sum(1 for h in health_analysis if h["health_level"] == "警告")
    danger_count = sum(1 for h in health_analysis if h["health_level"] == "危险")
    
    avg_score = sum(h["health_score"] for h in health_analysis) / total_projects if total_projects > 0 else 0
    
    if health_analysis:
        columns = list(health_analysis[0].keys())
        data = [list(row.values()) for row in health_analysis]
    else:
        columns = ["project_key", "project_code", "project_name", "contract_amount", "total_cost", "total_output", "profit", "profit_rate", "total_receivable", "total_received", "total_outstanding", "collection_rate", "outstanding_ratio", "total_payment", "net_cash_flow", "cost_ratio", "health_score", "health_level"]
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