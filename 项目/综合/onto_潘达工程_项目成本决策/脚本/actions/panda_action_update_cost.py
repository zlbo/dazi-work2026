"""Panda Construction Update Cost Action

功能：更新项目成本数据
参数：project_id, report_month, cost_amount, cost_type, confirm_status

放置位置：项目/onto_潘达工程_项目成本决策/脚本/actions/panda_action_update_cost.py
"""


def main(params: dict, context: dict) -> dict:
    """
    Action 入口。
    context 包含触发者信息、权限标签等。
    """
    s = space.get(ctx.space_id or "")

    project_id = params.get("project_id", "")
    report_month = params.get("report_month", "")
    cost_amount = params.get("cost_amount", 0)
    cost_type = params.get("cost_type", "unknown")
    confirm_status = params.get("confirm_status", "unconfirmed")

    if not project_id or not report_month:
        return {"status": "error", "message": "project_id and report_month are required"}

    cost_id = f"COST_{project_id}_{report_month}_{cost_type}_{confirm_status}"

    insert_sql = f"""
    INSERT INTO fact_cost_record (cost_id, project_id, report_month, cost_type, cost_amount, confirm_status, cost_date)
    VALUES ('{cost_id}', '{project_id}', '{report_month}', '{cost_type}', {cost_amount}, '{confirm_status}', today())
    """

    try:
        s.sql.execute(insert_sql)
    except Exception as e:
        return {"status": "error", "message": f"Failed to insert cost: {str(e)}"}

    update_wide_sql = f"""
    INSERT INTO wide_project_monthly (
        project_id, report_month,
        cost_confirmed, cost_total
    )
    SELECT
        project_id,
        '{report_month}',
        SUM(CASE WHEN confirm_status = 'confirmed' THEN cost_amount ELSE 0 END) as cost_confirmed,
        SUM(cost_amount) as cost_total
    FROM fact_cost_record
    WHERE project_id = '{project_id}' AND report_month = '{report_month}'
    GROUP BY project_id
    """

    try:
        s.sql.execute(update_wide_sql)
    except Exception as e:
        return {"status": "error", "message": f"Failed to update wide table: {str(e)}"}

    return {
        "status": "ok",
        "message": "Cost updated successfully",
        "cost_id": cost_id,
        "project_id": project_id,
        "report_month": report_month,
        "cost_amount": cost_amount,
        "cost_type": cost_type,
        "confirm_status": confirm_status
    }
