SELECT account_code,
    account_name,
    account_type,
    parent_code,
    level,
    is_active,
    erp_code,
    description,
    created_at 
FROM dim_actual_account
LIMIT 200000