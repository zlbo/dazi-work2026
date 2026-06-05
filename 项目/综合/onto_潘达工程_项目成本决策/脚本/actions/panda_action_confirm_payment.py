"""Panda Construction Confirm Payment Action

功能：确认项目收款
参数：project_id, report_month, payment_amount, payment_type

放置位置：项目/onto_潘达工程_项目成本决策/脚本/actions/panda_action_confirm_payment.py
"""


def main(params: dict, context: dict) -> dict:
    """
    Action 入口。
    context 包含触发者信息、权限标签等。
    """
    s = space.get(ctx.space_id or "")

    project_id = params.get("project_id", "")
    report_month = params.get("report_month", "")
    payment_amount = params.get("payment_amount", 0)
    payment_type = params.get("payment_type", "owner")

    if not project_id or not report_month:
        return {"status": "error", "message": "project_id and report_month are required"}

    payment_id = f"PAY_{project_id}_{report_month}_{payment_type}"

    insert_sql = f"""
    INSERT INTO fact_payment (payment_id, project_id, report_month, payment_amount, payment_type, payment_date)
    VALUES ('{payment_id}', '{project_id}', '{report_month}', {payment_amount}, '{payment_type}', today())
    """

    try:
        s.sql.execute(insert_sql)
    except Exception as e:
        return {"status": "error", "message": f"Failed to insert payment: {str(e)}"}

    update_wide_sql = f"""
    INSERT INTO wide_project_monthly (
        project_id, report_month,
        received_amount
    )
    SELECT
        project_id,
        '{report_month}',
        SUM(CASE WHEN payment_type = 'owner' THEN payment_amount ELSE 0 END) as received_amount
    FROM fact_payment
    WHERE project_id = '{project_id}' AND report_month = '{report_month}'
    GROUP BY project_id
    """

    try:
        s.sql.execute(update_wide_sql)
    except Exception as e:
        return {"status": "error", "message": f"Failed to update wide table: {str(e)}"}

    return {
        "status": "ok",
        "message": "Payment confirmed successfully",
        "payment_id": payment_id,
        "project_id": project_id,
        "report_month": report_month,
        "payment_amount": payment_amount,
        "payment_type": payment_type
    }
