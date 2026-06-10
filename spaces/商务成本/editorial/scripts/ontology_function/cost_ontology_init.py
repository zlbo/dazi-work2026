"""商务成本本体初始化脚本 — space__panda_construction

初始化内容：
1. 创建物理表（7个事实表 + 3个维表）
2. 注册表到空间
3. 注册表间关系
4. 注册 Cube（10个）
5. 定义对象类型（10种）、绑定数据源、属性、链接

依据规范：《本体规划指南》《本体命名规范》
"""

def main():
    return _ontology_fn_body(p)


def _ontology_fn_body(p):
    space_id = p.arguments.get("space_id", "space__panda_construction")
    s = space.get(space_id)

    output.print("=== 商务成本本体初始化 ===")
    output.print(f"空间: {space_id}")

    # 1. 创建物理表
    output.print("\n[1/7] 创建物理表...")

    # dim_date - 公共日期维度表
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_date (
            dateId String,
            date Date,
            year Int32,
            quarter Int32,
            month Int32,
            day Int32,
            weekOfYear Int32,
            monthName String,
            quarterName String,
            yearMonth String,
            isWeekend Int8,
            holidayFlag Int8,
            holidayName String
        ) ENGINE = MergeTree()
        ORDER BY (date)
    """)
    output.print("OK dim_date")

    # dim_region - 地区维度表（支持大区/省/市/区县/海外）
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_region (
            regionId String,
            regionCode String,
            regionName String,
            regionLevel Int32,
            parentRegionId String,
            isDomestic Int8,
            majorRegion String,
            province String,
            city String,
            district String,
            country String,
            overseasRegion String
        ) ENGINE = MergeTree()
        ORDER BY (regionId)
    """)
    output.print("OK dim_region")

    # dim_department - 部门维度表
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_department (
            departmentId String,
            departmentCode String,
            departmentName String,
            departmentLevel Int32,
            parentDepartmentId String,
            departmentType String,
            companyId String
        ) ENGINE = MergeTree()
        ORDER BY (departmentId)
    """)
    output.print("OK dim_department")

    # dim_owner - 业主维度表
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_owner (
            ownerId String,
            ownerCode String,
            ownerName String,
            ownerType String,
            ownerLevel String,
            creditRating String,
            contactPerson String,
            contactPhone String,
            address String
        ) ENGINE = MergeTree()
        ORDER BY (ownerId)
    """)
    output.print("OK dim_owner")

    # dim_cost_subject - 成本科目维度表
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_cost_subject (
            subjectId String,
            subjectCode String,
            subjectName String,
            subjectLevel Int32,
            parentSubjectId String,
            subjectCategory String,
            subjectType String
        ) ENGINE = MergeTree()
        ORDER BY (subjectId)
    """)
    output.print("OK dim_cost_subject")

    # dim_project
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_project (
            id String,
            projectCode String,
            projectName String,
            projectType String,
            projectStatus String,
            province String,
            city String,
            address String,
            companyId String,
            contractAmount Float64,
            startDate Date,
            endDate Date,
            createdAt DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (id)
    """)
    output.print("OK dim_project")

    # dim_company
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_company (
            id String,
            companyCode String,
            companyName String,
            province String,
            city String
        ) ENGINE = MergeTree()
        ORDER BY (id)
    """)
    output.print("OK dim_company")

    # dim_supplier
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_supplier (
            id String,
            supplierName String,
            supplierType String,
            contactPerson String,
            contactPhone String,
            companyId String
        ) ENGINE = MergeTree()
        ORDER BY (id)
    """)
    output.print("OK dim_supplier")

    # dim_contract
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_contract (
            id String,
            contractCode String,
            contractName String,
            contractContent String,
            supplierName String,
            contractAmount Float64,
            paymentRatio Float64,
            taxRate Float64,
            settlementStatus String,
            projectId String
        ) ENGINE = MergeTree()
        ORDER BY (id)
    """)
    output.print("OK dim_contract")

    # fact_project_output - 实现ER001产值确认双轨制
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_project_output (
            id String,
            projectId String,
            reportPeriod String,
            outputValue Float64,
            outputTax Float64,
            outputWithoutTax Float64,
            outputType String,
            outputRatio Float64,
            confirmType String,
            confirmedOutput Float64,
            pendingOutput Float64
        ) ENGINE = MergeTree()
        ORDER BY (projectId, reportPeriod)
    """)
    output.print("OK fact_project_output")

    # fact_project_cost - 实现ER002成本三级分类
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_project_cost (
            id String,
            projectId String,
            contractId String,
            reportPeriod String,
            costAmount Float64,
            costType String,
            costLevel1 String,
            costLevel2 String,
            costLevel3 String,
            laborCost Float64,
            materialCost Float64,
            mechanicalCost Float64,
            otherCost Float64,
            targetCost Float64,
            varianceAmount Float64,
            varianceRatio Float64
        ) ENGINE = MergeTree()
        ORDER BY (projectId, reportPeriod)
    """)
    output.print("OK fact_project_cost")

    # fact_project_indicator - 实现ER005成本偏差率计算、ER006收款率计算
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_project_indicator (
            id String,
            projectId String,
            companyId String,
            reportPeriod String,
            indicatorType String,
            indicatorValue Float64,
            targetValue Float64,
            achievementRate Float64,
            rankLevel String,
            warningLevel String,
            varianceValue Float64,
            varianceRatio Float64,
            contractConversionRate Float64,
            claimRealizationRate Float64,
            receivableRecoveryRate Float64,
            materialPriceMarginRate Float64,
            projectGrossMargin Float64,
            costVarianceRate Float64,
            collectionRate Float64,
            paymentRate Float64,
            confirmationRate Float64
        ) ENGINE = MergeTree()
        ORDER BY (projectId, reportPeriod)
    """)
    output.print("OK fact_project_indicator")

    # fact_project_payment - 实现ER004资金月度批复
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_project_payment (
            id String,
            projectId String,
            contractId String,
            reportPeriod String,
            payableConfirmed Float64,
            laborPayable Float64,
            paidAmount Float64,
            payableUnconfirmed Float64,
            paymentRatio Float64,
            approvalStatus String,
            approvalAmount Float64,
            approvedDate Date,
            approvalComment String
        ) ENGINE = MergeTree()
        ORDER BY (projectId, reportPeriod)
    """)
    output.print("OK fact_project_payment")

    # fact_project_balance
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_project_balance (
            id String,
            projectId String,
            reportPeriod String,
            subjectCode String,
            subjectName String,
            projectAmount Float64,
            companyAmount Float64,
            totalAmount Float64,
            totalIncomeAcc Float64,
            totalExpenseAcc Float64,
            ownerIncomeAcc Float64,
            currentIncomeAcc Float64,
            costExpenseAcc Float64,
            currentExpenseAcc Float64,
            advanceCapital Float64
        ) ENGINE = MergeTree()
        ORDER BY (projectId, reportPeriod)
    """)
    output.print("OK fact_project_balance")

    # fact_project_risk - 实现ER003风险三色预警
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_project_risk (
            id String,
            projectId String,
            reportPeriod String,
            riskType String,
            riskCode String,
            riskName String,
            riskValue Float64,
            warningLevel String,
            riskScore Int32,
            indicatorAbnormalCount Int32,
            consecutiveLossMonths Int32,
            overallWarningLevel String,
            warningReason String
        ) ENGINE = MergeTree()
        ORDER BY (projectId, reportPeriod)
    """)
    output.print("OK fact_project_risk")

    # 2. 注册表（含 display_name / description）
    output.print("\n[2/7] 注册表到空间...")

    TABLE_REGISTRY = {
        "dim_date": {"display_name": "日期维表", "description": "公共日期维度表，包含年/季/月/日等时间维度"},
        "dim_region": {"display_name": "地区维表", "description": "地区维度表，支持大区/省/市/区县/海外层级"},
        "dim_department": {"display_name": "部门维表", "description": "组织部门维度表"},
        "dim_owner": {"display_name": "业主维表", "description": "业主/客户维度表"},
        "dim_cost_subject": {"display_name": "成本科目维表", "description": "成本科目层级维度表"},
        "dim_project": {"display_name": "项目维表", "description": "项目主数据"},
        "dim_company": {"display_name": "分公司维表", "description": "分公司主数据"},
        "dim_supplier": {"display_name": "供应商维表", "description": "供应商主数据"},
        "dim_contract": {"display_name": "合同维表", "description": "合同主数据"},
        "fact_project_output": {"display_name": "项目产值事实表", "description": "项目产值数据"},
        "fact_project_cost": {"display_name": "项目成本事实表", "description": "项目成本数据"},
        "fact_project_indicator": {"display_name": "项目指标事实表", "description": "项目关键指标数据"},
        "fact_project_payment": {"display_name": "项目付款事实表", "description": "项目付款数据"},
        "fact_project_balance": {"display_name": "项目收支事实表", "description": "项目收支数据"},
        "fact_project_risk": {"display_name": "项目风险事实表", "description": "项目风险预警数据"},
    }

    for tbl_name, meta in TABLE_REGISTRY.items():
        s.tables.register_with_meta(
            table_name=tbl_name,
            display_name=meta["display_name"],
            description=meta.get("description"),
        )
        output.print(f"OK {tbl_name}")

    # 3. 注册表间关系
    output.print("\n[3/7] 注册表间关系...")

    table_relationships = [
        {"from_table": "dim_project", "to_table": "dim_company", "join_sql": "dim_project.companyId = dim_company.id", "join_keys": [{"from": "companyId", "to": "id"}], "relationship_type": "many_to_one"},
        {"from_table": "dim_supplier", "to_table": "dim_company", "join_sql": "dim_supplier.companyId = dim_company.id", "join_keys": [{"from": "companyId", "to": "id"}], "relationship_type": "many_to_one"},
        {"from_table": "dim_contract", "to_table": "dim_project", "join_sql": "dim_contract.projectId = dim_project.id", "join_keys": [{"from": "projectId", "to": "id"}], "relationship_type": "many_to_one"},
        {"from_table": "fact_project_output", "to_table": "dim_project", "join_sql": "fact_project_output.projectId = dim_project.id", "join_keys": [{"from": "projectId", "to": "id"}], "relationship_type": "many_to_one"},
        {"from_table": "fact_project_cost", "to_table": "dim_project", "join_sql": "fact_project_cost.projectId = dim_project.id", "join_keys": [{"from": "projectId", "to": "id"}], "relationship_type": "many_to_one"},
        {"from_table": "fact_project_cost", "to_table": "dim_contract", "join_sql": "fact_project_cost.contractId = dim_contract.id", "join_keys": [{"from": "contractId", "to": "id"}], "relationship_type": "many_to_one"},
        {"from_table": "fact_project_indicator", "to_table": "dim_project", "join_sql": "fact_project_indicator.projectId = dim_project.id", "join_keys": [{"from": "projectId", "to": "id"}], "relationship_type": "many_to_one"},
        {"from_table": "fact_project_indicator", "to_table": "dim_company", "join_sql": "fact_project_indicator.companyId = dim_company.id", "join_keys": [{"from": "companyId", "to": "id"}], "relationship_type": "many_to_one"},
        {"from_table": "fact_project_payment", "to_table": "dim_project", "join_sql": "fact_project_payment.projectId = dim_project.id", "join_keys": [{"from": "projectId", "to": "id"}], "relationship_type": "many_to_one"},
        {"from_table": "fact_project_payment", "to_table": "dim_contract", "join_sql": "fact_project_payment.contractId = dim_contract.id", "join_keys": [{"from": "contractId", "to": "id"}], "relationship_type": "many_to_one"},
        {"from_table": "fact_project_balance", "to_table": "dim_project", "join_sql": "fact_project_balance.projectId = dim_project.id", "join_keys": [{"from": "projectId", "to": "id"}], "relationship_type": "many_to_one"},
        {"from_table": "fact_project_risk", "to_table": "dim_project", "join_sql": "fact_project_risk.projectId = dim_project.id", "join_keys": [{"from": "projectId", "to": "id"}], "relationship_type": "many_to_one"},
    ]
    for rel in table_relationships:
        s.tables.add_relationship(**rel)
        output.print(f"OK {rel['from_table']} -> {rel['to_table']}")

    # 4. 注册 Cube
    output.print("\n[4/7] 注册 Cube...")

    # DateCube - 公共日期维度Cube
    s.register_cube(
        name="DateCube",
        table="dim_date",
        title="日期维度Cube",
        measures=[],
        dimensions=[
            {"name": "dateId", "col": "dateId", "type": "string", "title": "日期ID"},
            {"name": "date", "col": "date", "type": "date", "title": "日期"},
            {"name": "year", "col": "year", "type": "int", "title": "年份"},
            {"name": "quarter", "col": "quarter", "type": "int", "title": "季度"},
            {"name": "month", "col": "month", "type": "int", "title": "月份"},
            {"name": "day", "col": "day", "type": "int", "title": "日期(日)"},
            {"name": "weekOfYear", "col": "weekOfYear", "type": "int", "title": "周序号"},
            {"name": "monthName", "col": "monthName", "type": "string", "title": "月份名称"},
            {"name": "quarterName", "col": "quarterName", "type": "string", "title": "季度名称"},
            {"name": "yearMonth", "col": "yearMonth", "type": "string", "title": "年月"},
            {"name": "isWeekend", "col": "isWeekend", "type": "int", "title": "是否周末"},
            {"name": "holidayFlag", "col": "holidayFlag", "type": "int", "title": "节假日标志"},
            {"name": "holidayName", "col": "holidayName", "type": "string", "title": "节假日名称"},
        ],
    )
    output.print("OK DateCube")

    # RegionCube - 地区维度Cube
    s.register_cube(
        name="RegionCube",
        table="dim_region",
        title="地区维度Cube",
        measures=[],
        dimensions=[
            {"name": "regionId", "col": "regionId", "type": "string", "title": "地区ID"},
            {"name": "regionCode", "col": "regionCode", "type": "string", "title": "地区编码"},
            {"name": "regionName", "col": "regionName", "type": "string", "title": "地区名称"},
            {"name": "regionLevel", "col": "regionLevel", "type": "int", "title": "地区层级"},
            {"name": "parentRegionId", "col": "parentRegionId", "type": "string", "title": "上级地区ID"},
            {"name": "isDomestic", "col": "isDomestic", "type": "int", "title": "是否国内"},
            {"name": "majorRegion", "col": "majorRegion", "type": "string", "title": "大区"},
            {"name": "province", "col": "province", "type": "string", "title": "省份"},
            {"name": "city", "col": "city", "type": "string", "title": "城市"},
            {"name": "district", "col": "district", "type": "string", "title": "区县"},
            {"name": "country", "col": "country", "type": "string", "title": "国家"},
            {"name": "overseasRegion", "col": "overseasRegion", "type": "string", "title": "海外区域"},
        ],
    )
    output.print("OK RegionCube")

    # DepartmentCube - 部门维度Cube
    s.register_cube(
        name="DepartmentCube",
        table="dim_department",
        title="部门维度Cube",
        measures=[],
        dimensions=[
            {"name": "departmentId", "col": "departmentId", "type": "string", "title": "部门ID"},
            {"name": "departmentCode", "col": "departmentCode", "type": "string", "title": "部门编码"},
            {"name": "departmentName", "col": "departmentName", "type": "string", "title": "部门名称"},
            {"name": "departmentLevel", "col": "departmentLevel", "type": "int", "title": "部门层级"},
            {"name": "parentDepartmentId", "col": "parentDepartmentId", "type": "string", "title": "上级部门ID"},
            {"name": "departmentType", "col": "departmentType", "type": "string", "title": "部门类型"},
            {"name": "companyId", "col": "companyId", "type": "string", "title": "所属公司ID"},
        ],
    )
    output.print("OK DepartmentCube")

    # OwnerCube - 业主维度Cube
    s.register_cube(
        name="OwnerCube",
        table="dim_owner",
        title="业主维度Cube",
        measures=[],
        dimensions=[
            {"name": "ownerId", "col": "ownerId", "type": "string", "title": "业主ID"},
            {"name": "ownerCode", "col": "ownerCode", "type": "string", "title": "业主编码"},
            {"name": "ownerName", "col": "ownerName", "type": "string", "title": "业主名称"},
            {"name": "ownerType", "col": "ownerType", "type": "string", "title": "业主类型"},
            {"name": "ownerLevel", "col": "ownerLevel", "type": "string", "title": "业主等级"},
            {"name": "creditRating", "col": "creditRating", "type": "string", "title": "信用等级"},
            {"name": "contactPerson", "col": "contactPerson", "type": "string", "title": "联系人"},
            {"name": "contactPhone", "col": "contactPhone", "type": "string", "title": "联系电话"},
            {"name": "address", "col": "address", "type": "string", "title": "地址"},
        ],
    )
    output.print("OK OwnerCube")

    # CostSubjectCube - 成本科目维度Cube
    s.register_cube(
        name="CostSubjectCube",
        table="dim_cost_subject",
        title="成本科目维度Cube",
        measures=[],
        dimensions=[
            {"name": "subjectId", "col": "subjectId", "type": "string", "title": "科目ID"},
            {"name": "subjectCode", "col": "subjectCode", "type": "string", "title": "科目编码"},
            {"name": "subjectName", "col": "subjectName", "type": "string", "title": "科目名称"},
            {"name": "subjectLevel", "col": "subjectLevel", "type": "int", "title": "科目层级"},
            {"name": "parentSubjectId", "col": "parentSubjectId", "type": "string", "title": "上级科目ID"},
            {"name": "subjectCategory", "col": "subjectCategory", "type": "string", "title": "科目类别"},
            {"name": "subjectType", "col": "subjectType", "type": "string", "title": "科目类型"},
        ],
    )
    output.print("OK CostSubjectCube")

    # ProjectCube
    s.register_cube(
        name="ProjectCube",
        table="dim_project",
        title="项目实体Cube",
        measures=[{"name": "contractAmount", "col": "contractAmount", "agg": "sum", "title": "合同金额"}],
        dimensions=[
            {"name": "id", "col": "id", "type": "string", "title": "项目ID"},
            {"name": "projectCode", "col": "projectCode", "type": "string", "title": "项目编码"},
            {"name": "projectName", "col": "projectName", "type": "string", "title": "项目名称"},
            {"name": "projectType", "col": "projectType", "type": "string", "title": "项目类型"},
            {"name": "projectStatus", "col": "projectStatus", "type": "string", "title": "项目状态"},
            {"name": "province", "col": "province", "type": "string", "title": "所属省份"},
            {"name": "city", "col": "city", "type": "string", "title": "所属城市"},
            {"name": "companyId", "col": "companyId", "type": "string", "title": "分公司ID"},
        ],
    )
    output.print("OK ProjectCube")

    # ProjectOutputCube - 实现ER001产值确认双轨制
    s.register_cube(
        name="ProjectOutputCube",
        table="fact_project_output",
        title="项目产值Cube",
        measures=[
            {"name": "outputValue", "col": "outputValue", "agg": "sum", "title": "产值金额"},
            {"name": "outputTax", "col": "outputTax", "agg": "sum", "title": "产值税额"},
            {"name": "outputWithoutTax", "col": "outputWithoutTax", "agg": "sum", "title": "产值不含税"},
            {"name": "outputRatio", "col": "outputRatio", "agg": "avg", "title": "产值占比"},
            {"name": "confirmedOutput", "col": "confirmedOutput", "agg": "sum", "title": "已确认产值"},
            {"name": "pendingOutput", "col": "pendingOutput", "agg": "sum", "title": "待确认产值"},
        ],
        dimensions=[
            {"name": "id", "col": "id", "type": "string", "title": "产值记录ID"},
            {"name": "projectId", "col": "projectId", "type": "string", "title": "项目ID"},
            {"name": "reportPeriod", "col": "reportPeriod", "type": "string", "title": "报告期间"},
            {"name": "outputType", "col": "outputType", "type": "string", "title": "产值类型"},
            {"name": "confirmType", "col": "confirmType", "type": "string", "title": "确认类型"},
        ],
    )
    output.print("OK ProjectOutputCube")

    # ProjectCostCube - 实现ER002成本三级分类、ER005成本偏差率
    s.register_cube(
        name="ProjectCostCube",
        table="fact_project_cost",
        title="项目成本Cube",
        measures=[
            {"name": "costAmount", "col": "costAmount", "agg": "sum", "title": "成本金额"},
            {"name": "laborCost", "col": "laborCost", "agg": "sum", "title": "人工费"},
            {"name": "materialCost", "col": "materialCost", "agg": "sum", "title": "材料费"},
            {"name": "mechanicalCost", "col": "mechanicalCost", "agg": "sum", "title": "机械费"},
            {"name": "otherCost", "col": "otherCost", "agg": "sum", "title": "其他费用"},
            {"name": "targetCost", "col": "targetCost", "agg": "sum", "title": "目标成本"},
            {"name": "varianceAmount", "col": "varianceAmount", "agg": "sum", "title": "偏差金额"},
            {"name": "varianceRatio", "col": "varianceRatio", "agg": "avg", "title": "偏差率"},
        ],
        dimensions=[
            {"name": "id", "col": "id", "type": "string", "title": "成本记录ID"},
            {"name": "projectId", "col": "projectId", "type": "string", "title": "项目ID"},
            {"name": "contractId", "col": "contractId", "type": "string", "title": "合同ID"},
            {"name": "reportPeriod", "col": "reportPeriod", "type": "string", "title": "报告期间"},
            {"name": "costType", "col": "costType", "type": "string", "title": "成本类型"},
            {"name": "costLevel1", "col": "costLevel1", "type": "string", "title": "成本一级分类"},
            {"name": "costLevel2", "col": "costLevel2", "type": "string", "title": "成本二级分类"},
            {"name": "costLevel3", "col": "costLevel3", "type": "string", "title": "成本三级分类"},
        ],
    )
    output.print("OK ProjectCostCube")

    # ProjectIndicatorCube - 实现ER005成本偏差率、ER006收款率
    s.register_cube(
        name="ProjectIndicatorCube",
        table="fact_project_indicator",
        title="项目指标Cube",
        measures=[
            {"name": "indicatorValue", "col": "indicatorValue", "agg": "sum", "title": "指标值"},
            {"name": "targetValue", "col": "targetValue", "agg": "sum", "title": "目标值"},
            {"name": "achievementRate", "col": "achievementRate", "agg": "avg", "title": "完成率"},
            {"name": "varianceValue", "col": "varianceValue", "agg": "sum", "title": "偏差值"},
            {"name": "varianceRatio", "col": "varianceRatio", "agg": "avg", "title": "偏差率"},
            {"name": "contractConversionRate", "col": "contractConversionRate", "agg": "avg", "title": "合同转化率"},
            {"name": "claimRealizationRate", "col": "claimRealizationRate", "agg": "avg", "title": "变更签证索赔实现率"},
            {"name": "receivableRecoveryRate", "col": "receivableRecoveryRate", "agg": "avg", "title": "应收款回收率"},
            {"name": "materialPriceMarginRate", "col": "materialPriceMarginRate", "agg": "avg", "title": "材料认价利润率"},
            {"name": "projectGrossMargin", "col": "projectGrossMargin", "agg": "avg", "title": "项目毛利率"},
            {"name": "costVarianceRate", "col": "costVarianceRate", "agg": "avg", "title": "成本偏差率"},
            {"name": "collectionRate", "col": "collectionRate", "agg": "avg", "title": "收现率"},
            {"name": "paymentRate", "col": "paymentRate", "agg": "avg", "title": "付现率"},
            {"name": "confirmationRate", "col": "confirmationRate", "agg": "avg", "title": "确权率"},
        ],
        dimensions=[
            {"name": "id", "col": "id", "type": "string", "title": "指标记录ID"},
            {"name": "projectId", "col": "projectId", "type": "string", "title": "项目ID"},
            {"name": "companyId", "col": "companyId", "type": "string", "title": "分公司ID"},
            {"name": "reportPeriod", "col": "reportPeriod", "type": "string", "title": "报告期间"},
            {"name": "indicatorType", "col": "indicatorType", "type": "string", "title": "指标类型"},
            {"name": "rankLevel", "col": "rankLevel", "type": "string", "title": "排名等级"},
            {"name": "warningLevel", "col": "warningLevel", "type": "string", "title": "预警级别"},
        ],
    )
    output.print("OK ProjectIndicatorCube")

    # ProjectPaymentCube - 实现ER004资金月度批复
    s.register_cube(
        name="ProjectPaymentCube",
        table="fact_project_payment",
        title="项目付款Cube",
        measures=[
            {"name": "payableConfirmed", "col": "payableConfirmed", "agg": "sum", "title": "已确认应付款"},
            {"name": "laborPayable", "col": "laborPayable", "agg": "sum", "title": "人工费应付款"},
            {"name": "paidAmount", "col": "paidAmount", "agg": "sum", "title": "已付款金额"},
            {"name": "payableUnconfirmed", "col": "payableUnconfirmed", "agg": "sum", "title": "待确认应付款"},
            {"name": "paymentRatio", "col": "paymentRatio", "agg": "avg", "title": "付款比例"},
            {"name": "approvalAmount", "col": "approvalAmount", "agg": "sum", "title": "批复金额"},
        ],
        dimensions=[
            {"name": "id", "col": "id", "type": "string", "title": "付款记录ID"},
            {"name": "projectId", "col": "projectId", "type": "string", "title": "项目ID"},
            {"name": "contractId", "col": "contractId", "type": "string", "title": "合同ID"},
            {"name": "reportPeriod", "col": "reportPeriod", "type": "string", "title": "报告期间"},
            {"name": "approvalStatus", "col": "approvalStatus", "type": "string", "title": "审批状态"},
            {"name": "approvalComment", "col": "approvalComment", "type": "string", "title": "审批意见"},
        ],
    )
    output.print("OK ProjectPaymentCube")

    # ProjectBalanceCube
    s.register_cube(
        name="ProjectBalanceCube",
        table="fact_project_balance",
        title="项目收支Cube",
        measures=[
            {"name": "projectAmount", "col": "projectAmount", "agg": "sum", "title": "项目层面金额"},
            {"name": "companyAmount", "col": "companyAmount", "agg": "sum", "title": "公司层面金额"},
            {"name": "totalAmount", "col": "totalAmount", "agg": "sum", "title": "合计金额"},
            {"name": "totalIncomeAcc", "col": "totalIncomeAcc", "agg": "sum", "title": "累计总收入"},
            {"name": "totalExpenseAcc", "col": "totalExpenseAcc", "agg": "sum", "title": "累计总支出"},
            {"name": "ownerIncomeAcc", "col": "ownerIncomeAcc", "agg": "sum", "title": "业主收入累计"},
            {"name": "currentIncomeAcc", "col": "currentIncomeAcc", "agg": "sum", "title": "往来收入累计"},
            {"name": "costExpenseAcc", "col": "costExpenseAcc", "agg": "sum", "title": "成本支出累计"},
            {"name": "currentExpenseAcc", "col": "currentExpenseAcc", "agg": "sum", "title": "往来支出累计"},
            {"name": "advanceCapital", "col": "advanceCapital", "agg": "sum", "title": "公司垫资本金"},
        ],
        dimensions=[
            {"name": "id", "col": "id", "type": "string", "title": "收支记录ID"},
            {"name": "projectId", "col": "projectId", "type": "string", "title": "项目ID"},
            {"name": "reportPeriod", "col": "reportPeriod", "type": "string", "title": "报告期间"},
            {"name": "subjectCode", "col": "subjectCode", "type": "string", "title": "科目编码"},
            {"name": "subjectName", "col": "subjectName", "type": "string", "title": "科目名称"},
        ],
    )
    output.print("OK ProjectBalanceCube")

    # ProjectRiskCube - 实现ER003风险三色预警
    s.register_cube(
        name="ProjectRiskCube",
        table="fact_project_risk",
        title="项目风险Cube",
        measures=[
            {"name": "riskValue", "col": "riskValue", "agg": "sum", "title": "风险值"},
            {"name": "riskScore", "col": "riskScore", "agg": "avg", "title": "风险评分"},
            {"name": "indicatorAbnormalCount", "col": "indicatorAbnormalCount", "agg": "sum", "title": "指标异常数量"},
            {"name": "consecutiveLossMonths", "col": "consecutiveLossMonths", "agg": "max", "title": "连续亏损月数"},
        ],
        dimensions=[
            {"name": "id", "col": "id", "type": "string", "title": "风险记录ID"},
            {"name": "projectId", "col": "projectId", "type": "string", "title": "项目ID"},
            {"name": "reportPeriod", "col": "reportPeriod", "type": "string", "title": "报告期间"},
            {"name": "riskType", "col": "riskType", "type": "string", "title": "风险类型"},
            {"name": "riskCode", "col": "riskCode", "type": "string", "title": "风险编码"},
            {"name": "riskName", "col": "riskName", "type": "string", "title": "风险名称"},
            {"name": "warningLevel", "col": "warningLevel", "type": "string", "title": "预警级别"},
            {"name": "overallWarningLevel", "col": "overallWarningLevel", "type": "string", "title": "综合预警级别"},
            {"name": "warningReason", "col": "warningReason", "type": "string", "title": "预警原因"},
        ],
    )
    output.print("OK ProjectRiskCube")

    # ContractCube
    s.register_cube(
        name="ContractCube",
        table="dim_contract",
        title="合同Cube",
        measures=[
            {"name": "contractAmount", "col": "contractAmount", "agg": "sum", "title": "合同金额"},
            {"name": "paymentRatio", "col": "paymentRatio", "agg": "avg", "title": "付款比例"},
            {"name": "taxRate", "col": "taxRate", "agg": "avg", "title": "税率"},
        ],
        dimensions=[
            {"name": "id", "col": "id", "type": "string", "title": "合同ID"},
            {"name": "contractCode", "col": "contractCode", "type": "string", "title": "合同编码"},
            {"name": "contractName", "col": "contractName", "type": "string", "title": "合同名称"},
            {"name": "supplierName", "col": "supplierName", "type": "string", "title": "供应商名称"},
            {"name": "settlementStatus", "col": "settlementStatus", "type": "string", "title": "结算状态"},
            {"name": "projectId", "col": "projectId", "type": "string", "title": "项目ID"},
        ],
    )
    output.print("OK ContractCube")

    # SupplierCube
    s.register_cube(
        name="SupplierCube",
        table="dim_supplier",
        title="供应商Cube",
        measures=[],
        dimensions=[
            {"name": "id", "col": "id", "type": "string", "title": "供应商ID"},
            {"name": "supplierName", "col": "supplierName", "type": "string", "title": "供应商名称"},
            {"name": "supplierType", "col": "supplierType", "type": "string", "title": "供应商类型"},
            {"name": "contactPerson", "col": "contactPerson", "type": "string", "title": "联系人"},
            {"name": "contactPhone", "col": "contactPhone", "type": "string", "title": "联系电话"},
            {"name": "companyId", "col": "companyId", "type": "string", "title": "所属分公司ID"},
        ],
    )
    output.print("OK SupplierCube")

    # CompanyCube
    s.register_cube(
        name="CompanyCube",
        table="dim_company",
        title="分公司Cube",
        measures=[],
        dimensions=[
            {"name": "id", "col": "id", "type": "string", "title": "分公司ID"},
            {"name": "companyCode", "col": "companyCode", "type": "string", "title": "分公司编码"},
            {"name": "companyName", "col": "companyName", "type": "string", "title": "分公司名称"},
            {"name": "province", "col": "province", "type": "string", "title": "所在省份"},
            {"name": "city", "col": "city", "type": "string", "title": "所在城市"},
        ],
    )
    output.print("OK CompanyCube")

    # 5. 定义对象类型
    output.print("\n[5/7] 定义对象类型...")

    object_types = [
        ("Date", "日期", "公共日期维度"),
        ("Region", "地区", "地区维度，支持大区/省/市/区县/海外"),
        ("Department", "部门", "组织部门维度"),
        ("Owner", "业主", "业主/客户维度"),
        ("CostSubject", "成本科目", "成本科目层级维度"),
        ("Project", "项目实体", "项目主数据"),
        ("ProjectOutput", "项目产值", "项目产值数据"),
        ("ProjectCost", "项目成本", "项目成本数据"),
        ("ProjectIndicator", "项目指标", "项目关键指标"),
        ("ProjectPayment", "项目付款", "项目付款数据"),
        ("ProjectBalance", "项目收支", "项目收支数据"),
        ("ProjectRisk", "风险预警", "项目风险预警"),
        ("Contract", "合同", "合同数据"),
        ("Supplier", "供应商", "供应商数据"),
        ("Company", "分公司", "分公司数据"),
    ]
    for code, name, desc in object_types:
        s.onto.define_object_type(code, name, description=desc)
        output.print(f"OK {code}")

    # 6. 绑定数据源和属性
    output.print("\n[6/7] 绑定数据源和属性...")

    # 绑定数据源
    bindings = [
        ("Date", "DateCube"),
        ("Region", "RegionCube"),
        ("Department", "DepartmentCube"),
        ("Owner", "OwnerCube"),
        ("CostSubject", "CostSubjectCube"),
        ("Project", "ProjectCube"),
        ("ProjectOutput", "ProjectOutputCube"),
        ("ProjectCost", "ProjectCostCube"),
        ("ProjectIndicator", "ProjectIndicatorCube"),
        ("ProjectPayment", "ProjectPaymentCube"),
        ("ProjectBalance", "ProjectBalanceCube"),
        ("ProjectRisk", "ProjectRiskCube"),
        ("Contract", "ContractCube"),
        ("Supplier", "SupplierCube"),
        ("Company", "CompanyCube"),
    ]
    for code, cube in bindings:
        s.onto.bind_source(code, "dazi_cube", config={"cube": cube})
        output.print(f"OK {code} -> {cube}")

    # 定义属性
    properties = [
        # Date - 日期维度属性
        ("Date", "dateId", "日期ID", "dimension", "DateCube.dateId"),
        ("Date", "date", "日期", "dimension", "DateCube.date"),
        ("Date", "year", "年份", "dimension", "DateCube.year"),
        ("Date", "quarter", "季度", "dimension", "DateCube.quarter"),
        ("Date", "month", "月份", "dimension", "DateCube.month"),
        ("Date", "day", "日期(日)", "dimension", "DateCube.day"),
        ("Date", "weekOfYear", "周序号", "dimension", "DateCube.weekOfYear"),
        ("Date", "monthName", "月份名称", "dimension", "DateCube.monthName"),
        ("Date", "quarterName", "季度名称", "dimension", "DateCube.quarterName"),
        ("Date", "yearMonth", "年月", "dimension", "DateCube.yearMonth"),
        ("Date", "isWeekend", "是否周末", "dimension", "DateCube.isWeekend"),
        ("Date", "holidayFlag", "节假日标志", "dimension", "DateCube.holidayFlag"),
        ("Date", "holidayName", "节假日名称", "dimension", "DateCube.holidayName"),
        # Project
        ("Project", "id", "项目ID", "dimension", "ProjectCube.id"),
        ("Project", "projectCode", "项目编码", "dimension", "ProjectCube.projectCode"),
        ("Project", "projectName", "项目名称", "dimension", "ProjectCube.projectName"),
        ("Project", "projectType", "项目类型", "dimension", "ProjectCube.projectType"),
        ("Project", "projectStatus", "项目状态", "dimension", "ProjectCube.projectStatus"),
        ("Project", "province", "所属省份", "dimension", "ProjectCube.province"),
        ("Project", "city", "所属城市", "dimension", "ProjectCube.city"),
        ("Project", "contractAmount", "合同金额", "measure", "ProjectCube.contractAmount"),
        # Region - 地区维度属性
        ("Region", "regionId", "地区ID", "dimension", "RegionCube.regionId"),
        ("Region", "regionCode", "地区编码", "dimension", "RegionCube.regionCode"),
        ("Region", "regionName", "地区名称", "dimension", "RegionCube.regionName"),
        ("Region", "regionLevel", "地区层级", "dimension", "RegionCube.regionLevel"),
        ("Region", "parentRegionId", "上级地区ID", "dimension", "RegionCube.parentRegionId"),
        ("Region", "isDomestic", "是否国内", "dimension", "RegionCube.isDomestic"),
        ("Region", "majorRegion", "大区", "dimension", "RegionCube.majorRegion"),
        ("Region", "province", "省份", "dimension", "RegionCube.province"),
        ("Region", "city", "城市", "dimension", "RegionCube.city"),
        ("Region", "district", "区县", "dimension", "RegionCube.district"),
        ("Region", "country", "国家", "dimension", "RegionCube.country"),
        ("Region", "overseasRegion", "海外区域", "dimension", "RegionCube.overseasRegion"),
        # Department - 部门维度属性
        ("Department", "departmentId", "部门ID", "dimension", "DepartmentCube.departmentId"),
        ("Department", "departmentCode", "部门编码", "dimension", "DepartmentCube.departmentCode"),
        ("Department", "departmentName", "部门名称", "dimension", "DepartmentCube.departmentName"),
        ("Department", "departmentLevel", "部门层级", "dimension", "DepartmentCube.departmentLevel"),
        ("Department", "parentDepartmentId", "上级部门ID", "dimension", "DepartmentCube.parentDepartmentId"),
        ("Department", "departmentType", "部门类型", "dimension", "DepartmentCube.departmentType"),
        ("Department", "companyId", "所属公司ID", "dimension", "DepartmentCube.companyId"),
        # Owner - 业主维度属性
        ("Owner", "ownerId", "业主ID", "dimension", "OwnerCube.ownerId"),
        ("Owner", "ownerCode", "业主编码", "dimension", "OwnerCube.ownerCode"),
        ("Owner", "ownerName", "业主名称", "dimension", "OwnerCube.ownerName"),
        ("Owner", "ownerType", "业主类型", "dimension", "OwnerCube.ownerType"),
        ("Owner", "ownerLevel", "业主等级", "dimension", "OwnerCube.ownerLevel"),
        ("Owner", "creditRating", "信用等级", "dimension", "OwnerCube.creditRating"),
        ("Owner", "contactPerson", "联系人", "dimension", "OwnerCube.contactPerson"),
        ("Owner", "contactPhone", "联系电话", "dimension", "OwnerCube.contactPhone"),
        ("Owner", "address", "地址", "dimension", "OwnerCube.address"),
        # CostSubject - 成本科目维度属性
        ("CostSubject", "subjectId", "科目ID", "dimension", "CostSubjectCube.subjectId"),
        ("CostSubject", "subjectCode", "科目编码", "dimension", "CostSubjectCube.subjectCode"),
        ("CostSubject", "subjectName", "科目名称", "dimension", "CostSubjectCube.subjectName"),
        ("CostSubject", "subjectLevel", "科目层级", "dimension", "CostSubjectCube.subjectLevel"),
        ("CostSubject", "parentSubjectId", "上级科目ID", "dimension", "CostSubjectCube.parentSubjectId"),
        ("CostSubject", "subjectCategory", "科目类别", "dimension", "CostSubjectCube.subjectCategory"),
        ("CostSubject", "subjectType", "科目类型", "dimension", "CostSubjectCube.subjectType"),
        # ProjectOutput
        ("ProjectOutput", "id", "产值记录ID", "dimension", "ProjectOutputCube.id"),
        ("ProjectOutput", "projectId", "项目ID", "dimension", "ProjectOutputCube.projectId"),
        ("ProjectOutput", "reportPeriod", "报告期间", "dimension", "ProjectOutputCube.reportPeriod"),
        ("ProjectOutput", "outputValue", "产值金额", "measure", "ProjectOutputCube.outputValue"),
        ("ProjectOutput", "outputTax", "产值税额", "measure", "ProjectOutputCube.outputTax"),
        ("ProjectOutput", "outputWithoutTax", "产值不含税", "measure", "ProjectOutputCube.outputWithoutTax"),
        ("ProjectOutput", "outputType", "产值类型", "dimension", "ProjectOutputCube.outputType"),
        # ProjectCost
        ("ProjectCost", "id", "成本记录ID", "dimension", "ProjectCostCube.id"),
        ("ProjectCost", "projectId", "项目ID", "dimension", "ProjectCostCube.projectId"),
        ("ProjectCost", "contractId", "合同ID", "dimension", "ProjectCostCube.contractId"),
        ("ProjectCost", "reportPeriod", "报告期间", "dimension", "ProjectCostCube.reportPeriod"),
        ("ProjectCost", "costAmount", "成本金额", "measure", "ProjectCostCube.costAmount"),
        ("ProjectCost", "costType", "成本类型", "dimension", "ProjectCostCube.costType"),
        ("ProjectCost", "laborCost", "人工费", "measure", "ProjectCostCube.laborCost"),
        ("ProjectCost", "materialCost", "材料费", "measure", "ProjectCostCube.materialCost"),
        ("ProjectCost", "mechanicalCost", "机械费", "measure", "ProjectCostCube.mechanicalCost"),
        ("ProjectCost", "otherCost", "其他费用", "measure", "ProjectCostCube.otherCost"),
        # ProjectIndicator
        ("ProjectIndicator", "id", "指标记录ID", "dimension", "ProjectIndicatorCube.id"),
        ("ProjectIndicator", "projectId", "项目ID", "dimension", "ProjectIndicatorCube.projectId"),
        ("ProjectIndicator", "companyId", "分公司ID", "dimension", "ProjectIndicatorCube.companyId"),
        ("ProjectIndicator", "reportPeriod", "报告期间", "dimension", "ProjectIndicatorCube.reportPeriod"),
        ("ProjectIndicator", "indicatorType", "指标类型", "dimension", "ProjectIndicatorCube.indicatorType"),
        ("ProjectIndicator", "indicatorValue", "指标值", "measure", "ProjectIndicatorCube.indicatorValue"),
        ("ProjectIndicator", "targetValue", "目标值", "measure", "ProjectIndicatorCube.targetValue"),
        ("ProjectIndicator", "achievementRate", "完成率", "measure", "ProjectIndicatorCube.achievementRate"),
        # ProjectPayment
        ("ProjectPayment", "id", "付款记录ID", "dimension", "ProjectPaymentCube.id"),
        ("ProjectPayment", "projectId", "项目ID", "dimension", "ProjectPaymentCube.projectId"),
        ("ProjectPayment", "contractId", "合同ID", "dimension", "ProjectPaymentCube.contractId"),
        ("ProjectPayment", "reportPeriod", "报告期间", "dimension", "ProjectPaymentCube.reportPeriod"),
        ("ProjectPayment", "payableConfirmed", "已确认应付款", "measure", "ProjectPaymentCube.payableConfirmed"),
        ("ProjectPayment", "laborPayable", "人工费应付款", "measure", "ProjectPaymentCube.laborPayable"),
        ("ProjectPayment", "paidAmount", "已付款金额", "measure", "ProjectPaymentCube.paidAmount"),
        ("ProjectPayment", "payableUnconfirmed", "待确认应付款", "measure", "ProjectPaymentCube.payableUnconfirmed"),
        # ProjectBalance
        ("ProjectBalance", "id", "收支记录ID", "dimension", "ProjectBalanceCube.id"),
        ("ProjectBalance", "projectId", "项目ID", "dimension", "ProjectBalanceCube.projectId"),
        ("ProjectBalance", "reportPeriod", "报告期间", "dimension", "ProjectBalanceCube.reportPeriod"),
        ("ProjectBalance", "subjectCode", "科目编码", "dimension", "ProjectBalanceCube.subjectCode"),
        ("ProjectBalance", "subjectName", "科目名称", "dimension", "ProjectBalanceCube.subjectName"),
        ("ProjectBalance", "projectAmount", "项目层面金额", "measure", "ProjectBalanceCube.projectAmount"),
        ("ProjectBalance", "companyAmount", "公司层面金额", "measure", "ProjectBalanceCube.companyAmount"),
        ("ProjectBalance", "totalAmount", "合计金额", "measure", "ProjectBalanceCube.totalAmount"),
        # ProjectRisk
        ("ProjectRisk", "id", "风险记录ID", "dimension", "ProjectRiskCube.id"),
        ("ProjectRisk", "projectId", "项目ID", "dimension", "ProjectRiskCube.projectId"),
        ("ProjectRisk", "reportPeriod", "报告期间", "dimension", "ProjectRiskCube.reportPeriod"),
        ("ProjectRisk", "riskType", "风险类型", "dimension", "ProjectRiskCube.riskType"),
        ("ProjectRisk", "riskCode", "风险编码", "dimension", "ProjectRiskCube.riskCode"),
        ("ProjectRisk", "riskName", "风险名称", "dimension", "ProjectRiskCube.riskName"),
        ("ProjectRisk", "riskValue", "风险值", "measure", "ProjectRiskCube.riskValue"),
        # Contract
        ("Contract", "id", "合同ID", "dimension", "ContractCube.id"),
        ("Contract", "contractCode", "合同编码", "dimension", "ContractCube.contractCode"),
        ("Contract", "contractName", "合同名称", "dimension", "ContractCube.contractName"),
        ("Contract", "supplierName", "供应商名称", "dimension", "ContractCube.supplierName"),
        ("Contract", "contractAmount", "合同金额", "measure", "ContractCube.contractAmount"),
        ("Contract", "paymentRatio", "付款比例", "measure", "ContractCube.paymentRatio"),
        ("Contract", "taxRate", "税率", "measure", "ContractCube.taxRate"),
        # Supplier
        ("Supplier", "id", "供应商ID", "dimension", "SupplierCube.id"),
        ("Supplier", "supplierName", "供应商名称", "dimension", "SupplierCube.supplierName"),
        ("Supplier", "supplierType", "供应商类型", "dimension", "SupplierCube.supplierType"),
        ("Supplier", "contactPerson", "联系人", "dimension", "SupplierCube.contactPerson"),
        ("Supplier", "contactPhone", "联系电话", "dimension", "SupplierCube.contactPhone"),
        # Company
        ("Company", "id", "分公司ID", "dimension", "CompanyCube.id"),
        ("Company", "companyCode", "分公司编码", "dimension", "CompanyCube.companyCode"),
        ("Company", "companyName", "分公司名称", "dimension", "CompanyCube.companyName"),
        ("Company", "province", "所在省份", "dimension", "CompanyCube.province"),
        ("Company", "city", "所在城市", "dimension", "CompanyCube.city"),
    ]
    for obj_code, prop_code, title, role, qualified_name in properties:
        s.onto.define_property(obj_code, prop_code, title, semantic_role=role, qualified_name=qualified_name)
    output.print(f"OK {len(properties)} 个属性")

    # 7. 定义链接类型
    output.print("\n[7/7] 定义链接类型...")

    link_types = [
        ("belongsTo_ProjectOutput_Project", "产值属于项目", "ProjectOutput", "Project"),
        ("belongsTo_ProjectCost_Project", "成本属于项目", "ProjectCost", "Project"),
        ("belongsTo_ProjectPayment_Project", "付款属于项目", "ProjectPayment", "Project"),
        ("belongsTo_ProjectBalance_Project", "收支属于项目", "ProjectBalance", "Project"),
        ("belongsTo_ProjectIndicator_Project", "指标属于项目", "ProjectIndicator", "Project"),
        ("belongsTo_ProjectRisk_Project", "风险属于项目", "ProjectRisk", "Project"),
        ("belongsTo_Contract_Project", "合同属于项目", "Contract", "Project"),
        ("belongsTo_Project_Company", "项目属于分公司", "Project", "Company"),
        ("belongsTo_Supplier_Company", "供应商属于分公司", "Supplier", "Company"),
        ("contains_ProjectCost_Contract", "成本包含合同项", "ProjectCost", "Contract"),
        ("contains_ProjectPayment_Contract", "付款包含合同项", "ProjectPayment", "Contract"),
    ]
    for code, name, from_obj, to_obj in link_types:
        s.onto.define_link_type(code, name, from_object_type_code=from_obj, to_object_type_code=to_obj)
        output.print(f"OK {code}")

    # 同步指标引用
    s.sync_metric_refs()
    output.print("OK sync_metric_refs")

    output.print("\n=== 商务成本本体初始化完成 ===")

    return p.function_result(success=True, data={"message": "本体初始化完成"})


# 测试参数定义
TEST_ARGUMENTS = {"arguments": {"space_id": "space__panda_construction"}}