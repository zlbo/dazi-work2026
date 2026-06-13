"""员工培训01 灌数 — space__onto_engine_test

前置：training01_ontology_init.py；引擎测试 seed 已灌 dim_org。
幂等：dim_employee 已有数据则跳过。
"""

import json
from datetime import date, datetime

SPACE_ID = "space__onto_engine_test"
_SEED_DT = datetime(2025, 1, 1, 0, 0, 0)
_PLAN_VERSION = "2025年度培训计划"
_PLAN_ID = "TRNPLAN2025"

_PROJECT_ORGS = ["ORG_P1", "ORG_P2", "ORG_P3", "ORG_P4", "ORG_P5", "ORG_P6"]
_JOB_TITLES = ["施工员", "安全员", "质检员", "资料员", "项目经理", "技术员"]
_INSTRUCTORS = ["张老师", "李老师", "王老师", "赵老师"]


def _count(s, table):
    try:
        row = s.sql.query("SELECT count() AS n FROM " + table)
        return int((row or [{}])[0].get("n") or 0)
    except Exception:
        return 0


def _month_date_key(year, month):
    return year * 10000 + month * 100 + 1


def main():
    s = space.get(SPACE_ID)
    output.print("=== 员工培训01 灌数 ===")

    if _count(s, "dim_employee") > 0:
        output.print("dim_employee 已有数据，跳过灌数")
        output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "skipped": True}, ensure_ascii=True))
        return

    org_rows = s.sql.query(
        "SELECT org_id, org_name FROM dim_org WHERE org_id IN ("
        + ",".join(f"'{o}'" for o in _PROJECT_ORGS)
        + ") ORDER BY org_id"
    ) or []
    if not org_rows:
        output.print("WARN dim_org 项目部为空，请先运行引擎测试 seed")
        return

    org_map = {r["org_id"]: r.get("org_name", "") for r in org_rows}

    # 1. dim_training_category
    output.print("\n[1/5] 灌入 dim_training_category...")
    categories = [
        {"category_id": "CAT_SAF", "category_code": "SAF", "category_name": "安全培训",
         "category_type": "安全", "parent_category_id": "", "category_level": 1, "is_mandatory": 1},
        {"category_id": "CAT_SAF_HIGH", "category_code": "SAF-HIGH", "category_name": "高处作业",
         "category_type": "安全", "parent_category_id": "CAT_SAF", "category_level": 2, "is_mandatory": 1},
        {"category_id": "CAT_SAF_FIRE", "category_code": "SAF-FIRE", "category_name": "消防安全",
         "category_type": "安全", "parent_category_id": "CAT_SAF", "category_level": 2, "is_mandatory": 1},
        {"category_id": "CAT_SKL", "category_code": "SKL", "category_name": "技能认证",
         "category_type": "技能", "parent_category_id": "", "category_level": 1, "is_mandatory": 0},
        {"category_id": "CAT_SKL_PROJ", "category_code": "SKL-PROJ", "category_name": "项目管理",
         "category_type": "技能", "parent_category_id": "CAT_SKL", "category_level": 2, "is_mandatory": 0},
        {"category_id": "CAT_MGT", "category_code": "MGT", "category_name": "管理提升",
         "category_type": "管理", "parent_category_id": "", "category_level": 1, "is_mandatory": 0},
        {"category_id": "CAT_CMP", "category_code": "CMP", "category_name": "合规培训",
         "category_type": "合规", "parent_category_id": "", "category_level": 1, "is_mandatory": 1},
        {"category_id": "CAT_CMP_LAW", "category_code": "CMP-LAW", "category_name": "劳动法合规",
         "category_type": "合规", "parent_category_id": "CAT_CMP", "category_level": 2, "is_mandatory": 1},
    ]
    cat_rows = [{**c, "status": "启用", "created_at": _SEED_DT} for c in categories]
    s.sql.insert_rows("dim_training_category", cat_rows)
    cat_by_id = {c["category_id"]: c for c in categories}

    # 2. dim_course
    output.print("\n[2/5] 灌入 dim_course...")
    course_defs = [
        ("CRS001", "新员工三级安全教育", "CAT_SAF", "线下", 8.0, 1, 12),
        ("CRS002", "高处作业安全专项", "CAT_SAF_HIGH", "线下", 4.0, 1, 12),
        ("CRS003", "消防安全与应急演练", "CAT_SAF_FIRE", "混合", 3.0, 1, 12),
        ("CRS004", "脚手架搭设规范", "CAT_SAF_HIGH", "线下", 6.0, 1, 24),
        ("CRS005", "BIM 施工应用", "CAT_SKL", "线上", 16.0, 0, 0),
        ("CRS006", "项目管理 PMP 基础", "CAT_SKL_PROJ", "线下", 24.0, 0, 36),
        ("CRS007", "工程质量验收标准", "CAT_SKL", "线下", 8.0, 0, 0),
        ("CRS008", "中层管理者领导力", "CAT_MGT", "线下", 16.0, 0, 0),
        ("CRS009", "沟通与团队协作", "CAT_MGT", "线上", 4.0, 0, 0),
        ("CRS010", "建筑法规与合规", "CAT_CMP", "线下", 8.0, 1, 24),
        ("CRS011", "劳动合同与用工合规", "CAT_CMP_LAW", "线上", 2.0, 1, 12),
        ("CRS012", "数据安全与隐私保护", "CAT_CMP", "线上", 2.0, 1, 12),
        ("CRS013", "特种作业操作规范", "CAT_SAF", "线下", 8.0, 1, 24),
        ("CRS014", "绿色施工与环保", "CAT_SKL", "混合", 4.0, 0, 0),
        ("CRS015", "成本管控实务", "CAT_MGT", "线下", 8.0, 0, 0),
        ("CRS016", "有限空间作业安全", "CAT_SAF_HIGH", "线下", 4.0, 1, 12),
        ("CRS017", "焊接作业安全", "CAT_SAF", "线下", 6.0, 1, 12),
        ("CRS018", "档案管理规范", "CAT_CMP", "线上", 2.0, 0, 0),
        ("CRS019", "Excel 数据分析", "CAT_SKL", "线上", 8.0, 0, 0),
        ("CRS020", "现场急救知识", "CAT_SAF_FIRE", "线下", 3.0, 1, 24),
    ]
    courses = []
    for idx, (code, name, cat_id, mode, hours, mandatory, valid_m) in enumerate(course_defs, 1):
        cat = cat_by_id[cat_id]
        courses.append({
            "course_id": f"CRS_{idx:03d}",
            "course_code": code,
            "course_name": name,
            "category_id": cat_id,
            "category_name": cat["category_name"],
            "category_type": cat["category_type"],
            "delivery_mode": mode,
            "standard_hours": hours,
            "is_mandatory": mandatory,
            "cert_valid_months": valid_m,
            "instructor": _INSTRUCTORS[idx % len(_INSTRUCTORS)],
            "status": "启用",
            "created_at": _SEED_DT,
        })
    s.sql.insert_rows("dim_course", courses)
    course_by_id = {c["course_id"]: c for c in courses}

    # 3. dim_employee
    output.print("\n[3/5] 灌入 dim_employee...")
    employees = []
    emp_no = 0
    for org_id in _PROJECT_ORGS:
        org_name = org_map.get(org_id, "")
        for i in range(1, 21):
            emp_no += 1
            employees.append({
                "employee_id": f"EMP_{emp_no:04d}",
                "employee_code": f"E{emp_no:05d}",
                "employee_name": f"员工{emp_no:03d}",
                "org_id": org_id,
                "org_name": org_name,
                "job_title": _JOB_TITLES[(emp_no + i) % len(_JOB_TITLES)],
                "job_level": "P" + str((emp_no % 5) + 1),
                "hire_date": date(2020 + (emp_no % 4), 1 + (emp_no % 12), 1 + (emp_no % 28)),
                "employment_status": "在职",
                "status": "启用",
                "created_at": _SEED_DT,
            })
    s.sql.insert_rows("dim_employee", employees)

    # 4. fact_training_record
    output.print("\n[4/5] 灌入 fact_training_record...")
    record_rows = []
    rec_no = 0
    mandatory_courses = [c for c in courses if c["is_mandatory"] == 1]
    elective_sample = [c for c in courses if c["is_mandatory"] == 0][:6]

    for emp in employees:
        assigned = mandatory_courses + elective_sample[: (rec_no % 3) + 2]
        for course in assigned:
            for month in [3, 6, 9, 12]:
                if (rec_no + month) % 5 == 0:
                    continue
                rec_no += 1
                dk = _month_date_key(2025, month)
                completion = "已完成" if rec_no % 8 != 0 else "未通过"
                if rec_no % 11 == 0:
                    completion = "缺勤"
                pass_flag = 1 if completion == "已完成" and rec_no % 13 != 0 else 0
                hours = float(course["standard_hours"]) if completion == "已完成" else 0.0
                cost = round(hours * 120 + (rec_no % 7) * 10, 2)
                score = 0.0 if completion != "已完成" else round(70 + (rec_no % 28), 1)
                record_rows.append({
                    "record_id": f"TRN{rec_no:07d}",
                    "session_id": f"SES_{course['course_id']}_{month:02d}",
                    "date_key": dk,
                    "training_date": date(2025, month, 10 + (rec_no % 18)),
                    "fiscal_year": 2025,
                    "fiscal_period": month,
                    "employee_id": emp["employee_id"],
                    "employee_name": emp["employee_name"],
                    "org_id": emp["org_id"],
                    "org_name": emp["org_name"],
                    "course_id": course["course_id"],
                    "course_name": course["course_name"],
                    "category_id": course["category_id"],
                    "category_name": course["category_name"],
                    "category_type": course["category_type"],
                    "enroll_status": "已报名",
                    "completion_status": completion,
                    "attendance_status": "出勤" if completion != "缺勤" else "缺勤",
                    "exam_score": score,
                    "pass_flag": pass_flag,
                    "training_hours": hours,
                    "training_cost": cost if completion == "已完成" else 0.0,
                    "satisfaction_score": round(3.5 + (rec_no % 15) * 0.1, 1) if completion == "已完成" else 0.0,
                    "instructor": course["instructor"],
                    "created_at": _SEED_DT,
                })

    s.sql.insert_rows("fact_training_record", record_rows)
    output.print(f"OK fact_training_record {len(record_rows)} 行")

    # 5. fact_training_plan
    output.print("\n[5/5] 灌入 fact_training_plan...")
    plan_rows = []
    line_no = 0
    main_cats = [c for c in categories if c["category_level"] == 1]
    for org_id in _PROJECT_ORGS:
        org_name = org_map.get(org_id, "")
        for month in range(1, 13):
            dk = _month_date_key(2025, month)
            for cat in main_cats:
                line_no += 1
                headcount = 15 + (line_no % 8)
                hours = headcount * (4 + (line_no % 5))
                plan_rows.append({
                    "plan_id": _PLAN_ID,
                    "line_id": f"TPL{line_no:06d}",
                    "date_key": dk,
                    "fiscal_year": 2025,
                    "fiscal_period": month,
                    "plan_version": _PLAN_VERSION,
                    "org_id": org_id,
                    "org_name": org_name,
                    "category_id": cat["category_id"],
                    "category_name": cat["category_name"],
                    "category_type": cat["category_type"],
                    "course_id": "",
                    "course_name": "",
                    "plan_headcount": headcount,
                    "plan_hours": float(hours),
                    "plan_cost": round(hours * 100, 2),
                    "target_completion_rate": 0.85 + (line_no % 10) * 0.01,
                    "target_pass_rate": 0.88 + (line_no % 8) * 0.01,
                    "status": "已发布",
                    "created_at": _SEED_DT,
                })

    s.sql.insert_rows("fact_training_plan", plan_rows)

    summary = {
        "ok": True,
        "categories": len(cat_rows),
        "courses": len(courses),
        "employees": len(employees),
        "records": len(record_rows),
        "plan_lines": len(plan_rows),
    }
    output.success("员工培训01 灌数完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True))
