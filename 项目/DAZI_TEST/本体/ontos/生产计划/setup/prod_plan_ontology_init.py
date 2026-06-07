"""生产计划本体初始化脚本 — space_cate_test01

初始化内容：
1. 创建物理表（4 维 + 5 事实，不含 dim_date）
2. 注册表到空间（含 display_name / description）
3. 注册表间关系（20 条，含 5 条 fact→dim_date）
4. 注册 Cube（9 个）及派生度量
5. 定义对象类型（11 种）、绑定数据源、属性、链接（17 种）
6. 同步指标引用
7. 输出 JSON summary

不含 apply_registry（分类在 prod_plan_category_mount.py）。

放置：项目/DAZI_TEST/本体/ontos/生产计划/setup/prod_plan_ontology_init.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/生产计划/setup/prod_plan_ontology_init.py --space space_cate_test01 --type setup
规划对照：项目/DAZI_TEST/本体/ontos/生产计划/plans/生产计划本体规划方案.md
"""

import json

# 与规划文档 §2 对齐：display_name=侧栏显示名，description=业务说明
TABLE_REGISTRY = {
    "dim_plant": {
        "display_name": "工厂维表",
        "description": "生产工厂/制造基地主数据",
        "columns": [
            {"name": "plant_id", "display_name": "工厂 ID", "description": "主键"},
            {"name": "plant_code", "display_name": "工厂编码"},
            {"name": "plant_name", "display_name": "工厂名称"},
            {"name": "company_code", "display_name": "公司代码"},
            {"name": "plant_type", "display_name": "工厂类型", "description": "炼油/烯烃/芳烃/精细化工"},
            {"name": "region", "display_name": "区域"},
            {"name": "design_capacity", "display_name": "设计产能"},
            {"name": "capacity_unit", "display_name": "产能单位", "description": "吨/年"},
            {"name": "status", "display_name": "状态", "description": "运行/检修/停产"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_work_center": {
        "display_name": "工作中心维表",
        "description": "产线、装置工段或工作中心主数据",
        "columns": [
            {"name": "work_center_id", "display_name": "工作中心 ID", "description": "主键"},
            {"name": "work_center_code", "display_name": "工作中心编码"},
            {"name": "work_center_name", "display_name": "工作中心名称"},
            {"name": "plant_id", "display_name": "所属工厂", "description": "关联 dim_plant"},
            {"name": "plant_name", "display_name": "工厂名称", "description": "冗余"},
            {"name": "center_type", "display_name": "中心类型", "description": "反应/分离/包装/公用"},
            {"name": "production_mode", "display_name": "生产模式", "description": "连续/批次/混合"},
            {"name": "standard_capacity_qty", "display_name": "标准产能"},
            {"name": "capacity_unit", "display_name": "产能单位", "description": "吨/批"},
            {"name": "available_hours_per_day", "display_name": "日可用工时", "description": "小时"},
            {"name": "criticality", "display_name": "关键等级", "description": "A/B/C"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_product": {
        "display_name": "产品维表",
        "description": "成品/半成品/关键物料主数据",
        "columns": [
            {"name": "product_id", "display_name": "产品 ID", "description": "主键"},
            {"name": "product_code", "display_name": "产品编码"},
            {"name": "product_name", "display_name": "产品名称"},
            {"name": "product_category", "display_name": "产品大类", "description": "烯烃/芳烃/聚合物等"},
            {"name": "product_subcategory", "display_name": "产品小类"},
            {"name": "product_type", "display_name": "物料类型", "description": "成品/半成品/关键组件"},
            {"name": "unit", "display_name": "计量单位", "description": "吨/千克/批"},
            {"name": "standard_cycle_hours", "display_name": "标准生产周期", "description": "小时/单位"},
            {"name": "shelf_life_days", "display_name": "保质期", "description": "天，可空"},
            {"name": "status", "display_name": "状态", "description": "在产/停产"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_plan_version": {
        "display_name": "计划版本维表",
        "description": "MPS/周计划/滚动计划版本主数据",
        "columns": [
            {"name": "plan_version_id", "display_name": "版本 ID", "description": "主键"},
            {"name": "plan_version_code", "display_name": "版本编码", "description": "如 MPS-2026-06"},
            {"name": "plan_version_name", "display_name": "版本名称"},
            {"name": "plan_type", "display_name": "计划类型", "description": "MPS/周计划/滚动计划"},
            {"name": "fiscal_year", "display_name": "计划年度"},
            {"name": "fiscal_month", "display_name": "计划月份", "description": "1-12"},
            {"name": "fiscal_week", "display_name": "计划周", "description": "1-53"},
            {"name": "effective_from", "display_name": "生效开始"},
            {"name": "effective_to", "display_name": "生效结束"},
            {"name": "status", "display_name": "状态", "description": "草稿/已发布/已关闭"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_production_plan": {
        "display_name": "生产计划事实表",
        "description": "MPS 计划行：产品×产线×周期",
        "columns": [
            {"name": "plan_line_id", "display_name": "计划行 ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date"},
            {"name": "plan_version_id", "display_name": "计划版本", "description": "关联 dim_plan_version"},
            {"name": "plan_version_code", "display_name": "版本编码", "description": "冗余"},
            {"name": "plant_id", "display_name": "工厂 ID", "description": "关联 dim_plant"},
            {"name": "plant_name", "display_name": "工厂名称", "description": "冗余"},
            {"name": "work_center_id", "display_name": "工作中心", "description": "关联 dim_work_center"},
            {"name": "work_center_name", "display_name": "工作中心名称", "description": "冗余"},
            {"name": "product_id", "display_name": "产品 ID", "description": "关联 dim_product"},
            {"name": "product_code", "display_name": "产品编码", "description": "冗余"},
            {"name": "product_name", "display_name": "产品名称", "description": "冗余"},
            {"name": "product_category", "display_name": "产品大类", "description": "冗余"},
            {"name": "fiscal_year", "display_name": "计划年度"},
            {"name": "fiscal_month", "display_name": "计划月份"},
            {"name": "fiscal_week", "display_name": "计划周"},
            {"name": "planned_qty", "display_name": "计划产量"},
            {"name": "planned_hours", "display_name": "计划工时"},
            {"name": "unit", "display_name": "计量单位", "description": "冗余"},
            {"name": "priority", "display_name": "优先级", "description": "1=最高"},
            {"name": "demand_source", "display_name": "需求来源", "description": "销售预测/安全库存/手工"},
            {"name": "status", "display_name": "状态", "description": "草稿/已确认/已关闭"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_work_order": {
        "display_name": "生产工单事实表",
        "description": "生产工单头粒度：计划量/完工量/状态",
        "columns": [
            {"name": "work_order_id", "display_name": "工单 ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date（下达日）"},
            {"name": "release_date", "display_name": "下达日期"},
            {"name": "plan_line_id", "display_name": "来源计划行", "description": "关联 fact_production_plan，可空"},
            {"name": "plan_version_id", "display_name": "计划版本", "description": "冗余"},
            {"name": "plant_id", "display_name": "工厂 ID", "description": "冗余"},
            {"name": "plant_name", "display_name": "工厂名称", "description": "冗余"},
            {"name": "work_center_id", "display_name": "工作中心", "description": "关联 dim_work_center"},
            {"name": "work_center_name", "display_name": "工作中心名称", "description": "冗余"},
            {"name": "product_id", "display_name": "产品 ID", "description": "关联 dim_product"},
            {"name": "product_code", "display_name": "产品编码", "description": "冗余"},
            {"name": "product_name", "display_name": "产品名称", "description": "冗余"},
            {"name": "order_qty", "display_name": "工单数量"},
            {"name": "completed_qty", "display_name": "完工数量"},
            {"name": "scrapped_qty", "display_name": "报废数量"},
            {"name": "unit", "display_name": "计量单位"},
            {"name": "planned_start_date", "display_name": "计划开工"},
            {"name": "planned_end_date", "display_name": "计划完工"},
            {"name": "actual_start_date", "display_name": "实际开工", "description": "可空"},
            {"name": "actual_end_date", "display_name": "实际完工", "description": "可空"},
            {"name": "status", "display_name": "工单状态", "description": "已创建/已下达/生产中/已完工/已关闭/已取消"},
            {"name": "is_on_schedule", "display_name": "是否按期", "description": "1=按期"},
            {"name": "delay_days", "display_name": "延期天数"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_production_daily": {
        "display_name": "日生产实绩事实表",
        "description": "产线×产品×日汇总实绩；计划对比实际侧主源",
        "columns": [
            {"name": "daily_id", "display_name": "实绩 ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date"},
            {"name": "calendar_date", "display_name": "统计日期"},
            {"name": "plant_id", "display_name": "工厂 ID", "description": "冗余"},
            {"name": "plant_name", "display_name": "工厂名称", "description": "冗余"},
            {"name": "work_center_id", "display_name": "工作中心", "description": "关联 dim_work_center"},
            {"name": "work_center_name", "display_name": "工作中心名称", "description": "冗余"},
            {"name": "product_id", "display_name": "产品 ID", "description": "关联 dim_product"},
            {"name": "product_code", "display_name": "产品编码", "description": "冗余"},
            {"name": "product_name", "display_name": "产品名称", "description": "冗余"},
            {"name": "product_category", "display_name": "产品大类", "description": "冗余"},
            {"name": "shift_code", "display_name": "班次", "description": "早/中/晚/全天"},
            {"name": "planned_qty", "display_name": "日计划产量"},
            {"name": "actual_qty", "display_name": "实际产量"},
            {"name": "qualified_qty", "display_name": "合格产量"},
            {"name": "rework_qty", "display_name": "返工量"},
            {"name": "scrapped_qty", "display_name": "报废量"},
            {"name": "planned_hours", "display_name": "计划工时"},
            {"name": "actual_hours", "display_name": "实际工时"},
            {"name": "unit", "display_name": "计量单位"},
            {"name": "data_source", "display_name": "数据来源", "description": "MES/手工"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_material_requirement": {
        "display_name": "物料需求事实表",
        "description": "组件需求 vs 发料对比",
        "columns": [
            {"name": "mrp_line_id", "display_name": "需求行 ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date（需求日）"},
            {"name": "requirement_date", "display_name": "需求日期"},
            {"name": "work_order_id", "display_name": "关联工单", "description": "关联 fact_work_order，可空"},
            {"name": "plant_id", "display_name": "工厂 ID", "description": "冗余"},
            {"name": "parent_product_id", "display_name": "父项产品", "description": "关联 dim_product"},
            {"name": "parent_product_code", "display_name": "父项编码", "description": "冗余"},
            {"name": "component_product_id", "display_name": "组件物料", "description": "关联 dim_product"},
            {"name": "component_product_code", "display_name": "组件编码", "description": "冗余"},
            {"name": "component_product_name", "display_name": "组件名称", "description": "冗余"},
            {"name": "planned_require_qty", "display_name": "计划需求量"},
            {"name": "actual_issue_qty", "display_name": "实际发料量"},
            {"name": "unit", "display_name": "计量单位"},
            {"name": "is_critical", "display_name": "是否关键料", "description": "0/1"},
            {"name": "kit_status", "display_name": "齐套状态", "description": "齐套/部分齐套/缺料"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_capacity_load": {
        "display_name": "产能负荷事实表",
        "description": "工作中心按日/周的可用产能与计划/实际负荷",
        "columns": [
            {"name": "load_id", "display_name": "负荷 ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date"},
            {"name": "calendar_date", "display_name": "统计日期"},
            {"name": "plan_version_id", "display_name": "计划版本", "description": "关联 dim_plan_version"},
            {"name": "plant_id", "display_name": "工厂 ID", "description": "冗余"},
            {"name": "work_center_id", "display_name": "工作中心", "description": "关联 dim_work_center"},
            {"name": "work_center_name", "display_name": "工作中心名称", "description": "冗余"},
            {"name": "available_hours", "display_name": "可用工时"},
            {"name": "planned_load_hours", "display_name": "计划负荷工时"},
            {"name": "actual_load_hours", "display_name": "实际负荷工时"},
            {"name": "planned_output_qty", "display_name": "计划产出量"},
            {"name": "actual_output_qty", "display_name": "实际产出量"},
            {"name": "capacity_unit", "display_name": "产能单位"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
}


def main():
    space_id = "space_cate_test01"
    s = space.get(space_id)

    output.print("=== 生产计划本体初始化 ===")
    output.print(f"空间: {space_id}")

    # 1. 创建物理表
    output.print("\n[1/8] 创建物理表...")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_plant (
            plant_id String,
            plant_code String,
            plant_name String,
            company_code String,
            plant_type String,
            region String,
            design_capacity Float64,
            capacity_unit String,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (plant_code)
    """)
    output.print("OK dim_plant")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_work_center (
            work_center_id String,
            work_center_code String,
            work_center_name String,
            plant_id String,
            plant_name String,
            center_type String,
            production_mode String,
            standard_capacity_qty Float64,
            capacity_unit String,
            available_hours_per_day Float64,
            criticality String,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (plant_id, work_center_code)
    """)
    output.print("OK dim_work_center")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_product (
            product_id String,
            product_code String,
            product_name String,
            product_category String,
            product_subcategory String,
            product_type String,
            unit String,
            standard_cycle_hours Float64,
            shelf_life_days Nullable(Int32),
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (product_code)
    """)
    output.print("OK dim_product")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_plan_version (
            plan_version_id String,
            plan_version_code String,
            plan_version_name String,
            plan_type String,
            fiscal_year Int32,
            fiscal_month Int32,
            fiscal_week Int32,
            effective_from Date,
            effective_to Date,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (fiscal_year, fiscal_month, plan_version_code)
    """)
    output.print("OK dim_plan_version")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_production_plan (
            plan_line_id String,
            date_key Int32,
            plan_version_id String,
            plan_version_code String,
            plant_id String,
            plant_name String,
            work_center_id String,
            work_center_name String,
            product_id String,
            product_code String,
            product_name String,
            product_category String,
            fiscal_year Int32,
            fiscal_month Int32,
            fiscal_week Int32,
            planned_qty Float64,
            planned_hours Float64,
            unit String,
            priority Int32,
            demand_source String,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (fiscal_year, fiscal_month, work_center_id, plan_line_id)
    """)
    output.print("OK fact_production_plan")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_work_order (
            work_order_id String,
            date_key Int32,
            release_date Date,
            plan_line_id String,
            plan_version_id String,
            plant_id String,
            plant_name String,
            work_center_id String,
            work_center_name String,
            product_id String,
            product_code String,
            product_name String,
            order_qty Float64,
            completed_qty Float64,
            scrapped_qty Float64,
            unit String,
            planned_start_date Date,
            planned_end_date Date,
            actual_start_date Nullable(Date),
            actual_end_date Nullable(Date),
            status String,
            is_on_schedule UInt8,
            delay_days Int32,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (date_key, work_center_id, work_order_id)
    """)
    output.print("OK fact_work_order")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_production_daily (
            daily_id String,
            date_key Int32,
            calendar_date Date,
            plant_id String,
            plant_name String,
            work_center_id String,
            work_center_name String,
            product_id String,
            product_code String,
            product_name String,
            product_category String,
            shift_code String,
            planned_qty Float64,
            actual_qty Float64,
            qualified_qty Float64,
            rework_qty Float64,
            scrapped_qty Float64,
            planned_hours Float64,
            actual_hours Float64,
            unit String,
            data_source String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (date_key, work_center_id, product_id, shift_code)
    """)
    output.print("OK fact_production_daily")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_material_requirement (
            mrp_line_id String,
            date_key Int32,
            requirement_date Date,
            work_order_id String,
            plant_id String,
            parent_product_id String,
            parent_product_code String,
            component_product_id String,
            component_product_code String,
            component_product_name String,
            planned_require_qty Float64,
            actual_issue_qty Float64,
            unit String,
            is_critical UInt8,
            kit_status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (date_key, work_order_id, mrp_line_id)
    """)
    output.print("OK fact_material_requirement")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_capacity_load (
            load_id String,
            date_key Int32,
            calendar_date Date,
            plan_version_id String,
            plant_id String,
            work_center_id String,
            work_center_name String,
            available_hours Float64,
            planned_load_hours Float64,
            actual_load_hours Float64,
            planned_output_qty Float64,
            actual_output_qty Float64,
            capacity_unit String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (date_key, work_center_id, load_id)
    """)
    output.print("OK fact_capacity_load")

    # 2. 注册表（含 display_name / description）
    output.print("\n[2/8] 注册表到空间...")

    for tbl_name, meta in TABLE_REGISTRY.items():
        s.tables.register_with_meta(
            table_name=tbl_name,
            display_name=meta["display_name"],
            description=meta.get("description"),
            columns=meta["columns"],
            force_column_meta=True,
        )
        output.print(f"OK {tbl_name} ({meta['display_name']})")

    # 3. 注册表间关系（20 条，规划 §三）
    output.print("\n[3/8] 注册表间关系...")

    table_relationships = [
        {
            "from_table": "fact_production_plan",
            "to_table": "dim_date",
            "join_sql": "fact_production_plan.date_key = dim_date.date_key",
            "join_keys": [{"from": "date_key", "to": "date_key"}],
            "relationship_type": "many_to_one",
            "description": "计划→日历",
        },
        {
            "from_table": "fact_work_order",
            "to_table": "dim_date",
            "join_sql": "fact_work_order.date_key = dim_date.date_key",
            "join_keys": [{"from": "date_key", "to": "date_key"}],
            "relationship_type": "many_to_one",
            "description": "工单→日历",
        },
        {
            "from_table": "fact_production_daily",
            "to_table": "dim_date",
            "join_sql": "fact_production_daily.date_key = dim_date.date_key",
            "join_keys": [{"from": "date_key", "to": "date_key"}],
            "relationship_type": "many_to_one",
            "description": "日实绩→日历",
        },
        {
            "from_table": "fact_material_requirement",
            "to_table": "dim_date",
            "join_sql": "fact_material_requirement.date_key = dim_date.date_key",
            "join_keys": [{"from": "date_key", "to": "date_key"}],
            "relationship_type": "many_to_one",
            "description": "物料需求→日历",
        },
        {
            "from_table": "fact_capacity_load",
            "to_table": "dim_date",
            "join_sql": "fact_capacity_load.date_key = dim_date.date_key",
            "join_keys": [{"from": "date_key", "to": "date_key"}],
            "relationship_type": "many_to_one",
            "description": "产能负荷→日历",
        },
        {
            "from_table": "dim_work_center",
            "to_table": "dim_plant",
            "join_sql": "dim_work_center.plant_id = dim_plant.plant_id",
            "join_keys": [{"from": "plant_id", "to": "plant_id"}],
            "relationship_type": "many_to_one",
            "description": "工作中心→工厂",
        },
        {
            "from_table": "fact_production_plan",
            "to_table": "dim_plant",
            "join_sql": "fact_production_plan.plant_id = dim_plant.plant_id",
            "join_keys": [{"from": "plant_id", "to": "plant_id"}],
            "relationship_type": "many_to_one",
            "description": "计划→工厂",
        },
        {
            "from_table": "fact_production_plan",
            "to_table": "dim_work_center",
            "join_sql": "fact_production_plan.work_center_id = dim_work_center.work_center_id",
            "join_keys": [{"from": "work_center_id", "to": "work_center_id"}],
            "relationship_type": "many_to_one",
            "description": "计划→工作中心",
        },
        {
            "from_table": "fact_production_plan",
            "to_table": "dim_product",
            "join_sql": "fact_production_plan.product_id = dim_product.product_id",
            "join_keys": [{"from": "product_id", "to": "product_id"}],
            "relationship_type": "many_to_one",
            "description": "计划→产品",
        },
        {
            "from_table": "fact_production_plan",
            "to_table": "dim_plan_version",
            "join_sql": "fact_production_plan.plan_version_id = dim_plan_version.plan_version_id",
            "join_keys": [{"from": "plan_version_id", "to": "plan_version_id"}],
            "relationship_type": "many_to_one",
            "description": "计划→版本",
        },
        {
            "from_table": "fact_work_order",
            "to_table": "dim_work_center",
            "join_sql": "fact_work_order.work_center_id = dim_work_center.work_center_id",
            "join_keys": [{"from": "work_center_id", "to": "work_center_id"}],
            "relationship_type": "many_to_one",
            "description": "工单→工作中心",
        },
        {
            "from_table": "fact_work_order",
            "to_table": "dim_product",
            "join_sql": "fact_work_order.product_id = dim_product.product_id",
            "join_keys": [{"from": "product_id", "to": "product_id"}],
            "relationship_type": "many_to_one",
            "description": "工单→产品",
        },
        {
            "from_table": "fact_work_order",
            "to_table": "fact_production_plan",
            "join_sql": "fact_work_order.plan_line_id = fact_production_plan.plan_line_id",
            "join_keys": [{"from": "plan_line_id", "to": "plan_line_id"}],
            "relationship_type": "many_to_one",
            "description": "工单来源计划行",
        },
        {
            "from_table": "fact_production_daily",
            "to_table": "dim_work_center",
            "join_sql": "fact_production_daily.work_center_id = dim_work_center.work_center_id",
            "join_keys": [{"from": "work_center_id", "to": "work_center_id"}],
            "relationship_type": "many_to_one",
            "description": "日实绩→工作中心",
        },
        {
            "from_table": "fact_production_daily",
            "to_table": "dim_product",
            "join_sql": "fact_production_daily.product_id = dim_product.product_id",
            "join_keys": [{"from": "product_id", "to": "product_id"}],
            "relationship_type": "many_to_one",
            "description": "日实绩→产品",
        },
        {
            "from_table": "fact_material_requirement",
            "to_table": "fact_work_order",
            "join_sql": "fact_material_requirement.work_order_id = fact_work_order.work_order_id",
            "join_keys": [{"from": "work_order_id", "to": "work_order_id"}],
            "relationship_type": "many_to_one",
            "description": "物料需求→工单",
        },
        {
            "from_table": "fact_material_requirement",
            "to_table": "dim_product",
            "join_sql": "fact_material_requirement.component_product_id = dim_product.product_id",
            "join_keys": [{"from": "component_product_id", "to": "product_id"}],
            "relationship_type": "many_to_one",
            "description": "组件→产品维",
        },
        {
            "from_table": "fact_capacity_load",
            "to_table": "dim_work_center",
            "join_sql": "fact_capacity_load.work_center_id = dim_work_center.work_center_id",
            "join_keys": [{"from": "work_center_id", "to": "work_center_id"}],
            "relationship_type": "many_to_one",
            "description": "负荷→工作中心",
        },
        {
            "from_table": "fact_capacity_load",
            "to_table": "dim_plan_version",
            "join_sql": "fact_capacity_load.plan_version_id = dim_plan_version.plan_version_id",
            "join_keys": [{"from": "plan_version_id", "to": "plan_version_id"}],
            "relationship_type": "many_to_one",
            "description": "负荷→计划版本",
        },
        {
            "from_table": "fact_production_plan",
            "to_table": "fact_production_daily",
            "join_sql": "fact_production_plan.work_center_id = fact_production_daily.work_center_id AND fact_production_plan.product_id = fact_production_daily.product_id AND fact_production_plan.date_key = fact_production_daily.date_key",
            "join_keys": [
                {"from": "work_center_id", "to": "work_center_id"},
                {"from": "product_id", "to": "product_id"},
                {"from": "date_key", "to": "date_key"},
            ],
            "relationship_type": "many_to_one",
            "description": "计划对比日实绩（逻辑 JOIN）",
        },
    ]
    for rel in table_relationships:
        s.tables.add_relationship(**rel)
        output.print(f"OK {rel['from_table']} -> {rel['to_table']}")

    # 4. 注册 Cube
    output.print("\n[4/8] 注册 Cube...")

    plan_tbl = "fact_production_plan"
    wo_tbl = "fact_work_order"
    daily_tbl = "fact_production_daily"
    mrp_tbl = "fact_material_requirement"
    load_tbl = "fact_capacity_load"

    daily_measures = [
        {"name": "planned_qty_total", "col": "planned_qty", "agg": "sum", "title": "日计划产量"},
        {"name": "actual_qty_total", "col": "actual_qty", "agg": "sum", "title": "实际产量"},
        {"name": "qualified_qty_total", "col": "qualified_qty", "agg": "sum", "title": "合格产量"},
        {"name": "rework_qty_total", "col": "rework_qty", "agg": "sum", "title": "返工量"},
        {"name": "scrapped_qty_total", "col": "scrapped_qty", "agg": "sum", "title": "报废量"},
        {"name": "planned_hours_total", "col": "planned_hours", "agg": "sum", "title": "计划工时"},
        {"name": "actual_hours_total", "col": "actual_hours", "agg": "sum", "title": "实际工时"},
        {"name": "daily_record_count", "col": "daily_id", "agg": "count", "title": "实绩行数"},
    ]

    daily_dims_full = [
        {"name": "daily_id", "col": "daily_id", "type": "string", "title": "实绩ID"},
        {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
        {"name": "calendar_date", "col": "calendar_date", "type": "date", "title": "统计日期"},
        {"name": "plant_id", "col": "plant_id", "type": "string", "title": "工厂ID"},
        {"name": "plant_name", "col": "plant_name", "type": "string", "title": "工厂名称"},
        {"name": "work_center_id", "col": "work_center_id", "type": "string", "title": "工作中心ID"},
        {"name": "work_center_name", "col": "work_center_name", "type": "string", "title": "工作中心名称"},
        {"name": "product_id", "col": "product_id", "type": "string", "title": "产品ID"},
        {"name": "product_code", "col": "product_code", "type": "string", "title": "产品编码"},
        {"name": "product_name", "col": "product_name", "type": "string", "title": "产品名称"},
        {"name": "product_category", "col": "product_category", "type": "string", "title": "产品大类"},
        {"name": "shift_code", "col": "shift_code", "type": "string", "title": "班次"},
    ]

    achievement_derived = lambda cube: [
        {
            "name": "achievement_rate",
            "title": "计划达成率",
            "expression": f"if({cube}.planned_qty_total > 0, {cube}.actual_qty_total / {cube}.planned_qty_total, 0)",
            "description": "实际产量 / 计划产量",
        },
        {
            "name": "first_pass_yield",
            "title": "一次合格率",
            "expression": f"if({cube}.actual_qty_total > 0, {cube}.qualified_qty_total / {cube}.actual_qty_total, 0)",
            "description": "合格产量 / 实际产量",
        },
    ]

    # ProductionPlanCube
    s.register_cube(
        name="ProductionPlanCube",
        table=plan_tbl,
        title="生产计划Cube",
        measures=[
            {"name": "planned_qty_total", "col": "planned_qty", "agg": "sum", "title": "计划产量合计"},
            {"name": "planned_hours_total", "col": "planned_hours", "agg": "sum", "title": "计划工时合计"},
            {"name": "plan_line_count", "col": "plan_line_id", "agg": "count", "title": "计划行数"},
        ],
        dimensions=[
            {"name": "plan_line_id", "col": "plan_line_id", "type": "string", "title": "计划行ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "plan_version_id", "col": "plan_version_id", "type": "string", "title": "计划版本ID"},
            {"name": "plan_version_code", "col": "plan_version_code", "type": "string", "title": "版本编码"},
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "计划年度"},
            {"name": "fiscal_month", "col": "fiscal_month", "type": "int", "title": "计划月份"},
            {"name": "fiscal_week", "col": "fiscal_week", "type": "int", "title": "计划周"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "工厂ID"},
            {"name": "plant_name", "col": "plant_name", "type": "string", "title": "工厂名称"},
            {"name": "work_center_id", "col": "work_center_id", "type": "string", "title": "工作中心ID"},
            {"name": "work_center_name", "col": "work_center_name", "type": "string", "title": "工作中心名称"},
            {"name": "product_id", "col": "product_id", "type": "string", "title": "产品ID"},
            {"name": "product_code", "col": "product_code", "type": "string", "title": "产品编码"},
            {"name": "product_name", "col": "product_name", "type": "string", "title": "产品名称"},
            {"name": "product_category", "col": "product_category", "type": "string", "title": "产品大类"},
            {"name": "priority", "col": "priority", "type": "int", "title": "优先级"},
            {"name": "demand_source", "col": "demand_source", "type": "string", "title": "需求来源"},
            {"name": "status", "col": "status", "type": "string", "title": "状态"},
        ],
    )
    output.print("OK ProductionPlanCube")

    # WorkOrderCube
    s.register_cube(
        name="WorkOrderCube",
        table=wo_tbl,
        title="生产工单Cube",
        measures=[
            {"name": "order_qty_total", "col": "order_qty", "agg": "sum", "title": "工单数量合计"},
            {"name": "completed_qty_total", "col": "completed_qty", "agg": "sum", "title": "完工数量合计"},
            {"name": "scrapped_qty_total", "col": "scrapped_qty", "agg": "sum", "title": "报废合计"},
            {"name": "work_order_count", "col": "work_order_id", "agg": "count", "title": "工单数"},
            {"name": "on_schedule_count", "col": "is_on_schedule", "agg": "sum", "title": "按期数"},
        ],
        dimensions=[
            {"name": "work_order_id", "col": "work_order_id", "type": "string", "title": "工单ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "release_date", "col": "release_date", "type": "date", "title": "下达日期"},
            {"name": "plan_version_id", "col": "plan_version_id", "type": "string", "title": "计划版本ID"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "工厂ID"},
            {"name": "work_center_id", "col": "work_center_id", "type": "string", "title": "工作中心ID"},
            {"name": "work_center_name", "col": "work_center_name", "type": "string", "title": "工作中心名称"},
            {"name": "product_id", "col": "product_id", "type": "string", "title": "产品ID"},
            {"name": "product_code", "col": "product_code", "type": "string", "title": "产品编码"},
            {"name": "product_name", "col": "product_name", "type": "string", "title": "产品名称"},
            {"name": "status", "col": "status", "type": "string", "title": "工单状态"},
            {"name": "is_on_schedule", "col": "is_on_schedule", "type": "int", "title": "是否按期"},
        ],
    )
    output.print("OK WorkOrderCube")

    # ProductionActualCube
    s.register_cube(
        name="ProductionActualCube",
        table=daily_tbl,
        title="日生产实绩Cube",
        measures=daily_measures,
        dimensions=daily_dims_full,
    )
    output.print("OK ProductionActualCube")

    # MaterialRequirementCube
    s.register_cube(
        name="MaterialRequirementCube",
        table=mrp_tbl,
        title="物料需求Cube",
        measures=[
            {"name": "planned_require_total", "col": "planned_require_qty", "agg": "sum", "title": "计划需求量"},
            {"name": "actual_issue_total", "col": "actual_issue_qty", "agg": "sum", "title": "实际发料量"},
            {"name": "mrp_line_count", "col": "mrp_line_id", "agg": "count", "title": "需求行数"},
        ],
        dimensions=[
            {"name": "mrp_line_id", "col": "mrp_line_id", "type": "string", "title": "需求行ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "requirement_date", "col": "requirement_date", "type": "date", "title": "需求日期"},
            {"name": "work_order_id", "col": "work_order_id", "type": "string", "title": "工单ID"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "工厂ID"},
            {"name": "parent_product_id", "col": "parent_product_id", "type": "string", "title": "父项产品ID"},
            {"name": "component_product_id", "col": "component_product_id", "type": "string", "title": "组件产品ID"},
            {"name": "component_product_code", "col": "component_product_code", "type": "string", "title": "组件编码"},
            {"name": "component_product_name", "col": "component_product_name", "type": "string", "title": "组件名称"},
            {"name": "is_critical", "col": "is_critical", "type": "int", "title": "是否关键料"},
            {"name": "kit_status", "col": "kit_status", "type": "string", "title": "齐套状态"},
        ],
    )
    output.print("OK MaterialRequirementCube")

    # CapacityLoadCube
    s.register_cube(
        name="CapacityLoadCube",
        table=load_tbl,
        title="产能负荷Cube",
        measures=[
            {"name": "available_hours_total", "col": "available_hours", "agg": "sum", "title": "可用工时"},
            {"name": "planned_load_hours_total", "col": "planned_load_hours", "agg": "sum", "title": "计划负荷工时"},
            {"name": "actual_load_hours_total", "col": "actual_load_hours", "agg": "sum", "title": "实际负荷工时"},
            {"name": "planned_output_total", "col": "planned_output_qty", "agg": "sum", "title": "计划产出"},
            {"name": "actual_output_total", "col": "actual_output_qty", "agg": "sum", "title": "实际产出"},
        ],
        dimensions=[
            {"name": "load_id", "col": "load_id", "type": "string", "title": "负荷ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "calendar_date", "col": "calendar_date", "type": "date", "title": "统计日期"},
            {"name": "plan_version_id", "col": "plan_version_id", "type": "string", "title": "计划版本ID"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "工厂ID"},
            {"name": "work_center_id", "col": "work_center_id", "type": "string", "title": "工作中心ID"},
            {"name": "work_center_name", "col": "work_center_name", "type": "string", "title": "工作中心名称"},
        ],
    )
    output.print("OK CapacityLoadCube")

    # WorkCenterCube（主体型，源表 fact_production_daily）
    s.register_cube(
        name="WorkCenterCube",
        table=daily_tbl,
        title="工作中心Cube",
        measures=daily_measures,
        dimensions=[
            {"name": "work_center_id", "col": "work_center_id", "type": "string", "title": "工作中心ID"},
            {"name": "work_center_code", "col": "work_center_id", "type": "string", "title": "工作中心编码"},
            {"name": "work_center_name", "col": "work_center_name", "type": "string", "title": "工作中心名称"},
            {"name": "center_type", "col": "work_center_id", "type": "string", "title": "中心类型"},
            {"name": "production_mode", "col": "work_center_id", "type": "string", "title": "生产模式"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "工厂ID"},
            {"name": "plant_name", "col": "plant_name", "type": "string", "title": "工厂名称"},
            {"name": "criticality", "col": "work_center_id", "type": "string", "title": "关键等级"},
        ],
    )
    output.print("OK WorkCenterCube")

    # PlantCube（主体型）
    s.register_cube(
        name="PlantCube",
        table=daily_tbl,
        title="工厂Cube",
        measures=daily_measures,
        dimensions=[
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "工厂ID"},
            {"name": "plant_name", "col": "plant_name", "type": "string", "title": "工厂名称"},
            {"name": "plant_type", "col": "plant_id", "type": "string", "title": "工厂类型"},
            {"name": "region", "col": "plant_id", "type": "string", "title": "区域"},
        ],
    )
    output.print("OK PlantCube")

    # ProductCube（主体型）
    s.register_cube(
        name="ProductCube",
        table=daily_tbl,
        title="产品Cube",
        measures=daily_measures,
        dimensions=[
            {"name": "product_id", "col": "product_id", "type": "string", "title": "产品ID"},
            {"name": "product_code", "col": "product_code", "type": "string", "title": "产品编码"},
            {"name": "product_name", "col": "product_name", "type": "string", "title": "产品名称"},
            {"name": "product_category", "col": "product_category", "type": "string", "title": "产品大类"},
            {"name": "product_subcategory", "col": "product_id", "type": "string", "title": "产品小类"},
            {"name": "product_type", "col": "product_id", "type": "string", "title": "物料类型"},
        ],
    )
    output.print("OK ProductCube")

    # PlanVsActualCube（对比型，基于日实绩表含计划与实际列）
    s.register_cube(
        name="PlanVsActualCube",
        table=daily_tbl,
        title="计划对比Cube",
        measures=[
            {"name": "planned_qty_total", "col": "planned_qty", "agg": "sum", "title": "计划产量合计"},
            {"name": "planned_hours_total", "col": "planned_hours", "agg": "sum", "title": "计划工时合计"},
            {"name": "actual_qty_total", "col": "actual_qty", "agg": "sum", "title": "实际产量合计"},
            {"name": "qualified_qty_total", "col": "qualified_qty", "agg": "sum", "title": "合格产量合计"},
            {"name": "actual_hours_total", "col": "actual_hours", "agg": "sum", "title": "实际工时合计"},
            {"name": "compare_record_count", "col": "daily_id", "agg": "count", "title": "对比行数"},
        ],
        dimensions=[
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "calendar_date", "col": "calendar_date", "type": "date", "title": "统计日期"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "工厂ID"},
            {"name": "work_center_id", "col": "work_center_id", "type": "string", "title": "工作中心ID"},
            {"name": "product_id", "col": "product_id", "type": "string", "title": "产品ID"},
            {"name": "product_category", "col": "product_category", "type": "string", "title": "产品大类"},
            {"name": "work_center_name", "col": "work_center_name", "type": "string", "title": "工作中心名称"},
            {"name": "product_code", "col": "product_code", "type": "string", "title": "产品编码"},
            {"name": "product_name", "col": "product_name", "type": "string", "title": "产品名称"},
        ],
    )
    output.print("OK PlanVsActualCube")

    # 派生度量
    output.print("\n[4b/8] 配置派生度量...")

    s.upsert_derived_measures(
        "ProductionPlanCube",
        [
            {
                "name": "avg_planned_qty_per_line",
                "title": "单行均计划量",
                "expression": "if(ProductionPlanCube.plan_line_count > 0, ProductionPlanCube.planned_qty_total / ProductionPlanCube.plan_line_count, 0)",
                "description": "计划产量 / 计划行数",
            },
        ],
    )
    output.print("OK ProductionPlanCube 派生度量")

    s.upsert_derived_measures(
        "WorkOrderCube",
        [
            {
                "name": "completion_rate",
                "title": "完工率",
                "expression": "if(WorkOrderCube.order_qty_total > 0, WorkOrderCube.completed_qty_total / WorkOrderCube.order_qty_total, 0)",
                "description": "完工数量 / 工单数量",
            },
            {
                "name": "on_time_rate",
                "title": "按期率",
                "expression": "if(WorkOrderCube.work_order_count > 0, WorkOrderCube.on_schedule_count / WorkOrderCube.work_order_count, 0)",
                "description": "按期数 / 工单数",
            },
            {
                "name": "wip_qty",
                "title": "在制量",
                "expression": "WorkOrderCube.order_qty_total - WorkOrderCube.completed_qty_total",
                "description": "工单数量 - 完工数量",
            },
        ],
    )
    output.print("OK WorkOrderCube 派生度量")

    actual_derived = achievement_derived("ProductionActualCube") + [
        {
            "name": "hour_efficiency",
            "title": "工时效率",
            "expression": "if(ProductionActualCube.actual_hours_total > 0, ProductionActualCube.actual_qty_total / ProductionActualCube.actual_hours_total, 0)",
            "description": "实际产量 / 实际工时",
        },
    ]
    s.upsert_derived_measures("ProductionActualCube", actual_derived)
    output.print("OK ProductionActualCube 派生度量")

    s.upsert_derived_measures(
        "MaterialRequirementCube",
        [
            {
                "name": "issue_rate",
                "title": "发料率",
                "expression": "if(MaterialRequirementCube.planned_require_total > 0, MaterialRequirementCube.actual_issue_total / MaterialRequirementCube.planned_require_total, 0)",
                "description": "实际发料 / 计划需求",
            },
            {
                "name": "shortage_qty",
                "title": "缺口量",
                "expression": "if(MaterialRequirementCube.planned_require_total > MaterialRequirementCube.actual_issue_total, MaterialRequirementCube.planned_require_total - MaterialRequirementCube.actual_issue_total, 0)",
                "description": "max(计划需求 - 实际发料, 0)",
            },
        ],
    )
    output.print("OK MaterialRequirementCube 派生度量")

    s.upsert_derived_measures(
        "CapacityLoadCube",
        [
            {
                "name": "planned_load_rate",
                "title": "计划负荷率",
                "expression": "if(CapacityLoadCube.available_hours_total > 0, CapacityLoadCube.planned_load_hours_total / CapacityLoadCube.available_hours_total, 0)",
                "description": "计划负荷 / 可用工时",
            },
            {
                "name": "actual_load_rate",
                "title": "实际负荷率",
                "expression": "if(CapacityLoadCube.available_hours_total > 0, CapacityLoadCube.actual_load_hours_total / CapacityLoadCube.available_hours_total, 0)",
                "description": "实际负荷 / 可用工时",
            },
            {
                "name": "load_variance",
                "title": "负荷偏差",
                "expression": "CapacityLoadCube.actual_load_hours_total - CapacityLoadCube.planned_load_hours_total",
                "description": "实际负荷 - 计划负荷",
            },
        ],
    )
    output.print("OK CapacityLoadCube 派生度量")

    for cube_name in ("WorkCenterCube", "PlantCube", "ProductCube"):
        s.upsert_derived_measures(cube_name, achievement_derived(cube_name))
        output.print(f"OK {cube_name} 派生度量")

    s.upsert_derived_measures(
        "PlanVsActualCube",
        [
            {
                "name": "qty_variance",
                "title": "产量偏差",
                "expression": "PlanVsActualCube.actual_qty_total - PlanVsActualCube.planned_qty_total",
                "description": "实际产量 - 计划产量",
            },
            {
                "name": "achievement_rate",
                "title": "达成率",
                "expression": "if(PlanVsActualCube.planned_qty_total > 0, PlanVsActualCube.actual_qty_total / PlanVsActualCube.planned_qty_total, 0)",
                "description": "实际产量 / 计划产量",
            },
            {
                "name": "hours_variance",
                "title": "工时偏差",
                "expression": "PlanVsActualCube.actual_hours_total - PlanVsActualCube.planned_hours_total",
                "description": "实际工时 - 计划工时",
            },
        ],
    )
    output.print("OK PlanVsActualCube 派生度量")

    # 5. 定义对象类型（11 种，规划 §5.1）
    output.print("\n[5/8] 定义对象类型...")

    s.onto.define_object_type(
        code="Plant",
        name="工厂",
        description="生产工厂/制造基地",
        category_347="主数据",
    )
    s.onto.bind_source("Plant", "dazi_cube", config={"cube": "PlantCube"})
    output.print("OK Plant")

    s.onto.define_object_type(
        code="WorkCenter",
        name="工作中心",
        description="产线、装置工段或工作中心",
        category_347="主数据",
    )
    s.onto.bind_source("WorkCenter", "dazi_cube", config={"cube": "WorkCenterCube"})
    output.print("OK WorkCenter")

    s.onto.define_object_type(
        code="Product",
        name="产品",
        description="成品/半成品/关键物料",
        category_347="主数据",
    )
    s.onto.bind_source("Product", "dazi_cube", config={"cube": "ProductCube"})
    output.print("OK Product")

    s.onto.define_object_type(
        code="PlanVersion",
        name="计划版本",
        description="MPS/周计划/滚动计划版本",
        category_347="参考",
    )
    output.print("OK PlanVersion（无 bind_source）")

    s.onto.define_object_type(
        code="ProductionPlanLine",
        name="生产计划行",
        description="MPS 计划明细行",
        category_347="事务",
    )
    s.onto.bind_source("ProductionPlanLine", "dazi_cube", config={"cube": "ProductionPlanCube"})
    output.print("OK ProductionPlanLine")

    s.onto.define_object_type(
        code="WorkOrder",
        name="生产工单",
        description="由计划分解或手工创建的生产工单",
        category_347="事务",
    )
    s.onto.bind_source("WorkOrder", "dazi_cube", config={"cube": "WorkOrderCube"})
    output.print("OK WorkOrder")

    s.onto.define_object_type(
        code="ProductionDaily",
        name="日生产实绩",
        description="产线×产品×日生产实绩汇总",
        category_347="事务",
    )
    s.onto.bind_source("ProductionDaily", "dazi_cube", config={"cube": "ProductionActualCube"})
    output.print("OK ProductionDaily")

    s.onto.define_object_type(
        code="MaterialRequirement",
        name="物料需求",
        description="组件需求与发料对比",
        category_347="事务",
    )
    s.onto.bind_source("MaterialRequirement", "dazi_cube", config={"cube": "MaterialRequirementCube"})
    output.print("OK MaterialRequirement")

    s.onto.define_object_type(
        code="CapacitySnapshot",
        name="产能负荷快照",
        description="工作中心产能与负荷快照",
        category_347="事务",
    )
    s.onto.bind_source("CapacitySnapshot", "dazi_cube", config={"cube": "CapacityLoadCube"})
    output.print("OK CapacitySnapshot")

    s.onto.define_object_type(
        code="ProductionAnalysis",
        name="生产分析",
        description="多维度生产指标聚合分析",
        category_347="分析",
    )
    s.onto.bind_source("ProductionAnalysis", "dazi_cube", config={"cube": "ProductionActualCube"})
    output.print("OK ProductionAnalysis")

    s.onto.define_object_type(
        code="PlanAnalysis",
        name="计划对比分析",
        description="MPS 计划与日实绩对比分析",
        category_347="分析",
    )
    s.onto.bind_source("PlanAnalysis", "dazi_cube", config={"cube": "PlanVsActualCube"})
    output.print("OK PlanAnalysis")

    # 6. 定义属性（主要对象，规划 §5.2）
    output.print("\n[6/8] 定义对象属性...")

    s.onto.define_property("Plant", "id", "工厂 ID", semantic_role="dimension", qualified_name="PlantCube.plant_id")
    s.onto.define_property("Plant", "name", "工厂名称", semantic_role="dimension", qualified_name="PlantCube.plant_name")
    s.onto.define_property("Plant", "planned_qty", "计划产量", semantic_role="measure", qualified_name="PlantCube.planned_qty_total")
    s.onto.define_property("Plant", "actual_qty", "实际产量", semantic_role="measure", qualified_name="PlantCube.actual_qty_total")
    s.onto.define_property("Plant", "achievement_rate", "计划达成率", semantic_role="measure", qualified_name="PlantCube.achievement_rate")

    s.onto.define_property("WorkCenter", "id", "工作中心 ID", semantic_role="dimension", qualified_name="WorkCenterCube.work_center_id")
    s.onto.define_property("WorkCenter", "code", "工作中心编码", semantic_role="dimension", qualified_name="WorkCenterCube.work_center_code")
    s.onto.define_property("WorkCenter", "name", "工作中心名称", semantic_role="dimension", qualified_name="WorkCenterCube.work_center_name")
    s.onto.define_property("WorkCenter", "planned_qty", "计划产量", semantic_role="measure", qualified_name="WorkCenterCube.planned_qty_total")
    s.onto.define_property("WorkCenter", "actual_qty", "实际产量", semantic_role="measure", qualified_name="WorkCenterCube.actual_qty_total")
    s.onto.define_property("WorkCenter", "achievement_rate", "计划达成率", semantic_role="measure", qualified_name="WorkCenterCube.achievement_rate")

    s.onto.define_property("Product", "id", "产品 ID", semantic_role="dimension", qualified_name="ProductCube.product_id")
    s.onto.define_property("Product", "code", "产品编码", semantic_role="dimension", qualified_name="ProductCube.product_code")
    s.onto.define_property("Product", "name", "产品名称", semantic_role="dimension", qualified_name="ProductCube.product_name")
    s.onto.define_property("Product", "planned_qty", "计划产量", semantic_role="measure", qualified_name="ProductCube.planned_qty_total")
    s.onto.define_property("Product", "actual_qty", "实际产量", semantic_role="measure", qualified_name="ProductCube.actual_qty_total")
    s.onto.define_property("Product", "achievement_rate", "计划达成率", semantic_role="measure", qualified_name="ProductCube.achievement_rate")

    # PlanVersion 无 bind_source，跳过 define_property

    s.onto.define_property("ProductionPlanLine", "id", "计划行 ID", semantic_role="dimension", qualified_name="ProductionPlanCube.plan_line_id")
    s.onto.define_property("ProductionPlanLine", "planned_qty", "计划产量", semantic_role="measure", qualified_name="ProductionPlanCube.planned_qty_total")
    s.onto.define_property("ProductionPlanLine", "planned_hours", "计划工时", semantic_role="measure", qualified_name="ProductionPlanCube.planned_hours_total")
    s.onto.define_property("ProductionPlanLine", "version", "计划版本", semantic_role="dimension", qualified_name="ProductionPlanCube.plan_version_code")

    s.onto.define_property("WorkOrder", "id", "工单 ID", semantic_role="dimension", qualified_name="WorkOrderCube.work_order_id")
    s.onto.define_property("WorkOrder", "order_qty", "工单数量", semantic_role="measure", qualified_name="WorkOrderCube.order_qty_total")
    s.onto.define_property("WorkOrder", "completed_qty", "完工数量", semantic_role="measure", qualified_name="WorkOrderCube.completed_qty_total")
    s.onto.define_property("WorkOrder", "completion_rate", "完工率", semantic_role="measure", qualified_name="WorkOrderCube.completion_rate")
    s.onto.define_property("WorkOrder", "on_time_rate", "按期率", semantic_role="measure", qualified_name="WorkOrderCube.on_time_rate")
    s.onto.define_property("WorkOrder", "status", "工单状态", semantic_role="dimension", qualified_name="WorkOrderCube.status")

    s.onto.define_property("ProductionDaily", "date", "统计日期", semantic_role="dimension", qualified_name="ProductionActualCube.calendar_date")
    s.onto.define_property("ProductionDaily", "planned_qty", "日计划产量", semantic_role="measure", qualified_name="ProductionActualCube.planned_qty_total")
    s.onto.define_property("ProductionDaily", "actual_qty", "实际产量", semantic_role="measure", qualified_name="ProductionActualCube.actual_qty_total")
    s.onto.define_property("ProductionDaily", "achievement_rate", "计划达成率", semantic_role="measure", qualified_name="ProductionActualCube.achievement_rate")
    s.onto.define_property("ProductionDaily", "first_pass_yield", "一次合格率", semantic_role="measure", qualified_name="ProductionActualCube.first_pass_yield")

    s.onto.define_property("MaterialRequirement", "id", "需求行 ID", semantic_role="dimension", qualified_name="MaterialRequirementCube.mrp_line_id")
    s.onto.define_property("MaterialRequirement", "planned_require", "计划需求量", semantic_role="measure", qualified_name="MaterialRequirementCube.planned_require_total")
    s.onto.define_property("MaterialRequirement", "actual_issue", "实际发料量", semantic_role="measure", qualified_name="MaterialRequirementCube.actual_issue_total")
    s.onto.define_property("MaterialRequirement", "issue_rate", "发料率", semantic_role="measure", qualified_name="MaterialRequirementCube.issue_rate")
    s.onto.define_property("MaterialRequirement", "shortage_qty", "缺口量", semantic_role="measure", qualified_name="MaterialRequirementCube.shortage_qty")

    s.onto.define_property("CapacitySnapshot", "id", "负荷 ID", semantic_role="dimension", qualified_name="CapacityLoadCube.load_id")
    s.onto.define_property("CapacitySnapshot", "available_hours", "可用工时", semantic_role="measure", qualified_name="CapacityLoadCube.available_hours_total")
    s.onto.define_property("CapacitySnapshot", "planned_load_rate", "计划负荷率", semantic_role="measure", qualified_name="CapacityLoadCube.planned_load_rate")
    s.onto.define_property("CapacitySnapshot", "actual_load_rate", "实际负荷率", semantic_role="measure", qualified_name="CapacityLoadCube.actual_load_rate")

    s.onto.define_property("ProductionAnalysis", "actual_qty", "实际产量", semantic_role="measure", qualified_name="ProductionActualCube.actual_qty_total")
    s.onto.define_property("ProductionAnalysis", "achievement_rate", "计划达成率", semantic_role="measure", qualified_name="ProductionActualCube.achievement_rate")
    s.onto.define_property("ProductionAnalysis", "first_pass_yield", "一次合格率", semantic_role="measure", qualified_name="ProductionActualCube.first_pass_yield")

    s.onto.define_property("PlanAnalysis", "planned_qty", "计划产量", semantic_role="measure", qualified_name="PlanVsActualCube.planned_qty_total")
    s.onto.define_property("PlanAnalysis", "actual_qty", "实际产量", semantic_role="measure", qualified_name="PlanVsActualCube.actual_qty_total")
    s.onto.define_property("PlanAnalysis", "qty_variance", "产量偏差", semantic_role="measure", qualified_name="PlanVsActualCube.qty_variance")
    s.onto.define_property("PlanAnalysis", "achievement_rate", "达成率", semantic_role="measure", qualified_name="PlanVsActualCube.achievement_rate")

    output.print("OK 属性定义完成")

    # 7. 定义链接类型（17 种，规划 §5.3）
    output.print("\n[7/8] 定义链接类型...")

    s.onto.define_link_type(code="wc_belongs_plant", name="工作中心归属工厂", from_object_type_code="WorkCenter", to_object_type_code="Plant", category_347="归属关系")
    s.onto.define_link_type(code="plan_for_version", name="计划属于版本", from_object_type_code="ProductionPlanLine", to_object_type_code="PlanVersion", category_347="归属关系")
    s.onto.define_link_type(code="plan_on_wc", name="计划排产中心", from_object_type_code="ProductionPlanLine", to_object_type_code="WorkCenter", category_347="归属关系")
    s.onto.define_link_type(code="plan_for_product", name="计划生产产品", from_object_type_code="ProductionPlanLine", to_object_type_code="Product", category_347="归属关系")
    s.onto.define_link_type(code="wo_on_wc", name="工单排产中心", from_object_type_code="WorkOrder", to_object_type_code="WorkCenter", category_347="归属关系")
    s.onto.define_link_type(code="wo_for_product", name="工单生产产品", from_object_type_code="WorkOrder", to_object_type_code="Product", category_347="归属关系")
    s.onto.define_link_type(code="wo_from_plan", name="工单来源计划", from_object_type_code="WorkOrder", to_object_type_code="ProductionPlanLine", category_347="归属关系")
    s.onto.define_link_type(code="daily_on_wc", name="实绩归属中心", from_object_type_code="ProductionDaily", to_object_type_code="WorkCenter", category_347="归属关系")
    s.onto.define_link_type(code="daily_for_product", name="实绩生产产品", from_object_type_code="ProductionDaily", to_object_type_code="Product", category_347="归属关系")
    s.onto.define_link_type(code="mrp_for_wo", name="物料需求对应工单", from_object_type_code="MaterialRequirement", to_object_type_code="WorkOrder", category_347="归属关系")
    s.onto.define_link_type(code="mrp_for_component", name="需求组件物料", from_object_type_code="MaterialRequirement", to_object_type_code="Product", category_347="归属关系")
    s.onto.define_link_type(code="capacity_on_wc", name="负荷归属中心", from_object_type_code="CapacitySnapshot", to_object_type_code="WorkCenter", category_347="归属关系")
    s.onto.define_link_type(code="capacity_for_version", name="负荷对应版本", from_object_type_code="CapacitySnapshot", to_object_type_code="PlanVersion", category_347="归属关系")

    s.onto.define_link_type(code="plan_compared_to_actual", name="计划对比实绩", from_object_type_code="PlanAnalysis", to_object_type_code="ProductionAnalysis", category_347="对比关系")

    s.onto.define_link_type(code="analysis_by_plant", name="分析归因工厂", from_object_type_code="ProductionAnalysis", to_object_type_code="Plant", category_347="分析归因")
    s.onto.define_link_type(code="analysis_by_wc", name="分析归因工作中心", from_object_type_code="ProductionAnalysis", to_object_type_code="WorkCenter", category_347="分析归因")
    s.onto.define_link_type(code="analysis_by_product", name="分析归因产品", from_object_type_code="ProductionAnalysis", to_object_type_code="Product", category_347="分析归因")
    s.onto.define_link_type(code="analysis_by_work_order", name="分析归因工单", from_object_type_code="ProductionAnalysis", to_object_type_code="WorkOrder", category_347="分析归因")

    output.print("OK 链接定义完成")

    # 8. 同步指标引用 + 输出摘要
    output.print("\n[8/8] 同步指标引用...")
    s.sync_metric_refs()
    output.print("OK sync_metric_refs")

    summary = {
        "ok": True,
        "space_id": space_id,
        "tables": len(TABLE_REGISTRY),
        "relationships": len(table_relationships),
        "cubes": 9,
        "objects": 11,
        "links": 18,
    }
    output.success("生产计划本体初始化完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))
