"""化工利润成本本体 — 平台分类挂载（CATEGORY_REGISTRY）

与灌数脚本类似，**独立步骤、放在实施流程最后**：
init → seed → 发布全部函数 → **本脚本**。

放置：项目/DAZI_TEST/本体/ontos/利润成本/setup/profit_category_mount.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本/setup/profit_category_mount.py --space space_cate_test01 --type setup
规划对照：项目/DAZI_TEST/本体/ontos/利润成本/plans/化工利润成本分析本体方案.md 附录 B
"""

import json

# 与规划附录 B 一一对应；category 值必须是平台标准分类中文名
CATEGORY_REGISTRY = {
    "table": {
        "时间维": ["dim_date"],
        "维度表": ["dim_plant", "dim_process_unit", "dim_account", "dim_cost_center", "dim_material", "dim_energy_type"],
        "事实表": ["fact_gl_journal_entry", "fact_budget_entry", "fact_production_cost", "fact_energy_consumption"],
    },
    "cube": {
        "流程型": ["ActualCube", "BudgetCube"],
        "对比型": ["ProfitStatementCube", "BudgetVsActualCube"],
        "主体型": ["ProductionCostCube", "EnergyCube", "MaterialPriceCube"],
    },
    "object": {
        "主数据": ["Plant", "ProcessUnit", "Account", "CostCenter", "Material", "EnergyType"],
        "事务": ["ProfitStatement", "BudgetLine", "ProductionCost", "EnergyConsumption"],
        "分析": ["CostAnalysis", "BudgetAnalysis"],
    },
    "relation": {
        "时间关联": [
            ("fact_gl_journal_entry", "dim_date"),
            ("fact_budget_entry", "dim_date"),
            ("fact_production_cost", "dim_date"),
            ("fact_energy_consumption", "dim_date"),
        ],
        "主数据关联": [
            ("dim_process_unit", "dim_plant"),
            ("dim_cost_center", "dim_process_unit"),
            ("fact_gl_journal_entry", "dim_account"),
            ("fact_gl_journal_entry", "dim_cost_center"),
            ("fact_budget_entry", "dim_account"),
            ("fact_budget_entry", "dim_cost_center"),
            ("fact_production_cost", "dim_plant"),
            ("fact_production_cost", "dim_process_unit"),
            ("fact_production_cost", "dim_material"),
            ("fact_production_cost", "dim_energy_type"),
            ("fact_energy_consumption", "dim_plant"),
            ("fact_energy_consumption", "dim_process_unit"),
        ],
    },
    "link": {
        "归属关系": [
            "unit_belongs_plant",
            "statement_belongs_account",
            "statement_belongs_cc",
            "budget_belongs_account",
            "budget_belongs_cc",
            "production_belongs_plant",
            "production_belongs_unit",
            "production_belongs_material",
            "production_belongs_energy",
            "energy_belongs_plant",
            "energy_belongs_unit",
            "energy_belongs_type",
        ],
        "分析归因": [
            "analysis_by_account",
            "analysis_by_cc",
            "analysis_by_plant",
            "analysis_by_unit",
            "analysis_by_material",
            "analysis_by_energy",
        ],
    },
    "function": {
        "总览分析": ["profit.fn.get_summary"],
        "结构分析": ["profit.fn.account_breakdown", "profit.fn.cost_element_breakdown", "profit.fn.energy_analysis", "profit.fn.material_price_analysis", "profit.fn.top_accounts"],
        "趋势分析": ["profit.fn.yoy_analysis", "profit.fn.mom_analysis"],
        "预实分析": ["profit.fn.budget_vs_actual"],
        "组织分析": ["profit.fn.unit_cost_analysis", "profit.fn.cost_center_profit"],
    },
}


def main():
    space_id = "space_cate_test01"
    s = space.get(space_id)

    output.print("=== 化工利润成本 — 平台分类挂载 ===")
    output.print(f"空间: {space_id}")

    cat_counts = s.categories.apply_registry(CATEGORY_REGISTRY, skip_missing=True)
    for kind, cnt in cat_counts.items():
        if cnt:
            output.print(f"OK 分类[{kind}] 挂载 {cnt} 项")

    summary = {
        "ok": True,
        "space_id": space_id,
        "category_mounts": cat_counts,
    }
    output.success("平台分类挂载完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))
