"""停机原因结构分析 equip_ops.fn.downtime_breakdown

参数：start_date, end_date, reason_level=2, plant_id（可选）
JOIN dim_downtime_reason，返回 reason_code, reason_name, reason_category,
is_planned, downtime_hours, event_count, share_pct

发布：
  dazi onto script publish 项目/DAZI_TEST/本体/ontos/设备运营/functions/equip_ops_fn_downtime_breakdown.py \
    --space space_cate_test01 --register-function-id equip_ops.fn.downtime_breakdown
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {
        "start_date": "2025-01-01",
        "end_date": "2026-06-30",
        "reason_level": 2,
    },
    "object_type_code": "EquipmentAnalysis",
}


def _build_where(start_date, end_date, plant_id=None):
    clauses = []
    if start_date and end_date:
        clauses.append(
            f"e.start_time >= '{start_date} 00:00:00' AND e.start_time <= '{end_date} 23:59:59'"
        )
    if plant_id:
        clauses.append(f"e.plant_id = '{plant_id}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    reason_level = int(params.get("reason_level", 2) or 2)
    plant_id = params.get("plant_id") or None
    where_clause = _build_where(start_date, end_date, plant_id)

    if reason_level <= 1:
        group_cols = "dr.reason_category"
        select_cols = """
            dr.reason_category AS reason_code,
            dr.reason_category AS reason_name,
            dr.reason_category AS reason_category,
            max(dr.is_planned) AS is_planned
        """
    else:
        group_cols = "dr.reason_code, dr.reason_name, dr.reason_category, dr.is_planned"
        select_cols = """
            dr.reason_code AS reason_code,
            dr.reason_name AS reason_name,
            dr.reason_category AS reason_category,
            dr.is_planned AS is_planned
        """

    sql = f"""
    SELECT
        {select_cols},
        sum(e.duration_min) AS downtime_min,
        count() AS event_count
    FROM fact_downtime_event AS e
    INNER JOIN dim_downtime_reason AS dr ON e.reason_id = dr.reason_id
    {where_clause}
    GROUP BY {group_cols}
    ORDER BY downtime_min DESC
    """

    result = p.sql.query(sql)
    if not result:
        return p.function_result(
            columns=[
                "reason_code", "reason_name", "reason_category",
                "is_planned", "downtime_hours", "event_count", "share_pct",
            ],
            data=[],
            row_count=0,
        )

    total_min = sum(float(r.get("downtime_min") or 0) for r in result)
    data = []
    for row in result:
        downtime_min = float(row.get("downtime_min") or 0)
        share_pct = downtime_min / total_min if total_min > 0 else 0.0
        data.append({
            "reason_code": str(row.get("reason_code") or ""),
            "reason_name": str(row.get("reason_name") or ""),
            "reason_category": str(row.get("reason_category") or ""),
            "is_planned": int(row.get("is_planned") or 0),
            "downtime_hours": round(downtime_min / 60.0, 2),
            "event_count": int(row.get("event_count") or 0),
            "share_pct": round(share_pct, 4),
        })

    return p.function_result(
        columns=[
            "reason_code", "reason_name", "reason_category",
            "is_planned", "downtime_hours", "event_count", "share_pct",
        ],
        data=data,
        row_count=len(data),
    )


def main():
    s = space.get(ctx.space_id or "")
    _Ports = type(
        "_Ports",
        (),
        {
            "get_params": lambda self: dict(ctx.params or {}),
            "function_result": lambda self, **kw: onto.function_result(**kw),
        },
    )
    p = _Ports()
    p.sql = s.sql
    return _ontology_fn_body(p)
