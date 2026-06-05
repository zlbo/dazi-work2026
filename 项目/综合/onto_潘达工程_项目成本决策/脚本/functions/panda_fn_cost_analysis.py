"""Panda Construction Cost Analysis Function

功能：分析项目成本构成及占比
参数：project_id, report_month
返回：成本结构分析数据

放置位置：项目/onto_潘达工程_项目成本决策/脚本/functions/panda_fn_cost_analysis.py
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

    where_clause = f"WHERE project_id = '{project_id}' AND report_month = '{report_month}'"

    sql = f"""
    SELECT
        project_id,
        report_month,
        contract_amount,
        cost_confirmed,
        cost_total
    FROM wide_project_monthly
    {where_clause}
    LIMIT 1
    """

    result = s.sql.query(sql)

    if not result:
        return {
            "ok": True,
            "data": [],
            "message": "No data found for the specified project and month"
        }

    row = result[0]
    cost_total = float(row.get("cost_total", 0) or 0)
    contract_amount = float(row.get("contract_amount", 0) or 0)

    cost_type_sql = f"""
    SELECT
        cost_type,
        SUM(cost_amount) as cost_amount,
        MAX(confirm_status) as confirm_status
    FROM fact_cost_record
    WHERE project_id = '{project_id}' AND report_month = '{report_month}'
    GROUP BY cost_type
    ORDER BY cost_amount DESC
    """

    cost_types = s.sql.query(cost_type_sql)

    data = []
    for cost_row in cost_types:
        cost_amount = float(cost_row.get("cost_amount", 0) or 0)
        cost_ratio = 0.0
        if cost_total > 0:
            cost_ratio = round(cost_amount / cost_total, 4)

        deviation = cost_amount - (contract_amount * 0.6)
        deviation_rate = 0.0
        if contract_amount > 0:
            deviation_rate = round(deviation / (contract_amount * 0.6), 4)

        data.append({
            "cost_type": str(cost_row.get("cost_type", "")),
            "cost_amount": round(cost_amount, 2),
            "cost_ratio": cost_ratio,
            "target_cost": round(contract_amount * 0.6, 2),
            "deviation": round(deviation, 2),
            "deviation_rate": deviation_rate,
            "confirm_status": str(cost_row.get("confirm_status", "")),
        })

    return {
        "ok": True,
        "data": data,
        "row_count": len(data),
        "summary": {
            "cost_total": round(cost_total, 2),
            "target_cost": round(contract_amount * 0.6, 2),
            "cost_type_count": len(data)
        }
    }
