SELECT 
    id,
    project_id,
    contract_id,
    year,
    month,
    base_contract_code,
    base_contract_name,
    base_contract_amount,
    settlement_amount,
    settlement_date,
    settlement_status,
    create_time,
    update_time
FROM "tb_project_cost_settlement_detail"
LIMIT 200000;