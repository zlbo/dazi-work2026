SELECT project_id,
    report_period,
    output_confirmed,
    output_unconfirmed,
    output_last_year_confirmed,
    output_last_year_unconfirmed
FROM tb_project_output
LIMIT 200000
