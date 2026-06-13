# -*- coding: utf-8 -*-
# 设备同步 - 数据转换节点
# output_variable_name = project_equipment_data

import pandas as pd
import numpy as np

output.print("[设备同步] 开始数据转换")

df = get_variable("equipment_raw_data")
output.print(f"输入数据 shape={df.shape}")
output.print(f"输入列: {list(df.columns)}")

target_fields = ['equipment_id', 'date_key', 'project_id', 'contract_id', 'equipment_code', 'equipment_name', 'equipment_type', 'equipment_value', 'purchase_date', 'equipment_status', 'depreciation_method', 'report_period', 'created_at']

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
    
    equipment_id = str(row['id']) if pd.notnull(row['id']) else ''
    project_id = str(row['project_id']) if pd.notnull(row['project_id']) else ''
    contract_id = str(row['contract_id']) if pd.notnull(row['contract_id']) else ''
    equipment_code = str(row['equipment_code']) if pd.notnull(row['equipment_code']) else ''
    equipment_name = str(row['equipment_name']) if pd.notnull(row['equipment_name']) else ''
    equipment_type = str(row['equipment_type']) if pd.notnull(row['equipment_type']) else ''
    equipment_value = float(row['equipment_value']) if pd.notnull(row['equipment_value']) else 0.0
    depreciation_method = str(row['depreciation_method']) if pd.notnull(row['depreciation_method']) else ''
    
    purchase_date_val = row.get('purchase_date', None)
    if pd.notnull(purchase_date_val):
        try:
            if isinstance(purchase_date_val, pd.Timestamp):
                purchase_date_val = purchase_date_val.to_pydatetime()
            elif isinstance(purchase_date_val, str):
                purchase_date_val = pd.to_datetime(purchase_date_val).to_pydatetime()
        except:
            purchase_date_val = None
    
    status = row.get('equipment_status', None)
    equipment_status_val = str(status) if pd.notnull(status) else ''
    
    result_row = {
        'equipment_id': equipment_id,
        'date_key': int(date_key),
        'project_id': project_id,
        'contract_id': contract_id,
        'equipment_code': equipment_code,
        'equipment_name': equipment_name,
        'equipment_type': equipment_type,
        'equipment_value': equipment_value,
        'purchase_date': purchase_date_val,
        'equipment_status': equipment_status_val,
        'depreciation_method': depreciation_method,
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
output.print("[设备同步] 数据转换完成")