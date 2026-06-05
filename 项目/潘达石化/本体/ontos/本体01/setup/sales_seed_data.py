"""产品销售演示数据灌入 — space__0519

前置：先执行 sales_ontology_init.py 建表。
幂等：sales_order_fact 已有数据则跳过。

放置：项目/onto_本体项目01/脚本/setup/sales_seed_data.py
"""

import json
import random
from datetime import date, datetime, timedelta

_SEED_DT = datetime(2025, 1, 1, 0, 0, 0)


def main():
    space_id = "space__0519"
    s = space.get(space_id)

    output.print("=== 产品销售演示数据灌入 ===")

    try:
        n = int(s.sql.query_one("SELECT count() FROM sales_order_fact") or 0)
    except Exception:
        n = 0
    if n > 0:
        output.print(f"sales_order_fact 已有 {n} 行，跳过灌数")
        output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "skipped": True, "rows": n}, ensure_ascii=True))
        return

    products = [
        {"product_id": "P001", "product_code": "SKU-001", "product_name": "智能手表 Pro", "product_category": "消费电子", "product_subcategory": "穿戴", "brand": "星联", "unit": "件", "list_price": 1999.0, "cost_price": 980.0, "status": "在售"},
        {"product_id": "P002", "product_code": "SKU-002", "product_name": "无线耳机 Air", "product_category": "消费电子", "product_subcategory": "音频", "brand": "星联", "unit": "件", "list_price": 899.0, "cost_price": 420.0, "status": "在售"},
        {"product_id": "P003", "product_code": "SKU-003", "product_name": "办公椅人体工学", "product_category": "家居办公", "product_subcategory": "家具", "brand": "舒适家", "unit": "件", "list_price": 2499.0, "cost_price": 1200.0, "status": "在售"},
        {"product_id": "P004", "product_code": "SKU-004", "product_name": "净水器旗舰版", "product_category": "家电", "product_subcategory": "净水", "brand": "清泉", "unit": "台", "list_price": 3299.0, "cost_price": 1650.0, "status": "在售"},
        {"product_id": "P005", "product_code": "SKU-005", "product_name": "运动跑鞋 X1", "product_category": "运动户外", "product_subcategory": "鞋类", "brand": "疾风", "unit": "双", "list_price": 699.0, "cost_price": 280.0, "status": "在售"},
        {"product_id": "P006", "product_code": "SKU-006", "product_name": "儿童学习平板", "product_category": "消费电子", "product_subcategory": "教育", "brand": "智学", "unit": "台", "list_price": 1599.0, "cost_price": 850.0, "status": "在售"},
    ]
    for p in products:
        p["created_at"] = _SEED_DT
        p["updated_at"] = _SEED_DT

    customers = [
        {"customer_id": "C001", "customer_code": "CUS-001", "customer_name": "华东连锁商超", "customer_region": "华东", "customer_type": "战略", "industry": "零售"},
        {"customer_id": "C002", "customer_code": "CUS-002", "customer_name": "北京科技贸易", "customer_region": "华北", "customer_type": "VIP", "industry": "贸易"},
        {"customer_id": "C003", "customer_code": "CUS-003", "customer_name": "广州电商运营", "customer_region": "华南", "customer_type": "VIP", "industry": "电商"},
        {"customer_id": "C004", "customer_code": "CUS-004", "customer_name": "成都区域经销", "customer_region": "西南", "customer_type": "普通", "industry": "经销"},
        {"customer_id": "C005", "customer_code": "CUS-005", "customer_name": "武汉制造企业", "customer_region": "华中", "customer_type": "普通", "industry": "制造"},
    ]
    for c in customers:
        c["created_at"] = _SEED_DT

    channels = [
        {"channel_id": "CH01", "channel_code": "DIR", "channel_name": "直营门店", "channel_type": "线下"},
        {"channel_id": "CH02", "channel_code": "ECOM", "channel_name": "官方电商", "channel_type": "线上"},
        {"channel_id": "CH03", "channel_code": "DIST", "channel_name": "经销渠道", "channel_type": "经销"},
    ]

    s.sql.insert_rows("product_master", products)
    s.sql.insert_rows("customer_dimension", customers)
    s.sql.insert_rows("channel_dimension", channels)
    output.print("OK 维表数据")

    random.seed(519)
    regions = {c["customer_id"]: c["customer_region"] for c in customers}
    ctypes = {c["customer_id"]: c["customer_type"] for c in customers}
    pcats = {p["product_id"]: p["product_category"] for p in products}
    prices = {p["product_id"]: p["list_price"] for p in products}

    fact_rows = []
    line_seq = 1
    start = date(2025, 1, 1)
    end = date(2026, 6, 30)
    days = (end - start).days + 1

    for d_offset in range(days):
        order_date = start + timedelta(days=d_offset)
        if random.random() > 0.35:
            continue
        daily_orders = random.randint(2, 8)
        for _ in range(daily_orders):
            order_id = f"O{order_date.strftime('%Y%m%d')}{random.randint(100, 999)}"
            customer_id = random.choice(list(regions.keys()))
            channel_id = random.choice(["CH01", "CH02", "CH03"])
            lines = random.randint(1, 3)
            for _ in range(lines):
                product_id = random.choice(list(pcats.keys()))
                qty = random.randint(1, 20)
                unit_price = round(prices[product_id] * random.uniform(0.85, 1.0), 2)
                discount = round(unit_price * qty * random.uniform(0, 0.08), 2)
                sales_amount = round(unit_price * qty - discount, 2)
                fact_rows.append({
                    "order_id": order_id,
                    "order_line_id": f"L{line_seq:06d}",
                    "order_date": order_date,
                    "product_id": product_id,
                    "product_category": pcats[product_id],
                    "customer_id": customer_id,
                    "customer_region": regions[customer_id],
                    "customer_type": ctypes[customer_id],
                    "channel_id": channel_id,
                    "quantity": qty,
                    "unit_price": unit_price,
                    "discount_amount": discount,
                    "sales_amount": sales_amount,
                    "currency": "CNY",
                    "order_status": random.choice(["已完成", "已完成", "已发货"]),
                })
                line_seq += 1

    inserted = s.sql.insert_rows("sales_order_fact", fact_rows)
    output.print(f"OK 销售事实表插入 {inserted} 行")

    summary = {
        "ok": True,
        "space_id": space_id,
        "products": len(products),
        "customers": len(customers),
        "channels": len(channels),
        "fact_inserted": inserted,
    }
    output.success("灌数完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))
