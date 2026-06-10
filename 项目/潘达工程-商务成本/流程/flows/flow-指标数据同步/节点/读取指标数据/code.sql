SELECT 
    id,
    project_id,
    year,
    month,
    code,
    title,
    value,
    value_type,
    remark,
    status
FROM "tb_project_indicator"
LIMIT 200000;
