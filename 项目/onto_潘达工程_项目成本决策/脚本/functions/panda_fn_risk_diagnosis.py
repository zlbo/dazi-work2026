"""Panda Construction Risk Diagnosis Function

功能：智能诊断项目风险并给出改进建议
参数：project_id, report_month
返回：风险诊断结果和改进措施

放置位置：项目/onto_潘达工程_项目成本决策/脚本/functions/panda_fn_risk_diagnosis.py
"""


def main(params: dict) -> dict:
    """
    函数入口，params 由平台传入。
    """
    s = space.get(ctx.space_id or "")

    project_id = params.get("project_id", "")
    report_month = params.get("report_month", "")

    if not project_id or not report_month:
        return {
            "ok": False,
            "error": "project_id and report_month are required",
            "data": []
        }

    indicator_sql = f"""
    SELECT
        indicator_code,
        indicator_name,
        current_value,
        reference_value,
        warning_level,
        issue_analysis,
        improvement
    FROM fact_risk_indicator
    WHERE project_id = '{project_id}' AND report_month = '{report_month}'
    ORDER BY
        CASE warning_level
            WHEN 'red' THEN 1
            WHEN 'yellow' THEN 2
            WHEN 'green' THEN 3
        END,
        indicator_code
    """

    indicators = s.sql.query(indicator_sql)

    if not indicators:
        project_sql = f"""
        SELECT
            project_name,
            warning_status,
            profit_rate_total,
            profit_rate_confirmed,
            receivable_ratio,
            received_amount,
            receivable_amount,
            output_confirm_rate
        FROM wide_project_monthly
        WHERE project_id = '{project_id}' AND report_month = '{report_month}'
        LIMIT 1
        """
        project_result = s.sql.query(project_sql)

        if project_result:
            row = project_result[0]
            warning_status = str(row.get("warning_status", "green"))
            return {
                "ok": True,
                "data": [{
                    "overall_status": warning_status,
                    "risk_indicators": [],
                    "diagnosis_result": f"项目【{row.get('project_name', '')}】整体运行正常，各项指标均在正常范围内。",
                    "improvement_actions": [],
                    "priority": "low"
                }],
                "row_count": 1
            }
        else:
            return {
                "ok": True,
                "data": [],
                "message": "No data found"
            }

    red_count = sum(1 for i in indicators if i.get("warning_level") == "red")
    yellow_count = sum(1 for i in indicators if i.get("warning_level") == "yellow")

    if red_count >= 2:
        overall_status = "red"
        priority = "high"
        diagnosis_result = f"项目存在{red_count}项红色预警指标和{yellow_count}项黄色预警指标，需要立即关注和处理。"
    elif yellow_count >= 2:
        overall_status = "yellow"
        priority = "medium"
        diagnosis_result = f"项目存在{yellow_count}项黄色预警指标，需要引起注意并采取改进措施。"
    elif red_count >= 1 or yellow_count >= 1:
        overall_status = "yellow"
        priority = "medium"
        diagnosis_result = f"项目存在{red_count if red_count else 0}项红色和{yellow_count}项黄色预警指标，需要关注。"
    else:
        overall_status = "green"
        priority = "low"
        diagnosis_result = "项目整体运行良好，各项指标均在正常范围内。"

    risk_indicators = []
    improvement_actions = []

    for ind in indicators:
        risk_indicators.append({
            "indicator_code": str(ind.get("indicator_code", "")),
            "indicator_name": str(ind.get("indicator_name", "")),
            "current_value": round(float(ind.get("current_value", 0) or 0), 4),
            "reference_value": str(ind.get("reference_value", "")),
            "warning_level": str(ind.get("warning_level", "green")),
            "issue_analysis": str(ind.get("issue_analysis", "")) if ind.get("issue_analysis") else "",
        })

        if ind.get("improvement"):
            improvement_actions.append({
                "indicator_code": str(ind.get("indicator_code", "")),
                "action": str(ind.get("improvement", "")),
                "priority": "high" if ind.get("warning_level") == "red" else "medium"
            })

    return {
        "ok": True,
        "data": [{
            "overall_status": overall_status,
            "risk_indicators": risk_indicators,
            "diagnosis_result": diagnosis_result,
            "improvement_actions": improvement_actions,
            "priority": priority
        }],
        "row_count": 1,
        "summary": {
            "red_count": red_count,
            "yellow_count": yellow_count,
            "total_indicators": len(indicators)
        }
    }
