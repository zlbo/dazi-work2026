"""潘达工程商务成本演示数据灌入 — space__panda_construction

前置：先执行 panda_cost_ontology_init.py 建表；dim_date 由空间其他域提供或已存在。
幂等：fact_project_output 已有数据则跳过。

放置：项目/潘达工程-商务成本/本体/ontos/本体规划02/setup/panda_cost_seed_data.py
发布：dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划02/setup/panda_cost_seed_data.py --space space__panda_construction --type data
规划对照：项目/潘达工程-商务成本/本体/ontos/本体规划02/plans/潘达工程商务成本管理本体方案.md §2
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


def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)

    output.print("=== 潘达工程商务成本演示数据灌入 ===")

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

    # 1. 地区维表
    regions = [
        {"region_id": "R001", "region_code": "GD", "region_name": "广东省", "province": "广东", "city": "广州", "district": "", "region_level": "华南", "status": "正常", "created_at": _SEED_DT},
        {"region_id": "R002", "region_code": "BJ", "region_name": "北京市", "province": "北京", "city": "北京", "district": "", "region_level": "华北", "status": "正常", "created_at": _SEED_DT},
        {"region_id": "R003", "region_code": "SH", "region_name": "上海市", "province": "上海", "city": "上海", "district": "", "region_level": "华东", "status": "正常", "created_at": _SEED_DT},
        {"region_id": "R004", "region_code": "ZJ", "region_name": "浙江省", "province": "浙江", "city": "杭州", "district": "", "region_level": "华东", "status": "正常", "created_at": _SEED_DT},
        {"region_id": "R005", "region_code": "CD", "region_name": "成都市", "province": "四川", "city": "成都", "district": "", "region_level": "西南", "status": "正常", "created_at": _SEED_DT},
    ]
    # 2. 分公司维表（含 region_id）
    companies = [
        {"company_id": "C001", "company_code": "PDJT", "company_name": "潘达建工集团", "region_id": "R001", "region_name": "广东省", "status": "正常", "created_at": _SEED_DT},
        {"company_id": "C002", "company_code": "PDGD", "company_name": "潘达广东分公司", "region_id": "R001", "region_name": "广东省", "status": "正常", "created_at": _SEED_DT},
        {"company_id": "C003", "company_code": "PDBJ", "company_name": "潘达北京分公司", "region_id": "R002", "region_name": "北京市", "status": "正常", "created_at": _SEED_DT},
        {"company_id": "C004", "company_code": "PDSH", "company_name": "潘达上海分公司", "region_id": "R003", "region_name": "上海市", "status": "正常", "created_at": _SEED_DT},
    ]
    # 3. 部门维表（含 company_id）
    departments = [
        {"department_id": "D001", "department_code": "BD", "department_name": "商务部", "company_id": "C001", "parent_id": "", "department_level": 1, "status": "正常", "created_at": _SEED_DT},
        {"department_id": "D002", "department_code": "CO", "department_name": "成本部", "company_id": "C001", "parent_id": "", "department_level": 1, "status": "正常", "created_at": _SEED_DT},
        {"department_id": "D003", "department_code": "FN", "department_name": "财务部", "company_id": "C001", "parent_id": "", "department_level": 1, "status": "正常", "created_at": _SEED_DT},
        {"department_id": "D004", "department_code": "PJ", "department_name": "项目管理部", "company_id": "C001", "parent_id": "", "department_level": 1, "status": "正常", "created_at": _SEED_DT},
        {"department_id": "D005", "department_code": "BD01", "department_name": "商务一部", "company_id": "C001", "parent_id": "D001", "department_level": 2, "status": "正常", "created_at": _SEED_DT},
    ]

    # 4. 业主维表
    owners = [
        {"owner_id": "O001", "owner_code": "GZRD", "owner_name": "广州市人民政府", "owner_type": "政府", "credit_level": "AAA", "status": "正常", "created_at": _SEED_DT},
        {"owner_id": "O002", "owner_code": "WHJT", "owner_name": "万科集团", "owner_type": "民企", "credit_level": "AA", "status": "正常", "created_at": _SEED_DT},
        {"owner_id": "O003", "owner_code": "HYDL", "owner_name": "华远地产", "owner_type": "民企", "credit_level": "A", "status": "正常", "created_at": _SEED_DT},
        {"owner_id": "O004", "owner_code": "ZJRJ", "owner_name": "中建科技", "owner_type": "国企", "credit_level": "AA", "status": "正常", "created_at": _SEED_DT},
        {"owner_id": "O005", "owner_code": "BJWY", "owner_name": "北京伟业", "owner_type": "民企", "credit_level": "A", "status": "正常", "created_at": _SEED_DT},
    ]
    # 5. 成本/收支科目维表（parent_subject_id, subject_type）
    cost_subjects = [
        {"subject_id": "CS001", "subject_code": "LB", "subject_name": "人工费", "subject_level": 1, "parent_subject_id": "", "subject_type": "成本", "is_leaf": 0, "status": "正常", "created_at": _SEED_DT},
        {"subject_id": "CS002", "subject_code": "CL", "subject_name": "材料费", "subject_level": 1, "parent_subject_id": "", "subject_type": "成本", "is_leaf": 0, "status": "正常", "created_at": _SEED_DT},
        {"subject_id": "CS003", "subject_code": "JX", "subject_name": "机械费", "subject_level": 1, "parent_subject_id": "", "subject_type": "成本", "is_leaf": 0, "status": "正常", "created_at": _SEED_DT},
        {"subject_id": "CS004", "subject_code": "QT", "subject_name": "其他费用", "subject_level": 1, "parent_subject_id": "", "subject_type": "成本", "is_leaf": 0, "status": "正常", "created_at": _SEED_DT},
        {"subject_id": "CS005", "subject_code": "LB01", "subject_name": "管理人员工资", "subject_level": 2, "parent_subject_id": "CS001", "subject_type": "成本", "is_leaf": 1, "status": "正常", "created_at": _SEED_DT},
        {"subject_id": "CS006", "subject_code": "CL01", "subject_name": "钢材", "subject_level": 2, "parent_subject_id": "CS002", "subject_type": "成本", "is_leaf": 1, "status": "正常", "created_at": _SEED_DT},
        {"subject_id": "CS007", "subject_code": "SR01", "subject_name": "主营业务收入", "subject_level": 1, "parent_subject_id": "", "subject_type": "收入", "is_leaf": 1, "status": "正常", "created_at": _SEED_DT},
        {"subject_id": "CS008", "subject_code": "ZC01", "subject_name": "主营业务成本", "subject_level": 1, "parent_subject_id": "", "subject_type": "支出", "is_leaf": 1, "status": "正常", "created_at": _SEED_DT},
    ]
    subject_map = {cs["subject_id"]: cs for cs in cost_subjects}

    # 6. 供应商维表（company_id, supplier_type）
    suppliers = [
        {"supplier_id": "S001", "supplier_code": "HBGC", "supplier_name": "河北钢铁集团", "supplier_type": "材料", "company_id": "C002", "contact_person": "张工", "contact_phone": "13800001001", "status": "正常", "created_at": _SEED_DT},
        {"supplier_id": "S002", "supplier_code": "SHNJ", "supplier_name": "上海水泥", "supplier_type": "材料", "company_id": "C004", "contact_person": "李经理", "contact_phone": "13800001002", "status": "正常", "created_at": _SEED_DT},
        {"supplier_id": "S003", "supplier_code": "GDGC", "supplier_name": "广东建工机械", "supplier_type": "设备", "company_id": "C002", "contact_person": "王总", "contact_phone": "13800001003", "status": "正常", "created_at": _SEED_DT},
        {"supplier_id": "S004", "supplier_code": "BJGS", "supplier_name": "北京钢构", "supplier_type": "分包", "company_id": "C003", "contact_person": "赵工", "contact_phone": "13800001004", "status": "正常", "created_at": _SEED_DT},
        {"supplier_id": "S005", "supplier_code": "HZAL", "supplier_name": "杭州铝材", "supplier_type": "材料", "company_id": "C001", "contact_person": "陈经理", "contact_phone": "13800001005", "status": "正常", "created_at": _SEED_DT},
    ]
    # 7. 项目维表（region_id, owner_id, department_id, project_status）
    projects = [
        {
            "project_id": "P001", "project_code": "GZ-2025-001", "project_name": "广州天河CBD项目",
            "company_id": "C002", "company_name": "潘达广东分公司",
            "region_id": "R001", "region_name": "广东省",
            "owner_id": "O001", "owner_name": "广州市人民政府",
            "department_id": "D005", "department_name": "商务一部",
            "section_id": "S01", "section_name": "一期",
            "building_area": 120000.0, "contract_amount": 580000000.0,
            "project_status": "在建", "monthly_budget_approved": 1,
            "created_at": _SEED_DT,
        },
        {
            "project_id": "P002", "project_code": "BJ-2025-002", "project_name": "北京望京SOHO",
            "company_id": "C003", "company_name": "潘达北京分公司",
            "region_id": "R002", "region_name": "北京市",
            "owner_id": "O005", "owner_name": "北京伟业",
            "department_id": "D005", "department_name": "商务一部",
            "section_id": "S01", "section_name": "主楼",
            "building_area": 85000.0, "contract_amount": 420000000.0,
            "project_status": "在建", "monthly_budget_approved": 1,
            "created_at": _SEED_DT,
        },
        {
            "project_id": "P003", "project_code": "SH-2025-003", "project_name": "上海浦东住宅项目",
            "company_id": "C004", "company_name": "潘达上海分公司",
            "region_id": "R003", "region_name": "上海市",
            "owner_id": "O002", "owner_name": "万科集团",
            "department_id": "D005", "department_name": "商务一部",
            "section_id": "S01", "section_name": "一期",
            "building_area": 200000.0, "contract_amount": 680000000.0,
            "project_status": "在建", "monthly_budget_approved": 1,
            "created_at": _SEED_DT,
        },
        {
            "project_id": "P004", "project_code": "GZ-2025-004", "project_name": "广州白云机场配套",
            "company_id": "C002", "company_name": "潘达广东分公司",
            "region_id": "R001", "region_name": "广东省",
            "owner_id": "O001", "owner_name": "广州市人民政府",
            "department_id": "D004", "department_name": "项目管理部",
            "section_id": "S01", "section_name": "航站楼",
            "building_area": 65000.0, "contract_amount": 320000000.0,
            "project_status": "竣工", "monthly_budget_approved": 1,
            "created_at": _SEED_DT,
        },
        {
            "project_id": "P005", "project_code": "HZ-2025-005", "project_name": "杭州滨江住宅",
            "company_id": "C001", "company_name": "潘达建工集团",
            "region_id": "R004", "region_name": "浙江省",
            "owner_id": "O003", "owner_name": "华远地产",
            "department_id": "D005", "department_name": "商务一部",
            "section_id": "S01", "section_name": "二期",
            "building_area": 150000.0, "contract_amount": 520000000.0,
            "project_status": "在建", "monthly_budget_approved": 0,
            "created_at": _SEED_DT,
        },
    ]

    # 8. 合同维表（supplier_id）
    contracts = [
        {"contract_id": "CT001", "contract_code": "HT-GZ-001", "contract_name": "广州天河CBD总包合同", "project_id": "P001", "supplier_id": "", "supplier_name": "", "contract_content": "施工总承包", "contract_amount": 580000000.0, "tax_rate": 0.09, "payment_ratio": 0.85, "settlement_status": "进行中", "status": "正常", "created_at": _SEED_DT},
        {"contract_id": "CT002", "contract_code": "HT-BJ-001", "contract_name": "北京望京SOHO总包", "project_id": "P002", "supplier_id": "", "supplier_name": "", "contract_content": "施工总承包", "contract_amount": 420000000.0, "tax_rate": 0.09, "payment_ratio": 0.80, "settlement_status": "进行中", "status": "正常", "created_at": _SEED_DT},
        {"contract_id": "CT003", "contract_code": "HT-SH-001", "contract_name": "上海浦东住宅总包", "project_id": "P003", "supplier_id": "", "supplier_name": "", "contract_content": "施工总承包", "contract_amount": 680000000.0, "tax_rate": 0.09, "payment_ratio": 0.82, "settlement_status": "进行中", "status": "正常", "created_at": _SEED_DT},
        {"contract_id": "CT004", "contract_code": "HT-GZ-002", "contract_name": "白云机场配套合同", "project_id": "P004", "supplier_id": "", "supplier_name": "", "contract_content": "配套工程", "contract_amount": 320000000.0, "tax_rate": 0.09, "payment_ratio": 1.0, "settlement_status": "已结算", "status": "正常", "created_at": _SEED_DT},
        {"contract_id": "CT005", "contract_code": "HT-HZ-001", "contract_name": "杭州滨江住宅总包", "project_id": "P005", "supplier_id": "", "supplier_name": "", "contract_content": "施工总承包", "contract_amount": 520000000.0, "tax_rate": 0.09, "payment_ratio": 0.78, "settlement_status": "进行中", "status": "正常", "created_at": _SEED_DT},
        {"contract_id": "CT006", "contract_code": "HT-GZ-M01", "contract_name": "天河CBD钢材采购", "project_id": "P001", "supplier_id": "S001", "supplier_name": "河北钢铁集团", "contract_content": "钢材供应", "contract_amount": 85000000.0, "tax_rate": 0.13, "payment_ratio": 0.75, "settlement_status": "进行中", "status": "正常", "created_at": _SEED_DT},
        {"contract_id": "CT007", "contract_code": "HT-BJ-M01", "contract_name": "望京SOHO幕墙分包", "project_id": "P002", "supplier_id": "S004", "supplier_name": "北京钢构", "contract_content": "幕墙分包", "contract_amount": 56000000.0, "tax_rate": 0.09, "payment_ratio": 0.70, "settlement_status": "进行中", "status": "正常", "created_at": _SEED_DT},
    ]

    def _project_contracts(project_id):
        return [c for c in contracts if c["project_id"] == project_id]

    # 灌入维表（顺序：地区 → 公司 → 部门 → 业主 → 科目 → 供应商 → 项目 → 合同）
    s.sql.insert_rows("dim_region", regions)
    output.print(f"OK dim_region {len(regions)} 条")
    s.sql.insert_rows("dim_company", companies)
    output.print(f"OK dim_company {len(companies)} 条")
    s.sql.insert_rows("dim_department", departments)
    output.print(f"OK dim_department {len(departments)} 条")
    s.sql.insert_rows("dim_owner", owners)
    output.print(f"OK dim_owner {len(owners)} 条")
    s.sql.insert_rows("dim_cost_subject", cost_subjects)
    output.print(f"OK dim_cost_subject {len(cost_subjects)} 条")
    s.sql.insert_rows("dim_supplier", suppliers)
    output.print(f"OK dim_supplier {len(suppliers)} 条")
    s.sql.insert_rows("dim_project", projects)
    output.print(f"OK dim_project {len(projects)} 条")
    s.sql.insert_rows("dim_contract", contracts)
    output.print(f"OK dim_contract {len(contracts)} 条")

    # 9. 项目产值事实表（2025-01 至 2025-06）
    output_rows = []
    output_seq = 1
    for year, month in _DEMO_MONTHS:
        dk = _month_end_date_key(year, month)
        report_period = _report_period(year, month)
        created_at = datetime(year, month, calendar.monthrange(year, month)[1], 12, 0, 0)

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

    # 10. 项目成本事实表
    cost_rows = []
    cost_seq = 1
    for year, month in _DEMO_MONTHS:
        dk = _month_end_date_key(year, month)
        report_period = _report_period(year, month)
        created_at = datetime(year, month, calendar.monthrange(year, month)[1], 12, 0, 0)
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
            contract_id = random.choice(proj_contracts)["contract_id"] if proj_contracts else ""

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
                "cost_code": "MC01",
                "cost_name": "主控费用",
                "cost_level": "L1",
                "contract_id": contract_id,
                "created_at": created_at,
            })
            cost_seq += 1

    cost_inserted = s.sql.insert_rows("fact_project_cost", cost_rows)
    output.print(f"OK fact_project_cost 插入 {cost_inserted} 行")

    # 11. 项目付款事实表（payment_id, payable_confirmed, paid_amount 等）
    payment_rows = []
    payment_seq = 1
    for year, month in _DEMO_MONTHS:
        dk = _month_end_date_key(year, month)
        report_period = _report_period(year, month)
        created_at = datetime(year, month, calendar.monthrange(year, month)[1], 12, 0, 0)

        for project in projects:
            proj_contracts = [c for c in contracts if c["project_id"] == project["project_id"] and c["supplier_id"]]
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
                "supplier_id": contract.get("supplier_id") or "S001",
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

    # 12. 项目收支事实表（含 subject_id）
    balance_rows = []
    balance_seq = 1
    balance_subjects = [subject_map["CS007"], subject_map["CS008"]]
    for year, month in _DEMO_MONTHS:
        dk = _month_end_date_key(year, month)
        report_period = _report_period(year, month)
        created_at = datetime(year, month, calendar.monthrange(year, month)[1], 12, 0, 0)

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
                    "subject_id": subject["subject_id"],
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

    # 13. 项目指标事实表（indicator_id, risk_value 等简化指标）
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
        created_at = datetime(year, month, calendar.monthrange(year, month)[1], 12, 0, 0)

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

    # 14. 项目风险事实表（risk_id, risk_value）
    risk_rows = []
    risk_seq = 1
    risk_types = ["成本风险", "进度风险", "质量风险", "安全风险", "资金风险"]
    warning_levels = ["green", "yellow", "red"]

    for year, month in _DEMO_MONTHS[::2]:  # 隔月生成风险记录
        dk = _month_end_date_key(year, month)
        report_period = _report_period(year, month)
        created_at = datetime(year, month, calendar.monthrange(year, month)[1], 12, 0, 0)

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

    summary = {
        "ok": True,
        "space_id": space_id,
        "regions": len(regions),
        "companies": len(companies),
        "departments": len(departments),
        "owners": len(owners),
        "cost_subjects": len(cost_subjects),
        "suppliers": len(suppliers),
        "projects": len(projects),
        "contracts": len(contracts),
        "output_inserted": out_inserted,
        "cost_inserted": cost_inserted,
        "payment_inserted": pay_inserted,
        "balance_inserted": bal_inserted,
        "indicator_inserted": ind_inserted,
        "risk_inserted": risk_inserted,
    }
    output.success("灌数完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))
