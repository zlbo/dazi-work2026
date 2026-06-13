SELECT 
    id,
    project_id,
    contract_id,
    year,
    month,
    compensation_type,
    compensation_amount,
    compensation_date,
    compensation_reason,
    compensation_status,
    create_time,
    update_time
FROM "tb_project_cost_compensation_detail"
LIMIT 200000;