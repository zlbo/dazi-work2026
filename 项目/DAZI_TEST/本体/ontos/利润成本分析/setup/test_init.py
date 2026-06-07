"""测试初始化脚本 — 不含 apply_registry（分类见 profit_cost_category_mount.py）"""

def main():
    space_id = "space_cate_test01"
    s = space.get(space_id)

    output.print("=== 测试初始化（仅验证 space 连接）===")
    output.print(f"空间: {space_id}")
    output.print("分类挂载请 run setup/profit_cost_category_mount.py")
    output.print("=== 测试完成 ===")
