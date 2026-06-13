"""商务成本 — 347 分类挂载（init + seed + 全部函数 publish 之后执行）

放置：项目/潘达工程-商务成本/本体/ontos/商务成本/setup/cost_category_mount.py
发布：dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/商务成本/setup/cost_category_mount.py --space space__panda_construction --type setup
规划对照：项目/潘达工程-商务成本/本体/ontos/商务成本/plans/规划文档_商务成本本体方案.md
"""

import json

CATEGORY_REGISTRY = {
    "table": {
        "维度表": [
            "dim_date",
            "dim_region",
            "dim_department",
            "dim_owner",
            "dim_cost_subject",
            "dim_project",
            "dim_company",
            "dim_supplier",
            "dim_contract",
        ],
        "事实表": [
            "fact_project_output",
            "fact_project_cost",
            "fact_project_indicator",
            "fact_project_payment",
            "fact_project_balance",
            "fact_project_risk",
        ],
    },
    "cube": {
        "流程型": ["ProjectOutputCube", "ProjectCostCube", "ProjectPaymentCube", "ProjectBalanceCube", "ProjectRiskCube", "ProjectIndicatorCube"],
        "主体型": ["ProjectCube", "CompanyCube", "RegionCube", "DepartmentCube", "OwnerCube", "SupplierCube", "ContractCube", "CostSubjectCube"],
    },
    "object": {
        "主数据": ["Region", "Department", "Owner", "CostSubject", "Project", "Company", "Supplier", "Contract"],
        "事务": ["ProjectOutput", "ProjectCost", "ProjectIndicator", "ProjectPayment", "ProjectBalance", "ProjectRisk"],
    },
    "relation": {
        "时间关联": [
            ("fact_project_output", "dim_date"),
            ("fact_project_cost", "dim_date"),
            ("fact_project_indicator", "dim_date"),
            ("fact_project_payment", "dim_date"),
            ("fact_project_balance", "dim_date"),
            ("fact_project_risk", "dim_date"),
        ],
        "主数据关联": [
            ("fact_project_output", "dim_project"),
            ("fact_project_cost", "dim_project"),
            ("fact_project_cost", "dim_contract"),
            ("fact_project_indicator", "dim_project"),
            ("fact_project_indicator", "dim_company"),
            ("fact_project_payment", "dim_project"),
            ("fact_project_payment", "dim_contract"),
            ("fact_project_balance", "dim_project"),
            ("fact_project_risk", "dim_project"),
            ("dim_project", "dim_company"),
            ("dim_contract", "dim_project"),
        ],
        "层级自关联": [
            ("dim_cost_subject", "dim_cost_subject"),
            ("dim_department", "dim_department"),
        ],
    },
    "link": {
        "归属关系": [
            "belongsTo_ProjectOutput_Project",
            "belongsTo_ProjectCost_Project",
            "belongsTo_ProjectCost_Contract",
            "belongsTo_ProjectIndicator_Project",
            "belongsTo_ProjectIndicator_Company",
            "belongsTo_ProjectPayment_Project",
            "belongsTo_ProjectPayment_Contract",
            "belongsTo_ProjectBalance_Project",
            "belongsTo_ProjectRisk_Project",
            "belongsTo_Project_Company",
            "belongsTo_Contract_Project",
        ],
    },
    "function": {
        "总览分析": ["cost.fn.project_summary"],
        "结构分析": ["cost.fn.cost_detail", "cost.fn.output_query", "cost.fn.payment_query", "cost.fn.balance_query", "cost.fn.risk_warning"],
        "趋势分析": ["cost.fn.indicator_analysis"],
    },
}


def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)
    output.print("=== 商务成本 — 347 分类挂载 ===")
    cat_counts = s.categories.apply_registry(CATEGORY_REGISTRY, skip_missing=True)
    output.print(f"OK 分类挂载: {json.dumps(cat_counts, ensure_ascii=True)}")
    output.success("分类挂载完成")
    output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "category_mounts": cat_counts}, ensure_ascii=True, default=str))