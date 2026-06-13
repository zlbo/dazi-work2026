SELECT 
    id,
    project_id,
    contract_id,
    year,
    month,
    equipment_code,
    equipment_name,
    equipment_type,
    equipment_value,
    purchase_date,
    equipment_status,
    depreciation_method,
    create_time,
    update_time
FROM "tb_project_cost_equipment_detail"
LIMIT 200000;