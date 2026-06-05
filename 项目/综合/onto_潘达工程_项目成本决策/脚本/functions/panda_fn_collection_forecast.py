"""Panda Construction Collection Forecast Function

功能：预测项目回款情况
参数：project_id, report_month
返回：回款预测数据

放置位置：项目/onto_潘达工程_项目成本决策/脚本/functions/panda_fn_collection_forecast.py
"""


def main(params: dict) -> dict:
    """
    函数入口，params 由平台传入。
    """
    s = space.get(ctx.space_id or "")

    project_id = params.get("project_id", "")
    report_month = params.get("report_month", "")

    if not project_id or not report_month:
        return {
            "ok": False,
            "error": "project_id and report_month are required",
            "data": []
        }

    current_sql = f"""
    SELECT
        project_id,
        project_name,
        output_total_confirmed,
        output_total_total,
        output_this_year_confirmed,
        output_this_year_total,
        receivable_amount,
        received_amount,
        receivable_ratio,
        profit_total,
        profit_rate_total,
        contract_amount
    FROM wide_project_monthly
    WHERE project_id = '{project_id}' AND report_month = '{report_month}'
    LIMIT 1
    """

    result = s.sql.query(current_sql)

    if not result:
        return {
            "ok": True,
            "data": [],
            "message": "No data found for the specified project and month"
        }

    row = result[0]
    receivable_amount = float(row.get("receivable_amount", 0) or 0)
    received_amount = float(row.get("received_amount", 0) or 0)
    output_total = float(row.get("output_total_total", 0) or 0)
    output_confirmed = float(row.get("output_total_confirmed", 0) or 0)
    contract_amount = float(row.get("contract_amount", 0) or 0)

    unconfirmed_amount = output_total - output_confirmed
    outstanding_amount = receivable_amount - received_amount
    collection_rate = round(received_amount / receivable_amount, 4) if receivable_amount > 0 else 0

    historical_sql = f"""
    SELECT
        report_month,
        receivable_amount as historical_receivable,
        received_amount as historical_received,
        receivable_ratio as historical_ratio
    FROM wide_project_monthly
    WHERE project_id = '{project_id}' AND report_month < '{report_month}'
    ORDER BY report_month DESC
    LIMIT 6
    """

    historical = s.sql.query(historical_sql)

    avg_monthly_collection = 0
    if historical:
        total_received = sum(float(h.get("historical_received", 0) or 0) for h in historical)
        avg_monthly_collection = total_received / len(historical)

    projected_collection = received_amount + avg_monthly_collection
    projected_outstanding = receivable_amount - projected_collection

    if outstanding_amount > 0 and avg_monthly_collection > 0:
        months_to_clear = round(outstanding_amount / avg_monthly_collection, 1)
    else:
        months_to_clear = 0

    risk_level = "low"
    if collection_rate < 0.5:
        risk_level = "high"
    elif collection_rate < 0.75:
        risk_level = "medium"

    return {
        "ok": True,
        "data": [{
            "project_id": str(row.get("project_id", "")),
            "project_name": str(row.get("project_name", "")),
            "report_month": report_month,
            "output_total": round(output_total, 2),
            "output_confirmed": round(output_confirmed, 2),
            "unconfirmed_amount": round(unconfirmed_amount, 2),
            "receivable_amount": round(receivable_amount, 2),
            "received_amount": round(received_amount, 2),
            "outstanding_amount": round(outstanding_amount, 2),
            "collection_rate": collection_rate,
            "avg_monthly_collection": round(avg_monthly_collection, 2),
            "projected_collection": round(projected_collection, 2),
            "projected_outstanding": round(projected_outstanding, 2),
            "months_to_clear": months_to_clear,
            "risk_level": risk_level,
            "profit_total": round(float(row.get("profit_total", 0) or 0), 2),
            "profit_rate": round(float(row.get("profit_rate_total", 0) or 0), 4),
            "contract_amount": round(contract_amount, 2),
            "completion_rate": round(output_total / contract_amount, 4) if contract_amount > 0 else 0,
        }],
        "row_count": 1
    }
