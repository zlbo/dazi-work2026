"""检查表字段显示名注册情况"""

def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)

    # 先查看所有表
    output.print("=== 查看 space__panda_construction 数据库的表 ===")
    result = s.sql.query("""
        SELECT database, table, name as column_name, comment as display_name
        FROM system.columns 
        WHERE database = 'space__panda_construction'
        ORDER BY table, column_name
        LIMIT 200
    """)
    
    # 按表分组显示
    current_table = None
    for row in result:
        tbl = row.get('table', '')
        if tbl != current_table:
            output.print(f"\n>>> 表: {tbl}")
            current_table = tbl
        col_name = row.get('column_name', 'N/A')
        display = row.get('display_name', '')
        if display:
            output.print(f"    {col_name} -> {display}")
        else:
            output.print(f"    {col_name} -> (无显示名)")
