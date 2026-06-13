"""现金流预测函数 — 商务成本智能决策体系

function_id: panda.cost.cash_flow_forecast
发布：dazi onto script publish .../functions/cash_flow_forecast.py --space space__panda_construction --register-function-id panda.cost.cash_flow_forecast --register-platform-category 预测函数
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"project_key": "PROJ001", "forecast_months": 3},
    "object_type_code": "Project",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    project_key = params.get("project_key", "")
    forecast_months = params.get("forecast_months", 3)
    
    if not project_key:
        return p.function_result(
            columns=["project_key", "project_name", "forecast_month", "expected_income", "expected_expense", "net_cash_flow", "cash_flow_status"],
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
            columns=["project_key", "project_name", "forecast_month", "expected_income", "expected_expense", "net_cash_flow", "cash_flow_status"],
            data=[],
            row_count=0,
        )
    
    project = rows[0]
    
    # 查询最近平均收入
    income_rows = p.sql.query("""
        SELECT AVG(cash_flow_amount) as avg_income 
        FROM fact_cash_flow 
        WHERE project_key = ? AND cash_flow_type = '收入'
    """, [project_key])
    
    recent_income = income_rows[0]["avg_income"] if income_rows and income_rows[0]["avg_income"] else 0
    
    # 查询最近平均支出
    expense_rows = p.sql.query("""
        SELECT AVG(cash_flow_amount) as avg_expense 
        FROM fact_cash_flow 
        WHERE project_key = ? AND cash_flow_type = '支出'
    """, [project_key])
    
    recent_expense = expense_rows[0]["avg_expense"] if expense_rows and expense_rows[0]["avg_expense"] else 0
    
    # 生成预测数据
    from datetime import datetime, timedelta
    current_date = datetime.now()
    data = []
    
    for i in range(forecast_months):
        forecast_date = current_date + timedelta(days=30 * (i + 1))
        forecast_month = forecast_date.strftime("%Y%m")
        
        # 考虑项目进度因素调整预测
        progress_factor = 1.0 + (i * 0.1)
        
        expected_income = round(recent_income * progress_factor, 2)
        expected_expense = round(recent_expense * progress_factor, 2)
        net_cash_flow = expected_income - expected_expense
        
        # 判定现金流状态
        if net_cash_flow >= 0:
            cash_flow_status = "正向"
        elif net_cash_flow >= -expected_income * 0.3:
            cash_flow_status = "紧张"
        else:
            cash_flow_status = "预警"
        
        data.append({
            "project_key": project["project_key"],
            "project_name": project["project_name"],
            "forecast_month": forecast_month,
            "expected_income": expected_income,
            "expected_expense": expected_expense,
            "net_cash_flow": round(net_cash_flow, 2),
            "cash_flow_status": cash_flow_status,
        })
    
    return p.function_result(
        columns=["project_key", "project_name", "forecast_month", "expected_income", "expected_expense", "net_cash_flow", "cash_flow_status"],
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