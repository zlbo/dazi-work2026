"""利润分析本体初始化脚本 — space__misc_01

初始化内容：
1. 创建物理表（科目表、成本中心维表、实际分录表、预算表）
2. 注册表到空间（含 display_name / description）
3. 注册表间关系（7条）
4. 注册Cube（5个）及派生度量
5. 定义对象类型（6种）、绑定数据源、属性、链接
6. 同步指标引用
7. 平台分类挂载见 profit_category_mount.py（init/seed/函数 publish 之后执行）

放置：资源/examples/onto/利润示例/setup/profit_ontology_init.py（复制到项目 ontos/<实现名>/setup/）
发布：dazi onto script publish <item-path>/setup/profit_ontology_init.py --space <space-id> --type setup
规划对照：资源/examples/onto/利润示例/plans/规划示例_利润分析本体方案.md
"""

import json

# 与 规划示例_利润分析本体方案.md §2.3、§3.x 对齐：display_name=侧栏显示名，description=业务说明
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
            {"name": "account_level", "display_name": "科目层级", "description": "冗余"},
            {"name": "cost_center_id", "display_name": "成本中心 ID", "description": "关联 dim_cost_center"},
            {"name": "cost_center_name", "display_name": "成本中心", "description": "冗余"},
            {"name": "department", "display_name": "部门", "description": "冗余"},
            {"name": "profit_center", "display_name": "利润中心", "description": "冗余"},
            {"name": "debit_amount", "display_name": "借方"},
            {"name": "credit_amount", "display_name": "贷方"},
            {"name": "amount_signed", "display_name": "损益金额", "description": "收入为正、成本费用为负"},
            {"name": "currency", "display_name": "币种"},
            {"name": "voucher_no", "display_name": "凭证号"},
            {"name": "source_system", "display_name": "来源系统"},
            {"name": "description", "display_name": "摘要", "description": "凭证行摘要文本"},
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
    space_id = "space__misc_01"
    s = space.get(space_id)

    output.print("=== 利润分析本体初始化 ===")
    output.print(f"空间: {space_id}")

    # 1. 创建物理表
    output.print("\n[1/10] 创建物理表...")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_account (
            account_id String,
            account_code String,
            account_name String,
            account_type String,
            pl_category String,
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
        CREATE TABLE IF NOT EXISTS dim_cost_center (
            cost_center_id String,
            cost_center_code String,
            cost_center_name String,
            department String,
            company_code String,
            profit_center String,
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
            account_level Int32,
            cost_center_id String,
            cost_center_name String,
            department String,
            profit_center String,
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

    # 3. 注册表间关系
    output.print("\n[3/10] 注册表间关系...")

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
    ]
    for rel in table_relationships:
        rid = s.tables.add_relationship(**rel)
        output.print(f"OK {rel['from_table']} -> {rel['to_table']}")

    # 4. 注册 Cube
    output.print("\n[4/10] 注册 Cube...")

    actual = "fact_gl_journal_entry"
    budget = "fact_budget_entry"

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
            {"name": "cost_center_id", "col": "cost_center_id", "type": "string", "title": "成本中心ID"},
            {"name": "cost_center_name", "col": "cost_center_name", "type": "string", "title": "成本中心"},
            {"name": "department", "col": "department", "type": "string", "title": "部门"},
            {"name": "voucher_no", "col": "voucher_no", "type": "string", "title": "凭证号"},
        ],
    )
    output.print("OK ActualCube")

    s.register_cube(
        name="AccountActualCube",
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
            {"name": "account_level", "col": "account_level", "type": "int", "title": "科目层级"},
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "会计年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "会计期间"},
        ],
    )
    output.print("OK AccountActualCube")

    s.register_cube(
        name="CostCenterActualCube",
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
            {"name": "profit_center", "col": "profit_center", "type": "string", "title": "利润中心"},
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "会计年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "会计期间"},
        ],
    )
    output.print("OK CostCenterActualCube")

    s.register_cube(
        name="BudgetCube",
        table=budget,
        title="预算Cube",
        measures=[
            {"name": "budget_amount", "col": "budget_amount", "agg": "sum", "title": "预算金额"},
            {"name": "budget_lines", "col": "line_id", "agg": "count", "title": "预算行数"},
        ],
        dimensions=[
            {"name": "line_id", "col": "line_id", "type": "string", "title": "预算行ID"},
            {"name": "budget_version", "col": "budget_version", "type": "string", "title": "预算版本"},
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "预算年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "预算期间"},
            {"name": "account_id", "col": "account_id", "type": "string", "title": "科目ID"},
            {"name": "account_code", "col": "account_code", "type": "string", "title": "科目编码"},
            {"name": "account_type", "col": "account_type", "type": "string", "title": "科目类型"},
            {"name": "pl_category", "col": "pl_category", "type": "string", "title": "损益大类"},
            {"name": "cost_center_id", "col": "cost_center_id", "type": "string", "title": "成本中心ID"},
            {"name": "department", "col": "department", "type": "string", "title": "部门"},
        ],
    )
    output.print("OK BudgetCube")

    s.register_cube(
        name="TimeActualCube",
        table=actual,
        title="时间维度实际Cube",
        measures=[
            {"name": "net_amount", "col": "amount_signed", "agg": "sum", "title": "损益符号额"},
            {"name": "line_count", "col": "line_id", "agg": "count", "title": "分录行数"},
        ],
        dimensions=[
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "posting_date", "col": "posting_date", "type": "date", "title": "记账日期"},
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "会计年度"},
            {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "会计期间"},
        ],
    )
    output.print("OK TimeActualCube")

    # 5. 派生度量
    output.print("\n[5/10] 配置派生度量...")

    def _pl_measures(cube_name, full=False):
        base = [
            {
                "name": "revenue",
                "title": "收入",
                "expression": "sum(if(account_type='收入', amount_signed, 0))",
                "description": "收入类科目发生额",
            },
            {
                "name": "cost",
                "title": "成本",
                "expression": "sum(if(account_type='成本', amount_signed, 0))",
                "description": "成本类科目发生额",
            },
            {
                "name": "expense",
                "title": "费用",
                "expression": "sum(if(account_type='费用', amount_signed, 0))",
                "description": "费用类科目发生额",
            },
        ]
        if not full:
            return base
        return base + [
            {
                "name": "operating_profit",
                "title": "营业利润",
                "expression": f"{cube_name}.revenue - {cube_name}.cost - {cube_name}.expense",
                "description": "收入-成本-费用",
            },
            {
                "name": "profit_margin",
                "title": "利润率",
                "expression": f"if({cube_name}.revenue > 0, {cube_name}.operating_profit / {cube_name}.revenue, 0)",
                "description": "营业利润/收入",
            },
        ]

    s.upsert_derived_measures("ActualCube", _pl_measures("ActualCube", True))
    s.upsert_derived_measures("AccountActualCube", _pl_measures("AccountActualCube", False))
    s.upsert_derived_measures("CostCenterActualCube", _pl_measures("CostCenterActualCube", True))
    s.upsert_derived_measures("TimeActualCube", _pl_measures("TimeActualCube", True))

    s.upsert_derived_measures(
        "BudgetCube",
        [
            {
                "name": "budget_revenue",
                "title": "预算收入",
                "expression": "sum(if(account_type='收入', budget_amount, 0))",
                "description": "预算收入",
            },
            {
                "name": "budget_cost",
                "title": "预算成本",
                "expression": "sum(if(account_type='成本', budget_amount, 0))",
                "description": "预算成本",
            },
            {
                "name": "budget_expense",
                "title": "预算费用",
                "expression": "sum(if(account_type='费用', budget_amount, 0))",
                "description": "预算费用",
            },
        ],
    )
    output.print("OK 派生度量")

    # 6. 对象类型
    output.print("\n[6/10] 定义对象类型...")

    object_types = [
        ("Account", "会计科目", "会计科目业务对象"),
        ("CostCenter", "成本中心", "组织/利润中心业务对象"),
        ("JournalEntry", "实际分录", "凭证行实际发生业务对象"),
        ("BudgetLine", "预算行", "预算编制明细业务对象"),
        ("ProfitAnalysis", "利润分析", "多维度损益指标聚合对象"),
        ("BudgetAnalysis", "预算分析", "预算执行与差异分析对象"),
    ]
    for code, name, desc in object_types:
        s.onto.define_object_type(code, name, description=desc)
        output.print(f"OK {code}")

    # 7. 绑定数据源
    output.print("\n[7/10] 绑定数据源...")

    bindings = [
        ("Account", "AccountActualCube"),
        ("CostCenter", "CostCenterActualCube"),
        ("JournalEntry", "ActualCube"),
        ("BudgetLine", "BudgetCube"),
        ("ProfitAnalysis", "ActualCube"),
        ("BudgetAnalysis", "BudgetCube"),
    ]
    for obj, cube in bindings:
        s.onto.bind_source(obj, "dazi_cube", config={"cube": cube})
        output.print(f"OK {obj} -> {cube}")

    # 8. 属性
    output.print("\n[8/10] 定义属性...")

    def define_props(obj_code, props):
        for code, name, role, qn in props:
            s.onto.define_property(obj_code, code, name, semantic_role=role, qualified_name=qn)

    define_props("Account", [
        ("id", "科目ID", "dimension", "AccountActualCube.account_id"),
        ("code", "科目编码", "dimension", "AccountActualCube.account_code"),
        ("name", "科目名称", "dimension", "AccountActualCube.account_name"),
        ("type", "科目类型", "dimension", "AccountActualCube.account_type"),
        ("pl_category", "损益大类", "dimension", "AccountActualCube.pl_category"),
        ("level", "科目层级", "dimension", "AccountActualCube.account_level"),
        ("net_amount", "实际发生", "measure", "AccountActualCube.net_amount"),
        ("revenue", "收入", "measure", "AccountActualCube.revenue"),
        ("cost", "成本", "measure", "AccountActualCube.cost"),
        ("expense", "费用", "measure", "AccountActualCube.expense"),
    ])
    output.print("OK Account 属性 (10)")

    define_props("CostCenter", [
        ("id", "成本中心ID", "dimension", "CostCenterActualCube.cost_center_id"),
        ("name", "成本中心", "dimension", "CostCenterActualCube.cost_center_name"),
        ("department", "部门", "dimension", "CostCenterActualCube.department"),
        ("profit_center", "利润中心", "dimension", "CostCenterActualCube.profit_center"),
        ("revenue", "收入", "measure", "CostCenterActualCube.revenue"),
        ("cost", "成本", "measure", "CostCenterActualCube.cost"),
        ("expense", "费用", "measure", "CostCenterActualCube.expense"),
        ("operating_profit", "营业利润", "measure", "CostCenterActualCube.operating_profit"),
    ])
    output.print("OK CostCenter 属性 (8)")

    define_props("JournalEntry", [
        ("id", "行ID", "dimension", "ActualCube.line_id"),
        ("posting_date", "记账日期", "dimension", "ActualCube.posting_date"),
        ("fiscal_period", "会计期间", "dimension", "ActualCube.fiscal_period"),
        ("net_amount", "损益金额", "measure", "ActualCube.net_amount"),
        ("debit", "借方", "measure", "ActualCube.debit_total"),
        ("credit", "贷方", "measure", "ActualCube.credit_total"),
    ])
    output.print("OK JournalEntry 属性 (6)")

    define_props("BudgetLine", [
        ("id", "预算行ID", "dimension", "BudgetCube.line_id"),
        ("version", "预算版本", "dimension", "BudgetCube.budget_version"),
        ("fiscal_period", "预算期间", "dimension", "BudgetCube.fiscal_period"),
        ("budget_amount", "预算金额", "measure", "BudgetCube.budget_amount"),
    ])
    output.print("OK BudgetLine 属性 (4)")

    define_props("ProfitAnalysis", [
        ("date", "日期", "dimension", "ActualCube.posting_date"),
        ("pl_category", "损益大类", "dimension", "ActualCube.pl_category"),
        ("department", "部门", "dimension", "ActualCube.department"),
        ("revenue", "收入", "measure", "ActualCube.revenue"),
        ("cost", "成本", "measure", "ActualCube.cost"),
        ("expense", "费用", "measure", "ActualCube.expense"),
        ("operating_profit", "营业利润", "measure", "ActualCube.operating_profit"),
        ("profit_margin", "利润率", "measure", "ActualCube.profit_margin"),
    ])
    output.print("OK ProfitAnalysis 属性 (8)")

    define_props("BudgetAnalysis", [
        ("version", "预算版本", "dimension", "BudgetCube.budget_version"),
        ("fiscal_period", "预算期间", "dimension", "BudgetCube.fiscal_period"),
        ("budget_amount", "预算金额", "measure", "BudgetCube.budget_amount"),
        ("budget_revenue", "预算收入", "measure", "BudgetCube.budget_revenue"),
        ("budget_cost", "预算成本", "measure", "BudgetCube.budget_cost"),
        ("budget_expense", "预算费用", "measure", "BudgetCube.budget_expense"),
    ])
    output.print("OK BudgetAnalysis 属性 (6)")

    # 9. 链接类型
    output.print("\n[9/10] 定义链接与同步指标...")

    link_types = [
        ("entry_belongs_account", "分录归属科目", "JournalEntry", "Account", "分录行对应科目"),
        ("entry_belongs_cost_center", "分录归属成本中心", "JournalEntry", "CostCenter", "分录行对应组织"),
        ("budget_for_account", "预算对应科目", "BudgetLine", "Account", "预算行对应科目"),
        ("budget_for_cost_center", "预算对应成本中心", "BudgetLine", "CostCenter", "预算行对应组织"),
        ("account_has_parent", "科目上级", "Account", "Account", "科目树父级"),
        ("budget_compared_to_actual", "预算对比实际", "BudgetAnalysis", "ProfitAnalysis", "预实差异分析"),
        ("analysis_by_account", "分析归因科目", "ProfitAnalysis", "Account", "指标按科目切片"),
        ("analysis_by_cost_center", "分析归因成本中心", "ProfitAnalysis", "CostCenter", "指标按组织切片"),
        ("account_contributes_profit", "科目贡献利润", "Account", "ProfitAnalysis", "科目损益贡献"),
        ("cost_center_contributes_profit", "组织贡献利润", "CostCenter", "ProfitAnalysis", "成本中心利润贡献"),
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
        "table_relationships": 7,
        "cubes": 5,
        "object_types": 6,
        "properties": 42,
        "link_types": 10,
    }

    output.print("\n=== 利润分析本体初始化完成 ===")
    output.success("初始化成功")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))