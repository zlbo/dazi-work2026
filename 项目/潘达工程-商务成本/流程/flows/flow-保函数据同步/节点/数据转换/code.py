# -*- coding: utf-8 -*-
# 保函同步 - 数据转换节点
# output_variable_name = project_guarantee_data

import pandas as pd
import numpy as np

output.print("[保函同步] 开始数据转换")

df = get_variable("guarantee_raw_data")
output.print(f"输入数据 shape={df.shape}")
output.print(f"输入列: {list(df.columns)}")

target_fields = ['guarantee_id', 'date_key', 'project_id', 'contract_id', 'guarantee_type', 'guarantee_amount', 'guarantee_date', 'expire_date', 'guarantee_status', 'report_period', 'created_at']

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
    
    guarantee_id = str(row['id']) if pd.notnull(row['id']) else ''
    project_id = str(row['project_id']) if pd.notnull(row['project_id']) else ''
    contract_id = str(row['contract_id']) if pd.notnull(row['contract_id']) else ''
    guarantee_type = str(row['guarantee_type']) if pd.notnull(row['guarantee_type']) else ''
    guarantee_amount = float(row['guarantee_amount']) if pd.notnull(row['guarantee_amount']) else 0.0
    
    guarantee_date_val = row.get('guarantee_date', None)
    if pd.notnull(guarantee_date_val):
        try:
            if isinstance(guarantee_date_val, pd.Timestamp):
                guarantee_date_val = guarantee_date_val.to_pydatetime()
            elif isinstance(guarantee_date_val, str):
                guarantee_date_val = pd.to_datetime(guarantee_date_val).to_pydatetime()
        except:
            guarantee_date_val = None
    
    expire_date_val = row.get('expire_date', None)
    if pd.notnull(expire_date_val):
        try:
            if isinstance(expire_date_val, pd.Timestamp):
                expire_date_val = expire_date_val.to_pydatetime()
            elif isinstance(expire_date_val, str):
                expire_date_val = pd.to_datetime(expire_date_val).to_pydatetime()
        except:
            expire_date_val = None
    
    status = row.get('guarantee_status', None)
    guarantee_status_val = str(status) if pd.notnull(status) else ''
    
    result_row = {
        'guarantee_id': guarantee_id,
        'date_key': int(date_key),
        'project_id': project_id,
        'contract_id': contract_id,
        'guarantee_type': guarantee_type,
        'guarantee_amount': guarantee_amount,
        'guarantee_date': guarantee_date_val,
        'expire_date': expire_date_val,
        'guarantee_status': guarantee_status_val,
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
output.print("[保函同步] 数据转换完成")