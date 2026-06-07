"""利润分析本体 — 平台分类挂载（CATEGORY_REGISTRY）

与灌数脚本类似，**独立步骤、放在实施流程最后**：
init → seed → 发布全部函数 → **本脚本**。

放置：资源/examples/onto/利润示例/setup/profit_category_mount.py
发布：dazi onto script publish <item-path>/setup/profit_category_mount.py --space <space-id> --type setup
规划对照：资源/examples/onto/利润示例/plans/规划示例_利润分析本体方案.md 附录 B
"""

import json

# 与规划附录 B 一一对应；category 值必须是平台标准分类中文名
CATEGORY_REGISTRY = {
    "table": {
        "维度表": ["dim_account", "dim_cost_center"],
        "事实表": ["fact_gl_journal_entry", "fact_budget_entry"],
    },
    "cube": {
        "流程型": ["ActualCube", "BudgetCube"],
        "主体型": ["AccountActualCube", "CostCenterActualCube", "TimeActualCube"],
    },
    "object": {
        "主数据": ["Account", "CostCenter"],
        "事务": ["JournalEntry", "BudgetLine"],
        "分析": ["ProfitAnalysis", "BudgetAnalysis"],
    },
    "relation": {
        "时间关联": [
            ("fact_gl_journal_entry", "dim_date"),
            ("fact_budget_entry", "dim_date"),
        ],
        "主数据关联": [
            ("fact_gl_journal_entry", "dim_account"),
            ("fact_gl_journal_entry", "dim_cost_center"),
            ("fact_budget_entry", "dim_account"),
            ("fact_budget_entry", "dim_cost_center"),
        ],
        "层级自关联": [("dim_account", "dim_account")],
    },
    "link": {
        "归属关系": [
            "entry_belongs_account",
            "entry_belongs_cost_center",
            "budget_for_account",
            "budget_for_cost_center",
        ],
        "分析归因": [
            "analysis_by_account",
            "analysis_by_cost_center",
            "account_contributes_profit",
            "cost_center_contributes_profit",
        ],
        "层级关系": ["account_has_parent"],
        "对比关系": ["budget_compared_to_actual"],
    },
    "function": {
        "总览分析": ["profit.fn.get_summary"],
        "趋势分析": ["profit.fn.yoy_analysis", "profit.fn.mom_analysis"],
        "结构分析": ["profit.fn.account_breakdown", "profit.fn.top_accounts"],
        "预实分析": ["profit.fn.budget_vs_actual"],
        "组织分析": ["profit.fn.cost_center_profit"],
    },
}


def main():
    space_id = "space__misc_01"
    s = space.get(space_id)

    output.print("=== 利润分析 — 平台分类挂载 ===")
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
