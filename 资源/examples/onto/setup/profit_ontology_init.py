"""Profit Analysis Ontology Initialization Script for space__profit0520

初始化内容：
1. 创建物理表（3张）
2. 注册Cube（4个）
3. 定义对象类型（4种）
4. 绑定数据源
5. 定义属性（25个）
6. 定义链接类型（6种）
7. 同步指标引用

参考示例：资源/examples/onto/setup/profit_ontology_init.py（开发请复制到 项目/onto_<名>/脚本/）
"""

import json


def main():
    space_id = "space__profit0520"
    s = space.get(space_id)

    output.print("=== Start Profit Analysis Ontology Initialization ===")
    output.print(f"Space: {space_id}")

    # 1. 创建物理表
    output.print("\n[1/7] Creating physical tables...")

    # 1.1 利润分析事实表
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS profit_analysis_fact (
            order_id String,
            product_id String,
            customer_id String,
            order_date Date,
            product_category String,
            customer_region String,
            customer_type String,
            quantity Int32,
            unit_price Float64,
            revenue Float64,
            cost Float64
        ) ENGINE = MergeTree()
        ORDER BY (order_date, order_id)
    """)
    output.print("OK profit_analysis_fact")

    # 1.2 产品维度表
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS product_dimension (
            product_id String,
            product_name String,
            product_category String,
            cost_price Float64,
            margin_ratio Float64,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (product_id)
    """)
    output.print("OK product_dimension")

    # 1.3 客户维度表
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS customer_dimension (
            customer_id String,
            customer_name String,
            customer_region String,
            customer_type String,
            credit_level String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (customer_id)
    """)
    output.print("OK customer_dimension")

    # 2. 注册表到空间
    output.print("\n[2/7] Registering tables to space...")

    s.tables.register("profit_analysis_fact", label="利润分析事实表")
    s.tables.sync_columns("profit_analysis_fact")
    output.print("OK profit_analysis_fact registered")

    s.tables.register("product_dimension", label="产品维度表")
    s.tables.sync_columns("product_dimension")
    output.print("OK product_dimension registered")

    s.tables.register("customer_dimension", label="客户维度表")
    s.tables.sync_columns("customer_dimension")
    output.print("OK customer_dimension registered")

    # 3. 注册Cube
    output.print("\n[3/7] Registering Cubes...")

    # 3.1 ProfitCube
    s.register_cube(
        name="ProfitCube",
        table="profit_analysis_fact",
        title="利润分析主Cube",
        measures=[
            {"name": "quantity", "col": "quantity", "agg": "sum", "title": "销售数量"},
            {"name": "revenue", "col": "revenue", "agg": "sum", "title": "收入"},
            {"name": "cost", "col": "cost", "agg": "sum", "title": "成本"},
            {"name": "order_count", "col": "order_id", "agg": "uniq", "title": "订单数量"},
        ],
        dimensions=[
            {"name": "order_id", "col": "order_id", "type": "string", "title": "订单ID"},
            {"name": "order_date", "col": "order_date", "type": "date", "title": "订单日期"},
            {"name": "product_id", "col": "product_id", "type": "string", "title": "产品ID"},
            {"name": "product_category", "col": "product_category", "type": "string", "title": "产品类别"},
            {"name": "customer_id", "col": "customer_id", "type": "string", "title": "客户ID"},
            {"name": "customer_region", "col": "customer_region", "type": "string", "title": "客户区域"},
            {"name": "customer_type", "col": "customer_type", "type": "string", "title": "客户类型"},
        ],
    )
    output.print("OK ProfitCube registered")

    # 3.2 ProductCube
    s.register_cube(
        name="ProductCube",
        table="profit_analysis_fact",
        title="产品分析Cube",
        measures=[
            {"name": "revenue", "col": "revenue", "agg": "sum", "title": "收入"},
            {"name": "cost", "col": "cost", "agg": "sum", "title": "成本"},
            {"name": "order_count", "col": "order_id", "agg": "uniq", "title": "订单数量"},
        ],
        dimensions=[
            {"name": "product_id", "col": "product_id", "type": "string", "title": "产品ID"},
            {"name": "product_category", "col": "product_category", "type": "string", "title": "产品类别"},
        ],
    )
    output.print("OK ProductCube registered")

    # 3.3 CustomerCube
    s.register_cube(
        name="CustomerCube",
        table="profit_analysis_fact",
        title="客户分析Cube",
        measures=[
            {"name": "revenue", "col": "revenue", "agg": "sum", "title": "收入"},
            {"name": "cost", "col": "cost", "agg": "sum", "title": "成本"},
            {"name": "order_count", "col": "order_id", "agg": "uniq", "title": "订单数量"},
        ],
        dimensions=[
            {"name": "customer_id", "col": "customer_id", "type": "string", "title": "客户ID"},
            {"name": "customer_region", "col": "customer_region", "type": "string", "title": "客户区域"},
            {"name": "customer_type", "col": "customer_type", "type": "string", "title": "客户类型"},
        ],
    )
    output.print("OK CustomerCube registered")

    # 3.4 TimeCube
    s.register_cube(
        name="TimeCube",
        table="profit_analysis_fact",
        title="时间维度Cube",
        measures=[
            {"name": "revenue", "col": "revenue", "agg": "sum", "title": "收入"},
            {"name": "cost", "col": "cost", "agg": "sum", "title": "成本"},
        ],
        dimensions=[
            {"name": "year", "col": "order_date", "type": "date", "title": "年份"},
            {"name": "year_month", "col": "order_date", "type": "string", "title": "年月"},
            {"name": "quarter", "col": "order_date", "type": "string", "title": "季度"},
        ],
    )
    output.print("OK TimeCube registered")

    # 4. 添加派生度量
    output.print("\n[4/7] Adding derived measures...")

    # ProfitCube派生度量
    s.upsert_derived_measures(
        "ProfitCube",
        [
            {
                "name": "profit",
                "title": "利润",
                "expression": "ProfitCube.revenue - ProfitCube.cost",
                "description": "利润（收入-成本）"
            },
            {
                "name": "profit_margin",
                "title": "利润率",
                "expression": "if(ProfitCube.revenue > 0, ProfitCube.profit / ProfitCube.revenue, 0)",
                "description": "利润率"
            }
        ]
    )
    output.print("OK ProfitCube derived measures")

    # ProductCube派生度量
    s.upsert_derived_measures(
        "ProductCube",
        [
            {
                "name": "profit",
                "title": "利润",
                "expression": "ProductCube.revenue - ProductCube.cost",
                "description": "利润（收入-成本）"
            },
            {
                "name": "profit_margin",
                "title": "利润率",
                "expression": "if(ProductCube.revenue > 0, ProductCube.profit / ProductCube.revenue, 0)",
                "description": "利润率"
            }
        ]
    )
    output.print("OK ProductCube derived measures")

    # CustomerCube派生度量
    s.upsert_derived_measures(
        "CustomerCube",
        [
            {
                "name": "profit",
                "title": "利润",
                "expression": "CustomerCube.revenue - CustomerCube.cost",
                "description": "利润（收入-成本）"
            },
            {
                "name": "profit_margin",
                "title": "利润率",
                "expression": "if(CustomerCube.revenue > 0, CustomerCube.profit / CustomerCube.revenue, 0)",
                "description": "利润率"
            }
        ]
    )
    output.print("OK CustomerCube derived measures")

    # TimeCube派生度量
    s.upsert_derived_measures(
        "TimeCube",
        [
            {
                "name": "profit",
                "title": "利润",
                "expression": "TimeCube.revenue - TimeCube.cost",
                "description": "利润（收入-成本）"
            },
            {
                "name": "profit_margin",
                "title": "利润率",
                "expression": "if(TimeCube.revenue > 0, TimeCube.profit / TimeCube.revenue, 0)",
                "description": "利润率"
            }
        ]
    )
    output.print("OK TimeCube derived measures")

    # 5. 定义对象类型
    output.print("\n[5/7] Defining object types...")

    object_types = [
        ("Order", "订单", "订单业务对象"),
        ("Product", "产品", "产品业务对象"),
        ("Customer", "客户", "客户业务对象"),
        ("ProfitAnalysis", "利润分析", "利润聚合对象"),
    ]

    for code, name, desc in object_types:
        s.onto.define_object_type(code, name, description=desc)
        output.print(f"OK {code}")

    # 6. 绑定数据源
    output.print("\n[6/7] Binding data sources...")

    s.onto.bind_source("Order", "dazi_cube", config={"cube": "ProfitCube"})
    output.print("OK Order -> ProfitCube")

    s.onto.bind_source("Product", "dazi_cube", config={"cube": "ProductCube"})
    output.print("OK Product -> ProductCube")

    s.onto.bind_source("Customer", "dazi_cube", config={"cube": "CustomerCube"})
    output.print("OK Customer -> CustomerCube")

    s.onto.bind_source("ProfitAnalysis", "dazi_cube", config={"cube": "ProfitCube"})
    output.print("OK ProfitAnalysis -> ProfitCube")

    # 7. 定义属性
    output.print("\n[7/7] Defining properties...")

    # Order属性
    order_props = [
        ("id", "订单ID", "dimension", "ProfitCube.order_id"),
        ("date", "订单日期", "dimension", "ProfitCube.order_date"),
        ("quantity", "销售数量", "measure", "ProfitCube.quantity"),
        ("revenue", "收入", "measure", "ProfitCube.revenue"),
        ("cost", "成本", "measure", "ProfitCube.cost"),
        ("profit", "利润", "measure", "ProfitCube.profit"),
        ("profit_margin", "利润率", "measure", "ProfitCube.profit_margin"),
    ]
    for code, name, role, qn in order_props:
        s.onto.define_property("Order", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK Order properties (7)")

    # Product属性
    product_props = [
        ("id", "产品ID", "dimension", "ProductCube.product_id"),
        ("category", "产品类别", "dimension", "ProductCube.product_category"),
        ("revenue", "累计收入", "measure", "ProductCube.revenue"),
        ("cost", "累计成本", "measure", "ProductCube.cost"),
        ("profit", "累计利润", "measure", "ProductCube.profit"),
        ("profit_margin", "利润率", "measure", "ProductCube.profit_margin"),
        ("order_count", "订单数", "measure", "ProductCube.order_count"),
    ]
    for code, name, role, qn in product_props:
        s.onto.define_property("Product", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK Product properties (7)")

    # Customer属性
    customer_props = [
        ("id", "客户ID", "dimension", "CustomerCube.customer_id"),
        ("region", "客户区域", "dimension", "CustomerCube.customer_region"),
        ("type", "客户类型", "dimension", "CustomerCube.customer_type"),
        ("revenue", "累计收入", "measure", "CustomerCube.revenue"),
        ("cost", "累计成本", "measure", "CustomerCube.cost"),
        ("profit", "累计利润", "measure", "CustomerCube.profit"),
        ("profit_margin", "利润率", "measure", "CustomerCube.profit_margin"),
        ("order_count", "订单数", "measure", "CustomerCube.order_count"),
    ]
    for code, name, role, qn in customer_props:
        s.onto.define_property("Customer", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK Customer properties (8)")

    # ProfitAnalysis属性
    profit_props = [
        ("date", "日期", "dimension", "ProfitCube.order_date"),
        ("product_category", "产品类别", "dimension", "ProfitCube.product_category"),
        ("customer_region", "客户区域", "dimension", "ProfitCube.customer_region"),
        ("customer_type", "客户类型", "dimension", "ProfitCube.customer_type"),
        ("revenue", "收入", "measure", "ProfitCube.revenue"),
        ("cost", "成本", "measure", "ProfitCube.cost"),
        ("profit", "利润", "measure", "ProfitCube.profit"),
        ("profit_margin", "利润率", "measure", "ProfitCube.profit_margin"),
    ]
    for code, name, role, qn in profit_props:
        s.onto.define_property("ProfitAnalysis", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK ProfitAnalysis properties (8)")

    # 8. 定义链接类型
    output.print("\n[8/7] Defining link types...")

    link_types = [
        ("order_to_product", "订单关联产品", "Order", "Product", "订单包含的产品"),
        ("order_to_customer", "订单关联客户", "Order", "Customer", "订单归属客户"),
        ("profit_to_product", "利润关联产品", "ProfitAnalysis", "Product", "利润归因到产品"),
        ("profit_to_customer", "利润关联客户", "ProfitAnalysis", "Customer", "利润归因到客户"),
        ("product_to_profit", "产品归属利润", "Product", "ProfitAnalysis", "产品利润聚合"),
        ("customer_to_profit", "客户归属利润", "Customer", "ProfitAnalysis", "客户利润聚合"),
    ]

    for code, name, from_obj, to_obj, desc in link_types:
        s.onto.define_link_type(
            code=code,
            name=name,
            from_object_type_code=from_obj,
            to_object_type_code=to_obj,
            description=desc
        )
        output.print(f"OK {code}")

    # 9. 同步指标引用
    output.print("\n[9/7] Syncing metric references...")
    s.sync_metric_refs()
    output.print("OK sync_metric_refs")

    # 总结
    summary = {
        "ok": True,
        "space_id": space_id,
        "tables": 3,
        "cubes": 4,
        "derived_measures": 8,
        "object_types": 4,
        "properties": 30,
        "link_types": 6,
    }

    output.print("\n=== Profit Analysis Ontology Initialization Completed ===")
    output.print(f"Tables: {summary['tables']}")
    output.print(f"Cubes: {summary['cubes']}")
    output.print(f"Derived Measures: {summary['derived_measures']}")
    output.print(f"Object Types: {summary['object_types']}")
    output.print(f"Properties: {summary['properties']}")
    output.print(f"Link Types: {summary['link_types']}")
    output.success("Initialization completed successfully")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))
