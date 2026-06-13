"""training01.fn.compliance_status — 必修/合规完成情况"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"fiscal_year": 2025},
    "object_type_code": "ComplianceAnalysis",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    fiscal_year = int(params.get("fiscal_year") or 2025)
    org_id = (params.get("org_id") or "").strip()
    org_cond = f" AND e.org_id = '{org_id}'" if org_id else ""

    sql = f"""
        SELECT
            e.org_name,
            c.course_id,
            c.course_name,
            c.category_type,
            count(DISTINCT e.employee_id) AS mandatory_count,
            countIf(r.pass_flag = 1 AND r.completion_status = '已完成') AS compliant_count,
            countIf(r.completion_status IN ('未通过', '缺勤') OR r.record_id = '') AS overdue_count
        FROM dim_employee e
        CROSS JOIN dim_course c
        LEFT JOIN fact_training_record r ON r.employee_id = e.employee_id
            AND r.course_id = c.course_id
            AND r.fiscal_year = {fiscal_year}
        WHERE c.is_mandatory = 1
          AND e.employment_status = '在职'
          {org_cond}
        GROUP BY e.org_name, c.course_id, c.course_name, c.category_type
        ORDER BY e.org_name, c.course_name
    """
    rows = p.sql.query(sql) or []
    data = []
    for r in rows:
        mandatory = int(r.get("mandatory_count") or 0)
        compliant = int(r.get("compliant_count") or 0)
        data.append({
            "org_name": r.get("org_name", ""),
            "course_id": r.get("course_id", ""),
            "course_name": r.get("course_name", ""),
            "category_type": r.get("category_type", ""),
            "mandatory_count": mandatory,
            "compliant_count": compliant,
            "compliance_rate": round(compliant / mandatory, 4) if mandatory > 0 else 0,
            "overdue_count": max(mandatory - compliant, 0),
        })
    return p.function_result(
        columns=["org_name", "course_id", "course_name", "category_type",
                 "mandatory_count", "compliant_count", "compliance_rate", "overdue_count"],
        data=data,
        row_count=len(data),
    )


def main():
    s = space.get(ctx.space_id or "")
    _Ports = type("_Ports", (), {
        "get_params": lambda self: dict(ctx.params or {}),
        "function_result": lambda self, **kw: onto.function_result(**kw),
    })
    p = _Ports()
    p.sql = s.sql
    return _ontology_fn_body(p)
