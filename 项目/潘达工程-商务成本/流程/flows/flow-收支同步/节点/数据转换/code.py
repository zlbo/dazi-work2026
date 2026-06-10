# -*- coding: utf-8 -*-
# 上游 sql-query 的 output_variable_name = balance_data
# 本节点 output_variable_name = project_balance_data
import pandas as pd

output.print("[python-script] 开始收支数据转换")

if df is None or df.empty:
    df = get_variable("balance_data")
    output.print(f"从变量获取数据 shape={df.shape}")
else:
    output.print(f"从入边获取数据 shape={df.shape}")

output.print(f"输入列: {list(df.columns)}")

result_df = df.copy()

result_df['net_balance'] = result_df['income_total'] - result_df['outcome_total']
result_df['income_rate'] = result_df['income_confirmed'] / result_df['income_total'] * 100 if result_df['income_total'].sum() > 0 else 0
result_df['outcome_rate'] = result_df['outcome_confirmed'] / result_df['outcome_total'] * 100 if result_df['outcome_total'].sum() > 0 else 0

result_df['data_source'] = 'tb_project_balance'
result_df['sync_time'] = pd.Timestamp.now()

output.print(f"输出 shape={result_df.shape}")
output.print(f"输出列: {list(result_df.columns)}")

output.print("[python-script] 收支数据转换完成")