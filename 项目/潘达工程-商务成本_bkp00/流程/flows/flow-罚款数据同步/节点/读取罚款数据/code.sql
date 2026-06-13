SELECT 
    id,
    project_id,
    contract_id,
    year,
    month,
    fine_type,
    fine_amount,
    fine_date,
    fine_reason,
    fine_status,
    create_time,
    update_time
FROM "tb_project_cost_fine_detail"
LIMIT 200000;