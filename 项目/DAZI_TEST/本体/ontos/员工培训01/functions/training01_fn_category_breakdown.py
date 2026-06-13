"""training01.fn.category_breakdown — 培训类别结构"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31"},
    "object_type_code": "TrainingCategory",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "2025-01-01")
    end_date = params.get("end_date", "2025-12-31")
    category_type = (params.get("category_type") or "").strip()
    lo = int(start_date.replace("-", "")[:8])
    hi = int(end_date.replace("-", "")[:8])
    type_filter = f" AND r.category_type = '{category_type}'" if category_type else ""

    sql = f"""
        SELECT
            r.category_type, r.category_id, r.category_name,
            count() AS enroll_count,
            countIf(r.completion_status = '已完成') AS complete_count,
            coalesce(sum(r.training_hours), 0) AS total_hours,
            coalesce(sum(r.training_cost), 0) AS total_cost
        FROM fact_training_record r
        WHERE r.date_key >= {lo} AND r.date_key <= {hi} {type_filter}
        GROUP BY r.category_type, r.category_id, r.category_name
        ORDER BY total_hours DESC
    """
    rows = p.sql.query(sql) or []
    total_hours = sum(float(r.get("total_hours") or 0) for r in rows)
    data = [{
        "category_type": r.get("category_type", ""),
        "category_id": r.get("category_id", ""),
        "category_name": r.get("category_name", ""),
        "enroll_count": int(r.get("enroll_count") or 0),
        "complete_count": int(r.get("complete_count") or 0),
        "total_hours": round(float(r.get("total_hours") or 0), 2),
        "total_cost": round(float(r.get("total_cost") or 0), 2),
        "share_pct": round(float(r.get("total_hours") or 0) / total_hours, 4) if total_hours > 0 else 0,
    } for r in rows]
    return p.function_result(
        columns=["category_type", "category_id", "category_name", "enroll_count", "complete_count",
                 "total_hours", "total_cost", "share_pct"],
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
