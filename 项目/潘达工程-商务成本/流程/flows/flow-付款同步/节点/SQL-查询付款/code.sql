SELECT 
    project_id,
    report_period,
    paid_amount,
    payable_confirmed,
    payable_unconfirmed,
    paid_amount_last_year,
    payment_rate
FROM tb_project_payment
WHERE report_period = '{{report_period}}';