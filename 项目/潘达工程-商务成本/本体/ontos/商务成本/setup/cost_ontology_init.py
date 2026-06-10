"""商务成本本体初始化脚本 — space__panda_construction

初始化内容：
1. 创建物理表（9 维 + 6 事实，不含 dim_date）
2. 注册表到空间（含 display_name / description）
3. 注册表间关系（16 条，含 6 条 fact→dim_date）
4. 注册 Cube（15 个）及派生度量
5. 定义对象类型（15 种）、绑定数据源、属性、链接（12 种）
6. 同步指标引用
7. 输出 JSON summary

不含 apply_registry（分类在 cost_category_mount.py）。

放置：项目/潘达工程-商务成本/本体/ontos/商务成本/setup/cost_ontology_init.py
发布：dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/商务成本/setup/cost_ontology_init.py --space space__panda_construction --type setup
规划对照：项目/潘达工程-商务成本/本体/ontos/商务成本/plans/规划文档_商务成本本体方案.md
"""

import json

# 与规划文档 §3 对齐：display_name=侧栏显示名，description=业务说明
TABLE_REGISTRY = {
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
            {"name": "parent_id", "display_name": "上级部门ID"},
            {"name": "department_level", "display_name": "部门层级"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_owner": {
        "display_name": "业主维表",
        "description": "业主主数据",
        "columns": [
            {"name": "owner_id", "display_name": "业主ID", "description": "主键"},
            {"name": "owner_code", "display_name": "业主编码"},
            {"name": "owner_name", "display_name": "业主名称"},
            {"name": "owner_type", "display_name": "业主类型"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_cost_subject": {
        "display_name": "成本科目维表",
        "description": "成本分类科目主数据",
        "columns": [
            {"name": "subject_id", "display_name": "科目ID", "description": "主键"},
            {"name": "subject_code", "display_name": "科目编码"},
            {"name": "subject_name", "display_name": "科目名称"},
            {"name": "subject_level", "display_name": "科目层级"},
            {"name": "parent_id", "display_name": "上级科目"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_project": {
        "display_name": "项目维表",
        "description": "项目主数据",
        "columns": [
            {"name": "project_id", "display_name": "项目ID", "description": "主键"},
            {"name": "project_code", "display_name": "项目编码"},
            {"name": "project_name", "display_name": "项目名称"},
            {"name": "company_id", "display_name": "公司ID", "description": "关联dim_company"},
            {"name": "company_name", "display_name": "公司名称", "description": "冗余"},
            {"name": "section_id", "display_name": "标段ID"},
            {"name": "section_name", "display_name": "标段名称"},
            {"name": "building_area", "display_name": "建筑面积"},
            {"name": "contract_amount", "display_name": "合同金额"},
            {"name": "project_type", "display_name": "项目类型"},
            {"name": "status", "display_name": "状态", "description": "在建/完工"},
            {"name": "created_at", "display_name": "创建时间"},
            {"name": "updated_at", "display_name": "更新时间"},
        ],
    },
    "dim_company": {
        "display_name": "公司维表",
        "description": "公司主数据",
        "columns": [
            {"name": "company_id", "display_name": "公司ID", "description": "主键"},
            {"name": "company_code", "display_name": "公司编码"},
            {"name": "company_name", "display_name": "公司名称"},
            {"name": "status", "display_name": "状态"},
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
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_contract": {
        "display_name": "合同维表",
        "description": "合同主数据",
        "columns": [
            {"name": "contract_id", "display_name": "合同ID", "description": "主键"},
            {"name": "contract_code", "display_name": "合同编码"},
            {"name": "contract_name", "display_name": "合同名称"},
            {"name": "project_id", "display_name": "项目ID", "description": "关联dim_project"},
            {"name": "contract_amount", "display_name": "合同金额"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_project_output": {
        "display_name": "项目产值事实表",
        "description": "项目产值数据；含已确认/待确认双轨制",
        "columns": [
            {"name": "id", "display_name": "记录ID", "description": "主键"},
            {"name": "project_id", "display_name": "项目ID", "description": "关联dim_project"},
            {"name": "date_key", "display_name": "日期键", "description": "关联dim_date"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "output_value", "display_name": "产值金额"},
            {"name": "output_tax", "display_name": "税金"},
            {"name": "output_without_tax", "display_name": "不含税产值"},
            {"name": "output_type", "display_name": "产值类型"},
            {"name": "output_ratio", "display_name": "产值比例"},
            {"name": "confirm_type", "display_name": "确认类型", "description": "已确认/待确认"},
            {"name": "confirmed_output", "display_name": "已确认产值"},
            {"name": "pending_output", "display_name": "待确认产值"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_project_cost": {
        "display_name": "项目成本事实表",
        "description": "项目成本数据；含三级成本分类",
        "columns": [
            {"name": "id", "display_name": "记录ID", "description": "主键"},
            {"name": "project_id", "display_name": "项目ID", "description": "关联dim_project"},
            {"name": "contract_id", "display_name": "合同ID", "description": "关联dim_contract"},
            {"name": "date_key", "display_name": "日期键", "description": "关联dim_date"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "cost_amount", "display_name": "成本金额"},
            {"name": "cost_type", "display_name": "成本类型"},
            {"name": "cost_level1", "display_name": "成本一级分类"},
            {"name": "cost_level2", "display_name": "成本二级分类"},
            {"name": "cost_level3", "display_name": "成本三级分类"},
            {"name": "labor_cost", "display_name": "人工费"},
            {"name": "material_cost", "display_name": "材料费"},
            {"name": "mechanical_cost", "display_name": "机械费"},
            {"name": "other_cost", "display_name": "其他费用"},
            {"name": "target_cost", "display_name": "目标成本"},
            {"name": "variance_amount", "display_name": "偏差金额"},
            {"name": "variance_ratio", "display_name": "偏差率"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_project_indicator": {
        "display_name": "项目指标事实表",
        "description": "项目指标数据；含毛利率、收款率等",
        "columns": [
            {"name": "id", "display_name": "记录ID", "description": "主键"},
            {"name": "project_id", "display_name": "项目ID", "description": "关联dim_project"},
            {"name": "company_id", "display_name": "公司ID", "description": "关联dim_company"},
            {"name": "date_key", "display_name": "日期键", "description": "关联dim_date"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "indicator_code", "display_name": "指标编码"},
            {"name": "indicator_name", "display_name": "指标名称"},
            {"name": "indicator_value", "display_name": "指标值"},
            {"name": "target_value", "display_name": "目标值"},
            {"name": "actual_value", "display_name": "实际值"},
            {"name": "variance_value", "display_name": "偏差值"},
            {"name": "variance_ratio", "display_name": "偏差率"},
            {"name": "gross_profit_rate", "display_name": "毛利率"},
            {"name": "collection_rate", "display_name": "收款率"},
            {"name": "receivable_recovery_rate", "display_name": "应收回收率"},
            {"name": "cost_variance_rate", "display_name": "成本偏差率"},
            {"name": "payment_ratio", "display_name": "付款比例"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_project_payment": {
        "display_name": "项目付款事实表",
        "description": "项目付款数据；含应付/已付/未付",
        "columns": [
            {"name": "id", "display_name": "记录ID", "description": "主键"},
            {"name": "project_id", "display_name": "项目ID", "description": "关联dim_project"},
            {"name": "contract_id", "display_name": "合同ID", "description": "关联dim_contract"},
            {"name": "date_key", "display_name": "日期键", "description": "关联dim_date"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "payable_amount", "display_name": "应付金额"},
            {"name": "paid_amount", "display_name": "已付金额"},
            {"name": "unpaid_amount", "display_name": "未付金额"},
            {"name": "approval_status", "display_name": "审批状态"},
            {"name": "approval_amount", "display_name": "批准金额"},
            {"name": "payment_type", "display_name": "付款类型"},
            {"name": "payment_ratio", "display_name": "付款比例"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_project_balance": {
        "display_name": "项目收支事实表",
        "description": "项目收支数据；含项目/公司层面",
        "columns": [
            {"name": "id", "display_name": "记录ID", "description": "主键"},
            {"name": "project_id", "display_name": "项目ID", "description": "关联dim_project"},
            {"name": "date_key", "display_name": "日期键", "description": "关联dim_date"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "subject_code", "display_name": "科目编码"},
            {"name": "subject_name", "display_name": "科目名称"},
            {"name": "project_amount", "display_name": "项目层面金额"},
            {"name": "company_amount", "display_name": "公司层面金额"},
            {"name": "total_amount", "display_name": "合计金额"},
            {"name": "balance_type", "display_name": "收支类型", "description": "收入/支出"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_project_risk": {
        "display_name": "项目风险事实表",
        "description": "项目风险数据；含三色预警",
        "columns": [
            {"name": "id", "display_name": "记录ID", "description": "主键"},
            {"name": "project_id", "display_name": "项目ID", "description": "关联dim_project"},
            {"name": "date_key", "display_name": "日期键", "description": "关联dim_date"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "risk_type", "display_name": "风险类型"},
            {"name": "risk_code", "display_name": "风险编码"},
            {"name": "risk_name", "display_name": "风险名称"},
            {"name": "risk_score", "display_name": "风险分数"},
            {"name": "warning_level", "display_name": "预警级别", "description": "绿/黄/红"},
            {"name": "warning_reason", "display_name": "预警原因"},
            {"name": "risk_description", "display_name": "风险描述"},
            {"name": "response_measure", "display_name": "应对措施"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
}


def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)

    output.print("=== 商务成本本体初始化 ===")
    output.print(f"空间: {space_id}")

    # 1. 创建物理表
    output.print("\n[1/8] 创建物理表...")

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
        ORDER BY (region_id)
    """)
    output.print("OK dim_region")

    s.sql.execute("DROP TABLE IF EXISTS dim_department")
    s.sql.execute("""
        CREATE TABLE dim_department (
            department_id String COMMENT '部门ID',
            department_code String COMMENT '部门编码',
            department_name String COMMENT '部门名称',
            parent_id String COMMENT '上级部门',
            department_level Int8 COMMENT '部门层级',
            status String DEFAULT 'active' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (department_id)
    """)
    output.print("OK dim_department")

    s.sql.execute("DROP TABLE IF EXISTS dim_owner")
    s.sql.execute("""
        CREATE TABLE dim_owner (
            owner_id String COMMENT '业主ID',
            owner_code String COMMENT '业主编码',
            owner_name String COMMENT '业主名称',
            owner_type String COMMENT '业主类型',
            status String DEFAULT 'active' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (owner_id)
    """)
    output.print("OK dim_owner")

    s.sql.execute("DROP TABLE IF EXISTS dim_cost_subject")
    s.sql.execute("""
        CREATE TABLE dim_cost_subject (
            subject_id String COMMENT '科目ID',
            subject_code String COMMENT '科目编码',
            subject_name String COMMENT '科目名称',
            subject_level Int8 COMMENT '科目层级',
            parent_id String COMMENT '上级科目',
            status String DEFAULT 'active' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (subject_id)
    """)
    output.print("OK dim_cost_subject")

    s.sql.execute("DROP TABLE IF EXISTS dim_project")
    s.sql.execute("""
        CREATE TABLE dim_project (
            project_id String COMMENT '项目ID',
            project_code String COMMENT '项目编码',
            project_name String COMMENT '项目名称',
            company_id String COMMENT '公司ID',
            company_name String COMMENT '公司名称',
            section_id String COMMENT '标段ID',
            section_name String COMMENT '标段名称',
            building_area Float64 COMMENT '建筑面积',
            contract_amount Float64 COMMENT '合同金额',
            project_type String COMMENT '项目类型',
            status String DEFAULT '在建' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间',
            updated_at DateTime DEFAULT now() COMMENT '更新时间'
        ) ENGINE = MergeTree()
        ORDER BY (project_id)
    """)
    output.print("OK dim_project")

    s.sql.execute("DROP TABLE IF EXISTS dim_company")
    s.sql.execute("""
        CREATE TABLE dim_company (
            company_id String COMMENT '公司ID',
            company_code String COMMENT '公司编码',
            company_name String COMMENT '公司名称',
            status String DEFAULT 'active' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (company_id)
    """)
    output.print("OK dim_company")

    s.sql.execute("DROP TABLE IF EXISTS dim_supplier")
    s.sql.execute("""
        CREATE TABLE dim_supplier (
            supplier_id String COMMENT '供应商ID',
            supplier_code String COMMENT '供应商编码',
            supplier_name String COMMENT '供应商名称',
            status String DEFAULT 'active' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (supplier_id)
    """)
    output.print("OK dim_supplier")

    s.sql.execute("DROP TABLE IF EXISTS dim_contract")
    s.sql.execute("""
        CREATE TABLE dim_contract (
            contract_id String COMMENT '合同ID',
            contract_code String COMMENT '合同编码',
            contract_name String COMMENT '合同名称',
            project_id String COMMENT '项目ID',
            contract_amount Float64 COMMENT '合同金额',
            status String DEFAULT 'active' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (contract_id)
    """)
    output.print("OK dim_contract")

    s.sql.execute("DROP TABLE IF EXISTS fact_project_output")
    s.sql.execute("""
        CREATE TABLE fact_project_output (
            id String COMMENT '记录ID',
            project_id String COMMENT '项目ID',
            date_key Int32 COMMENT '日期键',
            report_period String COMMENT '报告期间',
            output_value Float64 COMMENT '产值金额',
            output_tax Float64 COMMENT '税金',
            output_without_tax Float64 COMMENT '不含税产值',
            output_type String COMMENT '产值类型',
            output_ratio Float64 COMMENT '产值比例',
            confirm_type String COMMENT '确认类型',
            confirmed_output Float64 COMMENT '已确认产值',
            pending_output Float64 COMMENT '待确认产值',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id)
    """)
    output.print("OK fact_project_output")

    s.sql.execute("DROP TABLE IF EXISTS fact_project_cost")
    s.sql.execute("""
        CREATE TABLE fact_project_cost (
            id String COMMENT '记录ID',
            project_id String COMMENT '项目ID',
            contract_id String COMMENT '合同ID',
            date_key Int32 COMMENT '日期键',
            report_period String COMMENT '报告期间',
            cost_amount Float64 COMMENT '成本金额',
            cost_type String COMMENT '成本类型',
            cost_level1 String COMMENT '成本一级分类',
            cost_level2 String COMMENT '成本二级分类',
            cost_level3 String COMMENT '成本三级分类',
            labor_cost Float64 COMMENT '人工费',
            material_cost Float64 COMMENT '材料费',
            mechanical_cost Float64 COMMENT '机械费',
            other_cost Float64 COMMENT '其他费用',
            target_cost Float64 COMMENT '目标成本',
            variance_amount Float64 COMMENT '偏差金额',
            variance_ratio Float64 COMMENT '偏差率',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id)
    """)
    output.print("OK fact_project_cost")

    s.sql.execute("DROP TABLE IF EXISTS fact_project_indicator")
    s.sql.execute("""
        CREATE TABLE fact_project_indicator (
            id String COMMENT '记录ID',
            project_id String COMMENT '项目ID',
            company_id String COMMENT '公司ID',
            date_key Int32 COMMENT '日期键',
            report_period String COMMENT '报告期间',
            indicator_code String COMMENT '指标编码',
            indicator_name String COMMENT '指标名称',
            indicator_value Float64 COMMENT '指标值',
            target_value Float64 COMMENT '目标值',
            actual_value Float64 COMMENT '实际值',
            variance_value Float64 COMMENT '偏差值',
            variance_ratio Float64 COMMENT '偏差率',
            gross_profit_rate Float64 COMMENT '毛利率',
            collection_rate Float64 COMMENT '收款率',
            receivable_recovery_rate Float64 COMMENT '应收回收率',
            cost_variance_rate Float64 COMMENT '成本偏差率',
            payment_ratio Float64 COMMENT '付款比例',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id)
    """)
    output.print("OK fact_project_indicator")

    s.sql.execute("DROP TABLE IF EXISTS fact_project_payment")
    s.sql.execute("""
        CREATE TABLE fact_project_payment (
            id String COMMENT '记录ID',
            project_id String COMMENT '项目ID',
            contract_id String COMMENT '合同ID',
            date_key Int32 COMMENT '日期键',
            report_period String COMMENT '报告期间',
            payable_amount Float64 COMMENT '应付金额',
            paid_amount Float64 COMMENT '已付金额',
            unpaid_amount Float64 COMMENT '未付金额',
            approval_status String COMMENT '审批状态',
            approval_amount Float64 COMMENT '审批金额',
            payment_type String COMMENT '付款类型',
            payment_ratio Float64 COMMENT '付款比例',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id)
    """)
    output.print("OK fact_project_payment")

    s.sql.execute("DROP TABLE IF EXISTS fact_project_balance")
    s.sql.execute("""
        CREATE TABLE fact_project_balance (
            id String COMMENT '记录ID',
            project_id String COMMENT '项目ID',
            date_key Int32 COMMENT '日期键',
            report_period String COMMENT '报告期间',
            subject_code String COMMENT '科目编码',
            subject_name String COMMENT '科目名称',
            project_amount Float64 COMMENT '项目金额',
            company_amount Float64 COMMENT '公司金额',
            total_amount Float64 COMMENT '总金额',
            balance_type String COMMENT '余额类型',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id)
    """)
    output.print("OK fact_project_balance")

    s.sql.execute("DROP TABLE IF EXISTS fact_project_risk")
    s.sql.execute("""
        CREATE TABLE fact_project_risk (
            id String COMMENT '记录ID',
            project_id String COMMENT '项目ID',
            date_key Int32 COMMENT '日期键',
            report_period String COMMENT '报告期间',
            risk_type String COMMENT '风险类型',
            risk_code String COMMENT '风险编码',
            risk_name String COMMENT '风险名称',
            risk_score Float64 COMMENT '风险评分',
            warning_level String COMMENT '预警等级',
            warning_reason String COMMENT '预警原因',
            risk_description String COMMENT '风险描述',
            response_measure String COMMENT '应对措施',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id)
    """)
    output.print("OK fact_project_risk")

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

    # 3. 注册表间关系（16 条，规划 §3.9）
    output.print("\n[3/8] 注册表间关系...")

    table_relationships = [
        {"from_table": "fact_project_output", "to_table": "dim_date", "join_sql": "fact_project_output.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "产值关联日历"},
        {"from_table": "fact_project_output", "to_table": "dim_project", "join_sql": "fact_project_output.project_id = dim_project.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "产值关联项目"},
        {"from_table": "fact_project_cost", "to_table": "dim_date", "join_sql": "fact_project_cost.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "成本关联日历"},
        {"from_table": "fact_project_cost", "to_table": "dim_project", "join_sql": "fact_project_cost.project_id = dim_project.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "成本关联项目"},
        {"from_table": "fact_project_cost", "to_table": "dim_contract", "join_sql": "fact_project_cost.contract_id = dim_contract.contract_id", "join_keys": [{"from": "contract_id", "to": "contract_id"}], "relationship_type": "many_to_one", "description": "成本关联合同"},
        {"from_table": "fact_project_indicator", "to_table": "dim_date", "join_sql": "fact_project_indicator.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "指标关联日历"},
        {"from_table": "fact_project_indicator", "to_table": "dim_project", "join_sql": "fact_project_indicator.project_id = dim_project.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "指标关联项目"},
        {"from_table": "fact_project_payment", "to_table": "dim_date", "join_sql": "fact_project_payment.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "付款关联日历"},
        {"from_table": "fact_project_payment", "to_table": "dim_project", "join_sql": "fact_project_payment.project_id = dim_project.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "付款关联项目"},
        {"from_table": "fact_project_payment", "to_table": "dim_contract", "join_sql": "fact_project_payment.contract_id = dim_contract.contract_id", "join_keys": [{"from": "contract_id", "to": "contract_id"}], "relationship_type": "many_to_one", "description": "付款关联合同"},
        {"from_table": "fact_project_balance", "to_table": "dim_date", "join_sql": "fact_project_balance.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "收支关联日历"},
        {"from_table": "fact_project_balance", "to_table": "dim_project", "join_sql": "fact_project_balance.project_id = dim_project.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "收支关联项目"},
        {"from_table": "fact_project_risk", "to_table": "dim_date", "join_sql": "fact_project_risk.date_key = dim_date.date_key", "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one", "description": "风险关联日历"},
        {"from_table": "fact_project_risk", "to_table": "dim_project", "join_sql": "fact_project_risk.project_id = dim_project.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "风险关联项目"},
        {"from_table": "dim_project", "to_table": "dim_company", "join_sql": "dim_project.company_id = dim_company.company_id", "join_keys": [{"from": "company_id", "to": "company_id"}], "relationship_type": "many_to_one", "description": "项目关联公司"},
        {"from_table": "dim_contract", "to_table": "dim_project", "join_sql": "dim_contract.project_id = dim_project.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "合同关联项目"},
    ]
    for rel in table_relationships:
        s.tables.add_relationship(**rel)
        output.print(f"OK {rel['from_table']} -> {rel['to_table']}")

    # 4. 注册 Cube
    output.print("\n[4/8] 注册 Cube...")

    # 4.1 主体型 Cube（基于维度表）
    # RegionCube
    s.register_cube(
        name="RegionCube",
        table="dim_region",
        title="地区Cube",
        measures=[
            {"name": "region_count", "col": "region_id", "agg": "count", "title": "地区数量"},
        ],
        dimensions=[
            {"name": "region_id", "col": "region_id", "type": "string", "title": "地区ID"},
            {"name": "region_code", "col": "region_code", "type": "string", "title": "地区编码"},
            {"name": "region_name", "col": "region_name", "type": "string", "title": "地区名称"},
            {"name": "province", "col": "province", "type": "string", "title": "省份"},
            {"name": "city", "col": "city", "type": "string", "title": "城市"},
            {"name": "region_level", "col": "region_level", "type": "string", "title": "大区"},
        ],
    )
    output.print("OK RegionCube")

    # DepartmentCube
    s.register_cube(
        name="DepartmentCube",
        table="dim_department",
        title="部门Cube",
        measures=[
            {"name": "dept_count", "col": "department_id", "agg": "count", "title": "部门数量"},
        ],
        dimensions=[
            {"name": "department_id", "col": "department_id", "type": "string", "title": "部门ID"},
            {"name": "department_code", "col": "department_code", "type": "string", "title": "部门编码"},
            {"name": "department_name", "col": "department_name", "type": "string", "title": "部门名称"},
            {"name": "parent_id", "col": "parent_id", "type": "string", "title": "上级部门ID"},
            {"name": "department_level", "col": "department_level", "type": "int", "title": "部门层级"},
        ],
    )
    output.print("OK DepartmentCube")

    # OwnerCube
    s.register_cube(
        name="OwnerCube",
        table="dim_owner",
        title="业主Cube",
        measures=[
            {"name": "owner_count", "col": "owner_id", "agg": "count", "title": "业主数量"},
        ],
        dimensions=[
            {"name": "owner_id", "col": "owner_id", "type": "string", "title": "业主ID"},
            {"name": "owner_code", "col": "owner_code", "type": "string", "title": "业主编码"},
            {"name": "owner_name", "col": "owner_name", "type": "string", "title": "业主名称"},
            {"name": "owner_type", "col": "owner_type", "type": "string", "title": "业主类型"},
        ],
    )
    output.print("OK OwnerCube")

    # CostSubjectCube
    s.register_cube(
        name="CostSubjectCube",
        table="dim_cost_subject",
        title="成本科目Cube",
        measures=[
            {"name": "subject_count", "col": "subject_id", "agg": "count", "title": "科目数量"},
        ],
        dimensions=[
            {"name": "subject_id", "col": "subject_id", "type": "string", "title": "科目ID"},
            {"name": "subject_code", "col": "subject_code", "type": "string", "title": "科目编码"},
            {"name": "subject_name", "col": "subject_name", "type": "string", "title": "科目名称"},
            {"name": "subject_level", "col": "subject_level", "type": "int", "title": "科目层级"},
            {"name": "parent_id", "col": "parent_id", "type": "string", "title": "上级科目"},
        ],
    )
    output.print("OK CostSubjectCube")

    # ProjectCube
    s.register_cube(
        name="ProjectCube",
        table="dim_project",
        title="项目Cube",
        measures=[
            {"name": "project_count", "col": "project_id", "agg": "count", "title": "项目数量"},
            {"name": "building_area_total", "col": "building_area", "agg": "sum", "title": "建筑面积合计"},
            {"name": "contract_amount_total", "col": "contract_amount", "agg": "sum", "title": "合同金额合计"},
        ],
        dimensions=[
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "project_code", "col": "project_code", "type": "string", "title": "项目编码"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
            {"name": "company_id", "col": "company_id", "type": "string", "title": "公司ID"},
            {"name": "company_name", "col": "company_name", "type": "string", "title": "公司名称"},
            {"name": "project_type", "col": "project_type", "type": "string", "title": "项目类型"},
            {"name": "status", "col": "status", "type": "string", "title": "状态"},
        ],
    )
    output.print("OK ProjectCube")

    # CompanyCube
    s.register_cube(
        name="CompanyCube",
        table="dim_company",
        title="公司Cube",
        measures=[
            {"name": "company_count", "col": "company_id", "agg": "count", "title": "公司数量"},
        ],
        dimensions=[
            {"name": "company_id", "col": "company_id", "type": "string", "title": "公司ID"},
            {"name": "company_code", "col": "company_code", "type": "string", "title": "公司编码"},
            {"name": "company_name", "col": "company_name", "type": "string", "title": "公司名称"},
        ],
    )
    output.print("OK CompanyCube")

    # SupplierCube
    s.register_cube(
        name="SupplierCube",
        table="dim_supplier",
        title="供应商Cube",
        measures=[
            {"name": "supplier_count", "col": "supplier_id", "agg": "count", "title": "供应商数量"},
        ],
        dimensions=[
            {"name": "supplier_id", "col": "supplier_id", "type": "string", "title": "供应商ID"},
            {"name": "supplier_code", "col": "supplier_code", "type": "string", "title": "供应商编码"},
            {"name": "supplier_name", "col": "supplier_name", "type": "string", "title": "供应商名称"},
        ],
    )
    output.print("OK SupplierCube")

    # ContractCube
    s.register_cube(
        name="ContractCube",
        table="dim_contract",
        title="合同Cube",
        measures=[
            {"name": "contract_count", "col": "contract_id", "agg": "count", "title": "合同数量"},
            {"name": "contract_amount_total", "col": "contract_amount", "agg": "sum", "title": "合同金额合计"},
        ],
        dimensions=[
            {"name": "contract_id", "col": "contract_id", "type": "string", "title": "合同ID"},
            {"name": "contract_code", "col": "contract_code", "type": "string", "title": "合同编码"},
            {"name": "contract_name", "col": "contract_name", "type": "string", "title": "合同名称"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
        ],
    )
    output.print("OK ContractCube")

    # 4.2 流程型 Cube（基于事实表）
    # ProjectOutputCube
    s.register_cube(
        name="ProjectOutputCube",
        table="fact_project_output",
        title="项目产值Cube",
        measures=[
            {"name": "output_value", "col": "output_value", "agg": "sum", "title": "产值金额"},
            {"name": "output_tax", "col": "output_tax", "agg": "sum", "title": "税金"},
            {"name": "output_without_tax", "col": "output_without_tax", "agg": "sum", "title": "不含税产值"},
            {"name": "confirmed_output", "col": "confirmed_output", "agg": "sum", "title": "已确认产值"},
            {"name": "pending_output", "col": "pending_output", "agg": "sum", "title": "待确认产值"},
        ],
        dimensions=[
            {"name": "id", "col": "id", "type": "string", "title": "记录ID"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "output_type", "col": "output_type", "type": "string", "title": "产值类型"},
            {"name": "output_ratio", "col": "output_ratio", "type": "float", "title": "产值比例"},
            {"name": "confirm_type", "col": "confirm_type", "type": "string", "title": "确认类型"},
            {"name": "created_at", "col": "created_at", "type": "datetime", "title": "创建时间"},
        ],
    )
    output.print("OK ProjectOutputCube")

    # ProjectCostCube
    s.register_cube(
        name="ProjectCostCube",
        table="fact_project_cost",
        title="项目成本Cube",
        measures=[
            {"name": "cost_amount", "col": "cost_amount", "agg": "sum", "title": "成本金额"},
            {"name": "labor_cost", "col": "labor_cost", "agg": "sum", "title": "人工费"},
            {"name": "material_cost", "col": "material_cost", "agg": "sum", "title": "材料费"},
            {"name": "mechanical_cost", "col": "mechanical_cost", "agg": "sum", "title": "机械费"},
            {"name": "other_cost", "col": "other_cost", "agg": "sum", "title": "其他费用"},
            {"name": "target_cost", "col": "target_cost", "agg": "sum", "title": "目标成本"},
            {"name": "variance_amount", "col": "variance_amount", "agg": "sum", "title": "偏差金额"},
        ],
        dimensions=[
            {"name": "id", "col": "id", "type": "string", "title": "记录ID"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "contract_id", "col": "contract_id", "type": "string", "title": "合同ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "cost_type", "col": "cost_type", "type": "string", "title": "成本类型"},
            {"name": "cost_level1", "col": "cost_level1", "type": "string", "title": "成本一级分类"},
            {"name": "cost_level2", "col": "cost_level2", "type": "string", "title": "成本二级分类"},
            {"name": "cost_level3", "col": "cost_level3", "type": "string", "title": "成本三级分类"},
            {"name": "variance_ratio", "col": "variance_ratio", "type": "float", "title": "偏差率"},
            {"name": "created_at", "col": "created_at", "type": "datetime", "title": "创建时间"},
        ],
    )
    output.print("OK ProjectCostCube")

    # ProjectIndicatorCube
    s.register_cube(
        name="ProjectIndicatorCube",
        table="fact_project_indicator",
        title="项目指标Cube",
        measures=[
            {"name": "indicator_value", "col": "indicator_value", "agg": "sum", "title": "指标值"},
            {"name": "target_value", "col": "target_value", "agg": "sum", "title": "目标值"},
            {"name": "actual_value", "col": "actual_value", "agg": "sum", "title": "实际值"},
            {"name": "variance_value", "col": "variance_value", "agg": "sum", "title": "偏差值"},
            {"name": "gross_profit_rate", "col": "gross_profit_rate", "agg": "avg", "title": "毛利率"},
            {"name": "collection_rate", "col": "collection_rate", "agg": "avg", "title": "收款率"},
            {"name": "receivable_recovery_rate", "col": "receivable_recovery_rate", "agg": "avg", "title": "应收回收率"},
            {"name": "cost_variance_rate", "col": "cost_variance_rate", "agg": "avg", "title": "成本偏差率"},
            {"name": "payment_ratio", "col": "payment_ratio", "agg": "avg", "title": "付款比例"},
        ],
        dimensions=[
            {"name": "id", "col": "id", "type": "string", "title": "记录ID"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "company_id", "col": "company_id", "type": "string", "title": "公司ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "indicator_code", "col": "indicator_code", "type": "string", "title": "指标编码"},
            {"name": "indicator_name", "col": "indicator_name", "type": "string", "title": "指标名称"},
            {"name": "variance_ratio", "col": "variance_ratio", "type": "float", "title": "偏差率"},
            {"name": "created_at", "col": "created_at", "type": "datetime", "title": "创建时间"},
        ],
    )
    output.print("OK ProjectIndicatorCube")

    # ProjectPaymentCube
    s.register_cube(
        name="ProjectPaymentCube",
        table="fact_project_payment",
        title="项目付款Cube",
        measures=[
            {"name": "payable_amount", "col": "payable_amount", "agg": "sum", "title": "应付金额"},
            {"name": "paid_amount", "col": "paid_amount", "agg": "sum", "title": "已付金额"},
            {"name": "unpaid_amount", "col": "unpaid_amount", "agg": "sum", "title": "未付金额"},
            {"name": "approval_amount", "col": "approval_amount", "agg": "sum", "title": "批准金额"},
        ],
        dimensions=[
            {"name": "id", "col": "id", "type": "string", "title": "记录ID"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "contract_id", "col": "contract_id", "type": "string", "title": "合同ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "approval_status", "col": "approval_status", "type": "string", "title": "审批状态"},
            {"name": "payment_type", "col": "payment_type", "type": "string", "title": "付款类型"},
            {"name": "payment_ratio", "col": "payment_ratio", "type": "float", "title": "付款比例"},
            {"name": "created_at", "col": "created_at", "type": "datetime", "title": "创建时间"},
        ],
    )
    output.print("OK ProjectPaymentCube")

    # ProjectBalanceCube
    s.register_cube(
        name="ProjectBalanceCube",
        table="fact_project_balance",
        title="项目收支Cube",
        measures=[
            {"name": "project_amount", "col": "project_amount", "agg": "sum", "title": "项目层面金额"},
            {"name": "company_amount", "col": "company_amount", "agg": "sum", "title": "公司层面金额"},
            {"name": "total_amount", "col": "total_amount", "agg": "sum", "title": "合计金额"},
        ],
        dimensions=[
            {"name": "id", "col": "id", "type": "string", "title": "记录ID"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "subject_code", "col": "subject_code", "type": "string", "title": "科目编码"},
            {"name": "subject_name", "col": "subject_name", "type": "string", "title": "科目名称"},
            {"name": "balance_type", "col": "balance_type", "type": "string", "title": "收支类型"},
            {"name": "created_at", "col": "created_at", "type": "datetime", "title": "创建时间"},
        ],
    )
    output.print("OK ProjectBalanceCube")

    # ProjectRiskCube
    s.register_cube(
        name="ProjectRiskCube",
        table="fact_project_risk",
        title="项目风险Cube",
        measures=[
            {"name": "risk_score", "col": "risk_score", "agg": "sum", "title": "风险分数"},
            {"name": "risk_count", "col": "id", "agg": "count", "title": "风险数量"},
        ],
        dimensions=[
            {"name": "id", "col": "id", "type": "string", "title": "记录ID"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "risk_type", "col": "risk_type", "type": "string", "title": "风险类型"},
            {"name": "risk_code", "col": "risk_code", "type": "string", "title": "风险编码"},
            {"name": "risk_name", "col": "risk_name", "type": "string", "title": "风险名称"},
            {"name": "warning_level", "col": "warning_level", "type": "string", "title": "预警级别"},
            {"name": "warning_reason", "col": "warning_reason", "type": "string", "title": "预警原因"},
            {"name": "risk_description", "col": "risk_description", "type": "string", "title": "风险描述"},
            {"name": "response_measure", "col": "response_measure", "type": "string", "title": "应对措施"},
            {"name": "created_at", "col": "created_at", "type": "datetime", "title": "创建时间"},
        ],
    )
    output.print("OK ProjectRiskCube")

    # 4b. 派生度量
    output.print("\n[4b/8] 配置派生度量...")

    s.upsert_derived_measures(
        "ProjectCostCube",
        [
            {
                "name": "variance_ratio",
                "title": "成本偏差率",
                "expression": "if(ProjectCostCube.target_cost > 0, ProjectCostCube.variance_amount / ProjectCostCube.target_cost, 0)",
                "description": "成本偏差率 = 偏差金额 / 目标成本",
            },
        ],
    )
    output.print("OK ProjectCostCube 派生度量")

    s.upsert_derived_measures(
        "ProjectPaymentCube",
        [
            {
                "name": "payment_ratio",
                "title": "付款比例",
                "expression": "if(ProjectPaymentCube.payable_amount > 0, ProjectPaymentCube.paid_amount / ProjectPaymentCube.payable_amount, 0)",
                "description": "付款比例 = 已付金额 / 应付金额",
            },
        ],
    )
    output.print("OK ProjectPaymentCube 派生度量")

    # 5. 定义对象类型（15 种，规划 §5.1）
    output.print("\n[5/8] 定义对象类型...")

    s.onto.define_object_type(
        code="Region",
        name="地区",
        description="省市区大区层级主数据",
        category_347="主数据",
    )
    s.onto.bind_source("Region", "dazi_cube", config={"cube": "RegionCube"})
    output.print("OK Region")

    s.onto.define_object_type(
        code="Department",
        name="部门",
        description="组织架构主数据",
        category_347="主数据",
    )
    s.onto.bind_source("Department", "dazi_cube", config={"cube": "DepartmentCube"})
    output.print("OK Department")

    s.onto.define_object_type(
        code="Owner",
        name="业主",
        description="业主主数据",
        category_347="主数据",
    )
    s.onto.bind_source("Owner", "dazi_cube", config={"cube": "OwnerCube"})
    output.print("OK Owner")

    s.onto.define_object_type(
        code="CostSubject",
        name="成本科目",
        description="成本分类科目主数据",
        category_347="主数据",
    )
    s.onto.bind_source("CostSubject", "dazi_cube", config={"cube": "CostSubjectCube"})
    output.print("OK CostSubject")

    s.onto.define_object_type(
        code="Project",
        name="项目",
        description="项目主数据",
        category_347="主数据",
    )
    s.onto.bind_source("Project", "dazi_cube", config={"cube": "ProjectCube"})
    output.print("OK Project")

    s.onto.define_object_type(
        code="Company",
        name="公司",
        description="公司主数据",
        category_347="主数据",
    )
    s.onto.bind_source("Company", "dazi_cube", config={"cube": "CompanyCube"})
    output.print("OK Company")

    s.onto.define_object_type(
        code="Supplier",
        name="供应商",
        description="供应商主数据",
        category_347="主数据",
    )
    s.onto.bind_source("Supplier", "dazi_cube", config={"cube": "SupplierCube"})
    output.print("OK Supplier")

    s.onto.define_object_type(
        code="Contract",
        name="合同",
        description="合同主数据",
        category_347="主数据",
    )
    s.onto.bind_source("Contract", "dazi_cube", config={"cube": "ContractCube"})
    output.print("OK Contract")

    s.onto.define_object_type(
        code="ProjectOutput",
        name="项目产值",
        description="项目产值事务对象",
        category_347="事务",
    )
    s.onto.bind_source("ProjectOutput", "dazi_cube", config={"cube": "ProjectOutputCube"})
    output.print("OK ProjectOutput")

    s.onto.define_object_type(
        code="ProjectCost",
        name="项目成本",
        description="项目成本事务对象",
        category_347="事务",
    )
    s.onto.bind_source("ProjectCost", "dazi_cube", config={"cube": "ProjectCostCube"})
    output.print("OK ProjectCost")

    s.onto.define_object_type(
        code="ProjectIndicator",
        name="项目指标",
        description="项目指标事务对象",
        category_347="事务",
    )
    s.onto.bind_source("ProjectIndicator", "dazi_cube", config={"cube": "ProjectIndicatorCube"})
    output.print("OK ProjectIndicator")

    s.onto.define_object_type(
        code="ProjectPayment",
        name="项目付款",
        description="项目付款事务对象",
        category_347="事务",
    )
    s.onto.bind_source("ProjectPayment", "dazi_cube", config={"cube": "ProjectPaymentCube"})
    output.print("OK ProjectPayment")

    s.onto.define_object_type(
        code="ProjectBalance",
        name="项目收支",
        description="项目收支事务对象",
        category_347="事务",
    )
    s.onto.bind_source("ProjectBalance", "dazi_cube", config={"cube": "ProjectBalanceCube"})
    output.print("OK ProjectBalance")

    s.onto.define_object_type(
        code="ProjectRisk",
        name="项目风险",
        description="项目风险事务对象",
        category_347="事务",
    )
    s.onto.bind_source("ProjectRisk", "dazi_cube", config={"cube": "ProjectRiskCube"})
    output.print("OK ProjectRisk")

    # 6. 定义属性（规划 §5.2）
    output.print("\n[6/8] 定义对象属性...")

    # 主数据对象属性
    s.onto.define_property("Region", "id", "地区ID", semantic_role="dimension", qualified_name="RegionCube.region_id")
    s.onto.define_property("Region", "name", "地区名称", semantic_role="dimension", qualified_name="RegionCube.region_name")
    s.onto.define_property("Region", "province", "省份", semantic_role="dimension", qualified_name="RegionCube.province")

    s.onto.define_property("Department", "id", "部门ID", semantic_role="dimension", qualified_name="DepartmentCube.department_id")
    s.onto.define_property("Department", "name", "部门名称", semantic_role="dimension", qualified_name="DepartmentCube.department_name")

    s.onto.define_property("Owner", "id", "业主ID", semantic_role="dimension", qualified_name="OwnerCube.owner_id")
    s.onto.define_property("Owner", "name", "业主名称", semantic_role="dimension", qualified_name="OwnerCube.owner_name")
    s.onto.define_property("Owner", "type", "业主类型", semantic_role="dimension", qualified_name="OwnerCube.owner_type")

    s.onto.define_property("CostSubject", "id", "科目ID", semantic_role="dimension", qualified_name="CostSubjectCube.subject_id")
    s.onto.define_property("CostSubject", "name", "科目名称", semantic_role="dimension", qualified_name="CostSubjectCube.subject_name")

    s.onto.define_property("Project", "id", "项目ID", semantic_role="dimension", qualified_name="ProjectCube.project_id")
    s.onto.define_property("Project", "code", "项目编码", semantic_role="dimension", qualified_name="ProjectCube.project_code")
    s.onto.define_property("Project", "name", "项目名称", semantic_role="dimension", qualified_name="ProjectCube.project_name")
    s.onto.define_property("Project", "contract_amount", "合同金额", semantic_role="measure", qualified_name="ProjectCube.contract_amount_total")
    s.onto.define_property("Project", "status", "项目状态", semantic_role="dimension", qualified_name="ProjectCube.status")

    s.onto.define_property("Company", "id", "公司ID", semantic_role="dimension", qualified_name="CompanyCube.company_id")
    s.onto.define_property("Company", "name", "公司名称", semantic_role="dimension", qualified_name="CompanyCube.company_name")

    s.onto.define_property("Supplier", "id", "供应商ID", semantic_role="dimension", qualified_name="SupplierCube.supplier_id")
    s.onto.define_property("Supplier", "name", "供应商名称", semantic_role="dimension", qualified_name="SupplierCube.supplier_name")

    s.onto.define_property("Contract", "id", "合同ID", semantic_role="dimension", qualified_name="ContractCube.contract_id")
    s.onto.define_property("Contract", "name", "合同名称", semantic_role="dimension", qualified_name="ContractCube.contract_name")
    s.onto.define_property("Contract", "amount", "合同金额", semantic_role="measure", qualified_name="ContractCube.contract_amount_total")

    # 事务对象属性
    s.onto.define_property("ProjectOutput", "id", "记录ID", semantic_role="dimension", qualified_name="ProjectOutputCube.id")
    s.onto.define_property("ProjectOutput", "project_id", "项目ID", semantic_role="dimension", qualified_name="ProjectOutputCube.project_id")
    s.onto.define_property("ProjectOutput", "output_value", "产值金额", semantic_role="measure", qualified_name="ProjectOutputCube.output_value")
    s.onto.define_property("ProjectOutput", "confirmed_output", "已确认产值", semantic_role="measure", qualified_name="ProjectOutputCube.confirmed_output")
    s.onto.define_property("ProjectOutput", "pending_output", "待确认产值", semantic_role="measure", qualified_name="ProjectOutputCube.pending_output")
    s.onto.define_property("ProjectOutput", "output_type", "产值类型", semantic_role="dimension", qualified_name="ProjectOutputCube.output_type")
    s.onto.define_property("ProjectOutput", "report_period", "报告期间", semantic_role="dimension", qualified_name="ProjectOutputCube.report_period")

    s.onto.define_property("ProjectCost", "id", "记录ID", semantic_role="dimension", qualified_name="ProjectCostCube.id")
    s.onto.define_property("ProjectCost", "project_id", "项目ID", semantic_role="dimension", qualified_name="ProjectCostCube.project_id")
    s.onto.define_property("ProjectCost", "cost_amount", "成本金额", semantic_role="measure", qualified_name="ProjectCostCube.cost_amount")
    s.onto.define_property("ProjectCost", "labor_cost", "人工费", semantic_role="measure", qualified_name="ProjectCostCube.labor_cost")
    s.onto.define_property("ProjectCost", "material_cost", "材料费", semantic_role="measure", qualified_name="ProjectCostCube.material_cost")
    s.onto.define_property("ProjectCost", "variance_ratio", "成本偏差率", semantic_role="measure", qualified_name="ProjectCostCube.variance_ratio")
    s.onto.define_property("ProjectCost", "report_period", "报告期间", semantic_role="dimension", qualified_name="ProjectCostCube.report_period")

    s.onto.define_property("ProjectIndicator", "id", "记录ID", semantic_role="dimension", qualified_name="ProjectIndicatorCube.id")
    s.onto.define_property("ProjectIndicator", "project_id", "项目ID", semantic_role="dimension", qualified_name="ProjectIndicatorCube.project_id")
    s.onto.define_property("ProjectIndicator", "gross_profit_rate", "毛利率", semantic_role="measure", qualified_name="ProjectIndicatorCube.gross_profit_rate")
    s.onto.define_property("ProjectIndicator", "collection_rate", "收款率", semantic_role="measure", qualified_name="ProjectIndicatorCube.collection_rate")
    s.onto.define_property("ProjectIndicator", "cost_variance_rate", "成本偏差率", semantic_role="measure", qualified_name="ProjectIndicatorCube.cost_variance_rate")
    s.onto.define_property("ProjectIndicator", "report_period", "报告期间", semantic_role="dimension", qualified_name="ProjectIndicatorCube.report_period")

    s.onto.define_property("ProjectPayment", "id", "记录ID", semantic_role="dimension", qualified_name="ProjectPaymentCube.id")
    s.onto.define_property("ProjectPayment", "project_id", "项目ID", semantic_role="dimension", qualified_name="ProjectPaymentCube.project_id")
    s.onto.define_property("ProjectPayment", "payable_amount", "应付金额", semantic_role="measure", qualified_name="ProjectPaymentCube.payable_amount")
    s.onto.define_property("ProjectPayment", "paid_amount", "已付金额", semantic_role="measure", qualified_name="ProjectPaymentCube.paid_amount")
    s.onto.define_property("ProjectPayment", "payment_ratio", "付款比例", semantic_role="measure", qualified_name="ProjectPaymentCube.payment_ratio")
    s.onto.define_property("ProjectPayment", "report_period", "报告期间", semantic_role="dimension", qualified_name="ProjectPaymentCube.report_period")

    s.onto.define_property("ProjectBalance", "id", "记录ID", semantic_role="dimension", qualified_name="ProjectBalanceCube.id")
    s.onto.define_property("ProjectBalance", "project_id", "项目ID", semantic_role="dimension", qualified_name="ProjectBalanceCube.project_id")
    s.onto.define_property("ProjectBalance", "total_amount", "合计金额", semantic_role="measure", qualified_name="ProjectBalanceCube.total_amount")
    s.onto.define_property("ProjectBalance", "balance_type", "收支类型", semantic_role="dimension", qualified_name="ProjectBalanceCube.balance_type")
    s.onto.define_property("ProjectBalance", "report_period", "报告期间", semantic_role="dimension", qualified_name="ProjectBalanceCube.report_period")

    s.onto.define_property("ProjectRisk", "id", "记录ID", semantic_role="dimension", qualified_name="ProjectRiskCube.id")
    s.onto.define_property("ProjectRisk", "project_id", "项目ID", semantic_role="dimension", qualified_name="ProjectRiskCube.project_id")
    s.onto.define_property("ProjectRisk", "risk_score", "风险分数", semantic_role="measure", qualified_name="ProjectRiskCube.risk_score")
    s.onto.define_property("ProjectRisk", "warning_level", "预警级别", semantic_role="dimension", qualified_name="ProjectRiskCube.warning_level")
    s.onto.define_property("ProjectRisk", "risk_type", "风险类型", semantic_role="dimension", qualified_name="ProjectRiskCube.risk_type")
    s.onto.define_property("ProjectRisk", "report_period", "报告期间", semantic_role="dimension", qualified_name="ProjectRiskCube.report_period")

    output.print("OK 属性定义完成")

    # 7. 定义链接类型（12 种，规划 §5.2）
    output.print("\n[7/8] 定义链接类型...")

    s.onto.define_link_type(code="belongsTo_ProjectOutput_Project", name="产值归属项目", from_object_type_code="ProjectOutput", to_object_type_code="Project", category_347="归属关系")
    s.onto.define_link_type(code="belongsTo_ProjectCost_Project", name="成本归属项目", from_object_type_code="ProjectCost", to_object_type_code="Project", category_347="归属关系")
    s.onto.define_link_type(code="belongsTo_ProjectPayment_Project", name="付款归属项目", from_object_type_code="ProjectPayment", to_object_type_code="Project", category_347="归属关系")
    s.onto.define_link_type(code="belongsTo_ProjectBalance_Project", name="收支归属项目", from_object_type_code="ProjectBalance", to_object_type_code="Project", category_347="归属关系")
    s.onto.define_link_type(code="belongsTo_ProjectIndicator_Project", name="指标归属项目", from_object_type_code="ProjectIndicator", to_object_type_code="Project", category_347="归属关系")
    s.onto.define_link_type(code="belongsTo_ProjectRisk_Project", name="风险归属项目", from_object_type_code="ProjectRisk", to_object_type_code="Project", category_347="归属关系")
    s.onto.define_link_type(code="belongsTo_Contract_Project", name="合同归属项目", from_object_type_code="Contract", to_object_type_code="Project", category_347="归属关系")
    s.onto.define_link_type(code="belongsTo_Project_Company", name="项目归属公司", from_object_type_code="Project", to_object_type_code="Company", category_347="归属关系")
    s.onto.define_link_type(code="belongsTo_Supplier_Company", name="供应商归属公司", from_object_type_code="Supplier", to_object_type_code="Company", category_347="归属关系")
    s.onto.define_link_type(code="contains_ProjectCost_Contract", name="成本包含合同", from_object_type_code="ProjectCost", to_object_type_code="Contract", category_347="归属关系")
    s.onto.define_link_type(code="contains_ProjectPayment_Contract", name="付款包含合同", from_object_type_code="ProjectPayment", to_object_type_code="Contract", category_347="归属关系")

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
        "cubes": 15,
        "objects": 15,
        "links": 11,
    }
    output.success("商务成本本体初始化完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))