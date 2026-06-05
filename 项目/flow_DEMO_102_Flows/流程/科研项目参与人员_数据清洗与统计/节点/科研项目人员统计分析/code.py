# -*- coding: utf-8 -*-
import pandas as pd

# 使用项目参与人员明细作为主要输入数据源
df = get_variable("项目参与人员明细")

# ==================== 1. 项目规模分析 ====================
# 统计每个项目的参与人数
project_size = df.groupby('科研项目').agg(
    项目参与人数=('人员', 'count'),
    参与人员名单=('人员', lambda x: ', '.join(x))
).reset_index().sort_values('项目参与人数', ascending=False)

# ==================== 2. 人员活跃度分析 ====================
# 统计每个人参与的项目数量
person_activity = df.groupby('人员').agg(
    参与项目数量=('科研项目', 'nunique'),
    参与项目列表=('科研项目', lambda x: ', '.join(sorted(x.unique())))
).reset_index().sort_values('参与项目数量', ascending=False)

# ==================== 3. 姓氏分布统计 ====================
# 统计各姓氏在项目中的分布
def get_surname(name):
    if pd.isna(name):
        return '未知'
    return str(name)[0] if str(name) else '未知'

df['姓氏'] = df['人员'].apply(get_surname)
surname_stats = df.groupby(['科研项目', '姓氏']).agg(
    姓氏人数=('人员', 'count')
).reset_index()

# 全局姓氏统计
global_surname = df.groupby('姓氏').agg(
    总人数=('人员', 'nunique'),
    参与项目数=('科研项目', 'nunique')
).reset_index().sort_values('总人数', ascending=False)

# ==================== 4. 核心人员识别 ====================
# 参与项目最多的前10人（核心骨干）
core_personnel = person_activity.head(10).copy()
core_personnel['排名'] = range(1, len(core_personnel)+1)
core_personnel['评级'] = core_personnel['参与项目数量'].apply(
    lambda x: 'A' if x >= 3 else 'B' if x == 2 else 'C'
)

# ==================== 5. 项目人员密集度排名 ====================
# 按参与人数排序的项目排名
project_ranking = project_size.copy()
project_ranking['排名'] = project_ranking['项目参与人数'].rank(ascending=False, method='min').astype(int)
project_ranking['密集度等级'] = project_ranking['项目参与人数'].apply(
    lambda x: '高' if x >= 4 else '中' if x == 3 else '低'
)

# ==================== 6. 李姓、陈姓专项分析 ====================
# 李姓人员分析
li_personnel = df[df['姓氏'] == '李']
li_project_stats = li_personnel.groupby('科研项目').agg(李姓人数=('人员', 'nunique')).reset_index()

# 陈姓人员分析
chen_personnel = df[df['姓氏'] == '陈']
chen_project_stats = chen_personnel.groupby('科研项目').agg(陈姓人数=('人员', 'nunique')).reset_index()

# 姓氏对比
surname_comparison = project_size[['科研项目', '项目参与人数']].merge(
    li_project_stats, on='科研项目', how='left'
).merge(
    chen_project_stats, on='科研项目', how='left'
).fillna(0).astype({'李姓人数': int, '陈姓人数': int})
surname_comparison['李姓占比'] = (surname_comparison['李姓人数'] / surname_comparison['项目参与人数'] * 100).round(1)
surname_comparison['陈姓占比'] = (surname_comparison['陈姓人数'] / surname_comparison['项目参与人数'] * 100).round(1)

# ==================== 7. 汇总统计报告 ====================
# 创建汇总统计表格
summary_data = [
    {'统计指标': '项目总数', '数值': len(project_size), '单位': '个'},
    {'统计指标': '参与人员总数', '数值': len(person_activity), '单位': '人'},
    {'统计指标': '平均项目参与人数', '数值': round(project_size['项目参与人数'].mean(), 1), '单位': '人/项目'},
    {'统计指标': '平均人员参与项目数', '数值': round(person_activity['参与项目数量'].mean(), 1), '单位': '项目/人'},
    {'统计指标': '最大项目规模', '数值': project_size['项目参与人数'].max(), '单位': '人'},
    {'统计指标': '最高人员活跃度', '数值': person_activity['参与项目数量'].max(), '单位': '项目'},
    {'统计指标': '李姓人员总数', '数值': len(li_personnel['人员'].unique()), '单位': '人'},
    {'统计指标': '陈姓人员总数', '数值': len(chen_personnel['人员'].unique()), '单位': '人'},
]
summary_df = pd.DataFrame(summary_data)

# ==================== 8. 输出综合统计结果 ====================
# 将所有统计结果合并为一个结构化报告
result_data = []

# 添加项目规模排名
for _, row in project_ranking.iterrows():
    result_data.append({
        '统计类别': '项目规模排名',
        '项目名称': row['科研项目'],
        '指标名称': '项目参与人数',
        '数值': int(row['项目参与人数']),
        '排名': str(row['排名']),
        '等级': row['密集度等级'],
        '备注': row['参与人员名单'][:100] + '...' if len(row['参与人员名单']) > 100 else row['参与人员名单']
    })

# 添加核心人员排名
for _, row in core_personnel.iterrows():
    result_data.append({
        '统计类别': '核心人员排名',
        '项目名称': '-',
        '指标名称': '参与项目数量',
        '数值': int(row['参与项目数量']),
        '排名': str(row['排名']),
        '等级': row['评级'],
        '备注': row['参与项目列表'][:100] + '...' if len(row['参与项目列表']) > 100 else row['参与项目列表']
    })

# 添加姓氏分布
for _, row in surname_comparison.iterrows():
    result_data.append({
        '统计类别': '姓氏分布',
        '项目名称': row['科研项目'],
        '指标名称': f"李姓{row['李姓人数']}人/陈姓{row['陈姓人数']}人",
        '数值': int(row['项目参与人数']),
        '排名': '-',
        '等级': f"李姓{row['李姓占比']}%/陈姓{row['陈姓占比']}%",
        '备注': '-'
    })

# 添加汇总统计
for _, row in summary_df.iterrows():
    result_data.append({
        '统计类别': '汇总统计',
        '项目名称': '-',
        '指标名称': row['统计指标'],
        '数值': row['数值'],
        '排名': '-',
        '等级': row['单位'],
        '备注': '-'
    })

result_df = pd.DataFrame(result_data)

# 输出结果
result_df['排名'] = result_df['排名'].astype(str)
set_table_output("科研项目人员统计报表", result_df)