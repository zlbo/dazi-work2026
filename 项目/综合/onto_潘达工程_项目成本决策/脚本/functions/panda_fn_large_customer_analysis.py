"""Panda Construction Large Customer Analysis Function

功能：大客户项目分析
参数：report_month
返回：大客户项目经营分析

放置位置：项目/onto_潘达工程_项目成本决策/脚本/functions/panda_fn_large_customer_analysis.py
"""


def main(params: dict) -> dict:
    """
    函数入口，params 由平台传入。
    """
    s = space.get(ctx.space_id or "")

    report_month = params.get("report_month", "")

    if not report_month:
        return {
            "ok": False,
            "error": "report_month is required",
            "data": []
        }

    sql = f"""
    SELECT
        project_id,
        project_name,
        owner_name,
        region,
        operation_mode,
        contract_amount,
        output_total_total,
        output_this_year_total,
        cost_total,
        profit_total,
        profit_rate_total,
        receivable_amount,
        received_amount,
        receivable_ratio,
        warning_status
    FROM wide_project_monthly
    WHERE report_month = '{report_month}' AND is_large_customer = 1
    ORDER BY contract_amount DESC
    """

    result = s.sql.query(sql)

    if not result:
        return {
            "ok": True,
            "data": [],
            "message": "No large customer projects found"
        }

    data = []
    total_contract = 0
    total_output = 0
    total_cost = 0
    total_profit = 0
    total_receivable = 0
    total_received = 0

    for row in result:
        contract_amount = float(row.get("contract_amount", 0) or 0)
        output_total = float(row.get("output_total_total", 0) or 0)
        cost_total = float(row.get("cost_total", 0) or 0)
        profit_total_val = float(row.get("profit_total", 0) or 0)
        receivable_amount = float(row.get("receivable_amount", 0) or 0)
        received_amount = float(row.get("received_amount", 0) or 0)
        receivable_ratio = float(row.get("receivable_ratio", 0) or 0) if row.get("receivable_ratio") else 0

        total_contract += contract_amount
        total_output += output_total
        total_cost += cost_total
        total_profit += profit_total_val
        total_receivable += receivable_amount
        total_received += received_amount

        completion_rate = round(output_total / contract_amount, 4) if contract_amount > 0 else 0

        data.append({
            "project_id": str(row.get("project_id", "")),
            "project_name": str(row.get("project_name", "")),
            "owner_name": str(row.get("owner_name", "")),
            "region": str(row.get("region", "")),
            "operation_mode": str(row.get("operation_mode", "")),
            "contract_amount": round(contract_amount, 2),
            "completion_rate": completion_rate,
            "output_total": round(output_total, 2),
            "output_this_year": round(float(row.get("output_this_year_total", 0) or 0), 2),
            "cost_total": round(cost_total, 2),
            "profit_total": round(profit_total_val, 2),
            "profit_rate": round(float(row.get("profit_rate_total", 0) or 0), 4),
            "receivable_amount": round(receivable_amount, 2),
            "received_amount": round(received_amount, 2),
            "collection_rate": round(receivable_ratio, 4),
            "warning_status": str(row.get("warning_status", "green")),
        })

    total_collection_rate = round(total_received / total_receivable, 4) if total_receivable > 0 else 0
    total_profit_rate = round(total_profit / total_output, 4) if total_output > 0 else 0

    owner_summary = {}
    for row in result:
        owner = row.get("owner_name", "")
        if owner not in owner_summary:
            owner_summary[owner] = {
                "owner_name": owner,
                "project_count": 0,
                "total_contract": 0,
                "total_output": 0,
                "total_profit": 0,
                "total_receivable": 0,
                "total_received": 0,
            }
        owner_summary[owner]["project_count"] += 1
        owner_summary[owner]["total_contract"] += float(row.get("contract_amount", 0) or 0)
        owner_summary[owner]["total_output"] += float(row.get("output_total_total", 0) or 0)
        owner_summary[owner]["total_profit"] += float(row.get("profit_total", 0) or 0)
        owner_summary[owner]["total_receivable"] += float(row.get("receivable_amount", 0) or 0)
        owner_summary[owner]["total_received"] += float(row.get("received_amount", 0) or 0)

    owner_data = []
    for owner, info in owner_summary.items():
        owner_data.append({
            "owner_name": owner,
            "project_count": info["project_count"],
            "total_contract": round(info["total_contract"], 2),
            "total_output": round(info["total_output"], 2),
            "total_profit": round(info["total_profit"], 2),
            "avg_profit_rate": round(info["total_profit"] / info["total_output"], 4) if info["total_output"] > 0 else 0,
            "total_receivable": round(info["total_receivable"], 2),
            "total_received": round(info["total_received"], 2),
            "avg_collection_rate": round(info["total_received"] / info["total_receivable"], 4) if info["total_receivable"] > 0 else 0,
        })

    owner_data.sort(key=lambda x: x["total_contract"], reverse=True)

    return {
        "ok": True,
        "data": data,
        "row_count": len(data),
        "summary": {
            "report_month": report_month,
            "large_customer_count": len(data),
            "total_contract": round(total_contract, 2),
            "total_output": round(total_output, 2),
            "total_cost": round(total_cost, 2),
            "total_profit": round(total_profit, 2),
            "total_profit_rate": total_profit_rate,
            "total_receivable": round(total_receivable, 2),
            "total_received": round(total_received, 2),
            "total_collection_rate": total_collection_rate,
            "owner_summary": owner_data,
        }
    }
