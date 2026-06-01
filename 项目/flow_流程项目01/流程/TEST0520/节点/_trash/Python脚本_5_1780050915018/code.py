import pandas as pd

# 获取输入数据
df = get_variable('前5条')

# 选择需要的列
df = df[['地区', '产品', '规格']]

# 必须：主输出 DataFrame
result_df = df
