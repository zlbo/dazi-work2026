# -*- coding: utf-8 -*-
# 成本同步 - 数据转换节点
# output_variable_name = project_cost_data

import pandas as pd
import numpy as np

output.print("[成本同步] 开始数据转换")

# 获取上游数据
df = get_variable("cost_raw_data")
output.print(f"输入数据 shape={df.shape}")
output.print(f"输入列: {list(df.columns)}")

# 定义目标表字段
target_fields = [
    'cost_id', 'report_period', 'cost_confirmed_acc', 'cost_unconfirmed_acc',
    'cost_confirmed_cmonth', 'cost_unconfirmed_cmonth', 'labor_cost_acc',
    'material_cost_acc', 'equipment_cost_acc', 'management_fee_rate',
    'target_cost', 'cost_code', 'cost_name', 'created_at', 'project_id',
    'date_key', 'company_id', 'project_name', 'contract_id', 'cost_level'
]

# 创建结果列表，逐行处理确保类型正确
result_rows = []
current_time = pd.Timestamp.now().to_pydatetime() # 转换为 Python datetime

for _, row in df.iterrows():
    # 计算日期键
    try:
        year = int(row['year'])
        month = int(row['month'])
        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = 31
        elif month == 2:
            if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
                day = 29
            else:
                day = 28
        else:
            day = 30
        date_key = year * 10000 + month * 100 + day
        report_period = f"{int(row['year'])}-{int(row['month']):02d}" if pd.notnull(row['year']) and pd.notnull(row['month']) else ''
    except:
        date_key = 0
        report_period = ''
    
    # 确保所有值都是 Python 原生类型
    cost_id = str(row['id']) if pd.notnull(row['id']) else ''
    project_id = str(row['project_id']) if pd.notnull(row['project_id']) else ''
    project_name = str(row['name']) if pd.notnull(row['name']) else ''
    contract_id = str(row['contract_id']) if pd.notnull(row['contract_id']) else ''
    cost_code = str(row['cost_code']) if pd.notnull(row['cost_code']) else ''
    cost_name = str(row['name']) if pd.notnull(row['name']) else ''
    
    # 从数据源获取成本数据
    cost_confirmed_acc = float(row['cost_actual_confirmed_acc']) if pd.notnull(row['cost_actual_confirmed_acc']) else 0.0
    cost_unconfirmed_acc = float(row['cost_actual_unconfirmed_acc']) if pd.notnull(row['cost_actual_unconfirmed_acc']) else 0.0
    cost_confirmed_cmonth = float(row['cost_actual_confirmed_cmonth']) if pd.notnull(row['cost_actual_confirmed_cmonth']) else 0.0
    cost_unconfirmed_cmonth = float(row['cost_actual_unconfirmed_cmonth']) if pd.notnull(row['cost_actual_unconfirmed_cmonth']) else 0.0
    labor_cost_acc = float(row['cost_actual_labor_acc']) if pd.notnull(row['cost_actual_labor_acc']) else 0.0
    target_cost = float(row['base_contract_amount']) if pd.notnull(row['base_contract_amount']) else 0.0
    
    # 处理层级
    level = row.get('level')
    cost_level = ''
    if pd.notnull(level):
        level_int = int(level)
        if level_int == 1:
            cost_level = 'L1'
        elif level_int == 2:
            cost_level = 'L2'
        elif level_int == 3:
            cost_level = 'L3'
    
    # 构建行数据
    result_row = {
        'cost_id': cost_id,
        'report_period': report_period,
        'cost_confirmed_acc': cost_confirmed_acc,
        'cost_unconfirmed_acc': cost_unconfirmed_acc,
        'cost_confirmed_cmonth': cost_confirmed_cmonth,
        'cost_unconfirmed_cmonth': cost_unconfirmed_cmonth,
        'labor_cost_acc': labor_cost_acc,
        'material_cost_acc': 0.0,
        'equipment_cost_acc': 0.0,
        'management_fee_rate': 0.0,
        'target_cost': target_cost,
        'cost_code': cost_code,
        'cost_name': cost_name,
        'created_at': current_time,
        'project_id': project_id,
        'date_key': int(date_key),
        'company_id': '',
        'project_name': project_name,
        'contract_id': contract_id,
        'cost_level': cost_level
    }
    result_rows.append(result_row)

# 转换为 DataFrame
df_result = pd.DataFrame(result_rows, columns=target_fields)

# 强制转换所有列为 Python 原生类型 (SOP 2.2 核心要求)
result_df = pd.DataFrame()
for col in df_result.columns:
    result_df[col] = df_result[col].tolist()

output.print(f"输出 shape={result_df.shape}")
output.print(f"输出列: {list(result_df.columns)}")

output.print("[成本同步] 数据转换完成")
