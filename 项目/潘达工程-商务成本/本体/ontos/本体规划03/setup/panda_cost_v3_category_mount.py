"""潘达工程商务成本 V3 — 347 分类挂载（init + seed + 全部函数 publish 之后执行）

放置：项目/潘达工程-商务成本/本体/ontos/本体规划03/setup/panda_cost_v3_category_mount.py
发布：dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划03/setup/panda_cost_v3_category_mount.py --space space__panda_construction --type setup
规划对照：阶段二 V3.0 本体规划文档 + 物理表设计文档
"""

import json

# V3 附录 B：20 表 + 21 Cube + 21 对象(20+CostManagementAnalysis) + 26 链接 + 14 函数 + 28 表间关系
CATEGORY_REGISTRY = {
    "table": {
        "时间维": ["dim_date"],
        "维度表": [
            "dim_project",
            "dim_employer",
            "dim_contractor",
            "dim_supplier",
            "dim_subcontractor",
            "dim_company",
        ],
        "事实表": [
            "fact_project_output",
            "fact_project_cost",
            "fact_project_payment",
            "fact_project_balance",
            "fact_project_indicator",
            "fact_project_risk",
            "fact_receipt",
            "fact_settlement",
            "fact_bond",
            "fact_penalty",
            "fact_compensation",
            "fact_insurance",
            "fact_equipment",
        ],
    },
    "cube": {
        "主体型": [
            "ProjectCube",
            "EmployerCube",
            "ContractorCube",
            "SubcontractorCube",
            "SupplierCube",
            "CompanyCube",
        ],
        "流程型": [
            "ProjectOutputCube",
            "ProjectCostCube",
            "ProjectPaymentCube",
            "ProjectBalanceCube",
            "ProjectIndicatorCube",
            "ProjectRiskCube",
            "ReceiptCube",
            "SettlementCube",
            "BondCube",
            "PenaltyCube",
            "CompensationCube",
            "InsuranceCube",
            "EquipmentCube",
        ],
        "对比型": ["CostOutputComparisonCube"],
    },
    "object": {
        "主数据": [
            "Project",
            "Employer",
            "Contractor",
            "Subcontractor",
            "Supplier",
            "Company",
            "Contract",
        ],
        "事务": [
            "ProjectOutput",
            "ProjectCost",
            "ProjectPayment",
            "ProjectBalance",
            "ProjectIndicator",
            "ProjectRisk",
            "Bond",
            "Penalty",
            "Compensation",
            "Insurance",
            "Equipment",
            "Receipt",
            "Settlement",
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
            ("fact_receipt", "dim_date"),
            ("fact_settlement", "dim_date"),
            ("fact_bond", "dim_date"),
            ("fact_penalty", "dim_date"),
            ("fact_compensation", "dim_date"),
            ("fact_insurance", "dim_date"),
            ("fact_equipment", "dim_date"),
        ],
        "主数据关联": [
            ("dim_project", "dim_company"),
            ("dim_project", "dim_employer"),
            ("dim_project", "dim_contractor"),
            ("dim_employer", "dim_project"),
            ("dim_supplier", "dim_company"),
            ("fact_project_output", "dim_project"),
            ("fact_project_cost", "dim_project"),
            ("fact_project_payment", "dim_project"),
            ("fact_project_balance", "dim_project"),
            ("fact_project_indicator", "dim_project"),
            ("fact_project_risk", "dim_project"),
            ("fact_receipt", "dim_project"),
            ("fact_settlement", "dim_project"),
            ("fact_bond", "dim_project"),
            ("fact_penalty", "dim_project"),
            ("fact_compensation", "dim_project"),
            ("fact_insurance", "dim_project"),
            ("fact_equipment", "dim_project"),
            ("fact_bond", "fact_project_payment"),
            ("fact_receipt", "fact_project_output"),
            ("fact_settlement", "fact_project_cost"),
            ("fact_settlement", "fact_receipt"),
            ("fact_penalty", "fact_project_cost"),
            ("fact_insurance", "fact_project_cost"),
            ("fact_equipment", "fact_project_cost"),
        ],
    },
    "link": {
        "归属关系": [
            "project_belongs_company",
            "project_belongs_employer",
            "supplier_belongs_company",
            "output_belongs_project",
            "cost_belongs_project",
            "payment_belongs_project",
            "balance_belongs_project",
            "indicator_belongs_project",
            "risk_belongs_project",
            "bond_belongs_project",
            "penalty_belongs_project",
            "compensation_belongs_project",
            "insurance_belongs_project",
            "equipment_belongs_project",
            "receipt_belongs_project",
            "settlement_belongs_project",
            "contract_belongs_project",
            "bond_belongs_contract",
            "cost_contains_contract",
            "payment_contains_contract",
            "contract_signs_employer",
            "contract_signs_contractor",
            "contract_signs_subcontractor",
            "contract_supplies_supplier",
            "risk_affects_cost",
            "risk_affects_project",
            "penalty_affects_cost",
        ],
        "分析归因": [
            "analysis_by_project",
            "analysis_by_company",
            "analysis_by_employer",
            "analysis_by_contractor",
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
    output.print("=== 潘达工程商务成本 V3 — 347 分类挂载 ===")
    cat_counts = s.categories.apply_registry(CATEGORY_REGISTRY, skip_missing=True)
    output.print(f"OK 分类挂载: {json.dumps(cat_counts, ensure_ascii=True)}")
    output.success("V3 分类挂载完成")
    output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "version": "V3", "category_mounts": cat_counts}, ensure_ascii=True, default=str))
