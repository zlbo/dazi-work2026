# 本体函数脚本（从服务端拉取）
# function_id: panda_cost.fn.indicator_status
# script_id: cf164d7b-3d62-4be7-8f69-24776240b094
# space_id: space__panda_construction

"""核心指标达成与预警 panda_cost.fn.indicator_status（V3）

参数：report_period, project_id（可选）
返回：project_id, project_name, indicator_code, indicator_name, indicator_value,
      target_value, variance_value, variance_ratio, warning_level, is_warning, report_period

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/本体规划03/functions/panda_cost_v3_fn_indicator_status.py \
    --space space__panda_construction --register-function-id panda_cost.fn.indicator_status
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"report_period": "2025-06"},
    "object_type_code": "ProjectIndicator",
}



import math


def _safe_float(v, default=0.0):
    try:
        x = float(v if v is not None else default)
        return x if math.isfinite(x) else default
    except (TypeError, ValueError):
        return default


def _safe_round(v, ndigits=4, default=0.0):
    return round(_safe_float(v, default), ndigits)

def _build_where(report_period, project_id=None):
    clauses = []
    if report_period:
        clauses.append(f"i.report_period = '{report_period}'")
    if project_id:
        clauses.append(f"i.project_id = '{project_id}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    report_period = params.get("report_period", "")
    project_id = params.get("project_id") or None
    where_clause = _build_where(report_period, project_id)

    sql = f"""
    SELECT
        i.project_id,
        any(dp.project_name) AS project_name,
        i.indicator_code,
        any(i.indicator_name) AS indicator_name,
        avg(i.indicator_value) AS indicator_value,
        avg(i.target_value) AS target_value,
        any(i.warning_level) AS warning_level
    FROM fact_project_indicator i
    JOIN dim_project dp ON i.project_id = dp.project_id
    {where_clause}
    GROUP BY i.project_id, i.indicator_code
    ORDER BY i.project_id, i.indicator_code
    """

    rows = p.sql.query(sql)
    data = []
    for row in rows:
        indicator_value = _safe_float(row.get("indicator_value"))
        target_value = _safe_float(row.get("target_value"))
        variance_value = indicator_value - target_value
        variance_ratio = variance_value / target_value if target_value != 0 else 0.0
        is_warning = 1 if abs(variance_ratio) > 0.10 else 0
        data.append({
            "project_id": str(row.get("project_id") or ""),
            "project_name": str(row.get("project_name") or ""),
            "indicator_code": str(row.get("indicator_code") or ""),
            "indicator_name": str(row.get("indicator_name") or ""),
            "indicator_value": _safe_round(indicator_value, 4),
            "target_value": _safe_round(target_value, 4),
            "variance_value": _safe_round(variance_value, 4),
            "variance_ratio": _safe_round(variance_ratio, 4),
            "warning_level": str(row.get("warning_level") or ""),
            "is_warning": is_warning,
            "report_period": report_period,
        })

    return p.function_result(
        columns=["project_id", "project_name", "indicator_code", "indicator_name",
                 "indicator_value", "target_value", "variance_value", "variance_ratio",
                 "warning_level", "is_warning", "report_period"],
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
