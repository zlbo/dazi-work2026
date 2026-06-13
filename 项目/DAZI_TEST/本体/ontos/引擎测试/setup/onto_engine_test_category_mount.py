"""本体引擎测试空间 — 平台分类挂载"""

import json

CATEGORY_REGISTRY = {
    "table": {
        "时间维": ["dim_date"],
        "维度表": ["dim_org", "dim_project", "dim_cost_type"],
        "事实表": ["fact_cost", "fact_output"],
    },
    "cube": {
        "流程型": ["CostCube"],
        "主体型": ["OutputCube"],
    },
    "object": {
        "主数据": ["Project", "Org"],
        "参考": ["CostType"],
        "事务": ["CostRecord", "OutputRecord"],
        "分析": ["CostAnalysis"],
    },
    "relation": {
        "时间关联": [
            ("fact_cost", "dim_date"),
            ("fact_output", "dim_date"),
        ],
        "主数据关联": [
            ("fact_cost", "dim_project"),
            ("fact_cost", "dim_org"),
            ("fact_cost", "dim_cost_type"),
            ("fact_output", "dim_project"),
            ("fact_output", "dim_org"),
            ("dim_project", "dim_org"),
        ],
        "层级自关联": [
            ("dim_org", "dim_org"),
            ("dim_cost_type", "dim_cost_type"),
        ],
    },
    "link": {
        "归属关系": [
            "cost_for_project", "output_for_project", "project_belongs_org",
            "cost_has_type",
        ],
        "层级关系": ["org_has_parent", "costtype_has_parent"],
        "分析归因": ["analysis_by_project"],
    },
}


def main():
    space_id = "space__onto_engine_test"
    s = space.get(space_id)
    output.print("=== 本体引擎测试空间分类挂载 ===")
    result = s.categories.apply_registry(CATEGORY_REGISTRY, skip_missing=True)
    output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "category_mounts": result}, ensure_ascii=True, default=str))

