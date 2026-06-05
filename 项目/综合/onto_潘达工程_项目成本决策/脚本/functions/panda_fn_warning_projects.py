"""Panda Construction Warning Projects Function

功能：获取指定预警等级的项目列表
参数：report_month, warning_level（可选）
返回：预警项目列表

放置位置：项目/onto_潘达工程_项目成本决策/脚本/functions/panda_fn_warning_projects.py
"""


def main(params: dict) -> dict:
    """
    函数入口，params 由平台传入。
    """
    s = space.get(ctx.space_id or "")

    report_month = params.get("report_month", "")
    warning_level = params.get("warning_level", "")

    if not report_month:
        return {
            "ok": False,
            "error": "report_month is required",
            "data": []
        }

    where_clause = f"WHERE report_month = '{report_month}'"
    if warning_level:
        where_clause += f" AND warning_status = '{warning_level}'"

    sql = f"""
    SELECT
        project_id,
        project_name,
        warning_status,
        profit_rate_total,
        profit_rate_confirmed,
        output_total_total,
        cost_total,
        receivable_ratio,
        received_amount,
        receivable_amount,
        region,
        operation_mode,
        is_large_customer
    FROM wide_project_monthly
    {where_clause}
    ORDER BY
        CASE warning_status
            WHEN 'red' THEN 1
            WHEN 'yellow' THEN 2
            WHEN 'green' THEN 3
        END,
        profit_rate_total ASC,
        receivable_ratio ASC
    LIMIT 100
    """

    result = s.sql.query(sql)

    if not result:
        return {
            "ok": True,
            "data": [],
            "message": "No warning projects found"
        }

    indicator_sql = f"""
    SELECT
        project_id,
        indicator_code,
        indicator_name,
        warning_level,
        current_value,
        issue_analysis
    FROM fact_risk_indicator
    WHERE report_month = '{report_month}' AND warning_level != 'green'
    ORDER BY project_id, warning_level DESC, indicator_code
    """

    all_indicators = s.sql.query(indicator_sql)

    project_indicators = {}
    for ind in all_indicators:
        pid = ind.get("project_id", "")
        if pid not in project_indicators:
            project_indicators[pid] = []
        project_indicators[pid].append({
            "indicator_code": str(ind.get("indicator_code", "")),
            "indicator_name": str(ind.get("indicator_name", "")),
            "warning_level": str(ind.get("warning_level", "")),
            "current_value": round(float(ind.get("current_value", 0) or 0), 4),
            "issue_analysis": str(ind.get("issue_analysis", "")) if ind.get("issue_analysis") else ""
        })

    data = []
    for row in result:
        pid = row.get("project_id", "")
        indicators = project_indicators.get(pid, [])

        red_count = sum(1 for i in indicators if i.get("warning_level") == "red")
        yellow_count = sum(1 for i in indicators if i.get("warning_level") == "yellow")

        main_issues = []
        for i in indicators[:3]:
            if i.get("issue_analysis"):
                main_issues.append(i.get("issue_analysis"))

        data.append({
            "project_id": str(pid),
            "project_name": str(row.get("project_name", "")),
            "warning_level": str(row.get("warning_status", "green")),
            "warning_count": red_count + yellow_count,
            "red_count": red_count,
            "yellow_count": yellow_count,
            "profit_rate": round(float(row.get("profit_rate_total", 0) or 0), 4),
            "collection_rate": round(float(row.get("receivable_ratio", 0) or 0) if row.get("receivable_ratio") else 0, 4),
            "output_total": round(float(row.get("output_total_total", 0) or 0), 2),
            "cost_total": round(float(row.get("cost_total", 0) or 0), 2),
            "region": str(row.get("region", "")),
            "operation_mode": str(row.get("operation_mode", "")),
            "is_large_customer": "是" if row.get("is_large_customer") else "否",
            "main_issues": "; ".join(main_issues) if main_issues else "",
            "indicators": indicators[:5]
        })

    return {
        "ok": True,
        "data": data,
        "row_count": len(data),
        "summary": {
            "total_projects": len(data),
            "red_projects": sum(1 for d in data if d.get("warning_level") == "red"),
            "yellow_projects": sum(1 for d in data if d.get("warning_level") == "yellow")
        }
    }
