-- 上游变量：销售表、产品表、规格表
-- 本节点 output_variable_name = 销售明细宽表
SELECT
    s.ID          AS 销售ID,
    s.地区,
    s.产品        AS 产品ID,
    p.名称        AS 产品名称,
    p.说明        AS 产品说明,
    s.规格        AS 规格ID,
    g.名称        AS 规格名称,
    g.说明        AS 规格说明,
    s.颜色,
    s.数量,
    s.金额,
    s.日期
FROM 销售表 s
LEFT JOIN 产品表 p
    ON CAST(s.产品 AS VARCHAR) = CAST(p.ID AS VARCHAR)
LEFT JOIN 规格表 g
    ON CAST(s.规格 AS VARCHAR) = CAST(g.ID AS VARCHAR)
