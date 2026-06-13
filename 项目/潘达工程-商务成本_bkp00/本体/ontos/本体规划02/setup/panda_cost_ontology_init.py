"""潘达工程商务成本本体初始化脚本 — space__panda_construction

初始化内容：
1. 创建物理表（dim_date + 9 维 + 6 事实）
2. 创建读模型 VIEW（ProjectCube / CostOutputComparisonCube）
3. 注册表到空间（TABLE_REGISTRY + register_with_meta）
4. 注册表间关系（25 条，含 fact→dim_date）
5. 注册 Cube（13 个）及 §5.6 派生度量
6. 定义对象类型（15 种）、属性、链接（24 种）
7. 同步指标引用

不含 apply_registry（分类在 category_mount 脚本）。

放置：项目/潘达工程-商务成本/本体/ontos/本体规划02/setup/panda_cost_ontology_init.py
规划对照：项目/潘达工程-商务成本/本体/ontos/本体规划02/plans/潘达工程商务成本管理本体方案.md
"""

import json

# 与规划 §2 对齐：display_name=侧栏显示名，description=业务说明
TABLE_REGISTRY = {
    "dim_date": {
        "display_name": "日期维表",
        "description": "全空间共享日历，事实表通过 date_key 关联",
        "columns": [
            {"name": "date_key", "display_name": "日期键", "description": "YYYYMMDD，主键"},
            {"name": "calendar_date", "display_name": "自然日"},
            {"name": "year", "display_name": "公历年"},
            {"name": "quarter", "display_name": "季度", "description": "1-4"},
            {"name": "month", "display_name": "月", "description": "1-12"},
            {"name": "week_of_year", "display_name": "周"},
            {"name": "day_of_week", "display_name": "星期"},
            {"name": "is_weekend", "display_name": "是否周末", "description": "0/1"},
            {"name": "year_month", "display_name": "年月", "description": "如 2025-06"},
        ],
    },
    "dim_region": {
        "display_name": "地区维表",
        "description": "省市区大区层级主数据",
        "columns": [
            {"name": "region_id", "display_name": "地区ID", "description": "主键"},
            {"name": "region_code", "display_name": "地区编码"},
            {"name": "region_name", "display_name": "地区名称"},
            {"name": "province", "display_name": "省份"},
            {"name": "city", "display_name": "城市"},
            {"name": "district", "display_name": "区县"},
            {"name": "region_level", "display_name": "大区", "description": "华南/华东/西南等"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_department": {
        "display_name": "部门维表",
        "description": "组织架构主数据",
        "columns": [
            {"name": "department_id", "display_name": "部门ID", "description": "主键"},
            {"name": "department_code", "display_name": "部门编码"},
            {"name": "department_name", "display_name": "部门名称"},
            {"name": "company_id", "display_name": "所属分公司", "description": "FK→dim_company"},
            {"name": "parent_id", "display_name": "上级部门ID"},
            {"name": "department_level", "display_name": "部门层级"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_owner": {
        "display_name": "业主维表",
        "description": "业主/客户主数据",
        "columns": [
            {"name": "owner_id", "display_name": "业主ID", "description": "主键"},
            {"name": "owner_code", "display_name": "业主编码"},
            {"name": "owner_name", "display_name": "业主名称"},
            {"name": "owner_type", "display_name": "业主类型"},
            {"name": "credit_level", "display_name": "信用等级"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_company": {
        "display_name": "分公司维表",
        "description": "分公司/子公司主数据",
        "columns": [
            {"name": "company_id", "display_name": "分公司ID", "description": "主键"},
            {"name": "company_code", "display_name": "分公司编码"},
            {"name": "company_name", "display_name": "分公司名称"},
            {"name": "region_id", "display_name": "所属地区", "description": "FK→dim_region"},
            {"name": "region_name", "display_name": "地区名称", "description": "冗余"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_project": {
        "display_name": "项目维表",
        "description": "施工项目主数据",
        "columns": [
            {"name": "project_id", "display_name": "项目ID", "description": "主键"},
            {"name": "project_code", "display_name": "项目编码"},
            {"name": "project_name", "display_name": "项目名称"},
            {"name": "company_id", "display_name": "所属分公司", "description": "FK→dim_company"},
            {"name": "company_name", "display_name": "分公司名称", "description": "冗余"},
            {"name": "region_id", "display_name": "所在地区", "description": "FK→dim_region"},
            {"name": "region_name", "display_name": "地区名称", "description": "冗余"},
            {"name": "owner_id", "display_name": "业主", "description": "FK→dim_owner"},
            {"name": "owner_name", "display_name": "业主名称", "description": "冗余"},
            {"name": "department_id", "display_name": "主责部门", "description": "FK→dim_department"},
            {"name": "department_name", "display_name": "部门名称", "description": "冗余"},
            {"name": "section_id", "display_name": "标段ID"},
            {"name": "section_name", "display_name": "标段名称"},
            {"name": "building_area", "display_name": "建筑面积"},
            {"name": "contract_amount", "display_name": "合同金额"},
            {"name": "project_status", "display_name": "项目状态", "description": "在建/竣工/结算/归档"},
            {"name": "monthly_budget_approved", "display_name": "月度预算已批复"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_supplier": {
        "display_name": "供应商维表",
        "description": "供应商主数据",
        "columns": [
            {"name": "supplier_id", "display_name": "供应商ID", "description": "主键"},
            {"name": "supplier_code", "display_name": "供应商编码"},
            {"name": "supplier_name", "display_name": "供应商名称"},
            {"name": "supplier_type", "display_name": "供应商类型"},
            {"name": "company_id", "display_name": "所属分公司", "description": "FK→dim_company"},
            {"name": "contact_person", "display_name": "联系人"},
            {"name": "contact_phone", "display_name": "联系电话"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_contract": {
        "display_name": "合同维表",
        "description": "分包/采购合同主数据",
        "columns": [
            {"name": "contract_id", "display_name": "合同ID", "description": "主键"},
            {"name": "contract_code", "display_name": "合同编码"},
            {"name": "contract_name", "display_name": "合同名称"},
            {"name": "project_id", "display_name": "所属项目", "description": "FK→dim_project"},
            {"name": "supplier_id", "display_name": "供应商", "description": "FK→dim_supplier"},
            {"name": "supplier_name", "display_name": "供应商名称", "description": "冗余"},
            {"name": "contract_content", "display_name": "合同内容"},
            {"name": "contract_amount", "display_name": "合同金额"},
            {"name": "tax_rate", "display_name": "税率"},
            {"name": "payment_ratio", "display_name": "付款比例"},
            {"name": "settlement_status", "display_name": "结算状态"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_cost_subject": {
        "display_name": "成本收支科目维表",
        "description": "成本/收支科目码表",
        "columns": [
            {"name": "subject_id", "display_name": "科目ID", "description": "主键"},
            {"name": "subject_code", "display_name": "科目编码"},
            {"name": "subject_name", "display_name": "科目名称"},
            {"name": "subject_level", "display_name": "科目层级"},
            {"name": "parent_subject_id", "display_name": "上级科目"},
            {"name": "subject_type", "display_name": "科目类型", "description": "收入/支出/成本"},
            {"name": "is_leaf", "display_name": "是否末级"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_project_output": {
        "display_name": "项目产值事实表",
        "description": "月度产值确权（已确认+待确认双轨）",
        "columns": [
            {"name": "output_id", "display_name": "产值记录ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "FK→dim_date"},
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "project_name", "display_name": "项目名称", "description": "冗余"},
            {"name": "company_id", "display_name": "分公司ID", "description": "冗余"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "confirmed_output", "display_name": "已确认产值"},
            {"name": "unconfirmed_output", "display_name": "待确认产值"},
            {"name": "total_output", "display_name": "总产值"},
            {"name": "output_last_year_confirmed", "display_name": "上年已确认产值"},
            {"name": "output_last_year_unconfirmed", "display_name": "上年待确认产值"},
            {"name": "output_current_confirmed", "display_name": "本年已确认产值"},
            {"name": "output_current_unconfirmed", "display_name": "本年待确认产值"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_project_cost": {
        "display_name": "项目成本事实表",
        "description": "月度成本汇总（已确/待确+结构）",
        "columns": [
            {"name": "cost_id", "display_name": "成本记录ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "FK→dim_date"},
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "project_name", "display_name": "项目名称", "description": "冗余"},
            {"name": "company_id", "display_name": "分公司ID", "description": "冗余"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "cost_confirmed_acc", "display_name": "累计已确认成本"},
            {"name": "cost_unconfirmed_acc", "display_name": "累计待确认成本"},
            {"name": "cost_confirmed_cmonth", "display_name": "本月已确认成本"},
            {"name": "cost_unconfirmed_cmonth", "display_name": "本月待确认成本"},
            {"name": "labor_cost_acc", "display_name": "累计人工费"},
            {"name": "material_cost_acc", "display_name": "累计材料费"},
            {"name": "equipment_cost_acc", "display_name": "累计设备费"},
            {"name": "management_fee_rate", "display_name": "管理费率"},
            {"name": "target_cost", "display_name": "目标成本"},
            {"name": "cost_code", "display_name": "成本代码"},
            {"name": "cost_name", "display_name": "成本名称"},
            {"name": "cost_level", "display_name": "成本层级"},
            {"name": "contract_id", "display_name": "关联合同", "description": "FK→dim_contract"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_project_payment": {
        "display_name": "项目付款事实表",
        "description": "月度付款与应付款",
        "columns": [
            {"name": "payment_id", "display_name": "付款记录ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "FK→dim_date"},
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "contract_id", "display_name": "合同ID", "description": "FK→dim_contract"},
            {"name": "supplier_id", "display_name": "供应商ID", "description": "FK→dim_supplier"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "payable_confirmed", "display_name": "已确应付款"},
            {"name": "payable_unconfirmed", "display_name": "待确应付款"},
            {"name": "labor_payable", "display_name": "人工费应付款"},
            {"name": "paid_amount", "display_name": "已付款金额"},
            {"name": "payment_ratio", "display_name": "付款比例"},
            {"name": "approval_status", "display_name": "批复状态"},
            {"name": "approval_amount", "display_name": "批复金额"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_project_balance": {
        "display_name": "项目收支事实表",
        "description": "项目/公司层面收支科目汇总",
        "columns": [
            {"name": "balance_id", "display_name": "收支记录ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "FK→dim_date"},
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "subject_id", "display_name": "科目ID", "description": "FK→dim_cost_subject"},
            {"name": "subject_code", "display_name": "科目编码", "description": "冗余"},
            {"name": "subject_name", "display_name": "科目名称", "description": "冗余"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "project_amount", "display_name": "项目层面金额"},
            {"name": "company_amount", "display_name": "公司层面金额"},
            {"name": "total_amount", "display_name": "合计金额"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_project_indicator": {
        "display_name": "项目指标事实表",
        "description": "核心商务指标（简化字段）",
        "columns": [
            {"name": "indicator_id", "display_name": "指标记录ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "FK→dim_date"},
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "company_id", "display_name": "分公司ID", "description": "冗余"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "indicator_code", "display_name": "指标编码"},
            {"name": "indicator_name", "display_name": "指标名称"},
            {"name": "indicator_value", "display_name": "指标值"},
            {"name": "target_value", "display_name": "目标值"},
            {"name": "warning_level", "display_name": "预警级别"},
            {"name": "remark", "display_name": "备注"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_project_risk": {
        "display_name": "项目风险事实表",
        "description": "风险清单与三色预警",
        "columns": [
            {"name": "risk_id", "display_name": "风险记录ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "FK→dim_date"},
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "risk_type", "display_name": "风险类型"},
            {"name": "risk_code", "display_name": "风险编码"},
            {"name": "risk_name", "display_name": "风险名称"},
            {"name": "risk_value", "display_name": "风险值"},
            {"name": "warning_level", "display_name": "预警级别"},
            {"name": "risk_description", "display_name": "风险描述"},
            {"name": "overall_warning_level", "display_name": "综合预警"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
}

# 读模型 VIEW 元数据（Cube 事实源，不计入 15 张物理表）
VIEW_REGISTRY = {
    "view_project_cube": {
        "display_name": "项目Cube读模型",
        "description": "dim_project + 事实表聚合",
        "columns": [
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "project_code", "display_name": "项目编码"},
            {"name": "project_name", "display_name": "项目名称"},
            {"name": "company_id", "display_name": "分公司ID"},
            {"name": "company_name", "display_name": "分公司名称"},
            {"name": "region_id", "display_name": "地区ID"},
            {"name": "region_name", "display_name": "地区名称"},
            {"name": "owner_id", "display_name": "业主ID"},
            {"name": "owner_name", "display_name": "业主名称"},
            {"name": "department_id", "display_name": "部门ID"},
            {"name": "department_name", "display_name": "部门名称"},
            {"name": "section_name", "display_name": "标段名称"},
            {"name": "project_status", "display_name": "项目状态"},
            {"name": "building_area", "display_name": "建筑面积"},
            {"name": "contract_amount", "display_name": "合同金额"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "confirmed_output", "display_name": "已确认产值"},
            {"name": "total_output", "display_name": "总产值"},
            {"name": "cost_confirmed_acc", "display_name": "累计已确成本"},
            {"name": "labor_cost_acc", "display_name": "累计人工费"},
            {"name": "paid_amount", "display_name": "已付款"},
            {"name": "payable_confirmed", "display_name": "已确应付款"},
            {"name": "received_amount", "display_name": "收款金额"},
            {"name": "risk_value_sum", "display_name": "风险值合计"},
        ],
    },
    "view_cost_output_comparison": {
        "display_name": "成本产值对比读模型",
        "description": "fact_project_output + fact_project_cost 关联",
        "columns": [
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "total_output", "display_name": "总产值"},
            {"name": "confirmed_output", "display_name": "已确认产值"},
            {"name": "cost_confirmed_acc", "display_name": "累计已确成本"},
            {"name": "cost_unconfirmed_acc", "display_name": "累计待确成本"},
            {"name": "target_cost", "display_name": "目标成本"},
        ],
    },
}


def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)

    output.print("=== 潘达工程商务成本本体初始化 ===")
    output.print(f"空间: {space_id}")

    # 1. 创建物理表（dim_date + 9 维 + 6 事实）
    output.print("\n[1/9] 创建物理表...")

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
            year_month String
        ) ENGINE = MergeTree()
        ORDER BY (date_key)
    """)
    output.print("OK dim_date")

    s.sql.execute("DROP TABLE IF EXISTS dim_region")
    s.sql.execute("""
        CREATE TABLE dim_region (
            region_id String COMMENT '地区ID',
            region_code String COMMENT '地区编码',
            region_name String COMMENT '地区名称',
            province String COMMENT '省份',
            city String COMMENT '城市',
            district String COMMENT '区县',
            region_level String COMMENT '大区',
            status String DEFAULT 'active' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (region_code)
    """)
    output.print("OK dim_region")

    s.sql.execute("DROP TABLE IF EXISTS dim_department")
    s.sql.execute("""
        CREATE TABLE dim_department (
            department_id String COMMENT '部门ID',
            department_code String COMMENT '部门编码',
            department_name String COMMENT '部门名称',
            company_id String COMMENT '所属分公司',
            parent_id String COMMENT '上级部门ID',
            department_level Int8 COMMENT '部门层级',
            status String DEFAULT 'active' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (department_code)
    """)
    output.print("OK dim_department")

    s.sql.execute("DROP TABLE IF EXISTS dim_owner")
    s.sql.execute("""
        CREATE TABLE dim_owner (
            owner_id String COMMENT '业主ID',
            owner_code String COMMENT '业主编码',
            owner_name String COMMENT '业主名称',
            owner_type String COMMENT '业主类型',
            credit_level String COMMENT '信用等级',
            status String DEFAULT 'active' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (owner_code)
    """)
    output.print("OK dim_owner")

    s.sql.execute("DROP TABLE IF EXISTS dim_company")
    s.sql.execute("""
        CREATE TABLE dim_company (
            company_id String COMMENT '分公司ID',
            company_code String COMMENT '分公司编码',
            company_name String COMMENT '分公司名称',
            region_id String COMMENT '所属地区',
            region_name String COMMENT '地区名称',
            status String DEFAULT 'active' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (company_code)
    """)
    output.print("OK dim_company")

    s.sql.execute("DROP TABLE IF EXISTS dim_project")
    s.sql.execute("""
        CREATE TABLE dim_project (
            project_id String COMMENT '项目ID',
            project_code String COMMENT '项目编码',
            project_name String COMMENT '项目名称',
            company_id String COMMENT '所属分公司',
            company_name String COMMENT '分公司名称',
            region_id String COMMENT '所在地区',
            region_name String COMMENT '地区名称',
            owner_id String COMMENT '业主',
            owner_name String COMMENT '业主名称',
            department_id String COMMENT '主责部门',
            department_name String COMMENT '部门名称',
            section_id String COMMENT '标段ID',
            section_name String COMMENT '标段名称',
            building_area Float64 COMMENT '建筑面积',
            contract_amount Float64 COMMENT '合同金额',
            project_status String DEFAULT '在建' COMMENT '项目状态',
            monthly_budget_approved UInt8 DEFAULT 0 COMMENT '月度预算已批复',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (company_id, project_code)
    """)
    output.print("OK dim_project")

    s.sql.execute("DROP TABLE IF EXISTS dim_supplier")
    s.sql.execute("""
        CREATE TABLE dim_supplier (
            supplier_id String COMMENT '供应商ID',
            supplier_code String COMMENT '供应商编码',
            supplier_name String COMMENT '供应商名称',
            supplier_type String COMMENT '供应商类型',
            company_id String COMMENT '所属分公司',
            contact_person String COMMENT '联系人',
            contact_phone String COMMENT '联系电话',
            status String DEFAULT 'active' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (supplier_code)
    """)
    output.print("OK dim_supplier")

    s.sql.execute("DROP TABLE IF EXISTS dim_contract")
    s.sql.execute("""
        CREATE TABLE dim_contract (
            contract_id String COMMENT '合同ID',
            contract_code String COMMENT '合同编码',
            contract_name String COMMENT '合同名称',
            project_id String COMMENT '所属项目',
            supplier_id String COMMENT '供应商',
            supplier_name String COMMENT '供应商名称',
            contract_content String COMMENT '合同内容',
            contract_amount Float64 COMMENT '合同金额',
            tax_rate Float64 COMMENT '税率',
            payment_ratio Float64 COMMENT '付款比例',
            settlement_status String COMMENT '结算状态',
            status String DEFAULT 'active' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (project_id, contract_code)
    """)
    output.print("OK dim_contract")

    s.sql.execute("DROP TABLE IF EXISTS dim_cost_subject")
    s.sql.execute("""
        CREATE TABLE dim_cost_subject (
            subject_id String COMMENT '科目ID',
            subject_code String COMMENT '科目编码',
            subject_name String COMMENT '科目名称',
            subject_level Int32 COMMENT '科目层级',
            parent_subject_id String COMMENT '上级科目',
            subject_type String COMMENT '科目类型',
            is_leaf UInt8 DEFAULT 1 COMMENT '是否末级',
            status String DEFAULT 'active' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (subject_code)
    """)
    output.print("OK dim_cost_subject")

    s.sql.execute("DROP TABLE IF EXISTS fact_project_output")
    s.sql.execute("""
        CREATE TABLE fact_project_output (
            output_id String COMMENT '产值记录ID',
            date_key Int32 COMMENT '日期键',
            project_id String COMMENT '项目ID',
            project_name String COMMENT '项目名称',
            company_id String COMMENT '分公司ID',
            report_period String COMMENT '报告期间',
            confirmed_output Float64 COMMENT '已确认产值',
            unconfirmed_output Float64 COMMENT '待确认产值',
            total_output Float64 COMMENT '总产值',
            output_last_year_confirmed Float64 COMMENT '上年已确认产值',
            output_last_year_unconfirmed Float64 COMMENT '上年待确认产值',
            output_current_confirmed Float64 COMMENT '本年已确认产值',
            output_current_unconfirmed Float64 COMMENT '本年待确认产值',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id)
    """)
    output.print("OK fact_project_output")

    s.sql.execute("DROP TABLE IF EXISTS fact_project_cost")
    s.sql.execute("""
        CREATE TABLE fact_project_cost (
            cost_id String COMMENT '成本记录ID',
            date_key Int32 COMMENT '日期键',
            project_id String COMMENT '项目ID',
            project_name String COMMENT '项目名称',
            company_id String COMMENT '分公司ID',
            report_period String COMMENT '报告期间',
            cost_confirmed_acc Float64 COMMENT '累计已确认成本',
            cost_unconfirmed_acc Float64 COMMENT '累计待确认成本',
            cost_confirmed_cmonth Float64 COMMENT '本月已确认成本',
            cost_unconfirmed_cmonth Float64 COMMENT '本月待确认成本',
            labor_cost_acc Float64 COMMENT '累计人工费',
            material_cost_acc Float64 COMMENT '累计材料费',
            equipment_cost_acc Float64 COMMENT '累计设备费',
            management_fee_rate Float64 COMMENT '管理费率',
            target_cost Float64 COMMENT '目标成本',
            cost_code String COMMENT '成本代码',
            cost_name String COMMENT '成本名称',
            cost_level String COMMENT '成本层级',
            contract_id String COMMENT '关联合同',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id, cost_code)
    """)
    output.print("OK fact_project_cost")

    s.sql.execute("DROP TABLE IF EXISTS fact_project_payment")
    s.sql.execute("""
        CREATE TABLE fact_project_payment (
            payment_id String COMMENT '付款记录ID',
            date_key Int32 COMMENT '日期键',
            project_id String COMMENT '项目ID',
            contract_id String COMMENT '合同ID',
            supplier_id String COMMENT '供应商ID',
            report_period String COMMENT '报告期间',
            payable_confirmed Float64 COMMENT '已确应付款',
            payable_unconfirmed Float64 COMMENT '待确应付款',
            labor_payable Float64 COMMENT '人工费应付款',
            paid_amount Float64 COMMENT '已付款金额',
            payment_ratio Float64 COMMENT '付款比例',
            approval_status String COMMENT '批复状态',
            approval_amount Float64 COMMENT '批复金额',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id, payment_id)
    """)
    output.print("OK fact_project_payment")

    s.sql.execute("DROP TABLE IF EXISTS fact_project_balance")
    s.sql.execute("""
        CREATE TABLE fact_project_balance (
            balance_id String COMMENT '收支记录ID',
            date_key Int32 COMMENT '日期键',
            project_id String COMMENT '项目ID',
            subject_id String COMMENT '科目ID',
            subject_code String COMMENT '科目编码',
            subject_name String COMMENT '科目名称',
            report_period String COMMENT '报告期间',
            project_amount Float64 COMMENT '项目层面金额',
            company_amount Float64 COMMENT '公司层面金额',
            total_amount Float64 COMMENT '合计金额',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id, subject_code)
    """)
    output.print("OK fact_project_balance")

    s.sql.execute("DROP TABLE IF EXISTS fact_project_indicator")
    s.sql.execute("""
        CREATE TABLE fact_project_indicator (
            indicator_id String COMMENT '指标记录ID',
            date_key Int32 COMMENT '日期键',
            project_id String COMMENT '项目ID',
            company_id String COMMENT '分公司ID',
            report_period String COMMENT '报告期间',
            indicator_code String COMMENT '指标编码',
            indicator_name String COMMENT '指标名称',
            indicator_value Float64 COMMENT '指标值',
            target_value Float64 COMMENT '目标值',
            warning_level String COMMENT '预警级别',
            remark String COMMENT '备注',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id, indicator_code)
    """)
    output.print("OK fact_project_indicator")

    s.sql.execute("DROP TABLE IF EXISTS fact_project_risk")
    s.sql.execute("""
        CREATE TABLE fact_project_risk (
            risk_id String COMMENT '风险记录ID',
            date_key Int32 COMMENT '日期键',
            project_id String COMMENT '项目ID',
            report_period String COMMENT '报告期间',
            risk_type String COMMENT '风险类型',
            risk_code String COMMENT '风险编码',
            risk_name String COMMENT '风险名称',
            risk_value Int32 COMMENT '风险值',
            warning_level String COMMENT '预警级别',
            risk_description String COMMENT '风险描述',
            overall_warning_level String COMMENT '综合预警',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id, risk_code)
    """)
    output.print("OK fact_project_risk")

    # 1b. 创建读模型 VIEW
    output.print("\n[1b/9] 创建读模型 VIEW...")

    s.sql.execute("DROP VIEW IF EXISTS view_cost_output_comparison")
    s.sql.execute("""
        CREATE VIEW view_cost_output_comparison AS
        SELECT
            project_id,
            report_period,
            sum(total_output) AS total_output,
            sum(confirmed_output) AS confirmed_output,
            sum(cost_confirmed_acc) AS cost_confirmed_acc,
            sum(cost_unconfirmed_acc) AS cost_unconfirmed_acc,
            sum(target_cost) AS target_cost
        FROM (
            SELECT
                project_id,
                report_period,
                total_output,
                confirmed_output,
                toFloat64(0) AS cost_confirmed_acc,
                toFloat64(0) AS cost_unconfirmed_acc,
                toFloat64(0) AS target_cost
            FROM fact_project_output
            UNION ALL
            SELECT
                project_id,
                report_period,
                toFloat64(0) AS total_output,
                toFloat64(0) AS confirmed_output,
                cost_confirmed_acc,
                cost_unconfirmed_acc,
                target_cost
            FROM fact_project_cost
        )
        GROUP BY project_id, report_period
    """)
    output.print("OK view_cost_output_comparison")

    s.sql.execute("DROP VIEW IF EXISTS view_project_cube")
    s.sql.execute("""
        CREATE VIEW view_project_cube AS
        SELECT
            p.project_id AS project_id,
            p.project_code AS project_code,
            p.project_name AS project_name,
            p.company_id AS company_id,
            p.company_name AS company_name,
            p.region_id AS region_id,
            p.region_name AS region_name,
            p.owner_id AS owner_id,
            p.owner_name AS owner_name,
            p.department_id AS department_id,
            p.department_name AS department_name,
            p.section_name AS section_name,
            p.project_status AS project_status,
            p.building_area AS building_area,
            p.contract_amount AS contract_amount,
            agg.report_period AS report_period,
            agg.confirmed_output AS confirmed_output,
            agg.total_output AS total_output,
            agg.cost_confirmed_acc AS cost_confirmed_acc,
            agg.labor_cost_acc AS labor_cost_acc,
            agg.paid_amount AS paid_amount,
            agg.payable_confirmed AS payable_confirmed,
            agg.received_amount AS received_amount,
            agg.risk_value_sum AS risk_value_sum
        FROM dim_project AS p
        INNER JOIN (
            SELECT
                keys.project_id AS project_id,
                keys.report_period AS report_period,
                coalesce(o.confirmed_output, toFloat64(0)) AS confirmed_output,
                coalesce(o.total_output, toFloat64(0)) AS total_output,
                coalesce(c.cost_confirmed_acc, toFloat64(0)) AS cost_confirmed_acc,
                coalesce(c.labor_cost_acc, toFloat64(0)) AS labor_cost_acc,
                coalesce(pm.paid_amount, toFloat64(0)) AS paid_amount,
                coalesce(pm.payable_confirmed, toFloat64(0)) AS payable_confirmed,
                coalesce(rec.received_amount, toFloat64(0)) AS received_amount,
                coalesce(rk.risk_value_sum, toInt64(0)) AS risk_value_sum
            FROM (
                SELECT project_id, report_period FROM fact_project_output
                UNION DISTINCT
                SELECT project_id, report_period FROM fact_project_cost
                UNION DISTINCT
                SELECT project_id, report_period FROM fact_project_payment
                UNION DISTINCT
                SELECT project_id, report_period FROM fact_project_indicator
                UNION DISTINCT
                SELECT project_id, report_period FROM fact_project_risk
            ) AS keys
            LEFT JOIN (
                SELECT project_id, report_period,
                    sum(confirmed_output) AS confirmed_output,
                    sum(total_output) AS total_output
                FROM fact_project_output
                GROUP BY project_id, report_period
            ) AS o ON keys.project_id = o.project_id AND keys.report_period = o.report_period
            LEFT JOIN (
                SELECT project_id, report_period,
                    sum(cost_confirmed_acc) AS cost_confirmed_acc,
                    sum(labor_cost_acc) AS labor_cost_acc
                FROM fact_project_cost
                GROUP BY project_id, report_period
            ) AS c ON keys.project_id = c.project_id AND keys.report_period = c.report_period
            LEFT JOIN (
                SELECT project_id, report_period,
                    sum(paid_amount) AS paid_amount,
                    sum(payable_confirmed) AS payable_confirmed
                FROM fact_project_payment
                GROUP BY project_id, report_period
            ) AS pm ON keys.project_id = pm.project_id AND keys.report_period = pm.report_period
            LEFT JOIN (
                SELECT project_id, report_period,
                    sumIf(indicator_value, indicator_code IN ('received_amount', 'collection_amount')) AS received_amount
                FROM fact_project_indicator
                GROUP BY project_id, report_period
            ) AS rec ON keys.project_id = rec.project_id AND keys.report_period = rec.report_period
            LEFT JOIN (
                SELECT project_id, report_period,
                    sum(risk_value) AS risk_value_sum
                FROM fact_project_risk
                GROUP BY project_id, report_period
            ) AS rk ON keys.project_id = rk.project_id AND keys.report_period = rk.report_period
        ) AS agg ON p.project_id = agg.project_id
    """)
    output.print("OK view_project_cube")

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

    for view_name, meta in VIEW_REGISTRY.items():
        s.tables.register_with_meta(
            table_name=view_name,
            display_name=meta["display_name"],
            description=meta.get("description"),
            columns=meta["columns"],
            force_column_meta=True,
        )
        output.print(f"OK {view_name} ({meta['display_name']})")

    # 3. 注册表间关系（25 条，规划 §3）
    output.print("\n[3/9] 注册表间关系...")

    table_relationships = [
        {"from_table": "fact_project_output", "to_table": "dim_date", "join_sql": "fact_project_output.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "产值关联日历"},
        {"from_table": "fact_project_cost", "to_table": "dim_date", "join_sql": "fact_project_cost.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "成本关联日历"},
        {"from_table": "fact_project_payment", "to_table": "dim_date", "join_sql": "fact_project_payment.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "付款关联日历"},
        {"from_table": "fact_project_balance", "to_table": "dim_date", "join_sql": "fact_project_balance.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "收支关联日历"},
        {"from_table": "fact_project_indicator", "to_table": "dim_date", "join_sql": "fact_project_indicator.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "指标关联日历"},
        {"from_table": "fact_project_risk", "to_table": "dim_date", "join_sql": "fact_project_risk.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "风险关联日历"},
        {"from_table": "dim_project", "to_table": "dim_company", "join_sql": "dim_project.company_id = dim_company.company_id", "join_keys": [{"from": "company_id", "to": "company_id"}], "relationship_type": "many_to_one", "description": "项目关联分公司"},
        {"from_table": "dim_company", "to_table": "dim_region", "join_sql": "dim_company.region_id = dim_region.region_id", "join_keys": [{"from": "region_id", "to": "region_id"}], "relationship_type": "many_to_one", "description": "分公司关联地区"},
        {"from_table": "dim_project", "to_table": "dim_region", "join_sql": "dim_project.region_id = dim_region.region_id", "join_keys": [{"from": "region_id", "to": "region_id"}], "relationship_type": "many_to_one", "description": "项目关联地区"},
        {"from_table": "dim_project", "to_table": "dim_owner", "join_sql": "dim_project.owner_id = dim_owner.owner_id", "join_keys": [{"from": "owner_id", "to": "owner_id"}], "relationship_type": "many_to_one", "description": "项目关联业主"},
        {"from_table": "dim_project", "to_table": "dim_department", "join_sql": "dim_project.department_id = dim_department.department_id", "join_keys": [{"from": "department_id", "to": "department_id"}], "relationship_type": "many_to_one", "description": "项目关联主责部门"},
        {"from_table": "dim_department", "to_table": "dim_company", "join_sql": "dim_department.company_id = dim_company.company_id", "join_keys": [{"from": "company_id", "to": "company_id"}], "relationship_type": "many_to_one", "description": "部门关联分公司"},
        {"from_table": "dim_department", "to_table": "dim_department", "join_sql": "dim_department.parent_id = dim_department.department_id", "join_keys": [{"from": "parent_id", "to": "department_id"}], "relationship_type": "many_to_one", "description": "部门上级（树形）"},
        {"from_table": "fact_project_output", "to_table": "dim_project", "join_sql": "fact_project_output.project_id = dim_project.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "产值关联项目"},
        {"from_table": "fact_project_cost", "to_table": "dim_project", "join_sql": "fact_project_cost.project_id = dim_project.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "成本关联项目"},
        {"from_table": "fact_project_payment", "to_table": "dim_project", "join_sql": "fact_project_payment.project_id = dim_project.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "付款关联项目"},
        {"from_table": "fact_project_balance", "to_table": "dim_project", "join_sql": "fact_project_balance.project_id = dim_project.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "收支关联项目"},
        {"from_table": "fact_project_indicator", "to_table": "dim_project", "join_sql": "fact_project_indicator.project_id = dim_project.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "指标关联项目"},
        {"from_table": "fact_project_risk", "to_table": "dim_project", "join_sql": "fact_project_risk.project_id = dim_project.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "风险关联项目"},
        {"from_table": "dim_contract", "to_table": "dim_project", "join_sql": "dim_contract.project_id = dim_project.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "合同关联项目"},
        {"from_table": "dim_contract", "to_table": "dim_supplier", "join_sql": "dim_contract.supplier_id = dim_supplier.supplier_id", "join_keys": [{"from": "supplier_id", "to": "supplier_id"}], "relationship_type": "many_to_one", "description": "合同关联供应商"},
        {"from_table": "dim_supplier", "to_table": "dim_company", "join_sql": "dim_supplier.company_id = dim_company.company_id", "join_keys": [{"from": "company_id", "to": "company_id"}], "relationship_type": "many_to_one", "description": "供应商关联分公司"},
        {"from_table": "fact_project_payment", "to_table": "dim_contract", "join_sql": "fact_project_payment.contract_id = dim_contract.contract_id", "join_keys": [{"from": "contract_id", "to": "contract_id"}], "relationship_type": "many_to_one", "description": "付款关联合同"},
        {"from_table": "fact_project_cost", "to_table": "dim_contract", "join_sql": "fact_project_cost.contract_id = dim_contract.contract_id", "join_keys": [{"from": "contract_id", "to": "contract_id"}], "relationship_type": "many_to_one", "description": "成本关联合同"},
        {"from_table": "fact_project_balance", "to_table": "dim_cost_subject", "join_sql": "fact_project_balance.subject_id = dim_cost_subject.subject_id", "join_keys": [{"from": "subject_id", "to": "subject_id"}], "relationship_type": "many_to_one", "description": "收支关联科目"},
    ]
    for rel in table_relationships:
        s.tables.add_relationship(**rel)
        output.print(f"OK {rel['from_table']} -> {rel['to_table']}")

    # 4. 注册 Cube（13 个，规划 §4）
    output.print("\n[4/9] 注册 Cube...")

    s.register_cube(
        name="RegionCube",
        table="dim_region",
        title="地区Cube",
        category_347="主体型",
        measures=[{"name": "region_count", "col": "region_id", "agg": "count", "title": "地区数量"}],
        dimensions=[
            {"name": "region_id", "col": "region_id", "type": "string", "title": "地区ID"},
            {"name": "region_code", "col": "region_code", "type": "string", "title": "地区编码"},
            {"name": "region_name", "col": "region_name", "type": "string", "title": "地区名称"},
            {"name": "province", "col": "province", "type": "string", "title": "省份"},
            {"name": "city", "col": "city", "type": "string", "title": "城市"},
            {"name": "district", "col": "district", "type": "string", "title": "区县"},
            {"name": "region_level", "col": "region_level", "type": "string", "title": "大区"},
        ],
    )
    output.print("OK RegionCube")

    s.register_cube(
        name="DepartmentCube",
        table="dim_department",
        title="部门Cube",
        category_347="主体型",
        measures=[{"name": "dept_count", "col": "department_id", "agg": "count", "title": "部门数量"}],
        dimensions=[
            {"name": "department_id", "col": "department_id", "type": "string", "title": "部门ID"},
            {"name": "department_code", "col": "department_code", "type": "string", "title": "部门编码"},
            {"name": "department_name", "col": "department_name", "type": "string", "title": "部门名称"},
            {"name": "company_id", "col": "company_id", "type": "string", "title": "分公司ID"},
            {"name": "parent_id", "col": "parent_id", "type": "string", "title": "上级部门ID"},
            {"name": "department_level", "col": "department_level", "type": "int", "title": "部门层级"},
        ],
    )
    output.print("OK DepartmentCube")

    s.register_cube(
        name="OwnerCube",
        table="dim_owner",
        title="业主Cube",
        category_347="主体型",
        measures=[{"name": "owner_count", "col": "owner_id", "agg": "count", "title": "业主数量"}],
        dimensions=[
            {"name": "owner_id", "col": "owner_id", "type": "string", "title": "业主ID"},
            {"name": "owner_code", "col": "owner_code", "type": "string", "title": "业主编码"},
            {"name": "owner_name", "col": "owner_name", "type": "string", "title": "业主名称"},
            {"name": "owner_type", "col": "owner_type", "type": "string", "title": "业主类型"},
            {"name": "credit_level", "col": "credit_level", "type": "string", "title": "信用等级"},
        ],
    )
    output.print("OK OwnerCube")

    s.register_cube(
        name="CostSubjectCube",
        table="dim_cost_subject",
        title="成本科目Cube",
        category_347="主体型",
        measures=[{"name": "subject_count", "col": "subject_id", "agg": "count", "title": "科目数量"}],
        dimensions=[
            {"name": "subject_id", "col": "subject_id", "type": "string", "title": "科目ID"},
            {"name": "subject_code", "col": "subject_code", "type": "string", "title": "科目编码"},
            {"name": "subject_name", "col": "subject_name", "type": "string", "title": "科目名称"},
            {"name": "subject_level", "col": "subject_level", "type": "int", "title": "科目层级"},
            {"name": "parent_subject_id", "col": "parent_subject_id", "type": "string", "title": "上级科目"},
            {"name": "subject_type", "col": "subject_type", "type": "string", "title": "科目类型"},
        ],
    )
    output.print("OK CostSubjectCube")

    s.register_cube(
        name="ProjectOutputCube",
        table="fact_project_output",
        title="项目产值Cube",
        category_347="流程型",
        measures=[
            {"name": "confirmed_output_total", "col": "confirmed_output", "agg": "sum", "title": "已确认产值"},
            {"name": "unconfirmed_output_total", "col": "unconfirmed_output", "agg": "sum", "title": "待确认产值"},
            {"name": "total_output_total", "col": "total_output", "agg": "sum", "title": "总产值"},
            {"name": "output_last_year_confirmed_total", "col": "output_last_year_confirmed", "agg": "sum", "title": "上年已确认产值"},
            {"name": "output_last_year_unconfirmed_total", "col": "output_last_year_unconfirmed", "agg": "sum", "title": "上年待确认产值"},
            {"name": "output_current_confirmed_total", "col": "output_current_confirmed", "agg": "sum", "title": "本年已确认产值"},
            {"name": "output_current_unconfirmed_total", "col": "output_current_unconfirmed", "agg": "sum", "title": "本年待确认产值"},
            {"name": "output_record_count", "col": "output_id", "agg": "count", "title": "记录数"},
        ],
        dimensions=[
            {"name": "output_id", "col": "output_id", "type": "string", "title": "产值记录ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
            {"name": "company_id", "col": "company_id", "type": "string", "title": "分公司ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
        ],
    )
    output.print("OK ProjectOutputCube")

    s.register_cube(
        name="ProjectCostCube",
        table="fact_project_cost",
        title="项目成本Cube",
        category_347="流程型",
        measures=[
            {"name": "cost_confirmed_acc_total", "col": "cost_confirmed_acc", "agg": "sum", "title": "累计已确成本"},
            {"name": "cost_unconfirmed_acc_total", "col": "cost_unconfirmed_acc", "agg": "sum", "title": "累计待确成本"},
            {"name": "cost_confirmed_cmonth_total", "col": "cost_confirmed_cmonth", "agg": "sum", "title": "本月已确成本"},
            {"name": "cost_unconfirmed_cmonth_total", "col": "cost_unconfirmed_cmonth", "agg": "sum", "title": "本月待确成本"},
            {"name": "labor_cost_total", "col": "labor_cost_acc", "agg": "sum", "title": "累计人工费"},
            {"name": "material_cost_total", "col": "material_cost_acc", "agg": "sum", "title": "累计材料费"},
            {"name": "equipment_cost_total", "col": "equipment_cost_acc", "agg": "sum", "title": "累计设备费"},
            {"name": "target_cost_total", "col": "target_cost", "agg": "sum", "title": "目标成本"},
        ],
        dimensions=[
            {"name": "cost_id", "col": "cost_id", "type": "string", "title": "成本记录ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
            {"name": "company_id", "col": "company_id", "type": "string", "title": "分公司ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "cost_code", "col": "cost_code", "type": "string", "title": "成本代码"},
            {"name": "cost_name", "col": "cost_name", "type": "string", "title": "成本名称"},
            {"name": "cost_level", "col": "cost_level", "type": "string", "title": "成本层级"},
            {"name": "contract_id", "col": "contract_id", "type": "string", "title": "合同ID"},
        ],
    )
    output.print("OK ProjectCostCube")

    s.register_cube(
        name="ProjectPaymentCube",
        table="fact_project_payment",
        title="项目付款Cube",
        category_347="流程型",
        measures=[
            {"name": "payable_confirmed_total", "col": "payable_confirmed", "agg": "sum", "title": "已确应付款"},
            {"name": "payable_unconfirmed_total", "col": "payable_unconfirmed", "agg": "sum", "title": "待确应付款"},
            {"name": "labor_payable_total", "col": "labor_payable", "agg": "sum", "title": "人工费应付款"},
            {"name": "paid_amount_total", "col": "paid_amount", "agg": "sum", "title": "已付款金额"},
            {"name": "approval_amount_total", "col": "approval_amount", "agg": "sum", "title": "批复金额"},
            {"name": "payment_count", "col": "payment_id", "agg": "count", "title": "付款记录数"},
        ],
        dimensions=[
            {"name": "payment_id", "col": "payment_id", "type": "string", "title": "付款记录ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "contract_id", "col": "contract_id", "type": "string", "title": "合同ID"},
            {"name": "supplier_id", "col": "supplier_id", "type": "string", "title": "供应商ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "approval_status", "col": "approval_status", "type": "string", "title": "批复状态"},
        ],
    )
    output.print("OK ProjectPaymentCube")

    s.register_cube(
        name="ProjectBalanceCube",
        table="fact_project_balance",
        title="项目收支Cube",
        category_347="流程型",
        measures=[
            {"name": "project_amount_total", "col": "project_amount", "agg": "sum", "title": "项目层面金额"},
            {"name": "company_amount_total", "col": "company_amount", "agg": "sum", "title": "公司层面金额"},
            {"name": "total_amount_total", "col": "total_amount", "agg": "sum", "title": "合计金额"},
        ],
        dimensions=[
            {"name": "balance_id", "col": "balance_id", "type": "string", "title": "收支记录ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "subject_id", "col": "subject_id", "type": "string", "title": "科目ID"},
            {"name": "subject_code", "col": "subject_code", "type": "string", "title": "科目编码"},
            {"name": "subject_name", "col": "subject_name", "type": "string", "title": "科目名称"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
        ],
    )
    output.print("OK ProjectBalanceCube")

    s.register_cube(
        name="ProjectIndicatorCube",
        table="fact_project_indicator",
        title="项目指标Cube",
        category_347="流程型",
        measures=[
            {"name": "indicator_value_avg", "col": "indicator_value", "agg": "avg", "title": "指标值均值"},
            {"name": "indicator_value_sum", "col": "indicator_value", "agg": "sum", "title": "指标值合计"},
            {"name": "target_value_avg", "col": "target_value", "agg": "avg", "title": "目标值均值"},
            {"name": "indicator_count", "col": "indicator_id", "agg": "count", "title": "指标记录数"},
        ],
        dimensions=[
            {"name": "indicator_id", "col": "indicator_id", "type": "string", "title": "指标记录ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "company_id", "col": "company_id", "type": "string", "title": "分公司ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "indicator_code", "col": "indicator_code", "type": "string", "title": "指标编码"},
            {"name": "indicator_name", "col": "indicator_name", "type": "string", "title": "指标名称"},
            {"name": "warning_level", "col": "warning_level", "type": "string", "title": "预警级别"},
        ],
    )
    output.print("OK ProjectIndicatorCube")

    s.register_cube(
        name="ProjectRiskCube",
        table="fact_project_risk",
        title="项目风险Cube",
        category_347="流程型",
        measures=[
            {"name": "risk_value_sum", "col": "risk_value", "agg": "sum", "title": "风险值合计"},
            {"name": "risk_count", "col": "risk_id", "agg": "count", "title": "风险记录数"},
        ],
        dimensions=[
            {"name": "risk_id", "col": "risk_id", "type": "string", "title": "风险记录ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "risk_type", "col": "risk_type", "type": "string", "title": "风险类型"},
            {"name": "risk_code", "col": "risk_code", "type": "string", "title": "风险编码"},
            {"name": "risk_name", "col": "risk_name", "type": "string", "title": "风险名称"},
            {"name": "warning_level", "col": "warning_level", "type": "string", "title": "预警级别"},
        ],
    )
    output.print("OK ProjectRiskCube")

    s.register_cube(
        name="ProjectCube",
        table="view_project_cube",
        title="项目Cube",
        category_347="主体型",
        measures=[
            {"name": "confirmed_output_total", "col": "confirmed_output", "agg": "sum", "title": "已确认产值"},
            {"name": "total_output_total", "col": "total_output", "agg": "sum", "title": "总产值"},
            {"name": "cost_confirmed_acc_total", "col": "cost_confirmed_acc", "agg": "sum", "title": "累计已确成本"},
            {"name": "labor_cost_total", "col": "labor_cost_acc", "agg": "sum", "title": "累计人工费"},
            {"name": "paid_amount_total", "col": "paid_amount", "agg": "sum", "title": "已付款"},
            {"name": "payable_confirmed_total", "col": "payable_confirmed", "agg": "sum", "title": "已确应付款"},
            {"name": "received_amount_total", "col": "received_amount", "agg": "sum", "title": "收款金额"},
            {"name": "risk_score", "col": "risk_value_sum", "agg": "sum", "title": "风险综合得分"},
            {"name": "building_area", "col": "building_area", "agg": "sum", "title": "建筑面积"},
            {"name": "contract_amount", "col": "contract_amount", "agg": "sum", "title": "合同金额"},
        ],
        dimensions=[
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "project_code", "col": "project_code", "type": "string", "title": "项目编码"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
            {"name": "company_id", "col": "company_id", "type": "string", "title": "分公司ID"},
            {"name": "company_name", "col": "company_name", "type": "string", "title": "分公司名称"},
            {"name": "region_id", "col": "region_id", "type": "string", "title": "地区ID"},
            {"name": "region_name", "col": "region_name", "type": "string", "title": "地区名称"},
            {"name": "owner_id", "col": "owner_id", "type": "string", "title": "业主ID"},
            {"name": "owner_name", "col": "owner_name", "type": "string", "title": "业主名称"},
            {"name": "department_id", "col": "department_id", "type": "string", "title": "部门ID"},
            {"name": "department_name", "col": "department_name", "type": "string", "title": "部门名称"},
            {"name": "section_name", "col": "section_name", "type": "string", "title": "标段名称"},
            {"name": "project_status", "col": "project_status", "type": "string", "title": "项目状态"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
        ],
    )
    output.print("OK ProjectCube")

    s.register_cube(
        name="CompanyCube",
        table="dim_company",
        title="分公司Cube",
        category_347="主体型",
        measures=[
            {"name": "company_count", "col": "company_id", "agg": "count", "title": "分公司数量"},
        ],
        dimensions=[
            {"name": "company_id", "col": "company_id", "type": "string", "title": "分公司ID"},
            {"name": "company_code", "col": "company_code", "type": "string", "title": "分公司编码"},
            {"name": "company_name", "col": "company_name", "type": "string", "title": "分公司名称"},
            {"name": "region_id", "col": "region_id", "type": "string", "title": "地区ID"},
            {"name": "region_name", "col": "region_name", "type": "string", "title": "地区名称"},
        ],
    )
    output.print("OK CompanyCube")

    s.register_cube(
        name="CostOutputComparisonCube",
        table="view_cost_output_comparison",
        title="成本产值对比Cube",
        category_347="对比型",
        measures=[
            {"name": "total_output_total", "col": "total_output", "agg": "sum", "title": "总产值"},
            {"name": "confirmed_output_total", "col": "confirmed_output", "agg": "sum", "title": "已确认产值"},
            {"name": "cost_confirmed_acc_total", "col": "cost_confirmed_acc", "agg": "sum", "title": "累计已确成本"},
            {"name": "cost_unconfirmed_acc_total", "col": "cost_unconfirmed_acc", "agg": "sum", "title": "累计待确成本"},
            {"name": "target_cost_total", "col": "target_cost", "agg": "sum", "title": "目标成本"},
        ],
        dimensions=[
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
        ],
    )
    output.print("OK CostOutputComparisonCube")

    # 4b. 派生度量（规划 §5.6）
    output.print("\n[4b/9] 配置派生度量...")

    s.upsert_derived_measures(
        "ProjectOutputCube",
        [
            {"name": "confirmed_ratio", "title": "确权率", "expression": "if(ProjectOutputCube.total_output_total > 0, ProjectOutputCube.confirmed_output_total / ProjectOutputCube.total_output_total, 0)", "description": "已确认产值/总产值"},
            {"name": "unconfirmed_ratio", "title": "待确比例", "expression": "if(ProjectOutputCube.total_output_total > 0, ProjectOutputCube.unconfirmed_output_total / ProjectOutputCube.total_output_total, 0)", "description": "待确认产值/总产值"},
            {"name": "output_current", "title": "本年累计产值", "expression": "ProjectOutputCube.output_current_confirmed_total + ProjectOutputCube.output_current_unconfirmed_total - ProjectOutputCube.output_last_year_confirmed_total - ProjectOutputCube.output_last_year_unconfirmed_total", "description": "本年累计产值"},
            {"name": "output_growth", "title": "同比增长率", "expression": "if((ProjectOutputCube.output_last_year_confirmed_total + ProjectOutputCube.output_last_year_unconfirmed_total) > 0, (ProjectOutputCube.output_current_confirmed_total + ProjectOutputCube.output_current_unconfirmed_total) / (ProjectOutputCube.output_last_year_confirmed_total + ProjectOutputCube.output_last_year_unconfirmed_total) - 1, 0)", "description": "产值同比增长"},
        ],
    )
    output.print("OK ProjectOutputCube 派生度量")

    s.upsert_derived_measures(
        "ProjectCostCube",
        [
            {"name": "cost_total_acc", "title": "累计总成本", "expression": "ProjectCostCube.cost_confirmed_acc_total + ProjectCostCube.cost_unconfirmed_acc_total", "description": "累计已确+待确成本"},
            {"name": "cost_current", "title": "本月总成本", "expression": "ProjectCostCube.cost_confirmed_cmonth_total + ProjectCostCube.cost_unconfirmed_cmonth_total", "description": "本月已确+待确成本"},
            {"name": "labor_ratio", "title": "人工费占比", "expression": "if(ProjectCostCube.cost_confirmed_acc_total > 0, ProjectCostCube.labor_cost_total / ProjectCostCube.cost_confirmed_acc_total, 0)", "description": "人工费/累计已确成本"},
            {"name": "material_ratio", "title": "材料费占比", "expression": "if(ProjectCostCube.cost_confirmed_acc_total > 0, ProjectCostCube.material_cost_total / ProjectCostCube.cost_confirmed_acc_total, 0)", "description": "材料费/累计已确成本"},
            {"name": "equipment_ratio", "title": "设备费占比", "expression": "if(ProjectCostCube.cost_confirmed_acc_total > 0, ProjectCostCube.equipment_cost_total / ProjectCostCube.cost_confirmed_acc_total, 0)", "description": "设备费/累计已确成本"},
            {"name": "cost_variance", "title": "成本偏差", "expression": "ProjectCostCube.cost_confirmed_acc_total - ProjectCostCube.target_cost_total", "description": "累计已确成本-目标成本"},
            {"name": "cost_variance_ratio", "title": "成本偏差率", "expression": "if(ProjectCostCube.target_cost_total > 0, (ProjectCostCube.cost_confirmed_acc_total - ProjectCostCube.target_cost_total) / ProjectCostCube.target_cost_total, 0)", "description": "成本偏差/目标成本"},
            {"name": "cost_rigidity", "title": "成本刚性度", "expression": "if(ProjectCostCube.cost_confirmed_acc_total > 0, ProjectCostCube.labor_cost_total / ProjectCostCube.cost_confirmed_acc_total, 0)", "description": "人工费/累计已确成本"},
            {"name": "cost_ratio", "title": "成本率", "expression": "if(ProjectCostCube.target_cost_total > 0, ProjectCostCube.cost_confirmed_acc_total / ProjectCostCube.target_cost_total, 0)", "description": "累计已确成本/目标成本"},
        ],
    )
    output.print("OK ProjectCostCube 派生度量")

    s.upsert_derived_measures(
        "ProjectPaymentCube",
        [
            {"name": "unpaid_amount", "title": "未付款金额", "expression": "ProjectPaymentCube.payable_confirmed_total - ProjectPaymentCube.paid_amount_total", "description": "已确应付款-已付款"},
            {"name": "unpaid_ratio", "title": "未付款比例", "expression": "if(ProjectPaymentCube.payable_confirmed_total > 0, (ProjectPaymentCube.payable_confirmed_total - ProjectPaymentCube.paid_amount_total) / ProjectPaymentCube.payable_confirmed_total, 0)", "description": "未付款/已确应付款"},
            {"name": "payment_rate", "title": "付款率", "expression": "if(ProjectPaymentCube.payable_confirmed_total > 0, ProjectPaymentCube.paid_amount_total / ProjectPaymentCube.payable_confirmed_total, 0)", "description": "已付款/已确应付款"},
            {"name": "payment_progress", "title": "付款进度", "expression": "if(ProjectPaymentCube.payable_confirmed_total > 0, ProjectPaymentCube.paid_amount_total / ProjectPaymentCube.payable_confirmed_total, 0)", "description": "相对应付款的付款进度"},
            {"name": "payable_ratio", "title": "应付款比例", "expression": "if(ProjectPaymentCube.payable_confirmed_total > 0, ProjectPaymentCube.payable_confirmed_total / ProjectPaymentCube.payable_confirmed_total, 0)", "description": "应付款占比（P0占位）"},
            {"name": "labor_payment_ratio", "title": "人工费占应付款", "expression": "if(ProjectPaymentCube.payable_confirmed_total > 0, ProjectPaymentCube.labor_payable_total / ProjectPaymentCube.payable_confirmed_total, 0)", "description": "人工费应付款/已确应付款"},
        ],
    )
    output.print("OK ProjectPaymentCube 派生度量")

    s.upsert_derived_measures(
        "ProjectBalanceCube",
        [
            {"name": "balance_gap", "title": "收支差额", "expression": "ProjectBalanceCube.project_amount_total - ProjectBalanceCube.company_amount_total", "description": "项目层面-公司层面"},
            {"name": "income_ratio", "title": "收入占比", "expression": "if(ProjectBalanceCube.total_amount_total > 0, ProjectBalanceCube.project_amount_total / ProjectBalanceCube.total_amount_total, 0)", "description": "项目金额/合计"},
            {"name": "expense_ratio", "title": "支出占比", "expression": "if(ProjectBalanceCube.total_amount_total > 0, ProjectBalanceCube.company_amount_total / ProjectBalanceCube.total_amount_total, 0)", "description": "公司金额/合计"},
        ],
    )
    output.print("OK ProjectBalanceCube 派生度量")

    s.upsert_derived_measures(
        "ProjectIndicatorCube",
        [
            {"name": "variance_value", "title": "指标偏差值", "expression": "ProjectIndicatorCube.indicator_value_avg - ProjectIndicatorCube.target_value_avg", "description": "指标值-目标值"},
            {"name": "variance_ratio", "title": "指标偏差率", "expression": "if(ProjectIndicatorCube.target_value_avg > 0, (ProjectIndicatorCube.indicator_value_avg - ProjectIndicatorCube.target_value_avg) / ProjectIndicatorCube.target_value_avg, 0)", "description": "偏差值/目标值"},
            {"name": "is_warning", "title": "是否预警", "expression": "if(ProjectIndicatorCube.target_value_avg > 0, abs((ProjectIndicatorCube.indicator_value_avg - ProjectIndicatorCube.target_value_avg) / ProjectIndicatorCube.target_value_avg) > 0.10, 0)", "description": "偏差率>10%"},
        ],
    )
    output.print("OK ProjectIndicatorCube 派生度量")

    s.upsert_derived_measures(
        "ProjectRiskCube",
        [
            {"name": "risk_score", "title": "风险综合得分", "expression": "ProjectRiskCube.risk_value_sum", "description": "风险值加权合计"},
        ],
    )
    output.print("OK ProjectRiskCube 派生度量")

    s.upsert_derived_measures(
        "ProjectCube",
        [
            {"name": "profit_rate", "title": "毛利率", "expression": "if(ProjectCube.total_output_total > 0, (ProjectCube.total_output_total - ProjectCube.cost_confirmed_acc_total) / ProjectCube.total_output_total, 0)", "description": "(产值-成本)/产值"},
            {"name": "cost_ratio", "title": "成本率", "expression": "if(ProjectCube.total_output_total > 0, ProjectCube.cost_confirmed_acc_total / ProjectCube.total_output_total, 0)", "description": "成本/产值"},
            {"name": "confirmed_ratio", "title": "产值确认率", "expression": "if(ProjectCube.total_output_total > 0, ProjectCube.confirmed_output_total / ProjectCube.total_output_total, 0)", "description": "已确认产值/总产值"},
            {"name": "cost_rigidity", "title": "成本刚性度", "expression": "if(ProjectCube.cost_confirmed_acc_total > 0, ProjectCube.labor_cost_total / ProjectCube.cost_confirmed_acc_total, 0)", "description": "人工费/累计已确成本"},
            {"name": "collection_rate", "title": "回款率", "expression": "if(ProjectCube.confirmed_output_total > 0, ProjectCube.received_amount_total / ProjectCube.confirmed_output_total, 0)", "description": "收款/已确认产值"},
            {"name": "payment_rate", "title": "付款率", "expression": "if(ProjectCube.payable_confirmed_total > 0, ProjectCube.paid_amount_total / ProjectCube.payable_confirmed_total, 0)", "description": "已付款/已确应付款"},
            {"name": "cash_balance", "title": "资金结余", "expression": "ProjectCube.received_amount_total - ProjectCube.paid_amount_total", "description": "收款-付款"},
            {"name": "health_score", "title": "项目健康度", "expression": "(if(ProjectCube.total_output_total > 0, (ProjectCube.total_output_total - ProjectCube.cost_confirmed_acc_total) / ProjectCube.total_output_total, 0) / 0.20 + if(ProjectCube.confirmed_output_total > 0, ProjectCube.received_amount_total / ProjectCube.confirmed_output_total, 0) + if(ProjectCube.total_output_total > 0, ProjectCube.confirmed_output_total / ProjectCube.total_output_total, 0)) / 3", "description": "030健康度公式"},
        ],
    )
    output.print("OK ProjectCube 派生度量")

    s.upsert_derived_measures(
        "CostOutputComparisonCube",
        [
            {"name": "profit_rate", "title": "毛利率", "expression": "if(CostOutputComparisonCube.total_output_total > 0, (CostOutputComparisonCube.total_output_total - CostOutputComparisonCube.cost_confirmed_acc_total) / CostOutputComparisonCube.total_output_total, 0)", "description": "成本产值对比毛利率"},
            {"name": "cost_ratio", "title": "成本率", "expression": "if(CostOutputComparisonCube.total_output_total > 0, CostOutputComparisonCube.cost_confirmed_acc_total / CostOutputComparisonCube.total_output_total, 0)", "description": "成本/产值"},
            {"name": "confirmed_ratio", "title": "产值确认率", "expression": "if(CostOutputComparisonCube.total_output_total > 0, CostOutputComparisonCube.confirmed_output_total / CostOutputComparisonCube.total_output_total, 0)", "description": "已确认产值/总产值"},
        ],
    )
    output.print("OK CostOutputComparisonCube 派生度量")

    # 5. 定义对象类型（15 种，规划 §5.1）
    output.print("\n[5/9] 定义对象类型...")

    object_types = [
        ("Region", "地区", "省市区大区层级主数据", "主数据", "RegionCube"),
        ("Department", "部门", "组织架构主数据", "主数据", "DepartmentCube"),
        ("Owner", "业主", "业主/客户主数据", "主数据", "OwnerCube"),
        ("Company", "分公司", "分公司/子公司主数据", "主数据", "CompanyCube"),
        ("Project", "项目", "施工项目主数据", "主数据", "ProjectCube"),
        ("Contract", "合同", "分包/采购合同", "主数据", "ProjectPaymentCube"),
        ("Supplier", "供应商", "供应商主数据", "主数据", "ProjectPaymentCube"),
        ("CostSubject", "成本收支科目", "成本/收支科目码表", "参考", "CostSubjectCube"),
        ("ProjectOutput", "项目产值", "月度产值确权事务", "事务", "ProjectOutputCube"),
        ("ProjectCost", "项目成本", "月度成本汇总事务", "事务", "ProjectCostCube"),
        ("ProjectPayment", "项目付款", "月度付款事务", "事务", "ProjectPaymentCube"),
        ("ProjectBalance", "项目收支", "收支科目汇总事务", "事务", "ProjectBalanceCube"),
        ("ProjectIndicator", "项目指标", "核心商务指标事务", "事务", "ProjectIndicatorCube"),
        ("ProjectRisk", "项目风险", "风险清单预警事务", "事务", "ProjectRiskCube"),
        ("CostManagementAnalysis", "商务成本分析", "成本产值对比分析", "分析", "CostOutputComparisonCube"),
    ]
    for code, name, desc, cat, cube in object_types:
        s.onto.define_object_type(code=code, name=name, description=desc, category_347=cat)
        s.onto.bind_source(code, "dazi_cube", config={"cube": cube})
        output.print(f"OK {code}")

    # 6. 定义对象属性（规划 §5.2）
    output.print("\n[6/9] 定义对象属性...")

    properties = [
        ("Region", "id", "地区ID", "dimension", "RegionCube.region_id"),
        ("Region", "code", "地区编码", "dimension", "RegionCube.region_code"),
        ("Region", "name", "地区名称", "dimension", "RegionCube.region_name"),
        ("Region", "province", "省份", "dimension", "RegionCube.province"),
        ("Region", "city", "城市", "dimension", "RegionCube.city"),
        ("Region", "regionLevel", "大区", "dimension", "RegionCube.region_level"),
        ("Department", "id", "部门ID", "dimension", "DepartmentCube.department_id"),
        ("Department", "code", "部门编码", "dimension", "DepartmentCube.department_code"),
        ("Department", "name", "部门名称", "dimension", "DepartmentCube.department_name"),
        ("Department", "level", "部门层级", "dimension", "DepartmentCube.department_level"),
        ("Owner", "id", "业主ID", "dimension", "OwnerCube.owner_id"),
        ("Owner", "code", "业主编码", "dimension", "OwnerCube.owner_code"),
        ("Owner", "name", "业主名称", "dimension", "OwnerCube.owner_name"),
        ("Owner", "type", "业主类型", "dimension", "OwnerCube.owner_type"),
        ("Owner", "creditLevel", "信用等级", "dimension", "OwnerCube.credit_level"),
        ("Project", "id", "项目ID", "dimension", "ProjectCube.project_id"),
        ("Project", "code", "项目编码", "dimension", "ProjectCube.project_code"),
        ("Project", "name", "项目名称", "dimension", "ProjectCube.project_name"),
        ("Project", "companyName", "分公司名称", "dimension", "ProjectCube.company_name"),
        ("Project", "regionName", "所在地区", "dimension", "ProjectCube.region_name"),
        ("Project", "ownerName", "业主名称", "dimension", "ProjectCube.owner_name"),
        ("Project", "departmentName", "主责部门", "dimension", "ProjectCube.department_name"),
        ("Project", "buildingArea", "建筑面积", "measure", "ProjectCube.building_area"),
        ("Project", "contractAmount", "合同金额", "measure", "ProjectCube.contract_amount"),
        ("Project", "profitRate", "毛利率", "measure", "ProjectCube.profit_rate"),
        ("Project", "costRatio", "成本率", "measure", "ProjectCube.cost_ratio"),
        ("Project", "confirmedRatio", "产值确认率", "measure", "ProjectCube.confirmed_ratio"),
        ("Project", "costRigidity", "成本刚性度", "measure", "ProjectCube.cost_rigidity"),
        ("Project", "collectionRate", "回款率", "measure", "ProjectCube.collection_rate"),
        ("Project", "paymentRate", "付款率", "measure", "ProjectCube.payment_rate"),
        ("Project", "cashBalance", "资金结余", "measure", "ProjectCube.cash_balance"),
        ("Project", "riskScore", "风险综合得分", "measure", "ProjectCube.risk_score"),
        ("Project", "healthScore", "项目健康度", "measure", "ProjectCube.health_score"),
        ("Project", "reportPeriod", "报告期间", "dimension", "ProjectCube.report_period"),
        ("ProjectOutput", "id", "记录ID", "dimension", "ProjectOutputCube.output_id"),
        ("ProjectOutput", "projectId", "项目ID", "dimension", "ProjectOutputCube.project_id"),
        ("ProjectOutput", "reportPeriod", "报告期间", "dimension", "ProjectOutputCube.report_period"),
        ("ProjectOutput", "outputConfirmed", "已确认产值", "measure", "ProjectOutputCube.confirmed_output_total"),
        ("ProjectOutput", "outputUnconfirmed", "待确认产值", "measure", "ProjectOutputCube.unconfirmed_output_total"),
        ("ProjectOutput", "outputTotal", "总产值", "measure", "ProjectOutputCube.total_output_total"),
        ("ProjectOutput", "confirmedRatio", "确权率", "measure", "ProjectOutputCube.confirmed_ratio"),
        ("ProjectOutput", "unconfirmedRatio", "待确比例", "measure", "ProjectOutputCube.unconfirmed_ratio"),
        ("ProjectOutput", "outputCurrent", "本年累计产值", "measure", "ProjectOutputCube.output_current"),
        ("ProjectOutput", "outputGrowth", "同比增长率", "measure", "ProjectOutputCube.output_growth"),
        ("ProjectCost", "id", "记录ID", "dimension", "ProjectCostCube.cost_id"),
        ("ProjectCost", "projectId", "项目ID", "dimension", "ProjectCostCube.project_id"),
        ("ProjectCost", "costConfirmedAcc", "累计已确成本", "measure", "ProjectCostCube.cost_confirmed_acc_total"),
        ("ProjectCost", "costUnconfirmedAcc", "累计待确成本", "measure", "ProjectCostCube.cost_unconfirmed_acc_total"),
        ("ProjectCost", "laborCostAcc", "累计人工费", "measure", "ProjectCostCube.labor_cost_total"),
        ("ProjectCost", "materialCostAcc", "累计材料费", "measure", "ProjectCostCube.material_cost_total"),
        ("ProjectCost", "equipmentCostAcc", "累计设备费", "measure", "ProjectCostCube.equipment_cost_total"),
        ("ProjectCost", "costTotalAcc", "累计总成本", "measure", "ProjectCostCube.cost_total_acc"),
        ("ProjectCost", "costCurrent", "本月总成本", "measure", "ProjectCostCube.cost_current"),
        ("ProjectCost", "laborRatio", "人工费占比", "measure", "ProjectCostCube.labor_ratio"),
        ("ProjectCost", "materialRatio", "材料费占比", "measure", "ProjectCostCube.material_ratio"),
        ("ProjectCost", "equipmentRatio", "设备费占比", "measure", "ProjectCostCube.equipment_ratio"),
        ("ProjectCost", "costVariance", "成本偏差", "measure", "ProjectCostCube.cost_variance"),
        ("ProjectCost", "costVarianceRatio", "成本偏差率", "measure", "ProjectCostCube.cost_variance_ratio"),
        ("ProjectCost", "costRatio", "成本率", "measure", "ProjectCostCube.cost_ratio"),
        ("ProjectCost", "costRigidity", "成本刚性度", "measure", "ProjectCostCube.cost_rigidity"),
        ("ProjectPayment", "id", "记录ID", "dimension", "ProjectPaymentCube.payment_id"),
        ("ProjectPayment", "payableConfirmed", "已确应付款", "measure", "ProjectPaymentCube.payable_confirmed_total"),
        ("ProjectPayment", "paidAmount", "已付款", "measure", "ProjectPaymentCube.paid_amount_total"),
        ("ProjectPayment", "unpaidAmount", "未付款", "measure", "ProjectPaymentCube.unpaid_amount"),
        ("ProjectPayment", "unpaidRatio", "未付款比例", "measure", "ProjectPaymentCube.unpaid_ratio"),
        ("ProjectPayment", "paymentRate", "付款率", "measure", "ProjectPaymentCube.payment_rate"),
        ("ProjectPayment", "paymentProgress", "付款进度", "measure", "ProjectPaymentCube.payment_progress"),
        ("ProjectPayment", "payableRatio", "应付款比例", "measure", "ProjectPaymentCube.payable_ratio"),
        ("ProjectPayment", "laborPaymentRatio", "人工费占应付款", "measure", "ProjectPaymentCube.labor_payment_ratio"),
        ("ProjectBalance", "balanceAmount", "收支差额", "measure", "ProjectBalanceCube.balance_gap"),
        ("ProjectBalance", "incomeRatio", "收入占比", "measure", "ProjectBalanceCube.income_ratio"),
        ("ProjectBalance", "expenseRatio", "支出占比", "measure", "ProjectBalanceCube.expense_ratio"),
        ("ProjectIndicator", "varianceValue", "指标偏差值", "measure", "ProjectIndicatorCube.variance_value"),
        ("ProjectIndicator", "varianceRatio", "指标偏差率", "measure", "ProjectIndicatorCube.variance_ratio"),
        ("ProjectIndicator", "isWarning", "是否预警", "measure", "ProjectIndicatorCube.is_warning"),
        ("ProjectRisk", "id", "风险ID", "dimension", "ProjectRiskCube.risk_id"),
        ("ProjectRisk", "riskType", "风险类型", "dimension", "ProjectRiskCube.risk_type"),
        ("ProjectRisk", "riskName", "风险名称", "dimension", "ProjectRiskCube.risk_name"),
        ("ProjectRisk", "warningLevel", "预警级别", "dimension", "ProjectRiskCube.warning_level"),
        ("ProjectRisk", "riskValue", "风险值", "measure", "ProjectRiskCube.risk_value_sum"),
        ("ProjectRisk", "riskScore", "风险综合得分", "measure", "ProjectRiskCube.risk_score"),
    ]
    for obj, code, name, role, qn in properties:
        s.onto.define_property(obj, code, name, semantic_role=role, qualified_name=qn)
    output.print("OK 属性定义完成")

    # 7. 定义链接类型（24 种，规划 §5.3）
    output.print("\n[7/9] 定义链接类型...")

    link_types = [
        ("project_belongs_company", "项目归属分公司", "Project", "Company", "归属关系"),
        ("supplier_belongs_company", "供应商归属分公司", "Supplier", "Company", "归属关系"),
        ("company_located_in_region", "分公司所在地区", "Company", "Region", "归属关系"),
        ("project_located_in_region", "项目所在地区", "Project", "Region", "归属关系"),
        ("project_serves_owner", "项目服务业主", "Project", "Owner", "归属关系"),
        ("project_managed_by_department", "项目主责部门", "Project", "Department", "归属关系"),
        ("department_belongs_company", "部门归属分公司", "Department", "Company", "归属关系"),
        ("department_has_parent", "部门上级", "Department", "Department", "层级关系"),
        ("output_belongs_project", "产值归属项目", "ProjectOutput", "Project", "归属关系"),
        ("cost_belongs_project", "成本归属项目", "ProjectCost", "Project", "归属关系"),
        ("payment_belongs_project", "付款归属项目", "ProjectPayment", "Project", "归属关系"),
        ("balance_belongs_project", "收支归属项目", "ProjectBalance", "Project", "归属关系"),
        ("indicator_belongs_project", "指标归属项目", "ProjectIndicator", "Project", "归属关系"),
        ("risk_belongs_project", "风险归属项目", "ProjectRisk", "Project", "归属关系"),
        ("contract_belongs_project", "合同归属项目", "Contract", "Project", "归属关系"),
        ("contract_with_supplier", "合同关联供应商", "Contract", "Supplier", "归属关系"),
        ("cost_contains_contract", "成本关联合同", "ProjectCost", "Contract", "归属关系"),
        ("payment_contains_contract", "付款关联合同", "ProjectPayment", "Contract", "归属关系"),
        ("balance_has_subject", "收支关联科目", "ProjectBalance", "CostSubject", "归属关系"),
        ("analysis_by_project", "分析归因项目", "CostManagementAnalysis", "Project", "分析归因"),
        ("analysis_by_company", "分析归因分公司", "CostManagementAnalysis", "Company", "分析归因"),
        ("analysis_by_region", "分析归因地区", "CostManagementAnalysis", "Region", "分析归因"),
        ("analysis_by_owner", "分析归因业主", "CostManagementAnalysis", "Owner", "分析归因"),
        ("analysis_by_department", "分析归因部门", "CostManagementAnalysis", "Department", "分析归因"),
    ]
    for code, name, from_code, to_code, cat in link_types:
        s.onto.define_link_type(
            code=code,
            name=name,
            from_object_type_code=from_code,
            to_object_type_code=to_code,
            category_347=cat,
        )
    output.print("OK 链接定义完成")

    # 8. 同步指标引用 + 输出摘要
    output.print("\n[8/9] 同步指标引用...")
    s.sync_metric_refs()
    output.print("OK sync_metric_refs")

    summary = {
        "ok": True,
        "space_id": space_id,
        "tables": len(TABLE_REGISTRY),
        "views": len(VIEW_REGISTRY),
        "relationships": len(table_relationships),
        "cubes": 13,
        "objects": 15,
        "links": 24,
    }
    output.success("潘达工程商务成本本体初始化完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))

