# -*- coding: utf-8 -*-
# 风险同步 - 数据转换节点
# output_variable_name = project_risk_data

import pandas as pd
import numpy as np

output.print("[风险同步] 开始数据转换")

# 获取上游数据
df = get_variable("risk_raw_data")
output.print(f"输入数据 shape={df.shape}")
output.print(f"输入列: {list(df.columns)}")

# 定义目标表字段
target_fields = [
    'risk_id', 'date_key', 'project_id', 'risk_type', 
    'risk_code', 'risk_name', 'risk_value', 'warning_level', 
    'risk_description', 'overall_warning_level', 'report_period', 'created_at'
]

# 创建结果列表，逐行处理确保类型正确
result_rows = []
current_time = pd.Timestamp.now().to_pydatetime() # 转换为 Python datetime

for _, row in df.iterrows():
    # 计算日期键
    try:
        year = int(row['year']) if pd.notnull(row['year']) else 0
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
        report_period = f"{int(row['year'])}-{int(row['month']):02d}" if pd.notnull(row['year']) and pd.notnull(row['month']) else ''
    except:
        date_key = 0
        report_period = ''
    
    # 确保所有值都是 Python 原生类型
    risk_id = str(row['id']) if pd.notnull(row['id']) else ''
    project_id = str(row['project_id']) if pd.notnull(row['project_id']) else ''
    risk_type = str(row['risk_type']) if pd.notnull(row['risk_type']) else ''
    risk_code = str(row['code']) if pd.notnull(row['code']) else ''
    risk_name = str(row['name']) if pd.notnull(row['name']) else ''
    risk_description = str(row['analyse_reason']) if pd.notnull(row['analyse_reason']) else ''
    
    # 转换 warning 值（1=红, 2=黄, 3=绿）
    warning_val = row['warning']
    if pd.notnull(warning_val):
        warning_val_str = str(warning_val).strip()
        if warning_val_str == '1':
            warning_level = 'red'
        elif warning_val_str == '2':
            warning_level = 'yellow'
        elif warning_val_str == '3':
            warning_level = 'green'
        else:
            warning_level = warning_val_str
    else:
        warning_level = ''
    
    # 转换风险值
    risk_value = 0
    try:
        val = row['value']
        if pd.notnull(val) and val != '':
            risk_value = int(float(val))
    except:
        risk_value = 0
    
    # 构建行数据
    result_row = {
        'risk_id': risk_id,
        'date_key': int(date_key),
        'project_id': project_id,
        'risk_type': risk_type,
        'risk_code': risk_code,
        'risk_name': risk_name,
        'risk_value': risk_value,
        'warning_level': warning_level,
        'risk_description': risk_description,
        'overall_warning_level': '',
        'report_period': report_period,
        'created_at': current_time
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

output.print("[风险同步] 数据转换完成")
