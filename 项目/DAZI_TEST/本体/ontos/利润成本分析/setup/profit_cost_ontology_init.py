"""利润成本分析本体初始化脚本 — space_cate_test01

初始化内容：
1. 创建物理表（科目、利润项、成本项、成本中心、实际分录、预算）
2. 注册表到空间（含 display_name / description）
3. 注册表间关系（11条）
4. 注册Cube（7个）及派生度量
5. 定义对象类型（8种）、绑定数据源、属性、链接
6. 同步指标引用
7. 平台分类挂载见 profit_cost_category_mount.py（init/seed/函数 publish 之后执行）

放置：项目/DAZI_TEST/本体/ontos/利润成本分析/setup/profit_cost_ontology_init.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本分析/setup/profit_cost_ontology_init.py --space space_cate_test01 --type setup
规划对照：项目/DAZI_TEST/本体/ontos/利润成本分析/plans/利润成本分析本体方案.md
"""

import json

# 与规划文档 2.x 对齐：display_name=侧栏显示名，description=业务说明
TABLE_REGISTRY = {
    "dim_account": {
        "display_name": "科目维表",
        "description": "会计科目主数据",
        "columns": [
            {"name": "account_id", "display_name": "科目 ID", "description": "主键"},
            {"name": "account_code", "display_name": "科目编码"},
            {"name": "account_name", "display_name": "科目名称"},
            {"name": "account_type", "display_name": "科目类型", "description": "资产/负债/权益/收入/成本/费用"},
            {"name": "pl_category", "display_name": "损益大类"},
            {"name": "profit_item_id", "display_name": "利润项 ID", "description": "关联 dim_profit_item"},
            {"name": "cost_item_id", "display_name": "成本项 ID", "description": "关联 dim_cost_item"},
            {"name": "parent_account_id", "display_name": "上级科目"},
            {"name": "account_level", "display_name": "层级"},
            {"name": "is_leaf", "display_name": "末级"},
            {"name": "normal_balance", "display_name": "余额方向", "description": "借/贷"},
            {"name": "status", "display_name": "状态", "description": "启用/停用"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_profit_item": {
        "display_name": "利润项维表",
        "description": "利润项主数据",
        "columns": [
            {"name": "profit_item_id", "display_name": "利润项 ID", "description": "主键"},
            {"name": "profit_item_code", "display_name": "利润项编码"},
            {"name": "profit_item_name", "display_name": "利润项名称"},
            {"name": "profit_item_type", "display_name": "利润项类型", "description": "主营/其他/营业外"},
            {"name": "parent_profit_item_id", "display_name": "上级利润项"},
            {"name": "profit_item_level", "display_name": "层级"},
            {"name": "is_leaf", "display_name": "末级"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_cost_item": {
        "display_name": "成本项维表",
        "description": "成本项主数据",
        "columns": [
            {"name": "cost_item_id", "display_name": "成本项 ID", "description": "主键"},
            {"name": "cost_item_code", "display_name": "成本项编码"},
            {"name": "cost_item_name", "display_name": "成本项名称"},
            {"name": "cost_item_type", "display_name": "成本项类型", "description": "直接/间接/期间费用"},
            {"name": "cost_category", "display_name": "成本大类", "description": "生产成本/期间费用/其他"},
            {"name": "parent_cost_item_id", "display_name": "上级成本项"},
            {"name": "cost_item_level", "display_name": "层级"},
            {"name": "is_leaf", "display_name": "末级"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_cost_center": {
        "display_name": "成本中心维表",
        "description": "成本中心/部门主数据",
        "columns": [
            {"name": "cost_center_id", "display_name": "成本中心 ID", "description": "主键"},
            {"name": "cost_center_code", "display_name": "编码"},
            {"name": "cost_center_name", "display_name": "名称"},
            {"name": "department", "display_name": "部门"},
            {"name": "company_code", "display_name": "公司代码"},
            {"name": "profit_center", "display_name": "利润中心"},
            {"name": "cost_center_type", "display_name": "类型", "description": "生产/销售/管理/研发"},
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
            {"name": "profit_item_id", "display_name": "利润项 ID", "description": "冗余"},
            {"name": "profit_item_name", "display_name": "利润项名称", "description": "冗余"},
            {"name": "cost_item_id", "display_name": "成本项 ID", "description": "冗余"},
            {"name": "cost_item_name", "display_name": "成本项名称", "description": "冗余"},
            {"name": "cost_center_id", "display_name": "成本中心 ID", "description": "关联 dim_cost_center"},
            {"name": "cost_center_name", "display_name": "成本中心", "description": "冗余"},
            {"name": "department", "display_name": "部门", "description": "冗余"},
            {"name": "debit_amount", "display_name": "借方"},
            {"name": "credit_amount", "display_name": "贷方"},
            {"name": "amount_signed", "display_name": "损益金额", "description": "收入为正、成本费用为负"},
            {"name": "currency", "display_name": "币种"},
            {"name": "voucher_no", "display_name": "凭证号"},
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
            {"name": "pl_category", "display_name": "损益大类", "description": "冗余"},
            {"name": "profit_item_id", "display_name": "利润项 ID", "description": "冗余"},
            {"name": "profit_item_name", "display_name": "利润项名称", "description": "冗余"},
            {"name": "cost_item_id", "display_name": "成本项 ID", "description": "冗余"},
            {"name": "cost_item_name", "display_name": "成本项名称", "description": "冗余"},
            {"name": "cost_center_id", "display_name": "成本中心 ID", "description": "关联 dim_cost_center"},
            {"name": "cost_center_name", "display_name": "成本中心", "description": "冗余"},
            {"name": "department", "display_name": "部门", "description": "冗余"},
            {"name": "budget_amount", "display_name": "预算金额"},
            {"name": "currency", "display_name": "币种"},
            {"name": "status", "display_name": "状态", "description": "草稿/已发布"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
}


def main():
    space_id = "space_cate_test01"
    s = space.get(space_id)

    output.print("=== 利润成本分析本体初始化 ===")
    output.print(f"空间: {space_id}")

    # 1. 创建物理表
    output.print("\n[1/9] 创建物理表...")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_account (
            account_id String,
            account_code String,
            account_name String,
            account_type String,
            pl_category String,
            profit_item_id String,
            cost_item_id String,
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

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_profit_item (
            profit_item_id String,
            profit_item_code String,
            profit_item_name String,
            profit_item_type String,
            parent_profit_item_id String,
            profit_item_level Int32,
            is_leaf Boolean,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (profit_item_code)
    """)
    output.print("OK dim_profit_item")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_cost_item (
            cost_item_id String,
            cost_item_code String,
            cost_item_name String,
            cost_item_type String,
            cost_category String,
            parent_cost_item_id String,
            cost_item_level Int32,
            is_leaf Boolean,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (cost_item_code)
    """)
    output.print("OK dim_cost_item")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_cost_center (
            cost_center_id String,
            cost_center_code String,
            cost_center_name String,
            department String,
            company_code String,
            profit_center String,
            cost_center_type String,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (cost_center_id)
    """)
    output.print("OK dim_cost_center")

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
            profit_item_id String,
            profit_item_name String,
            cost_item_id String,
            cost_item_name String,
            cost_center_id String,
            cost_center_name String,
            department String,
            debit_amount Float64,
            credit_amount Float64,
            amount_signed Float64,
            currency String,
            voucher_no String,
            description String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (date_key, entry_id, line_id)
    """)
    output.print("OK fact_gl_journal_entry")

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
            pl_category String,
            profit_item_id String,
            profit_item_name String,
            cost_item_id String,
            cost_item_name String,
            cost_center_id String,
            cost_center_name String,
            department String,
            budget_amount Float64,
            currency String,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (fiscal_year, fiscal_period, account_id, line_id)
    """)
    output.print("OK fact_budget_entry")

    # 2. 注册表（含 display_name / description）
    output.print("\n[2/9] 注册表到空间...")

    for tbl_name, meta in TABLE_REGISTRY.items():
        s.tables.register_with_meta(
            table_name=tbl_name,
            display_name=meta["display_name"],
            description=meta.get("description"),
            columns=meta["columns"],
            force_column_meta=True,
        )
        output.print(f"OK {tbl_name} ({meta['display_name']})")

    # 3. 注册表间关系
    output.print("\n[3/9] 注册表间关系...")

    table_relationships = [
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
            "from_table": "fact_gl_journal_entry",
            "to_table": "dim_account",
            "join_sql": "fact_gl_journal_entry.account_id = dim_account.account_id",
            "join_keys": [{"from": "account_id", "to": "account_id"}],
            "relationship_type": "many_to_one",
            "description": "实际分录关联会计科目",
        },
        {
            "from_table": "fact_gl_journal_entry",
            "to_table": "dim_profit_item",
            "join_sql": "fact_gl_journal_entry.profit_item_id = dim_profit_item.profit_item_id",
            "join_keys": [{"from": "profit_item_id", "to": "profit_item_id"}],
            "relationship_type": "many_to_one",
            "description": "实际分录关联利润项",
        },
        {
            "from_table": "fact_gl_journal_entry",
            "to_table": "dim_cost_item",
            "join_sql": "fact_gl_journal_entry.cost_item_id = dim_cost_item.cost_item_id",
            "join_keys": [{"from": "cost_item_id", "to": "cost_item_id"}],
            "relationship_type": "many_to_one",
            "description": "实际分录关联成本项",
        },
        {
            "from_table": "fact_gl_journal_entry",
            "to_table": "dim_cost_center",
            "join_sql": "fact_gl_journal_entry.cost_center_id = dim_cost_center.cost_center_id",
            "join_keys": [{"from": "cost_center_id", "to": "cost_center_id"}],
            "relationship_type": "many_to_one",
            "description": "实际分录关联成本中心",
        },
        {
            "from_table": "fact_budget_entry",
            "to_table": "dim_account",
            "join_sql": "fact_budget_entry.account_id = dim_account.account_id",
            "join_keys": [{"from": "account_id", "to": "account_id"}],
            "relationship_type": "many_to_one",
            "description": "预算关联会计科目",
        },
        {
            "from_table": "fact_budget_entry",
            "to_table": "dim_cost_center",
            "join_sql": "fact_budget_entry.cost_center_id = dim_cost_center.cost_center_id",
            "join_keys": [{"from": "cost_center_id", "to": "cost_center_id"}],
            "relationship_type": "many_to_one",
            "description": "预算关联成本中心",
        },
        {
            "from_table": "dim_account",
            "to_table": "dim_account",
            "join_sql": "dim_account.parent_account_id = dim_account.account_id",
            "join_keys": [{"from": "parent_account_id", "to": "account_id"}],
            "relationship_type": "many_to_one",
            "description": "科目上级（树形）",
        },
        {
            "from_table": "dim_profit_item",
            "to_table": "dim_profit_item",
            "join_sql": "dim_profit_item.parent_profit_item_id = dim_profit_item.profit_item_id",
            "join_keys": [{"from": "parent_profit_item_id", "to": "profit_item_id"}],
            "relationship_type": "many_to_one",
            "description": "利润项上级（树形）",
        },
        {
            "from_table": "dim_cost_item",
            "to_table": "dim_cost_item",
            "join_sql": "dim_cost_item.parent_cost_item_id = dim_cost_item.cost_item_id",
            "join_keys": [{"from": "parent_cost_item_id", "to": "cost_item_id"}],
            "relationship_type": "many_to_one",
            "description": "成本项上级（树形）",
        },
    ]
    for rel in table_relationships:
        rid = s.tables.add_relationship(**rel)
        output.print(f"OK {rel['from_table']} -> {rel['to_table']}")

    # 4. 注册 Cube
    output.print("\n[4/9] 注册 Cube...")

    actual = "fact_gl_journal_entry"
    budget = "fact_budget_entry"

    # ActualCube
    s.register_cube(
        name="ActualCube",
        table=actual,
        title="实际发生主Cube",
        measures=[
            {"name": "debit_total", "col": "debit_amount", "agg": "sum", "title": "借方合计"},
            {"name": "credit_total", "col": "credit_amount", "agg": "sum", "title": "贷方合计"},
            {"name": "net_amount", "col": "amount_signed", "agg": "sum", "title": "损益符号额"},
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
            {"name": "profit_item_id", "col": "profit_item_id", "type": "string", "title": "利润项ID"},
            {"name": "profit_item_name", "col": "profit_item_name", "type": "string", "title": "利润项名称"},
            {"name": "cost_item_id", "col": "cost_item_id", "type": "string", "title": "成本项ID"},
            {"name": "cost_item_name", "col": "cost_item_name", "type": "string", "title": "成本项名称"},
            {"name": "cost_center_id", "col": "cost_center_id", "type": "string", "title": "成本中心ID"},
            {"name": "cost_center_name", "col": "cost_center_name", "type": "string", "title": "成本中心"},
            {"name": "department", "col": "department", "type": "string", "title": "部门"},
            {"name": "voucher_no", "col": "voucher_no", "type": "string", "title": "凭证号"},
        ],
    )
    output.print("OK ActualCube")

    # AccountCube
    s.register_cube(
        name="AccountCube",
        table=actual,
        title="科目实际Cube",
        measures=[
            {"name": "net_amount", "col": "amount_signed", "agg": "sum", "title": "实际发生"},
            {"name": "line_count", "col": "line_id", "agg": "count", "title": "分录行数"},
        ],
        dimensions=[
            {"name": "account_id", "col": "account_id", "type": "string", "title": "科目ID"},
            {"name": "account_code", "col": "account_code", "type": "string", "title": "科目编码"},
            {"name": "account_name", "col": "account_name", "type": "string", "title": "科目名称"},
            {"name": "account_type", "col": "account_type", "type": "string", "title": "科目类型"},
            {"name": "pl_category", "col": "pl_category", "type": "string", "title": "损益大类"},
            {"name": "profit_item_id", "col": "profit_item_id", "type": "string", "title": "利润项ID"},
            {"name": "cost_item_id", "col": "cost_item_id", "type": "string", "title": "成本项ID"},
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "会计年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "会计期间"},
        ],
    )
    output.print("OK AccountCube")

    # ProfitItemCube
    s.register_cube(
        name="ProfitItemCube",
        table=actual,
        title="利润项实际Cube",
        measures=[
            {"name": "net_amount", "col": "amount_signed", "agg": "sum", "title": "实际发生"},
            {"name": "line_count", "col": "line_id", "agg": "count", "title": "分录行数"},
        ],
        dimensions=[
            {"name": "profit_item_id", "col": "profit_item_id", "type": "string", "title": "利润项ID"},
            {"name": "profit_item_name", "col": "profit_item_name", "type": "string", "title": "利润项名称"},
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "会计年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "会计期间"},
        ],
    )
    output.print("OK ProfitItemCube")

    # CostItemCube
    s.register_cube(
        name="CostItemCube",
        table=actual,
        title="成本项实际Cube",
        measures=[
            {"name": "net_amount", "col": "amount_signed", "agg": "sum", "title": "实际发生"},
            {"name": "line_count", "col": "line_id", "agg": "count", "title": "分录行数"},
        ],
        dimensions=[
            {"name": "cost_item_id", "col": "cost_item_id", "type": "string", "title": "成本项ID"},
            {"name": "cost_item_name", "col": "cost_item_name", "type": "string", "title": "成本项名称"},
            {"name": "cost_item_type", "col": "cost_item_id", "type": "string", "title": "成本项类型"},
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "会计年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "会计期间"},
        ],
    )
    output.print("OK CostItemCube")

    # CostCenterCube
    s.register_cube(
        name="CostCenterCube",
        table=actual,
        title="成本中心实际Cube",
        measures=[
            {"name": "net_amount", "col": "amount_signed", "agg": "sum", "title": "实际发生"},
            {"name": "line_count", "col": "line_id", "agg": "count", "title": "分录行数"},
        ],
        dimensions=[
            {"name": "cost_center_id", "col": "cost_center_id", "type": "string", "title": "成本中心ID"},
            {"name": "cost_center_name", "col": "cost_center_name", "type": "string", "title": "成本中心"},
            {"name": "department", "col": "department", "type": "string", "title": "部门"},
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "会计年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "会计期间"},
        ],
    )
    output.print("OK CostCenterCube")

    # BudgetCube
    s.register_cube(
        name="BudgetCube",
        table=budget,
        title="预算Cube",
        measures=[
            {"name": "budget_amount", "col": "budget_amount", "agg": "sum", "title": "预算金额"},
            {"name": "budget_lines", "col": "line_id", "agg": "count", "title": "预算行数"},
        ],
        dimensions=[
            {"name": "budget_version", "col": "budget_version", "type": "string", "title": "预算版本"},
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "预算年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "预算期间"},
            {"name": "account_id", "col": "account_id", "type": "string", "title": "科目ID"},
            {"name": "profit_item_id", "col": "profit_item_id", "type": "string", "title": "利润项ID"},
            {"name": "cost_item_id", "col": "cost_item_id", "type": "string", "title": "成本项ID"},
            {"name": "cost_center_id", "col": "cost_center_id", "type": "string", "title": "成本中心ID"},
        ],
    )
    output.print("OK BudgetCube")

    # BudgetVsActualCube
    s.register_cube(
        name="BudgetVsActualCube",
        table=budget,
        title="预实对比Cube",
        measures=[
            {"name": "budget_amount", "col": "budget_amount", "agg": "sum", "title": "预算金额"},
            {"name": "budget_lines", "col": "line_id", "agg": "count", "title": "预算行数"},
        ],
        dimensions=[
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "期间"},
            {"name": "account_id", "col": "account_id", "type": "string", "title": "科目ID"},
            {"name": "profit_item_id", "col": "profit_item_id", "type": "string", "title": "利润项ID"},
            {"name": "cost_item_id", "col": "cost_item_id", "type": "string", "title": "成本项ID"},
            {"name": "cost_center_id", "col": "cost_center_id", "type": "string", "title": "成本中心ID"},
            {"name": "budget_version", "col": "budget_version", "type": "string", "title": "预算版本"},
        ],
    )
    output.print("OK BudgetVsActualCube")

    # 5. 定义对象类型
    output.print("\n[5/9] 定义对象类型...")

    # Account
    s.onto.define_object_type(
        code="Account",
        name="会计科目",
        description="会计科目主数据",
        category_347="主数据",
    )
    s.onto.bind_source(
        "Account",
        "dazi_cube",
        config={"cube": "AccountCube"}
    )
    output.print("OK Account")

    # ProfitItem
    s.onto.define_object_type(
        code="ProfitItem",
        name="利润项",
        description="利润项主数据",
        category_347="主数据",
    )
    s.onto.bind_source(
        "ProfitItem",
        "dazi_cube",
        config={"cube": "ProfitItemCube"}
    )
    output.print("OK ProfitItem")

    # CostItem
    s.onto.define_object_type(
        code="CostItem",
        name="成本项",
        description="成本项主数据",
        category_347="主数据",
    )
    s.onto.bind_source(
        "CostItem",
        "dazi_cube",
        config={"cube": "CostItemCube"}
    )
    output.print("OK CostItem")

    # CostCenter
    s.onto.define_object_type(
        code="CostCenter",
        name="成本中心",
        description="成本中心/部门主数据",
        category_347="主数据",
    )
    s.onto.bind_source(
        "CostCenter",
        "dazi_cube",
        config={"cube": "CostCenterCube"}
    )
    output.print("OK CostCenter")

    # JournalEntry
    s.onto.define_object_type(
        code="JournalEntry",
        name="实际分录",
        description="总账凭证行实际发生额",
        category_347="事务",
    )
    s.onto.bind_source(
        "JournalEntry",
        "dazi_cube",
        config={"cube": "ActualCube"}
    )
    output.print("OK JournalEntry")

    # BudgetLine
    s.onto.define_object_type(
        code="BudgetLine",
        name="预算行",
        description="预算编制数据行",
        category_347="事务",
    )
    s.onto.bind_source(
        "BudgetLine",
        "dazi_cube",
        config={"cube": "BudgetCube"}
    )
    output.print("OK BudgetLine")

    # ProfitAnalysis
    s.onto.define_object_type(
        code="ProfitAnalysis",
        name="利润分析",
        description="利润分析汇总对象",
        category_347="分析",
    )
    s.onto.bind_source(
        "ProfitAnalysis",
        "dazi_cube",
        config={"cube": "ActualCube"}
    )
    output.print("OK ProfitAnalysis")

    # BudgetAnalysis
    s.onto.define_object_type(
        code="BudgetAnalysis",
        name="预算分析",
        description="预算分析汇总对象",
        category_347="分析",
    )
    s.onto.bind_source(
        "BudgetAnalysis",
        "dazi_cube",
        config={"cube": "BudgetVsActualCube"}
    )
    output.print("OK BudgetAnalysis")

    # 6. 定义属性
    output.print("\n[6/9] 定义对象属性...")

    # Account 属性
    s.onto.define_property("Account", "code", "科目编码", semantic_role="dimension", qualified_name="AccountCube.account_code")
    s.onto.define_property("Account", "name", "科目名称", semantic_role="dimension", qualified_name="AccountCube.account_name")
    s.onto.define_property("Account", "type", "科目类型", semantic_role="dimension", qualified_name="AccountCube.account_type")
    s.onto.define_property("Account", "pl_category", "损益大类", semantic_role="dimension", qualified_name="AccountCube.pl_category")
    s.onto.define_property("Account", "net_amount", "实际发生", semantic_role="measure", qualified_name="AccountCube.net_amount")

    # ProfitItem 属性
    s.onto.define_property("ProfitItem", "name", "利润项名称", semantic_role="dimension", qualified_name="ProfitItemCube.profit_item_name")
    s.onto.define_property("ProfitItem", "net_amount", "实际发生", semantic_role="measure", qualified_name="ProfitItemCube.net_amount")

    # CostItem 属性
    s.onto.define_property("CostItem", "name", "成本项名称", semantic_role="dimension", qualified_name="CostItemCube.cost_item_name")
    s.onto.define_property("CostItem", "net_amount", "实际发生", semantic_role="measure", qualified_name="CostItemCube.net_amount")

    # CostCenter 属性
    s.onto.define_property("CostCenter", "name", "成本中心名称", semantic_role="dimension", qualified_name="CostCenterCube.cost_center_name")
    s.onto.define_property("CostCenter", "department", "部门", semantic_role="dimension", qualified_name="CostCenterCube.department")
    s.onto.define_property("CostCenter", "net_amount", "实际发生", semantic_role="measure", qualified_name="CostCenterCube.net_amount")

    # JournalEntry 属性
    s.onto.define_property("JournalEntry", "posting_date", "记账日期", semantic_role="dimension", qualified_name="ActualCube.posting_date")
    s.onto.define_property("JournalEntry", "net_amount", "损益金额", semantic_role="measure", qualified_name="ActualCube.net_amount")
    s.onto.define_property("JournalEntry", "debit", "借方", semantic_role="measure", qualified_name="ActualCube.debit_total")
    s.onto.define_property("JournalEntry", "credit", "贷方", semantic_role="measure", qualified_name="ActualCube.credit_total")

    output.print("OK 属性定义完成")

    # 7. 定义链接类型
    output.print("\n[7/9] 定义链接类型...")

    # 归属关系
    s.onto.define_link_type(code="entry_belongs_account", name="分录归属科目", from_object_type_code="JournalEntry", to_object_type_code="Account", category_347="归属关系")
    s.onto.define_link_type(code="entry_belongs_profit_item", name="分录归属利润项", from_object_type_code="JournalEntry", to_object_type_code="ProfitItem", category_347="归属关系")
    s.onto.define_link_type(code="entry_belongs_cost_item", name="分录归属成本项", from_object_type_code="JournalEntry", to_object_type_code="CostItem", category_347="归属关系")
    s.onto.define_link_type(code="entry_belongs_cost_center", name="分录归属成本中心", from_object_type_code="JournalEntry", to_object_type_code="CostCenter", category_347="归属关系")
    s.onto.define_link_type(code="budget_for_account", name="预算对应科目", from_object_type_code="BudgetLine", to_object_type_code="Account", category_347="归属关系")
    s.onto.define_link_type(code="budget_for_cost_center", name="预算对应成本中心", from_object_type_code="BudgetLine", to_object_type_code="CostCenter", category_347="归属关系")

    # 层级关系
    s.onto.define_link_type(code="account_has_parent", name="科目上级", from_object_type_code="Account", to_object_type_code="Account", category_347="层级关系")
    s.onto.define_link_type(code="profit_item_has_parent", name="利润项上级", from_object_type_code="ProfitItem", to_object_type_code="ProfitItem", category_347="层级关系")
    s.onto.define_link_type(code="cost_item_has_parent", name="成本项上级", from_object_type_code="CostItem", to_object_type_code="CostItem", category_347="层级关系")

    # 对比关系
    s.onto.define_link_type(code="budget_compared_to_actual", name="预算对比实际", from_object_type_code="BudgetAnalysis", to_object_type_code="ProfitAnalysis", category_347="对比关系")

    # 分析归因
    s.onto.define_link_type(code="analysis_by_account", name="分析归因科目", from_object_type_code="ProfitAnalysis", to_object_type_code="Account", category_347="分析归因")
    s.onto.define_link_type(code="analysis_by_profit_item", name="分析归因利润项", from_object_type_code="ProfitAnalysis", to_object_type_code="ProfitItem", category_347="分析归因")
    s.onto.define_link_type(code="analysis_by_cost_item", name="分析归因成本项", from_object_type_code="ProfitAnalysis", to_object_type_code="CostItem", category_347="分析归因")
    s.onto.define_link_type(code="analysis_by_cost_center", name="分析归因成本中心", from_object_type_code="ProfitAnalysis", to_object_type_code="CostCenter", category_347="分析归因")

    output.print("OK 链接定义完成")

    # 8. 同步指标引用
    output.print("\n[8/9] 同步指标引用...")
    s.sync_metric_refs()
    output.print("OK sync_metric_refs")

    # 9. 输出摘要
    output.print("\n[9/9] 初始化完成")

    summary = {
        "ok": True,
        "space_id": space_id,
        "tables": len(TABLE_REGISTRY),
        "relationships": len(table_relationships),
        "cubes": 7,
        "objects": 8,
        "links": 14,
    }
    output.success("利润成本分析本体初始化完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))