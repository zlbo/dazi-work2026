"""测试 CREATE TABLE 带 COMMENT"""

def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)

    # 先删除测试表
    s.sql.execute("DROP TABLE IF EXISTS test_comment")

    # 创建带 COMMENT 的表
    s.sql.execute("""
        CREATE TABLE test_comment (
            id String COMMENT '记录ID',
            name String COMMENT '名称',
            amount Float64 COMMENT '金额',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (id)
    """)

    output.print("OK test_comment 创建完成")

    # 验证
    result = s.sql.query("""
        SELECT name, comment
        FROM system.columns
        WHERE database = 'space__panda_construction'
          AND table = 'test_comment'
        ORDER BY name
    """)

    output.print("\n=== 验证字段 COMMENT ===")
    for row in result:
        output.print(f"字段: {row.get('name')} | COMMENT: {row.get('comment')}")

    # 清理
    s.sql.execute("DROP TABLE IF EXISTS test_comment")
    output.print("\n测试完成，已清理")
