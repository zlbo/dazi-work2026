-- 上游表名 = 预算明细_2025
-- output_variable_name = 预算年度交易合计
SELECT
  *,
  COALESCE(交易金额_01月, 0) + COALESCE(交易金额_02月, 0) + COALESCE(交易金额_03月, 0)
    + COALESCE(交易金额_04月, 0) + COALESCE(交易金额_05月, 0) + COALESCE(交易金额_06月, 0)
    + COALESCE(交易金额_07月, 0) + COALESCE(交易金额_08月, 0) + COALESCE(交易金额_09月, 0)
    + COALESCE(交易金额_10月, 0) + COALESCE(交易金额_11月, 0) + COALESCE(交易金额_12月, 0)
    AS 交易金额_1至12月合计,
  COALESCE(本币金额_01月, 0) + COALESCE(本币金额_02月, 0) + COALESCE(本币金额_03月, 0)
    + COALESCE(本币金额_04月, 0) + COALESCE(本币金额_05月, 0) + COALESCE(本币金额_06月, 0)
    + COALESCE(本币金额_07月, 0) + COALESCE(本币金额_08月, 0) + COALESCE(本币金额_09月, 0)
    + COALESCE(本币金额_10月, 0) + COALESCE(本币金额_11月, 0) + COALESCE(本币金额_12月, 0)
    AS 本币金额_1至12月合计
FROM 预算明细_2025
