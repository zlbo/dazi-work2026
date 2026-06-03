"""Panda Construction Project Comparison Function

功能：多项目对比分析
参数：project_ids, report_month, metrics（可选）
返回：项目对比数据

放置位置：项目/onto_潘达工程_项目成本决策/脚本/functions/panda_fn_project_comparison.py
"""


def main(params: dict) -> dict:
    """
    函数入口，params 由平台传入。
    """
    s = space.get(ctx.space_id or "")

    project_ids = params.get("project_ids", [])
    report_month = params.get("report_month", "")
    metrics = params.get("metrics", ["profit_rate", "collection_rate"])

    if not report_month:
        return {
            "ok": False,
            "error": "report_month is required",
            "data": []
        }

    if not project_ids:
        sql = f"""
        SELECT
            project_id,
            project_name,
            region,
            operation_mode,
            is_large_customer,
            contract_amount,
            output_total_total,
            cost_total,
            profit_total,
            profit_rate_total,
            receivable_amount,
            received_amount,
            receivable_ratio,
            warning_status
        FROM wide_project_monthly
        WHERE report_month = '{report_month}'
        ORDER BY profit_rate_total ASC
        LIMIT 20
        """
    else:
        ids_str = "','".join(project_ids)
        sql = f"""
        SELECT
            project_id,
            project_name,
            region,
            operation_mode,
            is_large_customer,
            contract_amount,
            output_total_total,
            cost_total,
            profit_total,
            profit_rate_total,
            receivable_amount,
            received_amount,
            receivable_ratio,
            warning_status
        FROM wide_project_monthly
        WHERE report_month = '{report_month}'
            AND project_id IN ('{ids_str}')
        ORDER BY profit_rate_total ASC
        """

    result = s.sql.query(sql)

    if not result:
        return {
            "ok": True,
            "data": [],
            "message": "No data found"
        }

    data = []
    for row in result:
        receivable_ratio_val = float(row.get("receivable_ratio", 0) or 0) if row.get("receivable_ratio") else 0

        data.append({
            "project_id": str(row.get("project_id", "")),
            "project_name": str(row.get("project_name", "")),
            "region": str(row.get("region", "")),
            "operation_mode": str(row.get("operation_mode", "")),
            "is_large_customer": "是" if row.get("is_large_customer") else "否",
            "contract_amount": round(float(row.get("contract_amount", 0) or 0), 2),
            "output_total": round(float(row.get("output_total_total", 0) or 0), 2),
            "cost_total": round(float(row.get("cost_total", 0) or 0), 2),
            "profit_total": round(float(row.get("profit_total", 0) or 0), 2),
            "profit_rate": round(float(row.get("profit_rate_total", 0) or 0), 4),
            "receivable_amount": round(float(row.get("receivable_amount", 0) or 0), 2),
            "received_amount": round(float(row.get("received_amount", 0) or 0), 2),
            "collection_rate": round(receivable_ratio_val, 4),
            "warning_status": str(row.get("warning_status", "green")),
        })

    avg_profit_rate = sum(float(d.get("profit_rate", 0) or 0) for d in data) / len(data) if data else 0
    avg_collection_rate = sum(float(d.get("collection_rate", 0) or 0) for d in data) / len(data) if data else 0

    ranked_data = []
    for i, d in enumerate(data):
        profit_rank = sum(1 for x in data if float(x.get("profit_rate", 0) or 0) > float(d.get("profit_rate", 0) or 0) if float(x.get("profit_rate", 0) or 0) != 0 else (x.get("profit_rate", 0) == 0 and d.get("profit_rate", 0) != 0)) + 1
        collection_rank = sum(1 for x in data if float(x.get("collection_rate", 0) or 0) > float(d.get("collection_rate", 0) or 0) if float(x.get("collection_rate", 0) or 0) != 0 else (x.get("collection_rate", 0) == 0 and d.get("collection_rate", 0) != 0)) + 1

        d["profit_rank"] = profit_rank
        d["collection_rank"] = collection_rank
        ranked_data.append(d)

    return {
        "ok": True,
        "data": ranked_data,
        "row_count": len(data),
        "summary": {
            "report_month": report_month,
            "project_count": len(data),
            "avg_profit_rate": round(avg_profit_rate, 4),
            "avg_collection_rate": round(avg_collection_rate, 4),
            "best_profit_project": min(data, key=lambda x: x.get("profit_rank", 999)).get("project_name", "") if data else "",
            "best_collection_project": min(data, key=lambda x: x.get("collection_rank", 999)).get("project_name", "") if data else "",
        }
    }
