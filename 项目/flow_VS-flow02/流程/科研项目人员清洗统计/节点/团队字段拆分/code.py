import pandas as pd
import re

output.print("[团队字段拆分] 开始")

if df is None or df.empty:
    df = get_variable("混杂数据")
output.print(f"输入数据: shape={df.shape}")

def split_team(team_str):
    if pd.isna(team_str):
        return []
    separators = r'[,，、\-_—@\s]+'
    names = re.split(separators, str(team_str).strip())
    return [name.strip() for name in names if name.strip()]

df['团队成员列表'] = df['团队'].apply(split_team)
result_df = df.explode('团队成员列表').rename(columns={'团队成员列表': '员工姓名'})
result_df = result_df[['科研项目', '员工姓名']].reset_index(drop=True)

output.print(f"拆分后: shape={result_df.shape}")
output.print(f"项目数: {result_df['科研项目'].nunique()}, 人员记录数: {len(result_df)}")

output.print("[团队字段拆分] 完成")