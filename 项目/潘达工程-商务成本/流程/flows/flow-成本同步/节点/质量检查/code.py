# -*- coding: utf-8 -*-
# 成本同步 - 质量检查节点
# output_variable_name = validated_cost_data

import pandas as pd

output.print("[成本同步] 开始数据质量检查")

# 获取上游数据
df = get_variable("project_cost_data")
output.print(f"输入数据 shape={df.shape}")

validated_df = df.copy()
errors = []
warnings = []

# 1. 必填字段检查
required_fields = ['cost_id', 'project_id', 'report_period']
for field in required_fields:
    missing = validated_df[field].isnull().sum()
    if missing > 0:
        errors.append(f"必填字段 {field} 有 {missing} 个空值")
        validated_df = validated_df[~validated_df[field].isnull()]

# 2. 金额范围检查
amount_fields = ['pay_amount', 'tax_amount', 'total_amount']
for field in amount_fields:
    if field in validated_df.columns:
        negative = validated_df[validated_df[field] < 0]
        if len(negative) > 0:
            warnings.append(f"{field} 有 {len(negative)} 条负数记录")

# 3. 日期格式检查
if 'date_key' in validated_df.columns:
    invalid_date = validated_df[~validated_df['date_key'].astype(str).str.match(r'^\d{8}$')]
    if len(invalid_date) > 0:
        errors.append(f"date_key格式错误: {len(invalid_date)} 条记录")

# 4. 数据完整性检查
total_input = len(df)
total_output = len(validated_df)
rejection_rate = ((total_input - total_output) / total_input * 100) if total_input > 0 else 0

# 输出检查结果
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

output.print("[成本同步] 数据质量检查完成")