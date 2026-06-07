"""产品销售本体初始化脚本 — space__misc_01

初始化内容：
1. 创建物理表（dim_date + 3 维表 + 1 事实表）
2. 注册表到空间
3. 注册表间关系（4 条，含 fact → dim_date）
4. 注册 Cube（4 个）及派生度量
5. 定义对象类型（5 种）、绑定数据源、属性、链接
6. 同步指标引用
7. 配置 平台分类对齐分类（ads_categories + 桥表）

放置：资源/examples/onto/销售示例/setup/sales_ontology_init.py（复制到项目 ontos/<实现名>/setup/）
发布：dazi onto script publish <item-path>/setup/sales_ontology_init.py --space <space-id> --type setup
规划对照：资源/examples/onto/销售示例/plans/规划示例_产品销售本体规划方案.md
"""

import json

# 与 规划示例_产品销售本体规划方案.md §2.3、§3.x 对齐：display_name=侧栏显示名，description=业务说明
TABLE_REGISTRY = {
    "dim_date": {
        "display_name": "日期维表",
        "description": "全空间共享日历，事实表通过 date_key 关联",
        "columns": [
            {"name": "date_key", "display_name": "日期键", "description": "YYYYMMDD，主键"},
            {"name": "calendar_date", "display_name": "自然日"},
            {"name": "year", "display_name": "公历年"},
            {"name": "quarter", "display_name": "季度", "description": "1-4"},
            {"name": "month", "display_name": "月", "description": "1-12"},
            {"name": "week_of_year", "display_name": "周"},
            {"name": "day_of_week", "display_name": "星期"},
            {"name": "is_weekend", "display_name": "是否周末", "description": "0/1"},
            {"name": "year_month", "display_name": "年月", "description": "如 2025-06"},
        ],
    },
    "dim_product": {
        "display_name": "产品维表",
        "description": "可售产品主数据",
        "columns": [
            {"name": "product_id", "display_name": "产品 ID", "description": "主键"},
            {"name": "product_code", "display_name": "产品编码"},
            {"name": "product_name", "display_name": "产品名称"},
            {"name": "product_category", "display_name": "产品大类"},
            {"name": "product_subcategory", "display_name": "产品小类"},
            {"name": "brand", "display_name": "品牌"},
            {"name": "unit", "display_name": "计量单位"},
            {"name": "list_price", "display_name": "挂牌价"},
            {"name": "cost_price", "display_name": "成本单价"},
            {"name": "status", "display_name": "状态", "description": "在售/停售"},
            {"name": "created_at", "display_name": "创建时间"},
            {"name": "updated_at", "display_name": "更新时间"},
        ],
    },
    "dim_customer": {
        "display_name": "客户维表",
        "description": "购买方主数据",
        "columns": [
            {"name": "customer_id", "display_name": "客户 ID", "description": "主键"},
            {"name": "customer_code", "display_name": "客户编码"},
            {"name": "customer_name", "display_name": "客户名称"},
            {"name": "customer_region", "display_name": "销售区域"},
            {"name": "customer_type", "display_name": "客户类型"},
            {"name": "industry", "display_name": "所属行业"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_channel": {
        "display_name": "渠道维表",
        "description": "销售渠道主数据",
        "columns": [
            {"name": "channel_id", "display_name": "渠道 ID", "description": "主键"},
            {"name": "channel_code", "display_name": "渠道编码"},
            {"name": "channel_name", "display_name": "渠道名称"},
            {"name": "channel_type", "display_name": "渠道类型"},
        ],
    },
    "fact_sales_order_line": {
        "display_name": "销售订单行事实表",
        "description": "订单行粒度销售流水",
        "columns": [
            {"name": "order_id", "display_name": "订单 ID"},
            {"name": "order_line_id", "display_name": "订单行 ID", "description": "主键组合"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date"},
            {"name": "order_date", "display_name": "订单日期"},
            {"name": "product_id", "display_name": "产品 ID", "description": "关联 dim_product"},
            {"name": "product_category", "display_name": "产品大类", "description": "冗余"},
            {"name": "customer_id", "display_name": "客户 ID", "description": "关联 dim_customer"},
            {"name": "customer_region", "display_name": "销售区域", "description": "冗余"},
            {"name": "customer_type", "display_name": "客户类型", "description": "冗余"},
            {"name": "channel_id", "display_name": "渠道 ID", "description": "关联 dim_channel"},
            {"name": "quantity", "display_name": "销售数量"},
            {"name": "unit_price", "display_name": "成交单价"},
            {"name": "discount_amount", "display_name": "折扣金额"},
            {"name": "sales_amount", "display_name": "销售金额"},
            {"name": "currency", "display_name": "币种"},
            {"name": "order_status", "display_name": "订单状态"},
        ],
    },
}

def main():
    space_id = "space__misc_01"
    s = space.get(space_id)

    output.print("=== 产品销售本体初始化 ===")
    output.print(f"空间: {space_id}")

    # 1. 创建物理表
    output.print("\n[1/10] 创建物理表...")

    # dim_date（强制时间维）
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_date (
            date_key Int32,
            calendar_date Date,
            year Int16,
            quarter Int8,
            month Int8,
            week_of_year Int8,
            day_of_week Int8,
            is_weekend UInt8,
            year_month String
        ) ENGINE = MergeTree()
        ORDER BY (date_key)
    """)
    output.print("OK dim_date")

    # dim_product
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_product (
            product_id String,
            product_code String,
            product_name String,
            product_category String,
            product_subcategory String,
            brand String,
            unit String,
            list_price Float64,
            cost_price Float64,
            status String,
            created_at DateTime DEFAULT now(),
            updated_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (product_id)
    """)
    output.print("OK dim_product")

    # dim_customer
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_customer (
            customer_id String,
            customer_code String,
            customer_name String,
            customer_region String,
            customer_type String,
            industry String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (customer_id)
    """)
    output.print("OK dim_customer")

    # dim_channel
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_channel (
            channel_id String,
            channel_code String,
            channel_name String,
            channel_type String
        ) ENGINE = MergeTree()
        ORDER BY (channel_id)
    """)
    output.print("OK dim_channel")

    # fact_sales_order_line（含 date_key）
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_sales_order_line (
            order_id String,
            order_line_id String,
            date_key Int32,
            order_date Date,
            product_id String,
            product_category String,
            customer_id String,
            customer_region String,
            customer_type String,
            channel_id String,
            quantity Int32,
            unit_price Float64,
            discount_amount Float64,
            sales_amount Float64,
            currency String,
            order_status String
        ) ENGINE = MergeTree()
        ORDER BY (date_key, order_id, order_line_id)
    """)
    output.print("OK fact_sales_order_line")

    # 2. 注册表（含 display_name / description）
    output.print("\n[2/10] 注册表到空间...")

    for tbl_name, meta in TABLE_REGISTRY.items():
        s.tables.register_with_meta(
            table_name=tbl_name,
            display_name=meta["display_name"],
            description=meta.get("description"),
            columns=meta["columns"],
            force_column_meta=True,
        )
        output.print(f"OK {tbl_name} ({meta['display_name']})")

    # 3. 注册表间关系（4 条，含 fact → dim_date）
    output.print("\n[3/10] 注册表间关系...")

    table_relationships = [
        {
            "from_table": "fact_sales_order_line",
            "to_table": "dim_date",
            "join_sql": "fact_sales_order_line.date_key = dim_date.date_key",
            "join_keys": [{"from": "date_key", "to": "date_key"}],
            "relationship_type": "many_to_one",
            "description": "销售订单行关联日期",
        },
        {
            "from_table": "fact_sales_order_line",
            "to_table": "dim_product",
            "join_sql": "fact_sales_order_line.product_id = dim_product.product_id",
            "join_keys": [{"from": "product_id", "to": "product_id"}],
            "relationship_type": "many_to_one",
            "description": "销售订单行关联产品",
        },
        {
            "from_table": "fact_sales_order_line",
            "to_table": "dim_customer",
            "join_sql": "fact_sales_order_line.customer_id = dim_customer.customer_id",
            "join_keys": [{"from": "customer_id", "to": "customer_id"}],
            "relationship_type": "many_to_one",
            "description": "销售订单行关联客户",
        },
        {
            "from_table": "fact_sales_order_line",
            "to_table": "dim_channel",
            "join_sql": "fact_sales_order_line.channel_id = dim_channel.channel_id",
            "join_keys": [{"from": "channel_id", "to": "channel_id"}],
            "relationship_type": "many_to_one",
            "description": "销售订单行关联渠道",
        },
    ]
    for rel in table_relationships:
        rid = s.tables.add_relationship(**rel)
        output.print(f"OK {rel['from_table']} -> {rel['to_table']} ({rid})")

    # 4. 注册 Cube（4 个）
    output.print("\n[4/10] 注册 Cube...")

    fact = "fact_sales_order_line"
    common_measures = [
        {"name": "quantity", "col": "quantity", "agg": "sum", "title": "销售数量"},
        {"name": "sales_amount", "col": "sales_amount", "agg": "sum", "title": "销售金额"},
        {"name": "discount", "col": "discount_amount", "agg": "sum", "title": "折扣金额"},
        {"name": "order_count", "col": "order_id", "agg": "uniq", "title": "订单数"},
        {"name": "line_count", "col": "order_line_id", "agg": "uniq", "title": "订单行数"},
    ]

    # SalesCube（Process · 销售分析主 Cube）
    s.register_cube(
        name="SalesCube",
        table=fact,
        title="销售分析主Cube",
        measures=common_measures,
        dimensions=[
            {"name": "order_id", "col": "order_id", "type": "string", "title": "订单ID"},
            {"name": "order_line_id", "col": "order_line_id", "type": "string", "title": "订单行ID"},
            {"name": "date_key", "col": "date_key", "type": "int32", "title": "日期键"},
            {"name": "order_date", "col": "order_date", "type": "date", "title": "订单日期"},
            {"name": "product_id", "col": "product_id", "type": "string", "title": "产品ID"},
            {"name": "product_category", "col": "product_category", "type": "string", "title": "产品大类"},
            {"name": "customer_id", "col": "customer_id", "type": "string", "title": "客户ID"},
            {"name": "customer_region", "col": "customer_region", "type": "string", "title": "销售区域"},
            {"name": "customer_type", "col": "customer_type", "type": "string", "title": "客户类型"},
            {"name": "channel_id", "col": "channel_id", "type": "string", "title": "渠道ID"},
        ],
    )
    output.print("OK SalesCube")

    # ProductSalesCube（Subject · 产品销售）
    s.register_cube(
        name="ProductSalesCube",
        table=fact,
        title="产品销售Cube",
        measures=[
            {"name": "quantity", "col": "quantity", "agg": "sum", "title": "销售数量"},
            {"name": "sales_amount", "col": "sales_amount", "agg": "sum", "title": "销售金额"},
            {"name": "order_count", "col": "order_id", "agg": "uniq", "title": "订单数"},
        ],
        dimensions=[
            {"name": "product_id", "col": "product_id", "type": "string", "title": "产品ID"},
            {"name": "product_category", "col": "product_category", "type": "string", "title": "产品大类"},
        ],
    )
    output.print("OK ProductSalesCube")

    # CustomerSalesCube（Subject · 客户销售）
    s.register_cube(
        name="CustomerSalesCube",
        table=fact,
        title="客户销售Cube",
        measures=[
            {"name": "quantity", "col": "quantity", "agg": "sum", "title": "销售数量"},
            {"name": "sales_amount", "col": "sales_amount", "agg": "sum", "title": "销售金额"},
            {"name": "order_count", "col": "order_id", "agg": "uniq", "title": "订单数"},
        ],
        dimensions=[
            {"name": "customer_id", "col": "customer_id", "type": "string", "title": "客户ID"},
            {"name": "customer_region", "col": "customer_region", "type": "string", "title": "销售区域"},
            {"name": "customer_type", "col": "customer_type", "type": "string", "title": "客户类型"},
        ],
    )
    output.print("OK CustomerSalesCube")

    # ChannelSalesCube（Subject · 渠道销售）
    s.register_cube(
        name="ChannelSalesCube",
        table=fact,
        title="渠道销售Cube",
        measures=[
            {"name": "quantity", "col": "quantity", "agg": "sum", "title": "销售数量"},
            {"name": "sales_amount", "col": "sales_amount", "agg": "sum", "title": "销售金额"},
            {"name": "order_count", "col": "order_id", "agg": "uniq", "title": "订单数"},
        ],
        dimensions=[
            {"name": "channel_id", "col": "channel_id", "type": "string", "title": "渠道ID"},
        ],
    )
    output.print("OK ChannelSalesCube")

    # 5. 派生度量
    output.print("\n[5/10] 配置派生度量...")

    s.upsert_derived_measures(
        "SalesCube",
        [
            {
                "name": "avg_unit_price",
                "title": "平均单价",
                "expression": "if(SalesCube.quantity > 0, SalesCube.sales_amount / SalesCube.quantity, 0)",
                "description": "销售金额/销量",
            },
            {
                "name": "avg_order_value",
                "title": "客单价",
                "expression": "if(SalesCube.order_count > 0, SalesCube.sales_amount / SalesCube.order_count, 0)",
                "description": "销售金额/订单数",
            },
        ],
    )
    output.print("OK SalesCube 派生度量")

    s.upsert_derived_measures(
        "ProductSalesCube",
        [
            {
                "name": "avg_unit_price",
                "title": "平均单价",
                "expression": "if(ProductSalesCube.quantity > 0, ProductSalesCube.sales_amount / ProductSalesCube.quantity, 0)",
                "description": "平均成交单价",
            },
        ],
    )
    output.print("OK ProductSalesCube 派生度量")

    s.upsert_derived_measures(
        "CustomerSalesCube",
        [
            {
                "name": "avg_order_value",
                "title": "客单价",
                "expression": "if(CustomerSalesCube.order_count > 0, CustomerSalesCube.sales_amount / CustomerSalesCube.order_count, 0)",
                "description": "客户客单价",
            },
        ],
    )
    output.print("OK CustomerSalesCube 派生度量")

    # 6. 对象类型
    output.print("\n[6/10] 定义对象类型...")

    object_types = [
        ("Product", "产品", "可售产品业务对象"),
        ("Customer", "客户", "购买方业务对象"),
        ("SalesChannel", "销售渠道", "渠道业务对象"),
        ("SalesOrder", "销售订单", "订单/订单行业务对象"),
        ("SalesAnalysis", "销售分析", "多维度销售指标聚合对象"),
    ]
    for code, name, desc in object_types:
        s.onto.define_object_type(code, name, description=desc)
        output.print(f"OK {code}")

    # 7. 绑定数据源
    output.print("\n[7/10] 绑定数据源...")

    bindings = [
        ("Product", "ProductSalesCube"),
        ("Customer", "CustomerSalesCube"),
        ("SalesChannel", "ChannelSalesCube"),
        ("SalesOrder", "SalesCube"),
        ("SalesAnalysis", "SalesCube"),
    ]
    for code, cube in bindings:
        s.onto.bind_source(code, "dazi_cube", config={"cube": cube})
        output.print(f"OK {code} -> {cube}")

    # 8. 定义属性
    output.print("\n[8/10] 定义属性...")

    properties = [
        # Product 属性
        ("Product", "id", "产品ID", "dimension", "ProductSalesCube.product_id"),
        ("Product", "category", "产品大类", "dimension", "ProductSalesCube.product_category"),
        ("Product", "quantity", "累计销量", "measure", "ProductSalesCube.quantity"),
        ("Product", "sales_amount", "累计销售额", "measure", "ProductSalesCube.sales_amount"),
        ("Product", "order_count", "订单数", "measure", "ProductSalesCube.order_count"),
        ("Product", "avg_unit_price", "平均单价", "measure", "ProductSalesCube.avg_unit_price"),
        # Customer 属性
        ("Customer", "id", "客户ID", "dimension", "CustomerSalesCube.customer_id"),
        ("Customer", "region", "销售区域", "dimension", "CustomerSalesCube.customer_region"),
        ("Customer", "type", "客户类型", "dimension", "CustomerSalesCube.customer_type"),
        ("Customer", "quantity", "累计销量", "measure", "CustomerSalesCube.quantity"),
        ("Customer", "sales_amount", "累计销售额", "measure", "CustomerSalesCube.sales_amount"),
        ("Customer", "order_count", "订单数", "measure", "CustomerSalesCube.order_count"),
        ("Customer", "avg_order_value", "客单价", "measure", "CustomerSalesCube.avg_order_value"),
        # SalesChannel 属性
        ("SalesChannel", "id", "渠道ID", "dimension", "ChannelSalesCube.channel_id"),
        ("SalesChannel", "quantity", "累计销量", "measure", "ChannelSalesCube.quantity"),
        ("SalesChannel", "sales_amount", "累计销售额", "measure", "ChannelSalesCube.sales_amount"),
        ("SalesChannel", "order_count", "订单数", "measure", "ChannelSalesCube.order_count"),
        # SalesOrder 属性
        ("SalesOrder", "id", "订单ID", "dimension", "SalesCube.order_id"),
        ("SalesOrder", "line_id", "订单行", "dimension", "SalesCube.order_line_id"),
        ("SalesOrder", "date", "订单日期", "dimension", "SalesCube.order_date"),
        ("SalesOrder", "quantity", "数量", "measure", "SalesCube.quantity"),
        ("SalesOrder", "sales_amount", "销售金额", "measure", "SalesCube.sales_amount"),
        ("SalesOrder", "unit_price", "成交单价", "measure", "SalesCube.avg_unit_price"),
        # SalesAnalysis 属性
        ("SalesAnalysis", "total_sales", "总销售额", "measure", "SalesCube.sales_amount"),
        ("SalesAnalysis", "total_quantity", "总销量", "measure", "SalesCube.quantity"),
        ("SalesAnalysis", "order_count", "订单数", "measure", "SalesCube.order_count"),
        ("SalesAnalysis", "avg_order_value", "客单价", "measure", "SalesCube.avg_order_value"),
        ("SalesAnalysis", "avg_unit_price", "平均单价", "measure", "SalesCube.avg_unit_price"),
    ]
    for obj_code, prop_code, title, role, qualified_name in properties:
        s.onto.define_property(obj_code, prop_code, title, semantic_role=role, qualified_name=qualified_name)
    output.print(f"OK {len(properties)} 个属性")

    # 9. 定义链接类型
    output.print("\n[9/10] 定义链接类型...")

    link_types = [
        ("order_contains_product", "订单包含产品", "SalesOrder", "Product"),
        ("order_belongs_customer", "订单归属客户", "SalesOrder", "Customer"),
        ("order_via_channel", "订单经渠道成交", "SalesOrder", "SalesChannel"),
        ("product_has_orders", "产品有订单", "Product", "SalesOrder"),
        ("customer_places_orders", "客户下单", "Customer", "SalesOrder"),
        ("analysis_by_product", "分析归因产品", "SalesAnalysis", "Product"),
        ("analysis_by_customer", "分析归因客户", "SalesAnalysis", "Customer"),
        ("analysis_by_channel", "分析归因渠道", "SalesAnalysis", "SalesChannel"),
    ]
    for code, name, from_obj, to_obj in link_types:
        s.onto.define_link_type(code, name, from_object_type_code=from_obj, to_object_type_code=to_obj)
        output.print(f"OK {code}")

    # 同步指标引用
    s.sync_metric_refs()
    output.print("OK sync_metric_refs")

    summary = {
        "ok": True,
        "space_id": space_id,
        "tables": 5,
        "table_relationships": 4,
        "cubes": 4,
        "object_types": 5,
        "properties": len(properties),
        "link_types": len(link_types),
    }
    output.success("本体初始化完成")
    output.print(f"space_id: {space_id}")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=False))
