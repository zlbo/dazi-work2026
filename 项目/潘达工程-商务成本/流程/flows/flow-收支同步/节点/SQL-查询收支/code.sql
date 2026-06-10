SELECT 
    project_id,
    report_period,
    income_total,
    outcome_total,
    income_confirmed,
    outcome_confirmed,
    balance_amount
FROM tb_project_balance
WHERE report_period = '{{report_period}}';