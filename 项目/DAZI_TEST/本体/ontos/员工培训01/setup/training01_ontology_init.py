"""员工培训01 本体初始化 — space__onto_engine_test

增量建设：复用 dim_date / dim_org，新建员工/课程/参训/计划表及 Cube/对象/链接。
规划对照：plans/员工培训01本体规划方案.md

实施顺序：init → seed → 发布全部函数 → training01_category_mount.py
"""

import json

SPACE_ID = "space__onto_engine_test"

TABLE_REGISTRY = {
    "dim_employee": {
        "display_name": "员工维表",
        "description": "员工主数据，归属组织",
        "columns": [
            {"name": "employee_id", "display_name": "员工 ID", "description": "主键"},
            {"name": "employee_code", "display_name": "工号"},
            {"name": "employee_name", "display_name": "姓名"},
            {"name": "org_id", "display_name": "所属组织", "description": "FK dim_org"},
            {"name": "org_name", "display_name": "组织名称", "description": "冗余"},
            {"name": "job_title", "display_name": "岗位"},
            {"name": "job_level", "display_name": "职级"},
            {"name": "hire_date", "display_name": "入职日期"},
            {"name": "employment_status", "display_name": "在职状态"},
            {"name": "status", "display_name": "记录状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_training_category": {
        "display_name": "培训类别维表",
        "description": "安全/技能/管理/合规培训类别树",
        "columns": [
            {"name": "category_id", "display_name": "类别 ID", "description": "主键"},
            {"name": "category_code", "display_name": "类别编码"},
            {"name": "category_name", "display_name": "类别名称"},
            {"name": "category_type", "display_name": "大类", "description": "安全/技能/管理/合规"},
            {"name": "parent_category_id", "display_name": "上级类别", "description": "自关联"},
            {"name": "category_level", "display_name": "层级"},
            {"name": "is_mandatory", "display_name": "是否组织必修"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_course": {
        "display_name": "课程维表",
        "description": "培训课程目录",
        "columns": [
            {"name": "course_id", "display_name": "课程 ID", "description": "主键"},
            {"name": "course_code", "display_name": "课程编码"},
            {"name": "course_name", "display_name": "课程名称"},
            {"name": "category_id", "display_name": "培训类别", "description": "FK dim_training_category"},
            {"name": "category_name", "display_name": "类别名称", "description": "冗余"},
            {"name": "category_type", "display_name": "类别大类", "description": "冗余"},
            {"name": "delivery_mode", "display_name": "授课方式"},
            {"name": "standard_hours", "display_name": "标准学时"},
            {"name": "is_mandatory", "display_name": "是否必修"},
            {"name": "cert_valid_months", "display_name": "资质有效期", "description": "月；0=无"},
            {"name": "instructor", "display_name": "默认讲师"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_training_record": {
        "display_name": "培训参训记录",
        "description": "报名/参训/完成/考核明细",
        "columns": [
            {"name": "record_id", "display_name": "记录 ID", "description": "主键"},
            {"name": "session_id", "display_name": "班次 ID"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date"},
            {"name": "training_date", "display_name": "培训日期"},
            {"name": "fiscal_year", "display_name": "财年"},
            {"name": "fiscal_period", "display_name": "期间", "description": "1-12"},
            {"name": "employee_id", "display_name": "员工 ID"},
            {"name": "employee_name", "display_name": "员工姓名", "description": "冗余"},
            {"name": "org_id", "display_name": "组织 ID"},
            {"name": "org_name", "display_name": "组织名称", "description": "冗余"},
            {"name": "course_id", "display_name": "课程 ID"},
            {"name": "course_name", "display_name": "课程名称", "description": "冗余"},
            {"name": "category_id", "display_name": "类别 ID"},
            {"name": "category_name", "display_name": "类别名称", "description": "冗余"},
            {"name": "category_type", "display_name": "类别大类", "description": "冗余"},
            {"name": "enroll_status", "display_name": "报名状态"},
            {"name": "completion_status", "display_name": "完成状态"},
            {"name": "attendance_status", "display_name": "出勤状态"},
            {"name": "exam_score", "display_name": "考核分数"},
            {"name": "pass_flag", "display_name": "是否通过", "description": "0/1"},
            {"name": "training_hours", "display_name": "实际学时"},
            {"name": "training_cost", "display_name": "培训费用"},
            {"name": "satisfaction_score", "display_name": "满意度"},
            {"name": "instructor", "display_name": "实际讲师"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_training_plan": {
        "display_name": "培训计划明细",
        "description": "组织×类别×期间计划指标",
        "columns": [
            {"name": "plan_id", "display_name": "计划批次"},
            {"name": "line_id", "display_name": "计划行 ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date"},
            {"name": "fiscal_year", "display_name": "计划年度"},
            {"name": "fiscal_period", "display_name": "计划期间", "description": "1-12"},
            {"name": "plan_version", "display_name": "计划版本"},
            {"name": "org_id", "display_name": "组织 ID"},
            {"name": "org_name", "display_name": "组织名称", "description": "冗余"},
            {"name": "category_id", "display_name": "类别 ID"},
            {"name": "category_name", "display_name": "类别名称", "description": "冗余"},
            {"name": "category_type", "display_name": "类别大类", "description": "冗余"},
            {"name": "course_id", "display_name": "课程 ID", "description": "可选"},
            {"name": "course_name", "display_name": "课程名称", "description": "冗余"},
            {"name": "plan_headcount", "display_name": "计划人次"},
            {"name": "plan_hours", "display_name": "计划学时"},
            {"name": "plan_cost", "display_name": "计划费用"},
            {"name": "target_completion_rate", "display_name": "目标完成率"},
            {"name": "target_pass_rate", "display_name": "目标通过率"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
}


def _link_extra(keys):
    return {"join_spec": {"join_keys": keys}}


def main():
    s = space.get(SPACE_ID)
    output.print("=== 员工培训01 本体初始化 ===")
    output.print(f"空间: {SPACE_ID}")

    output.print("\n[1/8] 创建物理表...")
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_employee (
            employee_id String, employee_code String, employee_name String,
            org_id String, org_name String, job_title String, job_level String,
            hire_date Date, employment_status String, status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree() ORDER BY (org_id, employee_code)
    """)
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_training_category (
            category_id String, category_code String, category_name String,
            category_type String, parent_category_id String,
            category_level Int32, is_mandatory UInt8, status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree() ORDER BY (category_type, category_code)
    """)
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_course (
            course_id String, course_code String, course_name String,
            category_id String, category_name String, category_type String,
            delivery_mode String, standard_hours Float64, is_mandatory UInt8,
            cert_valid_months Int32, instructor String, status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree() ORDER BY (category_id, course_code)
    """)
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_training_record (
            record_id String, session_id String, date_key Int32,
            training_date Date, fiscal_year Int32, fiscal_period Int32,
            employee_id String, employee_name String,
            org_id String, org_name String,
            course_id String, course_name String,
            category_id String, category_name String, category_type String,
            enroll_status String, completion_status String, attendance_status String,
            exam_score Float64, pass_flag UInt8,
            training_hours Float64, training_cost Float64, satisfaction_score Float64,
            instructor String, created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (fiscal_year, fiscal_period, org_id, employee_id, record_id)
    """)
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_training_plan (
            plan_id String, line_id String, date_key Int32,
            fiscal_year Int32, fiscal_period Int32, plan_version String,
            org_id String, org_name String,
            category_id String, category_name String, category_type String,
            course_id String, course_name String,
            plan_headcount Int32, plan_hours Float64, plan_cost Float64,
            target_completion_rate Float64, target_pass_rate Float64,
            status String, created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (fiscal_year, fiscal_period, org_id, category_id, line_id)
    """)
    output.print("OK 5 张新表")

    output.print("\n[2/8] 注册表到空间...")
    for tbl, meta in TABLE_REGISTRY.items():
        s.tables.register_with_meta(
            table_name=tbl,
            display_name=meta["display_name"],
            description=meta.get("description"),
            columns=meta["columns"],
            force_column_meta=True,
        )
    output.print(f"OK {len(TABLE_REGISTRY)} 张表")

    output.print("\n[3/8] 注册表间关系...")
    table_relationships = [
        {"from_table": "fact_training_record", "to_table": "dim_date",
         "join_sql": "fact_training_record.date_key = dim_date.date_key",
         "join_keys": [{"from": "date_key", "to": "date_key"}],
         "relationship_type": "many_to_one", "description": "参训记录→日历"},
        {"from_table": "fact_training_record", "to_table": "dim_employee",
         "join_sql": "fact_training_record.employee_id = dim_employee.employee_id",
         "join_keys": [{"from": "employee_id", "to": "employee_id"}],
         "relationship_type": "many_to_one", "description": "记录→员工"},
        {"from_table": "fact_training_record", "to_table": "dim_course",
         "join_sql": "fact_training_record.course_id = dim_course.course_id",
         "join_keys": [{"from": "course_id", "to": "course_id"}],
         "relationship_type": "many_to_one", "description": "记录→课程"},
        {"from_table": "fact_training_record", "to_table": "dim_training_category",
         "join_sql": "fact_training_record.category_id = dim_training_category.category_id",
         "join_keys": [{"from": "category_id", "to": "category_id"}],
         "relationship_type": "many_to_one", "description": "记录→类别"},
        {"from_table": "fact_training_record", "to_table": "dim_org",
         "join_sql": "fact_training_record.org_id = dim_org.org_id",
         "join_keys": [{"from": "org_id", "to": "org_id"}],
         "relationship_type": "many_to_one", "description": "记录→组织"},
        {"from_table": "fact_training_plan", "to_table": "dim_date",
         "join_sql": "fact_training_plan.date_key = dim_date.date_key",
         "join_keys": [{"from": "date_key", "to": "date_key"}],
         "relationship_type": "many_to_one", "description": "计划→日历"},
        {"from_table": "fact_training_plan", "to_table": "dim_org",
         "join_sql": "fact_training_plan.org_id = dim_org.org_id",
         "join_keys": [{"from": "org_id", "to": "org_id"}],
         "relationship_type": "many_to_one", "description": "计划→组织"},
        {"from_table": "fact_training_plan", "to_table": "dim_training_category",
         "join_sql": "fact_training_plan.category_id = dim_training_category.category_id",
         "join_keys": [{"from": "category_id", "to": "category_id"}],
         "relationship_type": "many_to_one", "description": "计划→类别"},
        {"from_table": "fact_training_plan", "to_table": "dim_course",
         "join_sql": "fact_training_plan.course_id = dim_course.course_id",
         "join_keys": [{"from": "course_id", "to": "course_id"}],
         "relationship_type": "many_to_one", "description": "计划→课程"},
        {"from_table": "dim_employee", "to_table": "dim_org",
         "join_sql": "dim_employee.org_id = dim_org.org_id",
         "join_keys": [{"from": "org_id", "to": "org_id"}],
         "relationship_type": "many_to_one", "description": "员工→组织"},
        {"from_table": "dim_course", "to_table": "dim_training_category",
         "join_sql": "dim_course.category_id = dim_training_category.category_id",
         "join_keys": [{"from": "category_id", "to": "category_id"}],
         "relationship_type": "many_to_one", "description": "课程→类别"},
        {"from_table": "dim_training_category", "to_table": "dim_training_category",
         "join_sql": "dim_training_category.parent_category_id = dim_training_category.category_id",
         "join_keys": [{"from": "parent_category_id", "to": "category_id"}],
         "relationship_type": "many_to_one", "description": "类别树"},
    ]
    for rel in table_relationships:
        s.tables.add_relationship(**rel)
    output.print(f"OK {len(table_relationships)} 条关系")

    output.print("\n[4/8] 注册 Cube...")
    s.register_cube(
        name="EmployeeCube", table="dim_employee", title="员工Cube",
        measures=[
            {"name": "employee_count", "col": "employee_id", "agg": "uniq", "title": "在职员工数"},
        ],
        dimensions=[
            {"name": "employee_id", "col": "employee_id", "type": "string", "title": "员工ID"},
            {"name": "employee_code", "col": "employee_code", "type": "string", "title": "工号"},
            {"name": "employee_name", "col": "employee_name", "type": "string", "title": "姓名"},
            {"name": "org_id", "col": "org_id", "type": "string", "title": "组织ID"},
            {"name": "org_name", "col": "org_name", "type": "string", "title": "组织名称"},
            {"name": "job_title", "col": "job_title", "type": "string", "title": "岗位"},
            {"name": "job_level", "col": "job_level", "type": "string", "title": "职级"},
            {"name": "employment_status", "col": "employment_status", "type": "string", "title": "在职状态"},
        ],
    )
    s.register_cube(
        name="CourseCube", table="dim_course", title="课程Cube",
        measures=[
            {"name": "course_count", "col": "course_id", "agg": "count", "title": "课程数"},
            {"name": "standard_hours_total", "col": "standard_hours", "agg": "sum", "title": "标准学时合计"},
        ],
        dimensions=[
            {"name": "course_id", "col": "course_id", "type": "string", "title": "课程ID"},
            {"name": "course_code", "col": "course_code", "type": "string", "title": "课程编码"},
            {"name": "course_name", "col": "course_name", "type": "string", "title": "课程名称"},
            {"name": "category_id", "col": "category_id", "type": "string", "title": "类别ID"},
            {"name": "category_name", "col": "category_name", "type": "string", "title": "类别名称"},
            {"name": "category_type", "col": "category_type", "type": "string", "title": "类别大类"},
            {"name": "delivery_mode", "col": "delivery_mode", "type": "string", "title": "授课方式"},
            {"name": "is_mandatory", "col": "is_mandatory", "type": "int", "title": "是否必修"},
        ],
    )
    record_dims = [
        {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
        {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "财年"},
        {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "期间"},
        {"name": "org_id", "col": "org_id", "type": "string", "title": "组织ID"},
        {"name": "org_name", "col": "org_name", "type": "string", "title": "组织名称"},
        {"name": "employee_id", "col": "employee_id", "type": "string", "title": "员工ID"},
        {"name": "course_id", "col": "course_id", "type": "string", "title": "课程ID"},
        {"name": "course_name", "col": "course_name", "type": "string", "title": "课程名称"},
        {"name": "category_id", "col": "category_id", "type": "string", "title": "类别ID"},
        {"name": "category_name", "col": "category_name", "type": "string", "title": "类别名称"},
        {"name": "category_type", "col": "category_type", "type": "string", "title": "类别大类"},
        {"name": "completion_status", "col": "completion_status", "type": "string", "title": "完成状态"},
        {"name": "pass_flag", "col": "pass_flag", "type": "int", "title": "是否通过"},
    ]
    s.register_cube(
        name="TrainingRecordCube", table="fact_training_record", title="参训记录Cube",
        measures=[
            {"name": "enroll_count", "col": "record_id", "agg": "count", "title": "参训人次"},
            {"name": "complete_count", "col": "record_id", "agg": "count", "title": "完成人次"},
            {"name": "pass_count", "col": "record_id", "agg": "count", "title": "通过人次"},
            {"name": "training_hours_total", "col": "training_hours", "agg": "sum", "title": "总学时"},
            {"name": "training_cost_total", "col": "training_cost", "agg": "sum", "title": "总费用"},
            {"name": "avg_exam_score", "col": "exam_score", "agg": "avg", "title": "平均考核分"},
            {"name": "avg_satisfaction", "col": "satisfaction_score", "agg": "avg", "title": "平均满意度"},
        ],
        dimensions=record_dims,
    )
    plan_dims = [
        {"name": "plan_version", "col": "plan_version", "type": "string", "title": "计划版本"},
        {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "计划年度"},
        {"name": "fiscal_period", "col": "fiscal_period", "type": "int", "title": "计划期间"},
        {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
        {"name": "org_id", "col": "org_id", "type": "string", "title": "组织ID"},
        {"name": "org_name", "col": "org_name", "type": "string", "title": "组织名称"},
        {"name": "category_id", "col": "category_id", "type": "string", "title": "类别ID"},
        {"name": "category_name", "col": "category_name", "type": "string", "title": "类别名称"},
        {"name": "category_type", "col": "category_type", "type": "string", "title": "类别大类"},
        {"name": "course_id", "col": "course_id", "type": "string", "title": "课程ID"},
    ]
    s.register_cube(
        name="TrainingPlanCube", table="fact_training_plan", title="培训计划Cube",
        measures=[
            {"name": "plan_headcount", "col": "plan_headcount", "agg": "sum", "title": "计划人次"},
            {"name": "plan_hours", "col": "plan_hours", "agg": "sum", "title": "计划学时"},
            {"name": "plan_cost", "col": "plan_cost", "agg": "sum", "title": "计划费用"},
            {"name": "plan_lines", "col": "line_id", "agg": "count", "title": "计划行数"},
        ],
        dimensions=plan_dims,
    )
    s.register_cube(
        name="OrgTrainingCube", table="fact_training_plan", title="组织培训对比Cube",
        measures=[
            {"name": "plan_headcount", "col": "plan_headcount", "agg": "sum", "title": "计划人次"},
            {"name": "plan_hours", "col": "plan_hours", "agg": "sum", "title": "计划学时"},
            {"name": "plan_cost", "col": "plan_cost", "agg": "sum", "title": "计划费用"},
        ],
        dimensions=plan_dims,
    )
    s.register_cube(
        name="ComplianceCube", table="fact_training_record", title="合规分析Cube",
        measures=[
            {"name": "enroll_count", "col": "record_id", "agg": "count", "title": "参训人次"},
            {"name": "pass_count", "col": "record_id", "agg": "count", "title": "通过人次"},
            {"name": "training_hours_total", "col": "training_hours", "agg": "sum", "title": "总学时"},
        ],
        dimensions=record_dims,
    )
    output.print("OK 6 个 Cube")

    output.print("\n[5/8] 配置派生度量...")
    s.upsert_derived_measures("TrainingRecordCube", [
        {"name": "completion_rate", "title": "完成率",
         "expression": "if(TrainingRecordCube.enroll_count > 0, TrainingRecordCube.complete_count / TrainingRecordCube.enroll_count, 0)",
         "description": "完成/参训"},
        {"name": "pass_rate", "title": "通过率",
         "expression": "if(TrainingRecordCube.complete_count > 0, TrainingRecordCube.pass_count / TrainingRecordCube.complete_count, 0)",
         "description": "通过/完成"},
    ])
    s.upsert_derived_measures("TrainingPlanCube", [
        {"name": "avg_target_completion", "title": "平均目标完成率",
         "expression": "avg(target_completion_rate)", "description": "计划目标"},
        {"name": "avg_target_pass", "title": "平均目标通过率",
         "expression": "avg(target_pass_rate)", "description": "计划目标"},
    ])
    output.print("OK 派生度量")

    output.print("\n[6/8] 定义对象类型...")
    objects = [
        ("Employee", "员工", "员工主数据", "主数据", "EmployeeCube"),
        ("Course", "课程", "培训课程目录", "主数据", "CourseCube"),
        ("TrainingCategory", "培训类别", "培训类别树", "参考", None),
        ("TrainingRecord", "参训记录", "培训参训完成明细", "事务", "TrainingRecordCube"),
        ("TrainingPlan", "培训计划", "培训计划编制行", "事务", "TrainingPlanCube"),
        ("TrainingAnalysis", "培训分析", "组织培训指标聚合", "分析", "TrainingRecordCube"),
        ("ComplianceAnalysis", "合规分析", "必修合规完成情况", "分析", "ComplianceCube"),
    ]
    for code, name, desc, cat, cube in objects:
        s.onto.define_object_type(code=code, name=name, description=desc, category_347=cat)
        if cube:
            s.onto.bind_source(code, "dazi_cube", config={"cube": cube})
    s.onto.define_object_type(code="Org", name="组织", description="组织主数据", category_347="主数据")
    s.onto.bind_source("Org", "dazi_cube", config={"cube": "TrainingRecordCube"})
    output.print(f"OK {len(objects) + 1} 个对象")

    output.print("\n[7/8] 定义对象属性...")
    s.onto.define_property("Employee", "id", "员工ID", semantic_role="dimension",
                           qualified_name="EmployeeCube.employee_id")
    s.onto.define_property("Employee", "code", "工号", semantic_role="dimension",
                           qualified_name="EmployeeCube.employee_code")
    s.onto.define_property("Employee", "name", "姓名", semantic_role="dimension",
                           qualified_name="EmployeeCube.employee_name")
    s.onto.define_property("Employee", "org_id", "所属组织", semantic_role="dimension",
                           qualified_name="EmployeeCube.org_id")
    s.onto.define_property("Employee", "headcount", "人数", semantic_role="measure",
                           qualified_name="EmployeeCube.employee_count")

    s.onto.define_property("Course", "id", "课程ID", semantic_role="dimension",
                           qualified_name="CourseCube.course_id")
    s.onto.define_property("Course", "name", "课程名称", semantic_role="dimension",
                           qualified_name="CourseCube.course_name")
    s.onto.define_property("Course", "category_type", "类别大类", semantic_role="dimension",
                           qualified_name="CourseCube.category_type")

    s.onto.define_property("TrainingRecord", "hours", "学时", semantic_role="measure",
                           qualified_name="TrainingRecordCube.training_hours_total")
    s.onto.define_property("TrainingRecord", "cost", "费用", semantic_role="measure",
                           qualified_name="TrainingRecordCube.training_cost_total")
    s.onto.define_property("TrainingRecord", "completion_rate", "完成率", semantic_role="measure",
                           qualified_name="TrainingRecordCube.completion_rate")
    s.onto.define_property("TrainingRecord", "pass_rate", "通过率", semantic_role="measure",
                           qualified_name="TrainingRecordCube.pass_rate")
    s.onto.define_property("TrainingRecord", "exam_score", "考核分", semantic_role="measure",
                           qualified_name="TrainingRecordCube.avg_exam_score")

    s.onto.define_property("TrainingPlan", "version", "计划版本", semantic_role="dimension",
                           qualified_name="TrainingPlanCube.plan_version")
    s.onto.define_property("TrainingPlan", "plan_hours", "计划学时", semantic_role="measure",
                           qualified_name="TrainingPlanCube.plan_hours")
    s.onto.define_property("TrainingPlan", "plan_headcount", "计划人次", semantic_role="measure",
                           qualified_name="TrainingPlanCube.plan_headcount")

    s.onto.define_property("TrainingAnalysis", "hours", "学时", semantic_role="measure",
                           qualified_name="TrainingRecordCube.training_hours_total")
    s.onto.define_property("TrainingAnalysis", "completion_rate", "完成率", semantic_role="measure",
                           qualified_name="TrainingRecordCube.completion_rate")
    s.onto.define_property("TrainingAnalysis", "period", "期间", semantic_role="dimension",
                           qualified_name="TrainingRecordCube.fiscal_year")

    s.onto.define_property("ComplianceAnalysis", "pass_count", "通过人次", semantic_role="measure",
                           qualified_name="ComplianceCube.pass_count")
    s.onto.define_property("ComplianceAnalysis", "enroll_count", "参训人次", semantic_role="measure",
                           qualified_name="ComplianceCube.enroll_count")
    s.onto.define_property("Org", "org_id", "组织ID", semantic_role="dimension",
                           qualified_name="TrainingRecordCube.org_id")
    s.onto.define_property("Org", "org_name", "组织名称", semantic_role="dimension",
                           qualified_name="TrainingRecordCube.org_name")
    output.print("OK 属性定义")

    output.print("\n[8/8] 定义链接类型...")
    link_defs = [
        ("employee_belongs_org", "员工归属组织", "Employee", "Org", "归属关系",
         "many_to_one", _link_extra([{"from": "org_id", "to": "org_id"}])),
        ("record_for_employee", "记录归属员工", "TrainingRecord", "Employee", "归属关系",
         "many_to_one", _link_extra([{"from": "employee_id", "to": "id"}])),
        ("record_for_course", "记录对应课程", "TrainingRecord", "Course", "归属关系",
         "many_to_one", _link_extra([{"from": "course_id", "to": "id"}])),
        ("record_for_org", "记录归属组织", "TrainingRecord", "Org", "归属关系",
         "many_to_one", _link_extra([{"from": "org_id", "to": "org_id"}])),
        ("course_in_category", "课程所属类别", "Course", "TrainingCategory", "归属关系",
         "many_to_one", _link_extra([{"from": "category_id", "to": "id"}])),
        ("plan_for_org", "计划对应组织", "TrainingPlan", "Org", "归属关系",
         "many_to_one", _link_extra([{"from": "org_id", "to": "org_id"}])),
        ("plan_for_category", "计划对应类别", "TrainingPlan", "TrainingCategory", "归属关系",
         "many_to_one", _link_extra([{"from": "category_id", "to": "id"}])),
        ("category_has_parent", "类别上级", "TrainingCategory", "TrainingCategory", "层级关系",
         "many_to_one", _link_extra([{"from": "parent_category_id", "to": "id"}])),
        ("org_has_parent", "组织上级", "Org", "Org", "层级关系",
         "many_to_one", _link_extra([{"from": "parent_org_id", "to": "org_id"}])),
        ("analysis_by_org", "按组织切片", "TrainingAnalysis", "Org", "分析归因",
         "many_to_one", _link_extra([{"from": "org_id", "to": "org_id"}])),
        ("analysis_by_category", "按类别切片", "TrainingAnalysis", "TrainingCategory", "分析归因",
         "many_to_one", _link_extra([{"from": "category_id", "to": "id"}])),
        ("compliance_for_course", "合规按课程", "ComplianceAnalysis", "Course", "分析归因",
         "many_to_one", _link_extra([{"from": "course_id", "to": "id"}])),
    ]
    for code, name, fr, to, cat, card, extra in link_defs:
        s.onto.define_link_type(
            code=code, name=name,
            from_object_type_code=fr, to_object_type_code=to,
            category_347=cat, cardinality=card, extra=extra,
        )
    output.print(f"OK {len(link_defs)} 条链接")

    s.sync_metric_refs()
    s.onto.engine.invalidate()
    output.print("OK sync_metric_refs")

    summary = {
        "ok": True,
        "space_id": SPACE_ID,
        "tables_new": len(TABLE_REGISTRY),
        "relationships": len(table_relationships),
        "cubes": 6,
        "objects": len(objects) + 1,
        "links": len(link_defs),
    }
    output.success("员工培训01 本体初始化完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True))
