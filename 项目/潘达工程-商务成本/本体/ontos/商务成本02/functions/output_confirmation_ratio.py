"""产值确权比分析函数 — 商务成本智能决策体系

function_id: panda.cost.output_confirmation_ratio
发布：dazi onto script publish .../functions/output_confirmation_ratio.py --space space__panda_construction --register-function-id panda.cost.output_confirmation_ratio --register-platform-category 分析函数
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
            columns=["project_key", "project_name", "total_output", "confirmed_output", "unconfirmed_output", "confirm_ratio", "confirm_status"],
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
            columns=["project_key", "project_name", "total_output", "confirmed_output", "unconfirmed_output", "confirm_ratio", "confirm_status"],
            data=[],
            row_count=0,
        )
    
    project = rows[0]
    
    # 查询总产值
    total_rows = p.sql.query("""
        SELECT SUM(output_amount) as total 
        FROM fact_project_output 
        WHERE project_key = ?
    """, [project_key])
    
    total_output = total_rows[0]["total"] if total_rows and total_rows[0]["total"] else 0
    
    # 查询已确认产值
    confirmed_rows = p.sql.query("""
        SELECT SUM(output_amount) as total 
        FROM fact_project_output 
        WHERE project_key = ? AND confirmation_status = '已确认'
    """, [project_key])
    
    confirmed_output = confirmed_rows[0]["total"] if confirmed_rows and confirmed_rows[0]["total"] else 0
    
    unconfirmed_output = total_output - confirmed_output
    
    if total_output > 0:
        confirm_ratio = round(confirmed_output / total_output, 4)
    else:
        confirm_ratio = 0
    
    # 判定确权状态
    if confirm_ratio >= 0.9:
        confirm_status = "优秀"
    elif confirm_ratio >= 0.7:
        confirm_status = "良好"
    elif confirm_ratio >= 0.5:
        confirm_status = "一般"
    else:
        confirm_status = "较差"
    
    data = [{
        "project_key": project["project_key"],
        "project_name": project["project_name"],
        "total_output": round(total_output, 2),
        "confirmed_output": round(confirmed_output, 2),
        "unconfirmed_output": round(unconfirmed_output, 2),
        "confirm_ratio": confirm_ratio,
        "confirm_status": confirm_status,
    }]
    
    return p.function_result(
        columns=["project_key", "project_name", "total_output", "confirmed_output", "unconfirmed_output", "confirm_ratio", "confirm_status"],
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