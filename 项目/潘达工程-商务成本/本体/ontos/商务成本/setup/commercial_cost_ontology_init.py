# 商务成本本体初始化脚本
# 参考：资源/docs/onto/本体脚本编写指南.md
# 实施顺序：建表 → 注册表 → 注册表间关系 → 注册Cube → 定义本体对象/属性/链接

def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)
    
    output.print("=== 商务成本本体初始化 ===")
    output.print(f"空间: {space_id}")

    # ==================== 1. 表定义与建表 ====================
    output.print("\n[1/5] 创建物理表...")

    # 时间维表
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
        fiscal_year Int16,
        fiscal_period Int8,
        PRIMARY KEY (date_key)
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(calendar_date)
    ORDER BY (date_key)
    """)
    output.print("OK dim_date")

    # 项目主数据
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS dim_project (
        project_key String,
        project_code String,
        project_name String,
        project_type String,
        project_category String,
        business_model String,
        contract_amount Decimal(18,2),
        management_fee_rate Decimal(5,4),
        project_status String,
        start_date Date,
        end_date Date,
        region_key String,
        organization_key String,
        project_manager String,
        is_key_client UInt8,
        is_new_increment UInt8,
        PRIMARY KEY (project_key)
    ) ENGINE = MergeTree()
    ORDER BY (project_key, project_code)
    """)
    output.print("OK dim_project")

    # 合同主数据
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS dim_contract (
        contract_key String,
        contract_code String,
        contract_name String,
        project_key String,
        contract_type String,
        contract_amount Decimal(18,2),
        sign_date Date,
        contract_status String,
        owner_key String,
        PRIMARY KEY (contract_key)
    ) ENGINE = MergeTree()
    ORDER BY (contract_key, project_key, contract_code)
    """)
    output.print("OK dim_contract")

    # 业主维度
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS dim_owner (
        owner_key String,
        owner_code String,
        owner_name String,
        owner_type String,
        credit_level String,
        region_key String,
        PRIMARY KEY (owner_key)
    ) ENGINE = MergeTree()
    ORDER BY (owner_key, owner_code)
    """)
    output.print("OK dim_owner")

    # 成本科目维度
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS dim_cost_subject (
        cost_subject_key String,
        subject_code String,
        subject_name String,
        subject_level Int32,
        parent_key Nullable(String),
        subject_type String,
        is_leaf UInt8,
        PRIMARY KEY (cost_subject_key)
    ) ENGINE = MergeTree()
    ORDER BY (cost_subject_key, subject_code)
    """)
    output.print("OK dim_cost_subject")

    # 地区维度
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS dim_region (
        region_key String,
        region_code String,
        region_name String,
        parent_key Nullable(String),
        region_level Int32,
        is_leaf UInt8,
        PRIMARY KEY (region_key)
    ) ENGINE = MergeTree()
    ORDER BY (region_key, region_code)
    """)
    output.print("OK dim_region")

    # 组织维度
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS dim_organization (
        organization_key String,
        organization_code String,
        organization_name String,
        parent_key Nullable(String),
        org_level Int32,
        is_leaf UInt8,
        PRIMARY KEY (organization_key)
    ) ENGINE = MergeTree()
    ORDER BY (organization_key, organization_code)
    """)
    output.print("OK dim_organization")

    # 项目状态维度
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS dim_project_status (
        project_status_key String,
        project_status_code String,
        project_status_name String,
        status_order Int32,
        is_active UInt8,
        PRIMARY KEY (project_status_key)
    ) ENGINE = MergeTree()
    ORDER BY (project_status_key, status_order)
    """)
    output.print("OK dim_project_status")

    # 合同状态维度
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS dim_contract_status (
        contract_status_key String,
        contract_status_code String,
        contract_status_name String,
        status_order Int32,
        is_active UInt8,
        PRIMARY KEY (contract_status_key)
    ) ENGINE = MergeTree()
    ORDER BY (contract_status_key, status_order)
    """)
    output.print("OK dim_contract_status")

    # 项目类别维度
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS dim_project_category (
        project_category_key String,
        category_type String,
        category_code String,
        category_name String,
        parent_key Nullable(String),
        level Int32,
        is_leaf UInt8,
        PRIMARY KEY (project_category_key)
    ) ENGINE = MergeTree()
    ORDER BY (project_category_key, category_code)
    """)
    output.print("OK dim_project_category")

    # 经营模式维度
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS dim_cooperation (
        cooperation_key String,
        cooperation_code String,
        cooperation_name String,
        is_active UInt8,
        PRIMARY KEY (cooperation_key)
    ) ENGINE = MergeTree()
    ORDER BY (cooperation_key, cooperation_code)
    """)
    output.print("OK dim_cooperation")

    # 客户维度
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS dim_client (
        client_key String,
        client_code String,
        client_name String,
        client_type String,
        credit_level String,
        region_key String,
        is_key_client UInt8,
        PRIMARY KEY (client_key)
    ) ENGINE = MergeTree()
    ORDER BY (client_key, client_code)
    """)
    output.print("OK dim_client")

    # 合同类型维度
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS dim_contract_type (
        contract_type_key String,
        contract_type_code String,
        contract_type_name String,
        description String,
        PRIMARY KEY (contract_type_key)
    ) ENGINE = MergeTree()
    ORDER BY (contract_type_key, contract_type_code)
    """)
    output.print("OK dim_contract_type")

    # 风险等级维度
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS dim_risk_level (
        risk_level_key String,
        risk_level_code String,
        risk_level_name String,
        risk_level_value Int32,
        threshold_min Decimal(5,2),
        threshold_max Decimal(5,2),
        PRIMARY KEY (risk_level_key)
    ) ENGINE = MergeTree()
    ORDER BY (risk_level_key, risk_level_value)
    """)
    output.print("OK dim_risk_level")

    # 项目成本事实表
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS fact_project_cost (
        cost_id String,
        date_key Int32,
        calendar_date Date,
        project_key String,
        cost_subject_key String,
        subject_code String,
        subject_name String,
        subject_level Int32,
        cost_amount Decimal(18,2),
        cost_type String,
        contract_key String,
        region_key String,
        organization_key String,
        PRIMARY KEY (cost_id)
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(calendar_date)
    ORDER BY (cost_id, date_key, project_key, cost_subject_key)
    """)
    output.print("OK fact_project_cost")

    # 项目产值事实表
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS fact_project_output (
        output_id String,
        date_key Int32,
        calendar_date Date,
        project_key String,
        output_type String,
        output_amount Decimal(18,2),
        confirmation_status String,
        contract_key String,
        region_key String,
        organization_key String,
        PRIMARY KEY (output_id)
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(calendar_date)
    ORDER BY (output_id, date_key, project_key, output_type)
    """)
    output.print("OK fact_project_output")

    # 付款事实表
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS fact_payment (
        payment_id String,
        date_key Int32,
        calendar_date Date,
        project_key String,
        contract_key String,
        payment_amount Decimal(18,2),
        payment_type String,
        payment_status String,
        supplier_key String,
        region_key String,
        organization_key String,
        PRIMARY KEY (payment_id)
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(calendar_date)
    ORDER BY (payment_id, date_key, project_key, contract_key)
    """)
    output.print("OK fact_payment")

    # 应收账款事实表
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS fact_receivable (
        receivable_id String,
        date_key Int32,
        calendar_date Date,
        project_key String,
        contract_key String,
        receivable_amount Decimal(18,2),
        received_amount Decimal(18,2),
        outstanding_amount Decimal(18,2),
        receivable_status String,
        due_date Date,
        region_key String,
        organization_key String,
        PRIMARY KEY (receivable_id)
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(calendar_date)
    ORDER BY (receivable_id, date_key, project_key, contract_key)
    """)
    output.print("OK fact_receivable")

    # 现金流事实表
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS fact_cash_flow (
        cash_flow_id String,
        date_key Int32,
        calendar_date Date,
        project_key String,
        cash_flow_type String,
        cash_flow_amount Decimal(18,2),
        cash_flow_category String,
        approval_status String,
        region_key String,
        organization_key String,
        PRIMARY KEY (cash_flow_id)
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(calendar_date)
    ORDER BY (cash_flow_id, date_key, project_key, cash_flow_type)
    """)
    output.print("OK fact_cash_flow")

    # 风险事实表
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS fact_risk (
        risk_id String,
        date_key Int32,
        calendar_date Date,
        project_key String,
        risk_type String,
        risk_level_key String,
        risk_value Decimal(5,2),
        region_key String,
        organization_key String,
        PRIMARY KEY (risk_id)
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(calendar_date)
    ORDER BY (risk_id, date_key, project_key, risk_type)
    """)
    output.print("OK fact_risk")

    # 变更签证事实表
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS fact_change_order (
        change_id String,
        date_key Int32,
        calendar_date Date,
        project_key String,
        contract_key String,
        change_type String,
        change_amount Decimal(18,2),
        approval_status String,
        region_key String,
        organization_key String,
        PRIMARY KEY (change_id)
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(calendar_date)
    ORDER BY (change_id, date_key, project_key, change_type)
    """)
    output.print("OK fact_change_order")

    # 索赔事实表
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS fact_claim (
        claim_id String,
        date_key Int32,
        calendar_date Date,
        project_key String,
        contract_key String,
        claim_type String,
        claim_amount Decimal(18,2),
        approved_amount Decimal(18,2),
        approval_status String,
        region_key String,
        organization_key String,
        PRIMARY KEY (claim_id)
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(calendar_date)
    ORDER BY (claim_id, date_key, project_key, claim_type)
    """)
    output.print("OK fact_claim")

    # 项目指标事实表
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS fact_project_indicator (
        indicator_id String,
        date_key Int32,
        calendar_date Date,
        project_key String,
        indicator_name String,
        indicator_value Decimal(18,4),
        indicator_unit String,
        quality_level String,
        region_key String,
        organization_key String,
        PRIMARY KEY (indicator_id)
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(calendar_date)
    ORDER BY (indicator_id, date_key, project_key, indicator_name)
    """)
    output.print("OK fact_project_indicator")

    # 业务规则事实表
    s.sql.execute("""
    CREATE TABLE IF NOT EXISTS fact_business_rules (
        rule_id String,
        rule_name String,
        rule_type String,
        formula String,
        description String,
        severity String,
        threshold String,
        PRIMARY KEY (rule_id)
    ) ENGINE = MergeTree()
    ORDER BY (rule_id, rule_type)
    """)
    output.print("OK fact_business_rules")

    output.print("✅ 24张表创建完成")

    # ==================== 2. 表元数据注册 ====================
    output.print("\n[2/5] 注册表到空间...")

    TABLE_REGISTRY = {
        "dim_date": {
            "display_name": "时间维度表",
            "description": "全空间共享日历维度",
            "columns": [
                {"name": "date_key", "display_name": "日期键", "description": "YYYYMMDD格式，主键"},
                {"name": "calendar_date", "display_name": "自然日"},
                {"name": "year", "display_name": "公历年"},
                {"name": "quarter", "display_name": "季度"},
                {"name": "month", "display_name": "月"},
                {"name": "week_of_year", "display_name": "周"},
                {"name": "day_of_week", "display_name": "星期"},
                {"name": "is_weekend", "display_name": "是否周末"},
                {"name": "year_month", "display_name": "年月"},
                {"name": "fiscal_year", "display_name": "会计年度"},
                {"name": "fiscal_period", "display_name": "会计期间"},
            ]
        },
        "dim_project": {
            "display_name": "项目主数据",
            "description": "建筑工程项目主数据",
            "columns": [
                {"name": "project_key", "display_name": "项目唯一标识", "description": "主键"},
                {"name": "project_code", "display_name": "项目编码"},
                {"name": "project_name", "display_name": "项目名称"},
                {"name": "project_type", "display_name": "项目类型"},
                {"name": "project_category", "display_name": "项目类别"},
                {"name": "business_model", "display_name": "经营模式"},
                {"name": "contract_amount", "display_name": "合同金额"},
                {"name": "management_fee_rate", "display_name": "管理费率(%)"},
                {"name": "project_status", "display_name": "项目状态"},
                {"name": "start_date", "display_name": "开工日期"},
                {"name": "end_date", "display_name": "竣工日期"},
                {"name": "region_key", "display_name": "地区标识", "description": "关联dim_region"},
                {"name": "organization_key", "display_name": "组织标识", "description": "关联dim_organization"},
                {"name": "project_manager", "display_name": "项目经理"},
                {"name": "is_key_client", "display_name": "是否大客户项目"},
                {"name": "is_new_increment", "display_name": "是否增量项目"},
            ]
        },
        "dim_contract": {
            "display_name": "合同主数据",
            "description": "合同信息主数据",
            "columns": [
                {"name": "contract_key", "display_name": "合同唯一标识", "description": "主键"},
                {"name": "contract_code", "display_name": "合同编码"},
                {"name": "contract_name", "display_name": "合同名称"},
                {"name": "project_key", "display_name": "项目唯一标识", "description": "关联dim_project"},
                {"name": "contract_type", "display_name": "合同类型"},
                {"name": "contract_amount", "display_name": "合同金额"},
                {"name": "sign_date", "display_name": "签订日期"},
                {"name": "contract_status", "display_name": "合同状态"},
                {"name": "owner_key", "display_name": "业主标识", "description": "关联dim_owner"},
            ]
        },
        "dim_owner": {
            "display_name": "业主维度",
            "description": "业主信息维度",
            "columns": [
                {"name": "owner_key", "display_name": "业主标识", "description": "主键"},
                {"name": "owner_code", "display_name": "业主编码"},
                {"name": "owner_name", "display_name": "业主名称"},
                {"name": "owner_type", "display_name": "业主类型"},
                {"name": "credit_level", "display_name": "信用等级"},
                {"name": "region_key", "display_name": "地区标识", "description": "关联dim_region"},
            ]
        },
        "dim_cost_subject": {
            "display_name": "成本科目维度",
            "description": "成本科目层级维度",
            "columns": [
                {"name": "cost_subject_key", "display_name": "科目标识", "description": "主键"},
                {"name": "subject_code", "display_name": "科目编码"},
                {"name": "subject_name", "display_name": "科目名称"},
                {"name": "subject_level", "display_name": "科目层级"},
                {"name": "parent_key", "display_name": "上级科目标识", "description": "自关联"},
                {"name": "subject_type", "display_name": "科目类型"},
                {"name": "is_leaf", "display_name": "是否末级"},
            ]
        },
        "dim_region": {
            "display_name": "地区维度",
            "description": "地区层级维度",
            "columns": [
                {"name": "region_key", "display_name": "地区标识", "description": "主键"},
                {"name": "region_code", "display_name": "地区编码"},
                {"name": "region_name", "display_name": "地区名称"},
                {"name": "parent_key", "display_name": "上级地区标识", "description": "自关联"},
                {"name": "region_level", "display_name": "地区层级"},
                {"name": "is_leaf", "display_name": "是否末级"},
            ]
        },
        "dim_organization": {
            "display_name": "组织维度",
            "description": "组织层级维度",
            "columns": [
                {"name": "organization_key", "display_name": "组织标识", "description": "主键"},
                {"name": "organization_code", "display_name": "组织编码"},
                {"name": "organization_name", "display_name": "组织名称"},
                {"name": "parent_key", "display_name": "上级组织标识", "description": "自关联"},
                {"name": "org_level", "display_name": "组织层级"},
                {"name": "is_leaf", "display_name": "是否末级"},
            ]
        },
        "dim_project_status": {
            "display_name": "项目状态维度",
            "description": "项目状态维度",
            "columns": [
                {"name": "project_status_key", "display_name": "状态标识", "description": "主键"},
                {"name": "project_status_code", "display_name": "状态编码"},
                {"name": "project_status_name", "display_name": "状态名称"},
                {"name": "status_order", "display_name": "状态顺序"},
                {"name": "is_active", "display_name": "是否活跃状态"},
            ]
        },
        "dim_contract_status": {
            "display_name": "合同状态维度",
            "description": "合同状态维度",
            "columns": [
                {"name": "contract_status_key", "display_name": "状态标识", "description": "主键"},
                {"name": "contract_status_code", "display_name": "状态编码"},
                {"name": "contract_status_name", "display_name": "状态名称"},
                {"name": "status_order", "display_name": "状态顺序"},
                {"name": "is_active", "display_name": "是否活跃状态"},
            ]
        },
        "dim_project_category": {
            "display_name": "项目类别维度",
            "description": "项目类别层级维度",
            "columns": [
                {"name": "project_category_key", "display_name": "类别标识", "description": "主键"},
                {"name": "category_type", "display_name": "类别类型"},
                {"name": "category_code", "display_name": "类别编码"},
                {"name": "category_name", "display_name": "类别名称"},
                {"name": "parent_key", "display_name": "上级类别标识", "description": "自关联"},
                {"name": "level", "display_name": "层级"},
                {"name": "is_leaf", "display_name": "是否末级"},
            ]
        },
        "dim_cooperation": {
            "display_name": "经营模式维度",
            "description": "经营模式维度",
            "columns": [
                {"name": "cooperation_key", "display_name": "经营模式标识", "description": "主键"},
                {"name": "cooperation_code", "display_name": "经营模式编码"},
                {"name": "cooperation_name", "display_name": "经营模式名称"},
                {"name": "is_active", "display_name": "是否启用"},
            ]
        },
        "dim_client": {
            "display_name": "客户维度",
            "description": "客户信息维度",
            "columns": [
                {"name": "client_key", "display_name": "客户标识", "description": "主键"},
                {"name": "client_code", "display_name": "客户编码"},
                {"name": "client_name", "display_name": "客户名称"},
                {"name": "client_type", "display_name": "客户类型"},
                {"name": "credit_level", "display_name": "信用等级"},
                {"name": "region_key", "display_name": "地区标识", "description": "关联dim_region"},
                {"name": "is_key_client", "display_name": "是否大客户"},
            ]
        },
        "dim_contract_type": {
            "display_name": "合同类型维度",
            "description": "合同类型维度",
            "columns": [
                {"name": "contract_type_key", "display_name": "合同类型标识", "description": "主键"},
                {"name": "contract_type_code", "display_name": "合同类型编码"},
                {"name": "contract_type_name", "display_name": "合同类型名称"},
                {"name": "description", "display_name": "说明"},
            ]
        },
        "dim_risk_level": {
            "display_name": "风险等级维度",
            "description": "风险等级维度",
            "columns": [
                {"name": "risk_level_key", "display_name": "风险等级标识", "description": "主键"},
                {"name": "risk_level_code", "display_name": "风险等级编码"},
                {"name": "risk_level_name", "display_name": "风险等级名称"},
                {"name": "risk_level_value", "display_name": "风险等级值"},
                {"name": "threshold_min", "display_name": "阈值下限(%)"},
                {"name": "threshold_max", "display_name": "阈值上限(%)"},
            ]
        },
        "fact_project_cost": {
            "display_name": "项目成本事实表",
            "description": "项目成本记录",
            "columns": [
                {"name": "cost_id", "display_name": "成本记录唯一标识", "description": "主键"},
                {"name": "date_key", "display_name": "日期键", "description": "关联dim_date"},
                {"name": "calendar_date", "display_name": "业务日期"},
                {"name": "project_key", "display_name": "项目唯一标识", "description": "关联dim_project"},
                {"name": "cost_subject_key", "display_name": "成本科目标识", "description": "关联dim_cost_subject"},
                {"name": "subject_code", "display_name": "科目编码"},
                {"name": "subject_name", "display_name": "科目名称"},
                {"name": "subject_level", "display_name": "科目层级"},
                {"name": "cost_amount", "display_name": "成本金额"},
                {"name": "cost_type", "display_name": "成本类型"},
                {"name": "contract_key", "display_name": "合同唯一标识", "description": "关联dim_contract"},
                {"name": "region_key", "display_name": "地区标识", "description": "关联dim_region"},
                {"name": "organization_key", "display_name": "组织标识", "description": "关联dim_organization"},
            ]
        },
        "fact_project_output": {
            "display_name": "项目产值事实表",
            "description": "项目产值记录",
            "columns": [
                {"name": "output_id", "display_name": "产值记录唯一标识", "description": "主键"},
                {"name": "date_key", "display_name": "日期键", "description": "关联dim_date"},
                {"name": "calendar_date", "display_name": "业务日期"},
                {"name": "project_key", "display_name": "项目唯一标识", "description": "关联dim_project"},
                {"name": "output_type", "display_name": "产值类型"},
                {"name": "output_amount", "display_name": "产值金额"},
                {"name": "confirmation_status", "display_name": "确认状态"},
                {"name": "contract_key", "display_name": "合同唯一标识", "description": "关联dim_contract"},
                {"name": "region_key", "display_name": "地区标识", "description": "关联dim_region"},
                {"name": "organization_key", "display_name": "组织标识", "description": "关联dim_organization"},
            ]
        },
        "fact_payment": {
            "display_name": "付款事实表",
            "description": "付款记录",
            "columns": [
                {"name": "payment_id", "display_name": "付款记录唯一标识", "description": "主键"},
                {"name": "date_key", "display_name": "日期键", "description": "关联dim_date"},
                {"name": "calendar_date", "display_name": "业务日期"},
                {"name": "project_key", "display_name": "项目唯一标识", "description": "关联dim_project"},
                {"name": "contract_key", "display_name": "合同唯一标识", "description": "关联dim_contract"},
                {"name": "payment_amount", "display_name": "付款金额"},
                {"name": "payment_type", "display_name": "付款类型"},
                {"name": "payment_status", "display_name": "付款状态"},
                {"name": "supplier_key", "display_name": "供应商标识"},
                {"name": "region_key", "display_name": "地区标识", "description": "关联dim_region"},
                {"name": "organization_key", "display_name": "组织标识", "description": "关联dim_organization"},
            ]
        },
        "fact_receivable": {
            "display_name": "应收账款事实表",
            "description": "应收账款记录",
            "columns": [
                {"name": "receivable_id", "display_name": "应收记录唯一标识", "description": "主键"},
                {"name": "date_key", "display_name": "日期键", "description": "关联dim_date"},
                {"name": "calendar_date", "display_name": "业务日期"},
                {"name": "project_key", "display_name": "项目唯一标识", "description": "关联dim_project"},
                {"name": "contract_key", "display_name": "合同唯一标识", "description": "关联dim_contract"},
                {"name": "receivable_amount", "display_name": "应收金额"},
                {"name": "received_amount", "display_name": "已收金额"},
                {"name": "outstanding_amount", "display_name": "未收金额"},
                {"name": "receivable_status", "display_name": "应收状态"},
                {"name": "due_date", "display_name": "到期日期"},
                {"name": "region_key", "display_name": "地区标识", "description": "关联dim_region"},
                {"name": "organization_key", "display_name": "组织标识", "description": "关联dim_organization"},
            ]
        },
        "fact_cash_flow": {
            "display_name": "现金流事实表",
            "description": "现金流记录",
            "columns": [
                {"name": "cash_flow_id", "display_name": "现金流记录唯一标识", "description": "主键"},
                {"name": "date_key", "display_name": "日期键", "description": "关联dim_date"},
                {"name": "calendar_date", "display_name": "业务日期"},
                {"name": "project_key", "display_name": "项目唯一标识", "description": "关联dim_project"},
                {"name": "cash_flow_type", "display_name": "现金流类型"},
                {"name": "cash_flow_amount", "display_name": "现金流金额"},
                {"name": "cash_flow_category", "display_name": "现金流分类"},
                {"name": "approval_status", "display_name": "审批状态"},
                {"name": "region_key", "display_name": "地区标识", "description": "关联dim_region"},
                {"name": "organization_key", "display_name": "组织标识", "description": "关联dim_organization"},
            ]
        },
        "fact_risk": {
            "display_name": "风险事实表",
            "description": "风险记录",
            "columns": [
                {"name": "risk_id", "display_name": "风险记录唯一标识", "description": "主键"},
                {"name": "date_key", "display_name": "日期键", "description": "关联dim_date"},
                {"name": "calendar_date", "display_name": "业务日期"},
                {"name": "project_key", "display_name": "项目唯一标识", "description": "关联dim_project"},
                {"name": "risk_type", "display_name": "风险类型"},
                {"name": "risk_level_key", "display_name": "风险等级标识", "description": "关联dim_risk_level"},
                {"name": "risk_value", "display_name": "风险值(%)"},
                {"name": "region_key", "display_name": "地区标识", "description": "关联dim_region"},
                {"name": "organization_key", "display_name": "组织标识", "description": "关联dim_organization"},
            ]
        },
        "fact_change_order": {
            "display_name": "变更签证事实表",
            "description": "变更签证记录",
            "columns": [
                {"name": "change_id", "display_name": "变更记录唯一标识", "description": "主键"},
                {"name": "date_key", "display_name": "日期键", "description": "关联dim_date"},
                {"name": "calendar_date", "display_name": "业务日期"},
                {"name": "project_key", "display_name": "项目唯一标识", "description": "关联dim_project"},
                {"name": "contract_key", "display_name": "合同唯一标识", "description": "关联dim_contract"},
                {"name": "change_type", "display_name": "变更类型"},
                {"name": "change_amount", "display_name": "变更金额"},
                {"name": "approval_status", "display_name": "审批状态"},
                {"name": "region_key", "display_name": "地区标识", "description": "关联dim_region"},
                {"name": "organization_key", "display_name": "组织标识", "description": "关联dim_organization"},
            ]
        },
        "fact_claim": {
            "display_name": "索赔事实表",
            "description": "索赔记录",
            "columns": [
                {"name": "claim_id", "display_name": "索赔记录唯一标识", "description": "主键"},
                {"name": "date_key", "display_name": "日期键", "description": "关联dim_date"},
                {"name": "calendar_date", "display_name": "业务日期"},
                {"name": "project_key", "display_name": "项目唯一标识", "description": "关联dim_project"},
                {"name": "contract_key", "display_name": "合同唯一标识", "description": "关联dim_contract"},
                {"name": "claim_type", "display_name": "索赔类型"},
                {"name": "claim_amount", "display_name": "索赔金额"},
                {"name": "approved_amount", "display_name": "批准金额"},
                {"name": "approval_status", "display_name": "审批状态"},
                {"name": "region_key", "display_name": "地区标识", "description": "关联dim_region"},
                {"name": "organization_key", "display_name": "组织标识", "description": "关联dim_organization"},
            ]
        },
        "fact_project_indicator": {
            "display_name": "项目指标事实表",
            "description": "项目指标记录",
            "columns": [
                {"name": "indicator_id", "display_name": "指标记录唯一标识", "description": "主键"},
                {"name": "date_key", "display_name": "日期键", "description": "关联dim_date"},
                {"name": "calendar_date", "display_name": "业务日期"},
                {"name": "project_key", "display_name": "项目唯一标识", "description": "关联dim_project"},
                {"name": "indicator_name", "display_name": "指标名称"},
                {"name": "indicator_value", "display_name": "指标值"},
                {"name": "indicator_unit", "display_name": "指标单位"},
                {"name": "quality_level", "display_name": "品质等级"},
                {"name": "region_key", "display_name": "地区标识", "description": "关联dim_region"},
                {"name": "organization_key", "display_name": "组织标识", "description": "关联dim_organization"},
            ]
        },
    }

    for tbl_name, meta in TABLE_REGISTRY.items():
        s.tables.register_with_meta(
            table_name=tbl_name,
            display_name=meta["display_name"],
            description=meta.get("description"),
            columns=meta["columns"],
            force_column_meta=True,
        )
        output.print(f"OK {tbl_name}")

    output.print("✅ 23张表元数据注册完成")

    # ==================== 3. 注册表间关系 ====================
    output.print("\n[3/5] 注册表间关系...")

    # 时间关联
    s.tables.add_relationship(
        from_table="fact_project_cost",
        to_table="dim_date",
        join_sql="fact_project_cost.date_key = dim_date.date_key",
        join_keys=[{"from": "date_key", "to": "date_key"}],
        relationship_type="many_to_one",
        description="成本→日历",
    )

    s.tables.add_relationship(
        from_table="fact_project_output",
        to_table="dim_date",
        join_sql="fact_project_output.date_key = dim_date.date_key",
        join_keys=[{"from": "date_key", "to": "date_key"}],
        relationship_type="many_to_one",
        description="产值→日历",
    )

    s.tables.add_relationship(
        from_table="fact_payment",
        to_table="dim_date",
        join_sql="fact_payment.date_key = dim_date.date_key",
        join_keys=[{"from": "date_key", "to": "date_key"}],
        relationship_type="many_to_one",
        description="付款→日历",
    )

    s.tables.add_relationship(
        from_table="fact_receivable",
        to_table="dim_date",
        join_sql="fact_receivable.date_key = dim_date.date_key",
        join_keys=[{"from": "date_key", "to": "date_key"}],
        relationship_type="many_to_one",
        description="应收→日历",
    )

    s.tables.add_relationship(
        from_table="fact_cash_flow",
        to_table="dim_date",
        join_sql="fact_cash_flow.date_key = dim_date.date_key",
        join_keys=[{"from": "date_key", "to": "date_key"}],
        relationship_type="many_to_one",
        description="现金流→日历",
    )

    s.tables.add_relationship(
        from_table="fact_risk",
        to_table="dim_date",
        join_sql="fact_risk.date_key = dim_date.date_key",
        join_keys=[{"from": "date_key", "to": "date_key"}],
        relationship_type="many_to_one",
        description="风险→日历",
    )

    s.tables.add_relationship(
        from_table="fact_change_order",
        to_table="dim_date",
        join_sql="fact_change_order.date_key = dim_date.date_key",
        join_keys=[{"from": "date_key", "to": "date_key"}],
        relationship_type="many_to_one",
        description="变更→日历",
    )

    s.tables.add_relationship(
        from_table="fact_claim",
        to_table="dim_date",
        join_sql="fact_claim.date_key = dim_date.date_key",
        join_keys=[{"from": "date_key", "to": "date_key"}],
        relationship_type="many_to_one",
        description="索赔→日历",
    )

    s.tables.add_relationship(
        from_table="fact_project_indicator",
        to_table="dim_date",
        join_sql="fact_project_indicator.date_key = dim_date.date_key",
        join_keys=[{"from": "date_key", "to": "date_key"}],
        relationship_type="many_to_one",
        description="指标→日历",
    )

    # 主数据关联
    s.tables.add_relationship(
        from_table="fact_project_cost",
        to_table="dim_project",
        join_sql="fact_project_cost.project_key = dim_project.project_key",
        join_keys=[{"from": "project_key", "to": "project_key"}],
        relationship_type="many_to_one",
        description="成本→项目",
    )

    s.tables.add_relationship(
        from_table="fact_project_output",
        to_table="dim_project",
        join_sql="fact_project_output.project_key = dim_project.project_key",
        join_keys=[{"from": "project_key", "to": "project_key"}],
        relationship_type="many_to_one",
        description="产值→项目",
    )

    s.tables.add_relationship(
        from_table="fact_payment",
        to_table="dim_project",
        join_sql="fact_payment.project_key = dim_project.project_key",
        join_keys=[{"from": "project_key", "to": "project_key"}],
        relationship_type="many_to_one",
        description="付款→项目",
    )

    s.tables.add_relationship(
        from_table="fact_receivable",
        to_table="dim_project",
        join_sql="fact_receivable.project_key = dim_project.project_key",
        join_keys=[{"from": "project_key", "to": "project_key"}],
        relationship_type="many_to_one",
        description="应收→项目",
    )

    s.tables.add_relationship(
        from_table="fact_cash_flow",
        to_table="dim_project",
        join_sql="fact_cash_flow.project_key = dim_project.project_key",
        join_keys=[{"from": "project_key", "to": "project_key"}],
        relationship_type="many_to_one",
        description="现金流→项目",
    )

    s.tables.add_relationship(
        from_table="fact_risk",
        to_table="dim_project",
        join_sql="fact_risk.project_key = dim_project.project_key",
        join_keys=[{"from": "project_key", "to": "project_key"}],
        relationship_type="many_to_one",
        description="风险→项目",
    )

    s.tables.add_relationship(
        from_table="fact_change_order",
        to_table="dim_project",
        join_sql="fact_change_order.project_key = dim_project.project_key",
        join_keys=[{"from": "project_key", "to": "project_key"}],
        relationship_type="many_to_one",
        description="变更→项目",
    )

    s.tables.add_relationship(
        from_table="fact_claim",
        to_table="dim_project",
        join_sql="fact_claim.project_key = dim_project.project_key",
        join_keys=[{"from": "project_key", "to": "project_key"}],
        relationship_type="many_to_one",
        description="索赔→项目",
    )

    s.tables.add_relationship(
        from_table="fact_project_indicator",
        to_table="dim_project",
        join_sql="fact_project_indicator.project_key = dim_project.project_key",
        join_keys=[{"from": "project_key", "to": "project_key"}],
        relationship_type="many_to_one",
        description="指标→项目",
    )

    s.tables.add_relationship(
        from_table="dim_contract",
        to_table="dim_project",
        join_sql="dim_contract.project_key = dim_project.project_key",
        join_keys=[{"from": "project_key", "to": "project_key"}],
        relationship_type="many_to_one",
        description="合同→项目",
    )

    s.tables.add_relationship(
        from_table="fact_project_cost",
        to_table="dim_cost_subject",
        join_sql="fact_project_cost.cost_subject_key = dim_cost_subject.cost_subject_key",
        join_keys=[{"from": "cost_subject_key", "to": "cost_subject_key"}],
        relationship_type="many_to_one",
        description="成本→科目",
    )

    s.tables.add_relationship(
        from_table="fact_project_cost",
        to_table="dim_contract",
        join_sql="fact_project_cost.contract_key = dim_contract.contract_key",
        join_keys=[{"from": "contract_key", "to": "contract_key"}],
        relationship_type="many_to_one",
        description="成本→合同",
    )

    s.tables.add_relationship(
        from_table="fact_payment",
        to_table="dim_contract",
        join_sql="fact_payment.contract_key = dim_contract.contract_key",
        join_keys=[{"from": "contract_key", "to": "contract_key"}],
        relationship_type="many_to_one",
        description="付款→合同",
    )

    s.tables.add_relationship(
        from_table="fact_receivable",
        to_table="dim_contract",
        join_sql="fact_receivable.contract_key = dim_contract.contract_key",
        join_keys=[{"from": "contract_key", "to": "contract_key"}],
        relationship_type="many_to_one",
        description="应收→合同",
    )

    s.tables.add_relationship(
        from_table="fact_change_order",
        to_table="dim_contract",
        join_sql="fact_change_order.contract_key = dim_contract.contract_key",
        join_keys=[{"from": "contract_key", "to": "contract_key"}],
        relationship_type="many_to_one",
        description="变更→合同",
    )

    s.tables.add_relationship(
        from_table="fact_claim",
        to_table="dim_contract",
        join_sql="fact_claim.contract_key = dim_contract.contract_key",
        join_keys=[{"from": "contract_key", "to": "contract_key"}],
        relationship_type="many_to_one",
        description="索赔→合同",
    )

    # 层级自关联
    s.tables.add_relationship(
        from_table="dim_cost_subject",
        to_table="dim_cost_subject",
        join_sql="dim_cost_subject.parent_key = dim_cost_subject.cost_subject_key",
        join_keys=[{"from": "parent_key", "to": "cost_subject_key"}],
        relationship_type="many_to_one",
        description="科目层级",
    )

    s.tables.add_relationship(
        from_table="dim_project_category",
        to_table="dim_project_category",
        join_sql="dim_project_category.parent_key = dim_project_category.project_category_key",
        join_keys=[{"from": "parent_key", "to": "project_category_key"}],
        relationship_type="many_to_one",
        description="类别层级",
    )

    s.tables.add_relationship(
        from_table="dim_region",
        to_table="dim_region",
        join_sql="dim_region.parent_key = dim_region.region_key",
        join_keys=[{"from": "parent_key", "to": "region_key"}],
        relationship_type="many_to_one",
        description="地区层级",
    )

    s.tables.add_relationship(
        from_table="dim_organization",
        to_table="dim_organization",
        join_sql="dim_organization.parent_key = dim_organization.organization_key",
        join_keys=[{"from": "parent_key", "to": "organization_key"}],
        relationship_type="many_to_one",
        description="组织层级",
    )

    output.print("✅ 29条表间关系注册完成")

    # ==================== 4. 注册Cube ====================
    output.print("\n[4/5] 注册Cube...")

    # ProjectCostCube
    s.register_cube(
        name="ProjectCostCube",
        table="fact_project_cost",
        title="项目成本Cube",
        measures=[
            {"name": "cost_amount_total", "col": "cost_amount", "agg": "sum", "title": "成本金额合计"},
            {"name": "cost_count", "col": "cost_id", "agg": "count", "title": "成本记录数"},
        ],
        dimensions=[
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目标识"},
            {"name": "project_code", "col": "project_code", "type": "string", "title": "项目编码"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
            {"name": "cost_subject_key", "col": "cost_subject_key", "type": "string", "title": "成本科目标识"},
            {"name": "subject_code", "col": "subject_code", "type": "string", "title": "科目编码"},
            {"name": "subject_name", "col": "subject_name", "type": "string", "title": "科目名称"},
            {"name": "cost_type", "col": "cost_type", "type": "string", "title": "成本类型"},
            {"name": "contract_key", "col": "contract_key", "type": "string", "title": "合同标识"},
            {"name": "region_key", "col": "region_key", "type": "string", "title": "地区标识"},
            {"name": "organization_key", "col": "organization_key", "type": "string", "title": "组织标识"},
        ],
    )
    output.print("OK ProjectCostCube")

    # ProjectOutputCube
    s.register_cube(
        name="ProjectOutputCube",
        table="fact_project_output",
        title="项目产值Cube",
        measures=[
            {"name": "output_amount_total", "col": "output_amount", "agg": "sum", "title": "产值金额合计"},
            {"name": "output_count", "col": "output_id", "agg": "count", "title": "产值记录数"},
        ],
        dimensions=[
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目标识"},
            {"name": "project_code", "col": "project_code", "type": "string", "title": "项目编码"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
            {"name": "output_type", "col": "output_type", "type": "string", "title": "产值类型"},
            {"name": "confirmation_status", "col": "confirmation_status", "type": "string", "title": "确认状态"},
            {"name": "contract_key", "col": "contract_key", "type": "string", "title": "合同标识"},
            {"name": "region_key", "col": "region_key", "type": "string", "title": "地区标识"},
            {"name": "organization_key", "col": "organization_key", "type": "string", "title": "组织标识"},
        ],
    )
    output.print("OK ProjectOutputCube")

    # PaymentCube
    s.register_cube(
        name="PaymentCube",
        table="fact_payment",
        title="付款Cube",
        measures=[
            {"name": "payment_amount_total", "col": "payment_amount", "agg": "sum", "title": "付款金额合计"},
            {"name": "payment_count", "col": "payment_id", "agg": "count", "title": "付款记录数"},
        ],
        dimensions=[
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目标识"},
            {"name": "project_code", "col": "project_code", "type": "string", "title": "项目编码"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
            {"name": "contract_key", "col": "contract_key", "type": "string", "title": "合同标识"},
            {"name": "payment_type", "col": "payment_type", "type": "string", "title": "付款类型"},
            {"name": "payment_status", "col": "payment_status", "type": "string", "title": "付款状态"},
            {"name": "region_key", "col": "region_key", "type": "string", "title": "地区标识"},
            {"name": "organization_key", "col": "organization_key", "type": "string", "title": "组织标识"},
        ],
    )
    output.print("OK PaymentCube")

    # ReceivableCube
    s.register_cube(
        name="ReceivableCube",
        table="fact_receivable",
        title="应收账款Cube",
        measures=[
            {"name": "receivable_amount_total", "col": "receivable_amount", "agg": "sum", "title": "应收金额合计"},
            {"name": "received_amount_total", "col": "received_amount", "agg": "sum", "title": "已收金额合计"},
            {"name": "outstanding_amount_total", "col": "outstanding_amount", "agg": "sum", "title": "未收金额合计"},
            {"name": "receivable_count", "col": "receivable_id", "agg": "count", "title": "应收记录数"},
        ],
        dimensions=[
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目标识"},
            {"name": "project_code", "col": "project_code", "type": "string", "title": "项目编码"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
            {"name": "contract_key", "col": "contract_key", "type": "string", "title": "合同标识"},
            {"name": "receivable_status", "col": "receivable_status", "type": "string", "title": "应收状态"},
            {"name": "region_key", "col": "region_key", "type": "string", "title": "地区标识"},
            {"name": "organization_key", "col": "organization_key", "type": "string", "title": "组织标识"},
        ],
    )
    output.print("OK ReceivableCube")

    # CashFlowCube
    s.register_cube(
        name="CashFlowCube",
        table="fact_cash_flow",
        title="现金流Cube",
        measures=[
            {"name": "cash_flow_amount_total", "col": "cash_flow_amount", "agg": "sum", "title": "现金流金额合计"},
            {"name": "cash_flow_count", "col": "cash_flow_id", "agg": "count", "title": "现金流记录数"},
        ],
        dimensions=[
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目标识"},
            {"name": "project_code", "col": "project_code", "type": "string", "title": "项目编码"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
            {"name": "cash_flow_type", "col": "cash_flow_type", "type": "string", "title": "现金流类型"},
            {"name": "cash_flow_category", "col": "cash_flow_category", "type": "string", "title": "现金流分类"},
            {"name": "approval_status", "col": "approval_status", "type": "string", "title": "审批状态"},
            {"name": "region_key", "col": "region_key", "type": "string", "title": "地区标识"},
            {"name": "organization_key", "col": "organization_key", "type": "string", "title": "组织标识"},
        ],
    )
    output.print("OK CashFlowCube")

    # RiskCube
    s.register_cube(
        name="RiskCube",
        table="fact_risk",
        title="风险Cube",
        measures=[
            {"name": "risk_count", "col": "risk_id", "agg": "count", "title": "风险记录数"},
            {"name": "risk_value_avg", "col": "risk_value", "agg": "avg", "title": "风险值均值"},
        ],
        dimensions=[
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目标识"},
            {"name": "project_code", "col": "project_code", "type": "string", "title": "项目编码"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
            {"name": "risk_type", "col": "risk_type", "type": "string", "title": "风险类型"},
            {"name": "risk_level_key", "col": "risk_level_key", "type": "string", "title": "风险等级标识"},
            {"name": "region_key", "col": "region_key", "type": "string", "title": "地区标识"},
            {"name": "organization_key", "col": "organization_key", "type": "string", "title": "组织标识"},
        ],
    )
    output.print("OK RiskCube")

    # ChangeOrderCube
    s.register_cube(
        name="ChangeOrderCube",
        table="fact_change_order",
        title="变更签证Cube",
        measures=[
            {"name": "change_amount_total", "col": "change_amount", "agg": "sum", "title": "变更金额合计"},
            {"name": "change_count", "col": "change_id", "agg": "count", "title": "变更记录数"},
        ],
        dimensions=[
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目标识"},
            {"name": "project_code", "col": "project_code", "type": "string", "title": "项目编码"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
            {"name": "contract_key", "col": "contract_key", "type": "string", "title": "合同标识"},
            {"name": "change_type", "col": "change_type", "type": "string", "title": "变更类型"},
            {"name": "approval_status", "col": "approval_status", "type": "string", "title": "审批状态"},
            {"name": "region_key", "col": "region_key", "type": "string", "title": "地区标识"},
            {"name": "organization_key", "col": "organization_key", "type": "string", "title": "组织标识"},
        ],
    )
    output.print("OK ChangeOrderCube")

    # ClaimCube
    s.register_cube(
        name="ClaimCube",
        table="fact_claim",
        title="索赔Cube",
        measures=[
            {"name": "claim_amount_total", "col": "claim_amount", "agg": "sum", "title": "索赔金额合计"},
            {"name": "approved_amount_total", "col": "approved_amount", "agg": "sum", "title": "批准金额合计"},
            {"name": "claim_count", "col": "claim_id", "agg": "count", "title": "索赔记录数"},
        ],
        dimensions=[
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目标识"},
            {"name": "project_code", "col": "project_code", "type": "string", "title": "项目编码"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
            {"name": "contract_key", "col": "contract_key", "type": "string", "title": "合同标识"},
            {"name": "claim_type", "col": "claim_type", "type": "string", "title": "索赔类型"},
            {"name": "approval_status", "col": "approval_status", "type": "string", "title": "审批状态"},
            {"name": "region_key", "col": "region_key", "type": "string", "title": "地区标识"},
            {"name": "organization_key", "col": "organization_key", "type": "string", "title": "组织标识"},
        ],
    )
    output.print("OK ClaimCube")

    # ProjectIndicatorCube
    s.register_cube(
        name="ProjectIndicatorCube",
        table="fact_project_indicator",
        title="项目指标Cube",
        measures=[
            {"name": "indicator_value_sum", "col": "indicator_value", "agg": "sum", "title": "指标值合计"},
            {"name": "indicator_value_avg", "col": "indicator_value", "agg": "avg", "title": "指标值均值"},
            {"name": "indicator_count", "col": "indicator_id", "agg": "count", "title": "指标记录数"},
        ],
        dimensions=[
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_key", "col": "project_key", "type": "string", "title": "项目标识"},
            {"name": "project_code", "col": "project_code", "type": "string", "title": "项目编码"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
            {"name": "indicator_name", "col": "indicator_name", "type": "string", "title": "指标名称"},
            {"name": "quality_level", "col": "quality_level", "type": "string", "title": "品质等级"},
            {"name": "region_key", "col": "region_key", "type": "string", "title": "地区标识"},
            {"name": "organization_key", "col": "organization_key", "type": "string", "title": "组织标识"},
        ],
    )
    output.print("OK ProjectIndicatorCube")

    output.print("✅ 9个Cube注册完成")

    # ==================== 5. 定义本体对象与链接 ====================
    output.print("\n[5/5] 定义本体对象类型...")

    # Project
    s.onto.define_object_type(
        code="Project",
        name="项目",
        description="工程项目主数据",
        category_347="主数据",
    )
    s.onto.bind_source("Project", "dazi_cube", config={"cube": "ProjectIndicatorCube"})
    s.onto.define_property("Project", "project_key", "项目唯一标识", semantic_role="dimension", qualified_name="ProjectIndicatorCube.project_key")
    s.onto.define_property("Project", "project_code", "项目编码", semantic_role="dimension", qualified_name="ProjectIndicatorCube.project_code")
    s.onto.define_property("Project", "project_name", "项目名称", semantic_role="dimension", qualified_name="ProjectIndicatorCube.project_name")
    s.onto.define_property("Project", "indicator_value_sum", "指标值合计", semantic_role="measure", qualified_name="ProjectIndicatorCube.indicator_value_sum")
    output.print("OK Project")

    # Contract
    s.onto.define_object_type(
        code="Contract",
        name="合同",
        description="工程合同主数据",
        category_347="主数据",
    )
    s.onto.bind_source("Contract", "dazi_cube", config={"cube": "PaymentCube"})
    s.onto.define_property("Contract", "contract_key", "合同唯一标识", semantic_role="dimension", qualified_name="PaymentCube.contract_key")
    s.onto.define_property("Contract", "payment_amount_total", "付款金额合计", semantic_role="measure", qualified_name="PaymentCube.payment_amount_total")
    output.print("OK Contract")

    # ProjectCost
    s.onto.define_object_type(
        code="ProjectCost",
        name="成本",
        description="项目成本事实",
        category_347="事务",
    )
    s.onto.bind_source("ProjectCost", "dazi_cube", config={"cube": "ProjectCostCube"})
    s.onto.define_property("ProjectCost", "date_key", "日期键", semantic_role="dimension", qualified_name="ProjectCostCube.date_key")
    s.onto.define_property("ProjectCost", "project_key", "项目标识", semantic_role="dimension", qualified_name="ProjectCostCube.project_key")
    s.onto.define_property("ProjectCost", "cost_amount_total", "成本金额合计", semantic_role="measure", qualified_name="ProjectCostCube.cost_amount_total")
    output.print("OK ProjectCost")

    # ProjectOutput
    s.onto.define_object_type(
        code="ProjectOutput",
        name="产值",
        description="项目产值事实",
        category_347="事务",
    )
    s.onto.bind_source("ProjectOutput", "dazi_cube", config={"cube": "ProjectOutputCube"})
    s.onto.define_property("ProjectOutput", "date_key", "日期键", semantic_role="dimension", qualified_name="ProjectOutputCube.date_key")
    s.onto.define_property("ProjectOutput", "project_key", "项目标识", semantic_role="dimension", qualified_name="ProjectOutputCube.project_key")
    s.onto.define_property("ProjectOutput", "output_amount_total", "产值金额合计", semantic_role="measure", qualified_name="ProjectOutputCube.output_amount_total")
    output.print("OK ProjectOutput")

    # Payment
    s.onto.define_object_type(
        code="Payment",
        name="付款",
        description="付款事实",
        category_347="事务",
    )
    s.onto.bind_source("Payment", "dazi_cube", config={"cube": "PaymentCube"})
    s.onto.define_property("Payment", "date_key", "日期键", semantic_role="dimension", qualified_name="PaymentCube.date_key")
    s.onto.define_property("Payment", "project_key", "项目标识", semantic_role="dimension", qualified_name="PaymentCube.project_key")
    s.onto.define_property("Payment", "payment_amount_total", "付款金额合计", semantic_role="measure", qualified_name="PaymentCube.payment_amount_total")
    output.print("OK Payment")

    # Receivable
    s.onto.define_object_type(
        code="Receivable",
        name="应收",
        description="应收账款事实",
        category_347="事务",
    )
    s.onto.bind_source("Receivable", "dazi_cube", config={"cube": "ReceivableCube"})
    s.onto.define_property("Receivable", "date_key", "日期键", semantic_role="dimension", qualified_name="ReceivableCube.date_key")
    s.onto.define_property("Receivable", "project_key", "项目标识", semantic_role="dimension", qualified_name="ReceivableCube.project_key")
    s.onto.define_property("Receivable", "receivable_amount_total", "应收金额合计", semantic_role="measure", qualified_name="ReceivableCube.receivable_amount_total")
    output.print("OK Receivable")

    # CashFlow
    s.onto.define_object_type(
        code="CashFlow",
        name="现金流",
        description="现金流事实",
        category_347="事务",
    )
    s.onto.bind_source("CashFlow", "dazi_cube", config={"cube": "CashFlowCube"})
    s.onto.define_property("CashFlow", "date_key", "日期键", semantic_role="dimension", qualified_name="CashFlowCube.date_key")
    s.onto.define_property("CashFlow", "project_key", "项目标识", semantic_role="dimension", qualified_name="CashFlowCube.project_key")
    s.onto.define_property("CashFlow", "cash_flow_amount_total", "现金流金额合计", semantic_role="measure", qualified_name="CashFlowCube.cash_flow_amount_total")
    output.print("OK CashFlow")

    # Risk
    s.onto.define_object_type(
        code="Risk",
        name="风险",
        description="风险事实",
        category_347="事务",
    )
    s.onto.bind_source("Risk", "dazi_cube", config={"cube": "RiskCube"})
    s.onto.define_property("Risk", "date_key", "日期键", semantic_role="dimension", qualified_name="RiskCube.date_key")
    s.onto.define_property("Risk", "project_key", "项目标识", semantic_role="dimension", qualified_name="RiskCube.project_key")
    s.onto.define_property("Risk", "risk_value_avg", "风险值均值", semantic_role="measure", qualified_name="RiskCube.risk_value_avg")
    output.print("OK Risk")

    # CostAnalysis (分析对象)
    s.onto.define_object_type(
        code="CostAnalysis",
        name="成本分析",
        description="成本多维度分析",
        category_347="分析",
    )
    s.onto.bind_source("CostAnalysis", "dazi_cube", config={"cube": "ProjectCostCube"})
    s.onto.define_property("CostAnalysis", "cost_amount_total", "成本合计", semantic_role="measure", qualified_name="ProjectCostCube.cost_amount_total")
    s.onto.define_property("CostAnalysis", "cost_count", "成本记录数", semantic_role="measure", qualified_name="ProjectCostCube.cost_count")
    output.print("OK CostAnalysis")

    # OutputAnalysis (分析对象)
    s.onto.define_object_type(
        code="OutputAnalysis",
        name="产值分析",
        description="产值多维度分析",
        category_347="分析",
    )
    s.onto.bind_source("OutputAnalysis", "dazi_cube", config={"cube": "ProjectOutputCube"})
    s.onto.define_property("OutputAnalysis", "output_amount_total", "产值合计", semantic_role="measure", qualified_name="ProjectOutputCube.output_amount_total")
    output.print("OK OutputAnalysis")

    output.print("\n✅ 11个本体对象类型定义完成")

    # ==================== 6. 定义本体链接类型 ====================
    output.print("\n[6/6] 定义本体链接类型...")

    # 项目→成本
    s.onto.define_link_type(code="ProjectHasCost", name="项目包含成本", from_object_type_code="Project", to_object_type_code="ProjectCost", category_347="归属关系")
    output.print("OK ProjectHasCost")

    # 项目→产值
    s.onto.define_link_type(code="ProjectHasOutput", name="项目包含产值", from_object_type_code="Project", to_object_type_code="ProjectOutput", category_347="归属关系")
    output.print("OK ProjectHasOutput")

    # 项目→合同
    s.onto.define_link_type(code="ProjectHasContract", name="项目包含合同", from_object_type_code="Project", to_object_type_code="Contract", category_347="归属关系")
    output.print("OK ProjectHasContract")

    # 项目→付款
    s.onto.define_link_type(code="ProjectHasPayment", name="项目包含付款", from_object_type_code="Project", to_object_type_code="Payment", category_347="归属关系")
    output.print("OK ProjectHasPayment")

    # 项目→应收
    s.onto.define_link_type(code="ProjectHasReceivable", name="项目包含应收", from_object_type_code="Project", to_object_type_code="Receivable", category_347="归属关系")
    output.print("OK ProjectHasReceivable")

    # 项目→现金流
    s.onto.define_link_type(code="ProjectHasCashFlow", name="项目包含现金流", from_object_type_code="Project", to_object_type_code="CashFlow", category_347="归属关系")
    output.print("OK ProjectHasCashFlow")

    # 项目→风险
    s.onto.define_link_type(code="ProjectHasRisk", name="项目包含风险", from_object_type_code="Project", to_object_type_code="Risk", category_347="归属关系")
    output.print("OK ProjectHasRisk")

    # 合同→成本
    s.onto.define_link_type(code="ContractRelatesCost", name="合同关联成本", from_object_type_code="Contract", to_object_type_code="ProjectCost", category_347="归属关系")
    output.print("OK ContractRelatesCost")

    # 合同→付款
    s.onto.define_link_type(code="ContractRelatesPayment", name="合同关联付款", from_object_type_code="Contract", to_object_type_code="Payment", category_347="归属关系")
    output.print("OK ContractRelatesPayment")

    # 合同→应收
    s.onto.define_link_type(code="ContractRelatesReceivable", name="合同关联应收", from_object_type_code="Contract", to_object_type_code="Receivable", category_347="归属关系")
    output.print("OK ContractRelatesReceivable")

    output.print("✅ 10个本体链接类型定义完成")

    output.print("\n=== 商务成本本体初始化完成 ===")

if __name__ == "__main__":
    main()