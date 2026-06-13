# -*- coding: utf-8 -*-
# 保险同步 - 数据转换节点
# output_variable_name = project_insurance_data

import pandas as pd
import numpy as np

output.print("[保险同步] 开始数据转换")

df = get_variable("insurance_raw_data")
output.print(f"输入数据 shape={df.shape}")
output.print(f"输入列: {list(df.columns)}")

target_fields = ['insurance_id', 'date_key', 'project_id', 'contract_id', 'insurance_type', 'insurance_amount', 'insurance_date', 'expire_date', 'insurance_status', 'insurance_company', 'report_period', 'created_at']

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
    
    insurance_id = str(row['id']) if pd.notnull(row['id']) else ''
    project_id = str(row['project_id']) if pd.notnull(row['project_id']) else ''
    contract_id = str(row['contract_id']) if pd.notnull(row['contract_id']) else ''
    insurance_type = str(row['insurance_type']) if pd.notnull(row['insurance_type']) else ''
    insurance_amount = float(row['insurance_amount']) if pd.notnull(row['insurance_amount']) else 0.0
    insurance_company = str(row['insurance_company']) if pd.notnull(row['insurance_company']) else ''
    
    insurance_date_val = row.get('insurance_date', None)
    if pd.notnull(insurance_date_val):
        try:
            if isinstance(insurance_date_val, pd.Timestamp):
                insurance_date_val = insurance_date_val.to_pydatetime()
            elif isinstance(insurance_date_val, str):
                insurance_date_val = pd.to_datetime(insurance_date_val).to_pydatetime()
        except:
            insurance_date_val = None
    
    expire_date_val = row.get('expire_date', None)
    if pd.notnull(expire_date_val):
        try:
            if isinstance(expire_date_val, pd.Timestamp):
                expire_date_val = expire_date_val.to_pydatetime()
            elif isinstance(expire_date_val, str):
                expire_date_val = pd.to_datetime(expire_date_val).to_pydatetime()
        except:
            expire_date_val = None
    
    status = row.get('insurance_status', None)
    insurance_status_val = str(status) if pd.notnull(status) else ''
    
    result_row = {
        'insurance_id': insurance_id,
        'date_key': int(date_key),
        'project_id': project_id,
        'contract_id': contract_id,
        'insurance_type': insurance_type,
        'insurance_amount': insurance_amount,
        'insurance_date': insurance_date_val,
        'expire_date': expire_date_val,
        'insurance_status': insurance_status_val,
        'insurance_company': insurance_company,
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
output.print("[保险同步] 数据转换完成")