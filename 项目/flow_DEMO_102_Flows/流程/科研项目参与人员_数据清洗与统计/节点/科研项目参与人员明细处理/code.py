import pandas as pd
import re

# 获取输入数据
df = get_variable('团队人员拆分')

# 删除团队列
df = df.drop(columns='团队')

# 按项目对人员进行列转行
result_df = pd.melt(df, id_vars='科研项目', var_name='原列名', value_name='人员')

# 去除可能因列转行产生的缺失值
result_df = result_df.dropna()

# 定义函数提取项目名称中的数字序号
def extract_project_id(name):
    match = re.search(r'\d+', name)
    return int(match.group()) if match else None

# 为项目添加ID，取名称中的数字序号
result_df['项目ID'] = result_df['科研项目'].apply(extract_project_id)

# 按项目ID排序
result_df = result_df.sort_values(by='项目ID')

# 获取人员名单表
person_list = get_variable('人员名单')

# 合并数据，将输入数据中的人员与人员名单里的员工姓名匹配，获取员工编码
result_df = pd.merge(result_df, person_list[['员工编码', '员工姓名']], left_on='人员', right_on='员工姓名', how='left')

# 删除多余的员工姓名字段
result_df = result_df.drop(columns='员工姓名')
