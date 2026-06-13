"""
业务函数脚本 - 商务成本智能决策体系
版本：V1.0
依据：阶段二设计文档（业务规则文档）
功能：实现7个核心业务函数
"""

from dazi.ontology import OntologyContext
from dazi.functions import register_function

# ==================== 1. 成本偏差率分析 ====================
@register_function(
    code="cost_deviation_analysis",
    display_name="成本偏差率分析",
    description="计算项目实际成本与预算成本的偏差率",
    input_parameters=[
        {"name": "project_key", "display_name": "项目标识", "type": "String", "required": True},
        {"name": "start_date", "display_name": "开始日期", "type": "Date"},
        {"name": "end_date", "display_name": "结束日期", "type": "Date"},
    ],
    output_parameters=[
        {"name": "project_key", "display_name": "项目标识", "type": "String"},
        {"name": "project_name", "display_name": "项目名称", "type": "String"},
        {"name": "budget_cost", "display_name": "预算成本", "type": "Decimal(18,2)"},
        {"name": "actual_cost", "display_name": "实际成本", "type": "Decimal(18,2)"},
        {"name": "deviation_amount", "display_name": "偏差金额", "type": "Decimal(18,2)"},
        {"name": "deviation_rate", "display_name": "偏差率(%)", "type": "Decimal(5,4)"},
        {"name": "deviation_status", "display_name": "偏差状态", "type": "String"},
    ],
    platform_category="分析函数"
)
def cost_deviation_analysis(project_key, start_date=None, end_date=None):
    """
    计算项目成本偏差率
    偏差率 = (实际成本 - 预算成本) / 预算成本 * 100%
    
    偏差状态判定：
    - 正常：偏差率 ∈ [-5%, 5%]
    - 预警：偏差率 ∈ [-10%, -5%) 或 (5%, 10%]
    - 严重：偏差率 < -10% 或 > 10%
    """
    with OntologyContext() as s:
        # 查询项目预算
        project = s.tables.query(
            table_name="dim_project",
            where={"project_key": project_key},
            select=["project_key", "project_name", "contract_amount_net"]
        ).first()
        
        if not project:
            return None
        
        budget_cost = project["contract_amount_net"] * 0.85  # 假设预算为合同金额的85%
        
        # 查询实际成本
        cost_filter = {"project_key": project_key}
        if start_date:
            cost_filter["calendar_date__gte"] = start_date
        if end_date:
            cost_filter["calendar_date__lte"] = end_date
        
        actual_cost = s.tables.aggregate(
            table_name="fact_project_cost",
            where=cost_filter,
            aggregations=[("cost_amount", "SUM", "total_cost")]
        ).get("total_cost", 0)
        
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
        
        return {
            "project_key": project["project_key"],
            "project_name": project["project_name"],
            "budget_cost": round(budget_cost, 2),
            "actual_cost": round(actual_cost, 2),
            "deviation_amount": round(deviation_amount, 2),
            "deviation_rate": deviation_rate,
            "deviation_status": deviation_status,
        }

# ==================== 2. 成本刚性度分析 ====================
@register_function(
    code="cost_rigidity_analysis",
    display_name="成本刚性度分析",
    description="分析项目成本结构中刚性成本占比",
    input_parameters=[
        {"name": "project_key", "display_name": "项目标识", "type": "String", "required": True},
    ],
    output_parameters=[
        {"name": "project_key", "display_name": "项目标识", "type": "String"},
        {"name": "project_name", "display_name": "项目名称", "type": "String"},
        {"name": "total_cost", "display_name": "总成本", "type": "Decimal(18,2)"},
        {"name": "rigid_cost", "display_name": "刚性成本", "type": "Decimal(18,2)"},
        {"name": "flexible_cost", "display_name": "弹性成本", "type": "Decimal(18,2)"},
        {"name": "rigidity_ratio", "display_name": "刚性度(%)", "type": "Decimal(5,4)"},
        {"name": "rigidity_level", "display_name": "刚性等级", "type": "String"},
    ],
    platform_category="分析函数"
)
def cost_rigidity_analysis(project_key):
    """
    分析成本刚性度
    刚性成本：人工成本、材料成本、机械成本（不可轻易压缩）
    弹性成本：管理费用、其他费用（可优化空间较大）
    
    刚性等级判定：
    - 低刚性：刚性度 < 60%
    - 中刚性：60% ≤ 刚性度 < 80%
    - 高刚性：刚性度 ≥ 80%
    """
    with OntologyContext() as s:
        # 查询项目信息
        project = s.tables.query(
            table_name="dim_project",
            where={"project_key": project_key},
            select=["project_key", "project_name"]
        ).first()
        
        if not project:
            return None
        
        # 查询刚性成本（人工、材料、机械）
        rigid_cost = s.tables.aggregate(
            table_name="fact_project_cost",
            where={
                "project_key": project_key,
                "cost_type__in": ["人工成本", "材料成本", "机械成本"]
            },
            aggregations=[("cost_amount", "SUM", "total_rigid")]
        ).get("total_rigid", 0)
        
        # 查询弹性成本（管理费用、其他费用）
        flexible_cost = s.tables.aggregate(
            table_name="fact_project_cost",
            where={
                "project_key": project_key,
                "cost_type__in": ["管理费用", "其他费用"]
            },
            aggregations=[("cost_amount", "SUM", "total_flexible")]
        ).get("total_flexible", 0)
        
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
        
        return {
            "project_key": project["project_key"],
            "project_name": project["project_name"],
            "total_cost": round(total_cost, 2),
            "rigid_cost": round(rigid_cost, 2),
            "flexible_cost": round(flexible_cost, 2),
            "rigidity_ratio": rigidity_ratio,
            "rigidity_level": rigidity_level,
        }

# ==================== 3. 成本科目同比分析 ====================
@register_function(
    code="cost_subject_yoy_analysis",
    display_name="成本科目同比分析",
    description="分析各成本科目同比变化情况",
    input_parameters=[
        {"name": "project_key", "display_name": "项目标识", "type": "String", "required": True},
        {"name": "year", "display_name": "分析年份", "type": "Int32", "required": True},
    ],
    output_parameters=[
        {"name": "project_key", "display_name": "项目标识", "type": "String"},
        {"name": "subject_code", "display_name": "科目编码", "type": "String"},
        {"name": "subject_name", "display_name": "科目名称", "type": "String"},
        {"name": "current_year_amount", "display_name": "本年金额", "type": "Decimal(18,2)"},
        {"name": "last_year_amount", "display_name": "上年金额", "type": "Decimal(18,2)"},
        {"name": "yoy_amount", "display_name": "同比增减额", "type": "Decimal(18,2)"},
        {"name": "yoy_rate", "display_name": "同比增长率(%)", "type": "Decimal(5,4)"},
    ],
    platform_category="分析函数",
    returns_list=True
)
def cost_subject_yoy_analysis(project_key, year):
    """
    分析成本科目同比变化
    """
    with OntologyContext() as s:
        results = []
        
        # 获取所有一级成本科目
        subjects = s.tables.query(
            table_name="dim_cost_subject",
            where={"subject_level": 1},
            select=["cost_subject_key", "subject_code", "subject_name"]
        ).all()
        
        for subject in subjects:
            # 查询本年成本
            current_cost = s.tables.aggregate(
                table_name="fact_project_cost",
                where={
                    "project_key": project_key,
                    "cost_subject_key": subject["cost_subject_key"],
                    "calendar_date__gte": f"{year}-01-01",
                    "calendar_date__lte": f"{year}-12-31"
                },
                aggregations=[("cost_amount", "SUM", "total")]
            ).get("total", 0)
            
            # 查询上年成本
            last_cost = s.tables.aggregate(
                table_name="fact_project_cost",
                where={
                    "project_key": project_key,
                    "cost_subject_key": subject["cost_subject_key"],
                    "calendar_date__gte": f"{year-1}-01-01",
                    "calendar_date__lte": f"{year-1}-12-31"
                },
                aggregations=[("cost_amount", "SUM", "total")]
            ).get("total", 0)
            
            yoy_amount = current_cost - last_cost
            yoy_rate = round(yoy_amount / last_cost, 4) if last_cost > 0 else 0
            
            results.append({
                "project_key": project_key,
                "subject_code": subject["subject_code"],
                "subject_name": subject["subject_name"],
                "current_year_amount": round(current_cost, 2),
                "last_year_amount": round(last_cost, 2),
                "yoy_amount": round(yoy_amount, 2),
                "yoy_rate": yoy_rate,
            })
        
        return results

# ==================== 4. 产值确权比分析 ====================
@register_function(
    code="output_confirmation_ratio",
    display_name="产值确权比分析",
    description="计算项目产值确权比例",
    input_parameters=[
        {"name": "project_key", "display_name": "项目标识", "type": "String", "required": True},
        {"name": "month", "display_name": "统计月份", "type": "String"},  # YYYYMM格式
    ],
    output_parameters=[
        {"name": "project_key", "display_name": "项目标识", "type": "String"},
        {"name": "project_name", "display_name": "项目名称", "type": "String"},
        {"name": "total_output", "display_name": "总产值", "type": "Decimal(18,2)"},
        {"name": "confirmed_output", "display_name": "已确认产值", "type": "Decimal(18,2)"},
        {"name": "unconfirmed_output", "display_name": "待确认产值", "type": "Decimal(18,2)"},
        {"name": "confirm_ratio", "display_name": "确权比(%)", "type": "Decimal(5,4)"},
        {"name": "confirm_status", "display_name": "确权状态", "type": "String"},
    ],
    platform_category="分析函数"
)
def output_confirmation_ratio(project_key, month=None):
    """
    计算产值确权比
    确权比 = 已确认产值 / 总产值 * 100%
    
    确权状态判定：
    - 优秀：确权比 ≥ 90%
    - 良好：70% ≤ 确权比 < 90%
    - 一般：50% ≤ 确权比 < 70%
    - 较差：确权比 < 50%
    """
    with OntologyContext() as s:
        # 查询项目信息
        project = s.tables.query(
            table_name="dim_project",
            where={"project_key": project_key},
            select=["project_key", "project_name"]
        ).first()
        
        if not project:
            return None
        
        # 构建查询条件
        output_filter = {"project_key": project_key}
        if month:
            output_filter["year_month"] = month
        
        # 查询总产值
        total_output = s.tables.aggregate(
            table_name="fact_project_output",
            where=output_filter,
            aggregations=[("output_amount", "SUM", "total")]
        ).get("total", 0)
        
        # 查询已确认产值
        confirmed_filter = output_filter.copy()
        confirmed_filter["confirmation_status"] = "已确认"
        confirmed_output = s.tables.aggregate(
            table_name="fact_project_output",
            where=confirmed_filter,
            aggregations=[("output_amount", "SUM", "total")]
        ).get("total", 0)
        
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
        
        return {
            "project_key": project["project_key"],
            "project_name": project["project_name"],
            "total_output": round(total_output, 2),
            "confirmed_output": round(confirmed_output, 2),
            "unconfirmed_output": round(unconfirmed_output, 2),
            "confirm_ratio": confirm_ratio,
            "confirm_status": confirm_status,
        }

# ==================== 5. 现金流预测 ====================
@register_function(
    code="cash_flow_forecast",
    display_name="现金流预测",
    description="预测项目未来现金流情况",
    input_parameters=[
        {"name": "project_key", "display_name": "项目标识", "type": "String", "required": True},
        {"name": "forecast_months", "display_name": "预测月数", "type": "Int32", "default": 3},
    ],
    output_parameters=[
        {"name": "project_key", "display_name": "项目标识", "type": "String"},
        {"name": "project_name", "display_name": "项目名称", "type": "String"},
        {"name": "forecast_month", "display_name": "预测月份", "type": "String"},
        {"name": "expected_income", "display_name": "预计收入", "type": "Decimal(18,2)"},
        {"name": "expected_expense", "display_name": "预计支出", "type": "Decimal(18,2)"},
        {"name": "net_cash_flow", "display_name": "净现金流", "type": "Decimal(18,2)"},
        {"name": "cash_flow_status", "display_name": "现金流状态", "type": "String"},
    ],
    platform_category="预测函数",
    returns_list=True
)
def cash_flow_forecast(project_key, forecast_months=3):
    """
    预测项目未来现金流
    基于历史数据预测未来收入和支出
    """
    with OntologyContext() as s:
        results = []
        
        # 查询项目信息
        project = s.tables.query(
            table_name="dim_project",
            where={"project_key": project_key},
            select=["project_key", "project_name"]
        ).first()
        
        if not project:
            return None
        
        # 查询最近3个月的平均收入和支出
        recent_income = s.tables.aggregate(
            table_name="fact_cash_flow",
            where={
                "project_key": project_key,
                "cash_flow_type": "收入",
            },
            aggregations=[("cash_flow_amount", "AVG", "avg_income")]
        ).get("avg_income", 0)
        
        recent_expense = s.tables.aggregate(
            table_name="fact_cash_flow",
            where={
                "project_key": project_key,
                "cash_flow_type": "支出",
            },
            aggregations=[("cash_flow_amount", "AVG", "avg_expense")]
        ).get("avg_expense", 0)
        
        # 生成预测数据
        from datetime import datetime, timedelta
        current_date = datetime.now()
        
        for i in range(forecast_months):
            forecast_date = current_date + timedelta(days=30 * (i + 1))
            forecast_month = forecast_date.strftime("%Y%m")
            
            # 考虑项目进度因素调整预测
            progress_factor = 1.0 + (i * 0.1)  # 随时间递增
            
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
            
            results.append({
                "project_key": project["project_key"],
                "project_name": project["project_name"],
                "forecast_month": forecast_month,
                "expected_income": expected_income,
                "expected_expense": expected_expense,
                "net_cash_flow": round(net_cash_flow, 2),
                "cash_flow_status": cash_flow_status,
            })
        
        return results

# ==================== 6. 风险三色预警 ====================
@register_function(
    code="risk_alert",
    display_name="风险三色预警",
    description="综合评估项目风险等级并发出预警",
    input_parameters=[
        {"name": "project_key", "display_name": "项目标识", "type": "String", "required": True},
    ],
    output_parameters=[
        {"name": "project_key", "display_name": "项目标识", "type": "String"},
        {"name": "project_name", "display_name": "项目名称", "type": "String"},
        {"name": "overall_risk_level", "display_name": "综合风险等级", "type": "String"},
        {"name": "overall_risk_score", "display_name": "综合风险分数", "type": "Decimal(5,2)"},
        {"name": "risk_items", "display_name": "风险项列表", "type": "Array"},
        {"name": "alert_color", "display_name": "预警颜色", "type": "String"},
        {"name": "suggestion", "display_name": "建议措施", "type": "String"},
    ],
    platform_category="评估函数"
)
def risk_alert(project_key):
    """
    综合评估项目风险等级
    采用三色预警机制：
    - 绿色（正常）：风险分数 < 30
    - 黄色（预警）：30 ≤ 风险分数 < 70
    - 红色（严重）：风险分数 ≥ 70
    """
    with OntologyContext() as s:
        # 查询项目信息
        project = s.tables.query(
            table_name="dim_project",
            where={"project_key": project_key},
            select=["project_key", "project_name"]
        ).first()
        
        if not project:
            return None
        
        # 查询风险记录
        risks = s.tables.query(
            table_name="fact_risk",
            where={"project_key": project_key},
            select=["risk_type", "risk_level", "risk_value"]
        ).all()
        
        if not risks:
            return {
                "project_key": project["project_key"],
                "project_name": project["project_name"],
                "overall_risk_level": "正常",
                "overall_risk_score": 0.0,
                "risk_items": [],
                "alert_color": "绿色",
                "suggestion": "项目运行正常，继续保持监控",
            }
        
        # 计算综合风险分数
        # 严重风险权重1.0，预警风险权重0.5，正常风险权重0.1
        risk_weights = {"严重": 1.0, "预警": 0.5, "正常": 0.1}
        total_weight = 0
        weighted_score = 0
        
        risk_items = []
        for risk in risks:
            weight = risk_weights.get(risk["risk_level"], 0.1)
            weighted_score += risk["risk_value"] * weight
            total_weight += weight
            
            risk_items.append({
                "risk_type": risk["risk_type"],
                "risk_level": risk["risk_level"],
                "risk_value": risk["risk_value"]
            })
        
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
        
        return {
            "project_key": project["project_key"],
            "project_name": project["project_name"],
            "overall_risk_level": overall_level,
            "overall_risk_score": overall_score,
            "risk_items": risk_items,
            "alert_color": alert_color,
            "suggestion": suggestion,
        }

# ==================== 7. 项目利润评估 ====================
@register_function(
    code="project_profit_assessment",
    display_name="项目利润评估",
    description="综合评估项目利润情况",
    input_parameters=[
        {"name": "project_key", "display_name": "项目标识", "type": "String", "required": True},
    ],
    output_parameters=[
        {"name": "project_key", "display_name": "项目标识", "type": "String"},
        {"name": "project_name", "display_name": "项目名称", "type": "String"},
        {"name": "total_output", "display_name": "累计产值", "type": "Decimal(18,2)"},
        {"name": "total_cost", "display_name": "累计成本", "type": "Decimal(18,2)"},
        {"name": "profit", "display_name": "利润", "type": "Decimal(18,2)"},
        {"name": "profit_rate", "display_name": "利润率(%)", "type": "Decimal(5,4)"},
        {"name": "target_profit_rate", "display_name": "目标利润率(%)", "type": "Decimal(5,4)"},
        {"name": "profit_gap", "display_name": "利润差距", "type": "Decimal(18,2)"},
        {"name": "profit_status", "display_name": "利润状态", "type": "String"},
        {"name": "assessment", "display_name": "评估建议", "type": "String"},
    ],
    platform_category="评估函数"
)
def project_profit_assessment(project_key):
    """
    综合评估项目利润情况
    目标利润率根据经营品质等级设定：
    - A类项目：15%
    - B类项目：8%
    - C类项目：2%
    """
    with OntologyContext() as s:
        # 查询项目信息
        project = s.tables.query(
            table_name="dim_project",
            where={"project_key": project_key},
            select=["project_key", "project_name", "quality_level"]
        ).first()
        
        if not project:
            return None
        
        # 查询指标数据
        indicator = s.tables.query(
            table_name="fact_project_indicator",
            where={"project_key": project_key},
            select=["total_output", "total_cost", "profit", "profit_rate"]
        ).first()
        
        if not indicator:
            # 如果没有指标数据，从事实表计算
            total_output = s.tables.aggregate(
                table_name="fact_project_output",
                where={"project_key": project_key},
                aggregations=[("output_amount", "SUM", "total")]
            ).get("total", 0)
            
            total_cost = s.tables.aggregate(
                table_name="fact_project_cost",
                where={"project_key": project_key},
                aggregations=[("cost_amount", "SUM", "total")]
            ).get("total", 0)
            
            profit = total_output - total_cost
            profit_rate = round(profit / total_output, 4) if total_output > 0 else 0
        else:
            total_output = indicator["total_output"]
            total_cost = indicator["total_cost"]
            profit = indicator["profit"]
            profit_rate = indicator["profit_rate"]
        
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
        
        return {
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
        }

# ==================== 函数注册入口 ====================
def register_all_functions():
    """注册所有业务函数"""
    functions = [
        cost_deviation_analysis,
        cost_rigidity_analysis,
        cost_subject_yoy_analysis,
        output_confirmation_ratio,
        cash_flow_forecast,
        risk_alert,
        project_profit_assessment,
    ]
    
    print("=== 开始注册业务函数 ===")
    for func in functions:
        try:
            func.register()
            print(f"  ✓ 已注册: {func.__name__}")
        except Exception as e:
            print(f"  ✗ 注册失败 {func.__name__}: {e}")
    
    print(f"\n=== 共注册 {len(functions)} 个业务函数 ===")

if __name__ == "__main__":
    register_all_functions()