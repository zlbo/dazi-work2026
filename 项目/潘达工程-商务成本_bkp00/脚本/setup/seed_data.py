"""Panda Cost Analysis Seed Data Script for space__panda_cost01

模拟数据策略：
1. 基于现有数据库表模式生成模拟数据
2. 遵循业务规则和勾稽关系
3. 参考真实数据分布设置取值范围
4. 强制执行参照完整性

数据规模：
- 项目数：10个
- 报告期间：2024年1月至2024年12月
- 合同数：每个项目5-10个
- 供应商：每个项目3-5个

参考文档：
- 项目/潘达工程-商务成本/规划/130-阶段三-本体设计与确认/050-模拟数据计划.md
"""

import random
import json
from datetime import datetime


def generate_project_id(index):
    return f"PROJ_{str(index).zfill(4)}"


def generate_company_id(index):
    return f"COMP_{str(index).zfill(3)}"


def generate_contract_id(project_index, contract_index):
    return f"CON_{str(project_index).zfill(4)}_{str(contract_index).zfill(3)}"


def generate_report_period(year, month):
    return f"{year}{str(month).zfill(2)}"


def main():
    space_id = "space__panda_cost01"
    s = space.get(space_id)

    output.print("=== Start Panda Cost Analysis Seed Data Generation ===")
    output.print(f"Space: {space_id}")

    # 配置参数
    config = {
        "num_projects": 10,
        "years": [2024],
        "months": list(range(1, 13)),
        "num_contracts_per_project": (5, 10),
        "num_suppliers_per_project": (3, 5),
    }

    # 公司数据
    companies = [
        {"id": "COMP_001", "name": "华东分公司"},
        {"id": "COMP_002", "name": "华北分公司"},
        {"id": "COMP_003", "name": "华南分公司"},
        {"id": "COMP_004", "name": "西南分公司"},
        {"id": "COMP_005", "name": "华中分公司"},
    ]

    # 供应商类型
    supplier_types = ["劳务分包", "材料供应", "设备租赁", "专业分包"]

    # 指标类型
    indicators = [
        {"code": "IND001", "name": "产值完成率"},
        {"code": "IND002", "name": "成本利润率"},
        {"code": "IND003", "name": "回款率"},
        {"code": "IND004", "name": "存货周转率"},
        {"code": "IND005", "name": "资金占用率"},
    ]

    # 风险类型
    risk_types = [
        {"code": "RISK001", "name": "市场风险", "level": ["低", "中", "高"]},
        {"code": "RISK002", "name": "财务风险", "level": ["低", "中", "高"]},
        {"code": "RISK003", "name": "进度风险", "level": ["低", "中", "高"]},
        {"code": "RISK004", "name": "质量风险", "level": ["低", "中", "高"]},
    ]

    # 科目数据
    balance_subjects = [
        {"code": "101", "name": "应收账款"},
        {"code": "102", "name": "预付账款"},
        {"code": "201", "name": "应付账款"},
        {"code": "202", "name": "预收账款"},
        {"code": "301", "name": "工程结算"},
        {"code": "302", "name": "主营业务收入"},
        {"code": "303", "name": "主营业务成本"},
    ]

    output.print("\n[1/5] Generating ProjectIndicator data...")
    project_indicator_rows = []
    
    for project_idx in range(1, config["num_projects"] + 1):
        project_id = generate_project_id(project_idx)
        company = random.choice(companies)
        
        base_building_area = random.uniform(50000, 500000)
        base_contract_amount = base_building_area * random.uniform(1500, 3000)

        for year in config["years"]:
            for month in config["months"]:
                report_period = generate_report_period(year, month)
                
                for indicator in indicators:
                    indicator_value = random.uniform(0.5, 1.2)
                    target_value = random.uniform(0.8, 1.0)
                    warning_level = "正常"
                    if indicator_value < 0.6:
                        warning_level = "预警"
                    elif indicator_value < 0.8:
                        warning_level = "关注"

                    row = {
                        "id": f"PI_{project_id}_{report_period}_{indicator['code']}",
                        "project_id": project_id,
                        "project_name": f"项目{project_idx}",
                        "project_code": f"PD{str(project_idx).zfill(4)}",
                        "company_id": company["id"],
                        "company_name": company["name"],
                        "section_id": f"SEC_{project_idx}_{random.randint(1, 3)}",
                        "section_name": f"标段{random.randint(1, 3)}",
                        "building_area": base_building_area,
                        "contract_amount": base_contract_amount,
                        "report_period": report_period,
                        "indicator_code": indicator["code"],
                        "indicator_name": indicator["name"],
                        "indicator_value": indicator_value,
                        "target_value": target_value,
                        "warning_level": warning_level,
                        "remark": "",
                        "created_at": datetime.now().isoformat(),
                    }
                    project_indicator_rows.append(row)
    
    s.sql.insert("tb_project_indicator", project_indicator_rows)
    output.print(f"OK {len(project_indicator_rows)} rows inserted")

    output.print("\n[2/5] Generating ProjectOutput data...")
    project_output_rows = []
    
    for project_idx in range(1, config["num_projects"] + 1):
        project_id = generate_project_id(project_idx)
        base_contract_amount = random.uniform(10000000, 500000000)
        
        cumulative_output = 0
        for year in config["years"]:
            for month in config["months"]:
                report_period = generate_report_period(year, month)
                
                monthly_output = base_contract_amount * random.uniform(0.005, 0.02)
                confirmed_ratio = random.uniform(0.7, 0.95)
                
                confirmed_output = monthly_output * confirmed_ratio
                unconfirmed_output = monthly_output * (1 - confirmed_ratio)
                cumulative_output += monthly_output

                # 累计确认/待确认（按比例）
                last_year_confirmed = cumulative_output * random.uniform(0.6, 0.8) if month > 1 else 0
                last_year_unconfirmed = cumulative_output * (1 - (last_year_confirmed / cumulative_output)) if month > 1 else 0
                current_confirmed = confirmed_output
                current_unconfirmed = unconfirmed_output

                row = {
                    "id": f"PO_{project_id}_{report_period}",
                    "project_id": project_id,
                    "report_period": report_period,
                    "confirmed_output": confirmed_output,
                    "unconfirmed_output": unconfirmed_output,
                    "total_output": monthly_output,
                    "last_year_confirmed": last_year_confirmed,
                    "last_year_unconfirmed": last_year_unconfirmed,
                    "current_confirmed": current_confirmed,
                    "current_unconfirmed": current_unconfirmed,
                    "created_at": datetime.now().isoformat(),
                }
                project_output_rows.append(row)
    
    s.sql.insert("tb_project_output", project_output_rows)
    output.print(f"OK {len(project_output_rows)} rows inserted")

    output.print("\n[3/5] Generating ProjectCost data...")
    project_cost_rows = []
    
    for project_idx in range(1, config["num_projects"] + 1):
        project_id = generate_project_id(project_idx)
        base_contract_amount = random.uniform(10000000, 500000000)
        
        cumulative_cost_confirmed = 0
        cumulative_cost_unconfirmed = 0
        
        for year in config["years"]:
            for month in config["months"]:
                report_period = generate_report_period(year, month)
                
                # 成本约为产值的80-90%
                monthly_cost = base_contract_amount * random.uniform(0.004, 0.018)
                confirmed_ratio = random.uniform(0.75, 0.92)
                
                confirmed_cost_cmonth = monthly_cost * confirmed_ratio
                unconfirmed_cost_cmonth = monthly_cost * (1 - confirmed_ratio)
                
                cumulative_cost_confirmed += confirmed_cost_cmonth
                cumulative_cost_unconfirmed += unconfirmed_cost_cmonth

                # 成本构成比例
                labor_ratio = random.uniform(0.2, 0.3)
                material_ratio = random.uniform(0.5, 0.65)
                equipment_ratio = random.uniform(0.05, 0.15)
                
                labor_cost_acc = cumulative_cost_confirmed * labor_ratio
                material_cost_acc = cumulative_cost_confirmed * material_ratio
                equipment_cost_acc = cumulative_cost_confirmed * equipment_ratio

                row = {
                    "id": f"PC_{project_id}_{report_period}",
                    "project_id": project_id,
                    "report_period": report_period,
                    "confirmed_cost_acc": cumulative_cost_confirmed,
                    "unconfirmed_cost_acc": cumulative_cost_unconfirmed,
                    "confirmed_cost_cmonth": confirmed_cost_cmonth,
                    "unconfirmed_cost_cmonth": unconfirmed_cost_cmonth,
                    "labor_cost_acc": labor_cost_acc,
                    "material_cost_acc": material_cost_acc,
                    "equipment_cost_acc": equipment_cost_acc,
                    "management_fee_rate": random.uniform(0.03, 0.08),
                    "created_at": datetime.now().isoformat(),
                }
                project_cost_rows.append(row)
    
    s.sql.insert("tb_project_cost", project_cost_rows)
    output.print(f"OK {len(project_cost_rows)} rows inserted")

    output.print("\n[4/5] Generating ProjectPayment data...")
    project_payment_rows = []
    
    for project_idx in range(1, config["num_projects"] + 1):
        project_id = generate_project_id(project_idx)
        num_contracts = random.randint(*config["num_contracts_per_project"])
        
        contracts = []
        for contract_idx in range(1, num_contracts + 1):
            contract = {
                "id": generate_contract_id(project_idx, contract_idx),
                "code": f"HT{str(project_idx).zfill(4)}{str(contract_idx).zfill(3)}",
                "name": f"合同{contract_idx}",
                "amount": random.uniform(500000, 50000000),
                "supplier_name": f"供应商{project_idx}-{contract_idx}",
                "supplier_type": random.choice(supplier_types),
            }
            contracts.append(contract)

        for year in config["years"]:
            for month in config["months"]:
                report_period = generate_report_period(year, month)
                
                for contract in contracts:
                    # 付款进度随时间推进
                    time_factor = min(1.0, month / 12)
                    payable_confirmed = contract["amount"] * time_factor * random.uniform(0.7, 0.9)
                    labor_payable = payable_confirmed * random.uniform(0.2, 0.4)
                    paid_ratio = random.uniform(0.6, 0.95)
                    paid_amount = payable_confirmed * paid_ratio
                    payable_unconfirmed = payable_confirmed * random.uniform(0.1, 0.3)
                    tax_rate = random.choice([0.09, 0.06, 0.13])

                    row = {
                        "id": f"PP_{contract['id']}_{report_period}",
                        "project_id": project_id,
                        "contract_id": contract["id"],
                        "contract_code": contract["code"],
                        "contract_name": contract["name"],
                        "contract_content": f"{contract['name']} - {contract['supplier_type']}",
                        "supplier_name": contract["supplier_name"],
                        "supplier_type": contract["supplier_type"],
                        "contract_amount": contract["amount"],
                        "report_period": report_period,
                        "payable_confirmed": payable_confirmed,
                        "labor_payable": labor_payable,
                        "paid_amount": paid_amount,
                        "payable_unconfirmed": payable_unconfirmed,
                        "payment_ratio": paid_ratio,
                        "tax_rate": tax_rate,
                        "settlement_status": "已结算" if month >= 10 else "进行中",
                        "created_at": datetime.now().isoformat(),
                    }
                    project_payment_rows.append(row)
    
    s.sql.insert("tb_project_payment", project_payment_rows)
    output.print(f"OK {len(project_payment_rows)} rows inserted")

    output.print("\n[5/5] Generating ProjectBalance and ProjectRisk data...")
    project_balance_rows = []
    project_risk_rows = []
    
    for project_idx in range(1, config["num_projects"] + 1):
        project_id = generate_project_id(project_idx)
        
        for year in config["years"]:
            for month in config["months"]:
                report_period = generate_report_period(year, month)

                # 收支数据
                for subject in balance_subjects:
                    project_amount = random.uniform(-10000000, 10000000)
                    company_amount = project_amount * random.uniform(0.8, 1.2)
                    
                    row = {
                        "id": f"PB_{project_id}_{report_period}_{subject['code']}",
                        "project_id": project_id,
                        "report_period": report_period,
                        "subject_code": subject["code"],
                        "subject_name": subject["name"],
                        "project_amount": project_amount,
                        "company_amount": company_amount,
                        "total_amount": project_amount + company_amount,
                        "created_at": datetime.now().isoformat(),
                    }
                    project_balance_rows.append(row)

                # 风险数据
                for risk in risk_types:
                    risk_value = random.randint(1, 10)
                    warning_level = "低" if risk_value <= 3 else ("中" if risk_value <= 7 else "高")
                    
                    row = {
                        "id": f"PR_{project_id}_{report_period}_{risk['code']}",
                        "project_id": project_id,
                        "report_period": report_period,
                        "risk_type": risk["name"],
                        "risk_code": risk["code"],
                        "risk_name": risk["name"],
                        "risk_value": risk_value,
                        "warning_level": warning_level,
                        "risk_description": f"{risk['name']}评估值",
                        "created_at": datetime.now().isoformat(),
                    }
                    project_risk_rows.append(row)
    
    s.sql.insert("tb_project_balance", project_balance_rows)
    output.print(f"OK {len(project_balance_rows)} balance rows inserted")
    
    s.sql.insert("tb_project_risk", project_risk_rows)
    output.print(f"OK {len(project_risk_rows)} risk rows inserted")

    # 总结
    summary = {
        "ok": True,
        "space_id": space_id,
        "project_indicator": len(project_indicator_rows),
        "project_output": len(project_output_rows),
        "project_cost": len(project_cost_rows),
        "project_payment": len(project_payment_rows),
        "project_balance": len(project_balance_rows),
        "project_risk": len(project_risk_rows),
        "total_rows": sum([
            len(project_indicator_rows),
            len(project_output_rows),
            len(project_cost_rows),
            len(project_payment_rows),
            len(project_balance_rows),
            len(project_risk_rows),
        ]),
    }

    output.print("\n=== Panda Cost Analysis Seed Data Generation Completed ===")
    output.print(f"ProjectIndicator: {summary['project_indicator']}")
    output.print(f"ProjectOutput: {summary['project_output']}")
    output.print(f"ProjectCost: {summary['project_cost']}")
    output.print(f"ProjectPayment: {summary['project_payment']}")
    output.print(f"ProjectBalance: {summary['project_balance']}")
    output.print(f"ProjectRisk: {summary['project_risk']}")
    output.print(f"Total Rows: {summary['total_rows']}")
    output.success("Seed data generation completed successfully")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))