"""Panda Construction Update Output Action

功能：更新项目产值数据，触发相关计算
参数：project_id, report_month, output_amount, confirm_status, period_type

放置位置：项目/onto_潘达工程_项目成本决策/脚本/actions/panda_action_update_output.py
"""


def main(params: dict, context: dict) -> dict:
    """
    Action 入口。
    context 包含触发者信息、权限标签等。
    """
    s = space.get(ctx.space_id or "")

    project_id = params.get("project_id", "")
    report_month = params.get("report_month", "")
    output_amount = params.get("output_amount", 0)
    confirm_status = params.get("confirm_status", "unconfirmed")
    period_type = params.get("period_type", "this_year")

    if not project_id or not report_month:
        return {"status": "error", "message": "project_id and report_month are required"}

    output_id = f"OUT_{project_id}_{report_month}_{period_type}_{confirm_status}"

    insert_sql = f"""
    INSERT INTO fact_output_value (output_id, project_id, report_month, period_type, output_amount, confirm_status, output_date)
    VALUES ('{output_id}', '{project_id}', '{report_month}', '{period_type}', {output_amount}, '{confirm_status}', today())
    """

    try:
        s.sql.execute(insert_sql)
    except Exception as e:
        return {"status": "error", "message": f"Failed to insert output: {str(e)}"}

    update_wide_sql = f"""
    INSERT INTO wide_project_monthly (
        project_id, report_month,
        output_this_year_confirmed, output_this_year_unconfirmed, output_this_year_total,
        output_total_confirmed, output_total_unconfirmed, output_total_total,
        receivable_amount, receivable_ratio, received_amount
    )
    SELECT
        project_id,
        '{report_month}',
        SUM(CASE WHEN period_type = 'this_year' AND confirm_status = 'confirmed' THEN output_amount ELSE 0 END) as output_this_year_confirmed,
        SUM(CASE WHEN period_type = 'this_year' AND confirm_status = 'unconfirmed' THEN output_amount ELSE 0 END) as output_this_year_unconfirmed,
        SUM(CASE WHEN period_type = 'this_year' THEN output_amount ELSE 0 END) as output_this_year_total,
        SUM(CASE WHEN confirm_status = 'confirmed' THEN output_amount ELSE 0 END) as output_total_confirmed,
        SUM(CASE WHEN confirm_status = 'unconfirmed' THEN output_amount ELSE 0 END) as output_total_unconfirmed,
        SUM(output_amount) as output_total_total,
        SUM(output_amount) as receivable_amount,
        1.0 as receivable_ratio,
        0 as received_amount
    FROM fact_output_value
    WHERE project_id = '{project_id}' AND report_month = '{report_month}'
    GROUP BY project_id
    """

    try:
        s.sql.execute(update_wide_sql)
    except Exception as e:
        return {"status": "error", "message": f"Failed to update wide table: {str(e)}"}

    return {
        "status": "ok",
        "message": "Output updated successfully",
        "output_id": output_id,
        "project_id": project_id,
        "report_month": report_month,
        "output_amount": output_amount,
        "confirm_status": confirm_status
    }
