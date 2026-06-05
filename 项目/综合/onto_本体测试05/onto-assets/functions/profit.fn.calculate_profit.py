# 本体函数脚本（从服务端拉取）
# function_id: profit.fn.calculate_profit
# script_id: 6e70f76a-5d9c-40aa-9810-0554d5926e71
# space_id: space__0519

import json


def _step(title: str) -> None:
    output.print(f"\n===== {title} =====")


def main():
    # 获取指定空间
    space_id = "space__0519"
    database_name = "space__0519"
    s = space.get(space_id)

    _step("步骤0：空间")
    output.print(f"已获取空间: {s.name} id={s.id} db={database_name}")

    _step("步骤1：建表")
    s.sql.execute(
        """
        CREATE TABLE IF NOT EXISTS product_info (
            product_id String,
            product_name String,
            category String,
            PRIMARY KEY (product_id)
        ) ENGINE = MergeTree()
        ORDER BY (product_id)
        """
    )
    s.sql.execute(
        """
        CREATE TABLE IF NOT EXISTS price_info (
            product_id String,
            price Decimal(18, 2),
            price_date Date,
            PRIMARY KEY (product_id, price_date)
        ) ENGINE = MergeTree()
        ORDER BY (product_id, price_date)
        """
    )
    output.will_create("table", "product_info/price_info", "产品价格分析基础表")

    _step("步骤2：注册元数据")
    s.tables.register("product_info", label="产品信息")
    s.tables.sync_columns("product_info")
    s.tables.register("price_info", label="价格信息")
    s.tables.sync_columns("price_info")

    _step("步骤3：注册 Cube")
    s.register_cube(
        name="ProductPriceAnalysisCube",
        table="price_info",
        title="产品价格分析",
        measures=[
            {"name": "price", "col": "price", "agg": "avg", "title": "平均价格"},
        ],
        dimensions=[
            {"name": "product_id", "col": "product_id", "type": "string", "title": "产品 ID"},
            {"name": "price_date", "col": "price_date", "type": "string", "title": "价格日期"},
        ],
    )

    _step("步骤4：定义本体对象")
    s.onto.define_object_type("Product", "产品", description="产品价格分析中的产品对象")
    s.onto.bind_source("Product", "dazi_cube", config={"cube": "ProductPriceAnalysisCube"})
    s.onto.define_property(
        "Product", "product_id", "产品 ID", semantic_role="dimension", qualified_name="ProductPriceAnalysisCube.product_id"
    )
    s.onto.define_property(
        "Product", "price", "产品价格", semantic_role="measure", qualified_name="ProductPriceAnalysisCube.price"
    )
    s.onto.define_property(
        "Product", "price_date", "价格日期", semantic_role="dimension", qualified_name="ProductPriceAnalysisCube.price_date"
    )

    _step("步骤5：注册本体函数")
    onto.register_function("product_price_analysis", "dazi_script.ontology_function", script_id="<脚本UUID>", entry="main")

    ref_n = s.sync_metric_refs()
    output.print(f"sync_metric_refs: {ref_n}")

    output.success("产品价格分析本体方案 执行完成")
    summary = {
        "空间": s.name,
        "space_id": s.id,
        "database": database_name,
        "cubes": ["ProductPriceAnalysisCube"],
        "object_types": ["Product"],
        "ontology_explicit": True,
    }
    output.summary(summary)

    # AI 回归输出：固定前缀 + 单行 JSON，便于自动解析
    ai_summary = {
        "ok": True,
        "script": "product_price_analysis_setup",
        "space_id": s.id,
        "summary": summary,
    }
    output.print("__JSON_SUMMARY__" + json.dumps(ai_summary, ensure_ascii=True, default=str))