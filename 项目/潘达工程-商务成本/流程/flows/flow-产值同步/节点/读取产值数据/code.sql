SELECT 
    id,
    project_id,
    year,
    month,
    code,
    name,
    project_amount,
    company_amount,
    total,
    remark,
    status,
    create_time,
    create_by,
    update_time,
    update_by
FROM "tb_project_income_outcome_summary"
LIMIT 200000;