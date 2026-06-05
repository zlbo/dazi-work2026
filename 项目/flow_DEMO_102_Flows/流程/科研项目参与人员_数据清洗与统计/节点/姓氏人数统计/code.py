import pandas as pd

# 获取输入数据
df = get_variable('团队人员拆分')

# 把人员列合并成一列
person_columns = ['人员1', '人员2', '人员3', '人员4']
df_melted = pd.melt(df, id_vars=['科研项目'], value_vars=person_columns, value_name='人员')

# 筛选出姓李的人员数据
df_filtered_li = df_melted[df_melted['人员'].str.startswith('李', na=False)]
# 按科研项目分组，统计每个项目姓李的人数
grouped_df_li = df_filtered_li.groupby('科研项目')['人员'].count().reset_index(name='姓李的人数')

# 筛选出姓陈的人员数据
df_filtered_chen = df_melted[df_melted['人员'].str.startswith('陈', na=False)]
# 按科研项目分组，统计每个项目姓陈的人数
grouped_df_chen = df_filtered_chen.groupby('科研项目')['人员'].count().reset_index(name='姓陈的人数')

# 将姓李人数统计结果合并到原表
result_df = df.merge(grouped_df_li, on='科研项目', how='left')
# 将姓陈人数统计结果合并到原表
result_df = result_df.merge(grouped_df_chen, on='科研项目', how='left')

# 处理没有姓李、姓陈人员的项目，将人数填充为 0
result_df['姓李的人数'] = result_df['姓李的人数'].fillna(0).astype(int)
result_df['姓陈的人数'] = result_df['姓陈的人数'].fillna(0).astype(int)

