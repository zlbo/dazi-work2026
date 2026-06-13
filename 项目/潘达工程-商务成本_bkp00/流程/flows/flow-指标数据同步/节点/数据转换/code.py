# -*- coding: utf-8 -*-
# 指标同步 - 数据转换节点
# output_variable_name = project_indicator_data

import pandas as pd
import numpy as np

output.print("[指标同步] 开始数据转换")

# 获取上游数据
df = get_variable("indicator_raw_data")
output.print(f"输入数据 shape={df.shape}")
output.print(f"输入列: {list(df.columns)}")

# 定义目标表字段
target_fields = [
    'indicator_id', 'date_key', 'project_id', 'indicator_code', 
    'indicator_name', 'report_period', 'indicator_value', 
    'target_value', 'warning_level', 'remark', 'created_at', 'company_id'
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
    indicator_id = str(row['id']) if pd.notnull(row['id']) else ''
    project_id = str(row['project_id']) if pd.notnull(row['project_id']) else ''
    indicator_code = str(row['code']) if pd.notnull(row['code']) else ''
    indicator_name = str(row['title']) if pd.notnull(row['title']) else ''
    remark = str(row['remark']) if pd.notnull(row['remark']) else ''
    
    # 转换指标值
    indicator_value = 0.0
    try:
        val = row['value']
        if pd.notnull(val) and val != '':
            indicator_value = float(val)
    except:
        indicator_value = 0.0
    
    # 构建行数据
    result_row = {
        'indicator_id': indicator_id,
        'date_key': int(date_key),
        'project_id': project_id,
        'indicator_code': indicator_code,
        'indicator_name': indicator_name,
        'report_period': report_period,
        'indicator_value': indicator_value,
        'target_value': 0.0,
        'warning_level': '',
        'remark': remark,
        'created_at': current_time,
        'company_id': ''
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

output.print("[指标同步] 数据转换完成")
