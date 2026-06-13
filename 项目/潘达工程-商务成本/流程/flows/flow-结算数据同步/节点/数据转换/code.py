# -*- coding: utf-8 -*-
# 结算同步 - 数据转换节点
# output_variable_name = project_settlement_data

import pandas as pd
import numpy as np

output.print("[结算同步] 开始数据转换")

# 获取上游数据
df = get_variable("settlement_raw_data")
output.print(f"输入数据 shape={df.shape}")
output.print(f"输入列: {list(df.columns)}")

# 定义目标表字段
target_fields = [
    'settlement_id', 'date_key', 'contract_id', 'contract_name', 
    'contract_amount', 'settlement_amount', 'settlement_date',
    'settlement_status', 'report_period', 'project_id', 'created_at', 'contract_code'
]

# 创建结果列表，逐行处理确保类型正确
result_rows = []
current_time = pd.Timestamp.now().to_pydatetime()

for _, row in df.iterrows():
    # 计算日期键
    try:
        year = int(row['year']) if pd.notnull(row['year']) else 2025
        month = int(row['month']) if pd.notnull(row['month']) else 1
        
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
        report_period = f"{int(year)}-{int(month):02d}"
    except:
        date_key = 0
        report_period = ''
    
    # 确保所有值都是 Python 原生类型
    settlement_id = str(row['id']) if pd.notnull(row['id']) else ''
    project_id = str(row['project_id']) if pd.notnull(row['project_id']) else ''
    contract_id = str(row['contract_id']) if pd.notnull(row['contract_id']) else ''
    contract_name = str(row['base_contract_name']) if pd.notnull(row['base_contract_name']) else ''
    contract_code = str(row['base_contract_code']) if pd.notnull(row['base_contract_code']) else ''
    
    # 转换金额值
    contract_amount = float(row['base_contract_amount']) if pd.notnull(row['base_contract_amount']) else 0.0
    settlement_amount = float(row['settlement_amount']) if pd.notnull(row['settlement_amount']) else 0.0
    
    # 处理结算日期
    settlement_date_val = row.get('settlement_date', None)
    if pd.notnull(settlement_date_val):
        try:
            if isinstance(settlement_date_val, pd.Timestamp):
                settlement_date_val = settlement_date_val.to_pydatetime()
            elif isinstance(settlement_date_val, str):
                settlement_date_val = pd.to_datetime(settlement_date_val).to_pydatetime()
        except:
            settlement_date_val = None
    
    # 处理结算状态
    status = row.get('settlement_status', None)
    if pd.notnull(status):
        status = str(status)
        if status == '1' or status == '已结算':
            settlement_status_val = '已结算'
        elif status == '0' or status == '未结算':
            settlement_status_val = '未结算'
        else:
            settlement_status_val = status
    else:
        settlement_status_val = ''
    
    # 构建行数据
    result_row = {
        'settlement_id': settlement_id,
        'date_key': int(date_key),
        'contract_id': contract_id,
        'contract_name': contract_name,
        'contract_amount': contract_amount,
        'settlement_amount': settlement_amount,
        'settlement_date': settlement_date_val,
        'settlement_status': settlement_status_val,
        'report_period': report_period,
        'project_id': project_id,
        'created_at': current_time,
        'contract_code': contract_code
    }
    result_rows.append(result_row)

# 转换为 DataFrame
df_result = pd.DataFrame(result_rows, columns=target_fields)

# 强制转换所有列为 Python 原生类型
result_df = pd.DataFrame()
for col in df_result.columns:
    result_df[col] = df_result[col].tolist()

output.print(f"输出 shape={result_df.shape}")
output.print(f"输出列: {list(result_df.columns)}")

output.print("[结算同步] 数据转换完成")