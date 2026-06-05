"""Panda Construction Project Summary Function

功能：获取项目经营核心指标总览
参数：project_id, report_month
返回：项目经营核心指标

放置位置：项目/onto_潘达工程_项目成本决策/脚本/functions/panda_fn_project_summary.py
"""

import json


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

    where_clause = f"WHERE project_id = '{project_id}' AND report_month = '{report_month}'"

    sql = f"""
    SELECT
        project_id,
        project_name,
        contract_amount,
        output_total_confirmed,
        output_total_total,
        output_total_unconfirmed,
        output_this_year_confirmed,
        output_this_year_total,
        cost_confirmed,
        cost_total,
        profit_confirmed,
        profit_total,
        profit_rate_confirmed,
        profit_rate_total,
        receivable_amount,
        receivable_ratio,
        received_amount,
        warning_status
    FROM wide_project_monthly
    {where_clause}
    LIMIT 1
    """

    result = s.sql.query(sql)

    if not result:
        return {
            "ok": True,
            "data": [],
            "message": "No data found for the specified project and month"
        }

    row = result[0]

    output_confirm_rate = 0.0
    if float(row.get("output_total_total", 0) or 0) > 0:
        output_confirm_rate = round(
            float(row.get("output_total_confirmed", 0) or 0) / float(row.get("output_total_total", 0)),
            4
        )

    collection_rate = 0.0
    if float(row.get("receivable_amount", 0) or 0) > 0:
        collection_rate = round(
            float(row.get("received_amount", 0) or 0) / float(row.get("receivable_amount", 0)),
            4
        )

    data = {
        "project_id": str(row.get("project_id", "")),
        "project_name": str(row.get("project_name", "")),
        "contract_amount": round(float(row.get("contract_amount", 0) or 0), 2),
        "output_total": round(float(row.get("output_total_total", 0) or 0), 2),
        "output_confirmed": round(float(row.get("output_total_confirmed", 0) or 0), 2),
        "output_confirm_rate": output_confirm_rate,
        "output_this_year": round(float(row.get("output_this_year_total", 0) or 0), 2),
        "cost_total": round(float(row.get("cost_total", 0) or 0), 2),
        "cost_confirmed": round(float(row.get("cost_confirmed", 0) or 0), 2),
        "profit_total": round(float(row.get("profit_total", 0) or 0), 2),
        "profit_confirmed": round(float(row.get("profit_confirmed", 0) or 0), 2),
        "profit_rate_total": round(float(row.get("profit_rate_total", 0) or 0), 4),
        "profit_rate_confirmed": round(float(row.get("profit_rate_confirmed", 0) or 0), 4),
        "receivable_amount": round(float(row.get("receivable_amount", 0) or 0), 2),
        "received_amount": round(float(row.get("received_amount", 0) or 0), 2),
        "collection_rate": collection_rate,
        "warning_status": str(row.get("warning_status", "green")),
    }

    return {
        "ok": True,
        "data": [data],
        "row_count": 1
    }
