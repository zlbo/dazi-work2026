"""生产计划 — 347 分类挂载（init + seed + 全部函数 publish 之后执行）

放置：项目/DAZI_TEST/本体/ontos/生产计划/setup/prod_plan_category_mount.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/生产计划/setup/prod_plan_category_mount.py --space space_cate_test01 --type setup
规划对照：项目/DAZI_TEST/本体/ontos/生产计划/plans/生产计划本体规划方案.md 附录 B
"""

import json

CATEGORY_REGISTRY = {
    "table": {
        "维度表": [
            "dim_plant",
            "dim_work_center",
            "dim_product",
            "dim_plan_version",
        ],
        "事实表": [
            "fact_production_plan",
            "fact_work_order",
            "fact_production_daily",
            "fact_material_requirement",
            "fact_capacity_load",
        ],
    },
    "cube": {
        "流程型": [
            "ProductionPlanCube",
            "WorkOrderCube",
            "ProductionActualCube",
            "MaterialRequirementCube",
            "CapacityLoadCube",
        ],
        "主体型": ["WorkCenterCube", "PlantCube", "ProductCube"],
        "对比型": ["PlanVsActualCube"],
    },
    "object": {
        "主数据": ["Plant", "WorkCenter", "Product"],
        "参考": ["PlanVersion"],
        "事务": [
            "ProductionPlanLine",
            "WorkOrder",
            "ProductionDaily",
            "MaterialRequirement",
            "CapacitySnapshot",
        ],
        "分析": ["ProductionAnalysis", "PlanAnalysis"],
    },
    "relation": {
        "时间关联": [
            ("fact_production_plan", "dim_date"),
            ("fact_work_order", "dim_date"),
            ("fact_production_daily", "dim_date"),
            ("fact_material_requirement", "dim_date"),
            ("fact_capacity_load", "dim_date"),
        ],
        "主数据关联": [
            ("dim_work_center", "dim_plant"),
            ("fact_production_plan", "dim_plant"),
            ("fact_production_plan", "dim_work_center"),
            ("fact_production_plan", "dim_product"),
            ("fact_production_plan", "dim_plan_version"),
            ("fact_work_order", "dim_work_center"),
            ("fact_work_order", "dim_product"),
            ("fact_production_daily", "dim_work_center"),
            ("fact_production_daily", "dim_product"),
            ("fact_material_requirement", "fact_work_order"),
            ("fact_material_requirement", "dim_product"),
            ("fact_capacity_load", "dim_work_center"),
            ("fact_capacity_load", "dim_plan_version"),
        ],
        "预实关联": [
            ("fact_work_order", "fact_production_plan"),
            ("fact_production_plan", "fact_production_daily"),
        ],
    },
    "link": {
        "归属关系": [
            "wc_belongs_plant",
            "plan_for_version",
            "plan_on_wc",
            "plan_for_product",
            "wo_on_wc",
            "wo_for_product",
            "wo_from_plan",
            "daily_on_wc",
            "daily_for_product",
            "mrp_for_wo",
            "mrp_for_component",
            "capacity_on_wc",
            "capacity_for_version",
        ],
        "对比关系": ["plan_compared_to_actual"],
        "分析归因": [
            "analysis_by_plant",
            "analysis_by_wc",
            "analysis_by_product",
            "analysis_by_work_order",
        ],
    },
    "function": {
        "总览分析": ["prod_plan.fn.get_summary"],
        "趋势分析": ["prod_plan.fn.yoy_analysis", "prod_plan.fn.mom_analysis"],
        "结构分析": [
            "prod_plan.fn.work_order_status",
            "prod_plan.fn.capacity_load",
            "prod_plan.fn.material_shortage",
            "prod_plan.fn.product_mix",
            "prod_plan.fn.top_delayed_orders",
        ],
        "预实分析": ["prod_plan.fn.plan_vs_actual"],
        "组织分析": ["prod_plan.fn.line_comparison"],
    },
}


def main():
    space_id = "space_cate_test01"
    s = space.get(space_id)
    output.print("=== 生产计划 — 347 分类挂载 ===")
    cat_counts = s.categories.apply_registry(CATEGORY_REGISTRY, skip_missing=True)
    output.print(f"OK 分类挂载: {json.dumps(cat_counts, ensure_ascii=True)}")
    output.success("分类挂载完成")
    output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "category_mounts": cat_counts}, ensure_ascii=True, default=str))
