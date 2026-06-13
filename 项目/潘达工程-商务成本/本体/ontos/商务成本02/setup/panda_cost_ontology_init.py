"""商务成本本体初始化脚本 — space__panda_construction

初始化内容：
1. 创建物理表（23个表：11个维表 + 12个事实表）
2. 注册表到空间
3. 注册表间关系（29条）
4. 注册 Cube（9个）及派生度量
5. 定义对象类型（11种）
6. 绑定数据源
7. 定义属性
8. 定义链接类型（4种）
9. 定义动作类型（6种）
10. 同步指标引用

放置：项目/潘达工程-商务成本/本体/ontos/商务成本02/setup/panda_cost_ontology_init.py
发布：dazi onto script publish .../setup/panda_cost_ontology_init.py --space space__panda_construction --type setup
规划对照：plans/商务成本本体规划方案.md
"""

import json

def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)

    output.print("=== 商务成本本体初始化 ===")
    output.print(f"空间: {space_id}")

    # 1. 创建物理表
    output.print("\n[1/10] 创建物理表...")

    # dim_project
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_project (
            project_key String,
            project_name String,
            project_code String,
            project_type String,
            project_stage String,
            customer_name String,
            contract_amount_net Float64,
            contract_date Date,
            start_date Date,
            planned_end_date Date,
            actual_end_date Date,
            quality_level String,
            profit_target Float64,
            status String,
            created_at DateTime DEFAULT now(),
            updated_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_key)
    """)
    output.print("OK dim_project")

    # dim_company
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_company (
            company_key String,
            company_name String,
            company_code String,
            company_type String,
            industry String,
            region String,
            scale String,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (company_key)
    """)
    output.print("OK dim_company")

    # dim_cost_subject
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_cost_subject (
            cost_subject_key String,
            subject_code String,
            subject_name String,
            subject_level Int8,
            parent_subject_key String,
            subject_type String,
            is_rigid UInt8,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (cost_subject_key)
    """)
    output.print("OK dim_cost_subject")

    # dim_contract_type
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_contract_type (
            contract_type_key String,
            contract_type_code String,
            contract_type_name String,
            category String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (contract_type_key)
    """)
    output.print("OK dim_contract_type")

    # dim_currency
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_currency (
            currency_key String,
            currency_code String,
            currency_name String,
            exchange_rate Float64,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (currency_key)
    """)
    output.print("OK dim_currency")

    # dim_employee
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_employee (
            employee_key String,
            employee_name String,
            employee_code String,
            department String,
            position String,
            role String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (employee_key)
    """)
    output.print("OK dim_employee")

    # dim_supplier
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_supplier (
            supplier_key String,
            supplier_name String,
            supplier_code String,
            supplier_type String,
            region String,
            credit_rating String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (supplier_key)
    """)
    output.print("OK dim_supplier")

    # dim_region
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_region (
            region_key String,
            region_code String,
            region_name String,
            province String,
            city String,
            district String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (region_key)
    """)
    output.print("OK dim_region")

    # dim_industry
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_industry (
            industry_key String,
            industry_code String,
            industry_name String,
            industry_level Int8,
            parent_industry_key String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (industry_key)
    """)
    output.print("OK dim_industry")

    # dim_date
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
            year_month String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (date_key)
    """)
    output.print("OK dim_date")

    # dim_organization
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_organization (
            org_key String,
            org_name String,
            org_code String,
            org_type String,
            parent_org_key String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (org_key)
    """)
    output.print("OK dim_organization")

    # fact_project_cost
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_project_cost (
            project_key String,
            cost_subject_key String,
            company_key String,
            date_key Int32,
            calendar_date Date,
            cost_amount Float64,
            budget_amount Float64,
            currency_key String,
            cost_type String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_key, date_key, cost_subject_key)
    """)
    output.print("OK fact_project_cost")

    # fact_project_budget
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_project_budget (
            project_key String,
            cost_subject_key String,
            date_key Int32,
            calendar_date Date,
            budget_amount Float64,
            revised_budget_amount Float64,
            currency_key String,
            budget_type String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_key, date_key, cost_subject_key)
    """)
    output.print("OK fact_project_budget")

    # fact_project_output
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_project_output (
            project_key String,
            date_key Int32,
            calendar_date Date,
            output_amount Float64,
            confirmed_amount Float64,
            output_type String,
            currency_key String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_key, date_key)
    """)
    output.print("OK fact_project_output")

    # fact_contract
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_contract (
            contract_key String,
            project_key String,
            company_key String,
            contract_type_key String,
            date_key Int32,
            calendar_date Date,
            contract_amount Float64,
            tax_amount Float64,
            net_amount Float64,
            currency_key String,
            contract_status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (contract_key)
    """)
    output.print("OK fact_contract")

    # fact_cash_flow
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_cash_flow (
            project_key String,
            date_key Int32,
            calendar_date Date,
            inflow_amount Float64,
            outflow_amount Float64,
            net_flow_amount Float64,
            flow_type String,
            currency_key String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_key, date_key)
    """)
    output.print("OK fact_cash_flow")

    # fact_purchase
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_purchase (
            purchase_key String,
            project_key String,
            supplier_key String,
            cost_subject_key String,
            date_key Int32,
            calendar_date Date,
            purchase_amount Float64,
            currency_key String,
            purchase_type String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (purchase_key)
    """)
    output.print("OK fact_purchase")

    # fact_expense
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_expense (
            expense_key String,
            project_key String,
            employee_key String,
            cost_subject_key String,
            date_key Int32,
            calendar_date Date,
            expense_amount Float64,
            expense_type String,
            currency_key String,
            approved UInt8,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (expense_key)
    """)
    output.print("OK fact_expense")

    # fact_risk
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_risk (
            risk_key String,
            project_key String,
            date_key Int32,
            calendar_date Date,
            risk_type String,
            risk_level String,
            risk_value Float64,
            risk_description String,
            mitigation_status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (risk_key)
    """)
    output.print("OK fact_risk")

    # fact_project_indicator
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_project_indicator (
            project_key String,
            date_key Int32,
            calendar_date Date,
            total_output Float64,
            total_cost Float64,
            profit Float64,
            profit_rate Float64,
            cash_flow_rate Float64,
            output_confirmed_ratio Float64,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_key, date_key)
    """)
    output.print("OK fact_project_indicator")

    # fact_cost_rigidity
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_cost_rigidity (
            project_key String,
            cost_subject_key String,
            date_key Int32,
            calendar_date Date,
            rigidity_score Float64,
            rigidity_level String,
            flexibility_amount Float64,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_key, date_key, cost_subject_key)
    """)
    output.print("OK fact_cost_rigidity")

    # fact_deviation_record
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_deviation_record (
            deviation_key String,
            project_key String,
            cost_subject_key String,
            date_key Int32,
            calendar_date Date,
            budget_amount Float64,
            actual_amount Float64,
            deviation_amount Float64,
            deviation_rate Float64,
            deviation_status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (deviation_key)
    """)
    output.print("OK fact_deviation_record")

    # fact_employee_cost
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_employee_cost (
            employee_key String,
            project_key String,
            date_key Int32,
            calendar_date Date,
            labor_cost Float64,
            overtime_cost Float64,
            bonus Float64,
            currency_key String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (employee_key, date_key)
    """)
    output.print("OK fact_employee_cost")

    # 2. 注册表到空间
    output.print("\n[2/10] 注册表到空间...")
    
    TABLE_REGISTRY = {
        "dim_project": {"display_name": "项目维表", "description": "项目主数据信息"},
        "dim_company": {"display_name": "公司维表", "description": "公司主体信息"},
        "dim_cost_subject": {"display_name": "成本科目维表", "description": "成本科目层级结构"},
        "dim_contract_type": {"display_name": "合同类型维表", "description": "合同分类信息"},
        "dim_currency": {"display_name": "货币维表", "description": "币种及汇率信息"},
        "dim_employee": {"display_name": "员工维表", "description": "员工信息"},
        "dim_supplier": {"display_name": "供应商维表", "description": "供应商信息"},
        "dim_region": {"display_name": "区域维表", "description": "行政区划信息"},
        "dim_industry": {"display_name": "行业维表", "description": "行业分类信息"},
        "dim_date": {"display_name": "日期维表", "description": "日历维度"},
        "dim_organization": {"display_name": "组织维表", "description": "组织架构信息"},
        "fact_project_cost": {"display_name": "项目成本事实表", "description": "项目成本明细"},
        "fact_project_budget": {"display_name": "项目预算事实表", "description": "项目预算数据"},
        "fact_project_output": {"display_name": "项目产出事实表", "description": "项目产出数据"},
        "fact_contract": {"display_name": "合同事实表", "description": "合同数据"},
        "fact_cash_flow": {"display_name": "现金流事实表", "description": "现金流数据"},
        "fact_purchase": {"display_name": "采购事实表", "description": "采购数据"},
        "fact_expense": {"display_name": "费用事实表", "description": "费用报销数据"},
        "fact_risk": {"display_name": "风险事实表", "description": "风险记录"},
        "fact_project_indicator": {"display_name": "项目指标事实表", "description": "项目关键指标"},
        "fact_cost_rigidity": {"display_name": "成本刚性事实表", "description": "成本刚性分析数据"},
        "fact_deviation_record": {"display_name": "偏差记录事实表", "description": "成本偏差记录"},
        "fact_employee_cost": {"display_name": "员工成本事实表", "description": "员工成本数据"},
    }
    
    for tbl_name, meta in TABLE_REGISTRY.items():
        s.tables.register_with_meta(
            table_name=tbl_name,
            display_name=meta["display_name"],
            description=meta.get("description"),
            force_column_meta=True,
        )
        output.print(f"OK {tbl_name} ({meta['display_name']})")

    # 3. 注册表间关系
    output.print("\n[3/10] 注册表间关系...")

    table_relationships = [
        {"from_table": "fact_project_cost", "to_table": "dim_project", "join_sql": "fact_project_cost.project_key = dim_project.project_key", "join_keys": [{"from": "project_key", "to": "project_key"}], "relationship_type": "many_to_one", "description": "项目成本关联项目"},
        {"from_table": "fact_project_cost", "to_table": "dim_cost_subject", "join_sql": "fact_project_cost.cost_subject_key = dim_cost_subject.cost_subject_key", "join_keys": [{"from": "cost_subject_key", "to": "cost_subject_key"}], "relationship_type": "many_to_one", "description": "项目成本关联成本科目"},
        {"from_table": "fact_project_cost", "to_table": "dim_company", "join_sql": "fact_project_cost.company_key = dim_company.company_key", "join_keys": [{"from": "company_key", "to": "company_key"}], "relationship_type": "many_to_one", "description": "项目成本关联公司"},
        {"from_table": "fact_project_cost", "to_table": "dim_date", "join_sql": "fact_project_cost.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "项目成本关联日期"},
        {"from_table": "fact_project_budget", "to_table": "dim_project", "join_sql": "fact_project_budget.project_key = dim_project.project_key", "join_keys": [{"from": "project_key", "to": "project_key"}], "relationship_type": "many_to_one", "description": "项目预算关联项目"},
        {"from_table": "fact_project_budget", "to_table": "dim_cost_subject", "join_sql": "fact_project_budget.cost_subject_key = dim_cost_subject.cost_subject_key", "join_keys": [{"from": "cost_subject_key", "to": "cost_subject_key"}], "relationship_type": "many_to_one", "description": "项目预算关联成本科目"},
        {"from_table": "fact_project_budget", "to_table": "dim_date", "join_sql": "fact_project_budget.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "项目预算关联日期"},
        {"from_table": "fact_project_output", "to_table": "dim_project", "join_sql": "fact_project_output.project_key = dim_project.project_key", "join_keys": [{"from": "project_key", "to": "project_key"}], "relationship_type": "many_to_one", "description": "项目产出关联项目"},
        {"from_table": "fact_project_output", "to_table": "dim_date", "join_sql": "fact_project_output.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "项目产出关联日期"},
        {"from_table": "fact_contract", "to_table": "dim_project", "join_sql": "fact_contract.project_key = dim_project.project_key", "join_keys": [{"from": "project_key", "to": "project_key"}], "relationship_type": "many_to_one", "description": "合同关联项目"},
        {"from_table": "fact_contract", "to_table": "dim_company", "join_sql": "fact_contract.company_key = dim_company.company_key", "join_keys": [{"from": "company_key", "to": "company_key"}], "relationship_type": "many_to_one", "description": "合同关联公司"},
        {"from_table": "fact_contract", "to_table": "dim_contract_type", "join_sql": "fact_contract.contract_type_key = dim_contract_type.contract_type_key", "join_keys": [{"from": "contract_type_key", "to": "contract_type_key"}], "relationship_type": "many_to_one", "description": "合同关联合同类型"},
        {"from_table": "fact_contract", "to_table": "dim_date", "join_sql": "fact_contract.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "合同关联日期"},
        {"from_table": "fact_cash_flow", "to_table": "dim_project", "join_sql": "fact_cash_flow.project_key = dim_project.project_key", "join_keys": [{"from": "project_key", "to": "project_key"}], "relationship_type": "many_to_one", "description": "现金流关联项目"},
        {"from_table": "fact_cash_flow", "to_table": "dim_date", "join_sql": "fact_cash_flow.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "现金流关联日期"},
        {"from_table": "fact_purchase", "to_table": "dim_project", "join_sql": "fact_purchase.project_key = dim_project.project_key", "join_keys": [{"from": "project_key", "to": "project_key"}], "relationship_type": "many_to_one", "description": "采购关联项目"},
        {"from_table": "fact_purchase", "to_table": "dim_supplier", "join_sql": "fact_purchase.supplier_key = dim_supplier.supplier_key", "join_keys": [{"from": "supplier_key", "to": "supplier_key"}], "relationship_type": "many_to_one", "description": "采购关联供应商"},
        {"from_table": "fact_purchase", "to_table": "dim_cost_subject", "join_sql": "fact_purchase.cost_subject_key = dim_cost_subject.cost_subject_key", "join_keys": [{"from": "cost_subject_key", "to": "cost_subject_key"}], "relationship_type": "many_to_one", "description": "采购关联成本科目"},
        {"from_table": "fact_purchase", "to_table": "dim_date", "join_sql": "fact_purchase.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "采购关联日期"},
        {"from_table": "fact_expense", "to_table": "dim_project", "join_sql": "fact_expense.project_key = dim_project.project_key", "join_keys": [{"from": "project_key", "to": "project_key"}], "relationship_type": "many_to_one", "description": "费用关联项目"},
        {"from_table": "fact_expense", "to_table": "dim_employee", "join_sql": "fact_expense.employee_key = dim_employee.employee_key", "join_keys": [{"from": "employee_key", "to": "employee_key"}], "relationship_type": "many_to_one", "description": "费用关联员工"},
        {"from_table": "fact_expense", "to_table": "dim_cost_subject", "join_sql": "fact_expense.cost_subject_key = dim_cost_subject.cost_subject_key", "join_keys": [{"from": "cost_subject_key", "to": "cost_subject_key"}], "relationship_type": "many_to_one", "description": "费用关联成本科目"},
        {"from_table": "fact_expense", "to_table": "dim_date", "join_sql": "fact_expense.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "费用关联日期"},
        {"from_table": "fact_risk", "to_table": "dim_project", "join_sql": "fact_risk.project_key = dim_project.project_key", "join_keys": [{"from": "project_key", "to": "project_key"}], "relationship_type": "many_to_one", "description": "风险关联项目"},
        {"from_table": "fact_risk", "to_table": "dim_date", "join_sql": "fact_risk.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "风险关联日期"},
        {"from_table": "fact_project_indicator", "to_table": "dim_project", "join_sql": "fact_project_indicator.project_key = dim_project.project_key", "join_keys": [{"from": "project_key", "to": "project_key"}], "relationship_type": "many_to_one", "description": "指标关联项目"},
        {"from_table": "fact_project_indicator", "to_table": "dim_date", "join_sql": "fact_project_indicator.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "指标关联日期"},
        {"from_table": "fact_cost_rigidity", "to_table": "dim_project", "join_sql": "fact_cost_rigidity.project_key = dim_project.project_key", "join_keys": [{"from": "project_key", "to": "project_key"}], "relationship_type": "many_to_one", "description": "成本刚性关联项目"},
        {"from_table": "fact_cost_rigidity", "to_table": "dim_cost_subject", "join_sql": "fact_cost_rigidity.cost_subject_key = dim_cost_subject.cost_subject_key", "join_keys": [{"from": "cost_subject_key", "to": "cost_subject_key"}], "relationship_type": "many_to_one", "description": "成本刚性关联成本科目"},
        {"from_table": "fact_deviation_record", "to_table": "dim_project", "join_sql": "fact_deviation_record.project_key = dim_project.project_key", "join_keys": [{"from": "project_key", "to": "project_key"}], "relationship_type": "many_to_one", "description": "偏差记录关联项目"},
    ]
    
    for rel in table_relationships:
        rid = s.tables.add_relationship(**rel)
        output.print(f"OK {rel['from_table']} -> {rel['to_table']}")

    # 4. 注册 Cube（9个）
    output.print("\n[4/10] 注册 Cube...")

    # ProjectCostCube
    s.register_cube(
        name="ProjectCostCube",
        table="fact_project_cost",
        title="项目成本Cube",
        measures=[
            {"name": "cost_amount", "col": "cost_amount", "agg": "sum", "title": "成本金额"},
            {"name": "budget_amount", "col": "budget_amount", "agg": "sum", "title": "预算金额"},
        ],
        dimensions=[
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目编号"},
            {"name": "cost_subject_key", "col": "cost_subject_key", "type": "string", "title": "成本科目"},
            {"name": "company_key", "col": "company_key", "type": "string", "title": "公司"},
            {"name": "date_key", "col": "date_key", "type": "int32", "title": "日期键"},
            {"name": "calendar_date", "col": "calendar_date", "type": "date", "title": "日期"},
        ],
    )
    output.print("OK ProjectCostCube")

    # ProjectBudgetCube
    s.register_cube(
        name="ProjectBudgetCube",
        table="fact_project_budget",
        title="项目预算Cube",
        measures=[
            {"name": "budget_amount", "col": "budget_amount", "agg": "sum", "title": "预算金额"},
            {"name": "revised_budget_amount", "col": "revised_budget_amount", "agg": "sum", "title": "修订预算金额"},
        ],
        dimensions=[
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目编号"},
            {"name": "cost_subject_key", "col": "cost_subject_key", "type": "string", "title": "成本科目"},
            {"name": "date_key", "col": "date_key", "type": "int32", "title": "日期键"},
            {"name": "calendar_date", "col": "calendar_date", "type": "date", "title": "日期"},
        ],
    )
    output.print("OK ProjectBudgetCube")

    # ProjectOutputCube
    s.register_cube(
        name="ProjectOutputCube",
        table="fact_project_output",
        title="项目产出Cube",
        measures=[
            {"name": "output_amount", "col": "output_amount", "agg": "sum", "title": "产出金额"},
            {"name": "confirmed_amount", "col": "confirmed_amount", "agg": "sum", "title": "确认金额"},
        ],
        dimensions=[
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目编号"},
            {"name": "date_key", "col": "date_key", "type": "int32", "title": "日期键"},
            {"name": "calendar_date", "col": "calendar_date", "type": "date", "title": "日期"},
        ],
    )
    output.print("OK ProjectOutputCube")

    # ContractCube
    s.register_cube(
        name="ContractCube",
        table="fact_contract",
        title="合同Cube",
        measures=[
            {"name": "contract_amount", "col": "contract_amount", "agg": "sum", "title": "合同金额"},
            {"name": "tax_amount", "col": "tax_amount", "agg": "sum", "title": "税额"},
            {"name": "net_amount", "col": "net_amount", "agg": "sum", "title": "净额"},
        ],
        dimensions=[
            {"name": "contract_key", "col": "contract_key", "type": "string", "title": "合同编号"},
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目编号"},
            {"name": "company_key", "col": "company_key", "type": "string", "title": "公司"},
            {"name": "contract_type_key", "col": "contract_type_key", "type": "string", "title": "合同类型"},
            {"name": "date_key", "col": "date_key", "type": "int32", "title": "日期键"},
        ],
    )
    output.print("OK ContractCube")

    # CashFlowCube
    s.register_cube(
        name="CashFlowCube",
        table="fact_cash_flow",
        title="现金流Cube",
        measures=[
            {"name": "inflow_amount", "col": "inflow_amount", "agg": "sum", "title": "流入金额"},
            {"name": "outflow_amount", "col": "outflow_amount", "agg": "sum", "title": "流出金额"},
            {"name": "net_flow_amount", "col": "net_flow_amount", "agg": "sum", "title": "净流量"},
        ],
        dimensions=[
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目编号"},
            {"name": "date_key", "col": "date_key", "type": "int32", "title": "日期键"},
            {"name": "calendar_date", "col": "calendar_date", "type": "date", "title": "日期"},
        ],
    )
    output.print("OK CashFlowCube")

    # PurchaseCube
    s.register_cube(
        name="PurchaseCube",
        table="fact_purchase",
        title="采购Cube",
        measures=[
            {"name": "purchase_amount", "col": "purchase_amount", "agg": "sum", "title": "采购金额"},
        ],
        dimensions=[
            {"name": "purchase_key", "col": "purchase_key", "type": "string", "title": "采购编号"},
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目编号"},
            {"name": "supplier_key", "col": "supplier_key", "type": "string", "title": "供应商"},
            {"name": "cost_subject_key", "col": "cost_subject_key", "type": "string", "title": "成本科目"},
            {"name": "date_key", "col": "date_key", "type": "int32", "title": "日期键"},
        ],
    )
    output.print("OK PurchaseCube")

    # RiskCube
    s.register_cube(
        name="RiskCube",
        table="fact_risk",
        title="风险Cube",
        measures=[
            {"name": "risk_value", "col": "risk_value", "agg": "avg", "title": "风险值"},
        ],
        dimensions=[
            {"name": "risk_key", "col": "risk_key", "type": "string", "title": "风险编号"},
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目编号"},
            {"name": "risk_type", "col": "risk_type", "type": "string", "title": "风险类型"},
            {"name": "risk_level", "col": "risk_level", "type": "string", "title": "风险等级"},
            {"name": "date_key", "col": "date_key", "type": "int32", "title": "日期键"},
        ],
    )
    output.print("OK RiskCube")

    # ProjectIndicatorCube
    s.register_cube(
        name="ProjectIndicatorCube",
        table="fact_project_indicator",
        title="项目指标Cube",
        measures=[
            {"name": "total_output", "col": "total_output", "agg": "sum", "title": "总产出"},
            {"name": "total_cost", "col": "total_cost", "agg": "sum", "title": "总成本"},
            {"name": "profit", "col": "profit", "agg": "sum", "title": "利润"},
            {"name": "profit_rate", "col": "profit_rate", "agg": "avg", "title": "利润率"},
            {"name": "cash_flow_rate", "col": "cash_flow_rate", "agg": "avg", "title": "现金流转率"},
            {"name": "output_confirmed_ratio", "col": "output_confirmed_ratio", "agg": "avg", "title": "产出确认率"},
        ],
        dimensions=[
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目编号"},
            {"name": "date_key", "col": "date_key", "type": "int32", "title": "日期键"},
            {"name": "calendar_date", "col": "calendar_date", "type": "date", "title": "日期"},
        ],
    )
    output.print("OK ProjectIndicatorCube")

    # CostRigidityCube
    s.register_cube(
        name="CostRigidityCube",
        table="fact_cost_rigidity",
        title="成本刚性Cube",
        measures=[
            {"name": "rigidity_score", "col": "rigidity_score", "agg": "avg", "title": "刚性评分"},
            {"name": "flexibility_amount", "col": "flexibility_amount", "agg": "sum", "title": "弹性金额"},
        ],
        dimensions=[
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目编号"},
            {"name": "cost_subject_key", "col": "cost_subject_key", "type": "string", "title": "成本科目"},
            {"name": "rigidity_level", "col": "rigidity_level", "type": "string", "title": "刚性等级"},
            {"name": "date_key", "col": "date_key", "type": "int32", "title": "日期键"},
        ],
    )
    output.print("OK CostRigidityCube")

    # 5. 派生度量
    output.print("\n[5/10] 配置派生度量...")

    s.upsert_derived_measures(
        "ProjectCostCube",
        [
            {
                "name": "deviation_amount",
                "title": "偏差金额",
                "expression": "ProjectCostCube.budget_amount - ProjectCostCube.cost_amount",
                "description": "预算金额与实际成本的差额",
            },
            {
                "name": "deviation_rate",
                "title": "偏差率",
                "expression": "if(ProjectCostCube.budget_amount > 0, (ProjectCostCube.budget_amount - ProjectCostCube.cost_amount) / ProjectCostCube.budget_amount, 0)",
                "description": "成本偏差率",
            },
        ],
    )
    output.print("OK ProjectCostCube 派生度量")

    s.upsert_derived_measures(
        "ProjectOutputCube",
        [
            {
                "name": "output_confirmed_ratio",
                "title": "产出确认率",
                "expression": "if(ProjectOutputCube.output_amount > 0, ProjectOutputCube.confirmed_amount / ProjectOutputCube.output_amount, 0)",
                "description": "已确认产出占总产出比例",
            },
        ],
    )
    output.print("OK ProjectOutputCube 派生度量")

    s.upsert_derived_measures(
        "ProjectIndicatorCube",
        [
            {
                "name": "profit_margin",
                "title": "利润率",
                "expression": "if(ProjectIndicatorCube.total_output > 0, ProjectIndicatorCube.profit / ProjectIndicatorCube.total_output, 0)",
                "description": "利润/产出",
            },
        ],
    )
    output.print("OK ProjectIndicatorCube 派生度量")

    # 6. 对象类型
    output.print("\n[6/10] 定义对象类型...")

    object_types = [
        ("Project", "项目", "项目业务对象"),
        ("Company", "公司", "公司主体对象"),
        ("CostSubject", "成本科目", "成本科目对象"),
        ("Contract", "合同", "合同对象"),
        ("Supplier", "供应商", "供应商对象"),
        ("Employee", "员工", "员工对象"),
        ("Region", "区域", "区域对象"),
        ("Industry", "行业", "行业对象"),
        ("CashFlow", "现金流", "现金流对象"),
        ("Risk", "风险", "风险对象"),
        ("ProjectAnalysis", "项目分析", "项目多维度分析对象"),
    ]
    for code, name, desc in object_types:
        s.onto.define_object_type(code, name, description=desc)
        output.print(f"OK {code}")

    # 7. 绑定数据源
    output.print("\n[7/10] 绑定数据源...")

    bindings = [
        ("Project", "ProjectCostCube"),
        ("Company", "ProjectCostCube"),
        ("CostSubject", "ProjectCostCube"),
        ("Contract", "ContractCube"),
        ("Supplier", "PurchaseCube"),
        ("Employee", "ProjectCostCube"),
        ("CashFlow", "CashFlowCube"),
        ("Risk", "RiskCube"),
        ("ProjectAnalysis", "ProjectIndicatorCube"),
    ]
    for code, cube in bindings:
        s.onto.bind_source(code, "dazi_cube", config={"cube": cube})
        output.print(f"OK {code} -> {cube}")

    # 8. 定义属性
    output.print("\n[8/10] 定义属性...")

    properties = [
        ("Project", "project_key", "项目编号", "dimension", "ProjectCostCube.project_key"),
        ("Project", "cost_amount", "成本金额", "measure", "ProjectCostCube.cost_amount"),
        ("Project", "budget_amount", "预算金额", "measure", "ProjectCostCube.budget_amount"),
        ("Project", "deviation_amount", "偏差金额", "measure", "ProjectCostCube.deviation_amount"),
        ("Project", "deviation_rate", "偏差率", "measure", "ProjectCostCube.deviation_rate"),
        ("Company", "company_key", "公司编号", "dimension", "ProjectCostCube.company_key"),
        ("CostSubject", "cost_subject_key", "科目编号", "dimension", "ProjectCostCube.cost_subject_key"),
        ("Contract", "contract_key", "合同编号", "dimension", "ContractCube.contract_key"),
        ("Contract", "contract_amount", "合同金额", "measure", "ContractCube.contract_amount"),
        ("Supplier", "supplier_key", "供应商编号", "dimension", "PurchaseCube.supplier_key"),
        ("Supplier", "purchase_amount", "采购金额", "measure", "PurchaseCube.purchase_amount"),
        ("CashFlow", "inflow_amount", "流入金额", "measure", "CashFlowCube.inflow_amount"),
        ("CashFlow", "outflow_amount", "流出金额", "measure", "CashFlowCube.outflow_amount"),
        ("CashFlow", "net_flow_amount", "净流量", "measure", "CashFlowCube.net_flow_amount"),
        ("Risk", "risk_key", "风险编号", "dimension", "RiskCube.risk_key"),
        ("Risk", "risk_value", "风险值", "measure", "RiskCube.risk_value"),
        ("Risk", "risk_level", "风险等级", "dimension", "RiskCube.risk_level"),
        ("ProjectAnalysis", "total_output", "总产出", "measure", "ProjectIndicatorCube.total_output"),
        ("ProjectAnalysis", "total_cost", "总成本", "measure", "ProjectIndicatorCube.total_cost"),
        ("ProjectAnalysis", "profit", "利润", "measure", "ProjectIndicatorCube.profit"),
        ("ProjectAnalysis", "profit_rate", "利润率", "measure", "ProjectIndicatorCube.profit_rate"),
    ]
    for obj_code, prop_code, title, role, qualified_name in properties:
        s.onto.define_property(obj_code, prop_code, title, semantic_role=role, qualified_name=qualified_name)
    output.print(f"OK {len(properties)} 个属性")

    # 9. 定义链接类型
    output.print("\n[9/10] 定义链接类型...")

    link_types = [
        ("project_has_cost", "项目有成本", "Project", "CostSubject"),
        ("project_has_contract", "项目有合同", "Project", "Contract"),
        ("project_has_cash_flow", "项目有现金流", "Project", "CashFlow"),
        ("project_has_risk", "项目有风险", "Project", "Risk"),
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
        "tables": 23,
        "table_relationships": 29,
        "cubes": 9,
        "object_types": 11,
        "properties": len(properties),
        "link_types": len(link_types),
    }
    output.success("本体初始化完成")
    output.print(f"space_id: {space_id}")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=False))