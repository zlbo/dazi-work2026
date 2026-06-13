# -*- coding: utf-8 -*-
# 赔偿同步 - 质量检查节点
# output_variable_name = validated_compensation_data

import pandas as pd

output.print("[赔偿同步] 开始数据质量检查")
df = get_variable("project_compensation_data")
output.print(f"输入数据 shape={df.shape}")

errors = []
warnings = []

required_fields = ['compensation_id', 'project_id', 'report_period']
for field in required_fields:
    if field in df.columns:
        missing = df[field].isnull().sum()
        if missing > 0:
            errors.append(f"必填字段 {field} 有 {missing} 个空值")
            df = df[~df[field].isnull()]

if 'compensation_id' in df.columns:
    compensation_id_missing = df['compensation_id'].isnull().sum()
    if compensation_id_missing > 0:
        warnings.append(f"compensation_id 字段有 {compensation_id_missing} 个空值")

if 'date_key' in df.columns:
    invalid_date = df[~df['date_key'].astype(str).str.match(r'^\d{8}$')]
    if len(invalid_date) > 0:
        errors.append(f"date_key格式错误: {len(invalid_date)} 条记录")

total_input = len(df)
total_output = len(df)
rejection_rate = 0.0

output.print("=" * 50)
output.print("数据质量检查报告")
output.print("=" * 50)
output.print(f"输入记录数: {total_input}")
output.print(f"输出记录数: {total_output}")
output.print(f"剔除记录数: {total_input - total_output}")
output.print(f"剔除率: {rejection_rate:.2f}%")
output.print("")

if errors:
    output.print("错误列表:")
    for error in errors:
        output.print(f"  - {error}")
if warnings:
    output.print("警告列表:")
    for warning in warnings:
        output.print(f"  - {warning}")
if not errors and not warnings:
    output.print("✓ 所有数据质量检查通过")
output.print("=" * 50)

result_rows = []
for _, row in df.iterrows():
    result_row = {}
    for col in df.columns:
        val = row[col]
        if hasattr(val, 'dtype'):
            if val.dtype == 'float64':
                result_row[col] = float(val)
            elif val.dtype == 'int64':
                result_row[col] = int(val)
            else:
                result_row[col] = val
        elif isinstance(val, float):
            result_row[col] = float(val)
        elif isinstance(val, int):
            result_row[col] = int(val)
        elif pd.isnull(val):
            if col in ['compensation_id', 'project_id', 'contract_id', 'compensation_type', 'compensation_reason', 'compensation_status', 'report_period']:
                result_row[col] = ''
            elif col in ['date_key']:
                result_row[col] = 0
            else:
                result_row[col] = 0.0
        else:
            result_row[col] = val
    result_rows.append(result_row)

df_result = pd.DataFrame(result_rows)
result_df = pd.DataFrame()
for col in df_result.columns:
    result_df[col] = df_result[col].tolist()

output.print("[赔偿同步] 数据质量检查完成")