"""项目利润评估函数 — 商务成本智能决策体系

function_id: panda.cost.project_profit_assessment
发布：dazi onto script publish .../functions/project_profit_assessment.py --space space__panda_construction --register-function-id panda.cost.project_profit_assessment --register-platform-category 评估函数
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"project_key": "PROJ001"},
    "object_type_code": "Project",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    project_key = params.get("project_key", "")
    
    if not project_key:
        return p.function_result(
            columns=["project_key", "project_name", "total_output", "total_cost", "profit", "profit_rate", "target_profit_rate", "profit_gap", "profit_status", "assessment"],
            data=[],
            row_count=0,
        )
    
    # 查询项目信息
    rows = p.sql.query("""
        SELECT project_key, project_name, quality_level 
        FROM dim_project 
        WHERE project_key = ?
    """, [project_key])
    
    if not rows:
        return p.function_result(
            columns=["project_key", "project_name", "total_output", "total_cost", "profit", "profit_rate", "target_profit_rate", "profit_gap", "profit_status", "assessment"],
            data=[],
            row_count=0,
        )
    
    project = rows[0]
    
    # 查询指标数据
    indicator_rows = p.sql.query("""
        SELECT total_output, total_cost, profit, profit_rate 
        FROM fact_project_indicator 
        WHERE project_key = ?
    """, [project_key])
    
    if indicator_rows:
        indicator = indicator_rows[0]
        total_output = indicator["total_output"]
        total_cost = indicator["total_cost"]
        profit = indicator["profit"]
        profit_rate = indicator["profit_rate"]
    else:
        # 从事实表计算
        output_rows = p.sql.query("""
            SELECT SUM(output_amount) as total 
            FROM fact_project_output 
            WHERE project_key = ?
        """, [project_key])
        total_output = output_rows[0]["total"] if output_rows and output_rows[0]["total"] else 0
        
        cost_rows = p.sql.query("""
            SELECT SUM(cost_amount) as total 
            FROM fact_project_cost 
            WHERE project_key = ?
        """, [project_key])
        total_cost = cost_rows[0]["total"] if cost_rows and cost_rows[0]["total"] else 0
        
        profit = total_output - total_cost
        profit_rate = round(profit / total_output, 4) if total_output > 0 else 0
    
    # 根据品质等级设定目标利润率
    quality_targets = {"A": 0.15, "B": 0.08, "C": 0.02}
    target_profit_rate = quality_targets.get(project["quality_level"], 0.08)
    
    # 计算利润差距
    target_profit = total_output * target_profit_rate
    profit_gap = round(target_profit - profit, 2)
    
    # 判定利润状态
    actual_rate = profit_rate
    target_rate = target_profit_rate
    
    if actual_rate >= target_rate:
        profit_status = "达标"
        assessment = "项目利润表现良好，达到预期目标"
    elif actual_rate >= target_rate * 0.8:
        profit_status = "接近达标"
        assessment = "利润接近目标，建议进一步优化成本控制"
    elif actual_rate >= target_rate * 0.5:
        profit_status = "未达标"
        assessment = "利润未达标，需要采取成本优化措施"
    else:
        profit_status = "严重未达标"
        assessment = "利润差距较大，建议全面审查成本结构，制定改进方案"
    
    data = [{
        "project_key": project["project_key"],
        "project_name": project["project_name"],
        "total_output": round(total_output, 2),
        "total_cost": round(total_cost, 2),
        "profit": round(profit, 2),
        "profit_rate": profit_rate,
        "target_profit_rate": target_profit_rate,
        "profit_gap": profit_gap,
        "profit_status": profit_status,
        "assessment": assessment,
    }]
    
    return p.function_result(
        columns=["project_key", "project_name", "total_output", "total_cost", "profit", "profit_rate", "target_profit_rate", "profit_gap", "profit_status", "assessment"],
        data=data,
        row_count=1,
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