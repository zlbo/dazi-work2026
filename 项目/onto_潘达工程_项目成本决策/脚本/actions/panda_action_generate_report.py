"""Panda Construction Generate Report Action

功能：生成项目月度经营报表
参数：report_month

放置位置：项目/onto_潘达工程_项目成本决策/脚本/actions/panda_action_generate_report.py
"""


def main(params: dict, context: dict) -> dict:
    """
    Action 入口。
    context 包含触发者信息、权限标签等。
    """
    s = space.get(ctx.space_id or "")

    report_month = params.get("report_month", "")

    if not report_month:
        return {"status": "error", "message": "report_month is required"}

    generate_sql = f"""
    INSERT INTO wide_project_monthly (
        project_id, report_month, project_name, project_status, customer_system,
        management_rate, profession, is_large_customer, operation_mode, region,
        project_scale, contract_amount, owner_name,
        output_last_year, output_this_year_confirmed, output_this_year_unconfirmed,
        output_this_year_total, output_this_month_confirmed, output_this_month_unconfirmed,
        output_this_month_total, output_total_confirmed, output_total_unconfirmed,
        output_total_total, receivable_amount, receivable_ratio, received_amount,
        cost_confirmed, cost_total, profit_confirmed, profit_total,
        profit_rate_confirmed, profit_rate_total, warning_status
    )
    SELECT
        p.project_id,
        '{report_month}',
        p.project_name,
        p.project_status,
        p.customer_system,
        p.management_rate,
        p.profession,
        p.is_large_customer,
        p.operation_mode,
        p.region,
        p.project_scale,
        p.contract_amount,
        o.owner_name,
        COALESCE(ov_last.output_last_year, 0) as output_last_year,
        COALESCE(ov_ty_c.output_this_year_confirmed, 0) as output_this_year_confirmed,
        COALESCE(ov_ty_u.output_this_year_unconfirmed, 0) as output_this_year_unconfirmed,
        COALESCE(ov_ty_c.output_this_year_confirmed, 0) + COALESCE(ov_ty_u.output_this_year_unconfirmed, 0) as output_this_year_total,
        COALESCE(ov_tm_c.output_this_month_confirmed, 0) as output_this_month_confirmed,
        COALESCE(ov_tm_u.output_this_month_unconfirmed, 0) as output_this_month_unconfirmed,
        COALESCE(ov_tm_c.output_this_month_confirmed, 0) + COALESCE(ov_tm_u.output_this_month_unconfirmed, 0) as output_this_month_total,
        COALESCE(ov_all_c.output_total_confirmed, 0) as output_total_confirmed,
        COALESCE(ov_all_u.output_total_unconfirmed, 0) as output_total_unconfirmed,
        COALESCE(ov_all_c.output_total_confirmed, 0) + COALESCE(ov_all_u.output_total_unconfirmed, 0) as output_total_total,
        COALESCE(ov_all_c.output_total_confirmed, 0) as receivable_amount,
        1.0 as receivable_ratio,
        COALESCE(py.received_amount, 0) as received_amount,
        COALESCE(cr.cost_confirmed, 0) as cost_confirmed,
        COALESCE(cr.cost_total, 0) as cost_total,
        COALESCE(ov_all_c.output_total_confirmed, 0) - COALESCE(cr.cost_confirmed, 0) as profit_confirmed,
        COALESCE(ov_all_c.output_total_confirmed, 0) + COALESCE(ov_all_u.output_total_unconfirmed, 0) - COALESCE(cr.cost_total, 0) as profit_total,
        CASE WHEN COALESCE(ov_all_c.output_total_confirmed, 0) > 0
            THEN (COALESCE(ov_all_c.output_total_confirmed, 0) - COALESCE(cr.cost_confirmed, 0)) / COALESCE(ov_all_c.output_total_confirmed, 0)
            ELSE 0 END as profit_rate_confirmed,
        CASE WHEN (COALESCE(ov_all_c.output_total_confirmed, 0) + COALESCE(ov_all_u.output_total_unconfirmed, 0)) > 0
            THEN (COALESCE(ov_all_c.output_total_confirmed, 0) + COALESCE(ov_all_u.output_total_unconfirmed, 0) - COALESCE(cr.cost_total, 0)) / (COALESCE(ov_all_c.output_total_confirmed, 0) + COALESCE(ov_all_u.output_total_unconfirmed, 0))
            ELSE 0 END as profit_rate_total,
        CASE
            WHEN (SELECT count() FROM fact_risk_indicator ri WHERE ri.project_id = p.project_id AND ri.report_month = '{report_month}' AND ri.warning_level = 'red') >= 2 THEN 'red'
            WHEN (SELECT count() FROM fact_risk_indicator ri WHERE ri.project_id = p.project_id AND ri.report_month = '{report_month}' AND ri.warning_level IN ('red', 'yellow')) >= 2 THEN 'yellow'
            ELSE 'green'
        END as warning_status
    FROM dim_project p
    LEFT JOIN dim_owner o ON p.owner_id = o.owner_id
    LEFT JOIN (
        SELECT project_id, SUM(output_amount) as output_last_year
        FROM fact_output_value
        WHERE report_month < '{report_month}' AND period_type = 'last_year'
        GROUP BY project_id
    ) ov_last ON p.project_id = ov_last.project_id
    LEFT JOIN (
        SELECT project_id, SUM(output_amount) as output_this_year_confirmed
        FROM fact_output_value
        WHERE report_month = '{report_month}' AND period_type = 'this_year' AND confirm_status = 'confirmed'
        GROUP BY project_id
    ) ov_ty_c ON p.project_id = ov_ty_c.project_id
    LEFT JOIN (
        SELECT project_id, SUM(output_amount) as output_this_year_unconfirmed
        FROM fact_output_value
        WHERE report_month = '{report_month}' AND period_type = 'this_year' AND confirm_status = 'unconfirmed'
        GROUP BY project_id
    ) ov_ty_u ON p.project_id = ov_ty_u.project_id
    LEFT JOIN (
        SELECT project_id, SUM(output_amount) as output_this_month_confirmed
        FROM fact_output_value
        WHERE report_month = '{report_month}' AND period_type = 'this_month' AND confirm_status = 'confirmed'
        GROUP BY project_id
    ) ov_tm_c ON p.project_id = ov_tm_c.project_id
    LEFT JOIN (
        SELECT project_id, SUM(output_amount) as output_this_month_unconfirmed
        FROM fact_output_value
        WHERE report_month = '{report_month}' AND period_type = 'this_month' AND confirm_status = 'unconfirmed'
        GROUP BY project_id
    ) ov_tm_u ON p.project_id = ov_tm_u.project_id
    LEFT JOIN (
        SELECT project_id, SUM(output_amount) as output_total_confirmed
        FROM fact_output_value
        WHERE period_type = 'this_year' AND confirm_status = 'confirmed'
        GROUP BY project_id
    ) ov_all_c ON p.project_id = ov_all_c.project_id
    LEFT JOIN (
        SELECT project_id, SUM(output_amount) as output_total_unconfirmed
        FROM fact_output_value
        WHERE period_type = 'this_year' AND confirm_status = 'unconfirmed'
        GROUP BY project_id
    ) ov_all_u ON p.project_id = ov_all_u.project_id
    LEFT JOIN (
        SELECT project_id, SUM(payment_amount) as received_amount
        FROM fact_payment
        WHERE report_month = '{report_month}' AND payment_type = 'owner'
        GROUP BY project_id
    ) py ON p.project_id = py.project_id
    LEFT JOIN (
        SELECT project_id,
            SUM(CASE WHEN confirm_status = 'confirmed' THEN cost_amount ELSE 0 END) as cost_confirmed,
            SUM(cost_amount) as cost_total
        FROM fact_cost_record
        WHERE report_month = '{report_month}'
        GROUP BY project_id
    ) cr ON p.project_id = cr.project_id
    """

    try:
        s.sql.execute(generate_sql)
    except Exception as e:
        return {"status": "error", "message": f"Failed to generate report: {str(e)}"}

    count_sql = f"""
    SELECT count() as project_count
    FROM wide_project_monthly
    WHERE report_month = '{report_month}'
    """

    result = s.sql.query(count_sql)
    project_count = result[0].get("project_count", 0) if result else 0

    return {
        "status": "ok",
        "message": f"Report generated successfully for {report_month}",
        "report_month": report_month,
        "project_count": project_count
    }
