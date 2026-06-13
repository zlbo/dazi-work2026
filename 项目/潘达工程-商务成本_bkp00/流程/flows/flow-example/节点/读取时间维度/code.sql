SELECT date_key,
    date_date,
    year,
    quarter,
    month,
    month_name,
    week,
    day_of_month,
    day_of_week,
    is_weekend,
    is_holiday,
    fiscal_year,
    fiscal_period 
FROM dim_time
LIMIT 200000