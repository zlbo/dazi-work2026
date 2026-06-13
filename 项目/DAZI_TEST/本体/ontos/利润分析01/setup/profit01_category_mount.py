"""利润分析01 — 平台分类 + 本体域成员挂载

init → seed → 发布全部函数 → **本脚本**
规划对照：plans/利润分析01本体规划方案.md 附录 B

域 code 与快速启动 §1 一致（profit01）；function_id 前缀同为 profit01.fn.*
"""

import json

SPACE_ID = "space__onto_engine_test"
DOMAIN_CODE = "profit01"
DOMAIN_NAME = "利润分析01"

CATEGORY_REGISTRY = {
    "table": {
        "维度表": ["dim_account", "dim_org", "dim_project", "dim_cost_type", "bridge_cost_type_account"],
        "事实表": ["fact_pl_budget", "fact_cost", "fact_output", "fact_project_profit"],
    },
    "cube": {
        "流程型": ["OutputCube", "CostCube", "BudgetPlCube"],
        "主体型": ["AccountCostCube"],
        "对比型": ["ProjectProfitCube", "BudgetVsActualCube"],
    },
    "object": {
        "主数据": ["Account", "Org", "Project"],
        "参考": ["CostType"],
        "事务": ["RevenueRecord", "CostRecord", "BudgetLine"],
        "分析": ["ProfitAnalysis", "BudgetAnalysis"],
    },
    "relation": {
        "时间关联": [
            ("fact_pl_budget", "dim_date"),
            ("fact_project_profit", "dim_date"),
        ],
        "主数据关联": [
            ("fact_pl_budget", "dim_project"),
            ("fact_pl_budget", "dim_org"),
            ("fact_pl_budget", "dim_account"),
            ("bridge_cost_type_account", "dim_cost_type"),
            ("bridge_cost_type_account", "dim_account"),
            ("fact_project_profit", "dim_project"),
            ("fact_project_profit", "dim_org"),
        ],
        "层级自关联": [("dim_account", "dim_account")],
    },
    "link": {
        "归属关系": [
            "cost_maps_account",
            "revenue_belongs_project",
            "budget_for_account",
            "budget_for_project",
        ],
        "层级关系": ["account_has_parent"],
        "分析归因": ["profit_analysis_by_project", "profit_analysis_by_account"],
        "对比关系": ["budget_compared_to_actual"],
    },
    "function": {
        "总览分析": ["profit01.fn.get_summary"],
        "结构分析": [
            "profit01.fn.project_profit",
            "profit01.fn.account_breakdown",
            "profit01.fn.cost_type_breakdown",
        ],
        "预实分析": ["profit01.fn.budget_vs_actual"],
        "组织分析": ["profit01.fn.region_profit", "profit01.fn.org_profit"],
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
    output.print("=== 利润分析01 — 平台分类 + 本体域成员 ===")
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
    output.print(
        f"OK 本体域成员 kinds: {json.dumps(domain_summary.get('kinds', {}), ensure_ascii=True, default=str)}"
    )

    summary = {
        "ok": True,
        "space_id": SPACE_ID,
        "domain_code": DOMAIN_CODE,
        "category_mounts": cat_counts,
        "domain_mounts": domain_summary.get("kinds", {}),
    }
    output.success("平台分类与本体域成员挂载完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))
