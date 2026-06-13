SELECT 
    id,
    project_id,
    contract_id,
    year,
    month,
    base_contract_code,
    base_contract_name,
    base_contract_amount,
    base_contract_pay_ratio,
    base_contract_tax_rate,
    base_contract_is_settlement,
    cost_actual_confirmed_acc,
    cost_actual_unconfirmed_acc,
    cost_actual_labor_acc,
    fund_plan_approve_amount,
    pay_amount_acc,
    pay_ratio_acc,
    create_time,
    update_time
FROM "tb_project_cost_pay_detail"
LIMIT 200000;
