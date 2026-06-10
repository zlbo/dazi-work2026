SELECT 
    id,
    project_id,
    project_name,
    contract_no,
    contract_name,
    payee_name,
    payee_account,
    pay_amount,
    pay_date,
    pay_type,
    pay_status,
    report_period,
    created_at,
    updated_at
FROM tb_payment_record
LIMIT 200000;