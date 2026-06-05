"""员工培训本体初始化脚本 — space__0519

初始化内容：
1. 创建物理表（5 张）
2. 注册表到空间
3. 注册 Cube（5 个）及派生度量
4. 定义对象类型（5 种）、绑定数据源、属性、链接
5. 同步指标引用

放置：项目/onto_本体项目01/脚本/setup/training_ontology_init.py
发布：dazi-onto script publish 项目/onto_本体项目01/脚本/setup/training_ontology_init.py --space space__0519
"""

import json


def main():
    space_id = "space__0519"
    s = space.get(space_id)

    output.print("=== 员工培训本体初始化 ===")
    output.print(f"空间: {space_id}")

    # 1. 创建物理表
    output.print("\n[1/8] 创建物理表...")

    s.sql.execute("DROP TABLE IF EXISTS employee_master")
    s.sql.execute("DROP TABLE IF EXISTS course_master")
    s.sql.execute("DROP TABLE IF EXISTS trainer_master")
    s.sql.execute("DROP TABLE IF EXISTS training_record")
    s.sql.execute("DROP TABLE IF EXISTS training_evaluation")
    output.print("OK 清理旧表")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS employee_master (
            employee_id String,
            employee_code String,
            employee_name String,
            department String,
            position String,
            level String,
            hire_date Date,
            status String,
            created_at DateTime DEFAULT now(),
            updated_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (employee_id)
    """)
    output.print("OK employee_master")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS course_master (
            course_id String,
            course_code String,
            course_name String,
            course_category String,
            course_level String,
            duration_hours Float64,
            required Boolean,
            trainer_id String,
            capacity Int32,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (course_id)
    """)
    output.print("OK course_master")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS trainer_master (
            trainer_id String,
            trainer_name String,
            department String,
            expertise String,
            qualification String,
            status String
        ) ENGINE = MergeTree()
        ORDER BY (trainer_id)
    """)
    output.print("OK trainer_master")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS training_record (
            record_id String,
            employee_id String,
            employee_name String,
            department String,
            position String,
            level String,
            hire_date Date,
            course_id String,
            course_name String,
            course_category String,
            course_level String,
            trainer_id String,
            trainer_name String,
            trainer_department String,
            trainer_expertise String,
            training_date Date,
            attendance String,
            completion String,
            score Float64,
            certificate_no String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (training_date, employee_id, course_id)
    """)
    output.print("OK training_record")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS training_evaluation (
            evaluation_id String,
            record_id String,
            employee_id String,
            course_id String,
            trainer_id String,
            trainer_score Float64,
            content_score Float64,
            environment_score Float64,
            overall_score Float64,
            suggestion String,
            evaluated_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (record_id)
    """)
    output.print("OK training_evaluation")

    # 2. 注册表
    output.print("\n[2/8] 注册表到空间...")

    for tbl, label in [
        ("employee_master", "员工主数据表"),
        ("course_master", "培训课程主数据表"),
        ("trainer_master", "讲师主数据表"),
        ("training_record", "培训记录事实表"),
        ("training_evaluation", "培训评估事实表"),
    ]:
        s.tables.register(tbl, label=label)
        s.tables.sync_columns(tbl)
        output.print(f"OK {tbl}")

    # 3. 注册 Cube
    output.print("\n[3/8] 注册 Cube...")

    fact = "training_record"
    eval_fact = "training_evaluation"

    s.register_cube(
        name="TrainingCube",
        table=fact,
        title="培训分析主Cube",
        measures=[
            {"name": "total_records", "col": "record_id", "agg": "count", "title": "培训记录数"},
            {"name": "avg_score", "col": "score", "agg": "avg", "title": "平均成绩"},
        ],
        dimensions=[
            {"name": "record_id", "col": "record_id", "type": "string", "title": "记录ID"},
            {"name": "employee_id", "col": "employee_id", "type": "string", "title": "员工ID"},
            {"name": "employee_name", "col": "employee_name", "type": "string", "title": "员工姓名"},
            {"name": "department", "col": "department", "type": "string", "title": "部门"},
            {"name": "position", "col": "position", "type": "string", "title": "岗位"},
            {"name": "level", "col": "level", "type": "string", "title": "职级"},
            {"name": "course_id", "col": "course_id", "type": "string", "title": "课程ID"},
            {"name": "course_name", "col": "course_name", "type": "string", "title": "课程名称"},
            {"name": "course_category", "col": "course_category", "type": "string", "title": "课程类别"},
            {"name": "course_level", "col": "course_level", "type": "string", "title": "课程级别"},
            {"name": "trainer_id", "col": "trainer_id", "type": "string", "title": "讲师ID"},
            {"name": "trainer_name", "col": "trainer_name", "type": "string", "title": "讲师姓名"},
            {"name": "training_date", "col": "training_date", "type": "date", "title": "培训日期"},
            {"name": "attendance", "col": "attendance", "type": "string", "title": "出勤状态"},
            {"name": "completion", "col": "completion", "type": "string", "title": "完成状态"},
            {"name": "certificate_no", "col": "certificate_no", "type": "string", "title": "证书编号"},
        ],
    )
    output.print("OK TrainingCube")

    s.register_cube(
        name="EmployeeTrainingCube",
        table=fact,
        title="员工培训Cube",
        measures=[
            {"name": "total_records", "col": "record_id", "agg": "count", "title": "培训记录数"},
            {"name": "avg_score", "col": "score", "agg": "avg", "title": "平均成绩"},
        ],
        dimensions=[
            {"name": "employee_id", "col": "employee_id", "type": "string", "title": "员工ID"},
            {"name": "employee_name", "col": "employee_name", "type": "string", "title": "员工姓名"},
            {"name": "department", "col": "department", "type": "string", "title": "部门"},
            {"name": "position", "col": "position", "type": "string", "title": "岗位"},
            {"name": "level", "col": "level", "type": "string", "title": "职级"},
            {"name": "hire_date", "col": "hire_date", "type": "date", "title": "入职日期"},
            {"name": "training_date", "col": "training_date", "type": "date", "title": "培训日期"},
            {"name": "completion", "col": "completion", "type": "string", "title": "完成状态"},
        ],
    )
    output.print("OK EmployeeTrainingCube")

    s.register_cube(
        name="CourseTrainingCube",
        table=fact,
        title="课程培训Cube",
        measures=[
            {"name": "total_records", "col": "record_id", "agg": "count", "title": "培训记录数"},
            {"name": "avg_score", "col": "score", "agg": "avg", "title": "平均成绩"},
        ],
        dimensions=[
            {"name": "course_id", "col": "course_id", "type": "string", "title": "课程ID"},
            {"name": "course_name", "col": "course_name", "type": "string", "title": "课程名称"},
            {"name": "course_category", "col": "course_category", "type": "string", "title": "课程类别"},
            {"name": "course_level", "col": "course_level", "type": "string", "title": "课程级别"},
            {"name": "training_date", "col": "training_date", "type": "date", "title": "培训日期"},
            {"name": "completion", "col": "completion", "type": "string", "title": "完成状态"},
        ],
    )
    output.print("OK CourseTrainingCube")

    s.register_cube(
        name="TrainerPerformanceCube",
        table=eval_fact,
        title="讲师绩效Cube",
        measures=[
            {"name": "trainer_score", "col": "trainer_score", "agg": "avg", "title": "讲师评分"},
            {"name": "content_score", "col": "content_score", "agg": "avg", "title": "内容评分"},
            {"name": "environment_score", "col": "environment_score", "agg": "avg", "title": "环境评分"},
            {"name": "overall_score", "col": "overall_score", "agg": "avg", "title": "综合评分"},
            {"name": "evaluation_count", "col": "evaluation_id", "agg": "count", "title": "评估次数"},
        ],
        dimensions=[
            {"name": "trainer_id", "col": "trainer_id", "type": "string", "title": "讲师ID"},
            {"name": "trainer_name", "col": "record_id", "type": "string", "title": "讲师姓名"},
            {"name": "department", "col": "record_id", "type": "string", "title": "所属部门"},
            {"name": "expertise", "col": "record_id", "type": "string", "title": "专业领域"},
            {"name": "course_id", "col": "course_id", "type": "string", "title": "课程ID"},
        ],
    )
    output.print("OK TrainerPerformanceCube")

    s.register_cube(
        name="TimeTrainingCube",
        table=fact,
        title="时间维度培训Cube",
        measures=[
            {"name": "total_records", "col": "record_id", "agg": "count", "title": "培训记录数"},
            {"name": "avg_score", "col": "score", "agg": "avg", "title": "平均成绩"},
        ],
        dimensions=[
            {"name": "training_date", "col": "training_date", "type": "date", "title": "培训日期"},
            {"name": "year_month", "col": "training_date", "type": "string", "title": "年月"},
            {"name": "quarter", "col": "training_date", "type": "string", "title": "季度"},
            {"name": "year", "col": "training_date", "type": "date", "title": "年份"},
        ],
    )
    output.print("OK TimeTrainingCube")

    # 4. 派生度量
    output.print("\n[4/8] 配置派生度量...")

    s.upsert_derived_measures(
        "TrainingCube",
        [
            {
                "name": "attendance_rate",
                "title": "出勤率",
                "expression": "sum(attendance='出勤') / TrainingCube.total_records * 100",
                "description": "出勤人数/总人数 * 100",
            },
            {
                "name": "completion_rate",
                "title": "完成率",
                "expression": "sum(completion='完成') / TrainingCube.total_records * 100",
                "description": "完成人数/总人数 * 100",
            },
            {
                "name": "qualified_count",
                "title": "合格人数",
                "expression": "sum(score >= 60)",
                "description": "成绩>=60的人数",
            },
            {
                "name": "qualified_rate",
                "title": "合格率",
                "expression": "sum(score >= 60) / TrainingCube.total_records * 100",
                "description": "合格人数/总人数 * 100",
            },
        ],
    )
    s.upsert_derived_measures(
        "EmployeeTrainingCube",
        [
            {
                "name": "completion_rate",
                "title": "完成率",
                "expression": "sum(completion='完成') / EmployeeTrainingCube.total_records * 100",
                "description": "员工培训完成率",
            },
            {
                "name": "qualified_rate",
                "title": "合格率",
                "expression": "sum(score >= 60) / EmployeeTrainingCube.total_records * 100",
                "description": "员工合格率",
            },
        ],
    )
    s.upsert_derived_measures(
        "CourseTrainingCube",
        [
            {
                "name": "completion_rate",
                "title": "完成率",
                "expression": "sum(completion='完成') / CourseTrainingCube.total_records * 100",
                "description": "课程完成率",
            },
            {
                "name": "qualified_rate",
                "title": "合格率",
                "expression": "sum(score >= 60) / CourseTrainingCube.total_records * 100",
                "description": "课程合格率",
            },
        ],
    )
    output.print("OK 派生度量")

    # 5. 对象类型
    output.print("\n[5/8] 定义对象类型...")

    object_types = [
        ("Employee", "员工", "企业员工业务对象"),
        ("Course", "课程", "培训课程业务对象"),
        ("Trainer", "讲师", "培训讲师业务对象"),
        ("TrainingRecord", "培训记录", "员工培训记录业务对象"),
        ("TrainingAnalysis", "培训分析", "多维度培训指标聚合对象"),
    ]
    for code, name, desc in object_types:
        s.onto.define_object_type(code, name, description=desc)
        output.print(f"OK {code}")

    # 6. 绑定数据源
    output.print("\n[6/8] 绑定数据源...")

    bindings = [
        ("Employee", "EmployeeTrainingCube"),
        ("Course", "CourseTrainingCube"),
        ("Trainer", "TrainerPerformanceCube"),
        ("TrainingRecord", "TrainingCube"),
        ("TrainingAnalysis", "TrainingCube"),
    ]
    for obj, cube in bindings:
        s.onto.bind_source(obj, "dazi_cube", config={"cube": cube})
        output.print(f"OK {obj} -> {cube}")

    # 7. 属性
    output.print("\n[7/8] 定义属性...")

    def define_props(obj_code, props):
        for code, name, role, qn in props:
            s.onto.define_property(obj_code, code, name, semantic_role=role, qualified_name=qn)

    define_props("Employee", [
        ("id", "员工ID", "dimension", "EmployeeTrainingCube.employee_id"),
        ("department", "部门", "dimension", "EmployeeTrainingCube.department"),
        ("position", "岗位", "dimension", "EmployeeTrainingCube.position"),
        ("level", "职级", "dimension", "EmployeeTrainingCube.level"),
        ("name", "员工姓名", "dimension", "EmployeeTrainingCube.employee_name"),
        ("hire_date", "入职日期", "dimension", "EmployeeTrainingCube.hire_date"),
        ("total_trainings", "累计培训次数", "measure", "EmployeeTrainingCube.total_records"),
        ("completion_rate", "培训完成率", "measure", "EmployeeTrainingCube.completion_rate"),
        ("avg_score", "平均成绩", "measure", "EmployeeTrainingCube.avg_score"),
        ("qualified_rate", "合格率", "measure", "EmployeeTrainingCube.qualified_rate"),
    ])
    output.print("OK Employee 属性 (10)")

    define_props("Course", [
        ("id", "课程ID", "dimension", "CourseTrainingCube.course_id"),
        ("category", "课程类别", "dimension", "CourseTrainingCube.course_category"),
        ("level", "课程级别", "dimension", "CourseTrainingCube.course_level"),
        ("name", "课程名称", "dimension", "CourseTrainingCube.course_name"),
        ("trained_count", "培训人次", "measure", "CourseTrainingCube.total_records"),
        ("completion_rate", "完成率", "measure", "CourseTrainingCube.completion_rate"),
        ("avg_score", "平均成绩", "measure", "CourseTrainingCube.avg_score"),
        ("qualified_rate", "合格率", "measure", "CourseTrainingCube.qualified_rate"),
    ])
    output.print("OK Course 属性 (8)")

    define_props("Trainer", [
        ("id", "讲师ID", "dimension", "TrainerPerformanceCube.trainer_id"),
        ("name", "讲师姓名", "dimension", "TrainerPerformanceCube.trainer_name"),
        ("avg_trainer_score", "讲师评分", "measure", "TrainerPerformanceCube.trainer_score"),
        ("avg_content_score", "内容评分", "measure", "TrainerPerformanceCube.content_score"),
        ("avg_environment_score", "环境评分", "measure", "TrainerPerformanceCube.environment_score"),
        ("avg_overall_score", "综合评分", "measure", "TrainerPerformanceCube.overall_score"),
    ])
    output.print("OK Trainer 属性 (6)")

    define_props("TrainingRecord", [
        ("id", "记录ID", "dimension", "TrainingCube.record_id"),
        ("training_date", "培训日期", "dimension", "TrainingCube.training_date"),
        ("attendance", "出勤状态", "dimension", "TrainingCube.attendance"),
        ("completion", "完成状态", "dimension", "TrainingCube.completion"),
        ("score", "考核成绩", "measure", "TrainingCube.avg_score"),
        ("certificate_no", "证书编号", "dimension", "TrainingCube.certificate_no"),
    ])
    output.print("OK TrainingRecord 属性 (6)")

    define_props("TrainingAnalysis", [
        ("date", "日期", "dimension", "TrainingCube.training_date"),
        ("department", "部门", "dimension", "TrainingCube.department"),
        ("course_category", "课程类别", "dimension", "TrainingCube.course_category"),
        ("total_records", "培训人次", "measure", "TrainingCube.total_records"),
        ("attendance_rate", "出勤率", "measure", "TrainingCube.attendance_rate"),
        ("completion_rate", "完成率", "measure", "TrainingCube.completion_rate"),
        ("avg_score", "平均成绩", "measure", "TrainingCube.avg_score"),
        ("qualified_rate", "合格率", "measure", "TrainingCube.qualified_rate"),
    ])
    output.print("OK TrainingAnalysis 属性 (8)")

    # 8. 链接类型
    output.print("\n[8/8] 定义链接与同步指标...")

    link_types = [
        ("employee_takes_course", "员工参加课程", "Employee", "Course", "员工与课程的学习关系"),
        ("course_has_trainer", "课程由讲师授课", "Course", "Trainer", "课程与讲师关系"),
        ("record_belongs_employee", "记录归属员工", "TrainingRecord", "Employee", "培训记录所属员工"),
        ("record_for_course", "记录对应课程", "TrainingRecord", "Course", "培训记录对应课程"),
        ("analysis_by_employee", "分析归因员工", "TrainingAnalysis", "Employee", "指标按员工切片"),
        ("analysis_by_course", "分析归因课程", "TrainingAnalysis", "Course", "指标按课程切片"),
        ("analysis_by_trainer", "分析归因讲师", "TrainingAnalysis", "Trainer", "指标按讲师切片"),
        ("employee_evaluates", "员工评估", "Employee", "TrainingRecord", "员工对培训的评估"),
    ]
    for code, name, from_obj, to_obj, desc in link_types:
        s.onto.define_link_type(
            code=code,
            name=name,
            from_object_type_code=from_obj,
            to_object_type_code=to_obj,
            description=desc,
        )
        output.print(f"OK {code}")

    s.sync_metric_refs()
    output.print("OK sync_metric_refs")

    summary = {
        "ok": True,
        "space_id": space_id,
        "tables": 5,
        "cubes": 5,
        "object_types": 5,
        "properties": 38,
        "link_types": 8,
    }

    output.print("\n=== 员工培训本体初始化完成 ===")
    output.success("初始化成功")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))