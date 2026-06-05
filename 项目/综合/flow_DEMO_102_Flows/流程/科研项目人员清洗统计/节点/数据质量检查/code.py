import pandas as pd

output.print("[数据质量检查] 开始")

if df is None or df.empty:
    df = get_variable("项目人员拆分")
output.print(f"输入数据: shape={df.shape}")

rules = []

empty_project = df['科研项目'].isna().sum()
rules.append({
    '规则名称': '空项目名检查',
    '检查项': '科研项目',
    '问题数量': empty_project,
    '状态': '通过' if empty_project == 0 else '失败',
    '详情': f'发现 {empty_project} 条空项目名记录'
})

empty_name = df['员工姓名'].isna().sum() + (df['员工姓名'] == '').sum()
rules.append({
    '规则名称': '空员工姓名检查',
    '检查项': '员工姓名',
    '问题数量': empty_name,
    '状态': '通过' if empty_name == 0 else '失败',
    '详情': f'发现 {empty_name} 条空员工姓名记录'
})

duplicate_rows = df.duplicated().sum()
rules.append({
    '规则名称': '重复记录检查',
    '检查项': '科研项目+员工姓名',
    '问题数量': duplicate_rows,
    '状态': '通过' if duplicate_rows == 0 else '失败',
    '详情': f'发现 {duplicate_rows} 条重复记录'
})

stats = df.groupby('科研项目').size().describe()
rules.append({
    '规则名称': '项目人员数量统计',
    '检查项': '人数分布',
    '问题数量': 0,
    '状态': '通过',
    '详情': f"最小:{stats['min']}人, 最大:{stats['max']}人, 平均:{stats['mean']:.1f}人"
})

result_df = pd.DataFrame(rules)

passed = sum(1 for r in rules if r['状态'] == '通过')
total = len(rules)
score = (passed / total) * 100

output.print(f"数据质量得分: {score:.1f}分 ({passed}/{total} 通过)")

set_scalar_output('V_DQ_SCORE', score)
set_scalar_output('quality_passed', score >= 80)

output.print("[数据质量检查] 完成")