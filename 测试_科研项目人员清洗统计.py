#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
科研项目人员清洗统计 - 独立测试脚本
用于验证数据清洗和统计逻辑
"""

import pandas as pd
import re

# ==================== 步骤1: 读取Excel文件 ====================
print("=" * 60)
print("步骤1: 读取Excel文件")
print("=" * 60)

excel_path = r"D:\GitHub\dazi-work\资源\files\科研项目_模拟人员混杂数据.xlsx_72326a69\原文件.xlsx"

# 读取人员名单工作表
df_people = pd.read_excel(excel_path, sheet_name="人员名单", header=0, usecols="A:B")
print(f"人员名单: shape={df_people.shape}, columns={list(df_people.columns)}")
print(f"前5行:\n{df_people.head(5)}\n")

# 读取混杂数据工作表
df_mixed = pd.read_excel(excel_path, sheet_name="混杂数据", header=0, usecols="A:B")
print(f"混杂数据: shape={df_mixed.shape}, columns={list(df_mixed.columns)}")
print(f"前5行:\n{df_mixed.head(5)}\n")

# ==================== 步骤2: 团队字段拆分 ====================
print("=" * 60)
print("步骤2: 团队字段拆分")
print("=" * 60)

def split_team(team_str):
    """拆分团队字段，支持多种分隔符"""
    if pd.isna(team_str):
        return []
    separators = r'[,，、\-—_@\s]+'
    names = re.split(separators, str(team_str).strip())
    return [name.strip() for name in names if name.strip()]

df_mixed['团队成员列表'] = df_mixed['团队'].apply(split_team)
df_split = df_mixed.explode('团队成员列表').rename(columns={'团队成员列表': '员工姓名'})
df_split = df_split[['科研项目', '员工姓名']].reset_index(drop=True)

print(f"拆分后: shape={df_split.shape}")
print(f"项目数: {df_split['科研项目'].nunique()}, 人员记录数: {len(df_split)}")
print(f"前10行:\n{df_split.head(10)}\n")

# ==================== 步骤3: 数据质量检查 ====================
print("=" * 60)
print("步骤3: 数据质量检查")
print("=" * 60)

rules = []

# 规则1: 检查空项目名
empty_project = df_split['科研项目'].isna().sum()
rules.append({
    '规则名称': '空项目名检查',
    '检查项': '科研项目',
    '问题数量': empty_project,
    '状态': '通过' if empty_project == 0 else '失败',
    '详情': f'发现 {empty_project} 条空项目名记录'
})

# 规则2: 检查空员工姓名
empty_name = df_split['员工姓名'].isna().sum() + (df_split['员工姓名'] == '').sum()
rules.append({
    '规则名称': '空员工姓名检查',
    '检查项': '员工姓名',
    '问题数量': empty_name,
    '状态': '通过' if empty_name == 0 else '失败',
    '详情': f'发现 {empty_name} 条空员工姓名记录'
})

# 规则3: 检查重复记录
duplicate_rows = df_split.duplicated().sum()
rules.append({
    '规则名称': '重复记录检查',
    '检查项': '科研项目+员工姓名',
    '问题数量': duplicate_rows,
    '状态': '通过' if duplicate_rows == 0 else '失败',
    '详情': f'发现 {duplicate_rows} 条重复记录'
})

# 规则4: 检查项目人员数量分布
stats = df_split.groupby('科研项目').size().describe()
rules.append({
    '规则名称': '项目人员数量统计',
    '检查项': '人数分布',
    '问题数量': 0,
    '状态': '通过',
    '详情': f"最小:{stats['min']}人, 最大:{stats['max']}人, 平均:{stats['mean']:.1f}人"
})

dq_report = pd.DataFrame(rules)
print(f"数据质量报告:\n{dq_report}\n")

# 计算综合质量分数
passed = sum(1 for r in rules if r['状态'] == '通过')
total = len(rules)
score = (passed / total) * 100
print(f"数据质量得分: {score:.1f}分 ({passed}/{total} 通过)\n")

# ==================== 步骤4: 人员编码关联 ====================
print("=" * 60)
print("步骤4: 人员编码关联")
print("=" * 60)

df_join = df_split.merge(df_people, on='员工姓名', how='left')
df_join['匹配状态'] = df_join['员工编码'].apply(lambda x: '已匹配' if pd.notna(x) else '未匹配')

print(f"关联后: shape={df_join.shape}")
print(f"前10行:\n{df_join.head(10)}\n")

# 匹配统计
match_counts = df_join['匹配状态'].value_counts()
print(f"匹配统计:\n{match_counts}\n")

# ==================== 步骤5: 统计分析 ====================
print("=" * 60)
print("步骤5: 统计分析")
print("=" * 60)

# 统计1: 各项目参与人数统计
print("【统计1】各项目参与人数统计")
project_stats = df_join.groupby('科研项目').agg(
    参与人数=('员工姓名', 'nunique'),
    匹配人数=('匹配状态', lambda x: (x == '已匹配').sum()),
    未匹配人数=('匹配状态', lambda x: (x == '未匹配').sum())
).reset_index().sort_values('参与人数', ascending=False)
print(f"{project_stats.head(10)}\n")

# 统计2: 各人员参与项目数统计
print("【统计2】各人员参与项目数统计")
person_stats = df_join.groupby(['员工姓名', '匹配状态']).agg(
    参与项目数=('科研项目', 'nunique'),
    员工编码=('员工编码', 'first')
).reset_index().sort_values('参与项目数', ascending=False)
print(f"{person_stats.head(10)}\n")

# 统计3: 人员参与频次排名TOP10
print("【统计3】TOP10参与者")
top_participants = person_stats.head(10).reset_index(drop=True)
top_participants['排名'] = top_participants.index + 1
print(f"{top_participants[['排名', '员工姓名', '参与项目数', '匹配状态']]}\n")

# 统计4: 姓氏分布统计
print("【统计4】姓氏分布统计")
def get_surname(name):
    if pd.isna(name) or not isinstance(name, str):
        return '未知'
    return name[0] if name else '未知'

df_join['姓氏'] = df_join['员工姓名'].apply(get_surname)
surname_stats = df_join.groupby('姓氏')['员工姓名'].nunique().sort_values(ascending=False).reset_index()
surname_stats.columns = ['姓氏', '人数']
print(f"{surname_stats.head(10)}\n")

# 统计5: 匹配状态汇总
print("【统计5】匹配状态汇总")
match_summary = df_join['匹配状态'].value_counts().reset_index()
match_summary.columns = ['匹配状态', '人数']
match_summary['占比'] = (match_summary['人数'] / len(df_join) * 100).round(1).astype(str) + '%'
print(f"{match_summary}\n")

# 汇总摘要
print("【汇总摘要】")
summary_data = []
summary_data.append({'统计类别': '项目统计', '指标': '项目总数', '数值': str(df_join['科研项目'].nunique())})
summary_data.append({'统计类别': '项目统计', '指标': '平均参与人数', '数值': f"{project_stats['参与人数'].mean():.1f}"})
summary_data.append({'统计类别': '项目统计', '指标': '最大参与人数', '数值': str(project_stats['参与人数'].max())})
summary_data.append({'统计类别': '项目统计', '指标': '最小参与人数', '数值': str(project_stats['参与人数'].min())})
summary_data.append({'统计类别': '人员统计', '指标': '参与人员总数', '数值': str(df_join['员工姓名'].nunique())})
summary_data.append({'统计类别': '人员统计', '指标': '平均参与项目数', '数值': f"{person_stats['参与项目数'].mean():.1f}"})
summary_data.append({'统计类别': '人员统计', '指标': '最高参与项目数', '数值': str(person_stats['参与项目数'].max())})

matched_count = match_summary[match_summary['匹配状态'] == '已匹配']['人数'].values[0] if '已匹配' in match_summary['匹配状态'].values else 0
unmatched_count = match_summary[match_summary['匹配状态'] == '未匹配']['人数'].values[0] if '未匹配' in match_summary['匹配状态'].values else 0
summary_data.append({'统计类别': '匹配统计', '指标': '已匹配人数', '数值': str(matched_count)})
summary_data.append({'统计类别': '匹配统计', '指标': '未匹配人数', '数值': str(unmatched_count)})
summary_data.append({'统计类别': '匹配统计', '指标': '匹配率', '数值': f"{matched_count / len(df_join) * 100:.1f}%"})

summary_df = pd.DataFrame(summary_data)
print(f"{summary_df}\n")

print("=" * 60)
print("测试完成!")
print("=" * 60)

# 保存结果到文件
output_path = r"D:\GitHub\dazi-work\测试_科研项目人员清洗统计_结果.xlsx"
with pd.ExcelWriter(output_path) as writer:
    df_people.to_excel(writer, sheet_name='人员名单', index=False)
    df_mixed.to_excel(writer, sheet_name='混杂数据', index=False)
    df_split.to_excel(writer, sheet_name='项目人员拆分', index=False)
    dq_report.to_excel(writer, sheet_name='数据质量报告', index=False)
    df_join.to_excel(writer, sheet_name='项目人员关联', index=False)
    project_stats.to_excel(writer, sheet_name='项目参与人数统计', index=False)
    person_stats.to_excel(writer, sheet_name='人员参与项目统计', index=False)
    top_participants.to_excel(writer, sheet_name='TOP10参与者', index=False)
    surname_stats.to_excel(writer, sheet_name='姓氏分布统计', index=False)
    match_summary.to_excel(writer, sheet_name='匹配状态汇总', index=False)
    summary_df.to_excel(writer, sheet_name='汇总摘要', index=False)

print(f"\n结果已保存到: {output_path}")