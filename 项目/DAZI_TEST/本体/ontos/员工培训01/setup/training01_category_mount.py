"""员工培训01 — 平台分类 + 本体域成员挂载

init → seed → 发布全部函数 → **本脚本**
规划对照：plans/员工培训01本体规划方案.md 附录 B

域 code 与快速启动 §1 一致（training01）；function_id 前缀同为 training01.fn.*
"""

import json

SPACE_ID = "space__onto_engine_test"
DOMAIN_CODE = "training01"
DOMAIN_NAME = "员工培训01"

CATEGORY_REGISTRY = {
    "table": {
        "维度表": ["dim_employee", "dim_training_category", "dim_course", "dim_org"],
        "事实表": ["fact_training_record", "fact_training_plan"],
    },
    "cube": {
        "主体型": ["EmployeeCube", "CourseCube"],
        "流程型": ["TrainingRecordCube", "TrainingPlanCube"],
        "对比型": ["OrgTrainingCube", "ComplianceCube"],
    },
    "object": {
        "主数据": ["Employee", "Course", "Org"],
        "参考": ["TrainingCategory"],
        "事务": ["TrainingRecord", "TrainingPlan"],
        "分析": ["TrainingAnalysis", "ComplianceAnalysis"],
    },
    "relation": {
        "时间关联": [
            ("fact_training_record", "dim_date"),
            ("fact_training_plan", "dim_date"),
        ],
        "主数据关联": [
            ("fact_training_record", "dim_employee"),
            ("fact_training_record", "dim_course"),
            ("fact_training_record", "dim_training_category"),
            ("fact_training_record", "dim_org"),
            ("fact_training_plan", "dim_org"),
            ("fact_training_plan", "dim_training_category"),
            ("fact_training_plan", "dim_course"),
            ("dim_employee", "dim_org"),
            ("dim_course", "dim_training_category"),
        ],
        "层级自关联": [("dim_training_category", "dim_training_category")],
    },
    "link": {
        "归属关系": [
            "employee_belongs_org",
            "record_for_employee",
            "record_for_course",
            "record_for_org",
            "course_in_category",
            "plan_for_org",
            "plan_for_category",
        ],
        "层级关系": ["category_has_parent", "org_has_parent"],
        "分析归因": ["analysis_by_org", "analysis_by_category", "compliance_for_course"],
    },
    "function": {
        "总览分析": ["training01.fn.get_summary", "training01.fn.compliance_status"],
        "结构分析": ["training01.fn.category_breakdown", "training01.fn.top_courses"],
        "预实分析": ["training01.fn.plan_vs_actual"],
        "组织分析": ["training01.fn.org_breakdown", "training01.fn.coverage_analysis"],
    },
}


def _flatten_for_domain(reg):
    kind_map = {"object": "object_type", "link": "link_type"}
    members = {}
    for kind, cats in reg.items():
        if kind == "relation":
            continue
        dk = kind_map.get(kind, kind)
        keys = []
        for items in cats.values():
            for item in items:
                if isinstance(item, tuple):
                    continue
                keys.append(item)
        if keys:
            members[dk] = keys
    return members


def main():
    s = space.get(SPACE_ID)
    output.print("=== 员工培训01 — 平台分类 + 本体域成员 ===")
    output.print(f"空间: {SPACE_ID} · 域: {DOMAIN_CODE}")

    cat_counts = s.categories.apply_registry(CATEGORY_REGISTRY, skip_missing=True)
    for kind, cnt in cat_counts.items():
        if cnt:
            output.print(f"OK 分类[{kind}] 挂载 {cnt} 项")

    domain_summary = s.domain.apply_registry(
        {
            "code": DOMAIN_CODE,
            "name": DOMAIN_NAME,
            "members": _flatten_for_domain(CATEGORY_REGISTRY),
        },
        strict=False,
    )
    output.print(
        f"OK 本体域成员 kinds: {json.dumps(domain_summary.get('kinds', {}), ensure_ascii=True, default=str)}"
    )

    summary = {
        "ok": True,
        "space_id": SPACE_ID,
        "domain_code": DOMAIN_CODE,
        "category_mounts": cat_counts,
        "domain_mounts": domain_summary.get("kinds", {}),
    }
    output.success("平台分类与本体域成员挂载完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))
