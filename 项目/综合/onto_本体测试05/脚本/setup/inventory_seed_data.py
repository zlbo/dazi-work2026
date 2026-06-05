"""库存演示数据灌入 — space__0519

前置：先执行 inventory_ontology_init.py 建表。
幂等：inventory_balance_snapshot 已有数据则跳过。
字段对齐 DRAP 模板：SKU-001/002、WH-01/02。

放置：项目/onto_本体测试05/脚本/setup/inventory_seed_data.py
发布：dazi-onto script publish 项目/onto_本体测试05/脚本/setup/inventory_seed_data.py --space space__0519
"""

import json
import random
from datetime import date, datetime, timedelta

_SEED_DT = datetime(2026, 5, 1, 0, 0, 0)
_SNAPSHOT_DATE = date(2026, 5, 26)


def main():
    space_id = "space__0519"
    s = space.get(space_id)

    output.print("=== 库存演示数据灌入 ===")

    try:
        n = int(s.sql.query_one("SELECT count() FROM inventory_balance_snapshot") or 0)
    except Exception:
        n = 0
    if n > 0:
        output.print(f"inventory_balance_snapshot 已有 {n} 行，跳过灌数")
        output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "skipped": True, "rows": n}, ensure_ascii=True))
        return

    products = [
        {
            "product_id": "INV001",
            "product_code": "SKU-001",
            "product_name": "原料A",
            "product_category": "原料",
            "product_subcategory": "化工原料",
            "brand": "自有",
            "unit": "件",
            "list_price": 120.0,
            "cost_price": 85.0,
            "status": "在用",
            "created_at": _SEED_DT,
            "updated_at": _SEED_DT,
        },
        {
            "product_id": "INV002",
            "product_code": "SKU-002",
            "product_name": "成品B",
            "product_category": "成品",
            "product_subcategory": "包装成品",
            "brand": "自有",
            "unit": "件",
            "list_price": 560.0,
            "cost_price": 320.0,
            "status": "在用",
            "created_at": _SEED_DT,
            "updated_at": _SEED_DT,
        },
        {
            "product_id": "INV003",
            "product_code": "SKU-003",
            "product_name": "半成品C",
            "product_category": "半成品",
            "product_subcategory": "组装件",
            "brand": "自有",
            "unit": "件",
            "list_price": 280.0,
            "cost_price": 150.0,
            "status": "在用",
            "created_at": _SEED_DT,
            "updated_at": _SEED_DT,
        },
    ]

    warehouses = [
        {
            "warehouse_id": "WH-01",
            "warehouse_code": "WH-01",
            "warehouse_name": "原料仓一号",
            "warehouse_type": "原料仓",
            "region": "华东工厂",
            "status": "启用",
        },
        {
            "warehouse_id": "WH-02",
            "warehouse_code": "WH-02",
            "warehouse_name": "成品仓二号",
            "warehouse_type": "成品仓",
            "region": "华东工厂",
            "status": "启用",
        },
    ]

    for p in products:
        try:
            exists = s.sql.query_one(
                f"SELECT count() FROM product_master WHERE product_id = '{p['product_id']}'"
            )
            if int(exists or 0) == 0:
                s.sql.insert_rows("product_master", [p])
        except Exception:
            s.sql.insert_rows("product_master", [p])

    s.sql.insert_rows("warehouse_dimension", warehouses)
    output.print("OK 维表数据")

    snapshots = [
        {
            "snapshot_id": "SNAP-INV001-WH01",
            "snapshot_date": _SNAPSHOT_DATE,
            "product_id": "INV001",
            "warehouse_id": "WH-01",
            "on_hand_qty": 520.0,
            "available_qty": 500.0,
            "in_transit_qty": 80.0,
            "reserved_qty": 20.0,
            "safety_stock": 200.0,
            "unit_cost": 85.0,
            "inventory_amount": 44200.0,
        },
        {
            "snapshot_id": "SNAP-INV002-WH02",
            "snapshot_date": _SNAPSHOT_DATE,
            "product_id": "INV002",
            "warehouse_id": "WH-02",
            "on_hand_qty": 88.0,
            "available_qty": 88.0,
            "in_transit_qty": 0.0,
            "reserved_qty": 0.0,
            "safety_stock": 100.0,
            "unit_cost": 320.0,
            "inventory_amount": 28160.0,
        },
        {
            "snapshot_id": "SNAP-INV003-WH02",
            "snapshot_date": _SNAPSHOT_DATE,
            "product_id": "INV003",
            "warehouse_id": "WH-02",
            "on_hand_qty": 0.0,
            "available_qty": 0.0,
            "in_transit_qty": 0.0,
            "reserved_qty": 0.0,
            "safety_stock": 50.0,
            "unit_cost": 150.0,
            "inventory_amount": 0.0,
        },
        {
            "snapshot_id": "SNAP-INV003-WH01",
            "snapshot_date": _SNAPSHOT_DATE,
            "product_id": "INV003",
            "warehouse_id": "WH-01",
            "on_hand_qty": 340.0,
            "available_qty": 320.0,
            "in_transit_qty": 0.0,
            "reserved_qty": 20.0,
            "safety_stock": 120.0,
            "unit_cost": 150.0,
            "inventory_amount": 51000.0,
        },
    ]
    s.sql.insert_rows("inventory_balance_snapshot", snapshots)
    output.print("OK 库存快照")

    random.seed(526)
    txn_rows = []
    seq = 1
    end = _SNAPSHOT_DATE
    start = end - timedelta(days=29)
    product_ids = ["INV001", "INV002", "INV003"]
    wh_map = {"INV001": "WH-01", "INV002": "WH-02", "INV003": random.choice(["WH-01", "WH-02"])}

    for d_offset in range((end - start).days + 1):
        txn_date = start + timedelta(days=d_offset)
        daily = random.randint(1, 4)
        for _ in range(daily):
            product_id = random.choice(product_ids)
            warehouse_id = wh_map.get(product_id, "WH-01")
            txn_type = random.choice(["IN", "OUT", "OUT", "ADJUST"])
            qty = random.randint(5, 40)
            if txn_type == "OUT":
                qty = -qty
            unit_cost = {"INV001": 85.0, "INV002": 320.0, "INV003": 150.0}[product_id]
            txn_rows.append({
                "transaction_id": f"TXN{seq:06d}",
                "transaction_time": datetime.combine(txn_date, datetime.min.time()),
                "transaction_date": txn_date,
                "product_id": product_id,
                "warehouse_id": warehouse_id,
                "to_warehouse_id": "",
                "transaction_type": txn_type,
                "source_doc_type": random.choice(["采购入库", "销售出库", "生产领料", "盘点调整"]),
                "source_doc_id": f"DOC-{txn_date.strftime('%Y%m%d')}-{seq}",
                "quantity": float(qty),
                "unit_cost": unit_cost,
                "amount": round(abs(qty) * unit_cost, 2),
                "batch_no": f"B{txn_date.strftime('%Y%m')}",
                "operator": "system",
            })
            seq += 1

    inserted = s.sql.insert_rows("inventory_transaction", txn_rows)
    output.print(f"OK 库存流水插入 {inserted} 行")

    summary = {
        "ok": True,
        "space_id": space_id,
        "products": len(products),
        "warehouses": len(warehouses),
        "snapshots": len(snapshots),
        "txn_inserted": inserted,
        "snapshot_date": str(_SNAPSHOT_DATE),
    }
    output.success("灌数完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))
