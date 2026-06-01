"""
本体脚本入口（本地语法检查用，不连接平台）

完整流程见 脚本/README.md：
  1. setup/sales_ontology_init.py
  2. setup/sales_seed_data.py
  3. setup/training_ontology_init.py
  4. setup/training_seed_data.py
  5. functions/sales_fn_*.py（发布为 ontology_function）
  6. functions/training_fn_*.py（发布为 ontology_function）
"""


def main() -> None:
    print("本体脚本入口")
    print("产品销售本体：")
    print("  - setup/sales_ontology_init.py")
    print("  - setup/sales_seed_data.py")
    print("  - functions/sales_fn_*.py")
    print("员工培训本体：")
    print("  - setup/training_ontology_init.py")
    print("  - setup/training_seed_data.py")
    print("  - functions/training_fn_*.py")
    print("请通过 dazi-onto script publish 发布脚本")
    print("空间: space__0519")


if __name__ == "__main__":
    main()