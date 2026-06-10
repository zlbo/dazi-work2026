# -*- coding: utf-8 -*-
# 产值同步 - 数据转换节点
# output_variable_name = project_output_data

import pandas as pd
import numpy as np

output.print("[产值同步] 开始数据转换")

# 获取上游数据
df = get_variable("output_raw_data")
output.print(f"输入数据 shape={df.shape}")
output.print(f"输入列: {list(df.columns)}")

# 定义目标表字段
target_fields = [
    'output_id', 'date_key', 'project_id', 'project_name', 
    'unconfirmed_output', 'output_last_year_confirmed', 'output_last_year_unconfirmed',
    'output_current_confirmed', 'output_current_unconfirmed',
    'total_output', 'created_at', 'confirmed_output', 'report_period', 'company_id'
]

# 创建结果列表，逐行处理确保类型正确
result_rows = []
current_time = pd.Timestamp.now()

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
    except:
        date_key = 0
    
    # 确保所有值都是 Python 原生类型
    output_id = str(row['id']) if pd.notnull(row['id']) else ''
    project_id = str(row['project_id']) if pd.notnull(row['project_id']) else ''
    project_name = str(row['name']) if pd.notnull(row['name']) else ''
    company_amount = float(row['company_amount']) if pd.notnull(row['company_amount']) else 0.0
    project_amount = float(row['project_amount']) if pd.notnull(row['project_amount']) else 0.0
    total = float(row['total']) if pd.notnull(row['total']) else 0.0
    report_period = f"{int(row['year'])}-{int(row['month']):02d}" if pd.notnull(row['year']) and pd.notnull(row['month']) else ''
    
    # 构建行数据
    result_row = {
        'output_id': output_id,
        'date_key': int(date_key),
        'project_id': project_id,
        'project_name': project_name,
        'unconfirmed_output': company_amount,
        'output_last_year_confirmed': 0.0,
        'output_last_year_unconfirmed': 0.0,
        'output_current_confirmed': project_amount,
        'output_current_unconfirmed': company_amount,
        'total_output': total,
        'created_at': current_time,
        'confirmed_output': project_amount,
        'report_period': report_period,
        'company_id': ''
    }
    result_rows.append(result_row)

# 转换为 DataFrame
result_df = pd.DataFrame(result_rows, columns=target_fields)

output.print(f"输出 shape={result_df.shape}")
output.print(f"输出列: {list(result_df.columns)}")

output.print("[产值同步] 数据转换完成")