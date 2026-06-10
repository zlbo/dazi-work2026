SELECT id,
    date_key,
    actual_account_code,
    amount,
    quantity,
    department,
    product_line,
    region,
    voucher_no,
    created_at 
FROM fact_actual
LIMIT 200000