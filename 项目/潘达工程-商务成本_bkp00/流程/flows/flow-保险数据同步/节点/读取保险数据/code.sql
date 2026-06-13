SELECT 
    id,
    project_id,
    contract_id,
    year,
    month,
    insurance_type,
    insurance_amount,
    insurance_date,
    expire_date,
    insurance_status,
    insurance_company,
    create_time,
    update_time
FROM "tb_project_cost_insurance_detail"
LIMIT 200000;