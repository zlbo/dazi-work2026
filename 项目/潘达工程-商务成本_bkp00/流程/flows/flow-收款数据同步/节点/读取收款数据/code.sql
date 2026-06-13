SELECT 
    id,
    project_id,
    contract_id,
    year,
    month,
    base_contract_code,
    base_contract_name,
    base_contract_amount,
    receipt_amount_acc,
    receipt_ratio_acc,
    create_time,
    update_time
FROM "tb_project_cost_receipt_detail"
LIMIT 200000;