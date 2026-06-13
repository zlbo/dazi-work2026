"""利润分析本体 — 平台分类 + 本体域成员挂载

init → seed → 发布全部函数 → **本脚本**（含 `s.categories` 与 `s.domain`）。

放置：资源/examples/onto/利润示例/setup/profit_category_mount.py
发布：dazi onto script publish <item-path>/setup/profit_category_mount.py --space <space-id> --type setup
规划对照：资源/examples/onto/利润示例/plans/规划示例_利润分析本体方案.md 附录 B

本体域 code 与 function_id 前缀一致（`profit.fn.*`）；复制到业务项目时改为快速启动 §1 的本体域 code。
"""

import json

SPACE_ID = "space__misc_01"
DOMAIN_CODE = "profit"
DOMAIN_NAME = "利润分析示例"

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


def _flatten_for_domain(reg):
    """CATEGORY_REGISTRY → DOMAIN_REGISTRY members（relation 元组暂跳过）。"""
    kind_map = {"object": "object_type", "link": "link_type"}
    members = {}
    for kind, cats in reg.items():
        if kind == "relation":
            continue
        dk = kind_map.get(kind, kind)
        keys = []
        for items in cats.values():
            for item in items:
                if isinstance(item, tuple):
                    continue
                keys.append(item)
        if keys:
            members[dk] = keys
    return members


def main():
    s = space.get(SPACE_ID)

    output.print("=== 利润分析 — 平台分类 + 本体域成员 ===")
    output.print(f"空间: {SPACE_ID} · 域: {DOMAIN_CODE}")

    cat_counts = s.categories.apply_registry(CATEGORY_REGISTRY, skip_missing=True)
    for kind, cnt in cat_counts.items():
        if cnt:
            output.print(f"OK 分类[{kind}] 挂载 {cnt} 项")

    domain_summary = s.domain.apply_registry(
        {
            "code": DOMAIN_CODE,
            "name": DOMAIN_NAME,
            "members": _flatten_for_domain(CATEGORY_REGISTRY),
        },
        strict=False,
    )
    output.print(f"OK 本体域成员 kinds: {json.dumps(domain_summary.get('kinds', {}), ensure_ascii=True, default=str)}")

    summary = {
        "ok": True,
        "space_id": SPACE_ID,
        "domain_code": DOMAIN_CODE,
        "category_mounts": cat_counts,
        "domain_mounts": domain_summary.get("kinds", {}),
    }
    output.success("平台分类与本体域成员挂载完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))
