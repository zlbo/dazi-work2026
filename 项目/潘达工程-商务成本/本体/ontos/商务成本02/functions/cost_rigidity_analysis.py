"""成本刚性度分析函数 — 商务成本智能决策体系

function_id: panda.cost.cost_rigidity_analysis
发布：dazi onto script publish .../functions/cost_rigidity_analysis.py --space space__panda_construction --register-function-id panda.cost.cost_rigidity_analysis --register-platform-category 分析函数
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
            columns=["project_key", "project_name", "total_cost", "rigid_cost", "flexible_cost", "rigidity_ratio", "rigidity_level"],
            data=[],
            row_count=0,
        )
    
    # 查询项目信息
    rows = p.sql.query("""
        SELECT project_key, project_name 
        FROM dim_project 
        WHERE project_key = ?
    """, [project_key])
    
    if not rows:
        return p.function_result(
            columns=["project_key", "project_name", "total_cost", "rigid_cost", "flexible_cost", "rigidity_ratio", "rigidity_level"],
            data=[],
            row_count=0,
        )
    
    project = rows[0]
    
    # 查询刚性成本（人工、材料、机械）
    rigid_rows = p.sql.query("""
        SELECT SUM(cost_amount) as total_rigid 
        FROM fact_project_cost 
        WHERE project_key = ? AND cost_type IN ('人工成本', '材料成本', '机械成本')
    """, [project_key])
    
    rigid_cost = rigid_rows[0]["total_rigid"] if rigid_rows and rigid_rows[0]["total_rigid"] else 0
    
    # 查询弹性成本（管理费用、其他费用）
    flexible_rows = p.sql.query("""
        SELECT SUM(cost_amount) as total_flexible 
        FROM fact_project_cost 
        WHERE project_key = ? AND cost_type IN ('管理费用', '其他费用')
    """, [project_key])
    
    flexible_cost = flexible_rows[0]["total_flexible"] if flexible_rows and flexible_rows[0]["total_flexible"] else 0
    
    total_cost = rigid_cost + flexible_cost
    
    if total_cost > 0:
        rigidity_ratio = round(rigid_cost / total_cost, 4)
    else:
        rigidity_ratio = 0
    
    # 判定刚性等级
    if rigidity_ratio < 0.6:
        rigidity_level = "低刚性"
    elif rigidity_ratio < 0.8:
        rigidity_level = "中刚性"
    else:
        rigidity_level = "高刚性"
    
    data = [{
        "project_key": project["project_key"],
        "project_name": project["project_name"],
        "total_cost": round(total_cost, 2),
        "rigid_cost": round(rigid_cost, 2),
        "flexible_cost": round(flexible_cost, 2),
        "rigidity_ratio": rigidity_ratio,
        "rigidity_level": rigidity_level,
    }]
    
    return p.function_result(
        columns=["project_key", "project_name", "total_cost", "rigid_cost", "flexible_cost", "rigidity_ratio", "rigidity_level"],
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