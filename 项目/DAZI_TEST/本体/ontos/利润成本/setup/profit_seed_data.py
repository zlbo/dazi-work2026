"""化工利润成本本体灌数脚本 — space_cate_test01

灌数内容：
1. dim_plant（厂区）
2. dim_process_unit（工艺单元）
3. dim_account（会计科目）
4. dim_cost_center（成本中心）
5. dim_material（原料物料）
6. dim_energy_type（能源类型）
7. fact_gl_journal_entry（GL分录）
8. fact_budget_entry（预算）
9. fact_production_cost（生产成本归集）
10. fact_energy_consumption（能源消耗）

放置：项目/DAZI_TEST/本体/ontos/利润成本/setup/profit_seed_data.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本/setup/profit_seed_data.py --space space_cate_test01 --type data
规划对照：项目/DAZI_TEST/本体/ontos/利润成本/plans/化工利润成本分析本体方案.md
"""

import json
from datetime import date, datetime, timedelta


def main():
    space_id = "space_cate_test01"
    s = space.get(space_id)

    output.print("=== 化工利润成本本体灌数 ===")
    output.print(f"空间: {space_id}")

    today = date.today()
    current_year = today.year

    # 1. dim_plant 灌数
    output.print("\n[1/10] 灌数 dim_plant...")
    plants = [
        {"plant_id": "P001", "plant_code": "乙烯厂区", "plant_name": "乙烯装置区", "company_code": "C001", "plant_type": "烯烃", "location": "园区A", "design_capacity": 600000, "capacity_unit": "吨", "status": "运行"},
        {"plant_id": "P002", "plant_code": "芳烃厂区", "plant_name": "芳烃装置区", "company_code": "C001", "plant_type": "芳烃", "location": "园区A", "design_capacity": 400000, "capacity_unit": "吨", "status": "运行"},
        {"plant_id": "P003", "plant_code": "精细化工区", "plant_name": "精细化工装置区", "company_code": "C001", "plant_type": "精细化工", "location": "园区B", "design_capacity": 100000, "capacity_unit": "吨", "status": "检修"},
    ]
    for p in plants:
        s.sql.execute(
            "INSERT INTO dim_plant VALUES",
            [
                (
                    p["plant_id"], p["plant_code"], p["plant_name"],
                    p["company_code"], p["plant_type"], p["location"],
                    p["design_capacity"], p["capacity_unit"], p["status"],
                    datetime.now()
                )
            ],
        )
    output.print(f"OK dim_plant ({len(plants)} 条)")

    # 2. dim_process_unit 灌数
    output.print("\n[2/10] 灌数 dim_process_unit...")
    units = [
        {"unit_id": "U001", "unit_code": "裂解单元", "unit_name": "裂解炉区", "plant_id": "P001", "plant_name": "乙烯装置区", "unit_type": "反应", "criticality": "A", "status": "运行"},
        {"unit_id": "U002", "unit_code": "分离单元", "unit_name": "分离工段", "plant_id": "P001", "plant_name": "乙烯装置区", "unit_type": "分离", "criticality": "A", "status": "运行"},
        {"unit_id": "U003", "unit_code": "压缩单元", "unit_name": "压缩工段", "plant_id": "P001", "plant_name": "乙烯装置区", "unit_type": "压缩", "criticality": "B", "status": "运行"},
        {"unit_id": "U004", "unit_code": "芳烃抽提", "unit_name": "芳烃抽提工段", "plant_id": "P002", "plant_name": "芳烃装置区", "unit_type": "分离", "criticality": "A", "status": "运行"},
        {"unit_id": "U005", "unit_code": "歧化单元", "unit_name": "歧化工段", "plant_id": "P002", "plant_name": "芳烃装置区", "unit_type": "反应", "criticality": "B", "status": "运行"},
        {"unit_id": "U006", "unit_code": "加氢单元", "unit_name": "加氢工段", "plant_id": "P003", "plant_name": "精细化工装置区", "unit_type": "反应", "criticality": "A", "status": "检修"},
    ]
    for u in units:
        s.sql.execute(
            "INSERT INTO dim_process_unit VALUES",
            [
                (
                    u["unit_id"], u["unit_code"], u["unit_name"],
                    u["plant_id"], u["plant_name"], u["unit_type"],
                    u["criticality"], u["status"], datetime.now()
                )
            ],
        )
    output.print(f"OK dim_process_unit ({len(units)} 条)")

    # 3. dim_account 灌数
    output.print("\n[3/10] 灌数 dim_account...")
    accounts = [
        # 收入
        {"account_id": "A001", "account_code": "4001", "account_name": "主营业务收入", "account_type": "收入", "pl_category": "主营业务收入", "cost_element": None, "parent_account_id": None, "account_level": 1, "is_leaf": False, "normal_balance": "贷", "status": "启用"},
        {"account_id": "A002", "account_code": "400101", "account_name": "乙烯销售收入", "account_type": "收入", "pl_category": "主营业务收入", "cost_element": None, "parent_account_id": "A001", "account_level": 2, "is_leaf": True, "normal_balance": "贷", "status": "启用"},
        {"account_id": "A003", "account_code": "400102", "account_name": "丙烯销售收入", "account_type": "收入", "pl_category": "主营业务收入", "cost_element": None, "parent_account_id": "A001", "account_level": 2, "is_leaf": True, "normal_balance": "贷", "status": "启用"},
        {"account_id": "A004", "account_code": "400103", "account_name": "芳烃销售收入", "account_type": "收入", "pl_category": "主营业务收入", "cost_element": None, "parent_account_id": "A001", "account_level": 2, "is_leaf": True, "normal_balance": "贷", "status": "启用"},
        # 成本
        {"account_id": "A010", "account_code": "5001", "account_name": "主营业务成本", "account_type": "成本", "pl_category": "主营业务成本", "cost_element": None, "parent_account_id": None, "account_level": 1, "is_leaf": False, "normal_balance": "借", "status": "启用"},
        {"account_id": "A011", "account_code": "500101", "account_name": "直接材料", "account_type": "成本", "pl_category": "主营业务成本", "cost_element": "原料", "parent_account_id": "A010", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
        {"account_id": "A012", "account_code": "500102", "account_name": "直接人工", "account_type": "成本", "pl_category": "主营业务成本", "cost_element": "人工", "parent_account_id": "A010", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
        {"account_id": "A013", "account_code": "500103", "account_name": "能源成本", "account_type": "成本", "pl_category": "主营业务成本", "cost_element": "能源", "parent_account_id": "A010", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
        {"account_id": "A014", "account_code": "500104", "account_name": "制造费用", "account_type": "成本", "pl_category": "主营业务成本", "cost_element": "折旧", "parent_account_id": "A010", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
        # 费用
        {"account_id": "A020", "account_code": "6602", "account_name": "管理费用", "account_type": "费用", "pl_category": "管理费用", "cost_element": "其他", "parent_account_id": None, "account_level": 1, "is_leaf": False, "normal_balance": "借", "status": "启用"},
        {"account_id": "A021", "account_code": "660201", "account_name": "办公费", "account_type": "费用", "pl_category": "管理费用", "cost_element": "其他", "parent_account_id": "A020", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
        {"account_id": "A022", "account_code": "660202", "account_name": "差旅费", "account_type": "费用", "pl_category": "管理费用", "cost_element": "其他", "parent_account_id": "A020", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
        {"account_id": "A023", "account_code": "660203", "account_name": "折旧摊销", "account_type": "费用", "pl_category": "管理费用", "cost_element": "折旧", "parent_account_id": "A020", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
    ]
    for a in accounts:
        s.sql.execute(
            "INSERT INTO dim_account VALUES",
            [
                (
                    a["account_id"], a["account_code"], a["account_name"],
                    a["account_type"], a["pl_category"], a["cost_element"],
                    a["parent_account_id"], a["account_level"], a["is_leaf"],
                    a["normal_balance"], a["status"], datetime.now()
                )
            ],
        )
    output.print(f"OK dim_account ({len(accounts)} 条)")

    # 4. dim_cost_center 灌数
    output.print("\n[4/10] 灌数 dim_cost_center...")
    cost_centers = [
        {"cost_center_id": "CC001", "cost_center_code": "乙烯车间", "cost_center_name": "乙烯生产车间", "department": "生产部", "company_code": "C001", "profit_center": "乙烯事业部", "plant_id": "P001", "unit_id": None, "status": "启用"},
        {"cost_center_id": "CC002", "cost_center_code": "芳烃车间", "cost_center_name": "芳烃生产车间", "department": "生产部", "company_code": "C001", "profit_center": "芳烃事业部", "plant_id": "P002", "unit_id": None, "status": "启用"},
        {"cost_center_id": "CC003", "cost_center_code": "精细化工车间", "cost_center_name": "精细化工生产车间", "department": "生产部", "company_code": "C001", "profit_center": "精细化工事业部", "plant_id": "P003", "unit_id": None, "status": "启用"},
        {"cost_center_id": "CC004", "cost_center_code": "管理部门", "cost_center_name": "综合管理中心", "department": "管理部", "company_code": "C001", "profit_center": None, "plant_id": None, "unit_id": None, "status": "启用"},
    ]
    for cc in cost_centers:
        s.sql.execute(
            "INSERT INTO dim_cost_center VALUES",
            [
                (
                    cc["cost_center_id"], cc["cost_center_code"], cc["cost_center_name"],
                    cc["department"], cc["company_code"], cc["profit_center"],
                    cc["plant_id"], cc["unit_id"], cc["status"], datetime.now()
                )
            ],
        )
    output.print(f"OK dim_cost_center ({len(cost_centers)} 条)")

    # 5. dim_material 灌数
    output.print("\n[5/10] 灌数 dim_material...")
    materials = [
        {"material_id": "M001", "material_code": "石脑油", "material_name": "石脑油", "material_type": "原料", "unit_of_measure": "吨", "unit_price_standard": 4500.0, "status": "启用"},
        {"material_id": "M002", "material_code": "乙烯", "material_name": "乙烯", "material_type": "产品", "unit_of_measure": "吨", "unit_price_standard": 8000.0, "status": "启用"},
        {"material_id": "M003", "material_code": "丙烯", "material_name": "丙烯", "material_type": "产品", "unit_of_measure": "吨", "unit_price_standard": 7500.0, "status": "启用"},
        {"material_id": "M004", "material_code": "苯", "material_name": "苯", "material_type": "产品", "unit_of_measure": "吨", "unit_price_standard": 6500.0, "status": "启用"},
        {"material_id": "M005", "material_code": "催化剂A", "material_name": "裂解催化剂A", "material_type": "催化剂", "unit_of_measure": "千克", "unit_price_standard": 120.0, "status": "启用"},
    ]
    for m in materials:
        s.sql.execute(
            "INSERT INTO dim_material VALUES",
            [
                (
                    m["material_id"], m["material_code"], m["material_name"],
                    m["material_type"], m["unit_of_measure"], m["unit_price_standard"],
                    m["status"], datetime.now()
                )
            ],
        )
    output.print(f"OK dim_material ({len(materials)} 条)")

    # 6. dim_energy_type 灌数
    output.print("\n[6/10] 灌数 dim_energy_type...")
    energy_types = [
        {"energy_type_id": "E001", "energy_type_code": "电力", "energy_type_name": "电力", "unit_of_measure": "kWh", "unit_price_standard": 0.65, "status": "启用"},
        {"energy_type_id": "E002", "energy_type_code": "蒸汽", "energy_type_name": "蒸汽", "unit_of_measure": "吨", "unit_price_standard": 180.0, "status": "启用"},
        {"energy_type_id": "E003", "energy_type_code": "天然气", "energy_type_name": "天然气", "unit_of_measure": "立方米", "unit_price_standard": 2.8, "status": "启用"},
        {"energy_type_id": "E004", "energy_type_code": "循环水", "energy_type_name": "循环水", "unit_of_measure": "吨", "unit_price_standard": 0.3, "status": "启用"},
    ]
    for e in energy_types:
        s.sql.execute(
            "INSERT INTO dim_energy_type VALUES",
            [
                (
                    e["energy_type_id"], e["energy_type_code"], e["energy_type_name"],
                    e["unit_of_measure"], e["unit_price_standard"], e["status"],
                    datetime.now()
                )
            ],
        )
    output.print(f"OK dim_energy_type ({len(energy_types)} 条)")

    # 7. fact_gl_journal_entry 灌数（示例数据）
    output.print("\n[7/10] 灌数 fact_gl_journal_entry...")
    gl_entries = []
    entry_id = 1
    # 模拟12个月的数据
    for month in range(1, 7):  # 1-6月
        posting_date = date(current_year, month, 15)
        date_key = int(posting_date.strftime("%Y%m%d"))
        
        # 乙烯销售收入
        gl_entries.append((
            f"E{entry_id:05d}", f"L{entry_id:05d}", date_key, posting_date,
            current_year, month, "A002", "400101", "乙烯销售收入",
            "收入", "主营业务收入", None, 2,
            "CC001", "乙烯生产车间", "生产部", "P001", "U001",
            0.0, 5000000.0 - month * 50000, -4500000.0 + month * 40000,  # credit - debit = amount_signed
            "CNY", f"V{entry_id:05d}", "SAP", f"{month}月乙烯销售",
            datetime.now()
        ))
        entry_id += 1
        
        # 直接材料
        gl_entries.append((
            f"E{entry_id:05d}", f"L{entry_id:05d}", date_key, posting_date,
            current_year, month, "A011", "500101", "直接材料",
            "成本", "主营业务成本", "原料", 2,
            "CC001", "乙烯生产车间", "生产部", "P001", "U001",
            2800000.0 - month * 30000, 0.0, 2800000.0 - month * 30000,  # debit - credit = amount_signed
            "CNY", f"V{entry_id:05d}", "SAP", f"{month}月原材料消耗",
            datetime.now()
        ))
        entry_id += 1
        
        # 能源成本
        gl_entries.append((
            f"E{entry_id:05d}", f"L{entry_id:05d}", date_key, posting_date,
            current_year, month, "A013", "500103", "能源成本",
            "成本", "主营业务成本", "能源", 2,
            "CC001", "乙烯生产车间", "生产部", "P001", "U001",
            350000.0 - month * 5000, 0.0, 350000.0 - month * 5000,
            "CNY", f"V{entry_id:05d}", "SAP", f"{month}月能源消耗",
            datetime.now()
        ))
        entry_id += 1
        
        # 管理费用
        gl_entries.append((
            f"E{entry_id:05d}", f"L{entry_id:05d}", date_key, posting_date,
            current_year, month, "A021", "660201", "办公费",
            "费用", "管理费用", "其他", 2,
            "CC004", "综合管理中心", "管理部", None, None,
            80000.0, 0.0, 80000.0,
            "CNY", f"V{entry_id:05d}", "SAP", f"{month}月办公费",
            datetime.now()
        ))
        entry_id += 1

    s.sql.execute(
        "INSERT INTO fact_gl_journal_entry VALUES",
        gl_entries,
    )
    output.print(f"OK fact_gl_journal_entry ({len(gl_entries)} 条)")

    # 8. fact_budget_entry 灌数
    output.print("\n[8/10] 灌数 fact_budget_entry...")
    budget_entries = []
    line_id = 1
    for month in range(1, 7):
        posting_date = date(current_year, month, 1)
        date_key = int(posting_date.strftime("%Y%m%d"))
        
        # 乙烯销售收入预算
        budget_entries.append((
            f"B001", f"L{line_id:05d}", date_key, "2026年度预算",
            current_year, month, "A002", "400101", "乙烯销售收入",
            "收入", "主营业务收入", None,
            "CC001", "乙烯生产车间", "生产部", "P001", "U001",
            4800000.0, "CNY", "已发布", datetime.now()
        ))
        line_id += 1
        
        # 直接材料预算
        budget_entries.append((
            f"B001", f"L{line_id:05d}", date_key, "2026年度预算",
            current_year, month, "A011", "500101", "直接材料",
            "成本", "主营业务成本", "原料",
            "CC001", "乙烯生产车间", "生产部", "P001", "U001",
            2700000.0, "CNY", "已发布", datetime.now()
        ))
        line_id += 1
        
        # 能源成本预算
        budget_entries.append((
            f"B001", f"L{line_id:05d}", date_key, "2026年度预算",
            current_year, month, "A013", "500103", "能源成本",
            "成本", "主营业务成本", "能源",
            "CC001", "乙烯生产车间", "生产部", "P001", "U001",
            340000.0, "CNY", "已发布", datetime.now()
        ))
        line_id += 1
        
        # 管理费用预算
        budget_entries.append((
            f"B001", f"L{line_id:05d}", date_key, "2026年度预算",
            current_year, month, "A021", "660201", "办公费",
            "费用", "管理费用", "其他",
            "CC004", "综合管理中心", "管理部", None, None,
            85000.0, "CNY", "已发布", datetime.now()
        ))
        line_id += 1

    s.sql.execute(
        "INSERT INTO fact_budget_entry VALUES",
        budget_entries,
    )
    output.print(f"OK fact_budget_entry ({len(budget_entries)} 条)")

    # 9. fact_production_cost 灌数
    output.print("\n[9/10] 灌数 fact_production_cost...")
    production_costs = []
    cost_id = 1
    for month in range(1, 7):
        posting_date = date(current_year, month, 15)
        date_key = int(posting_date.strftime("%Y%m%d"))
        
        # 石脑油消耗
        production_costs.append((
            f"PC{cost_id:05d}", date_key, current_year, month,
            "P001", "乙烯装置区", "U001", "裂解炉区",
            "M001", "石脑油", None, None,
            620.0 - month * 5, 4500.0, 2790000.0 - month * 22500,
            "原料", "CC001", "乙烯生产车间",
            580.0 - month * 3, "吨", datetime.now()
        ))
        cost_id += 1
        
        # 电力消耗
        production_costs.append((
            f"PC{cost_id:05d}", date_key, current_year, month,
            "P001", "乙烯装置区", "U002", "分离工段",
            None, None, "E001", "电力",
            450000.0 - month * 5000, 0.65, 292500.0 - month * 3250,
            "能源", "CC001", "乙烯生产车间",
            580.0 - month * 3, "吨", datetime.now()
        ))
        cost_id += 1
        
        # 蒸汽消耗
        production_costs.append((
            f"PC{cost_id:05d}", date_key, current_year, month,
            "P001", "乙烯装置区", "U003", "压缩工段",
            None, None, "E002", "蒸汽",
            1800.0 - month * 20, 180.0, 324000.0 - month * 3600,
            "能源", "CC001", "乙烯生产车间",
            580.0 - month * 3, "吨", datetime.now()
        ))
        cost_id += 1
        
        # 催化剂
        production_costs.append((
            f"PC{cost_id:05d}", date_key, current_year, month,
            "P001", "乙烯装置区", "U001", "裂解炉区",
            "M005", "裂解催化剂A", None, None,
            500.0, 120.0, 60000.0,
            "原料", "CC001", "乙烯生产车间",
            580.0 - month * 3, "吨", datetime.now()
        ))
        cost_id += 1

    s.sql.execute(
        "INSERT INTO fact_production_cost VALUES",
        production_costs,
    )
    output.print(f"OK fact_production_cost ({len(production_costs)} 条)")

    # 10. fact_energy_consumption 灌数
    output.print("\n[10/10] 灌数 fact_energy_consumption...")
    energy_consumptions = []
    energy_id = 1
    for month in range(1, 7):
        posting_date = date(current_year, month, 15)
        date_key = int(posting_date.strftime("%Y%m%d"))
        
        # 电力消耗
        energy_consumptions.append((
            f"EN{energy_id:05d}", date_key, current_year, month,
            "P001", "乙烯装置区", "U001", "裂解炉区",
            "E001", "电力",
            280000.0 - month * 3000, "kWh", 0.65,
            182000.0 - month * 1950, "CC001",
            580.0 - month * 3, 480.0 - month * 4, datetime.now()
        ))
        energy_id += 1
        
        # 蒸汽消耗
        energy_consumptions.append((
            f"EN{energy_id:05d}", date_key, current_year, month,
            "P001", "乙烯装置区", "U002", "分离工段",
            "E002", "蒸汽",
            1200.0 - month * 15, "吨", 180.0,
            216000.0 - month * 2700, "CC001",
            580.0 - month * 3, 2.07, datetime.now()
        ))
        energy_id += 1
        
        # 天然气消耗
        energy_consumptions.append((
            f"EN{energy_id:05d}", date_key, current_year, month,
            "P001", "乙烯装置区", "U001", "裂解炉区",
            "E003", "天然气",
            85000.0 - month * 1000, "立方米", 2.8,
            238000.0 - month * 2800, "CC001",
            580.0 - month * 3, 146.0, datetime.now()
        ))
        energy_id += 1

    s.sql.execute(
        "INSERT INTO fact_energy_consumption VALUES",
        energy_consumptions,
    )
    output.print(f"OK fact_energy_consumption ({len(energy_consumptions)} 条)")

    summary = {
        "ok": True,
        "space_id": space_id,
        "dim_plant": len(plants),
        "dim_process_unit": len(units),
        "dim_account": len(accounts),
        "dim_cost_center": len(cost_centers),
        "dim_material": len(materials),
        "dim_energy_type": len(energy_types),
        "fact_gl_journal_entry": len(gl_entries),
        "fact_budget_entry": len(budget_entries),
        "fact_production_cost": len(production_costs),
        "fact_energy_consumption": len(energy_consumptions),
    }

    output.print("\n=== 化工利润成本本体灌数完成 ===")
    output.success("灌数成功")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))
