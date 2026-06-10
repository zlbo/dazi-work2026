"""删除所有商务成本相关表"""

def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)

    tables_to_drop = [
        "dim_region",
        "dim_department",
        "dim_owner",
        "dim_cost_subject",
        "dim_project",
        "dim_company",
        "dim_supplier",
        "dim_contract",
        "fact_project_output",
        "fact_project_cost",
        "fact_project_indicator",
        "fact_project_payment",
        "fact_project_balance",
        "fact_project_risk",
    ]

    for tbl in tables_to_drop:
        try:
            s.sql.execute(f"DROP TABLE IF EXISTS {tbl}")
            output.print(f"DROP OK: {tbl}")
        except Exception as e:
            output.print(f"DROP FAILED: {tbl} - {e}")

    output.print("\n全部删除完成")
