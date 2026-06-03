SELECT
    p.科研项目,
    p.员工姓名,
    COALESCE(m.员工编码, -1) AS 员工编码,
    CASE WHEN m.员工编码 IS NOT NULL THEN '已匹配' ELSE '未匹配' END AS 匹配状态
FROM 项目人员拆分 p
LEFT JOIN 人员名单 m ON p.员工姓名 = m.员工姓名
ORDER BY p.科研项目, 匹配状态 DESC, p.员工姓名;