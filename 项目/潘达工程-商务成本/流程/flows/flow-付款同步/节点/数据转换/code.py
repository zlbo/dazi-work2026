# -*- coding: utf-8 -*-
# 上游 sql-query 的 output_variable_name = payment_data
# 本节点 output_variable_name = project_payment_data
import pandas as pd

output.print("[python-script] 开始付款数据转换")

if df is None or df.empty:
    df = get_variable("payment_data")
    output.print(f"从变量获取数据 shape={df.shape}")
else:
    output.print(f"从入边获取数据 shape={df.shape}")

output.print(f"输入列: {list(df.columns)}")

result_df = df.copy()

result_df['payable_total'] = result_df['payable_confirmed'] + result_df['payable_unconfirmed']
result_df['unpaid_amount'] = result_df['payable_total'] - result_df['paid_amount']

result_df['data_source'] = 'tb_project_payment'
result_df['sync_time'] = pd.Timestamp.now()

output.print(f"输出 shape={result_df.shape}")
output.print(f"输出列: {list(result_df.columns)}")

output.print("[python-script] 付款数据转换完成")