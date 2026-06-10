SELECT id,
    date_key,
    budget_account_code,
    budget_amount,
    budget_version,
    budget_type,
    created_at,
    updated_at,
    created_by,
    remarks 
FROM fact_budget
LIMIT 200000