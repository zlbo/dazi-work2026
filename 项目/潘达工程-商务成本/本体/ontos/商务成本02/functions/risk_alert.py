"""风险三色预警函数 — 商务成本智能决策体系

function_id: panda.cost.risk_alert
发布：dazi onto script publish .../functions/risk_alert.py --space space__panda_construction --register-function-id panda.cost.risk_alert --register-platform-category 评估函数
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
            columns=["project_key", "project_name", "overall_risk_level", "overall_risk_score", "alert_color", "suggestion"],
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
            columns=["project_key", "project_name", "overall_risk_level", "overall_risk_score", "alert_color", "suggestion"],
            data=[],
            row_count=0,
        )
    
    project = rows[0]
    
    # 查询风险记录
    risk_rows = p.sql.query("""
        SELECT risk_type, risk_level, risk_value 
        FROM fact_risk 
        WHERE project_key = ?
    """, [project_key])
    
    if not risk_rows:
        data = [{
            "project_key": project["project_key"],
            "project_name": project["project_name"],
            "overall_risk_level": "正常",
            "overall_risk_score": 0.0,
            "alert_color": "绿色",
            "suggestion": "项目运行正常，继续保持监控",
        }]
        return p.function_result(
            columns=["project_key", "project_name", "overall_risk_level", "overall_risk_score", "alert_color", "suggestion"],
            data=data,
            row_count=1,
        )
    
    # 计算综合风险分数
    risk_weights = {"严重": 1.0, "预警": 0.5, "正常": 0.1}
    total_weight = 0
    weighted_score = 0
    
    for risk in risk_rows:
        weight = risk_weights.get(risk["risk_level"], 0.1)
        weighted_score += risk["risk_value"] * weight
        total_weight += weight
    
    if total_weight > 0:
        overall_score = round(weighted_score / total_weight, 2)
    else:
        overall_score = 0
    
    # 判定综合风险等级和预警颜色
    if overall_score < 30:
        overall_level = "正常"
        alert_color = "绿色"
        suggestion = "项目运行正常，继续保持监控"
    elif overall_score < 70:
        overall_level = "预警"
        alert_color = "黄色"
        suggestion = "存在一定风险，建议加强监控并制定应对措施"
    else:
        overall_level = "严重"
        alert_color = "红色"
        suggestion = "风险较高，建议立即采取干预措施，必要时升级处理"
    
    data = [{
        "project_key": project["project_key"],
        "project_name": project["project_name"],
        "overall_risk_level": overall_level,
        "overall_risk_score": overall_score,
        "alert_color": alert_color,
        "suggestion": suggestion,
    }]
    
    return p.function_result(
        columns=["project_key", "project_name", "overall_risk_level", "overall_risk_score", "alert_color", "suggestion"],
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