# -*- coding: utf-8 -*-
import pandas as pd

# 读取输入数据
df = get_variable("项目参与人员明细")

# 初始化质检结果列表
quality_issues = []
total_records = len(df)
valid_project_id_count = 0
valid_employee_code_count = 0

# 检查每个记录
for idx, row in df.iterrows():
    project_id = row.get('项目ID')
    employee_code = row.get('员工编码')
    project_name = row.get('科研项目', '')
    person_name = row.get('人员', '')
    
    # 检查项目ID是否有效（0表示未匹配）
    if project_id == 0 or pd.isna(project_id):
        quality_issues.append({
            '问题类型': '项目ID未匹配',
            '科研项目': project_name,
            '人员': person_name,
            '项目ID': project_id,
            '员工编码': employee_code,
            '描述': f"项目'{project_name}'中的人员'{person_name}'未匹配到项目ID"
        })
    else:
        valid_project_id_count += 1
    
    # 检查员工编码是否有效（0或空表示未匹配）
    if employee_code == 0 or pd.isna(employee_code):
        quality_issues.append({
            '问题类型': '员工编码未匹配',
            '科研项目': project_name,
            '人员': person_name,
            '项目ID': project_id,
            '员工编码': employee_code,
            '描述': f"项目'{project_name}'中的人员'{person_name}'未匹配到员工编码"
        })
    else:
        valid_employee_code_count += 1

# 生成质检报告
if quality_issues:
    issues_df = pd.DataFrame(quality_issues)
    result_df = issues_df
    status = "FAIL"
    message = f"发现 {len(quality_issues)} 个数据质量问题"
else:
    result_df = pd.DataFrame([{
        '问题类型': '无',
        '科研项目': '全部',
        '人员': '全部',
        '项目ID': '全部有效',
        '员工编码': '全部有效',
        '描述': '所有数据均通过质量检查'
    }])
    status = "PASS"
    message = "所有数据均通过质量检查"

# 输出质检结果
set_table_output("质检报告", result_df)