"""成本科目同比分析函数 — 商务成本智能决策体系

function_id: panda.cost.cost_subject_yoy_analysis
发布：dazi onto script publish .../functions/cost_subject_yoy_analysis.py --space space__panda_construction --register-function-id panda.cost.cost_subject_yoy_analysis --register-platform-category 分析函数
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"project_key": "PROJ001", "year": 2026},
    "object_type_code": "Project",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    project_key = params.get("project_key", "")
    year = params.get("year", 2026)
    
    if not project_key:
        return p.function_result(
            columns=["project_key", "subject_code", "subject_name", "current_year_amount", "last_year_amount", "yoy_amount", "yoy_rate"],
            data=[],
            row_count=0,
        )
    
    # 获取所有一级成本科目
    subjects = p.sql.query("""
        SELECT cost_subject_key, subject_code, subject_name 
        FROM dim_cost_subject 
        WHERE subject_level = 1
    """)
    
    data = []
    for subject in subjects:
        # 查询本年成本
        current_rows = p.sql.query("""
            SELECT SUM(cost_amount) as total 
            FROM fact_project_cost 
            WHERE project_key = ? AND cost_subject_key = ? 
              AND calendar_date >= ? AND calendar_date <= ?
        """, [project_key, subject["cost_subject_key"], f"{year}-01-01", f"{year}-12-31"])
        
        current_cost = current_rows[0]["total"] if current_rows and current_rows[0]["total"] else 0
        
        # 查询上年成本
        last_rows = p.sql.query("""
            SELECT SUM(cost_amount) as total 
            FROM fact_project_cost 
            WHERE project_key = ? AND cost_subject_key = ? 
              AND calendar_date >= ? AND calendar_date <= ?
        """, [project_key, subject["cost_subject_key"], f"{year-1}-01-01", f"{year-1}-12-31"])
        
        last_cost = last_rows[0]["total"] if last_rows and last_rows[0]["total"] else 0
        
        yoy_amount = current_cost - last_cost
        yoy_rate = round(yoy_amount / last_cost, 4) if last_cost > 0 else 0
        
        data.append({
            "project_key": project_key,
            "subject_code": subject["subject_code"],
            "subject_name": subject["subject_name"],
            "current_year_amount": round(current_cost, 2),
            "last_year_amount": round(last_cost, 2),
            "yoy_amount": round(yoy_amount, 2),
            "yoy_rate": yoy_rate,
        })
    
    return p.function_result(
        columns=["project_key", "subject_code", "subject_name", "current_year_amount", "last_year_amount", "yoy_amount", "yoy_rate"],
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