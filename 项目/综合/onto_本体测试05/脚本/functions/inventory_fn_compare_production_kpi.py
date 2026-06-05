"""产量与出库对照 inventory.fn.compare_production_kpi

参数：start_date, end_date
返回：stat_date, output_qty, outbound_qty, outbound_to_output_ratio

发布：
  dazi-onto script publish 项目/onto_本体测试05/脚本/functions/inventory_fn_compare_production_kpi.py \\
    --space space__0519 --register-function-id inventory.fn.compare_production_kpi
"""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")

    date_filter_kpi = ""
    date_filter_txn = ""
    if start_date and end_date:
        date_filter_kpi = f"AND stat_date >= '{start_date}' AND stat_date <= '{end_date}'"
        date_filter_txn = f"AND transaction_date >= '{start_date}' AND transaction_date <= '{end_date}'"

    sql = f"""
    WITH production AS (
        SELECT
            stat_date,
            sumIf(kpi_value, kpi_code = 'output_today') AS output_qty
        FROM pcc_kpi_daily
        WHERE 1 = 1 {date_filter_kpi}
        GROUP BY stat_date
    ),
    outbound AS (
        SELECT
            transaction_date AS stat_date,
            sumIf(abs(quantity), transaction_type = 'OUT') AS outbound_qty
        FROM inventory_transaction
        WHERE 1 = 1 {date_filter_txn}
        GROUP BY transaction_date
    )
    SELECT
        coalesce(p.stat_date, o.stat_date) AS stat_date,
        coalesce(p.output_qty, 0) AS output_qty,
        coalesce(o.outbound_qty, 0) AS outbound_qty,
        if(coalesce(p.output_qty, 0) > 0, coalesce(o.outbound_qty, 0) / p.output_qty, 0) AS outbound_to_output_ratio
    FROM production AS p
    FULL OUTER JOIN outbound AS o ON p.stat_date = o.stat_date
    ORDER BY stat_date
    """

    try:
        result = p.sql.query(sql)
    except Exception:
        result = []

    data = []
    for row in result:
        output_qty = float(row.get("output_qty", 0) or 0)
        outbound_qty = float(row.get("outbound_qty", 0) or 0)
        ratio = float(row.get("outbound_to_output_ratio", 0) or 0)
        data.append({
            "stat_date": str(row.get("stat_date", "")),
            "output_qty": round(output_qty, 2),
            "outbound_qty": round(outbound_qty, 2),
            "outbound_to_output_ratio": round(ratio, 4),
        })

    return p.function_result(
        columns=["stat_date", "output_qty", "outbound_qty", "outbound_to_output_ratio"],
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
