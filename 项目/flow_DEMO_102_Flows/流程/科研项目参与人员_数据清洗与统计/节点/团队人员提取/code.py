# -*- coding: utf-8 -*-
import pandas as pd
import re

# 读取混杂数据表
df = get_variable("混杂数据")

# 定义多种分隔符：逗号、顿号、分号、破折号、@符号、空格等
def split_team(team_str):
    if pd.isna(team_str):
        return []
    # 使用正则表达式匹配多种分隔符
    separators = r'[,，、;；\-—@．. \s]+'
    names = re.split(separators, str(team_str).strip())
    # 过滤空字符串
    return [name.strip() for name in names if name.strip()]

# 拆分团队列
df['团队人员列表'] = df['团队'].apply(split_team)

# 找出最大人数
max_people = df['团队人员列表'].apply(len).max()

# 创建人员列
for i in range(max_people):
    df[f'人员{i+1}'] = df['团队人员列表'].apply(lambda x: x[i] if i < len(x) else None)

# 移除临时列
df = df.drop('团队人员列表', axis=1)

# 输出结果
result_df = df