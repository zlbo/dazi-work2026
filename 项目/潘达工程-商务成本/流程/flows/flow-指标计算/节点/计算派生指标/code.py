# -*- coding: utf-8 -*-
# 上游变量来源：
# - output_data: 从 flow-001 获取产值数据
# - cost_data: 从 flow-002 获取成本数据
# - payment_data: 从 flow-003 获取付款数据
# - balance_data: 从 flow-004 获取收支数据
# 本节点 output_variable_name = project_indicator_data
import pandas as pd

output.print("[python-script] 开始计算派生指标")

output_data = get_variable("output_data")
cost_data = get_variable("cost_data")
payment_data = get_variable("payment_data")
balance_data = get_variable("balance_data")

output.print(f"产值数据 shape={output_data.shape}")
output.print(f"成本数据 shape={cost_data.shape}")
output.print(f"付款数据 shape={payment_data.shape}")
output.print(f"收支数据 shape={balance_data.shape}")

merged_df = output_data.merge(cost_data, on=['project_id', 'report_period'], how='outer')
merged_df = merged_df.merge(payment_data, on=['project_id', 'report_period'], how='outer')
merged_df = merged_df.merge(balance_data, on=['project_id', 'report_period'], how='outer')

result_df = merged_df.copy()

result_df['profit_rate'] = (result_df['output_confirmed'] - result_df['cost_confirmed_acc']) / result_df['output_confirmed'] * 100
result_df['cost_rate'] = result_df['cost_confirmed_acc'] / result_df['output_confirmed'] * 100
result_df['payment_rate'] = result_df['paid_amount'] / result_df['payable_confirmed'] * 100 if result_df['payable_confirmed'].sum() > 0 else 0
result_df['gross_profit_rate'] = (result_df['output_confirmed'] - result_df['cost_confirmed_acc']) / result_df['output_confirmed'] * 100

result_df['indicator_level'] = 'L2'
result_df['data_source'] = 'flow-005-指标计算'
result_df['calc_time'] = pd.Timestamp.now()

output.print(f"输出 shape={result_df.shape}")
output.print(f"输出列: {list(result_df.columns)}")

output.print("[python-script] 派生指标计算完成")