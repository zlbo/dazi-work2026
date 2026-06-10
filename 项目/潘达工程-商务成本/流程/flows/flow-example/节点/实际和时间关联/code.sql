SELECT 
  "fact_actual"."id",
  "fact_actual"."date_key",
  "dim_time"."month",
  "fact_actual"."actual_account_code",
  "fact_actual"."amount",
  "fact_actual"."quantity",
  "fact_actual"."department",
  "fact_actual"."product_line",
  "fact_actual"."created_at",
  "fact_actual"."voucher_no",
  "fact_actual"."region"
FROM "fact_actual"
INNER JOIN "dim_time" ON "fact_actual"."date_key" = "dim_time"."date_key";