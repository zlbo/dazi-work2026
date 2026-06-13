"""商务成本本体分类挂载脚本

放置：项目/潘达工程-商务成本/本体/ontos/商务成本/setup/commercial_cost_category_mount.py
发布：dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/商务成本/setup/commercial_cost_category_mount.py --space space__panda_construction --type category
"""

def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)

    output.print("=== 商务成本本体分类挂载 ===")

    # 平台分类注册（与规划附录B对齐）
    CATEGORY_REGISTRY = {
        "table": {
            "维度表": [
                "dim_date",
                "dim_project",
                "dim_contract",
                "dim_owner",
                "dim_cost_subject",
                "dim_region",
                "dim_organization",
                "dim_project_status",
                "dim_contract_status",
                "dim_project_category",
                "dim_cooperation",
                "dim_client",
                "dim_contract_type",
                "dim_risk_level",
            ],
            "事实表": [
                "fact_project_cost",
                "fact_project_output",
                "fact_payment",
                "fact_receivable",
                "fact_cash_flow",
                "fact_risk",
                "fact_change_order",
                "fact_claim",
                "fact_project_indicator",
                "fact_business_rules",
            ],
        },
        "cube": {
            "流程型": [
                "ProjectCostCube",
                "ProjectOutputCube",
                "PaymentCube",
                "ReceivableCube",
                "CashFlowCube",
                "RiskCube",
                "ChangeOrderCube",
                "ClaimCube",
            ],
            "主体型": [
                "ProjectIndicatorCube",
            ],
        },
        "object": {
            "主数据": [
                "Project",
            ],
            "事务": [
                "Contract",
                "ProjectCost",
                "ProjectOutput",
                "Payment",
                "CashFlow",
                "ChangeOrder",
                "Claim",
            ],
            "分析": [
                "Receivable",
                "Risk",
                "CostAnalysis",
                "OutputAnalysis",
            ],
        },
        "link": {
            "归属关系": [
                "ProjectHasCost",
                "ProjectHasOutput",
                "ProjectHasContract",
                "ProjectHasPayment",
                "ProjectHasReceivable",
                "ProjectHasCashFlow",
                "ProjectHasRisk",
                "ContractRelatesCost",
                "ContractRelatesPayment",
                "ContractRelatesReceivable",
            ],
        },
    }

    # 执行挂载
    mount_count = 0
    for category_type, categories in CATEGORY_REGISTRY.items():
        for category_name, items in categories.items():
            for item in items:
                try:
                    if category_type == "table":
                        s.onto.mount_table_to_category(item, category_name)
                    elif category_type == "cube":
                        s.onto.mount_cube_to_category(item, category_name)
                    elif category_type == "object":
                        s.onto.mount_object_to_category(item, category_name)
                    elif category_type == "link":
                        s.onto.mount_link_to_category(item, category_name)
                    mount_count += 1
                except Exception as e:
                    output.print(f"警告: 挂载 {item} 到 {category_name} 失败 - {str(e)}")

    output.print(f"\n已挂载 {mount_count} 个分类关系")
    output.print("=== 商务成本本体分类挂载完成 ===")
    output.print("__JSON_SUMMARY__{\"ok\": true, \"mounted\": %d}" % mount_count)