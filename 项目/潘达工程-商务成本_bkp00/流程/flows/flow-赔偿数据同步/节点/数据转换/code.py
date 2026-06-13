# -*- coding: utf-8 -*-
# 赔偿同步 - 数据转换节点
# output_variable_name = project_compensation_data

import pandas as pd
import numpy as np

output.print("[赔偿同步] 开始数据转换")

df = get_variable("compensation_raw_data")
output.print(f"输入数据 shape={df.shape}")
output.print(f"输入列: {list(df.columns)}")

target_fields = ['compensation_id', 'date_key', 'project_id', 'contract_id', 'compensation_type', 'compensation_amount', 'compensation_date', 'compensation_reason', 'compensation_status', 'report_period', 'created_at']

result_rows = []
current_time = pd.Timestamp.now().to_pydatetime()

for _, row in df.iterrows():
    try:
        year = int(row['year']) if pd.notnull(row['year']) else 2025
        month = int(row['month']) if pd.notnull(row['month']) else 1
        day = 31 if month in [1,3,5,7,8,10,12] else (29 if (month==2 and (year%4==0 and year%100!=0 or year%400==0)) else (28 if month==2 else 30))
        date_key = year * 10000 + month * 100 + day
        report_period = f"{int(year)}-{int(month):02d}"
    except:
        date_key = 0
        report_period = ''
    
    compensation_id = str(row['id']) if pd.notnull(row['id']) else ''
    project_id = str(row['project_id']) if pd.notnull(row['project_id']) else ''
    contract_id = str(row['contract_id']) if pd.notnull(row['contract_id']) else ''
    compensation_type = str(row['compensation_type']) if pd.notnull(row['compensation_type']) else ''
    compensation_amount = float(row['compensation_amount']) if pd.notnull(row['compensation_amount']) else 0.0
    compensation_reason = str(row['compensation_reason']) if pd.notnull(row['compensation_reason']) else ''
    
    compensation_date_val = row.get('compensation_date', None)
    if pd.notnull(compensation_date_val):
        try:
            if isinstance(compensation_date_val, pd.Timestamp):
                compensation_date_val = compensation_date_val.to_pydatetime()
            elif isinstance(compensation_date_val, str):
                compensation_date_val = pd.to_datetime(compensation_date_val).to_pydatetime()
        except:
            compensation_date_val = None
    
    status = row.get('compensation_status', None)
    compensation_status_val = str(status) if pd.notnull(status) else ''
    
    result_row = {
        'compensation_id': compensation_id,
        'date_key': int(date_key),
        'project_id': project_id,
        'contract_id': contract_id,
        'compensation_type': compensation_type,
        'compensation_amount': compensation_amount,
        'compensation_date': compensation_date_val,
        'compensation_reason': compensation_reason,
        'compensation_status': compensation_status_val,
        'report_period': report_period,
        'created_at': current_time
    }
    result_rows.append(result_row)

df_result = pd.DataFrame(result_rows, columns=target_fields)
result_df = pd.DataFrame()
for col in df_result.columns:
    result_df[col] = df_result[col].tolist()

output.print(f"输出 shape={result_df.shape}")
output.print(f"输出列: {list(result_df.columns)}")
output.print("[赔偿同步] 数据转换完成")