SELECT account_code,
    account_name,
    account_type,
    parent_code,
    level,
    report_order,
    is_active,
    description,
    created_at 
FROM dim_budget_account
LIMIT 200000