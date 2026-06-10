"""潘达工程商务成本 V3 演示数据灌入 — space__panda_construction

前置：先执行 panda_cost_v3_ontology_init.py 建表；dim_date 由空间其他域提供或已存在。
幂等：fact_project_output 已有数据则跳过。

V3 表结构：6 维表（dim_project/employer/contractor/supplier/subcontractor/company）
+ 13 事实表（含 fact_bond/penalty/receipt/settlement/compensation/insurance/equipment）。

放置：项目/潘达工程-商务成本/本体/ontos/本体规划03/setup/panda_cost_v3_seed_data.py
发布：dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划03/setup/panda_cost_v3_seed_data.py --space space__panda_construction --type data
规划对照：阶段二 V3.0 物理表设计文档 + 020-本体规划文档.md
"""

import calendar
import json
import random
from datetime import datetime

_SEED_DT = datetime(2025, 1, 1, 0, 0, 0)

# 演示期间：2025-01 至 2025-06
_DEMO_MONTHS = [(2025, m) for m in range(1, 7)]


def _month_end_date_key(year, month):
    """返回报告月末 date_key（YYYYMMDD）。"""
    last_day = calendar.monthrange(year, month)[1]
    return int(f"{year}{month:02d}{last_day:02d}")


def _report_period(year, month):
    return f"{year}-{month:02d}"


def _month_end_datetime(year, month, hour=12):
    """返回月末 DateTime，用于 created_at / 业务日期字段。"""
    last_day = calendar.monthrange(year, month)[1]
    return datetime(year, month, last_day, hour, 0, 0)


def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)

    output.print("=== 潘达工程商务成本 V3 演示数据灌入 ===")

    # 幂等性检查：fact_project_output 有数据则跳过
    try:
        n = int(s.sql.query_one("SELECT count() FROM fact_project_output") or 0)
    except Exception:
        n = 0
    if n > 0:
        output.print(f"fact_project_output 已有 {n} 行，跳过灌数")
        output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "skipped": True, "rows": n}, ensure_ascii=True))
        return

    random.seed(8806)

    # ------------------------------------------------------------------ #
    # 1. 分公司维表
    # ------------------------------------------------------------------ #
    companies = [
        {"company_id": "C001", "company_code": "PDJT", "company_name": "潘达建工集团", "status": "正常", "created_at": _SEED_DT},
        {"company_id": "C002", "company_code": "PDGD", "company_name": "潘达广东分公司", "status": "正常", "created_at": _SEED_DT},
        {"company_id": "C003", "company_code": "PDBJ", "company_name": "潘达北京分公司", "status": "正常", "created_at": _SEED_DT},
        {"company_id": "C004", "company_code": "PDSH", "company_name": "潘达上海分公司", "status": "正常", "created_at": _SEED_DT},
    ]

    # ------------------------------------------------------------------ #
    # 2. 发包人维表（V3 替代 dim_owner）
    # ------------------------------------------------------------------ #
    employers = [
        {
            "employer_id": "E001", "employer_code": "GZRD", "employer_name": "广州市人民政府",
            "credit_code": "11440100000000001X", "contact_person": "王主任", "contact_phone": "020-88880001",
            "industry": "政府", "fund_source": "财政拨款", "status": "正常", "created_at": _SEED_DT,
        },
        {
            "employer_id": "E002", "employer_code": "WHJT", "employer_name": "万科集团",
            "credit_code": "91440300123456789A", "contact_person": "李总", "contact_phone": "0755-88880002",
            "industry": "房地产", "fund_source": "自筹", "status": "正常", "created_at": _SEED_DT,
        },
        {
            "employer_id": "E003", "employer_code": "HYDL", "employer_name": "华远地产",
            "credit_code": "91110000123456789B", "contact_person": "张经理", "contact_phone": "010-88880003",
            "industry": "房地产", "fund_source": "自筹", "status": "正常", "created_at": _SEED_DT,
        },
        {
            "employer_id": "E004", "employer_code": "BJWY", "employer_name": "北京伟业",
            "credit_code": "91110100123456789C", "contact_person": "赵总", "contact_phone": "010-88880004",
            "industry": "房地产", "fund_source": "自筹", "status": "正常", "created_at": _SEED_DT,
        },
        {
            "employer_id": "E005", "employer_code": "ZJRJ", "employer_name": "中建科技",
            "credit_code": "91110000987654321D", "contact_person": "刘工", "contact_phone": "010-88880005",
            "industry": "建筑", "fund_source": "自筹", "status": "正常", "created_at": _SEED_DT,
        },
    ]

    # ------------------------------------------------------------------ #
    # 3. 总承包人维表
    # ------------------------------------------------------------------ #
    contractors = [
        {
            "contractor_id": "CTR001", "contractor_code": "PDJT", "contractor_name": "潘达建工集团",
            "qualification_level": "特级", "project_manager": "陈建国", "safety_license": "SAF-2025-001",
            "credit_rating": "AAA", "status": "正常", "created_at": _SEED_DT,
        },
        {
            "contractor_id": "CTR002", "contractor_code": "PDGD", "contractor_name": "潘达广东分公司",
            "qualification_level": "一级", "project_manager": "林志强", "safety_license": "SAF-2025-002",
            "credit_rating": "AA", "status": "正常", "created_at": _SEED_DT,
        },
        {
            "contractor_id": "CTR003", "contractor_code": "PDBJ", "contractor_name": "潘达北京分公司",
            "qualification_level": "一级", "project_manager": "张明", "safety_license": "SAF-2025-003",
            "credit_rating": "AA", "status": "正常", "created_at": _SEED_DT,
        },
    ]

    # ------------------------------------------------------------------ #
    # 4. 分包商维表
    # ------------------------------------------------------------------ #
    subcontractors = [
        {
            "subcontractor_id": "SC001", "subcontractor_code": "BJGS", "subcontractor_name": "北京钢构",
            "qualification_level": "一级", "professional_category": "钢结构", "project_manager": "赵工",
            "subcontract_type": "专业分包", "safety_license": "SAF-SC-001", "status": "正常", "created_at": _SEED_DT,
        },
        {
            "subcontractor_id": "SC002", "subcontractor_code": "GDGC", "subcontractor_name": "广东建工机械",
            "qualification_level": "二级", "professional_category": "机械租赁", "project_manager": "王总",
            "subcontract_type": "劳务分包", "safety_license": "SAF-SC-002", "status": "正常", "created_at": _SEED_DT,
        },
        {
            "subcontractor_id": "SC003", "subcontractor_code": "SHLW", "subcontractor_name": "上海劳务",
            "qualification_level": "二级", "professional_category": "劳务", "project_manager": "李经理",
            "subcontract_type": "劳务分包", "safety_license": "SAF-SC-003", "status": "正常", "created_at": _SEED_DT,
        },
    ]

    # ------------------------------------------------------------------ #
    # 5. 供应商维表
    # ------------------------------------------------------------------ #
    suppliers = [
        {
            "supplier_id": "S001", "supplier_code": "HBGC", "supplier_name": "河北钢铁集团",
            "supplier_type": "材料", "company_id": "C002", "contact_person": "张工",
            "contact_phone": "13800001001", "status": "正常", "created_at": _SEED_DT,
        },
        {
            "supplier_id": "S002", "supplier_code": "SHNJ", "supplier_name": "上海水泥",
            "supplier_type": "材料", "company_id": "C004", "contact_person": "李经理",
            "contact_phone": "13800001002", "status": "正常", "created_at": _SEED_DT,
        },
        {
            "supplier_id": "S003", "supplier_code": "HZAL", "supplier_name": "杭州铝材",
            "supplier_type": "材料", "company_id": "C001", "contact_person": "陈经理",
            "contact_phone": "13800001005", "status": "正常", "created_at": _SEED_DT,
        },
        {
            "supplier_id": "S004", "supplier_code": "BJGS", "supplier_name": "北京钢构",
            "supplier_type": "分包", "company_id": "C003", "contact_person": "赵工",
            "contact_phone": "13800001004", "status": "正常", "created_at": _SEED_DT,
        },
    ]

    # ------------------------------------------------------------------ #
    # 6. 项目维表（employer_id 替代 owner_id，无 region/department）
    # ------------------------------------------------------------------ #
    projects = [
        {
            "project_id": "P001", "project_code": "GZ-2025-001", "project_name": "广州天河CBD项目",
            "company_id": "C002", "company_name": "潘达广东分公司",
            "employer_id": "E001", "employer_name": "广州市人民政府",
            "contractor_id": "CTR002", "contractor_name": "潘达广东分公司",
            "section_id": "S01", "section_name": "一期",
            "building_area": 120000.0, "contract_amount": 580000000.0,
            "project_status": "在建", "created_at": _SEED_DT,
        },
        {
            "project_id": "P002", "project_code": "BJ-2025-002", "project_name": "北京望京SOHO",
            "company_id": "C003", "company_name": "潘达北京分公司",
            "employer_id": "E004", "employer_name": "北京伟业",
            "contractor_id": "CTR003", "contractor_name": "潘达北京分公司",
            "section_id": "S01", "section_name": "主楼",
            "building_area": 85000.0, "contract_amount": 420000000.0,
            "project_status": "在建", "created_at": _SEED_DT,
        },
        {
            "project_id": "P003", "project_code": "SH-2025-003", "project_name": "上海浦东住宅项目",
            "company_id": "C004", "company_name": "潘达上海分公司",
            "employer_id": "E002", "employer_name": "万科集团",
            "contractor_id": "CTR001", "contractor_name": "潘达建工集团",
            "section_id": "S01", "section_name": "一期",
            "building_area": 200000.0, "contract_amount": 680000000.0,
            "project_status": "在建", "created_at": _SEED_DT,
        },
        {
            "project_id": "P004", "project_code": "GZ-2025-004", "project_name": "广州白云机场配套",
            "company_id": "C002", "company_name": "潘达广东分公司",
            "employer_id": "E001", "employer_name": "广州市人民政府",
            "contractor_id": "CTR002", "contractor_name": "潘达广东分公司",
            "section_id": "S01", "section_name": "航站楼",
            "building_area": 65000.0, "contract_amount": 320000000.0,
            "project_status": "竣工", "created_at": _SEED_DT,
        },
        {
            "project_id": "P005", "project_code": "HZ-2025-005", "project_name": "杭州滨江住宅",
            "company_id": "C001", "company_name": "潘达建工集团",
            "employer_id": "E003", "employer_name": "华远地产",
            "contractor_id": "CTR001", "contractor_name": "潘达建工集团",
            "section_id": "S02", "section_name": "二期",
            "building_area": 150000.0, "contract_amount": 520000000.0,
            "project_status": "在建", "created_at": _SEED_DT,
        },
    ]

    # 合同主数据（嵌入付款事实，无 dim_contract 表）
    contract_defs = [
        {"contract_id": "CT001", "contract_code": "HT-GZ-001", "contract_name": "广州天河CBD总包合同", "project_id": "P001", "supplier_id": "", "supplier_name": "", "subcontractor_id": "", "contract_content": "施工总承包", "contract_amount": 580000000.0, "tax_rate": 0.09, "payment_ratio": 0.85, "settlement_status": "进行中"},
        {"contract_id": "CT002", "contract_code": "HT-BJ-001", "contract_name": "北京望京SOHO总包", "project_id": "P002", "supplier_id": "", "supplier_name": "", "subcontractor_id": "", "contract_content": "施工总承包", "contract_amount": 420000000.0, "tax_rate": 0.09, "payment_ratio": 0.80, "settlement_status": "进行中"},
        {"contract_id": "CT003", "contract_code": "HT-SH-001", "contract_name": "上海浦东住宅总包", "project_id": "P003", "supplier_id": "", "supplier_name": "", "subcontractor_id": "", "contract_content": "施工总承包", "contract_amount": 680000000.0, "tax_rate": 0.09, "payment_ratio": 0.82, "settlement_status": "进行中"},
        {"contract_id": "CT004", "contract_code": "HT-GZ-002", "contract_name": "白云机场配套合同", "project_id": "P004", "supplier_id": "", "supplier_name": "", "subcontractor_id": "", "contract_content": "配套工程", "contract_amount": 320000000.0, "tax_rate": 0.09, "payment_ratio": 1.0, "settlement_status": "已结算"},
        {"contract_id": "CT005", "contract_code": "HT-HZ-001", "contract_name": "杭州滨江住宅总包", "project_id": "P005", "supplier_id": "", "supplier_name": "", "subcontractor_id": "", "contract_content": "施工总承包", "contract_amount": 520000000.0, "tax_rate": 0.09, "payment_ratio": 0.78, "settlement_status": "进行中"},
        {"contract_id": "CT006", "contract_code": "HT-GZ-M01", "contract_name": "天河CBD钢材采购", "project_id": "P001", "supplier_id": "S001", "supplier_name": "河北钢铁集团", "subcontractor_id": "", "contract_content": "钢材供应", "contract_amount": 85000000.0, "tax_rate": 0.13, "payment_ratio": 0.75, "settlement_status": "进行中"},
        {"contract_id": "CT007", "contract_code": "HT-BJ-M01", "contract_name": "望京SOHO幕墙分包", "project_id": "P002", "supplier_id": "S004", "supplier_name": "北京钢构", "subcontractor_id": "SC001", "contract_content": "幕墙分包", "contract_amount": 56000000.0, "tax_rate": 0.09, "payment_ratio": 0.70, "settlement_status": "进行中"},
    ]

    def _project_contracts(project_id):
        return [c for c in contract_defs if c["project_id"] == project_id]

    # ------------------------------------------------------------------ #
    # 灌入维表（顺序：公司 → 参与方 → 项目）
    # ------------------------------------------------------------------ #
    s.sql.insert_rows("dim_company", companies)
    output.print(f"OK dim_company {len(companies)} 条")
    s.sql.insert_rows("dim_employer", employers)
    output.print(f"OK dim_employer {len(employers)} 条")
    s.sql.insert_rows("dim_contractor", contractors)
    output.print(f"OK dim_contractor {len(contractors)} 条")
    s.sql.insert_rows("dim_subcontractor", subcontractors)
    output.print(f"OK dim_subcontractor {len(subcontractors)} 条")
    s.sql.insert_rows("dim_supplier", suppliers)
    output.print(f"OK dim_supplier {len(suppliers)} 条")
    s.sql.insert_rows("dim_project", projects)
    output.print(f"OK dim_project {len(projects)} 条")

    # ------------------------------------------------------------------ #
    # 7. 项目产值事实表（2025-01 至 2025-06）
    # ------------------------------------------------------------------ #
    output_rows = []
    output_seq = 1
    for year, month in _DEMO_MONTHS:
        dk = _month_end_date_key(year, month)
        report_period = _report_period(year, month)
        created_at = _month_end_datetime(year, month)

        for project in projects:
            base_value = project["contract_amount"] / 24
            month_total = base_value * (1 + random.uniform(-0.1, 0.2))
            confirmed_ratio = random.uniform(0.6, 0.9)
            confirmed = month_total * confirmed_ratio
            unconfirmed = month_total - confirmed
            month_idx = month

            output_rows.append({
                "output_id": f"OUT{output_seq:06d}",
                "date_key": dk,
                "project_id": project["project_id"],
                "project_name": project["project_name"],
                "company_id": project["company_id"],
                "report_period": report_period,
                "confirmed_output": round(confirmed, 2),
                "unconfirmed_output": round(unconfirmed, 2),
                "total_output": round(month_total, 2),
                "output_last_year_confirmed": round(confirmed * month_idx * 0.8, 2),
                "output_last_year_unconfirmed": round(unconfirmed * month_idx * 0.5, 2),
                "output_current_confirmed": round(confirmed * month_idx, 2),
                "output_current_unconfirmed": round(unconfirmed * month_idx, 2),
                "created_at": created_at,
            })
            output_seq += 1

    out_inserted = s.sql.insert_rows("fact_project_output", output_rows)
    output.print(f"OK fact_project_output 插入 {out_inserted} 行")

    # ------------------------------------------------------------------ #
    # 8. 项目成本事实表（含 cost_level L1/L2/L3）
    # ------------------------------------------------------------------ #
    cost_rows = []
    cost_seq = 1
    cost_levels = ["L1", "L2", "L3"]
    for year, month in _DEMO_MONTHS:
        dk = _month_end_date_key(year, month)
        report_period = _report_period(year, month)
        created_at = _month_end_datetime(year, month)
        month_idx = month

        for project in projects:
            cmonth = project["contract_amount"] * random.uniform(0.015, 0.025)
            confirmed_cmonth = cmonth * random.uniform(0.65, 0.85)
            unconfirmed_cmonth = cmonth - confirmed_cmonth
            labor_ratio = random.uniform(0.2, 0.35)
            material_ratio = random.uniform(0.4, 0.55)
            equipment_ratio = random.uniform(0.1, 0.15)
            target = cmonth * random.uniform(0.95, 1.05)
            proj_contracts = _project_contracts(project["project_id"])
            contract = random.choice(proj_contracts) if proj_contracts else contract_defs[0]
            cost_level = random.choice(cost_levels)

            cost_rows.append({
                "cost_id": f"COST{cost_seq:06d}",
                "date_key": dk,
                "project_id": project["project_id"],
                "project_name": project["project_name"],
                "company_id": project["company_id"],
                "report_period": report_period,
                "cost_confirmed_acc": round(confirmed_cmonth * month_idx, 2),
                "cost_unconfirmed_acc": round(unconfirmed_cmonth * month_idx, 2),
                "cost_confirmed_cmonth": round(confirmed_cmonth, 2),
                "cost_unconfirmed_cmonth": round(unconfirmed_cmonth, 2),
                "labor_cost_acc": round(cmonth * labor_ratio * month_idx, 2),
                "material_cost_acc": round(cmonth * material_ratio * month_idx, 2),
                "equipment_cost_acc": round(cmonth * equipment_ratio * month_idx, 2),
                "management_fee_rate": round(random.uniform(0.03, 0.06), 4),
                "target_cost": round(target, 2),
                "cost_code": f"MC0{random.randint(1, 3)}",
                "cost_name": {"L1": "主控费用", "L2": "分项费用", "L3": "明细费用"}[cost_level],
                "cost_level": cost_level,
                "contract_id": contract["contract_id"],
                "created_at": created_at,
            })
            cost_seq += 1

    cost_inserted = s.sql.insert_rows("fact_project_cost", cost_rows)
    output.print(f"OK fact_project_cost 插入 {cost_inserted} 行")

    # ------------------------------------------------------------------ #
    # 9. 项目付款事实表（含合同字段，Contract 对象绑定源）
    # ------------------------------------------------------------------ #
    payment_rows = []
    payment_seq = 1
    for year, month in _DEMO_MONTHS:
        dk = _month_end_date_key(year, month)
        report_period = _report_period(year, month)
        created_at = _month_end_datetime(year, month)

        for project in projects:
            proj_contracts = [c for c in contract_defs if c["project_id"] == project["project_id"] and c["supplier_id"]]
            if not proj_contracts:
                proj_contracts = _project_contracts(project["project_id"])
            contract = random.choice(proj_contracts)
            payable_total = contract["contract_amount"] * random.uniform(0.02, 0.04)
            confirmed_ratio = random.uniform(0.7, 0.95)
            payable_confirmed = payable_total * confirmed_ratio
            payable_unconfirmed = payable_total - payable_confirmed
            paid_ratio = random.uniform(0.5, 0.9)
            paid_amount = payable_confirmed * paid_ratio

            payment_rows.append({
                "payment_id": f"PAY{payment_seq:06d}",
                "date_key": dk,
                "project_id": project["project_id"],
                "contract_id": contract["contract_id"],
                "contract_code": contract["contract_code"],
                "contract_name": contract["contract_name"],
                "contract_amount": contract["contract_amount"],
                "tax_rate": contract["tax_rate"],
                "settlement_status": contract["settlement_status"],
                "supplier_id": contract.get("supplier_id") or "S001",
                "supplier_name": contract.get("supplier_name") or "",
                "report_period": report_period,
                "payable_confirmed": round(payable_confirmed, 2),
                "payable_unconfirmed": round(payable_unconfirmed, 2),
                "labor_payable": round(payable_confirmed * random.uniform(0.15, 0.25), 2),
                "paid_amount": round(paid_amount, 2),
                "payment_ratio": round(paid_ratio, 4),
                "approval_status": "已批复" if random.random() > 0.1 else "审批中",
                "approval_amount": round(payable_total * random.uniform(0.8, 1.0), 2),
                "created_at": created_at,
            })
            payment_seq += 1

    pay_inserted = s.sql.insert_rows("fact_project_payment", payment_rows)
    output.print(f"OK fact_project_payment 插入 {pay_inserted} 行")

    # ------------------------------------------------------------------ #
    # 10. 项目收支事实表（无 dim_cost_subject，科目字段冗余）
    # ------------------------------------------------------------------ #
    balance_subjects = [
        {"subject_code": "SR01", "subject_name": "主营业务收入", "subject_type": "收入"},
        {"subject_code": "ZC01", "subject_name": "主营业务成本", "subject_type": "支出"},
    ]
    balance_rows = []
    balance_seq = 1
    for year, month in _DEMO_MONTHS:
        dk = _month_end_date_key(year, month)
        report_period = _report_period(year, month)
        created_at = _month_end_datetime(year, month)

        for project in projects:
            for subject in balance_subjects:
                ratio = 0.04 if subject["subject_type"] == "收入" else 0.035
                amount = project["contract_amount"] * random.uniform(ratio * 0.8, ratio * 1.2)
                project_amount = amount * 0.8
                company_amount = amount * 0.2

                balance_rows.append({
                    "balance_id": f"BAL{balance_seq:06d}",
                    "date_key": dk,
                    "project_id": project["project_id"],
                    "subject_code": subject["subject_code"],
                    "subject_name": subject["subject_name"],
                    "report_period": report_period,
                    "project_amount": round(project_amount, 2),
                    "company_amount": round(company_amount, 2),
                    "total_amount": round(amount, 2),
                    "created_at": created_at,
                })
                balance_seq += 1

    bal_inserted = s.sql.insert_rows("fact_project_balance", balance_rows)
    output.print(f"OK fact_project_balance 插入 {bal_inserted} 行")

    # ------------------------------------------------------------------ #
    # 11. 项目指标事实表
    # ------------------------------------------------------------------ #
    indicator_defs = [
        ("profit_rate", "毛利率", 18.0),
        ("cost_rate", "成本率", 75.0),
        ("confirm_rate", "确权率", 80.0),
        ("collection_rate", "回款率", 70.0),
        ("payment_rate", "付款率", 65.0),
    ]
    indicator_rows = []
    indicator_seq = 1
    for year, month in _DEMO_MONTHS:
        dk = _month_end_date_key(year, month)
        report_period = _report_period(year, month)
        created_at = _month_end_datetime(year, month)

        for project in projects:
            for code, name, target in indicator_defs:
                actual = target * random.uniform(0.85, 1.15)
                if actual >= target * 1.05:
                    warning = "green"
                elif actual >= target * 0.9:
                    warning = "yellow"
                else:
                    warning = "red"

                indicator_rows.append({
                    "indicator_id": f"IND{indicator_seq:06d}",
                    "date_key": dk,
                    "project_id": project["project_id"],
                    "company_id": project["company_id"],
                    "report_period": report_period,
                    "indicator_code": code,
                    "indicator_name": name,
                    "indicator_value": round(actual, 2),
                    "target_value": target,
                    "warning_level": warning,
                    "remark": f"{report_period} {name}达成情况",
                    "created_at": created_at,
                })
                indicator_seq += 1

    ind_inserted = s.sql.insert_rows("fact_project_indicator", indicator_rows)
    output.print(f"OK fact_project_indicator 插入 {ind_inserted} 行")

    # ------------------------------------------------------------------ #
    # 12. 项目风险事实表
    # ------------------------------------------------------------------ #
    risk_rows = []
    risk_seq = 1
    risk_types = ["成本风险", "进度风险", "质量风险", "安全风险", "资金风险"]
    warning_levels = ["green", "yellow", "red"]

    for year, month in _DEMO_MONTHS[::2]:
        dk = _month_end_date_key(year, month)
        report_period = _report_period(year, month)
        created_at = _month_end_datetime(year, month)

        for project in projects:
            if random.random() > 0.3:
                risk_type = random.choice(risk_types)
                level = random.choices(warning_levels, weights=[0.5, 0.35, 0.15])[0]
                if level == "red":
                    risk_value = random.randint(70, 100)
                elif level == "yellow":
                    risk_value = random.randint(40, 69)
                else:
                    risk_value = random.randint(10, 39)

                risk_rows.append({
                    "risk_id": f"RISK{risk_seq:06d}",
                    "date_key": dk,
                    "project_id": project["project_id"],
                    "report_period": report_period,
                    "risk_type": risk_type,
                    "risk_code": f"RK-{risk_type[:2]}-{risk_seq:04d}",
                    "risk_name": f"{project['project_name']}{risk_type}",
                    "risk_value": risk_value,
                    "warning_level": level,
                    "risk_description": f"{project['project_name']}存在{risk_type}，需加强监控",
                    "overall_warning_level": level,
                    "created_at": created_at,
                })
                risk_seq += 1

    risk_inserted = s.sql.insert_rows("fact_project_risk", risk_rows)
    output.print(f"OK fact_project_risk 插入 {risk_inserted} 行")

    # ------------------------------------------------------------------ #
    # 13. 收款事实表（V3 新增）
    # ------------------------------------------------------------------ #
    receipt_rows = []
    receipt_seq = 1
    receipt_types = ["预付款", "进度款", "结算款", "质保金"]
    for year, month in _DEMO_MONTHS:
        dk = _month_end_date_key(year, month)
        report_period = _report_period(year, month)
        created_at = _month_end_datetime(year, month)

        for project in projects:
            main_contract = _project_contracts(project["project_id"])[0]
            receipt_amount = project["contract_amount"] * random.uniform(0.015, 0.035)
            overdue = random.randint(0, 15) if random.random() > 0.7 else 0

            receipt_rows.append({
                "receipt_id": f"RCP{receipt_seq:06d}",
                "date_key": dk,
                "project_id": project["project_id"],
                "contract_id": main_contract["contract_id"],
                "report_period": report_period,
                "receipt_amount": round(receipt_amount, 2),
                "receipt_date": created_at,
                "receipt_method": random.choice(["银行转账", "承兑汇票", "现金"]),
                "receipt_type": random.choice(receipt_types),
                "overdue_days": overdue,
                "created_at": created_at,
            })
            receipt_seq += 1

    receipt_inserted = s.sql.insert_rows("fact_receipt", receipt_rows)
    output.print(f"OK fact_receipt 插入 {receipt_inserted} 行")

    # ------------------------------------------------------------------ #
    # 14. 结算事实表（V3 新增）
    # ------------------------------------------------------------------ #
    settlement_rows = []
    settlement_seq = 1
    for year, month in _DEMO_MONTHS[2:5]:
        dk = _month_end_date_key(year, month)
        report_period = _report_period(year, month)
        created_at = _month_end_datetime(year, month)

        for project in projects[:3]:
            settlement_amount = project["contract_amount"] * random.uniform(0.05, 0.12)
            settlement_rows.append({
                "settlement_id": f"STL{settlement_seq:06d}",
                "date_key": dk,
                "project_id": project["project_id"],
                "report_period": report_period,
                "settlement_amount": round(settlement_amount, 2),
                "settlement_date": created_at,
                "audit_status": random.choice(["已审核", "审核中", "待审核"]),
                "audit_opinion": "审计无重大异常" if random.random() > 0.3 else "需补充资料",
                "three_estimate_comparison": random.choice(["概算>预算>决算", "概算=预算>决算"]),
                "review_deduction_amount": round(settlement_amount * random.uniform(0, 0.05), 2),
                "created_at": created_at,
            })
            settlement_seq += 1

    settlement_inserted = s.sql.insert_rows("fact_settlement", settlement_rows)
    output.print(f"OK fact_settlement 插入 {settlement_inserted} 行")

    # ------------------------------------------------------------------ #
    # 15. 保证金事实表（V3 新增）
    # ------------------------------------------------------------------ #
    bond_rows = []
    bond_seq = 1
    bond_types = ["投标保证金", "履约保证金", "质量保证金", "农民工工资保证金"]
    for project in projects:
        for bond_type in random.sample(bond_types, k=2):
            bond_amount = project["contract_amount"] * random.uniform(0.005, 0.02)
            returned = bond_amount * random.uniform(0, 0.6)
            unreturned = bond_amount - returned
            payment_dt = datetime(2025, 1, 15, 0, 0, 0)
            due_dt = datetime(2025, 12, 31, 0, 0, 0)
            main_contract = _project_contracts(project["project_id"])[0]

            bond_rows.append({
                "bond_id": f"BND{bond_seq:06d}",
                "date_key": _month_end_date_key(2025, 6),
                "project_id": project["project_id"],
                "contract_id": main_contract["contract_id"],
                "report_period": "2025-06",
                "bond_type": bond_type,
                "bond_amount": round(bond_amount, 2),
                "payment_date": payment_dt,
                "due_date": due_dt,
                "return_conditions": "工程竣工验收且无违约",
                "returned_amount": round(returned, 2),
                "unreturned_amount": round(unreturned, 2),
                "forfeit_status": "无" if unreturned > 0 else "已退还",
                "created_at": _month_end_datetime(2025, 6),
            })
            bond_seq += 1

    bond_inserted = s.sql.insert_rows("fact_bond", bond_rows)
    output.print(f"OK fact_bond 插入 {bond_inserted} 行")

    # ------------------------------------------------------------------ #
    # 16. 罚款事实表（V3 新增）
    # ------------------------------------------------------------------ #
    penalty_rows = []
    penalty_seq = 1
    penalty_types = ["违约罚款", "违规罚款", "质量安全罚款"]
    for year, month in _DEMO_MONTHS[::3]:
        dk = _month_end_date_key(year, month)
        report_period = _report_period(year, month)
        created_at = _month_end_datetime(year, month)

        for project in random.sample(projects, k=3):
            penalty_amount = random.uniform(50000, 500000)
            penalty_rows.append({
                "penalty_id": f"PEN{penalty_seq:06d}",
                "date_key": dk,
                "project_id": project["project_id"],
                "report_period": report_period,
                "penalty_type": random.choice(penalty_types),
                "penalty_amount": round(penalty_amount, 2),
                "penalty_reason": f"{project['project_name']}施工违规",
                "issuing_unit": project["employer_name"],
                "penalty_date": created_at,
                "payment_status": random.choice(["已缴纳", "待缴纳", "申诉中"]),
                "appeal_status": random.choice(["无", "申诉中", "已驳回"]),
                "created_at": created_at,
            })
            penalty_seq += 1

    penalty_inserted = s.sql.insert_rows("fact_penalty", penalty_rows)
    output.print(f"OK fact_penalty 插入 {penalty_inserted} 行")

    # ------------------------------------------------------------------ #
    # 17. 赔偿事实表（V3 新增）
    # ------------------------------------------------------------------ #
    compensation_rows = []
    compensation_seq = 1
    compensation_types = ["合同赔偿", "侵权赔偿", "工伤赔偿"]
    for project in random.sample(projects, k=3):
        compensation_amount = random.uniform(100000, 800000)
        compensation_rows.append({
            "compensation_id": f"CMP{compensation_seq:06d}",
            "date_key": _month_end_date_key(2025, 4),
            "project_id": project["project_id"],
            "report_period": "2025-04",
            "compensation_type": random.choice(compensation_types),
            "compensation_amount": round(compensation_amount, 2),
            "compensation_reason": f"{project['project_name']}第三方损失",
            "responsible_party": project["contractor_name"],
            "compensation_date": _month_end_datetime(2025, 4),
            "payment_status": random.choice(["已支付", "待支付"]),
            "created_at": _month_end_datetime(2025, 4),
        })
        compensation_seq += 1

    compensation_inserted = s.sql.insert_rows("fact_compensation", compensation_rows)
    output.print(f"OK fact_compensation 插入 {compensation_inserted} 行")

    # ------------------------------------------------------------------ #
    # 18. 工程保险事实表（V3 新增）
    # ------------------------------------------------------------------ #
    insurance_rows = []
    insurance_seq = 1
    insurance_types = ["工程险", "意外险", "责任险"]
    for project in projects:
        for ins_type in random.sample(insurance_types, k=2):
            insurance_amount = project["contract_amount"] * random.uniform(0.01, 0.03)
            premium = insurance_amount * random.uniform(0.001, 0.005)
            insurance_rows.append({
                "insurance_id": f"INS{insurance_seq:06d}",
                "date_key": _month_end_date_key(2025, 6),
                "project_id": project["project_id"],
                "report_period": "2025-06",
                "insurance_type": ins_type,
                "insurance_company": random.choice(["中国人保", "中国平安", "太平洋保险"]),
                "insurance_amount": round(insurance_amount, 2),
                "premium_amount": round(premium, 2),
                "purchase_date": datetime(2025, 1, 10, 0, 0, 0),
                "expiry_date": datetime(2026, 1, 9, 0, 0, 0),
                "claim_status": random.choice(["无理赔", "待理赔", "已理赔"]),
                "created_at": _month_end_datetime(2025, 6),
            })
            insurance_seq += 1

    insurance_inserted = s.sql.insert_rows("fact_insurance", insurance_rows)
    output.print(f"OK fact_insurance 插入 {insurance_inserted} 行")

    # ------------------------------------------------------------------ #
    # 19. 机械设备事实表（V3 新增）
    # ------------------------------------------------------------------ #
    equipment_rows = []
    equipment_seq = 1
    equipment_catalog = [
        ("EQ-T001", "塔吊", "QTZ80", 850000.0),
        ("EQ-E001", "挖掘机", "CAT320", 420000.0),
        ("EQ-P001", "混凝土泵车", "SY5418", 680000.0),
        ("EQ-L001", "汽车吊", "QY25K", 350000.0),
    ]
    for project in projects:
        for code, name, model, orig_val in random.sample(equipment_catalog, k=2):
            equipment_rows.append({
                "equipment_id": f"EQP{equipment_seq:06d}",
                "date_key": _month_end_date_key(2025, 6),
                "project_id": project["project_id"],
                "report_period": "2025-06",
                "equipment_code": f"{code}-{project['project_id']}",
                "equipment_name": name,
                "model_spec": model,
                "original_value": orig_val,
                "depreciation_method": "直线法",
                "unit_price": round(random.uniform(800, 2500), 2),
                "usage_status": random.choice(["在用", "闲置", "维修"]),
                "equipment_status": random.choice(["自有", "租赁"]),
                "created_at": _month_end_datetime(2025, 6),
            })
            equipment_seq += 1

    equipment_inserted = s.sql.insert_rows("fact_equipment", equipment_rows)
    output.print(f"OK fact_equipment 插入 {equipment_inserted} 行")

    summary = {
        "ok": True,
        "space_id": space_id,
        "version": "V3",
        "companies": len(companies),
        "employers": len(employers),
        "contractors": len(contractors),
        "subcontractors": len(subcontractors),
        "suppliers": len(suppliers),
        "projects": len(projects),
        "output_inserted": out_inserted,
        "cost_inserted": cost_inserted,
        "payment_inserted": pay_inserted,
        "balance_inserted": bal_inserted,
        "indicator_inserted": ind_inserted,
        "risk_inserted": risk_inserted,
        "receipt_inserted": receipt_inserted,
        "settlement_inserted": settlement_inserted,
        "bond_inserted": bond_inserted,
        "penalty_inserted": penalty_inserted,
        "compensation_inserted": compensation_inserted,
        "insurance_inserted": insurance_inserted,
        "equipment_inserted": equipment_inserted,
    }
    output.success("V3 灌数完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))
