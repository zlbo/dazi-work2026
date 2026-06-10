import pandas as pd
from datetime import datetime

# 获取输入数据
input_df = get_variable('output_data')

# 数据转换
df = input_df.copy()

# 计算同比增长率
df['output_total_growth_rate'] = (
    (df['output_confirmed'] - df['output_last_year_confirmed']) / 
    df['output_last_year_confirmed'] * 100
).round(2)

# 添加处理时间
df['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 返回结果
result_df = df
