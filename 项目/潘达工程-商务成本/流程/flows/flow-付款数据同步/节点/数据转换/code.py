# -*- coding: utf-8 -*-
# 付款同步 - 数据转换节点
# output_variable_name = project_payment_data

import pandas as pd
import numpy as np

output.print("[付款同步] 开始数据转换")

# 获取上游数据
df = get_variable("payment_raw_data")
output.print(f"输入数据 shape={df.shape}")
output.print(f"输入列: {list(df.columns)}")

# 定义目标表字段
target_fields = [
    'payment_id', 'date_key', 'contract_id', 'contract_name', 
    'contract_amount', 'settlement_status', 'supplier_id',
    'report_period', 'payable_confirmed', 'payable_unconfirmed',
    'labor_payable', 'approval_status', 'approval_amount',
    'paid_amount', 'tax_rate', 'payment_ratio', 'project_id',
    'created_at', 'supplier_name', 'contract_code'
]

# 创建结果列表，逐行处理确保类型正确
result_rows = []
current_time = pd.Timestamp.now().to_pydatetime() # 转换为 Python datetime

for _, row in df.iterrows():
    # 计算日期键
    try:
        # 从 year 和 month 字段提取
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
    payment_id = str(row['id']) if pd.notnull(row['id']) else ''
    project_id = str(row['project_id']) if pd.notnull(row['project_id']) else ''
    contract_id = str(row['contract_id']) if pd.notnull(row['contract_id']) else ''
    contract_name = str(row['base_contract_name']) if pd.notnull(row['base_contract_name']) else ''
    contract_code = str(row['base_contract_code']) if pd.notnull(row['base_contract_code']) else ''
    
    # 转换金额值
    contract_amount = float(row['base_contract_amount']) if pd.notnull(row['base_contract_amount']) else 0.0
    payable_confirmed = float(row['cost_actual_confirmed_acc']) if pd.notnull(row['cost_actual_confirmed_acc']) else 0.0
    payable_unconfirmed = float(row['cost_actual_unconfirmed_acc']) if pd.notnull(row['cost_actual_unconfirmed_acc']) else 0.0
    labor_payable = float(row['cost_actual_labor_acc']) if pd.notnull(row['cost_actual_labor_acc']) else 0.0
    approval_amount = float(row['fund_plan_approve_amount']) if pd.notnull(row['fund_plan_approve_amount']) else 0.0
    paid_amount = float(row['pay_amount_acc']) if pd.notnull(row['pay_amount_acc']) else 0.0
    tax_rate = float(row['base_contract_tax_rate']) if pd.notnull(row['base_contract_tax_rate']) else 0.09
    payment_ratio = float(row['base_contract_pay_ratio']) if pd.notnull(row['base_contract_pay_ratio']) else 0.0
    
    # 转换结算状态
    is_settlement = row.get('base_contract_is_settlement', None)
    if pd.notnull(is_settlement):
        if is_settlement == 1 or is_settlement == '1' or is_settlement is True:
            settlement_status = '已结算'
        else:
            settlement_status = '进行中'
    else:
        settlement_status = ''
    
    # 构建行数据
    result_row = {
        'payment_id': payment_id,
        'date_key': int(date_key),
        'contract_id': contract_id,
        'contract_name': contract_name,
        'contract_amount': contract_amount,
        'settlement_status': settlement_status,
        'supplier_id': '',
        'report_period': report_period,
        'payable_confirmed': payable_confirmed,
        'payable_unconfirmed': payable_unconfirmed,
        'labor_payable': labor_payable,
        'approval_status': '',
        'approval_amount': approval_amount,
        'paid_amount': paid_amount,
        'tax_rate': tax_rate,
        'payment_ratio': payment_ratio,
        'project_id': project_id,
        'created_at': current_time,
        'supplier_name': '',
        'contract_code': contract_code
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

output.print("[付款同步] 数据转换完成")
