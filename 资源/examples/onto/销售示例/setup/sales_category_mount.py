"""产品销售本体 — 平台分类挂载（CATEGORY_REGISTRY）

与灌数脚本类似，**独立步骤、放在实施流程最后**：
init → seed → 发布全部函数 → **本脚本**。

放置：资源/examples/onto/销售示例/setup/sales_category_mount.py
发布：dazi onto script publish <item-path>/setup/sales_category_mount.py --space <space-id> --type setup
规划对照：资源/examples/onto/销售示例/plans/规划示例_产品销售本体规划方案.md 附录 B
"""

import json

CATEGORY_REGISTRY = {
    "table": {
        "时间维": ["dim_date"],
        "维度表": ["dim_product", "dim_customer", "dim_channel"],
        "事实表": ["fact_sales_order_line"],
    },
    "cube": {
        "流程型": ["SalesCube"],
        "主体型": ["ProductSalesCube", "CustomerSalesCube", "ChannelSalesCube"],
    },
    "object": {
        "主数据": ["Product", "Customer"],
        "参考": ["SalesChannel"],
        "事务": ["SalesOrder"],
        "分析": ["SalesAnalysis"],
    },
    "relation": {
        "时间关联": [("fact_sales_order_line", "dim_date")],
        "主数据关联": [
            ("fact_sales_order_line", "dim_product"),
            ("fact_sales_order_line", "dim_customer"),
            ("fact_sales_order_line", "dim_channel"),
        ],
    },
    "link": {
        "归属关系": [
            "order_contains_product",
            "order_belongs_customer",
            "order_via_channel",
            "product_has_orders",
            "customer_places_orders",
        ],
        "分析归因": [
            "analysis_by_product",
            "analysis_by_customer",
            "analysis_by_channel",
        ],
    },
    "function": {
        "总览分析": ["sales.fn.get_summary"],
        "趋势分析": ["sales.fn.yoy_analysis", "sales.fn.mom_analysis"],
        "结构分析": [
            "sales.fn.top_products",
            "sales.fn.customer_segmentation",
            "sales.fn.channel_mix",
        ],
        "组织分析": ["sales.fn.region_breakdown"],
    },
}


def main():
    space_id = "space__misc_01"
    s = space.get(space_id)

    output.print("=== 产品销售 — 平台分类挂载 ===")
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
