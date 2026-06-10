SELECT 
    id,
    project_id,
    project_name,
    cost_item_code,
    cost_item_name,
    contract_no,
    contract_name,
    pay_date,
    pay_amount,
    tax_amount,
    total_amount,
    pay_type,
    pay_status,
    report_period,
    created_at,
    updated_at
FROM tb_project_cost_pay_detail
LIMIT 200000;