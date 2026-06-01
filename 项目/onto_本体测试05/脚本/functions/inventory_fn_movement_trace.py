"""SKU 流水追溯 inventory.fn.movement_trace

参数：product_id, warehouse_id, start_date, end_date
返回：transaction_id, transaction_date, transaction_type, source_doc_type,
      source_doc_id, quantity, amount

发布：
  dazi-onto script publish 项目/onto_本体测试05/脚本/functions/inventory_fn_movement_trace.py \\
    --space space__0519 --register-function-id inventory.fn.movement_trace
"""


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    product_id = params.get("product_id", "")
    warehouse_id = params.get("warehouse_id", "")
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")

    if not product_id:
        return p.function_result(
            columns=[
                "transaction_id", "transaction_date", "transaction_type",
                "source_doc_type", "source_doc_id", "quantity", "amount",
            ],
            data=[],
            row_count=0,
        )

    filters = [f"product_id = '{product_id}'"]
    if warehouse_id:
        filters.append(f"warehouse_id = '{warehouse_id}'")
    if start_date and end_date:
        filters.append(f"transaction_date >= '{start_date}' AND transaction_date <= '{end_date}'")
    where_clause = "WHERE " + " AND ".join(filters)

    sql = f"""
    SELECT
        transaction_id,
        transaction_date,
        transaction_type,
        source_doc_type,
        source_doc_id,
        quantity,
        amount
    FROM inventory_transaction
    {where_clause}
    ORDER BY transaction_date DESC, transaction_id DESC
    LIMIT 200
    """

    result = p.sql.query(sql)
    data = []
    for row in result:
        data.append({
            "transaction_id": str(row.get("transaction_id", "")),
            "transaction_date": str(row.get("transaction_date", "")),
            "transaction_type": str(row.get("transaction_type", "")),
            "source_doc_type": str(row.get("source_doc_type", "")),
            "source_doc_id": str(row.get("source_doc_id", "")),
            "quantity": round(float(row.get("quantity", 0) or 0), 2),
            "amount": round(float(row.get("amount", 0) or 0), 2),
        })

    return p.function_result(
        columns=[
            "transaction_id", "transaction_date", "transaction_type",
            "source_doc_type", "source_doc_id", "quantity", "amount",
        ],
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
