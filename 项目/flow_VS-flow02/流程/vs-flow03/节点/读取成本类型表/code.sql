-- spaceId = space__xsh_01
-- output_variable_name = 成本类型表
-- 主读 cost_type_info；维表暂无数据时从 budget_plan 补充 distinct 成本类型
SELECT id, name, code, category, unit, description
FROM cost_type_info
UNION ALL
SELECT
    cost_type AS id,
    cost_type AS name,
    cost_type AS code,
    cost_category AS category,
    '' AS unit,
    '' AS description
FROM (
    SELECT cost_type, cost_category
    FROM budget_plan
    WHERE cost_type IS NOT NULL
    GROUP BY cost_type, cost_category
) bp
WHERE bp.cost_type NOT IN (SELECT id FROM cost_type_info)
LIMIT 100000;
