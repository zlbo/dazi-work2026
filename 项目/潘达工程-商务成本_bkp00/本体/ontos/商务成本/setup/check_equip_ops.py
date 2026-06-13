"""检查设备运营示例的表字段显示名"""

def main():
    # 检查设备运营示例的 space
    space_id = "space_cate_test01"
    s = space.get(space_id)

    output.print("=== 检查 dim_plant 字段元数据 ===")
    result = s.sql.query("""
        SELECT name as column_name, comment as display_name
        FROM system.columns
        WHERE database = 'space_cate_test01'
          AND table = 'dim_plant'
        ORDER BY name
    """)

    for row in result:
        output.print(f"字段: {row.get('column_name', 'N/A')} | 显示名: {row.get('display_name', '(空)')}")
