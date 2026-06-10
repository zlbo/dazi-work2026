# -*- coding: utf-8 -*-
# 成本同步 - 数据转换节点
# output_variable_name = project_cost_data

import pandas as pd

output.print("[成本同步] 开始数据转换")

# 获取上游数据
df = get_variable("cost_raw_data")
output.print(f"输入数据 shape={df.shape}")
output.print(f"输入列: {list(df.columns)}")

result_df = df.copy()

# ========== 字段重命名 ==========
field_mapping = {
    'id': 'cost_id',
    'pay_amount': 'amount_without_tax',
    'total_amount': 'amount_with_tax'
}
result_df = result_df.rename(columns=field_mapping)

# ========== 派生字段计算 ==========
def calculate_date_key(report_period):
    try:
        year = int(report_period[:4])
        month = int(report_period[5:7])
        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = 31
        elif month == 2:
            if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
                day = 29
            else:
                day = 28
        else:
            day = 30
        return year * 10000 + month * 100 + day
    except:
        return None

result_df['date_key'] = result_df['report_period'].apply(calculate_date_key)
result_df['cost_ratio'] = result_df['amount_without_tax'] / result_df['amount_with_tax'].replace(0, 1)

# ========== 数据类型转换 ==========
result_df['pay_amount'] = pd.to_numeric(result_df['pay_amount'], errors='coerce')
result_df['tax_amount'] = pd.to_numeric(result_df['tax_amount'], errors='coerce')
result_df['total_amount'] = pd.to_numeric(result_df['total_amount'], errors='coerce')

# 添加元数据字段
result_df['data_source'] = 'tb_project_cost_pay_detail'
result_df['sync_time'] = pd.Timestamp.now()

output.print(f"输出 shape={result_df.shape}")
output.print(f"输出列: {list(result_df.columns)}")

output.print("[成本同步] 数据转换完成")