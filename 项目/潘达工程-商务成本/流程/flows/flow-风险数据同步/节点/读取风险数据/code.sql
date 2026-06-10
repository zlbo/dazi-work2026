SELECT 
    id,
    project_id,
    year,
    month,
    risk_type,
    code,
    name,
    value,
    value_type,
    value_remark,
    warning,
    analyse_reason,
    analyse_correction,
    remark
FROM "tb_project_risk_list_analyse"
LIMIT 200000;
