SELECT 
    id,
    project_id,
    contract_id,
    year,
    month,
    name,
    cost_code,
    level,
    base_contract_amount,
    cost_actual_confirmed_acc,
    cost_actual_unconfirmed_acc,
    cost_actual_confirmed_cmonth,
    cost_actual_unconfirmed_cmonth,
    cost_actual_labor_acc
FROM "tb_project_cost_pay_detail"
LIMIT 200000;
