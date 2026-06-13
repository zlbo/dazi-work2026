"""商务成本本体业务规则脚本

放置：项目/潘达工程-商务成本/本体/ontos/商务成本/setup/commercial_cost_business_rules.py
发布：dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/商务成本/setup/commercial_cost_business_rules.py --space space__panda_construction --type rule
"""

def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)

    output.print("=== 商务成本本体业务规则初始化 ===")

    # ==================== 计算规则注册 ====================
    output.print("\n--- 注册计算规则 ---")

    # 检查是否已注册规则
    try:
        existing_rules = s.sql.query("SELECT rule_id FROM fact_business_rules LIMIT 1")
        if existing_rules:
            output.print("规则表已有数据，跳过注册")
            output.print("__JSON_SUMMARY__{\"ok\": true, \"skipped\": true}")
            return
    except Exception:
        pass

    # 成本类规则
    rules_data = [
        {"rule_id": "QR-C001", "rule_name": "成本偏差率", "rule_type": "calculation", 
         "formula": "(实际成本 - 目标成本) / 目标成本 × 100%", 
         "description": "成本偏差率 > 5% 时预警", "severity": "warning", "threshold": "{\"gt\": 5}"},
        {"rule_id": "QR-C002", "rule_name": "成本节约率", "rule_type": "calculation", 
         "formula": "(目标成本 - 实际成本) / 目标成本 × 100%", 
         "description": "计算成本节约比例", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-C003", "rule_name": "成本刚性度", "rule_type": "calculation", 
         "formula": "已确认成本 / 总成本 × 100%", 
         "description": "≥95% 正常，<95% 预警", "severity": "warning", "threshold": "{\"lt\": 95}"},
        {"rule_id": "QR-C004", "rule_name": "材料成本占比", "rule_type": "calculation", 
         "formula": "材料成本 / 总成本 × 100%", 
         "description": "材料成本占总成本比例", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-C005", "rule_name": "人工成本占比", "rule_type": "calculation", 
         "formula": "人工成本 / 总成本 × 100%", 
         "description": "人工成本占总成本比例", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-C006", "rule_name": "机械费用占比", "rule_type": "calculation", 
         "formula": "机械费用 / 总成本 × 100%", 
         "description": "机械费用占总成本比例", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-C007", "rule_name": "管理费用占比", "rule_type": "calculation", 
         "formula": "管理费用 / 总成本 × 100%", 
         "description": "管理费用占总成本比例", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-C008", "rule_name": "分包成本占比", "rule_type": "calculation", 
         "formula": "分包成本 / 总成本 × 100%", 
         "description": "分包成本占总成本比例", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-C009", "rule_name": "成本累计偏差", "rule_type": "calculation", 
         "formula": "累计实际成本 - 累计目标成本", 
         "description": "成本累计偏差计算", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-C010", "rule_name": "成本绩效指数", "rule_type": "calculation", 
         "formula": "挣值 / 实际成本", 
         "description": "CPI < 1 表示成本超支", "severity": "warning", "threshold": "{\"lt\": 1}"},
        
        # 收入类规则
        {"rule_id": "QR-R001", "rule_name": "产值偏差率", "rule_type": "calculation", 
         "formula": "(实际产值 - 计划产值) / 计划产值 × 100%", 
         "description": "产值偏差率分析", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-R002", "rule_name": "产值完成率", "rule_type": "calculation", 
         "formula": "实际产值 / 计划产值 × 100%", 
         "description": "产值完成率 < 80% 预警", "severity": "warning", "threshold": "{\"lt\": 80}"},
        {"rule_id": "QR-R003", "rule_name": "合同收款率", "rule_type": "calculation", 
         "formula": "已收款 / 合同金额 × 100%", 
         "description": "合同收款进度", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-R004", "rule_name": "回款及时率", "rule_type": "calculation", 
         "formula": "按时回款金额 / 应回款金额 × 100%", 
         "description": "<90% 预警", "severity": "warning", "threshold": "{\"lt\": 90}"},
        {"rule_id": "QR-R005", "rule_name": "应收账款周转率", "rule_type": "calculation", 
         "formula": "营业收入 / 平均应收账款", 
         "description": "应收账款周转效率", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-R006", "rule_name": "质保金回收率", "rule_type": "calculation", 
         "formula": "已回收质保金 / 应回收质保金 × 100%", 
         "description": "质保金回收情况", "severity": "info", "threshold": "{}"},
        
        # 利润类规则
        {"rule_id": "QR-P001", "rule_name": "项目利润率", "rule_type": "calculation", 
         "formula": "项目利润 / 项目收入 × 100%", 
         "description": "项目盈利水平", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-P002", "rule_name": "毛利率", "rule_type": "calculation", 
         "formula": "(收入 - 成本) / 收入 × 100%", 
         "description": "项目毛利率", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-P003", "rule_name": "净利率", "rule_type": "calculation", 
         "formula": "净利润 / 收入 × 100%", 
         "description": "项目净利率", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-P004", "rule_name": "管理费费率", "rule_type": "calculation", 
         "formula": "管理费 / 合同金额 × 100%", 
         "description": "管理费占合同金额比例", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-P005", "rule_name": "目标利润达成率", "rule_type": "calculation", 
         "formula": "实际利润 / 目标利润 × 100%", 
         "description": "<90% 预警", "severity": "warning", "threshold": "{\"lt\": 90}"},
        
        # 现金流规则
        {"rule_id": "QR-F001", "rule_name": "现金流动比率", "rule_type": "calculation", 
         "formula": "流动资产 / 流动负债", 
         "description": "流动性指标", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-F002", "rule_name": "现金流充足率", "rule_type": "calculation", 
         "formula": "经营现金流 / 流动负债 × 100%", 
         "description": "<100% 预警", "severity": "warning", "threshold": "{\"lt\": 100}"},
        {"rule_id": "QR-F003", "rule_name": "资金周转天数", "rule_type": "calculation", 
         "formula": "365 / 资金周转率", 
         "description": "资金周转效率", "severity": "info", "threshold": "{}"},
        
        # 风险类规则
        {"rule_id": "QR-RISK001", "rule_name": "风险综合指数", "rule_type": "calculation", 
         "formula": "(成本风险×0.4 + 进度风险×0.3 + 质量风险×0.3)", 
         "description": "综合风险评估", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-RISK002", "rule_name": "成本风险指数", "rule_type": "calculation", 
         "formula": "成本偏差率 × 成本刚性度", 
         "description": "成本风险评估", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-RISK003", "rule_name": "进度风险指数", "rule_type": "calculation", 
         "formula": "进度偏差率 × 关键路径占比", 
         "description": "进度风险评估", "severity": "info", "threshold": "{}"},
        {"rule_id": "QR-RISK004", "rule_name": "收款风险指数", "rule_type": "calculation", 
         "formula": "应收账款逾期率 × 客户信用等级", 
         "description": "收款风险评估", "severity": "info", "threshold": "{}"},
    ]

    # 插入规则数据
    if rules_data:
        s.sql.insert_rows("fact_business_rules", rules_data)
        output.print(f"已注册 {len(rules_data)} 条计算规则")

    output.print("\n=== 商务成本本体业务规则初始化完成 ===")
    output.print("__JSON_SUMMARY__{\"ok\": true, \"rules_registered\": 27}")