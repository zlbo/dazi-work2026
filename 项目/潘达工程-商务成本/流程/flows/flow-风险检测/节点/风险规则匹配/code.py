# -*- coding: utf-8 -*-
# 上游变量来源：
# - output_data: 从 flow-001 获取产值数据
# - cost_data: 从 flow-002 获取成本数据
# - payment_data: 从 flow-003 获取付款数据
# - balance_data: 从 flow-004 获取收支数据
# 本节点 output_variable_name = risk_matched_data
import pandas as pd

output.print("[python-script] 开始风险规则匹配")

output_data = get_variable("output_data")
cost_data = get_variable("cost_data")
payment_data = get_variable("payment_data")

output.print(f"产值数据 shape={output_data.shape}")
output.print(f"成本数据 shape={cost_data.shape}")
output.print(f"付款数据 shape={payment_data.shape}")

merged_df = output_data.merge(cost_data, on=['project_id', 'report_period'], how='outer')
merged_df = merged_df.merge(payment_data, on=['project_id', 'report_period'], how='outer')

risk_results = []

for _, row in merged_df.iterrows():
    project_id = row['project_id']
    report_period = row['report_period']
    
    output_confirmed = row.get('output_confirmed', 0)
    output_unconfirmed = row.get('output_unconfirmed', 0)
    cost_confirmed_acc = row.get('cost_confirmed_acc', 0)
    cost_unconfirmed_acc = row.get('cost_unconfirmed_acc', 0)
    paid_amount = row.get('paid_amount', 0)
    payable_confirmed = row.get('payable_confirmed', 0)
    
    if output_confirmed > 0 and output_unconfirmed > output_confirmed * 0.5:
        risk_results.append({
            'project_id': project_id,
            'report_period': report_period,
            'risk_rule_id': 'R001',
            'risk_rule_name': '产值确认超时',
            'risk_level': '中',
            'risk_desc': f'待确认产值({output_unconfirmed})超过已确认产值({output_confirmed})的50%',
            'risk_value': output_unconfirmed / output_confirmed
        })
    
    if output_confirmed > 0 and cost_confirmed_acc > output_confirmed * 0.8:
        risk_results.append({
            'project_id': project_id,
            'report_period': report_period,
            'risk_rule_id': 'R002',
            'risk_rule_name': '成本异常偏高',
            'risk_level': '高',
            'risk_desc': f'成本率({cost_confirmed_acc/output_confirmed*100:.1f}%)超过行业均值(80%)',
            'risk_value': cost_confirmed_acc / output_confirmed
        })
    
    if payable_confirmed > 0 and paid_amount / payable_confirmed < 0.7:
        risk_results.append({
            'project_id': project_id,
            'report_period': report_period,
            'risk_rule_id': 'R003',
            'risk_rule_name': '回款率偏低',
            'risk_level': '高',
            'risk_desc': f'回款率({paid_amount/payable_confirmed*100:.1f}%)低于70%',
            'risk_value': paid_amount / payable_confirmed
        })
    
    if cost_confirmed_acc > 0 and cost_unconfirmed_acc > cost_confirmed_acc * 0.3:
        risk_results.append({
            'project_id': project_id,
            'report_period': report_period,
            'risk_rule_id': 'R004',
            'risk_rule_name': '成本确认滞后',
            'risk_level': '中',
            'risk_desc': f'待确认成本({cost_unconfirmed_acc})超过已确认成本({cost_confirmed_acc})的30%',
            'risk_value': cost_unconfirmed_acc / cost_confirmed_acc
        })

result_df = pd.DataFrame(risk_results)
output.print(f"匹配到 {len(result_df)} 条风险记录")

output.print("[python-script] 风险规则匹配完成")