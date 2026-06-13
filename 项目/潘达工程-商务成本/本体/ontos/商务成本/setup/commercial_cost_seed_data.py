"""商务成本本体灌数脚本

前置：先执行 commercial_cost_ontology_init.py 建表
幂等：已有数据则跳过

放置：项目/潘达工程-商务成本/本体/ontos/商务成本/setup/commercial_cost_seed_data.py
发布：dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/商务成本/setup/commercial_cost_seed_data.py --space space__panda_construction --type data
"""

import json
import random
from datetime import datetime, timedelta


def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)

    output.print("=== 商务成本本体数据灌入 ===")

    # 检查是否已有数据
    try:
        n = int(s.sql.query_one("SELECT count() FROM dim_project") or 0)
    except Exception:
        n = 0
    if n > 0:
        output.print(f"dim_project 已有 {n} 行，跳过灌数")
        output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "skipped": True, "rows": n}, ensure_ascii=True))
        return

    random.seed(8806)

    # ==================== 时间维度数据 ====================
    date_data = []
    start_date = datetime(2024, 1, 1)
    for i in range(730):  # 2年数据
        d = start_date + timedelta(days=i)
        date_data.append({
            "date_key": int(d.strftime("%Y%m%d")),
            "calendar_date": d.date(),
            "year": d.year,
            "quarter": (d.month - 1) // 3 + 1,
            "month": d.month,
            "week_of_year": int(d.strftime("%W")),
            "day_of_week": d.weekday() + 1,
            "is_weekend": 1 if d.weekday() >= 5 else 0,
            "year_month": d.strftime("%Y-%m"),
            "fiscal_year": d.year if d.month >= 4 else d.year - 1,
            "fiscal_period": (d.month - 4) % 12 + 1 if d.month >= 4 else d.month + 9,
        })
    s.sql.insert_rows("dim_date", date_data)
    output.print("OK dim_date")

    # ==================== 地区维度数据 ====================
    region_data = [
        {"region_key": "R001", "region_code": "BJ", "region_name": "北京", "parent_key": "", "region_level": 1, "is_leaf": 0},
        {"region_key": "R002", "region_code": "SH", "region_name": "上海", "parent_key": "", "region_level": 1, "is_leaf": 0},
        {"region_key": "R003", "region_code": "GD", "region_name": "广东", "parent_key": "", "region_level": 1, "is_leaf": 0},
        {"region_key": "R004", "region_code": "ZS", "region_name": "中山", "parent_key": "R003", "region_level": 2, "is_leaf": 1},
        {"region_key": "R005", "region_code": "SZ", "region_name": "深圳", "parent_key": "R003", "region_level": 2, "is_leaf": 1},
        {"region_key": "R006", "region_code": "GZ", "region_name": "广州", "parent_key": "R003", "region_level": 2, "is_leaf": 1},
        {"region_key": "R007", "region_code": "CD", "region_name": "成都", "parent_key": "", "region_level": 1, "is_leaf": 0},
        {"region_key": "R008", "region_code": "SC", "region_name": "四川", "parent_key": "", "region_level": 1, "is_leaf": 0},
        {"region_key": "R009", "region_code": "CDQ", "region_name": "成都区", "parent_key": "R008", "region_level": 2, "is_leaf": 1},
        {"region_key": "R010", "region_code": "CY", "region_name": "朝阳", "parent_key": "R001", "region_level": 2, "is_leaf": 1},
    ]
    s.sql.insert_rows("dim_region", region_data)
    output.print("OK dim_region")

    # ==================== 组织维度数据 ====================
    org_data = [
        {"organization_key": "O001", "organization_code": "HQ", "organization_name": "总部", "parent_key": "", "org_level": 1, "is_leaf": 0},
        {"organization_key": "O002", "organization_code": "BJ", "organization_name": "北京分公司", "parent_key": "O001", "org_level": 2, "is_leaf": 0},
        {"organization_key": "O003", "organization_code": "SH", "organization_name": "上海分公司", "parent_key": "O001", "org_level": 2, "is_leaf": 0},
        {"organization_key": "O004", "organization_code": "GD", "organization_name": "广东分公司", "parent_key": "O001", "org_level": 2, "is_leaf": 0},
        {"organization_key": "O005", "organization_code": "ZS", "organization_name": "中山项目部", "parent_key": "O004", "org_level": 3, "is_leaf": 1},
        {"organization_key": "O006", "organization_code": "SZ", "organization_name": "深圳项目部", "parent_key": "O004", "org_level": 3, "is_leaf": 1},
        {"organization_key": "O007", "organization_code": "GZ", "organization_name": "广州项目部", "parent_key": "O004", "org_level": 3, "is_leaf": 1},
        {"organization_key": "O008", "organization_code": "CD", "organization_name": "成都分公司", "parent_key": "O001", "org_level": 2, "is_leaf": 0},
        {"organization_key": "O009", "organization_code": "CDQ", "organization_name": "成都区项目组", "parent_key": "O008", "org_level": 3, "is_leaf": 1},
        {"organization_key": "O010", "organization_code": "CY", "organization_name": "朝阳项目组", "parent_key": "O002", "org_level": 3, "is_leaf": 1},
    ]
    s.sql.insert_rows("dim_organization", org_data)
    output.print("OK dim_organization")

    # ==================== 成本科目维度数据 ====================
    subject_data = [
        {"cost_subject_key": "S001", "subject_code": "CB", "subject_name": "成本", "subject_level": 1, "parent_key": "", "subject_type": "一级", "is_leaf": 0},
        {"cost_subject_key": "S002", "subject_code": "CB-01", "subject_name": "直接成本", "subject_level": 2, "parent_key": "S001", "subject_type": "二级", "is_leaf": 0},
        {"cost_subject_key": "S003", "subject_code": "CB-02", "subject_name": "间接成本", "subject_level": 2, "parent_key": "S001", "subject_type": "二级", "is_leaf": 0},
        {"cost_subject_key": "S004", "subject_code": "CB-01-01", "subject_name": "人工成本", "subject_level": 3, "parent_key": "S002", "subject_type": "三级", "is_leaf": 1},
        {"cost_subject_key": "S005", "subject_code": "CB-01-02", "subject_name": "材料成本", "subject_level": 3, "parent_key": "S002", "subject_type": "三级", "is_leaf": 1},
        {"cost_subject_key": "S006", "subject_code": "CB-01-03", "subject_name": "机械费用", "subject_level": 3, "parent_key": "S002", "subject_type": "三级", "is_leaf": 1},
        {"cost_subject_key": "S007", "subject_code": "CB-02-01", "subject_name": "管理费用", "subject_level": 3, "parent_key": "S003", "subject_type": "三级", "is_leaf": 1},
        {"cost_subject_key": "S008", "subject_code": "CB-02-02", "subject_name": "财务费用", "subject_level": 3, "parent_key": "S003", "subject_type": "三级", "is_leaf": 1},
        {"cost_subject_key": "S009", "subject_code": "CB-02-03", "subject_name": "税费", "subject_level": 3, "parent_key": "S003", "subject_type": "三级", "is_leaf": 1},
        {"cost_subject_key": "S010", "subject_code": "CB-01-04", "subject_name": "分包成本", "subject_level": 3, "parent_key": "S002", "subject_type": "三级", "is_leaf": 1},
    ]
    s.sql.insert_rows("dim_cost_subject", subject_data)
    output.print("OK dim_cost_subject")

    # ==================== 项目类别维度数据 ====================
    category_data = [
        {"project_category_key": "PC001", "category_type": "project_type", "category_code": "HT", "category_name": "合同项目", "parent_key": "", "level": 1, "is_leaf": 0},
        {"project_category_key": "PC002", "category_type": "project_type", "category_code": "ZC", "category_name": "总承包", "parent_key": "PC001", "level": 2, "is_leaf": 1},
        {"project_category_key": "PC003", "category_type": "project_type", "category_code": "FB", "category_name": "分包", "parent_key": "PC001", "level": 2, "is_leaf": 1},
        {"project_category_key": "PC004", "category_type": "project_type", "category_code": "GL", "category_name": "挂靠", "parent_key": "PC001", "level": 2, "is_leaf": 1},
        {"project_category_key": "PC005", "category_type": "project_category", "category_code": "JG", "category_name": "建工", "parent_key": "", "level": 1, "is_leaf": 0},
        {"project_category_key": "PC006", "category_type": "project_category", "category_code": "JG-01", "category_name": "房建", "parent_key": "PC005", "level": 2, "is_leaf": 1},
        {"project_category_key": "PC007", "category_type": "project_category", "category_code": "JG-02", "category_name": "市政", "parent_key": "PC005", "level": 2, "is_leaf": 1},
        {"project_category_key": "PC008", "category_type": "project_category", "category_code": "JG-03", "category_name": "公路", "parent_key": "PC005", "level": 2, "is_leaf": 1},
        {"project_category_key": "PC009", "category_type": "project_category", "category_code": "JG-04", "category_name": "桥梁", "parent_key": "PC005", "level": 2, "is_leaf": 1},
        {"project_category_key": "PC010", "category_type": "project_category", "category_code": "JG-05", "category_name": "隧道", "parent_key": "PC005", "level": 2, "is_leaf": 1},
    ]
    s.sql.insert_rows("dim_project_category", category_data)
    output.print("OK dim_project_category")

    # ==================== 经营模式维度数据 ====================
    cooperation_data = [
        {"cooperation_key": "CP001", "cooperation_code": "ZC", "cooperation_name": "总承包", "is_active": 1},
        {"cooperation_key": "CP002", "cooperation_code": "FB", "cooperation_name": "专业分包", "is_active": 1},
        {"cooperation_key": "CP003", "cooperation_code": "GL", "cooperation_name": "挂靠", "is_active": 1},
        {"cooperation_key": "CP004", "cooperation_code": "LH", "cooperation_name": "联合投标", "is_active": 1},
        {"cooperation_key": "CP005", "cooperation_code": "BT", "cooperation_name": "BT模式", "is_active": 1},
        {"cooperation_key": "CP006", "cooperation_code": "PPP", "cooperation_name": "PPP模式", "is_active": 1},
    ]
    s.sql.insert_rows("dim_cooperation", cooperation_data)
    output.print("OK dim_cooperation")

    # ==================== 客户/业主维度数据 ====================
    owner_data = [
        {"owner_key": "OW001", "owner_code": "YZH001", "owner_name": "远洋地产", "owner_type": "房地产", "credit_level": "A", "region_key": "R001"},
        {"owner_key": "OW002", "owner_code": "WY001", "owner_name": "万科集团", "owner_type": "房地产", "credit_level": "A", "region_key": "R003"},
        {"owner_key": "OW003", "owner_code": "LD001", "owner_name": "绿地集团", "owner_type": "房地产", "credit_level": "A", "region_key": "R002"},
        {"owner_key": "OW004", "owner_code": "ZS001", "owner_name": "中山市住建局", "owner_type": "政府", "credit_level": "A+", "region_key": "R004"},
        {"owner_key": "OW005", "owner_code": "SZ001", "owner_name": "深圳市交委", "owner_type": "政府", "credit_level": "A+", "region_key": "R005"},
        {"owner_key": "OW006", "owner_code": "CD001", "owner_name": "成都城投", "owner_type": "国企", "credit_level": "A", "region_key": "R007"},
    ]
    s.sql.insert_rows("dim_owner", owner_data)
    output.print("OK dim_owner")

    client_data = [
        {"client_key": "CL001", "client_code": "YLDC", "client_name": "远洋地产", "client_type": "房地产", "credit_level": "A", "region_key": "R001", "is_key_client": 1},
        {"client_key": "CL002", "client_code": "WKJT", "client_name": "万科集团", "client_type": "房地产", "credit_level": "A", "region_key": "R003", "is_key_client": 1},
        {"client_key": "CL003", "client_code": "LDJT", "client_name": "绿地集团", "client_type": "房地产", "credit_level": "A", "region_key": "R002", "is_key_client": 1},
        {"client_key": "CL004", "client_code": "ZSZJJ", "client_name": "中山市住建局", "client_type": "政府", "credit_level": "A+", "region_key": "R004", "is_key_client": 1},
        {"client_key": "CL005", "client_code": "SZJWW", "client_name": "深圳市交委", "client_type": "政府", "credit_level": "A+", "region_key": "R005", "is_key_client": 1},
        {"client_key": "CL006", "client_code": "CDCT", "client_name": "成都城投", "client_type": "国企", "credit_level": "A", "region_key": "R007", "is_key_client": 0},
    ]
    s.sql.insert_rows("dim_client", client_data)
    output.print("OK dim_client")

    # ==================== 合同类型维度数据 ====================
    contract_type_data = [
        {"contract_type_key": "CT001", "contract_type_code": "HT-ZC", "contract_type_name": "总承包合同", "description": "项目总承包合同"},
        {"contract_type_key": "CT002", "contract_type_code": "HT-FB", "contract_type_name": "分包合同", "description": "专业分包合同"},
        {"contract_type_key": "CT003", "contract_type_code": "HT-CL", "contract_type_name": "材料采购合同", "description": "建筑材料采购"},
        {"contract_type_key": "CT004", "contract_type_code": "HT-JX", "contract_type_name": "机械租赁合同", "description": "机械设备租赁"},
        {"contract_type_key": "CT005", "contract_type_code": "HT-GC", "contract_type_name": "工程劳务合同", "description": "劳务分包"},
    ]
    s.sql.insert_rows("dim_contract_type", contract_type_data)
    output.print("OK dim_contract_type")

    # ==================== 项目状态维度数据 ====================
    project_status_data = [
        {"project_status_key": "PS001", "project_status_code": "QL", "project_status_name": "立项", "status_order": 1, "is_active": 1},
        {"project_status_key": "PS002", "project_status_code": "KAI", "project_status_name": "开工", "status_order": 2, "is_active": 1},
        {"project_status_key": "PS003", "project_status_code": "JZ", "project_status_name": "在建", "status_order": 3, "is_active": 1},
        {"project_status_key": "PS004", "project_status_code": "JS", "project_status_name": "竣工", "status_order": 4, "is_active": 1},
        {"project_status_key": "PS005", "project_status_code": "YSS", "project_status_name": "验收", "status_order": 5, "is_active": 1},
        {"project_status_key": "PS006", "project_status_code": "WC", "project_status_name": "完成", "status_order": 6, "is_active": 1},
    ]
    s.sql.insert_rows("dim_project_status", project_status_data)
    output.print("OK dim_project_status")

    # ==================== 合同状态维度数据 ====================
    contract_status_data = [
        {"contract_status_key": "CS001", "contract_status_code": "QD", "contract_status_name": "签订", "status_order": 1, "is_active": 1},
        {"contract_status_key": "CS002", "contract_status_code": "ZX", "contract_status_name": "执行中", "status_order": 2, "is_active": 1},
        {"contract_status_key": "CS003", "contract_status_code": "HF", "contract_status_name": "回款中", "status_order": 3, "is_active": 1},
        {"contract_status_key": "CS004", "contract_status_code": "WC", "contract_status_name": "完成", "status_order": 4, "is_active": 1},
        {"contract_status_key": "CS005", "contract_status_code": "CX", "contract_status_name": "撤销", "status_order": 5, "is_active": 0},
    ]
    s.sql.insert_rows("dim_contract_status", contract_status_data)
    output.print("OK dim_contract_status")

    # ==================== 风险等级维度数据 ====================
    risk_level_data = [
        {"risk_level_key": "RL001", "risk_level_code": "G", "risk_level_name": "高风险", "risk_level_value": 3, "threshold_min": 70, "threshold_max": 100},
        {"risk_level_key": "RL002", "risk_level_code": "Z", "risk_level_name": "中风险", "risk_level_value": 2, "threshold_min": 30, "threshold_max": 70},
        {"risk_level_key": "RL003", "risk_level_code": "D", "risk_level_name": "低风险", "risk_level_value": 1, "threshold_min": 0, "threshold_max": 30},
    ]
    s.sql.insert_rows("dim_risk_level", risk_level_data)
    output.print("OK dim_risk_level")

    # ==================== 项目主数据 ====================
    project_data = [
        {"project_key": "P001", "project_code": "GD-ZS-2024-001", "project_name": "中山远洋城住宅项目", "project_type": "ZC", "project_category": "JG-01", "business_model": "ZC", "contract_amount": 500000000, "management_fee_rate": 0.03, "project_status": "JZ", "start_date": datetime(2024, 1, 15).date(), "end_date": datetime(2026, 6, 30).date(), "region_key": "R004", "organization_key": "O005", "project_manager": "张三", "is_key_client": 1, "is_new_increment": 1},
        {"project_key": "P002", "project_code": "GD-SZ-2024-002", "project_name": "深圳前海市政道路工程", "project_type": "ZC", "project_category": "JG-02", "business_model": "ZC", "contract_amount": 320000000, "management_fee_rate": 0.04, "project_status": "JZ", "start_date": datetime(2024, 3, 1).date(), "end_date": datetime(2025, 12, 31).date(), "region_key": "R005", "organization_key": "O006", "project_manager": "李四", "is_key_client": 1, "is_new_increment": 1},
        {"project_key": "P003", "project_code": "GD-GZ-2024-003", "project_name": "广州绿地中心写字楼", "project_type": "ZC", "project_category": "JG-01", "business_model": "ZC", "contract_amount": 800000000, "management_fee_rate": 0.03, "project_status": "KAI", "start_date": datetime(2024, 5, 1).date(), "end_date": datetime(2027, 12, 31).date(), "region_key": "R006", "organization_key": "O007", "project_manager": "王五", "is_key_client": 1, "is_new_increment": 1},
        {"project_key": "P004", "project_code": "BJ-CY-2024-004", "project_name": "北京朝阳商业综合体", "project_type": "ZC", "project_category": "JG-01", "business_model": "ZC", "contract_amount": 1200000000, "management_fee_rate": 0.025, "project_status": "JZ", "start_date": datetime(2023, 10, 1).date(), "end_date": datetime(2026, 9, 30).date(), "region_key": "R010", "organization_key": "O010", "project_manager": "赵六", "is_key_client": 1, "is_new_increment": 0},
        {"project_key": "P005", "project_code": "SH-PD-2024-005", "project_name": "上海浦东科技园项目", "project_type": "FB", "project_category": "JG-01", "business_model": "FB", "contract_amount": 200000000, "management_fee_rate": 0.05, "project_status": "JZ", "start_date": datetime(2024, 2, 1).date(), "end_date": datetime(2025, 8, 31).date(), "region_key": "R002", "organization_key": "O003", "project_manager": "孙七", "is_key_client": 0, "is_new_increment": 1},
        {"project_key": "P006", "project_code": "CD-CD-2024-006", "project_name": "成都天府新区道路工程", "project_type": "ZC", "project_category": "JG-02", "business_model": "ZC", "contract_amount": 450000000, "management_fee_rate": 0.035, "project_status": "KAI", "start_date": datetime(2024, 4, 1).date(), "end_date": datetime(2026, 3, 31).date(), "region_key": "R009", "organization_key": "O009", "project_manager": "周八", "is_key_client": 1, "is_new_increment": 1},
        {"project_key": "P007", "project_code": "GD-ZS-2023-007", "project_name": "中山南区保障房项目", "project_type": "ZC", "project_category": "JG-01", "business_model": "ZC", "contract_amount": 180000000, "management_fee_rate": 0.04, "project_status": "JS", "start_date": datetime(2023, 6, 1).date(), "end_date": datetime(2024, 12, 31).date(), "region_key": "R004", "organization_key": "O005", "project_manager": "吴九", "is_key_client": 0, "is_new_increment": 0},
        {"project_key": "P008", "project_code": "GD-SZ-2023-008", "project_name": "深圳地铁14号线附属工程", "project_type": "FB", "project_category": "JG-03", "business_model": "FB", "contract_amount": 150000000, "management_fee_rate": 0.06, "project_status": "JS", "start_date": datetime(2023, 3, 1).date(), "end_date": datetime(2024, 6, 30).date(), "region_key": "R005", "organization_key": "O006", "project_manager": "郑十", "is_key_client": 1, "is_new_increment": 0},
    ]
    s.sql.insert_rows("dim_project", project_data)
    output.print("OK dim_project")

    # ==================== 合同主数据 ====================
    contract_data = [
        {"contract_key": "C001", "contract_code": "HT-ZS-2024-001", "contract_name": "中山远洋城总包合同", "project_key": "P001", "contract_type": "HT-ZC", "contract_amount": 500000000, "sign_date": datetime(2023, 12, 15).date(), "contract_status": "ZX", "owner_key": "OW001"},
        {"contract_key": "C002", "contract_code": "HT-SZ-2024-002", "contract_name": "深圳前海道路工程合同", "project_key": "P002", "contract_type": "HT-ZC", "contract_amount": 320000000, "sign_date": datetime(2024, 2, 20).date(), "contract_status": "ZX", "owner_key": "OW005"},
        {"contract_key": "C003", "contract_code": "HT-GZ-2024-003", "contract_name": "广州绿地中心总包合同", "project_key": "P003", "contract_type": "HT-ZC", "contract_amount": 800000000, "sign_date": datetime(2024, 4, 10).date(), "contract_status": "QD", "owner_key": "OW003"},
        {"contract_key": "C004", "contract_code": "HT-BJ-2023-004", "contract_name": "北京朝阳综合体合同", "project_key": "P004", "contract_type": "HT-ZC", "contract_amount": 1200000000, "sign_date": datetime(2023, 9, 15).date(), "contract_status": "ZX", "owner_key": "OW001"},
        {"contract_key": "C005", "contract_code": "HT-SH-2024-005", "contract_name": "上海科技园分包合同", "project_key": "P005", "contract_type": "HT-FB", "contract_amount": 200000000, "sign_date": datetime(2024, 1, 25).date(), "contract_status": "ZX", "owner_key": "OW003"},
        {"contract_key": "C006", "contract_code": "HT-CD-2024-006", "contract_name": "成都天府新区道路合同", "project_key": "P006", "contract_type": "HT-ZC", "contract_amount": 450000000, "sign_date": datetime(2024, 3, 28).date(), "contract_status": "QD", "owner_key": "OW006"},
        {"contract_key": "C007", "contract_code": "HT-ZS-2023-007", "contract_name": "中山南区保障房合同", "project_key": "P007", "contract_type": "HT-ZC", "contract_amount": 180000000, "sign_date": datetime(2023, 5, 10).date(), "contract_status": "WC", "owner_key": "OW004"},
        {"contract_key": "C008", "contract_code": "HT-SZ-2023-008", "contract_name": "深圳地铁14号线分包合同", "project_key": "P008", "contract_type": "HT-FB", "contract_amount": 150000000, "sign_date": datetime(2023, 2, 15).date(), "contract_status": "WC", "owner_key": "OW005"},
    ]
    s.sql.insert_rows("dim_contract", contract_data)
    output.print("OK dim_contract")

    # ==================== 成本事实数据 ====================
    cost_data = []
    cost_id = 1
    subjects = ["S004", "S005", "S006", "S007", "S008", "S009", "S010"]
    cost_types = ["预算成本", "实际成本", "目标成本"]

    for project in project_data:
        for month in range(1, 13):
            date_key = 20240000 + month * 100 + 15
            for subject in subjects:
                for cost_type in cost_types:
                    base_amount = random.randint(100000, 5000000)
                    cost_data.append({
                        "cost_id": f"COST{cost_id:06d}",
                        "date_key": date_key,
                        "calendar_date": datetime(2024, month, 15).date(),
                        "project_key": project["project_key"],
                        "cost_subject_key": subject,
                        "subject_code": subject,
                        "subject_name": subject,
                        "subject_level": 3,
                        "cost_amount": base_amount,
                        "cost_type": cost_type,
                        "contract_key": "",
                        "region_key": project.get("region_key"),
                        "organization_key": project.get("organization_key"),
                    })
                    cost_id += 1
                    if len(cost_data) >= 1000:
                        break
                if len(cost_data) >= 1000:
                    break
            if len(cost_data) >= 1000:
                break
        if len(cost_data) >= 1000:
            break

    s.sql.insert_rows("fact_project_cost", cost_data[:1000])
    output.print(f"OK fact_project_cost ({len(cost_data[:1000])} rows)")

    # ==================== 产值事实数据 ====================
    output_data = []
    output_id = 1
    for project in project_data:
        for month in range(1, 13):
            date_key = 20240000 + month * 100 + 15
            base_amount = random.randint(500000, 10000000)
            output_data.append({
                "output_id": f"OUT{output_id:06d}",
                "date_key": date_key,
                "calendar_date": datetime(2024, month, 15).date(),
                "project_key": project["project_key"],
                "output_amount": base_amount,
                "output_type": "完成产值",
                "confirmation_status": "已确认",
                "contract_key": "",
                "region_key": project.get("region_key", ""),
                "organization_key": project.get("organization_key", ""),
            })
            output_id += 1

    s.sql.insert_rows("fact_project_output", output_data)
    output.print(f"OK fact_project_output ({len(output_data)} rows)")

    # ==================== 付款事实数据 ====================
    payment_data = []
    payment_id = 1
    for contract in contract_data:
        for month in range(1, 13):
            date_key = 20240000 + month * 100 + 15
            base_amount = random.randint(100000, 5000000)
            payment_data.append({
                "payment_id": f"PAY{payment_id:06d}",
                "date_key": date_key,
                "calendar_date": datetime(2024, month, 15).date(),
                "project_key": contract["project_key"],
                "contract_key": contract["contract_key"],
                "payment_amount": base_amount,
                "payment_type": random.choice(["进度款", "结算款", "预付款"]),
                "payment_status": random.choice(["已支付", "待支付", "部分支付"]),
                "supplier_key": "",
                "region_key": "",
                "organization_key": "",
            })
            payment_id += 1

    s.sql.insert_rows("fact_payment", payment_data)
    output.print(f"OK fact_payment ({len(payment_data)} rows)")

    # ==================== 应收事实数据 ====================
    receivable_data = []
    receivable_id = 1
    for contract in contract_data:
        for month in range(1, 13):
            date_key = 20240000 + month * 100 + 15
            base_amount = random.randint(100000, 5000000)
            receivable_data.append({
                "receivable_id": f"REC{receivable_id:06d}",
                "date_key": date_key,
                "calendar_date": datetime(2024, month, 15).date(),
                "project_key": contract["project_key"],
                "contract_key": contract["contract_key"],
                "receivable_amount": base_amount,
                "receivable_type": random.choice(["工程款", "质保金", "进度款"]),
                "receivable_status": random.choice(["已收款", "待收款", "部分收款"]),
                "region_key": "",
                "organization_key": "",
            })
            receivable_id += 1

    s.sql.insert_rows("fact_receivable", receivable_data)
    output.print(f"OK fact_receivable ({len(receivable_data)} rows)")

    # ==================== 现金流事实数据 ====================
    cashflow_data = []
    cashflow_id = 1
    for project in project_data:
        for month in range(1, 13):
            date_key = 20240000 + month * 100 + 15
            inflow = random.randint(500000, 10000000)
            outflow = random.randint(300000, 8000000)
            cashflow_data.append({
                "cash_flow_id": f"CF{cashflow_id:06d}",
                "date_key": date_key,
                "calendar_date": datetime(2024, month, 15).date(),
                "project_key": project["project_key"],
                "cash_inflow": inflow,
                "cash_outflow": outflow,
                "net_cash_flow": inflow - outflow,
                "cash_type": random.choice(["经营", "投资", "筹资"]),
                "region_key": project.get("region_key", ""),
                "organization_key": project.get("organization_key", ""),
            })
            cashflow_id += 1

    s.sql.insert_rows("fact_cash_flow", cashflow_data)
    output.print(f"OK fact_cash_flow ({len(cashflow_data)} rows)")

    # ==================== 风险事实数据 ====================
    risk_data = []
    risk_id = 1
    for project in project_data:
        for month in range(1, 13):
            date_key = 20240000 + month * 100 + 15
            risk_value = random.randint(10, 90)
            risk_data.append({
                "risk_id": f"RSK{risk_id:06d}",
                "date_key": date_key,
                "calendar_date": datetime(2024, month, 15).date(),
                "project_key": project["project_key"],
                "risk_type": random.choice(["进度风险", "成本风险", "质量风险", "安全风险"]),
                "risk_value": risk_value,
                "risk_level": "G" if risk_value >= 70 else ("Z" if risk_value >= 30 else "D"),
                "region_key": project.get("region_key", ""),
                "organization_key": project.get("organization_key", ""),
            })
            risk_id += 1

    s.sql.insert_rows("fact_risk", risk_data)
    output.print(f"OK fact_risk ({len(risk_data)} rows)")

    # ==================== 变更签证事实数据 ====================
    change_data = []
    change_id = 1
    for project in project_data:
        for month in range(1, 13):
            if random.random() > 0.3:
                date_key = 20240000 + month * 100 + 15
                change_data.append({
                    "change_id": f"CHG{change_id:06d}",
                    "date_key": date_key,
                    "calendar_date": datetime(2024, month, 15).date(),
                    "project_key": project["project_key"],
                    "change_type": random.choice(["设计变更", "现场签证", "技术核定"]),
                    "change_amount": random.randint(50000, 2000000),
                    "change_reason": random.choice(["设计优化", "业主需求", "现场条件变化"]),
                    "approval_status": random.choice(["已批准", "待审批", "已拒绝"]),
                    "region_key": project.get("region_key", ""),
                    "organization_key": project.get("organization_key", ""),
                })
                change_id += 1

    s.sql.insert_rows("fact_change_order", change_data)
    output.print(f"OK fact_change_order ({len(change_data)} rows)")

    # ==================== 索赔事实数据 ====================
    claim_data = []
    claim_id = 1
    for project in project_data:
        for month in range(1, 13):
            if random.random() > 0.7:
                date_key = 20240000 + month * 100 + 15
                claim_data.append({
                    "claim_id": f"CLM{claim_id:06d}",
                    "date_key": date_key,
                    "calendar_date": datetime(2024, month, 15).date(),
                    "project_key": project["project_key"],
                    "claim_type": random.choice(["工期索赔", "费用索赔", "综合索赔"]),
                    "claim_amount": random.randint(100000, 3000000),
                    "claim_status": random.choice(["申请中", "已批准", "已拒绝"]),
                    "region_key": project.get("region_key", ""),
                    "organization_key": project.get("organization_key", ""),
                })
                claim_id += 1

    s.sql.insert_rows("fact_claim", claim_data)
    output.print(f"OK fact_claim ({len(claim_data)} rows)")

    # ==================== 项目指标事实数据 ====================
    indicator_data = []
    indicator_id = 1
    for project in project_data:
        for month in range(1, 13):
            date_key = 20240000 + month * 100 + 15
            indicator_data.append({
                "indicator_id": f"IND{indicator_id:06d}",
                "date_key": date_key,
                "calendar_date": datetime(2024, month, 15).date(),
                "project_key": project["project_key"],
                "indicator_code": random.choice(["ROI", "利润率", "成本率", "产值完成率"]),
                "indicator_name": random.choice(["投资回报率", "项目利润率", "成本占收比", "产值完成率"]),
                "indicator_value": random.uniform(0.1, 0.9),
                "indicator_unit": random.choice(["%", "倍", "万元"]),
                "region_key": project.get("region_key", ""),
                "organization_key": project.get("organization_key", ""),
            })
            indicator_id += 1

    s.sql.insert_rows("fact_project_indicator", indicator_data)
    output.print(f"OK fact_project_indicator ({len(indicator_data)} rows)")

    output.print("\n=== 商务成本本体数据灌入完成 ===")
    output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "rows": {
        "dim_date": len(date_data),
        "dim_region": len(region_data),
        "dim_organization": len(org_data),
        "dim_cost_subject": len(subject_data),
        "dim_project_category": len(category_data),
        "dim_cooperation": len(cooperation_data),
        "dim_owner": len(owner_data),
        "dim_client": len(client_data),
        "dim_contract_type": len(contract_type_data),
        "dim_project_status": len(project_status_data),
        "dim_contract_status": len(contract_status_data),
        "dim_risk_level": len(risk_level_data),
        "dim_project": len(project_data),
        "dim_contract": len(contract_data),
        "fact_project_cost": len(cost_data[:1000]),
        "fact_project_output": len(output_data),
        "fact_payment": len(payment_data),
        "fact_receivable": len(receivable_data),
        "fact_cash_flow": len(cashflow_data),
        "fact_risk": len(risk_data),
        "fact_change_order": len(change_data),
        "fact_claim": len(claim_data),
        "fact_project_indicator": len(indicator_data),
    }}, ensure_ascii=True))