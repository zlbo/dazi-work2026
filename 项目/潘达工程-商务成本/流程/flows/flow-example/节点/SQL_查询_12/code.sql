SELECT 
    fa.*,
    daa.account_name,
    daa.account_type,
    daa.parent_code,
    daa.level,
    daa.is_active,
    daa.erp_code,
    daa.description
FROM 
    fact_actual fa
JOIN 
    dim_actual_account daa
ON 
    fa.actual_account_code = daa.account_code;
