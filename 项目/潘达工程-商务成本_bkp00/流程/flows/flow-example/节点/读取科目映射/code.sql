SELECT mapping_id,
    actual_account_code,
    budget_account_code,
    allocation_percent,
    allocation_method,
    effective_from,
    effective_to,
    is_active,
    created_by,
    created_at,
    updated_at,
    remarks 
FROM dim_account_mapping
LIMIT 200000