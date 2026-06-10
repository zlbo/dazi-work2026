# -*- coding: utf-8 -*-
# 上游 sql-query 的 output_variable_name = cost_data
# 本节点 output_variable_name = project_cost_data
import pandas as pd

output.print("[python-script] 开始成本数据转换")

if df is None or df.empty:
    df = get_variable("cost_data")
    output.print(f"从变量获取数据 shape={df.shape}")
else:
    output.print(f"从入边获取数据 shape={df.shape}")

output.print(f"输入列: {list(df.columns)}")

result_df = df.copy()

result_df['cost_total_acc'] = result_df['cost_confirmed_acc'] + result_df['cost_unconfirmed_acc']
result_df['direct_cost_acc'] = result_df['labor_cost_acc'] + result_df['material_cost_acc'] + result_df['equipment_cost_acc']

result_df['data_source'] = 'tb_project_cost'
result_df['sync_time'] = pd.Timestamp.now()

output.print(f"输出 shape={result_df.shape}")
output.print(f"输出列: {list(result_df.columns)}")

output.print("[python-script] 成本数据转换完成")