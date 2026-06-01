# 本体函数脚本（从服务端拉取）
# function_id: fc02.fn.month_pl_budget_kpi
# script_id: cdfee9fa-47e4-430d-a0c2-2d507731ac2f
# space_id: space__0519

"""FC02 B1：月利润/预算/达成率（由种子写入，文档 201）"""


def main():
    args = dict(ctx.params or {})
    s = space.get(ctx.space_id)

    if args.get("date_key") is not None:
        dk = int(args["date_key"])
        if dk < 19000101 or dk > 20991231:
            output.error("date_key 超出合理范围")
            return None
        ymi = dk // 100
    else:
        ym = str(args.get("year_month") or "").strip()
        parts = ym.split("-")
        if len(parts) == 2 and len(parts[0]) == 4 and len(parts[1]) == 2:
            ymi = int(parts[0]) * 100 + int(parts[1])
        else:
            output.error("需要提供 year_month(YYYY-MM) 或 date_key(YYYYMMDD)")
            return None

    vid_raw = args.get("version_id")
    vid = int(vid_raw) if vid_raw is not None and str(vid_raw).strip() != "" else 1
    if vid < 0 or vid > 255:
        output.error("version_id 无效")
        return None

    ym_str = "{:04d}-{:02d}".format(ymi // 100, ymi % 100)
    y, mo = divmod(ymi, 100)
    date_key_first = y * 10000 + mo * 100 + 1

    sql = """
    SELECT
        '{ym}' AS year_month,
        toUInt8({v}) AS version_id,
        act.s AS actual_total,
        bud.s AS budget_total,
        if(ifNull(bud.s, 0) != 0, act.s / bud.s, NULL) AS achievement_rate
    FROM
        (
            SELECT sum(p.amount) AS s
            FROM v_profit_month_enriched AS p
            WHERE p.year_month = '{ym}'
        ) AS act,
        (
            SELECT sum(b.budget_value) AS s
            FROM fact_budget_month AS b
            WHERE b.date_key = {dk} AND b.version_id = {v}
        ) AS bud
    """.format(ym=ym_str, v=vid, dk=date_key_first).strip()

    rows = s.sql.query(sql)
    if not rows:
        return onto.function_result(columns=[], data=[], row_count=0)
    cols = list(rows[0].keys())
    return onto.function_result(columns=cols, data=rows, row_count=len(rows))
