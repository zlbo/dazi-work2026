"""商务成本演示数据灌入 — space__panda_construction

前置：先执行 cost_ontology_init.py 建表；dim_date 由空间其他域提供或已存在。
幂等：fact_project_output 已有数据则跳过。

放置：项目/潘达工程-商务成本/本体/ontos/商务成本/setup/cost_seed_data.py
发布：dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/商务成本/setup/cost_seed_data.py --space space__panda_construction --type data
"""

import json
import random
from datetime import date, datetime, timedelta

_SEED_DT = datetime(2025, 1, 1, 0, 0, 0)


def _date_key(d):
    return int(d.strftime("%Y%m%d"))


def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)

    output.print("=== 商务成本演示数据灌入 ===")

    # 幂等性检查
    try:
        n = int(s.sql.query_one("SELECT count() FROM fact_project_output") or 0)
    except Exception:
        n = 0
    if n > 0:
        output.print(f"fact_project_output 已有 {n} 行，跳过灌数")
        output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "skipped": True, "rows": n}, ensure_ascii=True))
        return

    random.seed(8806)

    # 1. 地区维表数据
    regions = [
        {"region_id": "R001", "region_code": "GD", "region_name": "广东省", "province": "广东", "city": "广州", "district": "", "region_level": "华南", "status": "active", "created_at": _SEED_DT},
        {"region_id": "R002", "region_code": "BJ", "region_name": "北京市", "province": "北京", "city": "北京", "district": "", "region_level": "华北", "status": "active", "created_at": _SEED_DT},
        {"region_id": "R003", "region_code": "SH", "region_name": "上海市", "province": "上海", "city": "上海", "district": "", "region_level": "华东", "status": "active", "created_at": _SEED_DT},
        {"region_id": "R004", "region_code": "ZJ", "region_name": "浙江省", "province": "浙江", "city": "杭州", "district": "", "region_level": "华东", "status": "active", "created_at": _SEED_DT},
        {"region_id": "R005", "region_code": "CD", "region_name": "成都市", "province": "四川", "city": "成都", "district": "", "region_level": "西南", "status": "active", "created_at": _SEED_DT},
    ]

    # 2. 部门维表数据
    departments = [
        {"department_id": "D001", "department_code": "BD", "department_name": "商务部", "parent_id": "", "department_level": 1, "status": "active", "created_at": _SEED_DT},
        {"department_id": "D002", "department_code": "CO", "department_name": "成本部", "parent_id": "", "department_level": 1, "status": "active", "created_at": _SEED_DT},
        {"department_id": "D003", "department_code": "FN", "department_name": "财务部", "parent_id": "", "department_level": 1, "status": "active", "created_at": _SEED_DT},
        {"department_id": "D004", "department_code": "PJ", "department_name": "项目管理部", "parent_id": "", "department_level": 1, "status": "active", "created_at": _SEED_DT},
        {"department_id": "D005", "department_code": "BD01", "department_name": "商务一部", "parent_id": "D001", "department_level": 2, "status": "active", "created_at": _SEED_DT},
    ]

    # 3. 业主维表数据
    owners = [
        {"owner_id": "O001", "owner_code": "GZRD", "owner_name": "广州市人民政府", "owner_type": "政府", "status": "active", "created_at": _SEED_DT},
        {"owner_id": "O002", "owner_code": "WHJT", "owner_name": "万科集团", "owner_type": "房地产", "status": "active", "created_at": _SEED_DT},
        {"owner_id": "O003", "owner_code": "HYDL", "owner_name": "华远地产", "owner_type": "房地产", "status": "active", "created_at": _SEED_DT},
        {"owner_id": "O004", "owner_code": "ZJRJ", "owner_name": "中建科技", "owner_type": "企业", "status": "active", "created_at": _SEED_DT},
        {"owner_id": "O005", "owner_code": "BJWY", "owner_name": "北京伟业", "owner_type": "房地产", "status": "active", "created_at": _SEED_DT},
    ]

    # 4. 成本科目维表数据
    cost_subjects = [
        {"subject_id": "CS001", "subject_code": "LB", "subject_name": "人工费", "subject_level": 1, "parent_id": "", "status": "active", "created_at": _SEED_DT},
        {"subject_id": "CS002", "subject_code": "CL", "subject_name": "材料费", "subject_level": 1, "parent_id": "", "status": "active", "created_at": _SEED_DT},
        {"subject_id": "CS003", "subject_code": "JX", "subject_name": "机械费", "subject_level": 1, "parent_id": "", "status": "active", "created_at": _SEED_DT},
        {"subject_id": "CS004", "subject_code": "QT", "subject_name": "其他费用", "subject_level": 1, "parent_id": "", "status": "active", "created_at": _SEED_DT},
        {"subject_id": "CS005", "subject_code": "LB01", "subject_name": "管理人员工资", "subject_level": 2, "parent_id": "CS001", "status": "active", "created_at": _SEED_DT},
        {"subject_id": "CS006", "subject_code": "CL01", "subject_name": "钢材", "subject_level": 2, "parent_id": "CS002", "status": "active", "created_at": _SEED_DT},
    ]

    # 5. 公司维表数据
    companies = [
        {"company_id": "C001", "company_code": "PDJT", "company_name": "潘达建工集团", "status": "active", "created_at": _SEED_DT},
        {"company_id": "C002", "company_code": "PDGD", "company_name": "潘达广东分公司", "status": "active", "created_at": _SEED_DT},
        {"company_id": "C003", "company_code": "PDBJ", "company_name": "潘达北京分公司", "status": "active", "created_at": _SEED_DT},
        {"company_id": "C004", "company_code": "PDSH", "company_name": "潘达上海分公司", "status": "active", "created_at": _SEED_DT},
    ]

    # 6. 供应商维表数据
    suppliers = [
        {"supplier_id": "S001", "supplier_code": "HBGC", "supplier_name": "河北钢铁集团", "status": "active", "created_at": _SEED_DT},
        {"supplier_id": "S002", "supplier_code": "SHNJ", "supplier_name": "上海水泥", "status": "active", "created_at": _SEED_DT},
        {"supplier_id": "S003", "supplier_code": "GDGC", "supplier_name": "广东建工机械", "status": "active", "created_at": _SEED_DT},
        {"supplier_id": "S004", "supplier_code": "BJGS", "supplier_name": "北京钢构", "status": "active", "created_at": _SEED_DT},
        {"supplier_id": "S005", "supplier_code": "HZAL", "supplier_name": "杭州铝材", "status": "active", "created_at": _SEED_DT},
    ]

    # 7. 项目维表数据
    projects = [
        {"project_id": "P001", "project_code": "GZ-2025-001", "project_name": "广州天河CBD项目", "company_id": "C002", "company_name": "潘达广东分公司", "section_id": "S01", "section_name": "一期", "building_area": 120000.0, "contract_amount": 580000000.0, "project_type": "商业综合体", "status": "在建", "created_at": _SEED_DT, "updated_at": _SEED_DT},
        {"project_id": "P002", "project_code": "BJ-2025-002", "project_name": "北京望京SOHO", "company_id": "C003", "company_name": "潘达北京分公司", "section_id": "S01", "section_name": "主楼", "building_area": 85000.0, "contract_amount": 420000000.0, "project_type": "办公楼", "status": "在建", "created_at": _SEED_DT, "updated_at": _SEED_DT},
        {"project_id": "P003", "project_code": "SH-2025-003", "project_name": "上海浦东住宅项目", "company_id": "C004", "company_name": "潘达上海分公司", "section_id": "S01", "section_name": "一期", "building_area": 200000.0, "contract_amount": 680000000.0, "project_type": "住宅", "status": "在建", "created_at": _SEED_DT, "updated_at": _SEED_DT},
        {"project_id": "P004", "project_code": "GZ-2025-004", "project_name": "广州白云机场配套", "company_id": "C002", "company_name": "潘达广东分公司", "section_id": "S01", "section_name": "航站楼", "building_area": 65000.0, "contract_amount": 320000000.0, "project_type": "公共建筑", "status": "完工", "created_at": _SEED_DT, "updated_at": _SEED_DT},
        {"project_id": "P005", "project_code": "HZ-2025-005", "project_name": "杭州滨江住宅", "company_id": "C001", "company_name": "潘达建工集团", "section_id": "S01", "section_name": "二期", "building_area": 150000.0, "contract_amount": 520000000.0, "project_type": "住宅", "status": "在建", "created_at": _SEED_DT, "updated_at": _SEED_DT},
    ]
    project_map = {p["project_id"]: p for p in projects}

    # 8. 合同维表数据
    contracts = [
        {"contract_id": "CT001", "contract_code": "HT-GZ-001", "contract_name": "广州天河CBD总包合同", "project_id": "P001", "contract_amount": 580000000.0, "status": "active", "created_at": _SEED_DT},
        {"contract_id": "CT002", "contract_code": "HT-BJ-001", "contract_name": "北京望京SOHO总包", "project_id": "P002", "contract_amount": 420000000.0, "status": "active", "created_at": _SEED_DT},
        {"contract_id": "CT003", "contract_code": "HT-SH-001", "contract_name": "上海浦东住宅总包", "project_id": "P003", "contract_amount": 680000000.0, "status": "active", "created_at": _SEED_DT},
        {"contract_id": "CT004", "contract_code": "HT-GZ-002", "contract_name": "白云机场配套合同", "project_id": "P004", "contract_amount": 320000000.0, "status": "completed", "created_at": _SEED_DT},
        {"contract_id": "CT005", "contract_code": "HT-HZ-001", "contract_name": "杭州滨江住宅总包", "project_id": "P005", "contract_amount": 520000000.0, "status": "active", "created_at": _SEED_DT},
        {"contract_id": "CT006", "contract_code": "HT-GZ-M01", "contract_name": "天河CBD钢材采购", "project_id": "P001", "contract_amount": 85000000.0, "status": "active", "created_at": _SEED_DT},
        {"contract_id": "CT007", "contract_code": "HT-BJ-M01", "contract_name": "望京SOHO幕墙分包", "project_id": "P002", "contract_amount": 56000000.0, "status": "active", "created_at": _SEED_DT},
    ]
    contract_map = {c["contract_id"]: c for c in contracts}

    # 灌入维表
    s.sql.insert_rows("dim_region", regions)
    output.print(f"OK dim_region {len(regions)} 条")
    s.sql.insert_rows("dim_department", departments)
    output.print(f"OK dim_department {len(departments)} 条")
    s.sql.insert_rows("dim_owner", owners)
    output.print(f"OK dim_owner {len(owners)} 条")
    s.sql.insert_rows("dim_cost_subject", cost_subjects)
    output.print(f"OK dim_cost_subject {len(cost_subjects)} 条")
    s.sql.insert_rows("dim_company", companies)
    output.print(f"OK dim_company {len(companies)} 条")
    s.sql.insert_rows("dim_supplier", suppliers)
    output.print(f"OK dim_supplier {len(suppliers)} 条")
    s.sql.insert_rows("dim_project", projects)
    output.print(f"OK dim_project {len(projects)} 条")
    s.sql.insert_rows("dim_contract", contracts)
    output.print(f"OK dim_contract {len(contracts)} 条")

    # 9. 项目产值事实表数据（2025年1月至6月每月数据）
    output_rows = []
    output_seq = 1
    start_month = date(2025, 1, 1)
    for month_offset in range(6):
        current_month = start_month + timedelta(days=month_offset * 30)
        dk = _date_key(current_month)
        report_period = current_month.strftime("%Y-%m")

        for project in projects:
            base_value = project["contract_amount"] / 24  # 假设24个月完成
            month_value = base_value * (1 + random.uniform(-0.1, 0.2))
            
            confirmed_ratio = random.uniform(0.6, 0.9)
            confirmed = month_value * confirmed_ratio
            pending = month_value * (1 - confirmed_ratio)
            tax = month_value * 0.09  # 9%税率
            
            output_rows.append({
                "id": f"OUT{output_seq:06d}",
                "project_id": project["project_id"],
                "date_key": dk,
                "report_period": report_period,
                "output_value": round(month_value, 2),
                "output_tax": round(tax, 2),
                "output_without_tax": round(month_value - tax, 2),
                "output_type": "进度产值",
                "output_ratio": round(random.uniform(0.02, 0.06), 4),
                "confirm_type": "已确认" if random.random() > 0.3 else "待确认",
                "confirmed_output": round(confirmed, 2),
                "pending_output": round(pending, 2),
                "created_at": datetime.combine(current_month, datetime.min.time()),
            })
            output_seq += 1

    out_inserted = s.sql.insert_rows("fact_project_output", output_rows)
    output.print(f"OK fact_project_output 插入 {out_inserted} 行")

    # 10. 项目成本事实表数据
    cost_rows = []
    cost_seq = 1
    for month_offset in range(6):
        current_month = start_month + timedelta(days=month_offset * 30)
        dk = _date_key(current_month)
        report_period = current_month.strftime("%Y-%m")

        for project in projects:
            cost_amount = project["contract_amount"] * random.uniform(0.015, 0.025)
            labor_ratio = random.uniform(0.2, 0.35)
            material_ratio = random.uniform(0.4, 0.55)
            mechanical_ratio = random.uniform(0.1, 0.15)
            other_ratio = 1 - labor_ratio - material_ratio - mechanical_ratio

            labor = cost_amount * labor_ratio
            material = cost_amount * material_ratio
            mechanical = cost_amount * mechanical_ratio
            other = cost_amount * other_ratio
            
            target_cost = cost_amount * random.uniform(0.95, 1.05)
            variance = cost_amount - target_cost

            cost_rows.append({
                "id": f"COST{cost_seq:06d}",
                "project_id": project["project_id"],
                "contract_id": random.choice([c["contract_id"] for c in contracts if c["project_id"] == project["project_id"]]),
                "date_key": dk,
                "report_period": report_period,
                "cost_amount": round(cost_amount, 2),
                "cost_type": "直接成本",
                "cost_level1": "主控费用",
                "cost_level2": "分项费用",
                "cost_level3": "明细费用",
                "labor_cost": round(labor, 2),
                "material_cost": round(material, 2),
                "mechanical_cost": round(mechanical, 2),
                "other_cost": round(other, 2),
                "target_cost": round(target_cost, 2),
                "variance_amount": round(variance, 2),
                "variance_ratio": round(variance / target_cost if target_cost != 0 else 0, 4),
                "created_at": datetime.combine(current_month, datetime.min.time()),
            })
            cost_seq += 1

    cost_inserted = s.sql.insert_rows("fact_project_cost", cost_rows)
    output.print(f"OK fact_project_cost 插入 {cost_inserted} 行")

    # 11. 项目指标事实表数据
    indicator_rows = []
    indicator_seq = 1
    for month_offset in range(6):
        current_month = start_month + timedelta(days=month_offset * 30)
        dk = _date_key(current_month)
        report_period = current_month.strftime("%Y-%m")

        for project in projects:
            gross_profit = random.uniform(0.12, 0.22)
            collection = random.uniform(0.65, 0.92)
            receivable = random.uniform(0.55, 0.85)
            cost_variance = random.uniform(-0.1, 0.1)
            payment = random.uniform(0.5, 0.85)

            indicator_rows.append({
                "id": f"IND{indicator_seq:06d}",
                "project_id": project["project_id"],
                "company_id": project["company_id"],
                "date_key": dk,
                "report_period": report_period,
                "indicator_code": "KPI001",
                "indicator_name": "综合指标",
                "indicator_value": round(gross_profit * 100, 2),
                "target_value": 18.0,
                "actual_value": round(gross_profit * 100, 2),
                "variance_value": round((gross_profit - 0.18) * 100, 2),
                "variance_ratio": round((gross_profit - 0.18) / 0.18, 4),
                "gross_profit_rate": round(gross_profit, 4),
                "collection_rate": round(collection, 4),
                "receivable_recovery_rate": round(receivable, 4),
                "cost_variance_rate": round(cost_variance, 4),
                "payment_ratio": round(payment, 4),
                "created_at": datetime.combine(current_month, datetime.min.time()),
            })
            indicator_seq += 1

    ind_inserted = s.sql.insert_rows("fact_project_indicator", indicator_rows)
    output.print(f"OK fact_project_indicator 插入 {ind_inserted} 行")

    # 12. 项目付款事实表数据
    payment_rows = []
    payment_seq = 1
    for month_offset in range(6):
        current_month = start_month + timedelta(days=month_offset * 30)
        dk = _date_key(current_month)
        report_period = current_month.strftime("%Y-%m")

        for project in projects:
            payable = project["contract_amount"] * random.uniform(0.02, 0.04)
            paid_ratio = random.uniform(0.5, 0.9)
            paid = payable * paid_ratio
            unpaid = payable * (1 - paid_ratio)

            payment_rows.append({
                "id": f"PAY{payment_seq:06d}",
                "project_id": project["project_id"],
                "contract_id": random.choice([c["contract_id"] for c in contracts if c["project_id"] == project["project_id"]]),
                "date_key": dk,
                "report_period": report_period,
                "payable_amount": round(payable, 2),
                "paid_amount": round(paid, 2),
                "unpaid_amount": round(unpaid, 2),
                "approval_status": "已批准" if random.random() > 0.1 else "审批中",
                "approval_amount": round(payable * random.uniform(0.8, 1.0), 2),
                "payment_type": "进度款",
                "payment_ratio": round(paid_ratio, 4),
                "created_at": datetime.combine(current_month, datetime.min.time()),
            })
            payment_seq += 1

    pay_inserted = s.sql.insert_rows("fact_project_payment", payment_rows)
    output.print(f"OK fact_project_payment 插入 {pay_inserted} 行")

    # 13. 项目收支事实表数据
    balance_rows = []
    balance_seq = 1
    for month_offset in range(6):
        current_month = start_month + timedelta(days=month_offset * 30)
        dk = _date_key(current_month)
        report_period = current_month.strftime("%Y-%m")

        for project in projects:
            for balance_type in ["收入", "支出"]:
                if balance_type == "收入":
                    amount = project["contract_amount"] * random.uniform(0.02, 0.05)
                else:
                    amount = project["contract_amount"] * random.uniform(0.018, 0.045)

                balance_rows.append({
                    "id": f"BAL{balance_seq:06d}",
                    "project_id": project["project_id"],
                    "date_key": dk,
                    "report_period": report_period,
                    "subject_code": "SR" if balance_type == "收入" else "ZC",
                    "subject_name": "主营业务收入" if balance_type == "收入" else "主营业务成本",
                    "project_amount": round(amount * 0.8, 2),
                    "company_amount": round(amount * 0.2, 2),
                    "total_amount": round(amount, 2),
                    "balance_type": balance_type,
                    "created_at": datetime.combine(current_month, datetime.min.time()),
                })
                balance_seq += 1

    bal_inserted = s.sql.insert_rows("fact_project_balance", balance_rows)
    output.print(f"OK fact_project_balance 插入 {bal_inserted} 行")

    # 14. 项目风险事实表数据
    risk_rows = []
    risk_seq = 1
    risk_types = ["成本风险", "进度风险", "质量风险", "安全风险", "资金风险"]
    warning_levels = ["绿色", "黄色", "红色"]
    
    for month_offset in range(3):  # 每两个月一条风险记录
        current_month = start_month + timedelta(days=month_offset * 60)
        dk = _date_key(current_month)
        report_period = current_month.strftime("%Y-%m")

        for project in projects:
            if random.random() > 0.3:  # 70%概率有风险
                risk_type = random.choice(risk_types)
                level = random.choices(warning_levels, weights=[0.5, 0.35, 0.15])[0]
                
                if level == "红色":
                    score = random.uniform(70, 100)
                elif level == "黄色":
                    score = random.uniform(40, 70)
                else:
                    score = random.uniform(10, 40)

                risk_rows.append({
                    "id": f"RISK{risk_seq:06d}",
                    "project_id": project["project_id"],
                    "date_key": dk,
                    "report_period": report_period,
                    "risk_type": risk_type,
                    "risk_code": f"RK-{risk_type[:2]}-{risk_seq}",
                    "risk_name": f"{project['project_name']}{risk_type}",
                    "risk_score": round(score, 2),
                    "warning_level": level,
                    "warning_reason": f"{risk_type}预警",
                    "risk_description": f"{project['project_name']}存在{risk_type}风险",
                    "response_measure": "加强监控",
                    "created_at": datetime.combine(current_month, datetime.min.time()),
                })
                risk_seq += 1

    risk_inserted = s.sql.insert_rows("fact_project_risk", risk_rows)
    output.print(f"OK fact_project_risk 插入 {risk_inserted} 行")

    summary = {
        "ok": True,
        "space_id": space_id,
        "regions": len(regions),
        "departments": len(departments),
        "owners": len(owners),
        "cost_subjects": len(cost_subjects),
        "companies": len(companies),
        "suppliers": len(suppliers),
        "projects": len(projects),
        "contracts": len(contracts),
        "output_inserted": out_inserted,
        "cost_inserted": cost_inserted,
        "indicator_inserted": ind_inserted,
        "payment_inserted": pay_inserted,
        "balance_inserted": bal_inserted,
        "risk_inserted": risk_inserted,
    }
    output.success("灌数完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))