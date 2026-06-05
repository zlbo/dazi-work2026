-- 生产指挥中心 KPI（sql_asset 模板示例）
SELECT
    '今日产量' AS label,
    toFloat64(12500) AS value,
    '件' AS unit
UNION ALL
SELECT '计划达成', toFloat64(96.8), '%'
UNION ALL
SELECT '一次合格率', toFloat64(99.1), '%'
