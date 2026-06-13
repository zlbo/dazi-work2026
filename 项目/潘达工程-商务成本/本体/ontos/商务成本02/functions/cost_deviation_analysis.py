"""成本偏差率分析函数 — 商务成本智能决策体系

function_id: panda.cost.cost_deviation_analysis
发布：dazi onto script publish .../functions/cost_deviation_analysis.py --space space__panda_construction --register-function-id panda.cost.cost_deviation_analysis --register-platform-category 分析函数
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
            columns=["project_key", "project_name", "budget_cost", "actual_cost", "deviation_amount", "deviation_rate", "deviation_status"],
            data=[],
            row_count=0,
        )
    
    # 查询项目预算
    rows = p.sql.query("""
        SELECT project_key, project_name, contract_amount_net 
        FROM dim_project 
        WHERE project_key = ?
    """, [project_key])
    
    if not rows:
        return p.function_result(
            columns=["project_key", "project_name", "budget_cost", "actual_cost", "deviation_amount", "deviation_rate", "deviation_status"],
            data=[],
            row_count=0,
        )
    
    project = rows[0]
    budget_cost = project["contract_amount_net"] * 0.85  # 假设预算为合同金额的85%
    
    # 查询实际成本
    cost_rows = p.sql.query("""
        SELECT SUM(cost_amount) as total_cost 
        FROM fact_project_cost 
        WHERE project_key = ?
    """, [project_key])
    
    actual_cost = cost_rows[0]["total_cost"] if cost_rows and cost_rows[0]["total_cost"] else 0
    
    # 计算偏差率
    if budget_cost > 0:
        deviation_amount = actual_cost - budget_cost
        deviation_rate = round(deviation_amount / budget_cost, 4)
    else:
        deviation_amount = 0
        deviation_rate = 0
    
    # 判定偏差状态
    if -0.05 <= deviation_rate <= 0.05:
        deviation_status = "正常"
    elif -0.1 <= deviation_rate < -0.05 or 0.05 < deviation_rate <= 0.1:
        deviation_status = "预警"
    else:
        deviation_status = "严重"
    
    data = [{
        "project_key": project["project_key"],
        "project_name": project["project_name"],
        "budget_cost": round(budget_cost, 2),
        "actual_cost": round(actual_cost, 2),
        "deviation_amount": round(deviation_amount, 2),
        "deviation_rate": deviation_rate,
        "deviation_status": deviation_status,
    }]
    
    return p.function_result(
        columns=["project_key", "project_name", "budget_cost", "actual_cost", "deviation_amount", "deviation_rate", "deviation_status"],
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