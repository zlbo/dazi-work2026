SELECT 
    project_id,
    report_period,
    cost_confirmed_acc,
    cost_unconfirmed_acc,
    labor_cost_acc,
    material_cost_acc,
    equipment_cost_acc,
    management_fee_rate
FROM tb_project_cost
WHERE report_period = '{{report_period}}';