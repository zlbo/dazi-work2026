"""员工培训演示数据灌入 — space__0519

前置：先执行 training_ontology_init.py 建表。
幂等：training_record 已有数据则跳过。

放置：项目/onto_本体项目01/脚本/setup/training_seed_data.py
"""

import json
import random
from datetime import date, datetime, timedelta

_SEED_DT = datetime(2025, 1, 1, 0, 0, 0)


def main():
    space_id = "space__0519"
    s = space.get(space_id)

    output.print("=== 员工培训演示数据灌入 ===")

    try:
        n = int(s.sql.query_one("SELECT count() FROM training_record") or 0)
    except Exception:
        n = 0
    if n > 0:
        output.print(f"training_record 已有 {n} 行，跳过灌数")
        output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "skipped": True, "rows": n}, ensure_ascii=True))
        return

    employees = [
        {"employee_id": "E001", "employee_code": "EMP-001", "employee_name": "张伟", "department": "技术部", "position": "软件工程师", "level": "P5", "hire_date": date(2023, 3, 15), "status": "在职"},
        {"employee_id": "E002", "employee_code": "EMP-002", "employee_name": "李娜", "department": "技术部", "position": "前端工程师", "level": "P5", "hire_date": date(2023, 6, 1), "status": "在职"},
        {"employee_id": "E003", "employee_code": "EMP-003", "employee_name": "王强", "department": "技术部", "position": "架构师", "level": "P7", "hire_date": date(2021, 8, 20), "status": "在职"},
        {"employee_id": "E004", "employee_code": "EMP-004", "employee_name": "刘芳", "department": "市场部", "position": "市场经理", "level": "P6", "hire_date": date(2022, 4, 10), "status": "在职"},
        {"employee_id": "E005", "employee_code": "EMP-005", "employee_name": "陈明", "department": "市场部", "position": "市场专员", "level": "P4", "hire_date": date(2024, 1, 5), "status": "在职"},
        {"employee_id": "E006", "employee_code": "EMP-006", "employee_name": "杨丽", "department": "人力资源部", "position": "HRBP", "level": "P5", "hire_date": date(2022, 9, 15), "status": "在职"},
        {"employee_id": "E007", "employee_code": "EMP-007", "employee_name": "赵磊", "department": "人力资源部", "position": "招聘专员", "level": "P4", "hire_date": date(2024, 2, 20), "status": "在职"},
        {"employee_id": "E008", "employee_code": "EMP-008", "employee_name": "周婷", "department": "财务部", "position": "会计", "level": "P5", "hire_date": date(2023, 7, 1), "status": "在职"},
        {"employee_id": "E009", "employee_code": "EMP-009", "employee_name": "吴刚", "department": "财务部", "position": "财务经理", "level": "P6", "hire_date": date(2021, 11, 8), "status": "在职"},
        {"employee_id": "E010", "employee_code": "EMP-010", "employee_name": "郑敏", "department": "技术部", "position": "测试工程师", "level": "P4", "hire_date": date(2024, 3, 10), "status": "在职"},
    ]
    for e in employees:
        e["created_at"] = _SEED_DT
        e["updated_at"] = _SEED_DT

    courses = [
        {"course_id": "C001", "course_code": "TECH-001", "course_name": "Python编程基础", "course_category": "技术", "course_level": "初级", "duration_hours": 16.0, "required": True, "trainer_id": "T001", "capacity": 30, "status": "启用"},
        {"course_id": "C002", "course_code": "TECH-002", "course_name": "数据分析实战", "course_category": "技术", "course_level": "中级", "duration_hours": 24.0, "required": False, "trainer_id": "T001", "capacity": 25, "status": "启用"},
        {"course_id": "C003", "course_code": "MGMT-001", "course_name": "项目管理入门", "course_category": "管理", "course_level": "初级", "duration_hours": 12.0, "required": True, "trainer_id": "T002", "capacity": 40, "status": "启用"},
        {"course_id": "C004", "course_code": "MGMT-002", "course_name": "团队领导力", "course_category": "管理", "course_level": "中级", "duration_hours": 20.0, "required": False, "trainer_id": "T002", "capacity": 20, "status": "启用"},
        {"course_id": "C005", "course_code": "GEN-001", "course_name": "商务沟通技巧", "course_category": "通用", "course_level": "初级", "duration_hours": 8.0, "required": True, "trainer_id": "T003", "capacity": 50, "status": "启用"},
        {"course_id": "C006", "course_code": "GEN-002", "course_name": "时间管理", "course_category": "通用", "course_level": "初级", "duration_hours": 6.0, "required": False, "trainer_id": "T003", "capacity": 40, "status": "启用"},
        {"course_id": "C007", "course_code": "TECH-003", "course_name": "云计算基础", "course_category": "技术", "course_level": "中级", "duration_hours": 20.0, "required": False, "trainer_id": "T001", "capacity": 30, "status": "启用"},
        {"course_id": "C008", "course_code": "MGMT-003", "course_name": "绩效管理", "course_category": "管理", "course_level": "高级", "duration_hours": 16.0, "required": False, "trainer_id": "T002", "capacity": 15, "status": "启用"},
    ]
    for c in courses:
        c["created_at"] = _SEED_DT

    trainers = [
        {"trainer_id": "T001", "trainer_name": "李教授", "department": "技术部", "expertise": "技术培训", "qualification": "高级讲师", "status": "在职"},
        {"trainer_id": "T002", "trainer_name": "王老师", "department": "人力资源部", "expertise": "管理培训", "qualification": "资深讲师", "status": "在职"},
        {"trainer_id": "T003", "trainer_name": "张顾问", "department": "市场部", "expertise": "通用技能", "qualification": "中级讲师", "status": "在职"},
    ]

    s.sql.insert_rows("employee_master", employees)
    s.sql.insert_rows("course_master", courses)
    s.sql.insert_rows("trainer_master", trainers)
    output.print("OK 维表数据")

    random.seed(519)
    
    emp_dict = {e["employee_id"]: e for e in employees}
    course_dict = {c["course_id"]: c for c in courses}
    trainer_dict = {t["trainer_id"]: t for t in trainers}

    fact_rows = []
    eval_rows = []
    record_seq = 1
    eval_seq = 1
    start = date(2025, 1, 1)
    end = date(2026, 5, 26)
    days = (end - start).days + 1

    for d_offset in range(days):
        training_date = start + timedelta(days=d_offset)
        if random.random() > 0.25:
            continue
        daily_trainings = random.randint(1, 4)
        for _ in range(daily_trainings):
            course = random.choice(courses)
            course_id = course["course_id"]
            trainer = trainer_dict.get(course["trainer_id"], {})
            participants = random.randint(3, min(10, course["capacity"]))
            for _ in range(participants):
                employee = random.choice(employees)
                employee_id = employee["employee_id"]
                attendance = random.choices(["出勤", "出勤", "出勤", "迟到", "缺勤"], weights=[0.7, 0.7, 0.7, 0.15, 0.15])[0]
                
                if attendance == "出勤":
                    completion = random.choices(["完成", "完成", "未完成"], weights=[0.8, 0.8, 0.2])[0]
                    if completion == "完成":
                        score = round(random.uniform(55, 100), 1)
                        if score >= 60:
                            certificate_no = f"CERT{training_date.strftime('%Y%m%d')}{record_seq:04d}"
                        else:
                            certificate_no = ""
                    else:
                        score = 0.0
                        certificate_no = ""
                else:
                    completion = "未完成"
                    score = 0.0
                    certificate_no = ""
                
                record_id = f"REC{training_date.strftime('%Y%m%d')}{record_seq:04d}"
                fact_rows.append({
                    "record_id": record_id,
                    "employee_id": employee_id,
                    "employee_name": employee["employee_name"],
                    "department": employee["department"],
                    "position": employee["position"],
                    "level": employee["level"],
                    "hire_date": employee["hire_date"],
                    "course_id": course_id,
                    "course_name": course["course_name"],
                    "course_category": course["course_category"],
                    "course_level": course["course_level"],
                    "trainer_id": trainer.get("trainer_id", ""),
                    "trainer_name": trainer.get("trainer_name", ""),
                    "trainer_department": trainer.get("department", ""),
                    "trainer_expertise": trainer.get("expertise", ""),
                    "training_date": training_date,
                    "attendance": attendance,
                    "completion": completion,
                    "score": score,
                    "certificate_no": certificate_no,
                    "created_at": datetime.combine(training_date, datetime.min.time()),
                })
                
                if attendance == "出勤" and completion == "完成" and random.random() > 0.3:
                    trainer_score = round(random.uniform(3.0, 5.0), 1)
                    content_score = round(random.uniform(3.0, 5.0), 1)
                    environment_score = round(random.uniform(3.0, 5.0), 1)
                    overall_score = round((trainer_score + content_score + environment_score) / 3, 1)
                    suggestions = [
                        "课程内容很实用，希望增加更多实战案例",
                        "讲师讲解清晰，互动环节很好",
                        "培训时长可以适当延长",
                        "希望提供更多学习资料",
                        "整体体验良好，没有建议",
                        "场地设施有待改善",
                        "课程节奏稍快，需要更多时间消化",
                    ]
                    suggestion = random.choice(suggestions) if random.random() > 0.5 else ""
                    
                    eval_rows.append({
                        "evaluation_id": f"EVAL{eval_seq:06d}",
                        "record_id": record_id,
                        "employee_id": employee_id,
                        "course_id": course_id,
                        "trainer_id": trainer.get("trainer_id", ""),
                        "trainer_score": trainer_score,
                        "content_score": content_score,
                        "environment_score": environment_score,
                        "overall_score": overall_score,
                        "suggestion": suggestion,
                        "evaluated_at": datetime.combine(training_date, datetime.min.time()),
                    })
                    eval_seq += 1
                
                record_seq += 1

    inserted = s.sql.insert_rows("training_record", fact_rows)
    output.print(f"OK 培训记录表插入 {inserted} 行")

    if eval_rows:
        inserted_eval = s.sql.insert_rows("training_evaluation", eval_rows)
        output.print(f"OK 培训评估表插入 {inserted_eval} 行")
    else:
        output.print("OK 培训评估表插入 0 行")

    summary = {
        "ok": True,
        "space_id": space_id,
        "employees": len(employees),
        "courses": len(courses),
        "trainers": len(trainers),
        "fact_inserted": inserted,
        "eval_inserted": len(eval_rows),
    }
    output.success("灌数完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))