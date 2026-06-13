"""潘达工程商务成本 — 347 分类挂载（init + seed + 全部函数 publish 之后执行）

放置：项目/潘达工程-商务成本/本体/ontos/本体规划02/setup/panda_cost_category_mount.py
发布：dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划02/setup/panda_cost_category_mount.py --space space__panda_construction --type setup
规划对照：项目/潘达工程-商务成本/本体/ontos/本体规划02/plans/潘达工程商务成本管理本体方案.md 附录 B
"""

import json

# 附录 B：13 cube, 15 object, 24 link, 14 function, 25 relation
CATEGORY_REGISTRY = {
    "table": {
        "时间维": ["dim_date"],
        "维度表": [
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
            "fact_project_payment",
            "fact_project_balance",
            "fact_project_indicator",
            "fact_project_risk",
        ],
    },
    "cube": {
        "主体型": [
            "RegionCube",
            "DepartmentCube",
            "OwnerCube",
            "CostSubjectCube",
            "ProjectCube",
            "CompanyCube",
        ],
        "流程型": [
            "ProjectOutputCube",
            "ProjectCostCube",
            "ProjectPaymentCube",
            "ProjectBalanceCube",
            "ProjectIndicatorCube",
            "ProjectRiskCube",
        ],
        "对比型": ["CostOutputComparisonCube"],
    },
    "object": {
        "主数据": [
            "Region",
            "Department",
            "Owner",
            "Company",
            "Project",
            "Contract",
            "Supplier",
        ],
        "参考": ["CostSubject"],
        "事务": [
            "ProjectOutput",
            "ProjectCost",
            "ProjectPayment",
            "ProjectBalance",
            "ProjectIndicator",
            "ProjectRisk",
        ],
        "分析": ["CostManagementAnalysis"],
    },
    "relation": {
        "时间关联": [
            ("fact_project_output", "dim_date"),
            ("fact_project_cost", "dim_date"),
            ("fact_project_payment", "dim_date"),
            ("fact_project_balance", "dim_date"),
            ("fact_project_indicator", "dim_date"),
            ("fact_project_risk", "dim_date"),
        ],
        "主数据关联": [
            ("dim_project", "dim_company"),
            ("dim_company", "dim_region"),
            ("dim_project", "dim_region"),
            ("dim_project", "dim_owner"),
            ("dim_project", "dim_department"),
            ("dim_department", "dim_company"),
            ("fact_project_output", "dim_project"),
            ("fact_project_cost", "dim_project"),
            ("fact_project_payment", "dim_project"),
            ("fact_project_balance", "dim_project"),
            ("fact_project_indicator", "dim_project"),
            ("fact_project_risk", "dim_project"),
            ("dim_contract", "dim_project"),
            ("dim_contract", "dim_supplier"),
            ("dim_supplier", "dim_company"),
            ("fact_project_payment", "dim_contract"),
            ("fact_project_cost", "dim_contract"),
            ("fact_project_balance", "dim_cost_subject"),
        ],
        "层级自关联": [
            ("dim_department", "dim_department"),
        ],
    },
    "link": {
        "归属关系": [
            "company_located_in_region",
            "project_located_in_region",
            "project_serves_owner",
            "project_managed_by_department",
            "department_belongs_company",
            "project_belongs_company",
            "supplier_belongs_company",
            "output_belongs_project",
            "cost_belongs_project",
            "payment_belongs_project",
            "balance_belongs_project",
            "indicator_belongs_project",
            "risk_belongs_project",
            "contract_belongs_project",
            "contract_with_supplier",
            "cost_contains_contract",
            "payment_contains_contract",
            "balance_has_subject",
        ],
        "层级关系": ["department_has_parent"],
        "分析归因": [
            "analysis_by_project",
            "analysis_by_company",
            "analysis_by_region",
            "analysis_by_owner",
            "analysis_by_department",
        ],
    },
    "function": {
        "总览分析": [
            "panda_cost.fn.get_summary",
            "panda_cost.fn.profit_analysis",
            "panda_cost.fn.indicator_status",
            "panda_cost.fn.risk_overview",
            "panda_cost.fn.project_health",
        ],
        "趋势分析": [
            "panda_cost.fn.yoy_analysis",
            "panda_cost.fn.mom_analysis",
        ],
        "结构分析": [
            "panda_cost.fn.output_analysis",
            "panda_cost.fn.cost_structure",
            "panda_cost.fn.payment_analysis",
            "panda_cost.fn.balance_breakdown",
            "panda_cost.fn.top_risk_projects",
        ],
        "组织分析": [
            "panda_cost.fn.company_comparison",
            "panda_cost.fn.region_comparison",
        ],
    },
}


def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)
    output.print("=== 潘达工程商务成本 — 347 分类挂载 ===")
    cat_counts = s.categories.apply_registry(CATEGORY_REGISTRY, skip_missing=True)
    output.print(f"OK 分类挂载: {json.dumps(cat_counts, ensure_ascii=True)}")
    output.success("分类挂载完成")
    output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "category_mounts": cat_counts}, ensure_ascii=True, default=str))
