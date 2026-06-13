"""种子数据灌数脚本 - 商务成本智能决策体系

版本：V1.0
依据：阶段二设计文档 + 阶段三种子数据生成交接词
功能：生成符合要求的模拟数据，包含业务主体唯一性、数据多样性、经营品质差异化

发布：dazi onto script publish .../setup/panda_cost_seed_data.py --space space__panda_construction --type setup
执行：dazi onto script run --file .../setup/panda_cost_seed_data.py --space space__panda_construction
"""

import random
from datetime import datetime, timedelta

def generate_date_key(date):
    return int(date.strftime('%Y%m%d'))

def generate_random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def get_quality_factor(quality_level):
    factors = {
        'A': {'cost_deviation': 0.05, 'profit_rate': 0.15, 'risk_probability': 0.1},
        'B': {'cost_deviation': 0.15, 'profit_rate': 0.08, 'risk_probability': 0.3},
        'C': {'cost_deviation': 0.30, 'profit_rate': 0.02, 'risk_probability': 0.6},
    }
    return factors[quality_level]

def generate_dim_date_data(start_date, end_date):
    data = []
    current_date = start_date
    while current_date <= end_date:
        data.append({
            'date_key': generate_date_key(current_date),
            'calendar_date': current_date.date(),
            'year': current_date.year,
            'quarter': (current_date.month - 1) // 3 + 1,
            'month': current_date.month,
            'week_of_year': current_date.isocalendar()[1],
            'day_of_week': current_date.isoweekday(),
            'is_weekend': 1 if current_date.isoweekday() in [6, 7] else 0,
            'year_month': current_date.strftime('%Y-%m'),
        })
        current_date += timedelta(days=1)
    return data

def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)
    
    output.print("=== 开始生成种子数据 ===")
    output.print(f"空间: {space_id}")
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    # 1. 生成日期维表数据
    output.print("\n[1/10] 生成日期维表数据...")
    date_data = generate_dim_date_data(start_date, end_date)
    s.sql.insert_rows('dim_date', date_data)
    output.print(f"  已插入 {len(date_data)} 条日期数据")
    
    # 2. 生成成本科目数据
    output.print("\n[2/10] 生成成本科目维表数据...")
    cost_subjects = []
    cost_subjects.append({'cost_subject_key': 'CS001', 'subject_code': '101', 'subject_name': '人工费', 'subject_level': 1, 'parent_subject_key': '', 'subject_type': '人工成本', 'is_rigid': 0})
    cost_subjects.append({'cost_subject_key': 'CS002', 'subject_code': '102', 'subject_name': '材料费', 'subject_level': 1, 'parent_subject_key': '', 'subject_type': '材料成本', 'is_rigid': 0})
    cost_subjects.append({'cost_subject_key': 'CS003', 'subject_code': '103', 'subject_name': '机械费', 'subject_level': 1, 'parent_subject_key': '', 'subject_type': '机械成本', 'is_rigid': 0})
    cost_subjects.append({'cost_subject_key': 'CS004', 'subject_code': '104', 'subject_name': '管理费', 'subject_level': 1, 'parent_subject_key': '', 'subject_type': '管理费用', 'is_rigid': 0})
    cost_subjects.append({'cost_subject_key': 'CS005', 'subject_code': '10101', 'subject_name': '基本工资', 'subject_level': 2, 'parent_subject_key': 'CS001', 'subject_type': '人工成本', 'is_rigid': 0})
    cost_subjects.append({'cost_subject_key': 'CS006', 'subject_code': '10102', 'subject_name': '绩效工资', 'subject_level': 2, 'parent_subject_key': 'CS001', 'subject_type': '人工成本', 'is_rigid': 0})
    cost_subjects.append({'cost_subject_key': 'CS007', 'subject_code': '10201', 'subject_name': '钢材', 'subject_level': 2, 'parent_subject_key': 'CS002', 'subject_type': '材料成本', 'is_rigid': 1})
    cost_subjects.append({'cost_subject_key': 'CS008', 'subject_code': '10202', 'subject_name': '水泥', 'subject_level': 2, 'parent_subject_key': 'CS002', 'subject_type': '材料成本', 'is_rigid': 1})
    cost_subjects.append({'cost_subject_key': 'CS009', 'subject_code': '10203', 'subject_name': '砂石料', 'subject_level': 2, 'parent_subject_key': 'CS002', 'subject_type': '材料成本', 'is_rigid': 1})
    cost_subjects.append({'cost_subject_key': 'CS010', 'subject_code': '10301', 'subject_name': '大型机械', 'subject_level': 2, 'parent_subject_key': 'CS003', 'subject_type': '机械成本', 'is_rigid': 1})
    cost_subjects.append({'cost_subject_key': 'CS011', 'subject_code': '10302', 'subject_name': '小型机具', 'subject_level': 2, 'parent_subject_key': 'CS003', 'subject_type': '机械成本', 'is_rigid': 0})
    cost_subjects.append({'cost_subject_key': 'CS012', 'subject_code': '10401', 'subject_name': '办公费', 'subject_level': 2, 'parent_subject_key': 'CS004', 'subject_type': '管理费用', 'is_rigid': 0})
    cost_subjects.append({'cost_subject_key': 'CS013', 'subject_code': '10402', 'subject_name': '差旅费', 'subject_level': 2, 'parent_subject_key': 'CS004', 'subject_type': '管理费用', 'is_rigid': 0})
    cost_subjects.append({'cost_subject_key': 'CS014', 'subject_code': '10403', 'subject_name': '招待费', 'subject_level': 2, 'parent_subject_key': 'CS004', 'subject_type': '管理费用', 'is_rigid': 0})
    s.sql.insert_rows('dim_cost_subject', cost_subjects)
    output.print(f"  已插入 {len(cost_subjects)} 条成本科目数据")
    
    # 3. 生成项目数据
    output.print("\n[3/10] 生成项目维表数据...")
    quality_levels = ['A', 'B', 'C']
    quality_weights = [0.2, 0.5, 0.3]
    project_types = ['房建工程', '市政工程', '公路工程', '桥梁工程', '水利工程', '机电安装']
    
    projects = []
    for i in range(50):
        quality_level = random.choices(quality_levels, weights=quality_weights)[0]
        factor = get_quality_factor(quality_level)
        start_dt = generate_random_date(datetime(2024, 1, 1), datetime(2025, 6, 30))
        end_dt = start_dt + timedelta(days=random.randint(90, 730))
        contract_amount = round(random.uniform(1000000, 50000000), 2)
        
        projects.append({
            'project_key': f'P{str(i+1).zfill(6)}',
            'project_name': f'{random.choice(project_types)}项目{i+1}',
            'project_code': f'PRJ{str(i+1).zfill(4)}',
            'project_type': random.choice(project_types),
            'project_stage': random.choice(['前期准备', '在建', '竣工', '结算']),
            'customer_name': f'客户{i+1}',
            'contract_amount_net': round(contract_amount * 0.9, 2),
            'contract_date': start_dt.date(),
            'start_date': start_dt.date(),
            'planned_end_date': end_dt.date(),
            'actual_end_date': end_dt.date() if random.random() > 0.3 else start_dt.date(),
            'quality_level': quality_level,
            'profit_target': round(contract_amount * factor['profit_rate'], 2),
            'status': random.choice(['正常', '风险', '暂停']),
        })
    
    s.sql.insert_rows('dim_project', projects)
    output.print(f"  已插入 {len(projects)} 条项目数据 (A类:{sum(1 for p in projects if p['quality_level']=='A')}, B类:{sum(1 for p in projects if p['quality_level']=='B')}, C类:{sum(1 for p in projects if p['quality_level']=='C')})")
    
    # 4. 生成公司数据
    output.print("\n[4/10] 生成公司维表数据...")
    companies = []
    companies.append({'company_key': 'COM001', 'company_name': '第一分公司', 'company_code': 'COM001', 'company_type': '分公司', 'industry': '建筑施工', 'region': '华东', 'scale': '大型', 'status': '正常'})
    companies.append({'company_key': 'COM002', 'company_name': '第二分公司', 'company_code': 'COM002', 'company_type': '分公司', 'industry': '建筑施工', 'region': '华南', 'scale': '大型', 'status': '正常'})
    companies.append({'company_key': 'COM003', 'company_name': '第三分公司', 'company_code': 'COM003', 'company_type': '分公司', 'industry': '建筑施工', 'region': '华北', 'scale': '中型', 'status': '正常'})
    companies.append({'company_key': 'COM004', 'company_name': '第四分公司', 'company_code': 'COM004', 'company_type': '分公司', 'industry': '建筑施工', 'region': '西南', 'scale': '中型', 'status': '正常'})
    companies.append({'company_key': 'COM005', 'company_name': '第五分公司', 'company_code': 'COM005', 'company_type': '分公司', 'industry': '建筑施工', 'region': '西北', 'scale': '小型', 'status': '正常'})
    s.sql.insert_rows('dim_company', companies)
    output.print(f"  已插入 {len(companies)} 条公司数据")
    
    # 5. 生成供应商数据
    output.print("\n[5/10] 生成供应商维表数据...")
    suppliers = []
    for i in range(20):
        suppliers.append({
            'supplier_key': f'SUP{str(i+1).zfill(4)}',
            'supplier_name': f'供应商{i+1}',
            'supplier_code': f'SUP{str(i+1).zfill(4)}',
            'supplier_type': random.choice(['材料供应商', '劳务供应商', '设备供应商']),
            'region': random.choice(['华东', '华南', '华北', '西南', '西北']),
            'credit_rating': random.choice(['AAA', 'AA', 'A', 'BBB']),
        })
    s.sql.insert_rows('dim_supplier', suppliers)
    output.print("  已插入 20 条供应商数据")
    
    # 6. 生成员工数据
    output.print("\n[6/10] 生成员工维表数据...")
    employees = []
    for i in range(50):
        employees.append({
            'employee_key': f'EMP{str(i+1).zfill(4)}',
            'employee_name': f'员工{i+1}',
            'employee_code': f'E{str(i+1).zfill(4)}',
            'department': random.choice(['工程部', '财务部', '合同部', '成本部']),
            'position': random.choice(['经理', '主管', '专员', '助理']),
            'role': random.choice(['项目经理', '成本专员', '合同管理员', '财务人员']),
        })
    s.sql.insert_rows('dim_employee', employees)
    output.print("  已插入 50 条员工数据")
    
    # 7. 生成项目成本事实数据
    output.print("\n[7/10] 生成项目成本事实数据...")
    costs = []
    for i in range(200):
        project = random.choice(projects)
        subject = random.choice(cost_subjects)
        factor = get_quality_factor(project['quality_level'])
        base_amount = random.uniform(1000, 500000)
        adjusted_amount = round(base_amount * (1 + random.uniform(-factor['cost_deviation'], factor['cost_deviation'])), 2)
        date_dt = generate_random_date(start_date, end_date)
        
        costs.append({
            'project_key': project['project_key'],
            'cost_subject_key': subject['cost_subject_key'],
            'company_key': 'COM001',
            'date_key': generate_date_key(date_dt),
            'calendar_date': date_dt.date(),
            'cost_amount': adjusted_amount,
            'budget_amount': round(adjusted_amount * (1 + random.uniform(-0.1, 0.1)), 2),
        })
    s.sql.insert_rows('fact_project_cost', costs)
    output.print("  已插入 200 条成本数据")
    
    # 8. 生成项目预算事实数据
    output.print("\n[8/10] 生成项目预算事实数据...")
    budgets = []
    for i in range(100):
        project = random.choice(projects)
        subject = random.choice(cost_subjects[:4])
        date_dt = generate_random_date(start_date, end_date)
        
        budgets.append({
            'project_key': project['project_key'],
            'cost_subject_key': subject['cost_subject_key'],
            'date_key': generate_date_key(date_dt),
            'calendar_date': date_dt.date(),
            'budget_amount': round(random.uniform(100000, 1000000), 2),
            'revised_budget_amount': round(random.uniform(100000, 1000000), 2),
        })
    s.sql.insert_rows('fact_project_budget', budgets)
    output.print("  已插入 100 条预算数据")
    
    # 9. 生成项目产出事实数据
    output.print("\n[9/10] 生成项目产出事实数据...")
    outputs = []
    for i in range(150):
        project = random.choice(projects)
        date_dt = generate_random_date(start_date, end_date)
        output_amount = round(random.uniform(50000, 2000000), 2)
        
        outputs.append({
            'project_key': project['project_key'],
            'date_key': generate_date_key(date_dt),
            'calendar_date': date_dt.date(),
            'output_amount': output_amount,
            'confirmed_amount': round(output_amount * random.uniform(0.7, 0.98), 2),
        })
    s.sql.insert_rows('fact_project_output', outputs)
    output.print("  已插入 150 条产出数据")
    
    # 10. 生成风险事实数据
    output.print("\n[10/10] 生成风险事实数据...")
    risks = []
    risk_types = ['成本风险', '进度风险', '质量风险', '安全风险', '资金风险']
    for i in range(50):
        project = random.choice(projects)
        factor = get_quality_factor(project['quality_level'])
        
        if project['quality_level'] == 'C':
            risk_level = random.choices(['正常', '预警', '严重'], weights=[0.2, 0.4, 0.4])[0]
        elif project['quality_level'] == 'B':
            risk_level = random.choices(['正常', '预警', '严重'], weights=[0.5, 0.4, 0.1])[0]
        else:
            risk_level = random.choices(['正常', '预警', '严重'], weights=[0.8, 0.2, 0.0])[0]
        
        date_dt = generate_random_date(start_date, end_date)
        risks.append({
            'risk_key': f'RISK{str(i+1).zfill(6)}',
            'project_key': project['project_key'],
            'date_key': generate_date_key(date_dt),
            'calendar_date': date_dt.date(),
            'risk_type': random.choice(risk_types),
            'risk_level': risk_level,
            'risk_value': round(random.uniform(0, 100), 2),
        })
    s.sql.insert_rows('fact_risk', risks)
    output.print("  已插入 50 条风险数据")
    
    output.success("=== 种子数据生成完成 ===")
    output.print("数据统计:")
    output.print(f"  - 日期维表: {len(date_data)} 天")
    output.print(f"  - 项目: {len(projects)} 个")
    output.print(f"  - 成本科目: {len(cost_subjects)} 条")
    output.print(f"  - 公司: {len(companies)} 条")
    output.print(f"  - 供应商: 20 条")
    output.print(f"  - 员工: 50 条")
    output.print(f"  - 成本记录: 200 条")
    output.print(f"  - 预算记录: 100 条")
    output.print(f"  - 产出记录: 150 条")
    output.print(f"  - 风险记录: 50 条")