"""潘达工程商务成本本体初始化脚本 V3.0 — space__panda_construction

阶段二 V3.0 全新实现（用户手动重建数据空间后发布）。

初始化内容：
1. 创建物理表（dim_date + 6 维 + 13 事实 = 20 张）
2. 创建读模型 VIEW（ProjectCube / CostOutputComparisonCube）
3. 注册表到空间（TABLE_REGISTRY + register_with_meta）
4. 注册表间关系（V3 文档 §5，25+ 条）
5. 注册 Cube（各 fact/dim 主体 + 2 个 VIEW Cube）及派生度量
6. 定义对象类型（20 + CostManagementAnalysis）、属性、链接（~26 条）
7. 同步指标引用

不含 apply_registry（分类在 category_mount 脚本）。

放置：项目/潘达工程-商务成本/本体/ontos/本体规划03/setup/panda_cost_v3_ontology_init.py
规划对照：
- 规划/200-阶段二-本体设计与确认/150-本体设计确认/020-本体规划文档.md
- 规划/200-阶段二-本体设计与确认/140-本体物理表模型设计/010-物理表设计文档.md
- 规划/200-阶段二-本体设计与确认/150-本体设计确认/030-派生属性定义.md
"""

import json

# 与 V3 规划 §2 对齐：display_name=侧栏显示名，description=业务说明
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
    "dim_company": {
        "display_name": "分公司维表",
        "description": "分公司/子公司主数据",
        "columns": [
            {"name": "company_id", "display_name": "分公司ID", "description": "主键"},
            {"name": "company_code", "display_name": "分公司编码"},
            {"name": "company_name", "display_name": "分公司名称"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_employer": {
        "display_name": "发包人维表",
        "description": "发包人/业主主数据",
        "columns": [
            {"name": "employer_id", "display_name": "发包人ID", "description": "主键"},
            {"name": "employer_code", "display_name": "发包人编号"},
            {"name": "employer_name", "display_name": "发包人名称"},
            {"name": "credit_code", "display_name": "统一社会信用代码"},
            {"name": "contact_person", "display_name": "联系人"},
            {"name": "contact_phone", "display_name": "联系方式"},
            {"name": "industry", "display_name": "所属行业"},
            {"name": "fund_source", "display_name": "资金来源"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_contractor": {
        "display_name": "总承包人维表",
        "description": "总承包人/施工单位主数据",
        "columns": [
            {"name": "contractor_id", "display_name": "总承包人ID", "description": "主键"},
            {"name": "contractor_code", "display_name": "总承包人编号"},
            {"name": "contractor_name", "display_name": "总承包人名称"},
            {"name": "qualification_level", "display_name": "资质等级"},
            {"name": "project_manager", "display_name": "项目经理"},
            {"name": "safety_license", "display_name": "安全许可证"},
            {"name": "credit_rating", "display_name": "信用等级"},
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
            {"name": "supplier_type", "display_name": "供应商类型"},
            {"name": "company_id", "display_name": "所属分公司", "description": "FK→dim_company"},
            {"name": "contact_person", "display_name": "联系人"},
            {"name": "contact_phone", "display_name": "联系电话"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_subcontractor": {
        "display_name": "分包商维表",
        "description": "分包商主数据",
        "columns": [
            {"name": "subcontractor_id", "display_name": "分包商ID", "description": "主键"},
            {"name": "subcontractor_code", "display_name": "分包商编号"},
            {"name": "subcontractor_name", "display_name": "分包商名称"},
            {"name": "qualification_level", "display_name": "资质等级"},
            {"name": "professional_category", "display_name": "专业类别"},
            {"name": "project_manager", "display_name": "项目经理"},
            {"name": "subcontract_type", "display_name": "分包类型", "description": "劳务/专业"},
            {"name": "safety_license", "display_name": "安全许可证"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_project": {
        "display_name": "项目维表",
        "description": "施工项目主数据（含标段属性，Section 不建独立对象）",
        "columns": [
            {"name": "project_id", "display_name": "项目ID", "description": "主键"},
            {"name": "project_code", "display_name": "项目编码"},
            {"name": "project_name", "display_name": "项目名称"},
            {"name": "company_id", "display_name": "所属分公司", "description": "FK→dim_company"},
            {"name": "company_name", "display_name": "分公司名称", "description": "冗余"},
            {"name": "employer_id", "display_name": "发包人", "description": "FK→dim_employer"},
            {"name": "employer_name", "display_name": "发包人名称", "description": "冗余"},
            {"name": "contractor_id", "display_name": "总承包人", "description": "FK→dim_contractor"},
            {"name": "contractor_name", "display_name": "总承包人名称", "description": "冗余"},
            {"name": "section_id", "display_name": "标段ID"},
            {"name": "section_name", "display_name": "标段名称"},
            {"name": "building_area", "display_name": "建筑面积"},
            {"name": "contract_amount", "display_name": "合同金额"},
            {"name": "project_status", "display_name": "项目状态", "description": "在建/竣工/结算/归档"},
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
        "description": "月度成本汇总（三级成本 L1/L2/L3）",
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
            {"name": "cost_code", "display_name": "三级成本编码"},
            {"name": "cost_name", "display_name": "成本名称"},
            {"name": "cost_level", "display_name": "成本层级", "description": "L1/L2/L3"},
            {"name": "contract_id", "display_name": "关联合同"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_project_payment": {
        "display_name": "项目付款事实表",
        "description": "月度付款与应付款（含合同冗余字段供 Contract 对象绑定）",
        "columns": [
            {"name": "payment_id", "display_name": "付款记录ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "FK→dim_date"},
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "contract_id", "display_name": "合同ID"},
            {"name": "contract_code", "display_name": "合同编码", "description": "冗余"},
            {"name": "contract_name", "display_name": "合同名称", "description": "冗余"},
            {"name": "contract_amount", "display_name": "合同金额", "description": "冗余"},
            {"name": "tax_rate", "display_name": "税率", "description": "冗余"},
            {"name": "settlement_status", "display_name": "结算状态", "description": "冗余"},
            {"name": "supplier_id", "display_name": "供应商ID"},
            {"name": "supplier_name", "display_name": "供应商名称", "description": "冗余"},
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
            {"name": "subject_code", "display_name": "科目编码"},
            {"name": "subject_name", "display_name": "科目名称"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "project_amount", "display_name": "项目层面金额"},
            {"name": "company_amount", "display_name": "公司层面金额"},
            {"name": "total_amount", "display_name": "合计金额"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_project_indicator": {
        "display_name": "项目指标事实表",
        "description": "核心商务指标",
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
        "description": "风险清单与三色预警（绿/黄/红）",
        "columns": [
            {"name": "risk_id", "display_name": "风险记录ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "FK→dim_date"},
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "risk_type", "display_name": "风险类型"},
            {"name": "risk_code", "display_name": "风险编码"},
            {"name": "risk_name", "display_name": "风险名称"},
            {"name": "risk_value", "display_name": "风险值"},
            {"name": "warning_level", "display_name": "预警级别", "description": "绿/黄/红"},
            {"name": "risk_description", "display_name": "风险描述"},
            {"name": "overall_warning_level", "display_name": "综合预警"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_receipt": {
        "display_name": "收款事实表",
        "description": "项目收款记录",
        "columns": [
            {"name": "receipt_id", "display_name": "收款记录ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "FK→dim_date"},
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "contract_id", "display_name": "合同ID"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "receipt_amount", "display_name": "收款金额"},
            {"name": "receipt_date", "display_name": "收款日期"},
            {"name": "receipt_method", "display_name": "收款方式"},
            {"name": "receipt_type", "display_name": "收款类型", "description": "预付款/进度款/结算款/质保金"},
            {"name": "overdue_days", "display_name": "逾期天数"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_settlement": {
        "display_name": "结算事实表",
        "description": "项目结算记录（含三算对比）",
        "columns": [
            {"name": "settlement_id", "display_name": "结算记录ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "FK→dim_date"},
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "settlement_amount", "display_name": "结算金额"},
            {"name": "settlement_date", "display_name": "结算日期"},
            {"name": "audit_status", "display_name": "审核状态"},
            {"name": "audit_opinion", "display_name": "审计意见"},
            {"name": "three_estimate_comparison", "display_name": "三算对比", "description": "概算/预算/决算"},
            {"name": "review_deduction_amount", "display_name": "审减金额"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_bond": {
        "display_name": "保证金事实表",
        "description": "投标/履约/质量/农民工工资保证金",
        "columns": [
            {"name": "bond_id", "display_name": "保证金记录ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "FK→dim_date"},
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "contract_id", "display_name": "合同ID"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "bond_type", "display_name": "保证金类型"},
            {"name": "bond_amount", "display_name": "保证金金额"},
            {"name": "payment_date", "display_name": "缴纳日期"},
            {"name": "due_date", "display_name": "到期日期"},
            {"name": "return_conditions", "display_name": "退还条件"},
            {"name": "returned_amount", "display_name": "已退还金额"},
            {"name": "unreturned_amount", "display_name": "未退还金额"},
            {"name": "forfeit_status", "display_name": "没收状态"},
            {"name": "forfeit_amount", "display_name": "没收金额"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_penalty": {
        "display_name": "罚款事实表",
        "description": "违约/违规/质量安全罚款",
        "columns": [
            {"name": "penalty_id", "display_name": "罚款记录ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "FK→dim_date"},
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "penalty_type", "display_name": "罚款类型"},
            {"name": "penalty_amount", "display_name": "罚款金额"},
            {"name": "penalty_reason", "display_name": "罚款原因"},
            {"name": "issuing_unit", "display_name": "开具单位"},
            {"name": "penalty_date", "display_name": "罚款日期"},
            {"name": "payment_status", "display_name": "缴纳状态"},
            {"name": "appeal_status", "display_name": "申诉状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_compensation": {
        "display_name": "赔偿事实表",
        "description": "合同/侵权/工伤赔偿",
        "columns": [
            {"name": "compensation_id", "display_name": "赔偿记录ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "FK→dim_date"},
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "compensation_type", "display_name": "赔偿类型"},
            {"name": "compensation_amount", "display_name": "赔偿金额"},
            {"name": "compensation_reason", "display_name": "赔偿原因"},
            {"name": "responsible_party", "display_name": "责任方"},
            {"name": "compensation_date", "display_name": "赔偿日期"},
            {"name": "payment_status", "display_name": "支付状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_insurance": {
        "display_name": "工程保险事实表",
        "description": "工程险/意外险/责任险",
        "columns": [
            {"name": "insurance_id", "display_name": "保险记录ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "FK→dim_date"},
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "insurance_type", "display_name": "保险类型"},
            {"name": "insurance_company", "display_name": "保险公司"},
            {"name": "insurance_amount", "display_name": "保险金额"},
            {"name": "premium_amount", "display_name": "保费金额"},
            {"name": "purchase_date", "display_name": "投保日期"},
            {"name": "expiry_date", "display_name": "到期日期"},
            {"name": "claim_status", "display_name": "理赔状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_equipment": {
        "display_name": "机械设备事实表",
        "description": "项目机械设备台账",
        "columns": [
            {"name": "equipment_id", "display_name": "设备记录ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "FK→dim_date"},
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "report_period", "display_name": "报告期间"},
            {"name": "equipment_code", "display_name": "设备编号"},
            {"name": "equipment_name", "display_name": "设备名称"},
            {"name": "model_spec", "display_name": "型号规格"},
            {"name": "original_value", "display_name": "原值"},
            {"name": "depreciation_method", "display_name": "折旧方法"},
            {"name": "unit_price", "display_name": "台班单价"},
            {"name": "usage_status", "display_name": "使用状态"},
            {"name": "equipment_status", "display_name": "设备状态", "description": "自有/租赁"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
}

# 读模型 VIEW 元数据（不计入 20 张物理表）
VIEW_REGISTRY = {
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
    "view_project_cube": {
        "display_name": "项目Cube读模型",
        "description": "dim_project + 多事实表聚合",
        "columns": [
            {"name": "project_id", "display_name": "项目ID"},
            {"name": "project_code", "display_name": "项目编码"},
            {"name": "project_name", "display_name": "项目名称"},
            {"name": "company_id", "display_name": "分公司ID"},
            {"name": "company_name", "display_name": "分公司名称"},
            {"name": "employer_id", "display_name": "发包人ID"},
            {"name": "employer_name", "display_name": "发包人名称"},
            {"name": "section_id", "display_name": "标段ID"},
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
}

def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)

    output.print("=== 潘达工程商务成本本体初始化 V3.0 ===")
    output.print(f"空间: {space_id}")

    # 1. 创建物理表（dim_date + 6 维 + 13 事实）
    output.print("\n[1/8] 创建物理表...")

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

    s.sql.execute("DROP TABLE IF EXISTS dim_company")
    s.sql.execute("""
        CREATE TABLE dim_company (
            company_id String COMMENT '分公司ID',
            company_code String COMMENT '分公司编码',
            company_name String COMMENT '分公司名称',
            status String DEFAULT 'active' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (company_code)
    """)
    output.print("OK dim_company")

    s.sql.execute("DROP TABLE IF EXISTS dim_employer")
    s.sql.execute("""
        CREATE TABLE dim_employer (
            employer_id String COMMENT '发包人ID',
            employer_code String COMMENT '发包人编号',
            employer_name String COMMENT '发包人名称',
            credit_code String COMMENT '统一社会信用代码',
            contact_person String COMMENT '联系人',
            contact_phone String COMMENT '联系方式',
            industry String COMMENT '所属行业',
            fund_source String COMMENT '资金来源',
            status String DEFAULT 'active' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (employer_code)
    """)
    output.print("OK dim_employer")

    s.sql.execute("DROP TABLE IF EXISTS dim_contractor")
    s.sql.execute("""
        CREATE TABLE dim_contractor (
            contractor_id String COMMENT '总承包人ID',
            contractor_code String COMMENT '总承包人编号',
            contractor_name String COMMENT '总承包人名称',
            qualification_level String COMMENT '资质等级',
            project_manager String COMMENT '项目经理',
            safety_license String COMMENT '安全许可证',
            credit_rating String COMMENT '信用等级',
            status String DEFAULT 'active' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (contractor_code)
    """)
    output.print("OK dim_contractor")

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

    s.sql.execute("DROP TABLE IF EXISTS dim_subcontractor")
    s.sql.execute("""
        CREATE TABLE dim_subcontractor (
            subcontractor_id String COMMENT '分包商ID',
            subcontractor_code String COMMENT '分包商编号',
            subcontractor_name String COMMENT '分包商名称',
            qualification_level String COMMENT '资质等级',
            professional_category String COMMENT '专业类别',
            project_manager String COMMENT '项目经理',
            subcontract_type String COMMENT '分包类型',
            safety_license String COMMENT '安全许可证',
            status String DEFAULT 'active' COMMENT '状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (subcontractor_code)
    """)
    output.print("OK dim_subcontractor")

    s.sql.execute("DROP TABLE IF EXISTS dim_project")
    s.sql.execute("""
        CREATE TABLE dim_project (
            project_id String COMMENT '项目ID',
            project_code String COMMENT '项目编码',
            project_name String COMMENT '项目名称',
            company_id String COMMENT '所属分公司',
            company_name String COMMENT '分公司名称',
            employer_id String COMMENT '发包人',
            employer_name String COMMENT '发包人名称',
            contractor_id String COMMENT '总承包人',
            contractor_name String COMMENT '总承包人名称',
            section_id String COMMENT '标段ID',
            section_name String COMMENT '标段名称',
            building_area Float64 COMMENT '建筑面积',
            contract_amount Float64 COMMENT '合同金额',
            project_status String DEFAULT '在建' COMMENT '项目状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (company_id, project_code)
    """)
    output.print("OK dim_project")

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
            cost_code String COMMENT '三级成本编码',
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
            contract_code String COMMENT '合同编码',
            contract_name String COMMENT '合同名称',
            contract_amount Float64 COMMENT '合同金额',
            tax_rate Float64 COMMENT '税率',
            settlement_status String COMMENT '结算状态',
            supplier_id String COMMENT '供应商ID',
            supplier_name String COMMENT '供应商名称',
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

    s.sql.execute("DROP TABLE IF EXISTS fact_receipt")
    s.sql.execute("""
        CREATE TABLE fact_receipt (
            receipt_id String COMMENT '收款记录ID',
            date_key Int32 COMMENT '日期键',
            project_id String COMMENT '项目ID',
            contract_id String COMMENT '合同ID',
            report_period String COMMENT '报告期间',
            receipt_amount Float64 COMMENT '收款金额',
            receipt_date Date COMMENT '收款日期',
            receipt_method String COMMENT '收款方式',
            receipt_type String COMMENT '收款类型',
            overdue_days Int32 COMMENT '逾期天数',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id, receipt_id)
    """)
    output.print("OK fact_receipt")

    s.sql.execute("DROP TABLE IF EXISTS fact_settlement")
    s.sql.execute("""
        CREATE TABLE fact_settlement (
            settlement_id String COMMENT '结算记录ID',
            date_key Int32 COMMENT '日期键',
            project_id String COMMENT '项目ID',
            report_period String COMMENT '报告期间',
            settlement_amount Float64 COMMENT '结算金额',
            settlement_date Date COMMENT '结算日期',
            audit_status String COMMENT '审核状态',
            audit_opinion String COMMENT '审计意见',
            three_estimate_comparison String COMMENT '三算对比',
            review_deduction_amount Float64 COMMENT '审减金额',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id, settlement_id)
    """)
    output.print("OK fact_settlement")

    s.sql.execute("DROP TABLE IF EXISTS fact_bond")
    s.sql.execute("""
        CREATE TABLE fact_bond (
            bond_id String COMMENT '保证金记录ID',
            date_key Int32 COMMENT '日期键',
            project_id String COMMENT '项目ID',
            contract_id String COMMENT '合同ID',
            report_period String COMMENT '报告期间',
            bond_type String COMMENT '保证金类型',
            bond_amount Float64 COMMENT '保证金金额',
            payment_date Date COMMENT '缴纳日期',
            due_date Date COMMENT '到期日期',
            return_conditions String COMMENT '退还条件',
            returned_amount Float64 COMMENT '已退还金额',
            unreturned_amount Float64 COMMENT '未退还金额',
            forfeit_status String COMMENT '没收状态',
            forfeit_amount Float64 COMMENT '没收金额',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id, bond_id)
    """)
    output.print("OK fact_bond")

    s.sql.execute("DROP TABLE IF EXISTS fact_penalty")
    s.sql.execute("""
        CREATE TABLE fact_penalty (
            penalty_id String COMMENT '罚款记录ID',
            date_key Int32 COMMENT '日期键',
            project_id String COMMENT '项目ID',
            report_period String COMMENT '报告期间',
            penalty_type String COMMENT '罚款类型',
            penalty_amount Float64 COMMENT '罚款金额',
            penalty_reason String COMMENT '罚款原因',
            issuing_unit String COMMENT '开具单位',
            penalty_date Date COMMENT '罚款日期',
            payment_status String COMMENT '缴纳状态',
            appeal_status String COMMENT '申诉状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id, penalty_id)
    """)
    output.print("OK fact_penalty")

    s.sql.execute("DROP TABLE IF EXISTS fact_compensation")
    s.sql.execute("""
        CREATE TABLE fact_compensation (
            compensation_id String COMMENT '赔偿记录ID',
            date_key Int32 COMMENT '日期键',
            project_id String COMMENT '项目ID',
            report_period String COMMENT '报告期间',
            compensation_type String COMMENT '赔偿类型',
            compensation_amount Float64 COMMENT '赔偿金额',
            compensation_reason String COMMENT '赔偿原因',
            responsible_party String COMMENT '责任方',
            compensation_date Date COMMENT '赔偿日期',
            payment_status String COMMENT '支付状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id, compensation_id)
    """)
    output.print("OK fact_compensation")

    s.sql.execute("DROP TABLE IF EXISTS fact_insurance")
    s.sql.execute("""
        CREATE TABLE fact_insurance (
            insurance_id String COMMENT '保险记录ID',
            date_key Int32 COMMENT '日期键',
            project_id String COMMENT '项目ID',
            report_period String COMMENT '报告期间',
            insurance_type String COMMENT '保险类型',
            insurance_company String COMMENT '保险公司',
            insurance_amount Float64 COMMENT '保险金额',
            premium_amount Float64 COMMENT '保费金额',
            purchase_date Date COMMENT '投保日期',
            expiry_date Date COMMENT '到期日期',
            claim_status String COMMENT '理赔状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id, insurance_id)
    """)
    output.print("OK fact_insurance")

    s.sql.execute("DROP TABLE IF EXISTS fact_equipment")
    s.sql.execute("""
        CREATE TABLE fact_equipment (
            equipment_id String COMMENT '设备记录ID',
            date_key Int32 COMMENT '日期键',
            project_id String COMMENT '项目ID',
            report_period String COMMENT '报告期间',
            equipment_code String COMMENT '设备编号',
            equipment_name String COMMENT '设备名称',
            model_spec String COMMENT '型号规格',
            original_value Float64 COMMENT '原值',
            depreciation_method String COMMENT '折旧方法',
            unit_price Float64 COMMENT '台班单价',
            usage_status String COMMENT '使用状态',
            equipment_status String COMMENT '设备状态',
            created_at DateTime DEFAULT now() COMMENT '创建时间'
        ) ENGINE = MergeTree()
        ORDER BY (date_key, project_id, equipment_code)
    """)
    output.print("OK fact_equipment")

    # 1b. 创建读模型 VIEW
    output.print("\n[1b/8] 创建读模型 VIEW...")

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
            SELECT project_id, report_period, total_output, confirmed_output,
                toFloat64(0) AS cost_confirmed_acc, toFloat64(0) AS cost_unconfirmed_acc, toFloat64(0) AS target_cost
            FROM fact_project_output
            UNION ALL
            SELECT project_id, report_period, toFloat64(0), toFloat64(0),
                cost_confirmed_acc, cost_unconfirmed_acc, target_cost
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
            p.employer_id AS employer_id,
            p.employer_name AS employer_name,
            p.section_id AS section_id,
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
                UNION DISTINCT SELECT project_id, report_period FROM fact_project_cost
                UNION DISTINCT SELECT project_id, report_period FROM fact_project_payment
                UNION DISTINCT SELECT project_id, report_period FROM fact_project_indicator
                UNION DISTINCT SELECT project_id, report_period FROM fact_project_risk
                UNION DISTINCT SELECT project_id, report_period FROM fact_receipt
                UNION DISTINCT SELECT project_id, report_period FROM fact_settlement
                UNION DISTINCT SELECT project_id, report_period FROM fact_bond
                UNION DISTINCT SELECT project_id, report_period FROM fact_penalty
                UNION DISTINCT SELECT project_id, report_period FROM fact_compensation
                UNION DISTINCT SELECT project_id, report_period FROM fact_insurance
                UNION DISTINCT SELECT project_id, report_period FROM fact_equipment
            ) AS keys
            LEFT JOIN (
                SELECT project_id, report_period, sum(confirmed_output) AS confirmed_output, sum(total_output) AS total_output
                FROM fact_project_output GROUP BY project_id, report_period
            ) AS o ON keys.project_id = o.project_id AND keys.report_period = o.report_period
            LEFT JOIN (
                SELECT project_id, report_period, sum(cost_confirmed_acc) AS cost_confirmed_acc, sum(labor_cost_acc) AS labor_cost_acc
                FROM fact_project_cost GROUP BY project_id, report_period
            ) AS c ON keys.project_id = c.project_id AND keys.report_period = c.report_period
            LEFT JOIN (
                SELECT project_id, report_period, sum(paid_amount) AS paid_amount, sum(payable_confirmed) AS payable_confirmed
                FROM fact_project_payment GROUP BY project_id, report_period
            ) AS pm ON keys.project_id = pm.project_id AND keys.report_period = pm.report_period
            LEFT JOIN (
                SELECT project_id, report_period, sum(receipt_amount) AS received_amount
                FROM fact_receipt GROUP BY project_id, report_period
            ) AS rec ON keys.project_id = rec.project_id AND keys.report_period = rec.report_period
            LEFT JOIN (
                SELECT project_id, report_period, sum(risk_value) AS risk_value_sum
                FROM fact_project_risk GROUP BY project_id, report_period
            ) AS rk ON keys.project_id = rk.project_id AND keys.report_period = rk.report_period
        ) AS agg ON p.project_id = agg.project_id
    """)
    output.print("OK view_project_cube")

    # 2. 注册表
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
    for view_name, meta in VIEW_REGISTRY.items():
        s.tables.register_with_meta(
            table_name=view_name,
            display_name=meta["display_name"],
            description=meta.get("description"),
            columns=meta["columns"],
            force_column_meta=True,
        )
        output.print(f"OK {view_name} ({meta['display_name']})")

    # 3. 注册表间关系（V3 §5，37 条）
    output.print("\n[3/8] 注册表间关系...")
    fact_tables = [
        "fact_project_output", "fact_project_cost", "fact_project_payment",
        "fact_project_balance", "fact_project_indicator", "fact_project_risk",
        "fact_receipt", "fact_settlement", "fact_bond", "fact_penalty",
        "fact_compensation", "fact_insurance", "fact_equipment",
    ]
    table_relationships = []
    for ft in fact_tables:
        table_relationships.append({
            "from_table": ft, "to_table": "dim_date",
            "join_sql": f"{ft}.date_key = dim_date.date_key",
            "join_keys": [{"from": "date_key", "to": "date_key"}],
            "relationship_type": "many_to_one",
            "description": f"{ft} 关联日历",
        })
        table_relationships.append({
            "from_table": ft, "to_table": "dim_project",
            "join_sql": f"{ft}.project_id = dim_project.project_id",
            "join_keys": [{"from": "project_id", "to": "project_id"}],
            "relationship_type": "many_to_one",
            "description": f"{ft} 关联项目",
        })
    table_relationships.extend([
        {"from_table": "dim_project", "to_table": "dim_company", "join_sql": "dim_project.company_id = dim_company.company_id", "join_keys": [{"from": "company_id", "to": "company_id"}], "relationship_type": "many_to_one", "description": "项目关联分公司"},
        {"from_table": "dim_project", "to_table": "dim_employer", "join_sql": "dim_project.employer_id = dim_employer.employer_id", "join_keys": [{"from": "employer_id", "to": "employer_id"}], "relationship_type": "many_to_one", "description": "项目关联发包人"},
        {"from_table": "dim_project", "to_table": "dim_contractor", "join_sql": "dim_project.contractor_id = dim_contractor.contractor_id", "join_keys": [{"from": "contractor_id", "to": "contractor_id"}], "relationship_type": "many_to_one", "description": "项目关联总承包人"},
        {"from_table": "dim_supplier", "to_table": "dim_company", "join_sql": "dim_supplier.company_id = dim_company.company_id", "join_keys": [{"from": "company_id", "to": "company_id"}], "relationship_type": "many_to_one", "description": "供应商关联分公司"},
        {"from_table": "fact_project_payment", "to_table": "dim_supplier", "join_sql": "fact_project_payment.supplier_id = dim_supplier.supplier_id", "join_keys": [{"from": "supplier_id", "to": "supplier_id"}], "relationship_type": "many_to_one", "description": "付款关联供应商"},
        {"from_table": "fact_bond", "to_table": "fact_project_payment", "join_sql": "fact_bond.contract_id = fact_project_payment.contract_id", "join_keys": [{"from": "contract_id", "to": "contract_id"}], "relationship_type": "many_to_one", "description": "保证金关联合同付款"},
        {"from_table": "fact_penalty", "to_table": "fact_project_cost", "join_sql": "fact_penalty.project_id = fact_project_cost.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "罚款计入成本"},
        {"from_table": "fact_insurance", "to_table": "fact_project_cost", "join_sql": "fact_insurance.project_id = fact_project_cost.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "保费计入成本"},
        {"from_table": "fact_equipment", "to_table": "fact_project_cost", "join_sql": "fact_equipment.project_id = fact_project_cost.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "设备费计入成本"},
        {"from_table": "fact_receipt", "to_table": "fact_project_output", "join_sql": "fact_receipt.project_id = fact_project_output.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "收款关联产值"},
        {"from_table": "fact_settlement", "to_table": "fact_project_cost", "join_sql": "fact_settlement.project_id = fact_project_cost.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "结算影响成本"},
        {"from_table": "fact_settlement", "to_table": "fact_receipt", "join_sql": "fact_settlement.project_id = fact_receipt.project_id", "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one", "description": "结算后收款"},
    ])
    for rel in table_relationships:
        s.tables.add_relationship(**rel)
        output.print(f"OK {rel['from_table']} -> {rel['to_table']}")

    # 4. 注册 Cube
    output.print("\n[4/8] 注册 Cube...")

    s.register_cube(
        name="DateCube",
        table="dim_date",
        title="日期Cube",
        category_347="主体型",
        measures=[{"name": "date_count", "col": "date_key", "agg": "count", "title": "日期数量"}],
        dimensions=[
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "calendar_date", "col": "calendar_date", "type": "date", "title": "自然日"},
            {"name": "year", "col": "year", "type": "int", "title": "公历年"},
            {"name": "quarter", "col": "quarter", "type": "int", "title": "季度"},
            {"name": "month", "col": "month", "type": "int", "title": "月"},
            {"name": "year_month", "col": "year_month", "type": "string", "title": "年月"},
        ],
    )
    output.print("OK DateCube")

    s.register_cube(
        name="CompanyCube",
        table="dim_company",
        title="分公司Cube",
        category_347="主体型",
        measures=[{"name": "company_count", "col": "company_id", "agg": "count", "title": "分公司数量"}],
        dimensions=[
            {"name": "company_id", "col": "company_id", "type": "string", "title": "分公司ID"},
            {"name": "company_code", "col": "company_code", "type": "string", "title": "分公司编码"},
            {"name": "company_name", "col": "company_name", "type": "string", "title": "分公司名称"},
        ],
    )
    output.print("OK CompanyCube")

    s.register_cube(
        name="EmployerCube",
        table="dim_employer",
        title="发包人Cube",
        category_347="主体型",
        measures=[{"name": "employer_count", "col": "employer_id", "agg": "count", "title": "发包人数量"}],
        dimensions=[
            {"name": "employer_id", "col": "employer_id", "type": "string", "title": "发包人ID"},
            {"name": "employer_code", "col": "employer_code", "type": "string", "title": "发包人编号"},
            {"name": "employer_name", "col": "employer_name", "type": "string", "title": "发包人名称"},
            {"name": "credit_code", "col": "credit_code", "type": "string", "title": "统一社会信用代码"},
            {"name": "industry", "col": "industry", "type": "string", "title": "所属行业"},
        ],
    )
    output.print("OK EmployerCube")

    s.register_cube(
        name="ContractorCube",
        table="dim_contractor",
        title="总承包人Cube",
        category_347="主体型",
        measures=[{"name": "contractor_count", "col": "contractor_id", "agg": "count", "title": "总承包人数量"}],
        dimensions=[
            {"name": "contractor_id", "col": "contractor_id", "type": "string", "title": "总承包人ID"},
            {"name": "contractor_code", "col": "contractor_code", "type": "string", "title": "总承包人编号"},
            {"name": "contractor_name", "col": "contractor_name", "type": "string", "title": "总承包人名称"},
            {"name": "qualification_level", "col": "qualification_level", "type": "string", "title": "资质等级"},
        ],
    )
    output.print("OK ContractorCube")

    s.register_cube(
        name="SupplierCube",
        table="dim_supplier",
        title="供应商Cube",
        category_347="主体型",
        measures=[{"name": "supplier_count", "col": "supplier_id", "agg": "count", "title": "供应商数量"}],
        dimensions=[
            {"name": "supplier_id", "col": "supplier_id", "type": "string", "title": "供应商ID"},
            {"name": "supplier_code", "col": "supplier_code", "type": "string", "title": "供应商编码"},
            {"name": "supplier_name", "col": "supplier_name", "type": "string", "title": "供应商名称"},
            {"name": "supplier_type", "col": "supplier_type", "type": "string", "title": "供应商类型"},
            {"name": "company_id", "col": "company_id", "type": "string", "title": "分公司ID"},
        ],
    )
    output.print("OK SupplierCube")

    s.register_cube(
        name="SubcontractorCube",
        table="dim_subcontractor",
        title="分包商Cube",
        category_347="主体型",
        measures=[{"name": "subcontractor_count", "col": "subcontractor_id", "agg": "count", "title": "分包商数量"}],
        dimensions=[
            {"name": "subcontractor_id", "col": "subcontractor_id", "type": "string", "title": "分包商ID"},
            {"name": "subcontractor_code", "col": "subcontractor_code", "type": "string", "title": "分包商编号"},
            {"name": "subcontractor_name", "col": "subcontractor_name", "type": "string", "title": "分包商名称"},
            {"name": "subcontract_type", "col": "subcontract_type", "type": "string", "title": "分包类型"},
        ],
    )
    output.print("OK SubcontractorCube")

    s.register_cube(
        name="ProjectDimCube",
        table="dim_project",
        title="项目维Cube",
        category_347="主体型",
        measures=[
            {"name": "project_count", "col": "project_id", "agg": "count", "title": "项目数量"},
            {"name": "building_area_total", "col": "building_area", "agg": "sum", "title": "建筑面积合计"},
            {"name": "contract_amount_total", "col": "contract_amount", "agg": "sum", "title": "合同金额合计"},
        ],
        dimensions=[
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "project_code", "col": "project_code", "type": "string", "title": "项目编码"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
            {"name": "company_id", "col": "company_id", "type": "string", "title": "分公司ID"},
            {"name": "employer_id", "col": "employer_id", "type": "string", "title": "发包人ID"},
            {"name": "section_id", "col": "section_id", "type": "string", "title": "标段ID"},
            {"name": "section_name", "col": "section_name", "type": "string", "title": "标段名称"},
            {"name": "project_status", "col": "project_status", "type": "string", "title": "项目状态"},
        ],
    )
    output.print("OK ProjectDimCube")

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
            {"name": "management_fee_rate_avg", "col": "management_fee_rate", "agg": "avg", "title": "管理费率均值"},
        ],
        dimensions=[
            {"name": "cost_id", "col": "cost_id", "type": "string", "title": "成本记录ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "cost_code", "col": "cost_code", "type": "string", "title": "成本编码"},
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
            {"name": "contract_amount_total", "col": "contract_amount", "agg": "sum", "title": "合同金额"},
            {"name": "payment_count", "col": "payment_id", "agg": "count", "title": "付款记录数"},
        ],
        dimensions=[
            {"name": "payment_id", "col": "payment_id", "type": "string", "title": "付款记录ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "contract_id", "col": "contract_id", "type": "string", "title": "合同ID"},
            {"name": "contract_code", "col": "contract_code", "type": "string", "title": "合同编码"},
            {"name": "contract_name", "col": "contract_name", "type": "string", "title": "合同名称"},
            {"name": "supplier_id", "col": "supplier_id", "type": "string", "title": "供应商ID"},
            {"name": "supplier_name", "col": "supplier_name", "type": "string", "title": "供应商名称"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "payment_ratio", "col": "payment_ratio", "type": "float", "title": "付款比例"},
            {"name": "tax_rate", "col": "tax_rate", "type": "float", "title": "税率"},
            {"name": "settlement_status", "col": "settlement_status", "type": "string", "title": "结算状态"},
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
        name="ReceiptCube",
        table="fact_receipt",
        title="收款Cube",
        category_347="流程型",
        measures=[
            {"name": "receipt_amount_total", "col": "receipt_amount", "agg": "sum", "title": "收款金额"},
            {"name": "receipt_count", "col": "receipt_id", "agg": "count", "title": "收款记录数"},
            {"name": "overdue_days_avg", "col": "overdue_days", "agg": "avg", "title": "平均逾期天数"},
        ],
        dimensions=[
            {"name": "receipt_id", "col": "receipt_id", "type": "string", "title": "收款记录ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "contract_id", "col": "contract_id", "type": "string", "title": "合同ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "receipt_type", "col": "receipt_type", "type": "string", "title": "收款类型"},
            {"name": "receipt_method", "col": "receipt_method", "type": "string", "title": "收款方式"},
        ],
    )
    output.print("OK ReceiptCube")

    s.register_cube(
        name="SettlementCube",
        table="fact_settlement",
        title="结算Cube",
        category_347="流程型",
        measures=[
            {"name": "settlement_amount_total", "col": "settlement_amount", "agg": "sum", "title": "结算金额"},
            {"name": "review_deduction_total", "col": "review_deduction_amount", "agg": "sum", "title": "审减金额"},
            {"name": "settlement_count", "col": "settlement_id", "agg": "count", "title": "结算记录数"},
        ],
        dimensions=[
            {"name": "settlement_id", "col": "settlement_id", "type": "string", "title": "结算记录ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "audit_status", "col": "audit_status", "type": "string", "title": "审核状态"},
            {"name": "three_estimate_comparison", "col": "three_estimate_comparison", "type": "string", "title": "三算对比"},
        ],
    )
    output.print("OK SettlementCube")

    s.register_cube(
        name="BondCube",
        table="fact_bond",
        title="保证金Cube",
        category_347="流程型",
        measures=[
            {"name": "bond_amount_total", "col": "bond_amount", "agg": "sum", "title": "保证金金额"},
            {"name": "returned_amount_total", "col": "returned_amount", "agg": "sum", "title": "已退还金额"},
            {"name": "unreturned_amount_total", "col": "unreturned_amount", "agg": "sum", "title": "未退还金额"},
            {"name": "forfeit_amount_total", "col": "forfeit_amount", "agg": "sum", "title": "没收金额"},
            {"name": "bond_count", "col": "bond_id", "agg": "count", "title": "保证金记录数"},
        ],
        dimensions=[
            {"name": "bond_id", "col": "bond_id", "type": "string", "title": "保证金记录ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "contract_id", "col": "contract_id", "type": "string", "title": "合同ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "bond_type", "col": "bond_type", "type": "string", "title": "保证金类型"},
            {"name": "forfeit_status", "col": "forfeit_status", "type": "string", "title": "没收状态"},
        ],
    )
    output.print("OK BondCube")

    s.register_cube(
        name="PenaltyCube",
        table="fact_penalty",
        title="罚款Cube",
        category_347="流程型",
        measures=[
            {"name": "penalty_amount_total", "col": "penalty_amount", "agg": "sum", "title": "罚款金额"},
            {"name": "penalty_count", "col": "penalty_id", "agg": "count", "title": "罚款记录数"},
        ],
        dimensions=[
            {"name": "penalty_id", "col": "penalty_id", "type": "string", "title": "罚款记录ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "penalty_type", "col": "penalty_type", "type": "string", "title": "罚款类型"},
            {"name": "payment_status", "col": "payment_status", "type": "string", "title": "缴纳状态"},
        ],
    )
    output.print("OK PenaltyCube")

    s.register_cube(
        name="CompensationCube",
        table="fact_compensation",
        title="赔偿Cube",
        category_347="流程型",
        measures=[
            {"name": "compensation_amount_total", "col": "compensation_amount", "agg": "sum", "title": "赔偿金额"},
            {"name": "compensation_count", "col": "compensation_id", "agg": "count", "title": "赔偿记录数"},
        ],
        dimensions=[
            {"name": "compensation_id", "col": "compensation_id", "type": "string", "title": "赔偿记录ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "compensation_type", "col": "compensation_type", "type": "string", "title": "赔偿类型"},
            {"name": "payment_status", "col": "payment_status", "type": "string", "title": "支付状态"},
        ],
    )
    output.print("OK CompensationCube")

    s.register_cube(
        name="InsuranceCube",
        table="fact_insurance",
        title="工程保险Cube",
        category_347="流程型",
        measures=[
            {"name": "insurance_amount_total", "col": "insurance_amount", "agg": "sum", "title": "保险金额"},
            {"name": "premium_amount_total", "col": "premium_amount", "agg": "sum", "title": "保费金额"},
            {"name": "insurance_count", "col": "insurance_id", "agg": "count", "title": "保险记录数"},
        ],
        dimensions=[
            {"name": "insurance_id", "col": "insurance_id", "type": "string", "title": "保险记录ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "insurance_type", "col": "insurance_type", "type": "string", "title": "保险类型"},
            {"name": "claim_status", "col": "claim_status", "type": "string", "title": "理赔状态"},
        ],
    )
    output.print("OK InsuranceCube")

    s.register_cube(
        name="EquipmentCube",
        table="fact_equipment",
        title="机械设备Cube",
        category_347="流程型",
        measures=[
            {"name": "original_value_total", "col": "original_value", "agg": "sum", "title": "原值合计"},
            {"name": "unit_price_avg", "col": "unit_price", "agg": "avg", "title": "台班单价均值"},
            {"name": "equipment_count", "col": "equipment_id", "agg": "count", "title": "设备记录数"},
        ],
        dimensions=[
            {"name": "equipment_id", "col": "equipment_id", "type": "string", "title": "设备记录ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
            {"name": "equipment_code", "col": "equipment_code", "type": "string", "title": "设备编号"},
            {"name": "equipment_name", "col": "equipment_name", "type": "string", "title": "设备名称"},
            {"name": "equipment_status", "col": "equipment_status", "type": "string", "title": "设备状态"},
        ],
    )
    output.print("OK EquipmentCube")

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
            {"name": "employer_id", "col": "employer_id", "type": "string", "title": "发包人ID"},
            {"name": "employer_name", "col": "employer_name", "type": "string", "title": "发包人名称"},
            {"name": "section_id", "col": "section_id", "type": "string", "title": "标段ID"},
            {"name": "section_name", "col": "section_name", "type": "string", "title": "标段名称"},
            {"name": "project_status", "col": "project_status", "type": "string", "title": "项目状态"},
            {"name": "report_period", "col": "report_period", "type": "string", "title": "报告期间"},
        ],
    )
    output.print("OK ProjectCube")

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

    # 4b. 派生度量（030-派生属性定义 + V3 §5）
    output.print("\n[4b/8] 配置派生度量...")

    s.upsert_derived_measures("ProjectOutputCube", [
        {"name": "confirmed_ratio", "title": "确权率", "expression": "if(ProjectOutputCube.total_output_total > 0, ProjectOutputCube.confirmed_output_total / ProjectOutputCube.total_output_total, 0)", "description": "已确认产值/总产值"},
        {"name": "unconfirmed_ratio", "title": "待确比例", "expression": "if(ProjectOutputCube.total_output_total > 0, ProjectOutputCube.unconfirmed_output_total / ProjectOutputCube.total_output_total, 0)", "description": "待确认产值/总产值"},
        {"name": "output_current", "title": "本年累计产值", "expression": "ProjectOutputCube.output_current_confirmed_total + ProjectOutputCube.output_current_unconfirmed_total - ProjectOutputCube.output_last_year_confirmed_total - ProjectOutputCube.output_last_year_unconfirmed_total", "description": "本年累计产值"},
        {"name": "output_growth", "title": "同比增长率", "expression": "if((ProjectOutputCube.output_last_year_confirmed_total + ProjectOutputCube.output_last_year_unconfirmed_total) > 0, (ProjectOutputCube.output_current_confirmed_total + ProjectOutputCube.output_current_unconfirmed_total) / (ProjectOutputCube.output_last_year_confirmed_total + ProjectOutputCube.output_last_year_unconfirmed_total) - 1, 0)", "description": "产值同比增长"},
    ])
    output.print("OK ProjectOutputCube 派生度量")

    s.upsert_derived_measures("ProjectCostCube", [
        {"name": "cost_total_acc", "title": "累计总成本", "expression": "ProjectCostCube.cost_confirmed_acc_total + ProjectCostCube.cost_unconfirmed_acc_total", "description": "累计已确+待确成本"},
        {"name": "cost_current", "title": "本月总成本", "expression": "ProjectCostCube.cost_confirmed_cmonth_total + ProjectCostCube.cost_unconfirmed_cmonth_total", "description": "本月已确+待确成本"},
        {"name": "labor_ratio", "title": "人工费占比", "expression": "if(ProjectCostCube.cost_confirmed_acc_total > 0, ProjectCostCube.labor_cost_total / ProjectCostCube.cost_confirmed_acc_total, 0)", "description": "人工费/累计已确成本"},
        {"name": "material_ratio", "title": "材料费占比", "expression": "if(ProjectCostCube.cost_confirmed_acc_total > 0, ProjectCostCube.material_cost_total / ProjectCostCube.cost_confirmed_acc_total, 0)", "description": "材料费/累计已确成本"},
        {"name": "equipment_ratio", "title": "设备费占比", "expression": "if(ProjectCostCube.cost_confirmed_acc_total > 0, ProjectCostCube.equipment_cost_total / ProjectCostCube.cost_confirmed_acc_total, 0)", "description": "设备费/累计已确成本"},
        {"name": "cost_variance", "title": "成本偏差", "expression": "ProjectCostCube.cost_confirmed_acc_total - ProjectCostCube.target_cost_total", "description": "累计已确成本-目标成本"},
        {"name": "cost_variance_ratio", "title": "成本偏差率", "expression": "if(ProjectCostCube.target_cost_total > 0, (ProjectCostCube.cost_confirmed_acc_total - ProjectCostCube.target_cost_total) / ProjectCostCube.target_cost_total, 0)", "description": "成本偏差/目标成本"},
        {"name": "cost_deviation_rate", "title": "成本偏差率(ER005)", "expression": "if(ProjectCostCube.target_cost_total > 0, (ProjectCostCube.cost_confirmed_acc_total - ProjectCostCube.target_cost_total) / ProjectCostCube.target_cost_total, 0)", "description": "实际成本相对目标成本偏差"},
        {"name": "l1_cost_amount", "title": "L1主控费用", "expression": "sumIf(cost_confirmed_acc, cost_level = 'L1')", "description": "三级成本 L1 汇总"},
        {"name": "l2_cost_amount", "title": "L2分项费用", "expression": "sumIf(cost_confirmed_acc, cost_level = 'L2')", "description": "三级成本 L2 汇总"},
        {"name": "l3_cost_amount", "title": "L3明细费用", "expression": "sumIf(cost_confirmed_acc, cost_level = 'L3')", "description": "三级成本 L3 汇总"},
    ])
    output.print("OK ProjectCostCube 派生度量")

    s.upsert_derived_measures("ProjectPaymentCube", [
        {"name": "unpaid_amount", "title": "未付款金额", "expression": "ProjectPaymentCube.payable_confirmed_total - ProjectPaymentCube.paid_amount_total", "description": "已确应付款-已付款"},
        {"name": "unpaid_ratio", "title": "未付款比例", "expression": "if(ProjectPaymentCube.payable_confirmed_total > 0, (ProjectPaymentCube.payable_confirmed_total - ProjectPaymentCube.paid_amount_total) / ProjectPaymentCube.payable_confirmed_total, 0)", "description": "未付款/已确应付款"},
        {"name": "payment_rate", "title": "付款率", "expression": "if(ProjectPaymentCube.payable_confirmed_total > 0, ProjectPaymentCube.paid_amount_total / ProjectPaymentCube.payable_confirmed_total, 0)", "description": "已付款/已确应付款"},
        {"name": "payment_progress", "title": "付款进度", "expression": "if(ProjectPaymentCube.contract_amount_total > 0, ProjectPaymentCube.paid_amount_total / ProjectPaymentCube.contract_amount_total, 0)", "description": "已付款/合同金额"},
        {"name": "labor_payment_ratio", "title": "人工费占应付款", "expression": "if(ProjectPaymentCube.payable_confirmed_total > 0, ProjectPaymentCube.labor_payable_total / ProjectPaymentCube.payable_confirmed_total, 0)", "description": "人工费应付款/已确应付款"},
    ])
    output.print("OK ProjectPaymentCube 派生度量")

    s.upsert_derived_measures("ProjectBalanceCube", [
        {"name": "balance_gap", "title": "收支差额", "expression": "ProjectBalanceCube.project_amount_total - ProjectBalanceCube.company_amount_total", "description": "项目层面-公司层面"},
        {"name": "income_ratio", "title": "收入占比", "expression": "if(ProjectBalanceCube.total_amount_total > 0, ProjectBalanceCube.project_amount_total / ProjectBalanceCube.total_amount_total, 0)", "description": "项目金额/合计"},
        {"name": "expense_ratio", "title": "支出占比", "expression": "if(ProjectBalanceCube.total_amount_total > 0, ProjectBalanceCube.company_amount_total / ProjectBalanceCube.total_amount_total, 0)", "description": "公司金额/合计"},
    ])
    output.print("OK ProjectBalanceCube 派生度量")

    s.upsert_derived_measures("ProjectIndicatorCube", [
        {"name": "variance_value", "title": "指标偏差值", "expression": "ProjectIndicatorCube.indicator_value_avg - ProjectIndicatorCube.target_value_avg", "description": "指标值-目标值"},
        {"name": "variance_ratio", "title": "指标偏差率", "expression": "if(ProjectIndicatorCube.target_value_avg > 0, (ProjectIndicatorCube.indicator_value_avg - ProjectIndicatorCube.target_value_avg) / ProjectIndicatorCube.target_value_avg, 0)", "description": "偏差值/目标值"},
        {"name": "is_warning", "title": "是否预警", "expression": "if(ProjectIndicatorCube.target_value_avg > 0, abs((ProjectIndicatorCube.indicator_value_avg - ProjectIndicatorCube.target_value_avg) / ProjectIndicatorCube.target_value_avg) > 0.10, 0)", "description": "偏差率>10%"},
    ])
    output.print("OK ProjectIndicatorCube 派生度量")

    s.upsert_derived_measures("ProjectRiskCube", [
        {"name": "risk_score", "title": "风险综合得分", "expression": "ProjectRiskCube.risk_value_sum", "description": "风险值加权合计"},
        {"name": "green_risk_count", "title": "绿色预警数量", "expression": "countIf(risk_id, warning_level = '绿')", "description": "三色预警-绿"},
        {"name": "yellow_risk_count", "title": "黄色预警数量", "expression": "countIf(risk_id, warning_level = '黄')", "description": "三色预警-黄"},
        {"name": "red_risk_count", "title": "红色预警数量", "expression": "countIf(risk_id, warning_level = '红')", "description": "三色预警-红"},
        {"name": "red_risk_immediate_report", "title": "红色预警立即上报", "expression": "if(countIf(risk_id, warning_level = '红') > 0, 1, 0)", "description": "存在红色预警"},
    ])
    output.print("OK ProjectRiskCube 派生度量")

    s.upsert_derived_measures("BondCube", [
        {"name": "unreturned_ratio", "title": "未退比例", "expression": "if(BondCube.bond_amount_total > 0, BondCube.unreturned_amount_total / BondCube.bond_amount_total, 0)", "description": "未退还/保证金"},
        {"name": "forfeit_ratio", "title": "没收比例", "expression": "if(BondCube.bond_amount_total > 0, BondCube.forfeit_amount_total / BondCube.bond_amount_total, 0)", "description": "没收/保证金"},
        {"name": "return_progress", "title": "退还进度", "expression": "if(BondCube.bond_amount_total > 0, BondCube.returned_amount_total / BondCube.bond_amount_total, 0)", "description": "已退还/保证金"},
    ])
    output.print("OK BondCube 派生度量")

    s.upsert_derived_measures("ProjectCube", [
        {"name": "profit_rate", "title": "毛利率", "expression": "if(ProjectCube.total_output_total > 0, (ProjectCube.total_output_total - ProjectCube.cost_confirmed_acc_total) / ProjectCube.total_output_total, 0)", "description": "(产值-成本)/产值"},
        {"name": "cost_ratio", "title": "成本率", "expression": "if(ProjectCube.total_output_total > 0, ProjectCube.cost_confirmed_acc_total / ProjectCube.total_output_total, 0)", "description": "成本/产值"},
        {"name": "confirmed_ratio", "title": "产值确认率", "expression": "if(ProjectCube.total_output_total > 0, ProjectCube.confirmed_output_total / ProjectCube.total_output_total, 0)", "description": "已确认产值/总产值"},
        {"name": "cost_rigidity", "title": "成本刚性度", "expression": "if(ProjectCube.cost_confirmed_acc_total > 0, ProjectCube.labor_cost_total / ProjectCube.cost_confirmed_acc_total, 0)", "description": "人工费/累计已确成本"},
        {"name": "collection_rate", "title": "回款率", "expression": "if(ProjectCube.confirmed_output_total > 0, ProjectCube.received_amount_total / ProjectCube.confirmed_output_total, 0)", "description": "收款/已确认产值"},
        {"name": "payment_rate", "title": "付款率", "expression": "if(ProjectCube.payable_confirmed_total > 0, ProjectCube.paid_amount_total / ProjectCube.payable_confirmed_total, 0)", "description": "已付款/已确应付款"},
        {"name": "cash_balance", "title": "资金结余", "expression": "ProjectCube.received_amount_total - ProjectCube.paid_amount_total", "description": "收款-付款"},
        {"name": "health_score", "title": "项目健康度", "expression": "(if(ProjectCube.total_output_total > 0, (ProjectCube.total_output_total - ProjectCube.cost_confirmed_acc_total) / ProjectCube.total_output_total, 0) / 0.20 + if(ProjectCube.confirmed_output_total > 0, ProjectCube.received_amount_total / ProjectCube.confirmed_output_total, 0) + if(ProjectCube.total_output_total > 0, ProjectCube.confirmed_output_total / ProjectCube.total_output_total, 0)) / 3", "description": "030健康度公式"},
    ])
    output.print("OK ProjectCube 派生度量")

    s.upsert_derived_measures("CostOutputComparisonCube", [
        {"name": "profit_rate", "title": "毛利率", "expression": "if(CostOutputComparisonCube.total_output_total > 0, (CostOutputComparisonCube.total_output_total - CostOutputComparisonCube.cost_confirmed_acc_total) / CostOutputComparisonCube.total_output_total, 0)", "description": "成本产值对比毛利率"},
        {"name": "cost_ratio", "title": "成本率", "expression": "if(CostOutputComparisonCube.total_output_total > 0, CostOutputComparisonCube.cost_confirmed_acc_total / CostOutputComparisonCube.total_output_total, 0)", "description": "成本/产值"},
        {"name": "confirmed_ratio", "title": "产值确认率", "expression": "if(CostOutputComparisonCube.total_output_total > 0, CostOutputComparisonCube.confirmed_output_total / CostOutputComparisonCube.total_output_total, 0)", "description": "已确认产值/总产值"},
        {"name": "cost_deviation_rate", "title": "成本偏差率", "expression": "if(CostOutputComparisonCube.target_cost_total > 0, (CostOutputComparisonCube.cost_confirmed_acc_total - CostOutputComparisonCube.target_cost_total) / CostOutputComparisonCube.target_cost_total, 0)", "description": "实际成本相对目标"},
    ])
    output.print("OK CostOutputComparisonCube 派生度量")

    # 5. 定义对象类型（20 + CostManagementAnalysis）
    output.print("\n[5/8] 定义对象类型...")
    object_types = [
        ("Project", "项目", "施工项目主数据（含标段属性）", "主数据", "ProjectCube"),
        ("Company", "分公司", "分公司/子公司主数据", "主数据", "CompanyCube"),
        ("Employer", "发包人", "发包人/业主主数据", "主数据", "EmployerCube"),
        ("Contractor", "总承包人", "总承包人/施工单位", "主数据", "ContractorCube"),
        ("Subcontractor", "分包商", "分包商主数据", "主数据", "SubcontractorCube"),
        ("Supplier", "供应商", "供应商主数据", "主数据", "ProjectPaymentCube"),
        ("Contract", "合同", "分包/采购/劳务合同", "主数据", "ProjectPaymentCube"),
        ("ProjectOutput", "项目产值", "月度产值确权事务", "事务", "ProjectOutputCube"),
        ("ProjectCost", "项目成本", "月度成本汇总事务", "事务", "ProjectCostCube"),
        ("ProjectPayment", "项目付款", "月度付款事务", "事务", "ProjectPaymentCube"),
        ("ProjectBalance", "项目收支", "收支科目汇总事务", "事务", "ProjectBalanceCube"),
        ("ProjectIndicator", "项目指标", "核心商务指标事务", "事务", "ProjectIndicatorCube"),
        ("ProjectRisk", "项目风险", "风险清单预警事务", "事务", "ProjectRiskCube"),
        ("Receipt", "收款", "项目收款记录", "事务", "ReceiptCube"),
        ("Settlement", "结算", "项目结算记录", "事务", "SettlementCube"),
        ("Bond", "保证金", "投标/履约/质量保证金", "事务", "BondCube"),
        ("Penalty", "罚款", "违约/违规/质量安全罚款", "事务", "PenaltyCube"),
        ("Compensation", "赔偿", "合同/侵权/工伤赔偿", "事务", "CompensationCube"),
        ("Insurance", "工程保险", "工程险/意外险/责任险", "事务", "InsuranceCube"),
        ("Equipment", "机械设备", "项目设备台账", "事务", "EquipmentCube"),
        ("CostManagementAnalysis", "商务成本分析", "成本产值对比分析", "分析", "CostOutputComparisonCube"),
    ]
    for code, name, desc, cat, cube in object_types:
        s.onto.define_object_type(code=code, name=name, description=desc, category_347=cat)
        s.onto.bind_source(code, "dazi_cube", config={"cube": cube})
        output.print(f"OK {code}")

    # 6. 定义对象属性
    output.print("\n[6/8] 定义对象属性...")
    properties = [
        ("Project", "id", "项目ID", "dimension", "ProjectCube.project_id"),
        ("Project", "code", "项目编码", "dimension", "ProjectCube.project_code"),
        ("Project", "name", "项目名称", "dimension", "ProjectCube.project_name"),
        ("Project", "companyId", "分公司ID", "dimension", "ProjectCube.company_id"),
        ("Project", "companyName", "分公司名称", "dimension", "ProjectCube.company_name"),
        ("Project", "employerId", "发包人ID", "dimension", "ProjectCube.employer_id"),
        ("Project", "employerName", "发包人名称", "dimension", "ProjectCube.employer_name"),
        ("Project", "sectionId", "标段ID", "dimension", "ProjectCube.section_id"),
        ("Project", "sectionName", "标段名称", "dimension", "ProjectCube.section_name"),
        ("Project", "projectStatus", "项目状态", "dimension", "ProjectCube.project_status"),
        ("Project", "buildingArea", "建筑面积", "measure", "ProjectCube.building_area"),
        ("Project", "contractAmount", "合同金额", "measure", "ProjectCube.contract_amount"),
        ("Project", "reportPeriod", "报告期间", "dimension", "ProjectCube.report_period"),
        ("Project", "profitRate", "毛利率", "measure", "ProjectCube.profit_rate"),
        ("Project", "costRatio", "成本率", "measure", "ProjectCube.cost_ratio"),
        ("Project", "confirmedRatio", "产值确认率", "measure", "ProjectCube.confirmed_ratio"),
        ("Project", "costRigidity", "成本刚性度", "measure", "ProjectCube.cost_rigidity"),
        ("Project", "collectionRate", "回款率", "measure", "ProjectCube.collection_rate"),
        ("Project", "paymentRate", "付款率", "measure", "ProjectCube.payment_rate"),
        ("Project", "cashBalance", "资金结余", "measure", "ProjectCube.cash_balance"),
        ("Project", "riskScore", "风险综合得分", "measure", "ProjectCube.risk_score"),
        ("Project", "healthScore", "项目健康度", "measure", "ProjectCube.health_score"),
        ("Company", "id", "分公司ID", "dimension", "CompanyCube.company_id"),
        ("Company", "code", "分公司编码", "dimension", "CompanyCube.company_code"),
        ("Company", "name", "分公司名称", "dimension", "CompanyCube.company_name"),
        ("Employer", "id", "发包人ID", "dimension", "EmployerCube.employer_id"),
        ("Employer", "code", "发包人编号", "dimension", "EmployerCube.employer_code"),
        ("Employer", "name", "发包人名称", "dimension", "EmployerCube.employer_name"),
        ("Employer", "creditCode", "统一社会信用代码", "dimension", "EmployerCube.credit_code"),
        ("Employer", "industry", "所属行业", "dimension", "EmployerCube.industry"),
        ("Contractor", "id", "总承包人ID", "dimension", "ContractorCube.contractor_id"),
        ("Contractor", "code", "总承包人编号", "dimension", "ContractorCube.contractor_code"),
        ("Contractor", "name", "总承包人名称", "dimension", "ContractorCube.contractor_name"),
        ("Contractor", "qualificationLevel", "资质等级", "dimension", "ContractorCube.qualification_level"),
        ("Subcontractor", "id", "分包商ID", "dimension", "SubcontractorCube.subcontractor_id"),
        ("Subcontractor", "code", "分包商编号", "dimension", "SubcontractorCube.subcontractor_code"),
        ("Subcontractor", "name", "分包商名称", "dimension", "SubcontractorCube.subcontractor_name"),
        ("Subcontractor", "subcontractType", "分包类型", "dimension", "SubcontractorCube.subcontract_type"),
        ("Supplier", "id", "供应商ID", "dimension", "ProjectPaymentCube.supplier_id"),
        ("Supplier", "name", "供应商名称", "dimension", "ProjectPaymentCube.supplier_name"),
        ("Contract", "id", "合同ID", "dimension", "ProjectPaymentCube.contract_id"),
        ("Contract", "projectId", "项目ID", "dimension", "ProjectPaymentCube.project_id"),
        ("Contract", "contractCode", "合同编码", "dimension", "ProjectPaymentCube.contract_code"),
        ("Contract", "contractName", "合同名称", "dimension", "ProjectPaymentCube.contract_name"),
        ("Contract", "contractAmount", "合同金额", "measure", "ProjectPaymentCube.contract_amount_total"),
        ("Contract", "paymentRatio", "付款比例", "dimension", "ProjectPaymentCube.payment_ratio"),
        ("Contract", "taxRate", "税率", "dimension", "ProjectPaymentCube.tax_rate"),
        ("Contract", "settlementStatus", "结算状态", "dimension", "ProjectPaymentCube.settlement_status"),
        ("Contract", "supplierName", "供应商名称", "dimension", "ProjectPaymentCube.supplier_name"),
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
        ("ProjectCost", "reportPeriod", "报告期间", "dimension", "ProjectCostCube.report_period"),
        ("ProjectCost", "costLevel", "成本层级", "dimension", "ProjectCostCube.cost_level"),
        ("ProjectCost", "costCode", "成本编码", "dimension", "ProjectCostCube.cost_code"),
        ("ProjectCost", "costConfirmedAcc", "累计已确成本", "measure", "ProjectCostCube.cost_confirmed_acc_total"),
        ("ProjectCost", "costUnconfirmedAcc", "累计待确成本", "measure", "ProjectCostCube.cost_unconfirmed_acc_total"),
        ("ProjectCost", "laborCostAcc", "累计人工费", "measure", "ProjectCostCube.labor_cost_total"),
        ("ProjectCost", "materialCostAcc", "累计材料费", "measure", "ProjectCostCube.material_cost_total"),
        ("ProjectCost", "equipmentCostAcc", "累计设备费", "measure", "ProjectCostCube.equipment_cost_total"),
        ("ProjectCost", "targetCost", "目标成本", "measure", "ProjectCostCube.target_cost_total"),
        ("ProjectCost", "managementFeeRate", "管理费率", "measure", "ProjectCostCube.management_fee_rate_avg"),
        ("ProjectCost", "costTotalAcc", "累计总成本", "measure", "ProjectCostCube.cost_total_acc"),
        ("ProjectCost", "costVariance", "成本偏差", "measure", "ProjectCostCube.cost_variance"),
        ("ProjectCost", "costVarianceRatio", "成本偏差率", "measure", "ProjectCostCube.cost_variance_ratio"),
        ("ProjectCost", "l1CostAmount", "L1主控费用", "measure", "ProjectCostCube.l1_cost_amount"),
        ("ProjectCost", "l2CostAmount", "L2分项费用", "measure", "ProjectCostCube.l2_cost_amount"),
        ("ProjectCost", "l3CostAmount", "L3明细费用", "measure", "ProjectCostCube.l3_cost_amount"),
        ("ProjectPayment", "id", "记录ID", "dimension", "ProjectPaymentCube.payment_id"),
        ("ProjectPayment", "projectId", "项目ID", "dimension", "ProjectPaymentCube.project_id"),
        ("ProjectPayment", "contractId", "合同ID", "dimension", "ProjectPaymentCube.contract_id"),
        ("ProjectPayment", "payableConfirmed", "已确应付款", "measure", "ProjectPaymentCube.payable_confirmed_total"),
        ("ProjectPayment", "paidAmount", "已付款", "measure", "ProjectPaymentCube.paid_amount_total"),
        ("ProjectPayment", "unpaidAmount", "未付款", "measure", "ProjectPaymentCube.unpaid_amount"),
        ("ProjectPayment", "paymentRate", "付款率", "measure", "ProjectPaymentCube.payment_rate"),
        ("ProjectBalance", "projectAmount", "项目层面金额", "measure", "ProjectBalanceCube.project_amount_total"),
        ("ProjectBalance", "companyAmount", "公司层面金额", "measure", "ProjectBalanceCube.company_amount_total"),
        ("ProjectBalance", "balanceAmount", "收支差额", "measure", "ProjectBalanceCube.balance_gap"),
        ("ProjectIndicator", "indicatorCode", "指标编码", "dimension", "ProjectIndicatorCube.indicator_code"),
        ("ProjectIndicator", "indicatorName", "指标名称", "dimension", "ProjectIndicatorCube.indicator_name"),
        ("ProjectIndicator", "indicatorValue", "指标值", "measure", "ProjectIndicatorCube.indicator_value_sum"),
        ("ProjectIndicator", "targetValue", "目标值", "measure", "ProjectIndicatorCube.target_value_avg"),
        ("ProjectIndicator", "varianceValue", "指标偏差值", "measure", "ProjectIndicatorCube.variance_value"),
        ("ProjectIndicator", "varianceRatio", "指标偏差率", "measure", "ProjectIndicatorCube.variance_ratio"),
        ("ProjectIndicator", "isWarning", "是否预警", "measure", "ProjectIndicatorCube.is_warning"),
        ("ProjectRisk", "id", "风险ID", "dimension", "ProjectRiskCube.risk_id"),
        ("ProjectRisk", "riskType", "风险类型", "dimension", "ProjectRiskCube.risk_type"),
        ("ProjectRisk", "riskName", "风险名称", "dimension", "ProjectRiskCube.risk_name"),
        ("ProjectRisk", "warningLevel", "预警级别", "dimension", "ProjectRiskCube.warning_level"),
        ("ProjectRisk", "riskValue", "风险值", "measure", "ProjectRiskCube.risk_value_sum"),
        ("ProjectRisk", "riskScore", "风险综合得分", "measure", "ProjectRiskCube.risk_score"),
        ("ProjectRisk", "greenRiskCount", "绿色预警数量", "measure", "ProjectRiskCube.green_risk_count"),
        ("ProjectRisk", "yellowRiskCount", "黄色预警数量", "measure", "ProjectRiskCube.yellow_risk_count"),
        ("ProjectRisk", "redRiskCount", "红色预警数量", "measure", "ProjectRiskCube.red_risk_count"),
        ("Receipt", "id", "收款ID", "dimension", "ReceiptCube.receipt_id"),
        ("Receipt", "projectId", "项目ID", "dimension", "ReceiptCube.project_id"),
        ("Receipt", "receiptAmount", "收款金额", "measure", "ReceiptCube.receipt_amount_total"),
        ("Receipt", "receiptType", "收款类型", "dimension", "ReceiptCube.receipt_type"),
        ("Receipt", "overdueDays", "逾期天数", "measure", "ReceiptCube.overdue_days_avg"),
        ("Settlement", "id", "结算ID", "dimension", "SettlementCube.settlement_id"),
        ("Settlement", "projectId", "项目ID", "dimension", "SettlementCube.project_id"),
        ("Settlement", "settlementAmount", "结算金额", "measure", "SettlementCube.settlement_amount_total"),
        ("Settlement", "auditStatus", "审核状态", "dimension", "SettlementCube.audit_status"),
        ("Settlement", "threeEstimateComparison", "三算对比", "dimension", "SettlementCube.three_estimate_comparison"),
        ("Bond", "id", "保证金ID", "dimension", "BondCube.bond_id"),
        ("Bond", "projectId", "项目ID", "dimension", "BondCube.project_id"),
        ("Bond", "bondType", "保证金类型", "dimension", "BondCube.bond_type"),
        ("Bond", "bondAmount", "保证金金额", "measure", "BondCube.bond_amount_total"),
        ("Bond", "unreturnedRatio", "未退比例", "measure", "BondCube.unreturned_ratio"),
        ("Bond", "forfeitRatio", "没收比例", "measure", "BondCube.forfeit_ratio"),
        ("Bond", "returnProgress", "退还进度", "measure", "BondCube.return_progress"),
        ("Penalty", "id", "罚款ID", "dimension", "PenaltyCube.penalty_id"),
        ("Penalty", "projectId", "项目ID", "dimension", "PenaltyCube.project_id"),
        ("Penalty", "penaltyType", "罚款类型", "dimension", "PenaltyCube.penalty_type"),
        ("Penalty", "penaltyAmount", "罚款金额", "measure", "PenaltyCube.penalty_amount_total"),
        ("Compensation", "id", "赔偿ID", "dimension", "CompensationCube.compensation_id"),
        ("Compensation", "projectId", "项目ID", "dimension", "CompensationCube.project_id"),
        ("Compensation", "compensationAmount", "赔偿金额", "measure", "CompensationCube.compensation_amount_total"),
        ("Insurance", "id", "保险ID", "dimension", "InsuranceCube.insurance_id"),
        ("Insurance", "projectId", "项目ID", "dimension", "InsuranceCube.project_id"),
        ("Insurance", "insuranceType", "保险类型", "dimension", "InsuranceCube.insurance_type"),
        ("Insurance", "premiumAmount", "保费金额", "measure", "InsuranceCube.premium_amount_total"),
        ("Equipment", "id", "设备ID", "dimension", "EquipmentCube.equipment_id"),
        ("Equipment", "projectId", "项目ID", "dimension", "EquipmentCube.project_id"),
        ("Equipment", "equipmentCode", "设备编号", "dimension", "EquipmentCube.equipment_code"),
        ("Equipment", "equipmentName", "设备名称", "dimension", "EquipmentCube.equipment_name"),
        ("Equipment", "equipmentStatus", "设备状态", "dimension", "EquipmentCube.equipment_status"),
    ]
    for obj, code, name, role, qn in properties:
        s.onto.define_property(obj, code, name, semantic_role=role, qualified_name=qn)
    output.print("OK 属性定义完成")

    # 7. 定义链接类型（~28 条，Section 不建对象，hasPart 不实现）
    output.print("\n[7/8] 定义链接类型...")
    link_types = [
        ("output_belongs_project", "产值归属项目", "ProjectOutput", "Project", "归属关系"),
        ("cost_belongs_project", "成本归属项目", "ProjectCost", "Project", "归属关系"),
        ("payment_belongs_project", "付款归属项目", "ProjectPayment", "Project", "归属关系"),
        ("balance_belongs_project", "收支归属项目", "ProjectBalance", "Project", "归属关系"),
        ("indicator_belongs_project", "指标归属项目", "ProjectIndicator", "Project", "归属关系"),
        ("risk_belongs_project", "风险归属项目", "ProjectRisk", "Project", "归属关系"),
        ("bond_belongs_project", "保证金归属项目", "Bond", "Project", "归属关系"),
        ("penalty_belongs_project", "罚款归属项目", "Penalty", "Project", "归属关系"),
        ("compensation_belongs_project", "赔偿归属项目", "Compensation", "Project", "归属关系"),
        ("insurance_belongs_project", "保险归属项目", "Insurance", "Project", "归属关系"),
        ("equipment_belongs_project", "设备归属项目", "Equipment", "Project", "归属关系"),
        ("receipt_belongs_project", "收款归属项目", "Receipt", "Project", "归属关系"),
        ("settlement_belongs_project", "结算归属项目", "Settlement", "Project", "归属关系"),
        ("project_belongs_company", "项目归属分公司", "Project", "Company", "归属关系"),
        ("supplier_belongs_company", "供应商归属分公司", "Supplier", "Company", "归属关系"),
        ("project_belongs_employer", "项目归属发包人", "Project", "Employer", "归属关系"),
        ("contract_belongs_project", "合同归属项目", "Contract", "Project", "归属关系"),
        ("bond_belongs_contract", "保证金归属合同", "Bond", "Contract", "归属关系"),
        ("cost_contains_contract", "成本包含合同", "ProjectCost", "Contract", "归属关系"),
        ("payment_contains_contract", "付款包含合同", "ProjectPayment", "Contract", "归属关系"),
        ("contract_signs_employer", "合同签订发包人", "Contract", "Employer", "归属关系"),
        ("contract_signs_contractor", "合同签订总承包人", "Contract", "Contractor", "归属关系"),
        ("contract_signs_subcontractor", "合同签订分包商", "Contract", "Subcontractor", "归属关系"),
        ("contract_supplies_supplier", "合同供应供应商", "Contract", "Supplier", "归属关系"),
        ("risk_affects_cost", "风险影响成本", "ProjectRisk", "ProjectCost", "归属关系"),
        ("risk_affects_project", "风险影响项目", "ProjectRisk", "Project", "归属关系"),
        ("penalty_affects_cost", "罚款影响成本", "Penalty", "ProjectCost", "归属关系"),
        ("analysis_by_project", "分析归因项目", "CostManagementAnalysis", "Project", "分析归因"),
        ("analysis_by_company", "分析归因分公司", "CostManagementAnalysis", "Company", "分析归因"),
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
    output.print("\n[8/8] 同步指标引用...")
    s.sync_metric_refs()
    output.print("OK sync_metric_refs")

    summary = {
        "ok": True,
        "space_id": space_id,
        "version": "V3.0",
        "tables": len(TABLE_REGISTRY),
        "views": len(VIEW_REGISTRY),
        "relationships": len(table_relationships),
        "cubes": 22,
        "objects": len(object_types),
        "links": len(link_types),
    }
    output.success("潘达工程商务成本本体 V3.0 初始化完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))

