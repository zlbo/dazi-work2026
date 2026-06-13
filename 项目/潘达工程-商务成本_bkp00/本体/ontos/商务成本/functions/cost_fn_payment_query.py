"""商务成本 - 项目付款查询 cost.fn.payment_query

参数：start_date, end_date, project_id（可选）, approval_status（可选）
返回：id, project_id, project_name, contract_id, contract_name, report_period, payable_amount, paid_amount, unpaid_amount, approval_status

发布：
  dazi onto script publish 项目/潘达工程-商务成本/本体/ontos/商务成本/functions/cost_fn_payment_query.py \
    --space space__panda_construction --register-function-id cost.fn.payment_query
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2025-12-31"},
    "object_type_code": "ProjectPayment",
}


def _build_where(start_date, end_date, project_id=None, approval_status=None):
    clauses = []
    if start_date and end_date:
        clauses.append(f"report_period >= '{start_date[:7]}' AND report_period <= '{end_date[:7]}'")
    if project_id:
        clauses.append(f"p.project_id = '{project_id}'")
    if approval_status:
        clauses.append(f"p.approval_status = '{approval_status}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")
    project_id = params.get("project_id") or None
    approval_status = params.get("approval_status") or None
    where_clause = _build_where(start_date, end_date, project_id, approval_status)

    sql = f"""
    SELECT 
        p.id,
        p.project_id,
        pr.project_name,
        p.contract_id,
        c.contract_name,
        p.report_period,
        p.payable_amount,
        p.paid_amount,
        p.unpaid_amount,
        p.approval_status,
        p.approval_amount,
        p.payment_type,
        p.payment_ratio
    FROM fact_project_payment p
    JOIN dim_project pr ON p.project_id = pr.project_id
    LEFT JOIN dim_contract c ON p.contract_id = c.contract_id
    {where_clause}
    ORDER BY p.report_period DESC, p.project_id
    """

    rows = p.sql.query(sql)
    data = []
    for row in rows:
        data.append({
            "id": row.get("id", ""),
            "project_id": row.get("project_id", ""),
            "project_name": row.get("project_name", ""),
            "contract_id": row.get("contract_id", ""),
            "contract_name": row.get("contract_name", ""),
            "report_period": row.get("report_period", ""),
            "payable_amount": round(float(row.get("payable_amount") or 0), 2),
            "paid_amount": round(float(row.get("paid_amount") or 0), 2),
            "unpaid_amount": round(float(row.get("unpaid_amount") or 0), 2),
            "approval_status": row.get("approval_status", ""),
            "approval_amount": round(float(row.get("approval_amount") or 0), 2),
            "payment_type": row.get("payment_type", ""),
            "payment_ratio": round(float(row.get("payment_ratio") or 0), 4),
        })

    return p.function_result(
        columns=["id", "project_id", "project_name", "contract_id", "contract_name", 
                 "report_period", "payable_amount", "paid_amount", "unpaid_amount", 
                 "approval_status", "approval_amount", "payment_type", "payment_ratio"],
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