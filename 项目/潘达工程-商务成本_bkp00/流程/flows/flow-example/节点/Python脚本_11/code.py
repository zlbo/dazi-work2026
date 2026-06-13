import pandas as pd

# 获取输入数据
df1 = get_variable('fact_actual')
df2 = get_variable('dim_actual_account')

# 关联两张表
merged_df = pd.merge(df1, df2, left_on='actual_account_code', right_on='account_code', how='inner')

# 获取不重复的列名
unique_columns = []
for col in merged_df.columns:
    if col not in unique_columns:
        unique_columns.append(col)

# 筛选不重复的列
result_df = merged_df[unique_columns]
