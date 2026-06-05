-- spaceId = space__xsh_01
-- output_variable_name = 成本中心表
-- 主读 cost_center_info；维表暂无数据时从 budget_plan 补充 distinct 成本中心
SELECT id, name, code, parent_id, mine_area, status
FROM cost_center_info
UNION ALL
SELECT
    cost_center AS id,
    cost_center AS name,
    cost_center AS code,
    '' AS parent_id,
    mine_area,
    'active' AS status
FROM (
    SELECT cost_center, mine_area
    FROM budget_plan
    WHERE cost_center IS NOT NULL
    GROUP BY cost_center, mine_area
) bp
WHERE bp.cost_center NOT IN (SELECT id FROM cost_center_info)
LIMIT 100000;
