-- 上游变量：成本中心表、成本类型表
-- 本节点 output_variable_name = 成本中心类型宽表
-- 按矿区关联成本中心与成本类型（维表组合宽表）
SELECT
    cc.id              AS 成本中心ID,
    cc.name            AS 成本中心名称,
    cc.code            AS 成本中心编码,
    cc.mine_area       AS 矿区,
    cc.status          AS 成本中心状态,
    ct.id              AS 成本类型ID,
    ct.name            AS 成本类型名称,
    ct.code            AS 成本类型编码,
    ct.category        AS 成本类别,
    ct.unit            AS 计量单位,
    ct.description     AS 成本类型说明
FROM 成本中心表 cc
CROSS JOIN 成本类型表 ct
