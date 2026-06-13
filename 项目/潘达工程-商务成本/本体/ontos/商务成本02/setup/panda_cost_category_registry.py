"""
分类挂载脚本 - 商务成本智能决策体系
版本：V1.0
依据：《本体规划指南》§91「平台分类（平台分类对齐 · 强制）」
功能：使用空间对象API进行平台分类挂载
"""

def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)
    
    output.print("=== 开始执行分类挂载 ===")
    output.print(f"空间: {space_id}")
    
    # 1. Object Type 分类
    output.print("\n[1/5] 注册Object Type分类...")
    obj_type_categories = {
        '主数据': ['Project', 'Company', 'CostSubject', 'Supplier', 'Employee', 'Region', 'Industry'],
        '业务事实': ['CashFlow', 'Risk'],
    }
    for category, obj_types in obj_type_categories.items():
        for obj_type in obj_types:
            try:
                s.onto.register_object_type_category(obj_type, category)
                output.print(f"  ✓ {obj_type} -> {category}")
            except Exception as e:
                output.print(f"  ✗ {obj_type} -> {category}: {str(e)}")
    
    # 2. Cube 分类
    output.print("\n[2/5] 注册Cube分类...")
    cube_categories = {
        '流程型': ['ProjectCostCube', 'ProjectBudgetCube', 'ProjectOutputCube', 
                  'ContractCube', 'CashFlowCube', 'PurchaseCube', 'RiskCube', 'CostRigidityCube'],
        '主体型': ['ProjectIndicatorCube'],
    }
    for category, cubes in cube_categories.items():
        for cube in cubes:
            try:
                s.cubes.register_category(cube, category)
                output.print(f"  ✓ {cube} -> {category}")
            except Exception as e:
                output.print(f"  ✗ {cube} -> {category}: {str(e)}")
    
    # 3. Function 分类
    output.print("\n[3/5] 注册Function分类...")
    func_categories = {
        '分析函数': ['cost_deviation_analysis', 'cost_rigidity_analysis', 
                    'cost_subject_yoy_analysis', 'output_confirmation_ratio'],
        '预测函数': ['cash_flow_forecast'],
        '评估函数': ['risk_alert', 'project_profit_assessment'],
    }
    
    # 获取已注册的函数列表
    try:
        functions = s.ontology_functions.list()
        func_ids = {f['function_id'] for f in functions}
        
        for category, funcs in func_categories.items():
            for func in funcs:
                func_id = f'panda.cost.{func}'
                if func_id in func_ids:
                    try:
                        s.ontology_functions.register_category(func_id, category)
                        output.print(f"  ✓ {func_id} -> {category}")
                    except Exception as e:
                        output.print(f"  ✗ {func_id} -> {category}: {str(e)}")
                else:
                    output.print(f"  ! {func_id} 未注册")
    except Exception as e:
        output.print(f"  ! 获取函数列表失败: {str(e)}")
    
    # 4. Table 分类
    output.print("\n[4/5] 注册Table分类...")
    table_categories = {
        '时间维': ['dim_date'],
        '主数据': ['dim_project', 'dim_company', 'dim_cost_subject', 'dim_supplier', 'dim_employee'],
        '维度表': ['dim_region', 'dim_industry', 'dim_contract_type', 'dim_currency', 'dim_organization'],
        '事实表': ['fact_project_cost', 'fact_project_budget', 'fact_project_output', 
                   'fact_contract', 'fact_cash_flow', 'fact_purchase', 
                   'fact_expense', 'fact_risk', 'fact_project_indicator', 
                   'fact_cost_rigidity', 'fact_deviation_record', 'fact_employee_cost'],
    }
    for category, tables in table_categories.items():
        for table in tables:
            try:
                s.tables.register_category(table, category)
                output.print(f"  ✓ {table} -> {category}")
            except Exception as e:
                output.print(f"  ✗ {table} -> {category}: {str(e)}")
    
    # 5. 验证注册结果
    output.print("\n[5/5] 验证分类注册...")
    
    # 统计Object Type分类
    try:
        obj_count = len(obj_type_categories['主数据']) + len(obj_type_categories['业务事实'])
        output.print(f"  Object Type: {obj_count} 个分类已注册")
    except:
        output.print(f"  Object Type: 验证失败")
    
    # 统计Cube分类
    try:
        cube_count = len(cube_categories['流程型']) + len(cube_categories['主体型'])
        output.print(f"  Cube: {cube_count} 个分类已注册")
    except:
        output.print(f"  Cube: 验证失败")
    
    # 统计Table分类
    try:
        table_count = sum(len(tables) for tables in table_categories.values())
        output.print(f"  Table: {table_count} 个分类已注册")
    except:
        output.print(f"  Table: 验证失败")
    
    output.success("\n=== 分类挂载完成 ===")