"""Panda Cost Analysis Ontology Initialization Script for space__panda_cost01

初始化内容：
1. 创建物理表（6张）
2. 注册Cube（6个）
3. 添加派生度量
4. 定义对象类型（10种）
5. 绑定数据源
6. 定义属性
7. 定义链接类型（11种）
8. 同步指标引用

参考文档：
- 项目/潘达工程-商务成本/规划/130-阶段三-本体设计与确认/020-本体规划文档.md
- 资源/docs/onto/dazi_script_sdk_reference.md
"""

import json


def main():
    space_id = "space__panda_cost01"
    s = space.get(space_id)

    output.print("=== Start Panda Cost Analysis Ontology Initialization ===")
    output.print(f"Space: {space_id}")

    # 1. 创建物理表
    output.print("\n[1/8] Creating physical tables...")

    # 1.1 项目基础信息表
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS tb_project_indicator (
            id String,
            project_id String,
            project_name String,
            project_code String,
            company_id String,
            company_name String,
            section_id String,
            section_name String,
            building_area Float64,
            contract_amount Float64,
            report_period String,
            indicator_code String,
            indicator_name String,
            indicator_value Float64,
            target_value Float64,
            warning_level String,
            remark String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_id, report_period)
    """)
    output.print("OK tb_project_indicator")

    # 1.2 项目产值表
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS tb_project_output (
            id String,
            project_id String,
            report_period String,
            confirmed_output Float64,
            unconfirmed_output Float64,
            total_output Float64,
            last_year_confirmed Float64,
            last_year_unconfirmed Float64,
            current_confirmed Float64,
            current_unconfirmed Float64,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_id, report_period)
    """)
    output.print("OK tb_project_output")

    # 1.3 项目成本表
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS tb_project_cost (
            id String,
            project_id String,
            report_period String,
            confirmed_cost_acc Float64,
            unconfirmed_cost_acc Float64,
            confirmed_cost_cmonth Float64,
            unconfirmed_cost_cmonth Float64,
            labor_cost_acc Float64,
            material_cost_acc Float64,
            equipment_cost_acc Float64,
            management_fee_rate Float64,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_id, report_period)
    """)
    output.print("OK tb_project_cost")

    # 1.4 项目付款表
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS tb_project_payment (
            id String,
            project_id String,
            contract_id String,
            contract_code String,
            contract_name String,
            contract_content String,
            supplier_name String,
            supplier_type String,
            contract_amount Float64,
            report_period String,
            payable_confirmed Float64,
            labor_payable Float64,
            paid_amount Float64,
            payable_unconfirmed Float64,
            payment_ratio Float64,
            tax_rate Float64,
            settlement_status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_id, report_period)
    """)
    output.print("OK tb_project_payment")

    # 1.5 项目收支表
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS tb_project_balance (
            id String,
            project_id String,
            report_period String,
            subject_code String,
            subject_name String,
            project_amount Float64,
            company_amount Float64,
            total_amount Float64,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_id, report_period)
    """)
    output.print("OK tb_project_balance")

    # 1.6 项目风险表
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS tb_project_risk (
            id String,
            project_id String,
            report_period String,
            risk_type String,
            risk_code String,
            risk_name String,
            risk_value Int32,
            warning_level String,
            risk_description String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_id, report_period)
    """)
    output.print("OK tb_project_risk")

    # 2. 注册表到空间
    output.print("\n[2/8] Registering tables to space...")

    tables = [
        ("tb_project_indicator", "项目指标表"),
        ("tb_project_output", "项目产值表"),
        ("tb_project_cost", "项目成本表"),
        ("tb_project_payment", "项目付款表"),
        ("tb_project_balance", "项目收支表"),
        ("tb_project_risk", "项目风险表"),
    ]

    for table_name, label in tables:
        s.tables.register(table_name, label=label)
        s.tables.sync_columns(table_name)
        output.print(f"OK {table_name} registered")

    # 3. 注册Cube
    output.print("\n[3/8] Registering Cubes...")

    # 3.1 ProjectIndicatorCube
    s.register_cube(
        name="ProjectIndicatorCube",
        table="tb_project_indicator",
        title="项目指标Cube",
        measures=[
            {"name": "building_area", "col": "building_area", "agg": "sum", "title": "建筑面积"},
            {"name": "contract_amount", "col": "contract_amount", "agg": "sum", "title": "合同金额"},
            {"name": "indicator_value", "col": "indicator_value", "agg": "sum", "title": "指标值"},
            {"name": "target_value", "col": "target_value", "agg": "sum", "title": "目标值"},
        ],
        dimensions=[
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
            {"name": "project_code", "col": "project_code", "type": "string", "title": "项目编码"},
            {"name": "company_id", "col": "company_id", "type": "string", "title": "分公司ID"},
            {"name": "company_name", "col": "company_name", "type": "string", "title": "分公司名称"},
            {"name": "section_id", "col": "section_id", "type": "string", "title": "标段ID"},
            {"name": "section_name", "col": "section_name", "type": "string", "title": "标段名称"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "indicator_code", "col": "indicator_code", "type": "string", "title": "指标编码"},
            {"name": "indicator_name", "col": "indicator_name", "type": "string", "title": "指标名称"},
            {"name": "warning_level", "col": "warning_level", "type": "string", "title": "预警级别"},
        ],
    )
    output.print("OK ProjectIndicatorCube registered")

    # 3.2 ProjectOutputCube
    s.register_cube(
        name="ProjectOutputCube",
        table="tb_project_output",
        title="项目产值Cube",
        measures=[
            {"name": "confirmed_output", "col": "confirmed_output", "agg": "sum", "title": "已确认产值"},
            {"name": "unconfirmed_output", "col": "unconfirmed_output", "agg": "sum", "title": "待确认产值"},
            {"name": "total_output", "col": "total_output", "agg": "sum", "title": "总产值"},
            {"name": "last_year_confirmed", "col": "last_year_confirmed", "agg": "sum", "title": "上年已确认"},
            {"name": "last_year_unconfirmed", "col": "last_year_unconfirmed", "agg": "sum", "title": "上年待确认"},
            {"name": "current_confirmed", "col": "current_confirmed", "agg": "sum", "title": "本年已确认"},
            {"name": "current_unconfirmed", "col": "current_unconfirmed", "agg": "sum", "title": "本年待确认"},
        ],
        dimensions=[
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
        ],
    )
    output.print("OK ProjectOutputCube registered")

    # 3.3 ProjectCostCube
    s.register_cube(
        name="ProjectCostCube",
        table="tb_project_cost",
        title="项目成本Cube",
        measures=[
            {"name": "confirmed_cost_acc", "col": "confirmed_cost_acc", "agg": "sum", "title": "累计已确认成本"},
            {"name": "unconfirmed_cost_acc", "col": "unconfirmed_cost_acc", "agg": "sum", "title": "累计待确认成本"},
            {"name": "confirmed_cost_cmonth", "col": "confirmed_cost_cmonth", "agg": "sum", "title": "本月已确认成本"},
            {"name": "unconfirmed_cost_cmonth", "col": "unconfirmed_cost_cmonth", "agg": "sum", "title": "本月待确认成本"},
            {"name": "labor_cost_acc", "col": "labor_cost_acc", "agg": "sum", "title": "累计人工费"},
            {"name": "material_cost_acc", "col": "material_cost_acc", "agg": "sum", "title": "累计材料费"},
            {"name": "equipment_cost_acc", "col": "equipment_cost_acc", "agg": "sum", "title": "累计设备费"},
        ],
        dimensions=[
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
        ],
    )
    output.print("OK ProjectCostCube registered")

    # 3.4 ProjectPaymentCube
    s.register_cube(
        name="ProjectPaymentCube",
        table="tb_project_payment",
        title="项目付款Cube",
        measures=[
            {"name": "contract_amount", "col": "contract_amount", "agg": "sum", "title": "合同金额"},
            {"name": "payable_confirmed", "col": "payable_confirmed", "agg": "sum", "title": "已确应付款"},
            {"name": "labor_payable", "col": "labor_payable", "agg": "sum", "title": "人工费应付款"},
            {"name": "paid_amount", "col": "paid_amount", "agg": "sum", "title": "已付款金额"},
            {"name": "payable_unconfirmed", "col": "payable_unconfirmed", "agg": "sum", "title": "待确应付款"},
        ],
        dimensions=[
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "contract_id", "col": "contract_id", "type": "string", "title": "合同ID"},
            {"name": "contract_code", "col": "contract_code", "type": "string", "title": "合同编码"},
            {"name": "contract_name", "col": "contract_name", "type": "string", "title": "合同名称"},
            {"name": "supplier_name", "col": "supplier_name", "type": "string", "title": "供应商名称"},
            {"name": "supplier_type", "col": "supplier_type", "type": "string", "title": "供应商类型"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "settlement_status", "col": "settlement_status", "type": "string", "title": "结算状态"},
        ],
    )
    output.print("OK ProjectPaymentCube registered")

    # 3.5 ProjectBalanceCube
    s.register_cube(
        name="ProjectBalanceCube",
        table="tb_project_balance",
        title="项目收支Cube",
        measures=[
            {"name": "project_amount", "col": "project_amount", "agg": "sum", "title": "项目层面金额"},
            {"name": "company_amount", "col": "company_amount", "agg": "sum", "title": "公司层面金额"},
            {"name": "total_amount", "col": "total_amount", "agg": "sum", "title": "合计金额"},
        ],
        dimensions=[
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "subject_code", "col": "subject_code", "type": "string", "title": "科目编码"},
            {"name": "subject_name", "col": "subject_name", "type": "string", "title": "科目名称"},
        ],
    )
    output.print("OK ProjectBalanceCube registered")

    # 3.6 ProjectRiskCube
    s.register_cube(
        name="ProjectRiskCube",
        table="tb_project_risk",
        title="项目风险Cube",
        measures=[
            {"name": "risk_value", "col": "risk_value", "agg": "avg", "title": "风险值"},
        ],
        dimensions=[
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "risk_type", "col": "risk_type", "type": "string", "title": "风险类型"},
            {"name": "risk_code", "col": "risk_code", "type": "string", "title": "风险编码"},
            {"name": "risk_name", "col": "risk_name", "type": "string", "title": "风险名称"},
            {"name": "warning_level", "col": "warning_level", "type": "string", "title": "预警级别"},
        ],
    )
    output.print("OK ProjectRiskCube registered")

    # 4. 添加派生度量
    output.print("\n[4/8] Adding derived measures...")

    # ProjectOutputCube派生度量
    s.upsert_derived_measures(
        "ProjectOutputCube",
        [
            {
                "name": "confirmed_ratio",
                "title": "确认率",
                "expression": "if(ProjectOutputCube.total_output > 0, ProjectOutputCube.confirmed_output / ProjectOutputCube.total_output, 0)",
                "description": "已确认产值占总产值比例"
            }
        ]
    )
    output.print("OK ProjectOutputCube derived measures")

    # ProjectCostCube派生度量
    s.upsert_derived_measures(
        "ProjectCostCube",
        [
            {
                "name": "total_cost_acc",
                "title": "累计总成本",
                "expression": "ProjectCostCube.confirmed_cost_acc + ProjectCostCube.unconfirmed_cost_acc",
                "description": "累计总成本"
            },
            {
                "name": "cost_ratio",
                "title": "成本刚性度",
                "expression": "if(ProjectCostCube.total_cost_acc > 0, ProjectCostCube.confirmed_cost_acc / ProjectCostCube.total_cost_acc, 0)",
                "description": "已确认成本占总成本比例"
            }
        ]
    )
    output.print("OK ProjectCostCube derived measures")

    # ProjectPaymentCube派生度量
    s.upsert_derived_measures(
        "ProjectPaymentCube",
        [
            {
                "name": "payable_ratio",
                "title": "应付款比例",
                "expression": "if(ProjectPaymentCube.contract_amount > 0, ProjectPaymentCube.payable_confirmed / ProjectPaymentCube.contract_amount, 0)",
                "description": "应付款占合同金额比例"
            },
            {
                "name": "paid_ratio",
                "title": "付款完成率",
                "expression": "if(ProjectPaymentCube.payable_confirmed > 0, ProjectPaymentCube.paid_amount / ProjectPaymentCube.payable_confirmed, 0)",
                "description": "已付款占应付款比例"
            }
        ]
    )
    output.print("OK ProjectPaymentCube derived measures")

    # 5. 定义对象类型
    output.print("\n[5/8] Defining object types...")

    object_types = [
        ("Project", "项目", "项目业务对象"),
        ("ProjectOutput", "项目产值", "项目产值数据"),
        ("ProjectCost", "项目成本", "项目成本数据"),
        ("ProjectPayment", "项目付款", "项目付款数据"),
        ("ProjectBalance", "项目收支", "项目收支数据"),
        ("ProjectIndicator", "项目指标", "项目指标数据"),
        ("ProjectRisk", "项目风险", "项目风险数据"),
        ("Contract", "合同", "合同业务对象"),
        ("Supplier", "供应商", "供应商业务对象"),
        ("Company", "分公司", "分公司业务对象"),
    ]

    for code, name, desc in object_types:
        s.onto.define_object_type(code, name, description=desc)
        output.print(f"OK {code}")

    # 6. 绑定数据源
    output.print("\n[6/8] Binding data sources...")

    s.onto.bind_source("Project", "dazi_cube", config={"cube": "ProjectIndicatorCube"})
    output.print("OK Project -> ProjectIndicatorCube")

    s.onto.bind_source("ProjectOutput", "dazi_cube", config={"cube": "ProjectOutputCube"})
    output.print("OK ProjectOutput -> ProjectOutputCube")

    s.onto.bind_source("ProjectCost", "dazi_cube", config={"cube": "ProjectCostCube"})
    output.print("OK ProjectCost -> ProjectCostCube")

    s.onto.bind_source("ProjectPayment", "dazi_cube", config={"cube": "ProjectPaymentCube"})
    output.print("OK ProjectPayment -> ProjectPaymentCube")

    s.onto.bind_source("ProjectBalance", "dazi_cube", config={"cube": "ProjectBalanceCube"})
    output.print("OK ProjectBalance -> ProjectBalanceCube")

    s.onto.bind_source("ProjectIndicator", "dazi_cube", config={"cube": "ProjectIndicatorCube"})
    output.print("OK ProjectIndicator -> ProjectIndicatorCube")

    s.onto.bind_source("ProjectRisk", "dazi_cube", config={"cube": "ProjectRiskCube"})
    output.print("OK ProjectRisk -> ProjectRiskCube")

    s.onto.bind_source("Contract", "dazi_cube", config={"cube": "ProjectPaymentCube"})
    output.print("OK Contract -> ProjectPaymentCube")

    s.onto.bind_source("Supplier", "dazi_cube", config={"cube": "ProjectPaymentCube"})
    output.print("OK Supplier -> ProjectPaymentCube")

    s.onto.bind_source("Company", "dazi_cube", config={"cube": "ProjectIndicatorCube"})
    output.print("OK Company -> ProjectIndicatorCube")

    # 7. 定义属性
    output.print("\n[7/8] Defining properties...")

    # Project属性
    project_props = [
        ("id", "项目ID", "dimension", "ProjectIndicatorCube.project_id"),
        ("name", "项目名称", "dimension", "ProjectIndicatorCube.project_name"),
        ("code", "项目编码", "dimension", "ProjectIndicatorCube.project_code"),
        ("companyId", "分公司ID", "dimension", "ProjectIndicatorCube.company_id"),
        ("companyName", "分公司名称", "dimension", "ProjectIndicatorCube.company_name"),
        ("sectionId", "标段ID", "dimension", "ProjectIndicatorCube.section_id"),
        ("sectionName", "标段名称", "dimension", "ProjectIndicatorCube.section_name"),
        ("buildingArea", "建筑面积", "measure", "ProjectIndicatorCube.building_area"),
        ("contractAmount", "合同金额", "measure", "ProjectIndicatorCube.contract_amount"),
        ("reportPeriod", "报告期间", "dimension", "ProjectIndicatorCube.report_period"),
    ]
    for code, name, role, qn in project_props:
        s.onto.define_property("Project", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK Project properties (10)")

    # ProjectOutput属性
    output_props = [
        ("id", "产值记录ID", "dimension", "ProjectOutputCube.id"),
        ("projectId", "项目ID", "dimension", "ProjectOutputCube.project_id"),
        ("reportPeriod", "报告期间", "dimension", "ProjectOutputCube.report_period"),
        ("outputConfirmed", "已确认产值", "measure", "ProjectOutputCube.confirmed_output"),
        ("outputUnconfirmed", "待确认产值", "measure", "ProjectOutputCube.unconfirmed_output"),
        ("outputTotal", "总产值", "measure", "ProjectOutputCube.total_output"),
        ("confirmedRatio", "确认率", "measure", "ProjectOutputCube.confirmed_ratio"),
    ]
    for code, name, role, qn in output_props:
        s.onto.define_property("ProjectOutput", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK ProjectOutput properties (7)")

    # ProjectCost属性
    cost_props = [
        ("id", "成本记录ID", "dimension", "ProjectCostCube.id"),
        ("projectId", "项目ID", "dimension", "ProjectCostCube.project_id"),
        ("reportPeriod", "报告期间", "dimension", "ProjectCostCube.report_period"),
        ("costConfirmedAcc", "累计已确认成本", "measure", "ProjectCostCube.confirmed_cost_acc"),
        ("costUnconfirmedAcc", "累计待确认成本", "measure", "ProjectCostCube.unconfirmed_cost_acc"),
        ("costConfirmedCmonth", "本月已确认成本", "measure", "ProjectCostCube.confirmed_cost_cmonth"),
        ("costUnconfirmedCmonth", "本月待确认成本", "measure", "ProjectCostCube.unconfirmed_cost_cmonth"),
        ("laborCostAcc", "累计人工费", "measure", "ProjectCostCube.labor_cost_acc"),
        ("materialCostAcc", "累计材料费", "measure", "ProjectCostCube.material_cost_acc"),
        ("equipmentCostAcc", "累计设备费", "measure", "ProjectCostCube.equipment_cost_acc"),
        ("costRatio", "成本刚性度", "measure", "ProjectCostCube.cost_ratio"),
    ]
    for code, name, role, qn in cost_props:
        s.onto.define_property("ProjectCost", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK ProjectCost properties (11)")

    # ProjectPayment属性
    payment_props = [
        ("id", "付款记录ID", "dimension", "ProjectPaymentCube.id"),
        ("projectId", "项目ID", "dimension", "ProjectPaymentCube.project_id"),
        ("contractId", "合同ID", "dimension", "ProjectPaymentCube.contract_id"),
        ("reportPeriod", "报告期间", "dimension", "ProjectPaymentCube.report_period"),
        ("payableConfirmed", "已确应付款", "measure", "ProjectPaymentCube.payable_confirmed"),
        ("laborPayable", "人工费应付款", "measure", "ProjectPaymentCube.labor_payable"),
        ("paidAmount", "已付款金额", "measure", "ProjectPaymentCube.paid_amount"),
        ("payableUnconfirmed", "待确应付款", "measure", "ProjectPaymentCube.payable_unconfirmed"),
        ("payableRatio", "应付款比例", "measure", "ProjectPaymentCube.payable_ratio"),
        ("paidRatio", "付款完成率", "measure", "ProjectPaymentCube.paid_ratio"),
    ]
    for code, name, role, qn in payment_props:
        s.onto.define_property("ProjectPayment", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK ProjectPayment properties (10)")

    # ProjectBalance属性
    balance_props = [
        ("id", "收支记录ID", "dimension", "ProjectBalanceCube.id"),
        ("projectId", "项目ID", "dimension", "ProjectBalanceCube.project_id"),
        ("reportPeriod", "报告期间", "dimension", "ProjectBalanceCube.report_period"),
        ("subjectCode", "科目编码", "dimension", "ProjectBalanceCube.subject_code"),
        ("subjectName", "科目名称", "dimension", "ProjectBalanceCube.subject_name"),
        ("projectAmount", "项目层面金额", "measure", "ProjectBalanceCube.project_amount"),
        ("companyAmount", "公司层面金额", "measure", "ProjectBalanceCube.company_amount"),
        ("totalAmount", "合计金额", "measure", "ProjectBalanceCube.total_amount"),
    ]
    for code, name, role, qn in balance_props:
        s.onto.define_property("ProjectBalance", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK ProjectBalance properties (8)")

    # ProjectIndicator属性
    indicator_props = [
        ("id", "指标记录ID", "dimension", "ProjectIndicatorCube.id"),
        ("projectId", "项目ID", "dimension", "ProjectIndicatorCube.project_id"),
        ("reportPeriod", "报告期间", "dimension", "ProjectIndicatorCube.report_period"),
        ("indicatorCode", "指标编码", "dimension", "ProjectIndicatorCube.indicator_code"),
        ("indicatorName", "指标名称", "dimension", "ProjectIndicatorCube.indicator_name"),
        ("indicatorValue", "指标值", "measure", "ProjectIndicatorCube.indicator_value"),
        ("targetValue", "目标值", "measure", "ProjectIndicatorCube.target_value"),
        ("warningLevel", "预警级别", "dimension", "ProjectIndicatorCube.warning_level"),
    ]
    for code, name, role, qn in indicator_props:
        s.onto.define_property("ProjectIndicator", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK ProjectIndicator properties (8)")

    # ProjectRisk属性
    risk_props = [
        ("id", "风险记录ID", "dimension", "ProjectRiskCube.id"),
        ("projectId", "项目ID", "dimension", "ProjectRiskCube.project_id"),
        ("reportPeriod", "报告期间", "dimension", "ProjectRiskCube.report_period"),
        ("riskType", "风险类型", "dimension", "ProjectRiskCube.risk_type"),
        ("riskCode", "风险编码", "dimension", "ProjectRiskCube.risk_code"),
        ("riskName", "风险名称", "dimension", "ProjectRiskCube.risk_name"),
        ("riskValue", "风险值", "measure", "ProjectRiskCube.risk_value"),
        ("warningLevel", "预警级别", "dimension", "ProjectRiskCube.warning_level"),
    ]
    for code, name, role, qn in risk_props:
        s.onto.define_property("ProjectRisk", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK ProjectRisk properties (8)")

    # Contract属性
    contract_props = [
        ("id", "合同ID", "dimension", "ProjectPaymentCube.contract_id"),
        ("projectId", "项目ID", "dimension", "ProjectPaymentCube.project_id"),
        ("contractCode", "合同编码", "dimension", "ProjectPaymentCube.contract_code"),
        ("contractName", "合同名称", "dimension", "ProjectPaymentCube.contract_name"),
        ("contractAmount", "合同金额", "measure", "ProjectPaymentCube.contract_amount"),
        ("supplierName", "供应商名称", "dimension", "ProjectPaymentCube.supplier_name"),
        ("settlementStatus", "结算状态", "dimension", "ProjectPaymentCube.settlement_status"),
    ]
    for code, name, role, qn in contract_props:
        s.onto.define_property("Contract", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK Contract properties (7)")

    # Supplier属性
    supplier_props = [
        ("id", "供应商ID", "dimension", "ProjectPaymentCube.id"),
        ("supplierName", "供应商名称", "dimension", "ProjectPaymentCube.supplier_name"),
        ("supplierType", "供应商类型", "dimension", "ProjectPaymentCube.supplier_type"),
    ]
    for code, name, role, qn in supplier_props:
        s.onto.define_property("Supplier", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK Supplier properties (3)")

    # Company属性
    company_props = [
        ("id", "分公司ID", "dimension", "ProjectIndicatorCube.company_id"),
        ("companyName", "分公司名称", "dimension", "ProjectIndicatorCube.company_name"),
        ("companyCode", "分公司编码", "dimension", "ProjectIndicatorCube.project_code"),
    ]
    for code, name, role, qn in company_props:
        s.onto.define_property("Company", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK Company properties (3)")

    # 8. 定义链接类型
    output.print("\n[8/8] Defining link types...")

    link_types = [
        ("belongsTo", "属于", "ProjectOutput", "Project", "产值属于项目"),
        ("belongsTo", "属于", "ProjectCost", "Project", "成本属于项目"),
        ("belongsTo", "属于", "ProjectPayment", "Project", "付款属于项目"),
        ("belongsTo", "属于", "ProjectBalance", "Project", "收支属于项目"),
        ("belongsTo", "属于", "ProjectIndicator", "Project", "指标属于项目"),
        ("belongsTo", "属于", "ProjectRisk", "Project", "风险属于项目"),
        ("belongsTo", "属于", "Contract", "Project", "合同属于项目"),
        ("belongsTo", "属于", "Project", "Company", "项目属于分公司"),
        ("belongsTo", "属于", "Supplier", "Company", "供应商属于分公司"),
        ("contains", "包含", "ProjectCost", "Contract", "成本包含合同项"),
        ("contains", "包含", "ProjectPayment", "Contract", "付款包含合同项"),
    ]

    for code, name, from_obj, to_obj, desc in link_types:
        s.onto.define_link_type(
            code=code,
            name=name,
            from_object_type_code=from_obj,
            to_object_type_code=to_obj,
            description=desc
        )
        output.print(f"OK {from_obj} -{code}-> {to_obj}")

    # 9. 同步指标引用
    output.print("\n[9/8] Syncing metric references...")
    s.sync_metric_refs()
    output.print("OK sync_metric_refs")

    # 总结
    summary = {
        "ok": True,
        "space_id": space_id,
        "tables": 6,
        "cubes": 6,
        "object_types": 10,
        "properties": 75,
        "link_types": 11,
    }

    output.print("\n=== Panda Cost Analysis Ontology Initialization Completed ===")
    output.print(f"Tables: {summary['tables']}")
    output.print(f"Cubes: {summary['cubes']}")
    output.print(f"Object Types: {summary['object_types']}")
    output.print(f"Properties: {summary['properties']}")
    output.print(f"Link Types: {summary['link_types']}")
    output.success("Initialization completed successfully")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))