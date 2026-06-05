"""Panda Construction Profit Trend Function

功能：计算项目利润趋势分析
参数：project_id, start_month, end_month
返回：利润趋势数据

放置位置：项目/onto_潘达工程_项目成本决策/脚本/functions/panda_fn_profit_trend.py
"""


def main(params: dict) -> dict:
    """
    函数入口，params 由平台传入。
    """
    s = space.get(ctx.space_id or "")

    project_id = params.get("project_id", "")
    start_month = params.get("start_month", "")
    end_month = params.get("end_month", "")

    if not project_id or not start_month or not end_month:
        return {
            "ok": False,
            "error": "project_id, start_month, and end_month are required",
            "data": []
        }

    sql = f"""
    SELECT
        project_id,
        project_name,
        report_month,
        output_total_total,
        output_this_year_total,
        cost_total,
        cost_confirmed,
        profit_total,
        profit_confirmed,
        profit_rate_total,
        profit_rate_confirmed,
        receivable_ratio,
        warning_status
    FROM wide_project_monthly
    WHERE project_id = '{project_id}'
        AND report_month >= '{start_month}'
        AND report_month <= '{end_month}'
    ORDER BY report_month ASC
    """

    result = s.sql.query(sql)

    if not result:
        return {
            "ok": True,
            "data": [],
            "message": "No data found for the specified period"
        }

    data = []
    prev_profit = None
    prev_month = None

    for row in result:
        current_profit = float(row.get("profit_total", 0) or 0)
        current_month = str(row.get("report_month", ""))

        mom_change = None
        mom_growth = None
        if prev_profit is not None and prev_profit != 0:
            mom_change = current_profit - prev_profit
            mom_growth = round(mom_change / abs(prev_profit), 4) if prev_profit != 0 else 0

        data.append({
            "project_id": str(row.get("project_id", "")),
            "project_name": str(row.get("project_name", "")),
            "report_month": current_month,
            "output_total": round(float(row.get("output_total_total", 0) or 0), 2),
            "output_this_year": round(float(row.get("output_this_year_total", 0) or 0), 2),
            "cost_total": round(float(row.get("cost_total", 0) or 0), 2),
            "cost_confirmed": round(float(row.get("cost_confirmed", 0) or 0), 2),
            "profit_total": round(current_profit, 2),
            "profit_confirmed": round(float(row.get("profit_confirmed", 0) or 0), 2),
            "profit_rate_total": round(float(row.get("profit_rate_total", 0) or 0), 4),
            "profit_rate_confirmed": round(float(row.get("profit_rate_confirmed", 0) or 0), 4),
            "collection_rate": round(float(row.get("receivable_ratio", 0) or 0) if row.get("receivable_ratio") else 0, 4),
            "mom_change": round(mom_change, 2) if mom_change is not None else None,
            "mom_growth": mom_growth,
            "warning_status": str(row.get("warning_status", "green")),
        })

        prev_profit = current_profit
        prev_month = current_month

    first_profit = float(result[0].get("profit_total", 0) or 0) if result else 0
    last_profit = float(result[-1].get("profit_total", 0) or 0) if result else 0
    period_change = last_profit - first_profit
    period_growth = round(period_change / abs(first_profit), 4) if first_profit != 0 else None

    return {
        "ok": True,
        "data": data,
        "row_count": len(data),
        "summary": {
            "period": f"{start_month} 至 {end_month}",
            "month_count": len(data),
            "first_profit": round(first_profit, 2),
            "last_profit": round(last_profit, 2),
            "period_change": round(period_change, 2),
            "period_growth": period_growth,
            "avg_profit_rate": round(sum(float(d.get("profit_rate_total", 0) or 0) for d in data) / len(data), 4) if data else 0,
            "min_profit_rate": round(min(float(d.get("profit_rate_total", 0) or 0) for d in data), 4) if data else 0,
            "max_profit_rate": round(max(float(d.get("profit_rate_total", 0) or 0) for d in data), 4) if data else 0,
        }
    }
