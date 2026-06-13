"""产品销售本体 — 平台分类 + 本体域成员挂载

init → seed → 发布全部函数 → **本脚本**（含 `s.categories` 与 `s.domain`）。

放置：资源/examples/onto/销售示例/setup/sales_category_mount.py
发布：dazi onto script publish <item-path>/setup/sales_category_mount.py --space <space-id> --type setup
规划对照：资源/examples/onto/销售示例/plans/规划示例_产品销售本体规划方案.md 附录 B

本体域 code 与 function_id 前缀一致（`sales.fn.*`）；复制到业务项目时改为快速启动 §1 的本体域 code。
"""

import json

SPACE_ID = "space__misc_01"
DOMAIN_CODE = "sales"
DOMAIN_NAME = "产品销售示例"

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

    output.print("=== 产品销售 — 平台分类 + 本体域成员 ===")
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
