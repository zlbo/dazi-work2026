"""Panda Construction Trigger Warning Action

功能：当指标超阈值时触发预警
参数：project_id, report_month, indicator_code, current_value, warning_level

放置位置：项目/onto_潘达工程_项目成本决策/脚本/actions/panda_action_trigger_warning.py
"""


def main(params: dict, context: dict) -> dict:
    """
    Action 入口。
    context 包含触发者信息、权限标签等。
    """
    s = space.get(ctx.space_id or "")

    project_id = params.get("project_id", "")
    report_month = params.get("report_month", "")
    indicator_code = params.get("indicator_code", "")
    current_value = params.get("current_value", 0)
    warning_level = params.get("warning_level", "green")
    issue_analysis = params.get("issue_analysis", "")
    improvement = params.get("improvement", "")

    if not project_id or not report_month or not indicator_code:
        return {"status": "error", "message": "project_id, report_month, and indicator_code are required"}

    indicator_id = f"IND_{project_id}_{report_month}_{indicator_code}"

    reference_values = {
        "10": "≥85%",
        "20": "≥75~80%",
        "30": "≥85%",
        "40": "≥95%",
        "50": "≥70%",
        "60": "根据合同约定",
        "70": "65%~80%",
    }

    indicator_names = {
        "10": "业主产值确权比",
        "20": "确权产值回款率",
        "30": "成本确权比",
        "40": "成本刚性度",
        "50": "产值现金流入比",
        "60": "成本资金收入比",
        "70": "成本资金支出比",
    }

    insert_sql = f"""
    INSERT INTO fact_risk_indicator (
        indicator_id, project_id, report_month, indicator_code, indicator_name,
        current_value, reference_value, warning_level, issue_analysis, improvement
    )
    VALUES (
        '{indicator_id}', '{project_id}', '{report_month}', '{indicator_code}',
        '{indicator_names.get(indicator_code, indicator_code)}',
        {current_value}, '{reference_values.get(indicator_code, "")}',
        '{warning_level}', '{issue_analysis}', '{improvement}'
    )
    """

    try:
        s.sql.execute(insert_sql)
    except Exception as e:
        return {"status": "error", "message": f"Failed to insert indicator: {str(e)}"}

    warning_count_sql = f"""
    SELECT
        project_id,
        countIf(warning_level = 'red') as red_count,
        countIf(warning_level = 'yellow') as yellow_count
    FROM fact_risk_indicator
    WHERE project_id = '{project_id}' AND report_month = '{report_month}'
    GROUP BY project_id
    """

    warning_counts = s.sql.query(warning_count_sql)

    overall_status = "green"
    if warning_counts:
        row = warning_counts[0]
        red_count = int(row.get("red_count", 0) or 0)
        yellow_count = int(row.get("yellow_count", 0) or 0)

        if red_count >= 2 or (red_count + yellow_count) >= 6:
            overall_status = "red"
        elif yellow_count >= 2 or (red_count + yellow_count) >= 2:
            overall_status = "yellow"

    update_status_sql = f"""
    INSERT INTO wide_project_monthly (project_id, report_month, warning_status)
    VALUES ('{project_id}', '{report_month}', '{overall_status}')
    """

    try:
        s.sql.execute(update_status_sql)
    except Exception as e:
        return {"status": "error", "message": f"Failed to update warning status: {str(e)}"}

    return {
        "status": "ok",
        "message": "Warning triggered successfully",
        "indicator_id": indicator_id,
        "project_id": project_id,
        "report_month": report_month,
        "indicator_code": indicator_code,
        "current_value": current_value,
        "warning_level": warning_level,
        "overall_status": overall_status
    }
