"""化工利润成本本体初始化脚本 — space_cate_test01

初始化内容：
1. 创建物理表（厂区、工艺单元、科目、成本中心、原料、能源类型、GL分录、预算、生产成本、能源消耗）
2. 注册表到空间（含 display_name / description）
3. 注册表间关系（16条）
4. 注册Cube（7个）及派生度量
5. 定义对象类型（12种）、绑定数据源、属性、链接
6. 同步指标引用
7. 平台分类挂载见 profit_category_mount.py（init/seed/函数 publish 之后执行）

放置：项目/DAZI_TEST/本体/ontos/利润成本/setup/profit_ontology_init.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本/setup/profit_ontology_init.py --space space_cate_test01 --type setup
规划对照：项目/DAZI_TEST/本体/ontos/利润成本/plans/化工利润成本分析本体方案.md
"""

import json

# 与规划 §2.x 对齐：display_name=侧栏显示名，description=业务说明
TABLE_REGISTRY = {
    "dim_plant": {
        "display_name": "厂区维表",
        "description": "化工生产厂区或大型装置区主数据",
        "columns": [
            {"name": "plant_id", "display_name": "厂区 ID", "description": "主键"},
            {"name": "plant_code", "display_name": "厂区编码"},
            {"name": "plant_name", "display_name": "厂区名称"},
            {"name": "company_code", "display_name": "公司代码"},
            {"name": "plant_type", "display_name": "装置类型", "description": "炼油/烯烃/芳烃/精细化工"},
            {"name": "location", "display_name": "地理位置"},
            {"name": "design_capacity", "display_name": "设计产能"},
            {"name": "capacity_unit", "display_name": "产能单位"},
            {"name": "status", "display_name": "状态", "description": "运行/检修/停产"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_process_unit": {
        "display_name": "工艺单元维表",
        "description": "装置内工艺单元（蒸馏、反应、压缩等工段）",
        "columns": [
            {"name": "unit_id", "display_name": "单元 ID", "description": "主键"},
            {"name": "unit_code", "display_name": "单元编码"},
            {"name": "unit_name", "display_name": "单元名称"},
            {"name": "plant_id", "display_name": "所属厂区", "description": "关联 dim_plant"},
            {"name": "plant_name", "display_name": "厂区名称", "description": "冗余"},
            {"name": "unit_type", "display_name": "单元类型", "description": "反应/分离/换热/公用工程"},
            {"name": "criticality", "display_name": "关键等级", "description": "A/B/C"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_account": {
        "display_name": "会计科目维表",
        "description": "会计科目主数据",
        "columns": [
            {"name": "account_id", "display_name": "科目 ID", "description": "主键"},
            {"name": "account_code", "display_name": "科目编码"},
            {"name": "account_name", "display_name": "科目名称"},
            {"name": "account_type", "display_name": "科目类型", "description": "资产/负债/权益/收入/成本/费用"},
            {"name": "pl_category", "display_name": "损益大类"},
            {"name": "cost_element", "display_name": "成本要素", "description": "原料/人工/能源/折旧/其他"},
            {"name": "parent_account_id", "display_name": "上级科目"},
            {"name": "account_level", "display_name": "层级"},
            {"name": "is_leaf", "display_name": "末级"},
            {"name": "normal_balance", "display_name": "余额方向", "description": "借/贷"},
            {"name": "status", "display_name": "状态", "description": "启用/停用"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_cost_center": {
        "display_name": "成本中心维表",
        "description": "组织/利润中心主数据",
        "columns": [
            {"name": "cost_center_id", "display_name": "成本中心 ID", "description": "主键"},
            {"name": "cost_center_code", "display_name": "编码"},
            {"name": "cost_center_name", "display_name": "名称"},
            {"name": "department", "display_name": "部门"},
            {"name": "company_code", "display_name": "公司代码"},
            {"name": "profit_center", "display_name": "利润中心"},
            {"name": "plant_id", "display_name": "归属厂区", "description": "关联 dim_plant"},
            {"name": "unit_id", "display_name": "归属单元", "description": "关联 dim_process_unit（可选）"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_material": {
        "display_name": "原料物料维表",
        "description": "化工生产用原料、主辅料、催化剂等",
        "columns": [
            {"name": "material_id", "display_name": "物料 ID", "description": "主键"},
            {"name": "material_code", "display_name": "物料编码"},
            {"name": "material_name", "display_name": "物料名称"},
            {"name": "material_type", "display_name": "物料类型", "description": "原料/辅料/催化剂/添加剂/产品"},
            {"name": "unit_of_measure", "display_name": "计量单位"},
            {"name": "unit_price_standard", "display_name": "标准单价"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_energy_type": {
        "display_name": "能源类型维表",
        "description": "电力、蒸汽、燃料、压缩空气等能源类型",
        "columns": [
            {"name": "energy_type_id", "display_name": "能源类型 ID", "description": "主键"},
            {"name": "energy_type_code", "display_name": "能源编码"},
            {"name": "energy_type_name", "display_name": "能源名称"},
            {"name": "unit_of_measure", "display_name": "计量单位"},
            {"name": "unit_price_standard", "display_name": "标准单价"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_gl_journal_entry": {
        "display_name": "总账实际分录",
        "description": "凭证行粒度损益流水",
        "columns": [
            {"name": "entry_id", "display_name": "凭证 ID"},
            {"name": "line_id", "display_name": "凭证行 ID"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date，YYYYMMDD"},
            {"name": "posting_date", "display_name": "记账日期"},
            {"name": "fiscal_year", "display_name": "会计年度"},
            {"name": "fiscal_period", "display_name": "会计期间"},
            {"name": "account_id", "display_name": "科目 ID", "description": "关联 dim_account"},
            {"name": "account_code", "display_name": "科目编码", "description": "冗余"},
            {"name": "account_name", "display_name": "科目名称", "description": "冗余"},
            {"name": "account_type", "display_name": "科目类型", "description": "冗余"},
            {"name": "pl_category", "display_name": "损益大类", "description": "冗余"},
            {"name": "cost_element", "display_name": "成本要素", "description": "冗余"},
            {"name": "account_level", "display_name": "科目层级", "description": "冗余"},
            {"name": "cost_center_id", "display_name": "成本中心 ID", "description": "关联 dim_cost_center"},
            {"name": "cost_center_name", "display_name": "成本中心", "description": "冗余"},
            {"name": "department", "display_name": "部门", "description": "冗余"},
            {"name": "plant_id", "display_name": "厂区 ID", "description": "冗余（可选）"},
            {"name": "unit_id", "display_name": "单元 ID", "description": "冗余（可选）"},
            {"name": "debit_amount", "display_name": "借方"},
            {"name": "credit_amount", "display_name": "贷方"},
            {"name": "amount_signed", "display_name": "损益金额", "description": "收入为正、成本费用为负"},
            {"name": "currency", "display_name": "币种"},
            {"name": "voucher_no", "display_name": "凭证号"},
            {"name": "source_system", "display_name": "来源系统"},
            {"name": "description", "display_name": "摘要"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_budget_entry": {
        "display_name": "预算明细",
        "description": "预算行粒度编制数据",
        "columns": [
            {"name": "budget_id", "display_name": "预算批次"},
            {"name": "line_id", "display_name": "预算行 ID"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date"},
            {"name": "budget_version", "display_name": "预算版本"},
            {"name": "fiscal_year", "display_name": "预算年度"},
            {"name": "fiscal_period", "display_name": "预算期间", "description": "1-12"},
            {"name": "account_id", "display_name": "科目 ID", "description": "关联 dim_account"},
            {"name": "account_code", "display_name": "科目编码", "description": "冗余"},
            {"name": "account_name", "display_name": "科目名称", "description": "冗余"},
            {"name": "account_type", "display_name": "科目类型", "description": "冗余"},
            {"name": "pl_category", "display_name": "损益大类", "description": "冗余"},
            {"name": "cost_element", "display_name": "成本要素", "description": "冗余"},
            {"name": "cost_center_id", "display_name": "成本中心 ID", "description": "关联 dim_cost_center"},
            {"name": "cost_center_name", "display_name": "成本中心", "description": "冗余"},
            {"name": "department", "display_name": "部门", "description": "冗余"},
            {"name": "plant_id", "display_name": "厂区 ID", "description": "冗余（可选）"},
            {"name": "unit_id", "display_name": "单元 ID", "description": "冗余（可选）"},
            {"name": "budget_amount", "display_name": "预算金额"},
            {"name": "currency", "display_name": "币种"},
            {"name": "status", "display_name": "状态", "description": "草稿/已发布"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_production_cost": {
        "display_name": "生产成本归集",
        "description": "按装置/单元归集的生产成本（化工特色）",
        "columns": [
            {"name": "cost_id", "display_name": "成本归集 ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date"},
            {"name": "fiscal_year", "display_name": "会计年度"},
            {"name": "fiscal_period", "display_name": "会计期间"},
            {"name": "plant_id", "display_name": "厂区 ID", "description": "关联 dim_plant"},
            {"name": "plant_name", "display_name": "厂区名称", "description": "冗余"},
            {"name": "unit_id", "display_name": "单元 ID", "description": "关联 dim_process_unit"},
            {"name": "unit_name", "display_name": "单元名称", "description": "冗余"},
            {"name": "material_id", "display_name": "物料 ID", "description": "关联 dim_material（可选）"},
            {"name": "material_name", "display_name": "物料名称", "description": "冗余"},
            {"name": "energy_type_id", "display_name": "能源类型 ID", "description": "关联 dim_energy_type（可选）"},
            {"name": "energy_type_name", "display_name": "能源名称", "description": "冗余"},
            {"name": "quantity", "display_name": "消耗量"},
            {"name": "unit_price", "display_name": "单价"},
            {"name": "amount", "display_name": "金额"},
            {"name": "cost_element", "display_name": "成本要素", "description": "原料/人工/能源/折旧/其他"},
            {"name": "cost_center_id", "display_name": "成本中心", "description": "关联 dim_cost_center"},
            {"name": "cost_center_name", "display_name": "成本中心名称", "description": "冗余"},
            {"name": "output_qty", "display_name": "产出量"},
            {"name": "output_unit", "display_name": "产出单位"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_energy_consumption": {
        "display_name": "能源消耗明细",
        "description": "各装置/单元的能源消耗明细（化工特色）",
        "columns": [
            {"name": "energy_id", "display_name": "能源消耗 ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date"},
            {"name": "fiscal_year", "display_name": "会计年度"},
            {"name": "fiscal_period", "display_name": "会计期间"},
            {"name": "plant_id", "display_name": "厂区 ID", "description": "关联 dim_plant"},
            {"name": "plant_name", "display_name": "厂区名称", "description": "冗余"},
            {"name": "unit_id", "display_name": "单元 ID", "description": "关联 dim_process_unit"},
            {"name": "unit_name", "display_name": "单元名称", "description": "冗余"},
            {"name": "energy_type_id", "display_name": "能源类型 ID", "description": "关联 dim_energy_type"},
            {"name": "energy_type_name", "display_name": "能源类型名称", "description": "冗余"},
            {"name": "consumption_qty", "display_name": "消耗量"},
            {"name": "consumption_unit", "display_name": "消耗单位"},
            {"name": "unit_price", "display_name": "单价"},
            {"name": "amount", "display_name": "金额"},
            {"name": "cost_center_id", "display_name": "成本中心", "description": "关联 dim_cost_center"},
            {"name": "output_qty", "display_name": "当期产量"},
            {"name": "intensity", "display_name": "能耗强度"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
}


def main():
    space_id = "space_cate_test01"
    s = space.get(space_id)

    output.print("=== 化工利润成本本体初始化 ===")
    output.print(f"空间: {space_id}")

    # 1. 创建物理表
    output.print("\n[1/10] 创建物理表...")

    # dim_plant
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_plant (
            plant_id String,
            plant_code String,
            plant_name String,
            company_code String,
            plant_type String,
            location String,
            design_capacity Float64,
            capacity_unit String,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (plant_code)
    """)
    output.print("OK dim_plant")

    # dim_process_unit
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_process_unit (
            unit_id String,
            unit_code String,
            unit_name String,
            plant_id String,
            plant_name String,
            unit_type String,
            criticality String,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (plant_id, unit_code)
    """)
    output.print("OK dim_process_unit")

    # dim_account
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_account (
            account_id String,
            account_code String,
            account_name String,
            account_type String,
            pl_category String,
            cost_element String,
            parent_account_id String,
            account_level Int32,
            is_leaf Boolean,
            normal_balance String,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (account_code)
    """)
    output.print("OK dim_account")

    # dim_cost_center
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_cost_center (
            cost_center_id String,
            cost_center_code String,
            cost_center_name String,
            department String,
            company_code String,
            profit_center String,
            plant_id String,
            unit_id String,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (cost_center_code)
    """)
    output.print("OK dim_cost_center")

    # dim_material
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_material (
            material_id String,
            material_code String,
            material_name String,
            material_type String,
            unit_of_measure String,
            unit_price_standard Float64,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (material_code)
    """)
    output.print("OK dim_material")

    # dim_energy_type
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_energy_type (
            energy_type_id String,
            energy_type_code String,
            energy_type_name String,
            unit_of_measure String,
            unit_price_standard Float64,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (energy_type_code)
    """)
    output.print("OK dim_energy_type")

    # fact_gl_journal_entry
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_gl_journal_entry (
            entry_id String,
            line_id String,
            date_key Int32,
            posting_date Date,
            fiscal_year Int32,
            fiscal_period Int32,
            account_id String,
            account_code String,
            account_name String,
            account_type String,
            pl_category String,
            cost_element String,
            account_level Int32,
            cost_center_id String,
            cost_center_name String,
            department String,
            plant_id String,
            unit_id String,
            debit_amount Float64,
            credit_amount Float64,
            amount_signed Float64,
            currency String,
            voucher_no String,
            source_system String,
            description String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (date_key, entry_id, line_id)
    """)
    output.print("OK fact_gl_journal_entry")

    # fact_budget_entry
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_budget_entry (
            budget_id String,
            line_id String,
            date_key Int32,
            budget_version String,
            fiscal_year Int32,
            fiscal_period Int32,
            account_id String,
            account_code String,
            account_name String,
            account_type String,
            pl_category String,
            cost_element String,
            cost_center_id String,
            cost_center_name String,
            department String,
            plant_id String,
            unit_id String,
            budget_amount Float64,
            currency String,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (fiscal_year, fiscal_period, account_id, line_id)
    """)
    output.print("OK fact_budget_entry")

    # fact_production_cost
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_production_cost (
            cost_id String,
            date_key Int32,
            fiscal_year Int32,
            fiscal_period Int32,
            plant_id String,
            plant_name String,
            unit_id String,
            unit_name String,
            material_id String,
            material_name String,
            energy_type_id String,
            energy_type_name String,
            quantity Float64,
            unit_price Float64,
            amount Float64,
            cost_element String,
            cost_center_id String,
            cost_center_name String,
            output_qty Float64,
            output_unit String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (date_key, plant_id, unit_id, cost_element)
    """)
    output.print("OK fact_production_cost")

    # fact_energy_consumption
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_energy_consumption (
            energy_id String,
            date_key Int32,
            fiscal_year Int32,
            fiscal_period Int32,
            plant_id String,
            plant_name String,
            unit_id String,
            unit_name String,
            energy_type_id String,
            energy_type_name String,
            consumption_qty Float64,
            consumption_unit String,
            unit_price Float64,
            amount Float64,
            cost_center_id String,
            output_qty Float64,
            intensity Float64,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (date_key, plant_id, unit_id, energy_type_id)
    """)
    output.print("OK fact_energy_consumption")

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

    # 3. 注册表间关系（16条）
    output.print("\n[3/10] 注册表间关系（16条）...")

    table_relationships = [
        # 时间关联（4条）
        {
            "from_table": "fact_gl_journal_entry",
            "to_table": "dim_date",
            "join_sql": "fact_gl_journal_entry.date_key = dim_date.date_key",
            "join_keys": [{"from": "date_key", "to": "date_key"}],
            "relationship_type": "many_to_one",
            "description": "分录关联日历",
        },
        {
            "from_table": "fact_budget_entry",
            "to_table": "dim_date",
            "join_sql": "fact_budget_entry.date_key = dim_date.date_key",
            "join_keys": [{"from": "date_key", "to": "date_key"}],
            "relationship_type": "many_to_one",
            "description": "预算关联日历",
        },
        {
            "from_table": "fact_production_cost",
            "to_table": "dim_date",
            "join_sql": "fact_production_cost.date_key = dim_date.date_key",
            "join_keys": [{"from": "date_key", "to": "date_key"}],
            "relationship_type": "many_to_one",
            "description": "成本归集关联日历",
        },
        {
            "from_table": "fact_energy_consumption",
            "to_table": "dim_date",
            "join_sql": "fact_energy_consumption.date_key = dim_date.date_key",
            "join_keys": [{"from": "date_key", "to": "date_key"}],
            "relationship_type": "many_to_one",
            "description": "能源消耗关联日历",
        },
        # 主数据关联（12条）
        {
            "from_table": "dim_process_unit",
            "to_table": "dim_plant",
            "join_sql": "dim_process_unit.plant_id = dim_plant.plant_id",
            "join_keys": [{"from": "plant_id", "to": "plant_id"}],
            "relationship_type": "many_to_one",
            "description": "单元归属厂区",
        },
        {
            "from_table": "dim_cost_center",
            "to_table": "dim_process_unit",
            "join_sql": "dim_cost_center.unit_id = dim_process_unit.unit_id",
            "join_keys": [{"from": "unit_id", "to": "unit_id"}],
            "relationship_type": "many_to_one",
            "description": "成本中心归属单元（可选）",
        },
        {
            "from_table": "fact_gl_journal_entry",
            "to_table": "dim_account",
            "join_sql": "fact_gl_journal_entry.account_id = dim_account.account_id",
            "join_keys": [{"from": "account_id", "to": "account_id"}],
            "relationship_type": "many_to_one",
            "description": "分录归属科目",
        },
        {
            "from_table": "fact_gl_journal_entry",
            "to_table": "dim_cost_center",
            "join_sql": "fact_gl_journal_entry.cost_center_id = dim_cost_center.cost_center_id",
            "join_keys": [{"from": "cost_center_id", "to": "cost_center_id"}],
            "relationship_type": "many_to_one",
            "description": "分录归属成本中心",
        },
        {
            "from_table": "fact_budget_entry",
            "to_table": "dim_account",
            "join_sql": "fact_budget_entry.account_id = dim_account.account_id",
            "join_keys": [{"from": "account_id", "to": "account_id"}],
            "relationship_type": "many_to_one",
            "description": "预算归属科目",
        },
        {
            "from_table": "fact_budget_entry",
            "to_table": "dim_cost_center",
            "join_sql": "fact_budget_entry.cost_center_id = dim_cost_center.cost_center_id",
            "join_keys": [{"from": "cost_center_id", "to": "cost_center_id"}],
            "relationship_type": "many_to_one",
            "description": "预算归属成本中心",
        },
        {
            "from_table": "fact_production_cost",
            "to_table": "dim_plant",
            "join_sql": "fact_production_cost.plant_id = dim_plant.plant_id",
            "join_keys": [{"from": "plant_id", "to": "plant_id"}],
            "relationship_type": "many_to_one",
            "description": "成本归属厂区",
        },
        {
            "from_table": "fact_production_cost",
            "to_table": "dim_process_unit",
            "join_sql": "fact_production_cost.unit_id = dim_process_unit.unit_id",
            "join_keys": [{"from": "unit_id", "to": "unit_id"}],
            "relationship_type": "many_to_one",
            "description": "成本归属单元",
        },
        {
            "from_table": "fact_production_cost",
            "to_table": "dim_material",
            "join_sql": "fact_production_cost.material_id = dim_material.material_id",
            "join_keys": [{"from": "material_id", "to": "material_id"}],
            "relationship_type": "many_to_one",
            "description": "成本关联物料",
        },
        {
            "from_table": "fact_production_cost",
            "to_table": "dim_energy_type",
            "join_sql": "fact_production_cost.energy_type_id = dim_energy_type.energy_type_id",
            "join_keys": [{"from": "energy_type_id", "to": "energy_type_id"}],
            "relationship_type": "many_to_one",
            "description": "成本关联能源类型",
        },
        {
            "from_table": "fact_energy_consumption",
            "to_table": "dim_plant",
            "join_sql": "fact_energy_consumption.plant_id = dim_plant.plant_id",
            "join_keys": [{"from": "plant_id", "to": "plant_id"}],
            "relationship_type": "many_to_one",
            "description": "能源消耗归属厂区",
        },
        {
            "from_table": "fact_energy_consumption",
            "to_table": "dim_process_unit",
            "join_sql": "fact_energy_consumption.unit_id = dim_process_unit.unit_id",
            "join_keys": [{"from": "unit_id", "to": "unit_id"}],
            "relationship_type": "many_to_one",
            "description": "能源消耗归属单元",
        },
    ]
    for rel in table_relationships:
        rid = s.tables.add_relationship(**rel)
        output.print(f"OK {rel['from_table']} -> {rel['to_table']}")

    # 4. 注册 Cube（7个）
    output.print("\n[4/10] 注册 Cube（7个）...")

    gl_table = "fact_gl_journal_entry"
    budget_table = "fact_budget_entry"
    cost_table = "fact_production_cost"
    energy_table = "fact_energy_consumption"

    # ActualCube
    s.register_cube(
        name="ActualCube",
        table=gl_table,
        title="GL实际分录主Cube",
        measures=[
            {"name": "debit_total", "col": "debit_amount", "agg": "sum", "title": "借方合计"},
            {"name": "credit_total", "col": "credit_amount", "agg": "sum", "title": "贷方合计"},
            {"name": "amount_signed_total", "col": "amount_signed", "agg": "sum", "title": "损益金额合计"},
            {"name": "line_count", "col": "line_id", "agg": "count", "title": "分录行数"},
        ],
        dimensions=[
            {"name": "entry_id", "col": "entry_id", "type": "string", "title": "凭证ID"},
            {"name": "line_id", "col": "line_id", "type": "string", "title": "行ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "posting_date", "col": "posting_date", "type": "date", "title": "记账日期"},
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "会计年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "会计期间"},
            {"name": "account_id", "col": "account_id", "type": "string", "title": "科目ID"},
            {"name": "account_code", "col": "account_code", "type": "string", "title": "科目编码"},
            {"name": "account_name", "col": "account_name", "type": "string", "title": "科目名称"},
            {"name": "account_type", "col": "account_type", "type": "string", "title": "科目类型"},
            {"name": "pl_category", "col": "pl_category", "type": "string", "title": "损益大类"},
            {"name": "cost_element", "col": "cost_element", "type": "string", "title": "成本要素"},
            {"name": "cost_center_id", "col": "cost_center_id", "type": "string", "title": "成本中心ID"},
            {"name": "cost_center_name", "col": "cost_center_name", "type": "string", "title": "成本中心"},
            {"name": "department", "col": "department", "type": "string", "title": "部门"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "厂区ID"},
            {"name": "unit_id", "col": "unit_id", "type": "string", "title": "单元ID"},
        ],
    )
    output.print("OK ActualCube")

    # BudgetCube
    s.register_cube(
        name="BudgetCube",
        table=budget_table,
        title="预算Cube",
        measures=[
            {"name": "budget_amount_total", "col": "budget_amount", "agg": "sum", "title": "预算金额合计"},
            {"name": "line_count", "col": "line_id", "agg": "count", "title": "预算行数"},
        ],
        dimensions=[
            {"name": "budget_id", "col": "budget_id", "type": "string", "title": "预算批次ID"},
            {"name": "line_id", "col": "line_id", "type": "string", "title": "预算行ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "budget_version", "col": "budget_version", "type": "string", "title": "预算版本"},
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "预算年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "预算期间"},
            {"name": "account_id", "col": "account_id", "type": "string", "title": "科目ID"},
            {"name": "account_code", "col": "account_code", "type": "string", "title": "科目编码"},
            {"name": "account_name", "col": "account_name", "type": "string", "title": "科目名称"},
            {"name": "account_type", "col": "account_type", "type": "string", "title": "科目类型"},
            {"name": "pl_category", "col": "pl_category", "type": "string", "title": "损益大类"},
            {"name": "cost_element", "col": "cost_element", "type": "string", "title": "成本要素"},
            {"name": "cost_center_id", "col": "cost_center_id", "type": "string", "title": "成本中心ID"},
            {"name": "cost_center_name", "col": "cost_center_name", "type": "string", "title": "成本中心"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "厂区ID"},
            {"name": "unit_id", "col": "unit_id", "type": "string", "title": "单元ID"},
        ],
    )
    output.print("OK BudgetCube")

    # ProfitStatementCube
    s.register_cube(
        name="ProfitStatementCube",
        table=gl_table,
        title="利润表Cube",
        measures=[
            {"name": "revenue", "col": "amount_signed", "agg": "sum", "title": "收入"},
            {"name": "total_cost", "col": "amount_signed", "agg": "sum", "title": "成本费用"},
            {"name": "line_count", "col": "line_id", "agg": "count", "title": "分录行数"},
        ],
        dimensions=[
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "会计年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "会计期间"},
            {"name": "account_id", "col": "account_id", "type": "string", "title": "科目ID"},
            {"name": "account_code", "col": "account_code", "type": "string", "title": "科目编码"},
            {"name": "account_name", "col": "account_name", "type": "string", "title": "科目名称"},
            {"name": "account_type", "col": "account_type", "type": "string", "title": "科目类型"},
            {"name": "pl_category", "col": "pl_category", "type": "string", "title": "损益大类"},
            {"name": "cost_element", "col": "cost_element", "type": "string", "title": "成本要素"},
            {"name": "cost_center_id", "col": "cost_center_id", "type": "string", "title": "成本中心ID"},
            {"name": "cost_center_name", "col": "cost_center_name", "type": "string", "title": "成本中心"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "厂区ID"},
            {"name": "plant_name", "col": "plant_name", "type": "string", "title": "厂区名称"},
        ],
    )
    output.print("OK ProfitStatementCube")

    # ProductionCostCube
    s.register_cube(
        name="ProductionCostCube",
        table=cost_table,
        title="生产成本Cube（化工特色）",
        measures=[
            {"name": "quantity_total", "col": "quantity", "agg": "sum", "title": "消耗量合计"},
            {"name": "amount_total", "col": "amount", "agg": "sum", "title": "金额合计"},
            {"name": "output_qty_total", "col": "output_qty", "agg": "sum", "title": "产出量合计"},
        ],
        dimensions=[
            {"name": "cost_id", "col": "cost_id", "type": "string", "title": "成本归集ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "会计年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "会计期间"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "厂区ID"},
            {"name": "plant_name", "col": "plant_name", "type": "string", "title": "厂区名称"},
            {"name": "unit_id", "col": "unit_id", "type": "string", "title": "单元ID"},
            {"name": "unit_name", "col": "unit_name", "type": "string", "title": "单元名称"},
            {"name": "material_id", "col": "material_id", "type": "string", "title": "物料ID"},
            {"name": "material_name", "col": "material_name", "type": "string", "title": "物料名称"},
            {"name": "energy_type_id", "col": "energy_type_id", "type": "string", "title": "能源类型ID"},
            {"name": "energy_type_name", "col": "energy_type_name", "type": "string", "title": "能源名称"},
            {"name": "cost_element", "col": "cost_element", "type": "string", "title": "成本要素"},
            {"name": "cost_center_id", "col": "cost_center_id", "type": "string", "title": "成本中心ID"},
            {"name": "cost_center_name", "col": "cost_center_name", "type": "string", "title": "成本中心名称"},
            {"name": "output_unit", "col": "output_unit", "type": "string", "title": "产出单位"},
        ],
    )
    output.print("OK ProductionCostCube")

    # EnergyCube
    s.register_cube(
        name="EnergyCube",
        table=energy_table,
        title="能源消耗Cube（化工特色）",
        measures=[
            {"name": "consumption_qty_total", "col": "consumption_qty", "agg": "sum", "title": "消耗量合计"},
            {"name": "amount_total", "col": "amount", "agg": "sum", "title": "金额合计"},
        ],
        dimensions=[
            {"name": "energy_id", "col": "energy_id", "type": "string", "title": "能源消耗ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "会计年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "会计期间"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "厂区ID"},
            {"name": "plant_name", "col": "plant_name", "type": "string", "title": "厂区名称"},
            {"name": "unit_id", "col": "unit_id", "type": "string", "title": "单元ID"},
            {"name": "unit_name", "col": "unit_name", "type": "string", "title": "单元名称"},
            {"name": "energy_type_id", "col": "energy_type_id", "type": "string", "title": "能源类型ID"},
            {"name": "energy_type_name", "col": "energy_type_name", "type": "string", "title": "能源类型名称"},
            {"name": "cost_center_id", "col": "cost_center_id", "type": "string", "title": "成本中心"},
        ],
    )
    output.print("OK EnergyCube")

    # BudgetVsActualCube
    s.register_cube(
        name="BudgetVsActualCube",
        table=budget_table,
        title="预算执行Cube",
        measures=[
            {"name": "budget_amount", "col": "budget_amount", "agg": "sum", "title": "预算金额"},
        ],
        dimensions=[
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "预算年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "预算期间"},
            {"name": "account_id", "col": "account_id", "type": "string", "title": "科目ID"},
            {"name": "account_code", "col": "account_code", "type": "string", "title": "科目编码"},
            {"name": "account_name", "col": "account_name", "type": "string", "title": "科目名称"},
            {"name": "pl_category", "col": "pl_category", "type": "string", "title": "损益大类"},
            {"name": "cost_element", "col": "cost_element", "type": "string", "title": "成本要素"},
            {"name": "cost_center_id", "col": "cost_center_id", "type": "string", "title": "成本中心ID"},
            {"name": "cost_center_name", "col": "cost_center_name", "type": "string", "title": "成本中心"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "厂区ID"},
            {"name": "plant_name", "col": "plant_name", "type": "string", "title": "厂区名称"},
            {"name": "unit_id", "col": "unit_id", "type": "string", "title": "单元ID"},
            {"name": "unit_name", "col": "unit_name", "type": "string", "title": "单元名称"},
            {"name": "budget_version", "col": "budget_version", "type": "string", "title": "预算版本"},
        ],
    )
    output.print("OK BudgetVsActualCube")

    # MaterialPriceCube
    s.register_cube(
        name="MaterialPriceCube",
        table=cost_table,
        title="原料价格Cube",
        measures=[
            {"name": "quantity_total", "col": "quantity", "agg": "sum", "title": "采购/消耗量"},
            {"name": "amount_total", "col": "amount", "agg": "sum", "title": "采购/消耗金额"},
        ],
        dimensions=[
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "会计年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "会计期间"},
            {"name": "material_id", "col": "material_id", "type": "string", "title": "物料ID"},
            {"name": "material_name", "col": "material_name", "type": "string", "title": "物料名称"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "厂区ID"},
            {"name": "plant_name", "col": "plant_name", "type": "string", "title": "厂区名称"},
            {"name": "unit_id", "col": "unit_id", "type": "string", "title": "单元ID"},
            {"name": "unit_name", "col": "unit_name", "type": "string", "title": "单元名称"},
        ],
    )
    output.print("OK MaterialPriceCube")

    # 5. 派生度量
    output.print("\n[5/10] 配置派生度量...")

    # ActualCube 派生度量
    s.upsert_derived_measures("ActualCube", [
        {
            "name": "revenue",
            "title": "收入",
            "expression": "sumIf(amount_signed, account_type='收入')",
            "description": "收入类科目发生额",
        },
        {
            "name": "total_cost",
            "title": "成本费用",
            "expression": "sumIf(amount_signed, account_type in ('成本','费用'))",
            "description": "成本费用类科目发生额（负值）",
        },
        {
            "name": "gross_profit",
            "title": "毛利润",
            "expression": "ActualCube.revenue + ActualCube.total_cost",
            "description": "收入+成本费用",
        },
        {
            "name": "profit_margin",
            "title": "毛利率",
            "expression": "if(ActualCube.revenue > 0, ActualCube.gross_profit / abs(ActualCube.revenue), 0)",
            "description": "毛利润/收入",
        },
    ])
    output.print("OK ActualCube 派生度量 (4)")

    # ProfitStatementCube 派生度量
    s.upsert_derived_measures("ProfitStatementCube", [
        {
            "name": "revenue",
            "title": "收入",
            "expression": "sumIf(amount_signed, account_type='收入')",
            "description": "收入合计",
        },
        {
            "name": "total_cost",
            "title": "成本费用",
            "expression": "sumIf(amount_signed, account_type in ('成本','费用'))",
            "description": "成本费用合计",
        },
        {
            "name": "gross_profit",
            "title": "毛利润",
            "expression": "ProfitStatementCube.revenue + ProfitStatementCube.total_cost",
            "description": "毛利润",
        },
        {
            "name": "profit_margin",
            "title": "毛利率",
            "expression": "if(ProfitStatementCube.revenue > 0, ProfitStatementCube.gross_profit / abs(ProfitStatementCube.revenue), 0)",
            "description": "毛利率",
        },
    ])
    output.print("OK ProfitStatementCube 派生度量 (4)")

    # ProductionCostCube 派生度量
    s.upsert_derived_measures("ProductionCostCube", [
        {
            "name": "material_cost",
            "title": "原料成本",
            "expression": "sumIf(amount, cost_element='原料')",
            "description": "原料成本",
        },
        {
            "name": "energy_cost",
            "title": "能源成本",
            "expression": "sumIf(amount, cost_element='能源')",
            "description": "能源成本",
        },
        {
            "name": "labor_cost",
            "title": "人工成本",
            "expression": "sumIf(amount, cost_element='人工')",
            "description": "人工成本",
        },
        {
            "name": "overhead_cost",
            "title": "制造费用",
            "expression": "sumIf(amount, cost_element='折旧') + sumIf(amount, cost_element='其他')",
            "description": "折旧+其他",
        },
        {
            "name": "unit_cost",
            "title": "单位成本",
            "expression": "if(ProductionCostCube.output_qty_total > 0, ProductionCostCube.amount_total / ProductionCostCube.output_qty_total, 0)",
            "description": "单位成本",
        },
        {
            "name": "material_cost_ratio",
            "title": "原料成本占比",
            "expression": "if(ProductionCostCube.amount_total > 0, ProductionCostCube.material_cost / ProductionCostCube.amount_total, 0)",
            "description": "原料占比",
        },
        {
            "name": "energy_cost_ratio",
            "title": "能源成本占比",
            "expression": "if(ProductionCostCube.amount_total > 0, ProductionCostCube.energy_cost / ProductionCostCube.amount_total, 0)",
            "description": "能源占比",
        },
    ])
    output.print("OK ProductionCostCube 派生度量 (7)")

    # EnergyCube 派生度量
    s.upsert_derived_measures("EnergyCube", [
        {
            "name": "avg_price",
            "title": "平均单价",
            "expression": "if(EnergyCube.consumption_qty_total > 0, EnergyCube.amount_total / EnergyCube.consumption_qty_total, 0)",
            "description": "能源平均单价",
        },
    ])
    output.print("OK EnergyCube 派生度量 (1)")

    # 6. 对象类型（12种）
    output.print("\n[6/10] 定义对象类型（12种）...")

    object_types = [
        ("Plant", "厂区/装置区", "化工生产厂区或大型装置区主数据"),
        ("ProcessUnit", "工艺单元", "装置内工艺单元（蒸馏、反应、压缩等工段）"),
        ("Account", "会计科目", "会计科目主数据"),
        ("CostCenter", "成本中心", "组织/利润中心主数据"),
        ("Material", "原料/物料", "化工生产用原料、主辅料、催化剂等"),
        ("EnergyType", "能源类型", "电力、蒸汽、燃料等能源类型"),
        ("ProfitStatement", "利润表分录", "凭证行粒度损益流水"),
        ("BudgetLine", "预算行", "预算编制明细业务对象"),
        ("ProductionCost", "生产成本归集", "按装置/单元归集的生产成本（化工特色）"),
        ("EnergyConsumption", "能源消耗", "各装置/单元的能源消耗明细（化工特色）"),
        ("CostAnalysis", "成本分析", "多维度成本指标聚合对象"),
        ("BudgetAnalysis", "预算分析", "预算执行与差异分析对象"),
    ]
    for code, name, desc in object_types:
        s.onto.define_object_type(code, name, description=desc)
        output.print(f"OK {code}")

    # 7. 绑定数据源
    output.print("\n[7/10] 绑定数据源...")

    bindings = [
        ("Plant", "ProfitStatementCube"),
        ("ProcessUnit", "ProductionCostCube"),
        ("Account", "ActualCube"),
        ("CostCenter", "ActualCube"),
        ("Material", "ProductionCostCube"),
        ("EnergyType", "EnergyCube"),
        ("ProfitStatement", "ActualCube"),
        ("BudgetLine", "BudgetCube"),
        ("ProductionCost", "ProductionCostCube"),
        ("EnergyConsumption", "EnergyCube"),
        ("CostAnalysis", "ProfitStatementCube"),
        ("BudgetAnalysis", "BudgetVsActualCube"),
    ]
    for obj, cube in bindings:
        s.onto.bind_source(obj, "dazi_cube", config={"cube": cube})
        output.print(f"OK {obj} -> {cube}")

    # 8. 属性
    output.print("\n[8/10] 定义属性...")

    def define_props(obj_code, props):
        for code, name, role, qn in props:
            s.onto.define_property(obj_code, code, name, semantic_role=role, qualified_name=qn)

    # Plant 属性
    define_props("Plant", [
        ("id", "厂区ID", "dimension", "ProfitStatementCube.plant_id"),
        ("name", "厂区名称", "dimension", "ProfitStatementCube.plant_name"),
        ("revenue", "收入", "measure", "ProfitStatementCube.revenue"),
        ("total_cost", "成本费用", "measure", "ProfitStatementCube.total_cost"),
        ("gross_profit", "毛利润", "measure", "ProfitStatementCube.gross_profit"),
    ])
    output.print("OK Plant 属性 (5)")

    # ProcessUnit 属性
    define_props("ProcessUnit", [
        ("id", "单元ID", "dimension", "ProductionCostCube.unit_id"),
        ("name", "单元名称", "dimension", "ProductionCostCube.unit_name"),
        ("amount_total", "成本金额", "measure", "ProductionCostCube.amount_total"),
        ("output_qty", "产出量", "measure", "ProductionCostCube.output_qty_total"),
        ("unit_cost", "单位成本", "measure", "ProductionCostCube.unit_cost"),
    ])
    output.print("OK ProcessUnit 属性 (5)")

    # Account 属性
    define_props("Account", [
        ("id", "科目ID", "dimension", "ActualCube.account_id"),
        ("code", "科目编码", "dimension", "ActualCube.account_code"),
        ("name", "科目名称", "dimension", "ActualCube.account_name"),
        ("type", "科目类型", "dimension", "ActualCube.account_type"),
        ("pl_category", "损益大类", "dimension", "ActualCube.pl_category"),
        ("cost_element", "成本要素", "dimension", "ActualCube.cost_element"),
        ("revenue", "收入", "measure", "ActualCube.revenue"),
        ("total_cost", "成本费用", "measure", "ActualCube.total_cost"),
        ("gross_profit", "毛利润", "measure", "ActualCube.gross_profit"),
    ])
    output.print("OK Account 属性 (9)")

    # CostCenter 属性
    define_props("CostCenter", [
        ("id", "成本中心ID", "dimension", "ActualCube.cost_center_id"),
        ("name", "成本中心", "dimension", "ActualCube.cost_center_name"),
        ("department", "部门", "dimension", "ActualCube.department"),
        ("revenue", "收入", "measure", "ActualCube.revenue"),
        ("total_cost", "成本费用", "measure", "ActualCube.total_cost"),
        ("gross_profit", "毛利润", "measure", "ActualCube.gross_profit"),
    ])
    output.print("OK CostCenter 属性 (6)")

    # Material 属性
    define_props("Material", [
        ("id", "物料ID", "dimension", "ProductionCostCube.material_id"),
        ("name", "物料名称", "dimension", "ProductionCostCube.material_name"),
        ("quantity_total", "消耗量", "measure", "ProductionCostCube.quantity_total"),
        ("amount_total", "金额", "measure", "ProductionCostCube.amount_total"),
        ("material_cost", "原料成本", "measure", "ProductionCostCube.material_cost"),
    ])
    output.print("OK Material 属性 (5)")

    # EnergyType 属性
    define_props("EnergyType", [
        ("id", "能源类型ID", "dimension", "EnergyCube.energy_type_id"),
        ("name", "能源名称", "dimension", "EnergyCube.energy_type_name"),
        ("consumption_qty_total", "消耗量", "measure", "EnergyCube.consumption_qty_total"),
        ("amount_total", "金额", "measure", "EnergyCube.amount_total"),
        ("avg_price", "平均单价", "measure", "EnergyCube.avg_price"),
    ])
    output.print("OK EnergyType 属性 (5)")

    # ProfitStatement 属性
    define_props("ProfitStatement", [
        ("id", "行ID", "dimension", "ActualCube.line_id"),
        ("posting_date", "记账日期", "dimension", "ActualCube.posting_date"),
        ("fiscal_period", "会计期间", "dimension", "ActualCube.fiscal_period"),
        ("account_name", "科目名称", "dimension", "ActualCube.account_name"),
        ("cost_center_name", "成本中心", "dimension", "ActualCube.cost_center_name"),
        ("amount_signed", "损益金额", "measure", "ActualCube.amount_signed_total"),
        ("revenue", "收入", "measure", "ActualCube.revenue"),
        ("total_cost", "成本费用", "measure", "ActualCube.total_cost"),
    ])
    output.print("OK ProfitStatement 属性 (8)")

    # BudgetLine 属性
    define_props("BudgetLine", [
        ("id", "预算行ID", "dimension", "BudgetCube.line_id"),
        ("version", "预算版本", "dimension", "BudgetCube.budget_version"),
        ("fiscal_period", "预算期间", "dimension", "BudgetCube.fiscal_period"),
        ("account_name", "科目名称", "dimension", "BudgetCube.account_name"),
        ("cost_center_name", "成本中心", "dimension", "BudgetCube.cost_center_name"),
        ("budget_amount_total", "预算金额", "measure", "BudgetCube.budget_amount_total"),
    ])
    output.print("OK BudgetLine 属性 (6)")

    # ProductionCost 属性
    define_props("ProductionCost", [
        ("id", "成本ID", "dimension", "ProductionCostCube.cost_id"),
        ("plant_name", "厂区", "dimension", "ProductionCostCube.plant_name"),
        ("unit_name", "单元", "dimension", "ProductionCostCube.unit_name"),
        ("material_name", "物料", "dimension", "ProductionCostCube.material_name"),
        ("energy_type_name", "能源类型", "dimension", "ProductionCostCube.energy_type_name"),
        ("cost_element", "成本要素", "dimension", "ProductionCostCube.cost_element"),
        ("quantity_total", "消耗量", "measure", "ProductionCostCube.quantity_total"),
        ("amount_total", "金额", "measure", "ProductionCostCube.amount_total"),
        ("output_qty", "产出量", "measure", "ProductionCostCube.output_qty_total"),
        ("unit_cost", "单位成本", "measure", "ProductionCostCube.unit_cost"),
    ])
    output.print("OK ProductionCost 属性 (10)")

    # EnergyConsumption 属性
    define_props("EnergyConsumption", [
        ("id", "能源消耗ID", "dimension", "EnergyCube.energy_id"),
        ("plant_name", "厂区", "dimension", "EnergyCube.plant_name"),
        ("unit_name", "单元", "dimension", "EnergyCube.unit_name"),
        ("energy_type_name", "能源类型", "dimension", "EnergyCube.energy_type_name"),
        ("consumption_qty_total", "消耗量", "measure", "EnergyCube.consumption_qty_total"),
        ("amount_total", "金额", "measure", "EnergyCube.amount_total"),
        ("avg_price", "平均单价", "measure", "EnergyCube.avg_price"),
    ])
    output.print("OK EnergyConsumption 属性 (7)")

    # CostAnalysis 属性
    define_props("CostAnalysis", [
        ("fiscal_period", "会计期间", "dimension", "ProfitStatementCube.fiscal_period"),
        ("pl_category", "损益大类", "dimension", "ProfitStatementCube.pl_category"),
        ("cost_element", "成本要素", "dimension", "ProfitStatementCube.cost_element"),
        ("plant_name", "厂区", "dimension", "ProfitStatementCube.plant_name"),
        ("cost_center_name", "成本中心", "dimension", "ProfitStatementCube.cost_center_name"),
        ("revenue", "收入", "measure", "ProfitStatementCube.revenue"),
        ("total_cost", "成本费用", "measure", "ProfitStatementCube.total_cost"),
        ("gross_profit", "毛利润", "measure", "ProfitStatementCube.gross_profit"),
        ("profit_margin", "毛利率", "measure", "ProfitStatementCube.profit_margin"),
    ])
    output.print("OK CostAnalysis 属性 (9)")

    # BudgetAnalysis 属性
    define_props("BudgetAnalysis", [
        ("fiscal_period", "预算期间", "dimension", "BudgetVsActualCube.fiscal_period"),
        ("pl_category", "损益大类", "dimension", "BudgetVsActualCube.pl_category"),
        ("cost_element", "成本要素", "dimension", "BudgetVsActualCube.cost_element"),
        ("cost_center_name", "成本中心", "dimension", "BudgetVsActualCube.cost_center_name"),
        ("plant_name", "厂区", "dimension", "BudgetVsActualCube.plant_name"),
        ("unit_name", "单元", "dimension", "BudgetVsActualCube.unit_name"),
        ("budget_version", "预算版本", "dimension", "BudgetVsActualCube.budget_version"),
        ("budget_amount", "预算金额", "measure", "BudgetVsActualCube.budget_amount"),
    ])
    output.print("OK BudgetAnalysis 属性 (8)")

    # 9. 链接类型（18种）
    output.print("\n[9/10] 定义链接类型（18种）...")

    link_types = [
        ("unit_belongs_plant", "单元归属厂区", "ProcessUnit", "Plant", "组织层级"),
        ("statement_belongs_account", "分录归属科目", "ProfitStatement", "Account", ""),
        ("statement_belongs_cc", "分录归属成本中心", "ProfitStatement", "CostCenter", ""),
        ("budget_belongs_account", "预算归属科目", "BudgetLine", "Account", ""),
        ("budget_belongs_cc", "预算归属成本中心", "BudgetLine", "CostCenter", ""),
        ("production_belongs_plant", "成本归属厂区", "ProductionCost", "Plant", ""),
        ("production_belongs_unit", "成本归属单元", "ProductionCost", "ProcessUnit", ""),
        ("production_belongs_material", "成本关联物料", "ProductionCost", "Material", ""),
        ("production_belongs_energy", "成本关联能源", "ProductionCost", "EnergyType", ""),
        ("energy_belongs_plant", "能源归属厂区", "EnergyConsumption", "Plant", ""),
        ("energy_belongs_unit", "能源归属单元", "EnergyConsumption", "ProcessUnit", ""),
        ("energy_belongs_type", "能源关联类型", "EnergyConsumption", "EnergyType", ""),
        ("analysis_by_account", "分析归因科目", "CostAnalysis", "Account", ""),
        ("analysis_by_cc", "分析归因成本中心", "CostAnalysis", "CostCenter", ""),
        ("analysis_by_plant", "分析归因厂区", "CostAnalysis", "Plant", ""),
        ("analysis_by_unit", "分析归因单元", "CostAnalysis", "ProcessUnit", ""),
        ("analysis_by_material", "分析归因物料", "CostAnalysis", "Material", ""),
        ("analysis_by_energy", "分析归因能源", "CostAnalysis", "EnergyType", ""),
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

    # 10. 同步指标引用
    output.print("\n[10/10] 同步指标引用...")
    s.sync_metric_refs()
    output.print("OK sync_metric_refs")

    summary = {
        "ok": True,
        "space_id": space_id,
        "tables": 10,
        "table_relationships": 16,
        "cubes": 7,
        "object_types": 12,
        "properties": 91,
        "link_types": 18,
    }

    output.print("\n=== 化工利润成本本体初始化完成 ===")
    output.success("初始化成功")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))
