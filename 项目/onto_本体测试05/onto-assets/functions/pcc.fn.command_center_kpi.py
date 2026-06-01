# 本体函数脚本（从服务端拉取）
# function_id: pcc.fn.command_center_kpi
# script_id: 42ddf99c-00a4-4929-833f-cfc6af636378
# space_id: space__0519

"""DRAP 生产指挥中心 KPI 本体函数"""

def main():
    from datetime import date
    stat_date = str((ctx.params or {}).get("stat_date") or "").strip() or str(date.today())
    s = space.get(ctx.space_id or "space__0519")
    sql = f"""
        SELECT kpi_label AS label, kpi_value AS value, unit
        FROM pcc_kpi_daily
        WHERE stat_date = toDate('{stat_date}')
        ORDER BY kpi_code
    """
    raw = s.sql.query(sql)
    data = [dict(r) for r in (raw or [])]
    return onto.function_result(
        columns=["label", "value", "unit"],
        data=data,
        row_count=len(data),
    )