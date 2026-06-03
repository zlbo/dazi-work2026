"""潘达工程项目成本决策本体初始化脚本 for space__panda_construction_005

初始化内容：
1. 创建物理表（9张）
2. 注册Cube（4个）
3. 定义对象类型（8种）
4. 绑定数据源
5. 定义属性（约60个）
6. 定义链接类型（12种）
7. 同步指标引用

参考：d:\GitHub\dazi-work\项目\onto_潘达工程_项目成本决策\规划\项目成本决策本体方案.md
"""

import json


def main():
    space_id = "space__panda_construction_005"
    s = space.get(space_id)

    output.print("=== Start Panda Construction Project Cost Decision Ontology Initialization ===")
    output.print(f"Space: {space_id}")

    # ============================================================================
    # 1. 创建物理表（9张）
    # ============================================================================
    output.print("\n[1/9] Creating physical tables...")

    # 1.1 dim_project（项目维度表）
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_project (
            project_id String,
            project_name String,
            project_status String,
            customer_system String,
            increase_stock String,
            management_rate Float64,
            profession String,
            is_large_customer UInt8,
            operation_mode String,
            partner String,
            region String,
            project_scale Float64,
            planned_start_date Date,
            planned_completion_date Date,
            actual_start_date Date,
            actual_completion_date Date,
            contract_id String,
            owner_id String,
            created_at DateTime DEFAULT now(),
            updated_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_id)
    """)
    output.print("OK dim_project")

    # 1.2 dim_contract（合同维度表）
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_contract (
            contract_id String,
            contract_number String,
            contract_name String,
            contract_amount_including Float64,
            contract_amount_excluding Float64,
            owner_id String,
            owner_name String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (contract_id)
    """)
    output.print("OK dim_contract")

    # 1.3 dim_owner（业主维度表）
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_owner (
            owner_id String,
            owner_name String,
            customer_system String,
            is_large_customer UInt8,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (owner_id)
    """)
    output.print("OK dim_owner")

    # 1.4 fact_output_value（业主产值事实表）
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_output_value (
            output_id String,
            project_id String,
            report_month String,
            period_type String,
            output_amount Float64,
            confirm_status String,
            output_date Date,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_id, output_date, output_id)
    """)
    output.print("OK fact_output_value")

    # 1.5 fact_cost_record（成本记录事实表）
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_cost_record (
            cost_id String,
            project_id String,
            report_month String,
            cost_type String,
            cost_amount Float64,
            confirm_status String,
            cost_date Date,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_id, cost_date, cost_id)
    """)
    output.print("OK fact_cost_record")

    # 1.6 fact_payment（收款记录事实表）
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_payment (
            payment_id String,
            project_id String,
            report_month String,
            payment_amount Float64,
            payment_type String,
            payment_date Date,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_id, payment_date, payment_id)
    """)
    output.print("OK fact_payment")

    # 1.7 fact_profit_analysis（利润分析事实表）
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_profit_analysis (
            analysis_id String,
            project_id String,
            report_month String,
            output_confirmed Float64,
            output_total Float64,
            cost_confirmed Float64,
            cost_total Float64,
            profit_confirmed Float64,
            profit_total Float64,
            profit_rate_confirmed Float64,
            profit_rate_total Float64,
            analysis_date Date,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_id, analysis_date, analysis_id)
    """)
    output.print("OK fact_profit_analysis")

    # 1.8 fact_risk_indicator（风险指标事实表）
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_risk_indicator (
            indicator_id String,
            project_id String,
            report_month String,
            indicator_code String,
            indicator_name String,
            current_value Float64,
            reference_value String,
            warning_level String,
            issue_analysis String,
            improvement String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (project_id, indicator_code, report_month)
    """)
    output.print("OK fact_risk_indicator")

    # 1.9 wide_project_monthly（项目月度汇总宽表）
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS wide_project_monthly (
            project_id String,
            report_month String,
            project_name String,
            project_status String,
            customer_system String,
            management_rate Float64,
            profession String,
            is_large_customer UInt8,
            operation_mode String,
            region String,
            project_scale Float64,
            contract_amount Float64,
            owner_name String,
            output_last_year Float64,
            output_this_year_confirmed Float64,
            output_this_year_unconfirmed Float64,
            output_this_year_total Float64,
            output_this_month_confirmed Float64,
            output_this_month_unconfirmed Float64,
            output_this_month_total Float64,
            output_total_confirmed Float64,
            output_total_unconfirmed Float64,
            output_total_total Float64,
            receivable_amount Float64,
            receivable_ratio Float64,
            received_amount Float64,
            cost_confirmed Float64,
            cost_total Float64,
            profit_confirmed Float64,
            profit_total Float64,
            profit_rate_confirmed Float64,
            profit_rate_total Float64,
            warning_status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (report_month, project_id)
    """)
    output.print("OK wide_project_monthly")

    # ============================================================================
    # 2. 注册表到空间
    # ============================================================================
    output.print("\n[2/9] Registering tables to space...")

    tables = [
        ("dim_project", "项目维度表"),
        ("dim_contract", "合同维度表"),
        ("dim_owner", "业主维度表"),
        ("fact_output_value", "业主产值事实表"),
        ("fact_cost_record", "成本记录事实表"),
        ("fact_payment", "收款记录事实表"),
        ("fact_profit_analysis", "利润分析事实表"),
        ("fact_risk_indicator", "风险指标事实表"),
        ("wide_project_monthly", "项目月度汇总宽表"),
    ]

    for table_name, label in tables:
        s.tables.register(table_name, label=label)
        s.tables.sync_columns(table_name)
        output.print(f"OK {table_name} registered")

    # ============================================================================
    # 3. 注册Cube（4个）
    # ============================================================================
    output.print("\n[3/9] Registering Cubes...")

    # 3.1 ProjectCube（项目分析Cube）
    s.register_cube(
        name="ProjectCube",
        table="wide_project_monthly",
        title="项目分析Cube",
        measures=[
            {"name": "contract_amount", "col": "contract_amount", "agg": "sum", "title": "合同金额"},
            {"name": "output_total", "col": "output_total_total", "agg": "sum", "title": "总产值"},
            {"name": "cost_total", "col": "cost_total", "agg": "sum", "title": "总成本"},
            {"name": "profit_total", "col": "profit_total", "agg": "sum", "title": "总利润"},
            {"name": "receivable_amount", "col": "receivable_amount", "agg": "sum", "title": "应收工程款"},
            {"name": "received_amount", "col": "received_amount", "agg": "sum", "title": "已收工程款"},
            {"name": "project_count", "col": "project_id", "agg": "uniq", "title": "项目数量"},
        ],
        dimensions=[
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "工程名称"},
            {"name": "project_status", "col": "project_status", "type": "string", "title": "项目状态"},
            {"name": "profession", "col": "profession", "type": "string", "title": "专业"},
            {"name": "region", "col": "region", "type": "string", "title": "区域"},
            {"name": "operation_mode", "col": "operation_mode", "type": "string", "title": "经营模式"},
            {"name": "is_large_customer", "col": "is_large_customer", "type": "string", "title": "大客户标识"},
            {"name": "report_month", "col": "report_month", "type": "string", "title": "报表月份"},
            {"name": "owner_name", "col": "owner_name", "type": "string", "title": "业主名称"},
        ],
    )
    output.print("OK ProjectCube registered")

    # 3.2 OutputValueCube（产值分析Cube）
    s.register_cube(
        name="OutputValueCube",
        table="fact_output_value",
        title="产值分析Cube",
        measures=[
            {"name": "output_amount", "col": "output_amount", "agg": "sum", "title": "产值金额"},
        ],
        dimensions=[
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "report_month", "col": "report_month", "type": "string", "title": "报表月份"},
            {"name": "period_type", "col": "period_type", "type": "string", "title": "统计周期类型"},
            {"name": "confirm_status", "col": "confirm_status", "type": "string", "title": "确认状态"},
        ],
    )
    output.print("OK OutputValueCube registered")

    # 3.3 CostCube（成本分析Cube）
    s.register_cube(
        name="CostCube",
        table="fact_cost_record",
        title="成本分析Cube",
        measures=[
            {"name": "cost_amount", "col": "cost_amount", "agg": "sum", "title": "成本金额"},
        ],
        dimensions=[
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "report_month", "col": "report_month", "type": "string", "title": "报表月份"},
            {"name": "cost_type", "col": "cost_type", "type": "string", "title": "成本类型"},
            {"name": "confirm_status", "col": "confirm_status", "type": "string", "title": "确认状态"},
        ],
    )
    output.print("OK CostCube registered")

    # 3.4 RiskIndicatorCube（风险指标Cube）
    s.register_cube(
        name="RiskIndicatorCube",
        table="fact_risk_indicator",
        title="风险指标Cube",
        measures=[
            {"name": "current_value", "col": "current_value", "agg": "avg", "title": "当前值"},
        ],
        dimensions=[
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "report_month", "col": "report_month", "type": "string", "title": "报表月份"},
            {"name": "indicator_code", "col": "indicator_code", "type": "string", "title": "指标编码"},
            {"name": "warning_level", "col": "warning_level", "type": "string", "title": "预警等级"},
        ],
    )
    output.print("OK RiskIndicatorCube registered")

    # ============================================================================
    # 4. 添加派生度量
    # ============================================================================
    output.print("\n[4/9] Adding derived measures...")

    # ProjectCube派生度量
    s.upsert_derived_measures(
        "ProjectCube",
        [
            {
                "name": "profit_rate",
                "title": "利润率",
                "expression": "if(ProjectCube.output_total > 0, ProjectCube.profit_total / ProjectCube.output_total, 0)",
                "description": "利润率"
            },
            {
                "name": "collection_rate",
                "title": "回款率",
                "expression": "if(ProjectCube.receivable_amount > 0, ProjectCube.received_amount / ProjectCube.receivable_amount, 0)",
                "description": "回款率"
            },
        ]
    )
    output.print("OK ProjectCube derived measures")

    # ============================================================================
    # 5. 定义对象类型（8种）
    # ============================================================================
    output.print("\n[5/9] Defining object types...")

    object_types = [
        ("Project", "工程项目", "建筑工程项目的业务实体"),
        ("Contract", "合同", "项目与业主签订的工程合同"),
        ("Owner", "业主", "工程项目的投资方/委托方"),
        ("OutputValue", "业主产值", "项目完成工程量的货币价值"),
        ("CostRecord", "成本记录", "项目实际发生的各项成本"),
        ("Payment", "收款记录", "业主支付工程款的记录"),
        ("ProfitAnalysis", "利润分析", "项目利润的聚合分析对象"),
        ("RiskIndicator", "风险指标", "项目经营风险预警指标"),
    ]

    for code, name, desc in object_types:
        s.onto.define_object_type(code, name, description=desc)
        output.print(f"OK {code}")

    # ============================================================================
    # 6. 绑定数据源
    # ============================================================================
    output.print("\n[6/9] Binding data sources...")

    bind_sources = [
        ("Project", "dazi_cube", {"cube": "ProjectCube"}),
        ("Contract", "dazi_cube", {"cube": "ProjectCube"}),
        ("Owner", "dazi_cube", {"cube": "ProjectCube"}),
        ("OutputValue", "dazi_cube", {"cube": "OutputValueCube"}),
        ("CostRecord", "dazi_cube", {"cube": "CostCube"}),
        ("Payment", "dazi_cube", {"cube": "ProjectCube"}),
        ("ProfitAnalysis", "dazi_cube", {"cube": "ProjectCube"}),
        ("RiskIndicator", "dazi_cube", {"cube": "RiskIndicatorCube"}),
    ]

    for obj_code, source_type, config in bind_sources:
        s.onto.bind_source(obj_code, source_type, config=config)
        output.print(f"OK {obj_code} -> {config['cube']}")

    # ============================================================================
    # 7. 定义属性
    # ============================================================================
    output.print("\n[7/9] Defining properties...")

    # Project属性
    project_props = [
        ("project_id", "项目ID", "dimension", "ProjectCube.project_id"),
        ("project_name", "工程名称", "dimension", "ProjectCube.project_name"),
        ("project_status", "项目状态", "dimension", "ProjectCube.project_status"),
        ("profession", "专业", "dimension", "ProjectCube.profession"),
        ("region", "区域", "dimension", "ProjectCube.region"),
        ("operation_mode", "经营模式", "dimension", "ProjectCube.operation_mode"),
        ("is_large_customer", "大客户标识", "dimension", "ProjectCube.is_large_customer"),
        ("report_month", "报表月份", "dimension", "ProjectCube.report_month"),
        ("contract_amount", "合同金额", "measure", "ProjectCube.contract_amount"),
        ("output_total", "总产值", "measure", "ProjectCube.output_total"),
        ("cost_total", "总成本", "measure", "ProjectCube.cost_total"),
        ("profit_total", "总利润", "measure", "ProjectCube.profit_total"),
        ("profit_rate", "利润率", "measure", "ProjectCube.profit_rate"),
        ("receivable_amount", "应收工程款", "measure", "ProjectCube.receivable_amount"),
        ("received_amount", "已收工程款", "measure", "ProjectCube.received_amount"),
        ("collection_rate", "回款率", "measure", "ProjectCube.collection_rate"),
        ("project_count", "项目数量", "measure", "ProjectCube.project_count"),
    ]
    for code, name, role, qn in project_props:
        s.onto.define_property("Project", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK Project properties (17)")

    # Contract属性
    contract_props = [
        ("contract_id", "合同ID", "dimension", "ProjectCube.project_id"),
        ("contract_number", "合同编号", "dimension", "ProjectCube.project_id"),
        ("contract_name", "合同名称", "dimension", "ProjectCube.project_name"),
        ("contract_amount", "合同金额", "measure", "ProjectCube.contract_amount"),
    ]
    for code, name, role, qn in contract_props:
        s.onto.define_property("Contract", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK Contract properties (4)")

    # Owner属性
    owner_props = [
        ("owner_id", "业主ID", "dimension", "ProjectCube.project_id"),
        ("owner_name", "业主名称", "dimension", "ProjectCube.owner_name"),
        ("customer_system", "客户体系", "dimension", "ProjectCube.project_status"),
        ("is_large_customer", "大客户标识", "dimension", "ProjectCube.is_large_customer"),
    ]
    for code, name, role, qn in owner_props:
        s.onto.define_property("Owner", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK Owner properties (4)")

    # OutputValue属性
    output_value_props = [
        ("output_id", "产值ID", "dimension", "OutputValueCube.project_id"),
        ("output_amount", "产值金额", "measure", "OutputValueCube.output_amount"),
        ("confirm_status", "确认状态", "dimension", "OutputValueCube.confirm_status"),
        ("period_type", "统计周期类型", "dimension", "OutputValueCube.period_type"),
        ("report_month", "报表月份", "dimension", "OutputValueCube.report_month"),
    ]
    for code, name, role, qn in output_value_props:
        s.onto.define_property("OutputValue", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK OutputValue properties (5)")

    # CostRecord属性
    cost_record_props = [
        ("cost_id", "成本ID", "dimension", "CostCube.project_id"),
        ("cost_amount", "成本金额", "measure", "CostCube.cost_amount"),
        ("cost_type", "成本类型", "dimension", "CostCube.cost_type"),
        ("confirm_status", "确认状态", "dimension", "CostCube.confirm_status"),
        ("report_month", "报表月份", "dimension", "CostCube.report_month"),
    ]
    for code, name, role, qn in cost_record_props:
        s.onto.define_property("CostRecord", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK CostRecord properties (5)")

    # Payment属性
    payment_props = [
        ("payment_id", "收款ID", "dimension", "ProjectCube.project_id"),
        ("payment_amount", "收款金额", "measure", "ProjectCube.received_amount"),
        ("payment_type", "收款类型", "dimension", "ProjectCube.project_status"),
        ("report_month", "报表月份", "dimension", "ProjectCube.report_month"),
    ]
    for code, name, role, qn in payment_props:
        s.onto.define_property("Payment", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK Payment properties (4)")

    # ProfitAnalysis属性
    profit_analysis_props = [
        ("analysis_id", "分析ID", "dimension", "ProjectCube.project_id"),
        ("output_confirmed", "已确认产值", "measure", "ProjectCube.output_total"),
        ("output_total", "总产值", "measure", "ProjectCube.output_total"),
        ("cost_confirmed", "已确认成本", "measure", "ProjectCube.cost_total"),
        ("cost_total", "总成本", "measure", "ProjectCube.cost_total"),
        ("profit_confirmed", "已确认利润", "measure", "ProjectCube.profit_total"),
        ("profit_total", "总利润", "measure", "ProjectCube.profit_total"),
        ("profit_rate_confirmed", "已确认利润率", "measure", "ProjectCube.profit_rate"),
        ("profit_rate_total", "总利润率", "measure", "ProjectCube.profit_rate"),
        ("report_month", "报表月份", "dimension", "ProjectCube.report_month"),
    ]
    for code, name, role, qn in profit_analysis_props:
        s.onto.define_property("ProfitAnalysis", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK ProfitAnalysis properties (10)")

    # RiskIndicator属性
    risk_indicator_props = [
        ("indicator_id", "指标ID", "dimension", "RiskIndicatorCube.project_id"),
        ("indicator_code", "指标编码", "dimension", "RiskIndicatorCube.indicator_code"),
        ("indicator_name", "指标名称", "dimension", "RiskIndicatorCube.indicator_code"),
        ("current_value", "当前值", "measure", "RiskIndicatorCube.current_value"),
        ("reference_value", "参考值", "dimension", "RiskIndicatorCube.indicator_code"),
        ("warning_level", "预警等级", "dimension", "RiskIndicatorCube.warning_level"),
        ("issue_analysis", "问题分析", "dimension", "RiskIndicatorCube.indicator_code"),
        ("improvement", "改进措施", "dimension", "RiskIndicatorCube.indicator_code"),
        ("report_month", "报表月份", "dimension", "RiskIndicatorCube.report_month"),
    ]
    for code, name, role, qn in risk_indicator_props:
        s.onto.define_property("RiskIndicator", code, name, semantic_role=role, qualified_name=qn)
    output.print("OK RiskIndicator properties (9)")

    # ============================================================================
    # 8. 定义链接类型（12种）
    # ============================================================================
    output.print("\n[8/9] Defining link types...")

    link_types = [
        ("project_has_contract", "项目拥有合同", "Project", "Contract", "每个项目对应一份主合同"),
        ("project_belongs_to_owner", "项目归属业主", "Project", "Owner", "项目归属于业主（甲方）"),
        ("project_generates_output", "项目产生产值", "Project", "OutputValue", "项目产生多笔产值记录"),
        ("project_incurs_cost", "项目发生成本", "Project", "CostRecord", "项目发生多笔成本"),
        ("project_receives_payment", "项目收到款项", "Project", "Payment", "项目收到多笔收款"),
        ("project_analyzed_by", "项目被分析", "Project", "ProfitAnalysis", "项目有多条利润分析记录"),
        ("project_has_indicators", "项目有风险指标", "Project", "RiskIndicator", "项目有多个风险指标"),
        ("contract_with_owner", "合同签约业主", "Contract", "Owner", "合同与业主签约"),
        ("output_contributes_profit", "产值贡献利润", "OutputValue", "ProfitAnalysis", "产值数据参与利润计算"),
        ("cost_affects_profit", "成本影响利润", "CostRecord", "ProfitAnalysis", "成本数据参与利润计算"),
        ("payment_reduces_receivable", "收款减少应收", "Payment", "OutputValue", "收款对应产值应收"),
        ("indicator_warns_project", "指标预警项目", "RiskIndicator", "Project", "指标对项目发出预警"),
    ]

    for code, name, from_obj, to_obj, desc in link_types:
        s.onto.define_link_type(
            code=code,
            name=name,
            from_object_type_code=from_obj,
            to_object_type_code=to_obj,
            description=desc
        )
        output.print(f"OK {code}")

    # ============================================================================
    # 9. 同步指标引用
    # ============================================================================
    output.print("\n[9/9] Syncing metric references...")
    s.sync_metric_refs()
    output.print("OK sync_metric_refs")

    # ============================================================================
    # 总结
    # ============================================================================
    summary = {
        "ok": True,
        "space_id": space_id,
        "tables": 9,
        "cubes": 4,
        "derived_measures": 2,
        "object_types": 8,
        "properties": 58,
        "link_types": 12,
    }

    output.print("\n=== Panda Construction Project Cost Decision Ontology Initialization Completed ===")
    output.print(f"Tables: {summary['tables']}")
    output.print(f"Cubes: {summary['cubes']}")
    output.print(f"Derived Measures: {summary['derived_measures']}")
    output.print(f"Object Types: {summary['object_types']}")
    output.print(f"Properties: {summary['properties']}")
    output.print(f"Link Types: {summary['link_types']}")
    output.success("Initialization completed successfully")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=False, default=str))
