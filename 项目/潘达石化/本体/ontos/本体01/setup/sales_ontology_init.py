"""产品销售本体初始化脚本 — space__0519

初始化内容：
1. 创建物理表（4 张）
2. 注册表到空间
3. 注册 Cube（5 个）及派生度量
4. 定义对象类型（5 种）、绑定数据源、属性、链接
5. 同步指标引用

放置：项目/onto_本体项目01/脚本/setup/sales_ontology_init.py
发布：dazi-onto script publish 项目/onto_本体项目01/脚本/setup/sales_ontology_init.py --space space__0519
"""

import json


def main():
    space_id = "space__0519"
    s = space.get(space_id)

    output.print("=== 产品销售本体初始化 ===")
    output.print(f"空间: {space_id}")

    # 1. 创建物理表
    output.print("\n[1/8] 创建物理表...")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS product_master (
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
    output.print("OK product_master")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS customer_dimension (
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
    output.print("OK customer_dimension")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS channel_dimension (
            channel_id String,
            channel_code String,
            channel_name String,
            channel_type String
        ) ENGINE = MergeTree()
        ORDER BY (channel_id)
    """)
    output.print("OK channel_dimension")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS sales_order_fact (
            order_id String,
            order_line_id String,
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
        ORDER BY (order_date, order_id, order_line_id)
    """)
    output.print("OK sales_order_fact")

    # 2. 注册表
    output.print("\n[2/8] 注册表到空间...")

    for tbl, label in [
        ("product_master", "产品主数据表"),
        ("customer_dimension", "客户维度表"),
        ("channel_dimension", "销售渠道表"),
        ("sales_order_fact", "销售订单事实表"),
    ]:
        s.tables.register(tbl, label=label)
        s.tables.sync_columns(tbl)
        output.print(f"OK {tbl}")

    # 3. 注册 Cube
    output.print("\n[3/8] 注册 Cube...")

    fact = "sales_order_fact"
    common_measures = [
        {"name": "quantity", "col": "quantity", "agg": "sum", "title": "销售数量"},
        {"name": "sales_amount", "col": "sales_amount", "agg": "sum", "title": "销售金额"},
        {"name": "discount", "col": "discount_amount", "agg": "sum", "title": "折扣金额"},
        {"name": "order_count", "col": "order_id", "agg": "uniq", "title": "订单数"},
        {"name": "line_count", "col": "order_line_id", "agg": "uniq", "title": "订单行数"},
    ]

    s.register_cube(
        name="SalesCube",
        table=fact,
        title="销售分析主Cube",
        measures=common_measures,
        dimensions=[
            {"name": "order_id", "col": "order_id", "type": "string", "title": "订单ID"},
            {"name": "order_line_id", "col": "order_line_id", "type": "string", "title": "订单行ID"},
            {"name": "order_date", "col": "order_date", "type": "date", "title": "订单日期"},
            {"name": "product_id", "col": "product_id", "type": "string", "title": "产品ID"},
            {"name": "product_category", "col": "product_category", "type": "string", "title": "产品大类"},
            {"name": "customer_id", "col": "customer_id", "type": "string", "title": "客户ID"},
            {"name": "customer_region", "col": "customer_region", "type": "string", "title": "销售区域"},
            {"name": "channel_id", "col": "channel_id", "type": "string", "title": "渠道ID"},
        ],
    )
    output.print("OK SalesCube")

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

    s.register_cube(
        name="TimeSalesCube",
        table=fact,
        title="时间维度销售Cube",
        measures=[
            {"name": "sales_amount", "col": "sales_amount", "agg": "sum", "title": "销售金额"},
            {"name": "quantity", "col": "quantity", "agg": "sum", "title": "销售数量"},
            {"name": "order_count", "col": "order_id", "agg": "uniq", "title": "订单数"},
        ],
        dimensions=[
            {"name": "order_date", "col": "order_date", "type": "date", "title": "订单日期"},
            {"name": "year_month", "col": "order_date", "type": "string", "title": "年月"},
            {"name": "quarter", "col": "order_date", "type": "string", "title": "季度"},
            {"name": "year", "col": "order_date", "type": "date", "title": "年份"},
        ],
    )
    output.print("OK TimeSalesCube")

    # 4. 派生度量
    output.print("\n[4/8] 配置派生度量...")

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
    output.print("OK 派生度量")

    # 5. 对象类型
    output.print("\n[5/8] 定义对象类型...")

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

    # 6. 绑定数据源
    output.print("\n[6/8] 绑定数据源...")

    bindings = [
        ("Product", "ProductSalesCube"),
        ("Customer", "CustomerSalesCube"),
        ("SalesChannel", "ChannelSalesCube"),
        ("SalesOrder", "SalesCube"),
        ("SalesAnalysis", "SalesCube"),
    ]
    for obj, cube in bindings:
        s.onto.bind_source(obj, "dazi_cube", config={"cube": cube})
        output.print(f"OK {obj} -> {cube}")

    # 7. 属性
    output.print("\n[7/8] 定义属性...")

    def define_props(obj_code, props):
        for code, name, role, qn in props:
            s.onto.define_property(obj_code, code, name, semantic_role=role, qualified_name=qn)

    define_props("Product", [
        ("id", "产品ID", "dimension", "ProductSalesCube.product_id"),
        ("category", "产品大类", "dimension", "ProductSalesCube.product_category"),
        ("quantity", "累计销量", "measure", "ProductSalesCube.quantity"),
        ("sales_amount", "累计销售额", "measure", "ProductSalesCube.sales_amount"),
        ("order_count", "订单数", "measure", "ProductSalesCube.order_count"),
        ("avg_unit_price", "平均单价", "measure", "ProductSalesCube.avg_unit_price"),
    ])
    output.print("OK Product 属性 (6)")

    define_props("Customer", [
        ("id", "客户ID", "dimension", "CustomerSalesCube.customer_id"),
        ("region", "销售区域", "dimension", "CustomerSalesCube.customer_region"),
        ("type", "客户类型", "dimension", "CustomerSalesCube.customer_type"),
        ("sales_amount", "累计销售额", "measure", "CustomerSalesCube.sales_amount"),
        ("order_count", "订单数", "measure", "CustomerSalesCube.order_count"),
        ("avg_order_value", "客单价", "measure", "CustomerSalesCube.avg_order_value"),
    ])
    output.print("OK Customer 属性 (6)")

    define_props("SalesChannel", [
        ("id", "渠道ID", "dimension", "ChannelSalesCube.channel_id"),
        ("sales_amount", "销售额", "measure", "ChannelSalesCube.sales_amount"),
        ("order_count", "订单数", "measure", "ChannelSalesCube.order_count"),
    ])
    output.print("OK SalesChannel 属性 (3)")

    define_props("SalesOrder", [
        ("id", "订单ID", "dimension", "SalesCube.order_id"),
        ("line_id", "订单行", "dimension", "SalesCube.order_line_id"),
        ("date", "订单日期", "dimension", "SalesCube.order_date"),
        ("quantity", "数量", "measure", "SalesCube.quantity"),
        ("sales_amount", "销售金额", "measure", "SalesCube.sales_amount"),
        ("unit_price", "成交单价", "measure", "SalesCube.avg_unit_price"),
    ])
    output.print("OK SalesOrder 属性 (6)")

    define_props("SalesAnalysis", [
        ("date", "日期", "dimension", "SalesCube.order_date"),
        ("product_category", "产品大类", "dimension", "SalesCube.product_category"),
        ("customer_region", "销售区域", "dimension", "SalesCube.customer_region"),
        ("channel_id", "渠道", "dimension", "SalesCube.channel_id"),
        ("quantity", "销量", "measure", "SalesCube.quantity"),
        ("sales_amount", "销售额", "measure", "SalesCube.sales_amount"),
        ("order_count", "订单数", "measure", "SalesCube.order_count"),
        ("avg_order_value", "客单价", "measure", "SalesCube.avg_order_value"),
    ])
    output.print("OK SalesAnalysis 属性 (8)")

    # 8. 链接类型
    output.print("\n[8/8] 定义链接与同步指标...")

    link_types = [
        ("order_contains_product", "订单包含产品", "SalesOrder", "Product", "订单行对应产品"),
        ("order_belongs_customer", "订单归属客户", "SalesOrder", "Customer", "订单归属客户"),
        ("order_via_channel", "订单经渠道成交", "SalesOrder", "SalesChannel", "订单销售渠道"),
        ("product_has_orders", "产品有订单", "Product", "SalesOrder", "产品被哪些订单购买"),
        ("customer_places_orders", "客户下单", "Customer", "SalesOrder", "客户历史订单"),
        ("analysis_by_product", "分析归因产品", "SalesAnalysis", "Product", "指标按产品切片"),
        ("analysis_by_customer", "分析归因客户", "SalesAnalysis", "Customer", "指标按客户切片"),
        ("analysis_by_channel", "分析归因渠道", "SalesAnalysis", "SalesChannel", "指标按渠道切片"),
    ]
    for code, name, from_obj, to_obj, desc in link_types:
        s.onto.define_link_type(
            code=code,
            name=name,
            from_object_type_code=from_obj,
            to_object_type_code=to_obj,
            description=desc,
        )
        output.print(f"OK {code}")

    s.sync_metric_refs()
    output.print("OK sync_metric_refs")

    summary = {
        "ok": True,
        "space_id": space_id,
        "tables": 4,
        "cubes": 5,
        "object_types": 5,
        "properties": 29,
        "link_types": 8,
    }

    output.print("\n=== 产品销售本体初始化完成 ===")
    output.success("初始化成功")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))
