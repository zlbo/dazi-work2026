import pandas as pd

# 获取输入数据
df1 = get_variable('fact_budget')
df2 = get_variable('dim_budget_account')

# 关联两张表
df = pd.merge(df1, df2, how='inner', left_on='budget_account_code', right_on='account_code')

# 返回结果
result_df = df
