"""利润分析01 本体初始化 — space__onto_engine_test

增量建设：复用引擎测试 dim/fact 表，新建损益科目、桥接、利润预算、项目利润快照。
规划对照：plans/利润分析01本体规划方案.md

实施顺序：init → seed → 发布全部函数 → profit01_category_mount.py
"""

import json

SPACE_ID = "space__onto_engine_test"

TABLE_REGISTRY = {
    "dim_account": {
        "display_name": "损益科目维表",
        "description": "会计损益科目主数据（收入/成本/费用）",
        "columns": [
            {"name": "account_id", "display_name": "科目 ID", "description": "主键"},
            {"name": "account_code", "display_name": "科目编码"},
            {"name": "account_name", "display_name": "科目名称"},
            {"name": "account_type", "display_name": "科目类型", "description": "收入/成本/费用"},
            {"name": "pl_category", "display_name": "损益大类"},
            {"name": "parent_account_id", "display_name": "上级科目", "description": "自关联"},
            {"name": "account_level", "display_name": "层级"},
            {"name": "is_leaf", "display_name": "末级"},
            {"name": "normal_balance", "display_name": "余额方向", "description": "借/贷"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "bridge_cost_type_account": {
        "display_name": "成本科目映射表",
        "description": "作业成本科目 → 损益科目桥接",
        "columns": [
            {"name": "cost_type_id", "display_name": "成本科目 ID", "description": "FK dim_cost_type"},
            {"name": "account_id", "display_name": "损益科目 ID", "description": "FK dim_account"},
            {"name": "mapping_type", "display_name": "映射类型"},
            {"name": "effective_from", "display_name": "生效日"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_pl_budget": {
        "display_name": "利润预算明细",
        "description": "项目×损益科目×期间预算编制",
        "columns": [
            {"name": "budget_id", "display_name": "预算批次"},
            {"name": "line_id", "display_name": "预算行 ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date"},
            {"name": "fiscal_year", "display_name": "预算年度"},
            {"name": "fiscal_period", "display_name": "预算期间", "description": "1-12"},
            {"name": "budget_version", "display_name": "预算版本"},
            {"name": "project_id", "display_name": "项目 ID"},
            {"name": "project_name", "display_name": "项目名称", "description": "冗余"},
            {"name": "org_id", "display_name": "组织 ID"},
            {"name": "org_name", "display_name": "组织名称", "description": "冗余"},
            {"name": "region", "display_name": "片区", "description": "冗余"},
            {"name": "account_id", "display_name": "损益科目 ID"},
            {"name": "account_code", "display_name": "科目编码", "description": "冗余"},
            {"name": "account_name", "display_name": "科目名称", "description": "冗余"},
            {"name": "account_type", "display_name": "科目类型", "description": "冗余"},
            {"name": "pl_category", "display_name": "损益大类", "description": "冗余"},
            {"name": "budget_amount", "display_name": "预算金额"},
            {"name": "actual_amount", "display_name": "实际金额", "description": "seed 灌入，供预实 Cube"},
            {"name": "currency", "display_name": "币种"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_project_profit": {
        "display_name": "项目利润快照",
        "description": "项目×月营收/成本/毛利物化表（§4.5 ProjectProfitCube 读模型）",
        "columns": [
            {"name": "profit_id", "display_name": "快照 ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date"},
            {"name": "year", "display_name": "公历年"},
            {"name": "month", "display_name": "月"},
            {"name": "year_month", "display_name": "年月"},
            {"name": "fiscal_year", "display_name": "会计年度"},
            {"name": "fiscal_period", "display_name": "会计期间"},
            {"name": "project_id", "display_name": "项目 ID"},
            {"name": "project_name", "display_name": "项目名称", "description": "冗余"},
            {"name": "region", "display_name": "片区", "description": "冗余"},
            {"name": "org_id", "display_name": "组织 ID"},
            {"name": "org_name", "display_name": "组织名称", "description": "冗余"},
            {"name": "revenue", "display_name": "营收"},
            {"name": "cost", "display_name": "成本"},
            {"name": "gross_profit", "display_name": "毛利"},
            {"name": "profit_margin", "display_name": "利润率"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
}


def _link_extra(keys):
    return {"join_spec": {"join_keys": keys}}


def main():
    s = space.get(SPACE_ID)
    output.print("=== 利润分析01 本体初始化 ===")
    output.print(f"空间: {SPACE_ID}")

    # 1. 建表（仅本域新建；引擎测试表 ensure 存在即可）
    output.print("\n[1/8] 创建物理表...")
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_account (
            account_id String, account_code String, account_name String,
            account_type String, pl_category String, parent_account_id String,
            account_level Int32, is_leaf UInt8, normal_balance String,
            status String, created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree() ORDER BY (account_code)
    """)
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS bridge_cost_type_account (
            cost_type_id String, account_id String, mapping_type String,
            effective_from Date, created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree() ORDER BY (cost_type_id, account_id)
    """)
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_pl_budget (
            budget_id String, line_id String, date_key Int32,
            fiscal_year Int32, fiscal_period Int32, budget_version String,
            project_id String, project_name String, org_id String, org_name String,
            region String, account_id String, account_code String, account_name String,
            account_type String, pl_category String, budget_amount Float64,
            actual_amount Float64, currency String, status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (fiscal_year, fiscal_period, project_id, account_id, line_id)
    """)
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_project_profit (
            profit_id String, date_key Int32, year Int16, month Int8, year_month String,
            fiscal_year Int32, fiscal_period Int32,
            project_id String, project_name String, region String,
            org_id String, org_name String,
            revenue Float64, cost Float64, gross_profit Float64, profit_margin Float64,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id)
    """)
    output.print("OK 4 张新表")

    # 2. 注册表元数据
    output.print("\n[2/8] 注册表到空间...")
    for tbl, meta in TABLE_REGISTRY.items():
        s.tables.register_with_meta(
            table_name=tbl,
            display_name=meta["display_name"],
            description=meta.get("description"),
            columns=meta["columns"],
            force_column_meta=True,
        )
    output.print(f"OK {len(TABLE_REGISTRY)} 张表")

    # 3. 表间关系（本域 7 条 + 项目利润快照 4 条）
    output.print("\n[3/8] 注册表间关系...")
    table_relationships = [
        {"from_table": "fact_pl_budget", "to_table": "dim_date",
         "join_sql": "fact_pl_budget.date_key = dim_date.date_key",
         "join_keys": [{"from": "date_key", "to": "date_key"}],
         "relationship_type": "many_to_one", "description": "预算→日历"},
        {"from_table": "fact_pl_budget", "to_table": "dim_project",
         "join_sql": "fact_pl_budget.project_id = dim_project.project_id",
         "join_keys": [{"from": "project_id", "to": "project_id"}],
         "relationship_type": "many_to_one", "description": "预算→项目"},
        {"from_table": "fact_pl_budget", "to_table": "dim_org",
         "join_sql": "fact_pl_budget.org_id = dim_org.org_id",
         "join_keys": [{"from": "org_id", "to": "org_id"}],
         "relationship_type": "many_to_one", "description": "预算→组织"},
        {"from_table": "fact_pl_budget", "to_table": "dim_account",
         "join_sql": "fact_pl_budget.account_id = dim_account.account_id",
         "join_keys": [{"from": "account_id", "to": "account_id"}],
         "relationship_type": "many_to_one", "description": "预算→损益科目"},
        {"from_table": "bridge_cost_type_account", "to_table": "dim_cost_type",
         "join_sql": "bridge_cost_type_account.cost_type_id = dim_cost_type.cost_type_id",
         "join_keys": [{"from": "cost_type_id", "to": "cost_type_id"}],
         "relationship_type": "many_to_one", "description": "映射→成本科目"},
        {"from_table": "bridge_cost_type_account", "to_table": "dim_account",
         "join_sql": "bridge_cost_type_account.account_id = dim_account.account_id",
         "join_keys": [{"from": "account_id", "to": "account_id"}],
         "relationship_type": "many_to_one", "description": "映射→损益科目"},
        {"from_table": "dim_account", "to_table": "dim_account",
         "join_sql": "dim_account.parent_account_id = dim_account.account_id",
         "join_keys": [{"from": "parent_account_id", "to": "account_id"}],
         "relationship_type": "many_to_one", "description": "科目树"},
        {"from_table": "fact_project_profit", "to_table": "dim_date",
         "join_sql": "fact_project_profit.date_key = dim_date.date_key",
         "join_keys": [{"from": "date_key", "to": "date_key"}],
         "relationship_type": "many_to_one", "description": "利润快照→日历"},
        {"from_table": "fact_project_profit", "to_table": "dim_project",
         "join_sql": "fact_project_profit.project_id = dim_project.project_id",
         "join_keys": [{"from": "project_id", "to": "project_id"}],
         "relationship_type": "many_to_one", "description": "利润快照→项目"},
        {"from_table": "fact_project_profit", "to_table": "dim_org",
         "join_sql": "fact_project_profit.org_id = dim_org.org_id",
         "join_keys": [{"from": "org_id", "to": "org_id"}],
         "relationship_type": "many_to_one", "description": "利润快照→组织"},
    ]
    for rel in table_relationships:
        s.tables.add_relationship(**rel)
    output.print(f"OK {len(table_relationships)} 条关系")

    # 4. Cube（ensure OutputCube/CostCube + 注册本域 Cube）
    output.print("\n[4/8] 注册 Cube...")
    s.register_cube(
        name="OutputCube", table="fact_output", title="营收分析Cube",
        measures=[
            {"name": "revenue_total", "col": "output_amount", "agg": "sum", "title": "营收合计"},
            {"name": "output_count", "col": "output_id", "agg": "count", "title": "产值行数"},
        ],
        dimensions=[
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
            {"name": "region", "col": "region", "type": "string", "title": "片区"},
            {"name": "org_id", "col": "org_id", "type": "string", "title": "组织ID"},
        ],
    )
    cost_dims = [
        {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
        {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
        {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
        {"name": "region", "col": "region", "type": "string", "title": "片区"},
        {"name": "org_id", "col": "org_id", "type": "string", "title": "组织ID"},
        {"name": "org_name", "col": "org_name", "type": "string", "title": "组织名称"},
        {"name": "cost_type_id", "col": "cost_type_id", "type": "string", "title": "成本科目ID"},
        {"name": "cost_type_name", "col": "cost_type_name", "type": "string", "title": "成本科目名称"},
        {"name": "parent_cost_type_id", "col": "parent_cost_type_id", "type": "string", "title": "上级科目ID"},
    ]
    s.register_cube(
        name="CostCube", table="fact_cost", title="成本分析Cube",
        measures=[
            {"name": "cost_total", "col": "cost_amount", "agg": "sum", "title": "成本合计"},
            {"name": "cost_budget_total", "col": "budget_amount", "agg": "sum", "title": "预算合计"},
            {"name": "cost_count", "col": "cost_id", "agg": "count", "title": "成本行数"},
        ],
        dimensions=cost_dims,
    )
    s.register_cube(
        name="AccountCostCube", table="fact_cost", title="损益科目成本Cube",
        measures=[
            {"name": "cost_total", "col": "cost_amount", "agg": "sum", "title": "成本合计"},
            {"name": "cost_count", "col": "cost_id", "agg": "count", "title": "成本行数"},
        ],
        dimensions=cost_dims,
    )
    s.register_cube(
        name="BudgetPlCube", table="fact_pl_budget", title="利润预算Cube",
        measures=[
            {"name": "budget_amount", "col": "budget_amount", "agg": "sum", "title": "预算金额"},
            {"name": "actual_amount", "col": "actual_amount", "agg": "sum", "title": "实际金额"},
            {"name": "budget_lines", "col": "line_id", "agg": "count", "title": "预算行数"},
        ],
        dimensions=[
            {"name": "budget_version", "col": "budget_version", "type": "string", "title": "预算版本"},
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "预算年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "预算期间"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "org_id", "col": "org_id", "type": "string", "title": "组织ID"},
            {"name": "region", "col": "region", "type": "string", "title": "片区"},
            {"name": "account_id", "col": "account_id", "type": "string", "title": "科目ID"},
            {"name": "account_code", "col": "account_code", "type": "string", "title": "科目编码"},
            {"name": "account_name", "col": "account_name", "type": "string", "title": "科目名称"},
            {"name": "account_type", "col": "account_type", "type": "string", "title": "科目类型"},
            {"name": "pl_category", "col": "pl_category", "type": "string", "title": "损益大类"},
        ],
    )
    profit_dims = [
        {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
        {"name": "year", "col": "year", "type": "int", "title": "年"},
        {"name": "month", "col": "month", "type": "int", "title": "月"},
        {"name": "year_month", "col": "year_month", "type": "string", "title": "年月"},
        {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "会计年度"},
        {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "会计期间"},
        {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
        {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
        {"name": "region", "col": "region", "type": "string", "title": "片区"},
        {"name": "org_id", "col": "org_id", "type": "string", "title": "组织ID"},
        {"name": "org_name", "col": "org_name", "type": "string", "title": "组织名称"},
    ]
    s.register_cube(
        name="ProjectProfitCube", table="fact_project_profit", title="项目利润Cube",
        measures=[
            {"name": "revenue", "col": "revenue", "agg": "sum", "title": "营收"},
            {"name": "cost", "col": "cost", "agg": "sum", "title": "成本"},
            {"name": "gross_profit", "col": "gross_profit", "agg": "sum", "title": "毛利"},
            {"name": "profit_margin", "col": "profit_margin", "agg": "avg", "title": "利润率"},
            {"name": "profit_rows", "col": "profit_id", "agg": "count", "title": "快照行数"},
        ],
        dimensions=profit_dims,
    )
    s.register_cube(
        name="BudgetVsActualCube", table="fact_pl_budget", title="预实对比Cube",
        measures=[
            {"name": "budget_amount", "col": "budget_amount", "agg": "sum", "title": "预算金额"},
            {"name": "actual_amount", "col": "actual_amount", "agg": "sum", "title": "实际金额"},
            {"name": "budget_lines", "col": "line_id", "agg": "count", "title": "预算行数"},
        ],
        dimensions=[
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "预算年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "预算期间"},
            {"name": "budget_version", "col": "budget_version", "type": "string", "title": "预算版本"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "org_id", "col": "org_id", "type": "string", "title": "组织ID"},
            {"name": "account_id", "col": "account_id", "type": "string", "title": "科目ID"},
            {"name": "pl_category", "col": "pl_category", "type": "string", "title": "损益大类"},
        ],
    )
    output.print("OK 6 个 Cube")

    # 5. 派生度量
    output.print("\n[5/8] 配置派生度量...")
    s.upsert_derived_measures("OutputCube", [
        {"name": "avg_revenue", "title": "平均营收",
         "expression": "if(OutputCube.output_count > 0, OutputCube.revenue_total / OutputCube.output_count, 0)",
         "description": "营收/行数"},
    ])
    s.upsert_derived_measures("CostCube", [
        {"name": "cost_budget_variance", "title": "预算偏差",
         "expression": "CostCube.cost_total - CostCube.cost_budget_total",
         "description": "成本-预算"},
        {"name": "cost_exec_rate", "title": "预算执行率",
         "expression": "if(CostCube.cost_budget_total > 0, CostCube.cost_total / CostCube.cost_budget_total, 0)",
         "description": "成本/预算"},
    ])
    s.upsert_derived_measures("BudgetPlCube", [
        {"name": "budget_revenue", "title": "营收预算",
         "expression": "sum(if(account_type='收入', budget_amount, 0))",
         "description": "收入类预算"},
        {"name": "budget_cost", "title": "成本预算",
         "expression": "sum(if(account_type='成本', budget_amount, 0))",
         "description": "成本类预算"},
        {"name": "budget_expense", "title": "费用预算",
         "expression": "sum(if(account_type='费用', budget_amount, 0))",
         "description": "费用类预算"},
    ])
    s.upsert_derived_measures("BudgetVsActualCube", [
        {"name": "variance", "title": "差异",
         "expression": "BudgetVsActualCube.actual_amount - BudgetVsActualCube.budget_amount",
         "description": "实际-预算"},
        {"name": "execution_rate", "title": "执行率",
         "expression": "if(BudgetVsActualCube.budget_amount > 0, BudgetVsActualCube.actual_amount / BudgetVsActualCube.budget_amount, 0)",
         "description": "实际/预算"},
    ])
    output.print("OK 派生度量")

    # 6. 对象类型（增量；与引擎测试共存）
    output.print("\n[6/8] 定义对象类型...")
    objects = [
        ("Account", "损益科目", "会计损益科目主数据", "主数据", "BudgetPlCube"),
        ("RevenueRecord", "营收记录", "项目产值/营收流水", "事务", "OutputCube"),
        ("BudgetLine", "预算行", "利润预算编制行", "事务", "BudgetPlCube"),
        ("ProfitAnalysis", "利润分析", "项目利润指标聚合", "分析", "ProjectProfitCube"),
        ("BudgetAnalysis", "预算分析", "预算执行与预实对比", "分析", "BudgetVsActualCube"),
    ]
    for code, name, desc, cat, cube in objects:
        s.onto.define_object_type(code=code, name=name, description=desc, category_347=cat)
        if cube:
            s.onto.bind_source(code, "dazi_cube", config={"cube": cube})
    # 增量属性：Project 利润读模型
    s.onto.define_object_type(code="Project", name="项目", description="工程项目主数据", category_347="主数据")
    s.onto.bind_source("Project", "dazi_cube", config={"cube": "ProjectProfitCube"})
    output.print(f"OK {len(objects) + 1} 个对象（含 Project 重绑）")

    # 7. 属性
    output.print("\n[7/8] 定义对象属性...")
    s.onto.define_property("Account", "id", "科目ID", semantic_role="dimension",
                           qualified_name="BudgetPlCube.account_id")
    s.onto.define_property("Account", "code", "科目编码", semantic_role="dimension",
                           qualified_name="BudgetPlCube.account_code")
    s.onto.define_property("Account", "name", "科目名称", semantic_role="dimension",
                           qualified_name="BudgetPlCube.account_name")
    s.onto.define_property("Account", "type", "科目类型", semantic_role="dimension",
                           qualified_name="BudgetPlCube.account_type")
    s.onto.define_property("Account", "pl_category", "损益大类", semantic_role="dimension",
                           qualified_name="BudgetPlCube.pl_category")
    s.onto.define_property("Account", "budget_amount", "预算金额", semantic_role="measure",
                           qualified_name="BudgetPlCube.budget_amount")
    s.onto.define_property("Account", "actual_amount", "实际金额", semantic_role="measure",
                           qualified_name="BudgetPlCube.actual_amount")

    s.onto.define_property("RevenueRecord", "date", "日期", semantic_role="dimension",
                           qualified_name="OutputCube.date_key")
    s.onto.define_property("RevenueRecord", "revenue", "营收", semantic_role="measure",
                           qualified_name="OutputCube.revenue_total")
    s.onto.define_property("RevenueRecord", "project", "项目", semantic_role="dimension",
                           qualified_name="OutputCube.project_name")

    s.onto.define_property("BudgetLine", "version", "预算版本", semantic_role="dimension",
                           qualified_name="BudgetPlCube.budget_version")
    s.onto.define_property("BudgetLine", "period", "预算期间", semantic_role="dimension",
                           qualified_name="BudgetPlCube.fiscal_period")
    s.onto.define_property("BudgetLine", "budget_amount", "预算金额", semantic_role="measure",
                           qualified_name="BudgetPlCube.budget_amount")

    s.onto.define_property("ProfitAnalysis", "revenue", "营收", semantic_role="measure",
                           qualified_name="ProjectProfitCube.revenue")
    s.onto.define_property("ProfitAnalysis", "cost", "成本", semantic_role="measure",
                           qualified_name="ProjectProfitCube.cost")
    s.onto.define_property("ProfitAnalysis", "gross_profit", "毛利", semantic_role="measure",
                           qualified_name="ProjectProfitCube.gross_profit")
    s.onto.define_property("ProfitAnalysis", "profit_margin", "利润率", semantic_role="measure",
                           qualified_name="ProjectProfitCube.profit_margin")
    s.onto.define_property("ProfitAnalysis", "period", "期间", semantic_role="dimension",
                           qualified_name="ProjectProfitCube.year_month")

    s.onto.define_property("Project", "revenue", "营收", semantic_role="measure",
                           qualified_name="ProjectProfitCube.revenue")
    s.onto.define_property("Project", "cost", "成本", semantic_role="measure",
                           qualified_name="ProjectProfitCube.cost")
    s.onto.define_property("Project", "gross_profit", "毛利", semantic_role="measure",
                           qualified_name="ProjectProfitCube.gross_profit")
    s.onto.define_property("Project", "profit_margin", "利润率", semantic_role="measure",
                           qualified_name="ProjectProfitCube.profit_margin")

    s.onto.define_property("BudgetAnalysis", "budget_amount", "预算", semantic_role="measure",
                           qualified_name="BudgetVsActualCube.budget_amount")
    s.onto.define_property("BudgetAnalysis", "actual_amount", "实际", semantic_role="measure",
                           qualified_name="BudgetVsActualCube.actual_amount")
    s.onto.define_property("BudgetAnalysis", "variance", "差异", semantic_role="measure",
                           qualified_name="BudgetVsActualCube.variance")
    s.onto.define_property("BudgetAnalysis", "execution_rate", "执行率", semantic_role="measure",
                           qualified_name="BudgetVsActualCube.execution_rate")
    output.print("OK 属性定义")

    # 8. 链接
    output.print("\n[8/8] 定义链接类型...")
    link_defs = [
        ("cost_maps_account", "成本映射损益科目", "CostType", "Account", "归属关系",
         "many_to_one", _link_extra([{"from": "cost_type_id", "to": "id"}])),
        ("revenue_belongs_project", "营收归属项目", "RevenueRecord", "Project", "归属关系",
         "many_to_one", _link_extra([{"from": "project_id", "to": "id"}])),
        ("budget_for_account", "预算对应科目", "BudgetLine", "Account", "归属关系",
         "many_to_one", _link_extra([{"from": "account_id", "to": "id"}])),
        ("budget_for_project", "预算对应项目", "BudgetLine", "Project", "归属关系",
         "many_to_one", _link_extra([{"from": "project_id", "to": "id"}])),
        ("account_has_parent", "科目上级", "Account", "Account", "层级关系",
         "many_to_one", _link_extra([{"from": "parent_account_id", "to": "id"}])),
        ("profit_analysis_by_project", "利润归因项目", "ProfitAnalysis", "Project", "分析归因",
         "many_to_one", _link_extra([{"from": "project_id", "to": "id"}])),
        ("profit_analysis_by_account", "利润归因科目", "ProfitAnalysis", "Account", "分析归因",
         "many_to_one", _link_extra([{"from": "account_id", "to": "id"}])),
        ("budget_compared_to_actual", "预算对比实际", "BudgetAnalysis", "ProfitAnalysis", "对比关系",
         "many_to_one", {}),
    ]
    for code, name, fr, to, cat, card, extra in link_defs:
        s.onto.define_link_type(
            code=code, name=name,
            from_object_type_code=fr, to_object_type_code=to,
            category_347=cat, cardinality=card, extra=extra,
        )
    output.print(f"OK {len(link_defs)} 条链接")

    s.sync_metric_refs()
    s.onto.engine.invalidate()
    output.print("OK sync_metric_refs")

    summary = {
        "ok": True,
        "space_id": SPACE_ID,
        "tables_new": len(TABLE_REGISTRY),
        "relationships": len(table_relationships),
        "cubes": 6,
        "objects": len(objects) + 1,
        "links": len(link_defs),
    }
    output.success("利润分析01 本体初始化完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True))
