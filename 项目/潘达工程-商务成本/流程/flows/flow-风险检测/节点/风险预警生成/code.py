# -*- coding: utf-8 -*-
# 上游变量来源：risk_matched_data - 从风险规则匹配节点获取
# 本节点 output_variable_name = project_risk_data
import pandas as pd

output.print("[python-script] 开始生成风险预警")

if df is None or df.empty:
    df = get_variable("risk_matched_data")
    output.print(f"从变量获取数据 shape={df.shape}")
else:
    output.print(f"从入边获取数据 shape={df.shape}")

result_df = df.copy()

result_df['alert_level'] = result_df['risk_level'].map({
    '高': '紧急',
    '中': '警告',
    '低': '提示'
})

result_df['alert_color'] = result_df['risk_level'].map({
    '高': '#ef4444',
    '中': '#f59e0b',
    '低': '#22c55e'
})

result_df['alert_time'] = pd.Timestamp.now()
result_df['alert_status'] = '待处理'
result_df['data_source'] = 'flow-006-风险检测'

high_risk_count = len(result_df[result_df['risk_level'] == '高'])
medium_risk_count = len(result_df[result_df['risk_level'] == '中'])

output.print(f"生成预警: 高风险{high_risk_count}条, 中风险{medium_risk_count}条")
output.print(f"输出 shape={result_df.shape}")

output.print("[python-script] 风险预警生成完成")