import pandas as pd

output.print("[统计分析] 开始")

if df is None or df.empty:
    df = get_variable("项目人员关联")
output.print(f"输入数据: shape={df.shape}")

project_stats = df.groupby('科研项目').agg(
    参与人数=('员工姓名', 'nunique'),
    匹配人数=('匹配状态', lambda x: (x == '已匹配').sum()),
    未匹配人数=('匹配状态', lambda x: (x == '未匹配').sum())
).reset_index().sort_values('参与人数', ascending=False)

person_stats = df.groupby(['员工姓名', '匹配状态']).agg(
    参与项目数=('科研项目', 'nunique'),
    员工编码=('员工编码', 'first')
).reset_index().sort_values('参与项目数', ascending=False)

top_participants = person_stats.head(10).reset_index(drop=True)
top_participants['排名'] = top_participants.index + 1

def get_surname(name):
    if pd.isna(name) or not isinstance(name, str):
        return '未知'
    return name[0] if name else '未知'

df['姓氏'] = df['员工姓名'].apply(get_surname)
surname_stats = df.groupby('姓氏')['员工姓名'].nunique().sort_values(ascending=False).reset_index()
surname_stats.columns = ['姓氏', '人数']

match_summary = df['匹配状态'].value_counts().reset_index()
match_summary.columns = ['匹配状态', '人数']
match_summary['占比'] = (match_summary['人数'] / len(df) * 100).round(1).astype(str) + '%'

summary_data = []
summary_data.append({'统计类别': '项目统计', '指标': '项目总数', '数值': str(df['科研项目'].nunique())})
summary_data.append({'统计类别': '项目统计', '指标': '平均参与人数', '数值': f"{project_stats['参与人数'].mean():.1f}"})
summary_data.append({'统计类别': '项目统计', '指标': '最大参与人数', '数值': str(project_stats['参与人数'].max())})
summary_data.append({'统计类别': '项目统计', '指标': '最小参与人数', '数值': str(project_stats['参与人数'].min())})
summary_data.append({'统计类别': '人员统计', '指标': '参与人员总数', '数值': str(df['员工姓名'].nunique())})
summary_data.append({'统计类别': '人员统计', '指标': '平均参与项目数', '数值': f"{person_stats['参与项目数'].mean():.1f}"})
summary_data.append({'统计类别': '人员统计', '指标': '最高参与项目数', '数值': str(person_stats['参与项目数'].max())})

matched_count = match_summary[match_summary['匹配状态'] == '已匹配']['人数'].values[0] if '已匹配' in match_summary['匹配状态'].values else 0
unmatched_count = match_summary[match_summary['匹配状态'] == '未匹配']['人数'].values[0] if '未匹配' in match_summary['匹配状态'].values else 0
summary_data.append({'统计类别': '匹配统计', '指标': '已匹配人数', '数值': str(matched_count)})
summary_data.append({'统计类别': '匹配统计', '指标': '未匹配人数', '数值': str(unmatched_count)})
summary_data.append({'统计类别': '匹配统计', '指标': '匹配率', '数值': f"{matched_count / len(df) * 100:.1f}%"})

result_df = pd.DataFrame(summary_data)

set_table_output('项目参与人数统计', project_stats)
set_table_output('人员参与项目统计', person_stats)
set_table_output('TOP10参与者', top_participants)
set_table_output('姓氏分布统计', surname_stats)
set_table_output('匹配状态汇总', match_summary)

output.print(f"统计完成 - 项目数:{df['科研项目'].nunique()}, 人员数:{df['员工姓名'].nunique()}")
output.print("[统计分析] 完成")