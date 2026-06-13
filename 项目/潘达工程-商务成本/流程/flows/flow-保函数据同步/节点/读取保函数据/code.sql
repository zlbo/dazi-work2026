SELECT 
    id,
    project_id,
    contract_id,
    year,
    month,
    guarantee_type,
    guarantee_amount,
    guarantee_date,
    expire_date,
    guarantee_status,
    create_time,
    update_time
FROM "tb_project_cost_guarantee_detail"
LIMIT 200000;