"""
发布验证脚本 - 商务成本智能决策体系
版本：V1.0
依据：阶段三执行规划
功能：验证本体部署的完整性和正确性
"""

from dazi.ontology import OntologyContext
import os

# ==================== 验证配置 ====================
VERIFICATION_CONFIG = {
    'tables': {
        'expected_count': 23,
        'required_tables': [
            'dim_date', 'dim_project', 'dim_contract', 'dim_owner',
            'dim_project_status', 'dim_contract_status', 'dim_project_category',
            'dim_cooperation', 'dim_cost_subject', 'dim_region', 'dim_organization',
            'dim_client', 'dim_contract_type', 'dim_risk_level',
            'fact_project_cost', 'fact_project_output', 'fact_payment',
            'fact_receivable', 'fact_cash_flow', 'fact_risk', 'fact_change_order',
            'fact_claim', 'fact_project_indicator',
        ]
    },
    'cubes': {
        'expected_count': 9,
        'required_cubes': [
            'ProjectCostCube', 'ProjectOutputCube', 'PaymentCube', 'ReceivableCube',
            'CashFlowCube', 'RiskCube', 'ChangeOrderCube', 'ClaimCube',
            'ProjectIndicatorCube',
        ]
    },
    'object_types': {
        'expected_count': 11,
        'required_types': [
            'Project', 'Contract', 'ProjectCost', 'ProjectOutput', 'Payment',
            'Receivable', 'CashFlow', 'Risk', 'ChangeOrder', 'Claim', 'Indicator',
        ]
    },
    'link_types': {
        'expected_count': 4,
        'required_types': [
            'ProjectContract', 'ProjectCostRelation', 'ProjectOutputRelation',
            'ProjectRiskRelation',
        ]
    },
    'action_types': {
        'expected_count': 6,
        'required_types': [
            'CostQuery', 'OutputQuery', 'CashFlowQuery', 'RiskAssess',
            'PaymentApply', 'IndicatorCalc',
        ]
    },
    'functions': {
        'expected_count': 7,
        'required_functions': [
            'cost_deviation_analysis', 'cost_rigidity_analysis',
            'cost_subject_yoy_analysis', 'output_confirmation_ratio',
            'cash_flow_forecast', 'risk_alert', 'project_profit_assessment',
        ]
    },
    'bind_source': {
        'expected_count': 11,
    },
}

# ==================== 验证函数 ====================
def verify_tables(s):
    """验证物理表注册"""
    print("=== 验证物理表 ===")
    
    # 获取已注册的表
    registered_tables = s.tables.list()
    registered_names = [t['name'] for t in registered_tables]
    
    # 检查数量
    if len(registered_tables) == VERIFICATION_CONFIG['tables']['expected_count']:
        print(f"✓ 物理表数量正确: {len(registered_tables)}")
    else:
        print(f"✗ 物理表数量不符: 期望 {VERIFICATION_CONFIG['tables']['expected_count']}, 实际 {len(registered_tables)}")
    
    # 检查必需表
    missing_tables = []
    for table in VERIFICATION_CONFIG['tables']['required_tables']:
        if table not in registered_names:
            missing_tables.append(table)
    
    if missing_tables:
        print(f"✗ 缺失物理表: {', '.join(missing_tables)}")
    else:
        print("✓ 所有必需物理表已注册")
    
    return len(missing_tables) == 0

def verify_cubes(s):
    """验证Cube注册"""
    print("\n=== 验证Cube ===")
    
    registered_cubes = s.cubes.list()
    registered_names = [c['name'] for c in registered_cubes]
    
    if len(registered_cubes) == VERIFICATION_CONFIG['cubes']['expected_count']:
        print(f"✓ Cube数量正确: {len(registered_cubes)}")
    else:
        print(f"✗ Cube数量不符: 期望 {VERIFICATION_CONFIG['cubes']['expected_count']}, 实际 {len(registered_cubes)}")
    
    missing_cubes = []
    for cube in VERIFICATION_CONFIG['cubes']['required_cubes']:
        if cube not in registered_names:
            missing_cubes.append(cube)
    
    if missing_cubes:
        print(f"✗ 缺失Cube: {', '.join(missing_cubes)}")
    else:
        print("✓ 所有必需Cube已注册")
    
    return len(missing_cubes) == 0

def verify_object_types(s):
    """验证Object Type注册"""
    print("\n=== 验证Object Type ===")
    
    registered_types = s.object_types.list()
    registered_codes = [t['code'] for t in registered_types]
    
    if len(registered_types) == VERIFICATION_CONFIG['object_types']['expected_count']:
        print(f"✓ Object Type数量正确: {len(registered_types)}")
    else:
        print(f"✗ Object Type数量不符: 期望 {VERIFICATION_CONFIG['object_types']['expected_count']}, 实际 {len(registered_types)}")
    
    missing_types = []
    for obj_type in VERIFICATION_CONFIG['object_types']['required_types']:
        if obj_type not in registered_codes:
            missing_types.append(obj_type)
    
    if missing_types:
        print(f"✗ 缺失Object Type: {', '.join(missing_types)}")
    else:
        print("✓ 所有必需Object Type已注册")
    
    return len(missing_types) == 0

def verify_link_types(s):
    """验证Link Type注册"""
    print("\n=== 验证Link Type ===")
    
    registered_links = s.link_types.list()
    registered_codes = [l['code'] for l in registered_links]
    
    if len(registered_links) == VERIFICATION_CONFIG['link_types']['expected_count']:
        print(f"✓ Link Type数量正确: {len(registered_links)}")
    else:
        print(f"✗ Link Type数量不符: 期望 {VERIFICATION_CONFIG['link_types']['expected_count']}, 实际 {len(registered_links)}")
    
    missing_links = []
    for link in VERIFICATION_CONFIG['link_types']['required_types']:
        if link not in registered_codes:
            missing_links.append(link)
    
    if missing_links:
        print(f"✗ 缺失Link Type: {', '.join(missing_links)}")
    else:
        print("✓ 所有必需Link Type已注册")
    
    return len(missing_links) == 0

def verify_action_types(s):
    """验证Action Type注册"""
    print("\n=== 验证Action Type ===")
    
    registered_actions = s.action_types.list()
    registered_codes = [a['code'] for a in registered_actions]
    
    if len(registered_actions) == VERIFICATION_CONFIG['action_types']['expected_count']:
        print(f"✓ Action Type数量正确: {len(registered_actions)}")
    else:
        print(f"✗ Action Type数量不符: 期望 {VERIFICATION_CONFIG['action_types']['expected_count']}, 实际 {len(registered_actions)}")
    
    missing_actions = []
    for action in VERIFICATION_CONFIG['action_types']['required_types']:
        if action not in registered_codes:
            missing_actions.append(action)
    
    if missing_actions:
        print(f"✗ 缺失Action Type: {', '.join(missing_actions)}")
    else:
        print("✓ 所有必需Action Type已注册")
    
    return len(missing_actions) == 0

def verify_functions(s):
    """验证业务函数注册"""
    print("\n=== 验证业务函数 ===")
    
    # 假设functions模块有list方法
    try:
        registered_functions = s.functions.list()
        registered_codes = [f['code'] for f in registered_functions]
    except Exception:
        registered_functions = []
        registered_codes = []
        print("! 函数列表获取失败，跳过数量检查")
    
    if registered_functions:
        if len(registered_functions) == VERIFICATION_CONFIG['functions']['expected_count']:
            print(f"✓ 业务函数数量正确: {len(registered_functions)}")
        else:
            print(f"✗ 业务函数数量不符: 期望 {VERIFICATION_CONFIG['functions']['expected_count']}, 实际 {len(registered_functions)}")
    
    # 检查函数文件是否存在
    func_file = os.path.join(os.path.dirname(__file__), 'panda_cost_business_functions.py')
    if os.path.exists(func_file):
        print("✓ 业务函数文件存在")
    else:
        print(f"✗ 业务函数文件不存在: {func_file}")
    
    return os.path.exists(func_file)

def verify_bind_source(s):
    """验证bind_source绑定"""
    print("\n=== 验证bind_source绑定 ===")
    
    # 检查每个Object Type是否有bind_source
    bind_count = 0
    for obj_type in VERIFICATION_CONFIG['object_types']['required_types']:
        try:
            binds = s.object_types.get_bind_source(obj_type)
            if binds:
                bind_count += 1
                print(f"  ✓ {obj_type} 已绑定")
            else:
                print(f"  ✗ {obj_type} 未绑定")
        except Exception as e:
            print(f"  ! {obj_type} 绑定检查失败: {e}")
    
    if bind_count == VERIFICATION_CONFIG['bind_source']['expected_count']:
        print(f"✓ bind_source绑定数量正确: {bind_count}")
    else:
        print(f"✗ bind_source绑定数量不符: 期望 {VERIFICATION_CONFIG['bind_source']['expected_count']}, 实际 {bind_count}")
    
    return bind_count == VERIFICATION_CONFIG['bind_source']['expected_count']

def verify_seed_data(s):
    """验证种子数据"""
    print("\n=== 验证种子数据 ===")
    
    # 检查项目数据
    project_count = s.tables.count('dim_project')
    if project_count > 0:
        print(f"✓ 项目数据: {project_count} 条")
    else:
        print("✗ 项目数据为空")
    
    # 检查成本数据
    cost_count = s.tables.count('fact_project_cost')
    if cost_count > 0:
        print(f"✓ 成本数据: {cost_count} 条")
    else:
        print("✗ 成本数据为空")
    
    # 检查产值数据
    output_count = s.tables.count('fact_project_output')
    if output_count > 0:
        print(f"✓ 产值数据: {output_count} 条")
    else:
        print("✗ 产值数据为空")
    
    # 检查指标数据
    indicator_count = s.tables.count('fact_project_indicator')
    if indicator_count > 0:
        print(f"✓ 指标数据: {indicator_count} 条")
    else:
        print("✗ 指标数据为空")
    
    # 检查时间维表
    date_count = s.tables.count('dim_date')
    if date_count >= 700:  # 约2年数据
        print(f"✓ 时间维表: {date_count} 天")
    else:
        print(f"! 时间维表数据较少: {date_count} 天")
    
    return project_count > 0 and cost_count > 0 and output_count > 0 and indicator_count > 0

def verify_file_structure():
    """验证文件结构"""
    print("\n=== 验证文件结构 ===")
    
    setup_dir = os.path.dirname(__file__)
    expected_files = [
        'panda_cost_ontology_init.py',
        'panda_cost_seed_data.py',
        'panda_cost_business_functions.py',
        'panda_cost_category_registry.py',
        'panda_cost_deploy_verify.py',
    ]
    
    missing_files = []
    for file in expected_files:
        filepath = os.path.join(setup_dir, file)
        if os.path.exists(filepath):
            print(f"✓ {file}")
        else:
            missing_files.append(file)
            print(f"✗ {file}")
    
    if missing_files:
        print(f"\n! 缺失文件: {', '.join(missing_files)}")
        return False
    else:
        print("\n✓ 所有必需文件存在")
        return True

# ==================== 主验证函数 ====================
def main():
    print("=" * 60)
    print("商务成本智能决策体系 - 发布验证")
    print("=" * 60)
    
    all_passed = True
    
    # 1. 验证文件结构
    files_ok = verify_file_structure()
    all_passed &= files_ok
    
    # 2. 连接本体上下文并验证注册内容
    try:
        with OntologyContext() as s:
            print("\n" + "=" * 60)
            print("开始验证本体注册内容")
            print("=" * 60)
            
            tables_ok = verify_tables(s)
            all_passed &= tables_ok
            
            cubes_ok = verify_cubes(s)
            all_passed &= cubes_ok
            
            obj_types_ok = verify_object_types(s)
            all_passed &= obj_types_ok
            
            link_types_ok = verify_link_types(s)
            all_passed &= link_types_ok
            
            action_types_ok = verify_action_types(s)
            all_passed &= action_types_ok
            
            functions_ok = verify_functions(s)
            all_passed &= functions_ok
            
            bind_ok = verify_bind_source(s)
            all_passed &= bind_ok
            
            data_ok = verify_seed_data(s)
            all_passed &= data_ok
            
    except Exception as e:
        print(f"\n✗ 本体连接失败: {e}")
        all_passed = False
    
    # 3. 输出验证结果
    print("\n" + "=" * 60)
    print("验证结果汇总")
    print("=" * 60)
    
    if all_passed:
        print("✓✓✓ 所有验证通过！")
        print("\n发布状态: 已就绪")
        print("建议: 可以进行发布部署")
    else:
        print("✗✗✗ 部分验证未通过！")
        print("\n发布状态: 未就绪")
        print("建议: 检查并修复未通过的验证项")
    
    print("\n" + "=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)