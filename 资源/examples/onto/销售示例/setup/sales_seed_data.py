"""产品销售演示数据灌入 — space__misc_01

前置：先执行 sales_ontology_init.py 建表。
幂等：fact_sales_order_line 已有数据则跳过。

放置：项目/DAZI_TEST/本体/ontos/销售本体示例/setup/sales_seed_data.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/销售本体示例/setup/sales_seed_data.py --space space__misc_01 --type data
"""

import json
import random
from datetime import date, datetime, timedelta


_SEED_DT = datetime(2025, 1, 1, 0, 0, 0)


def main():
    space_id = "space__misc_01"
    s = space.get(space_id)

    output.print("=== 产品销售演示数据灌入 ===")

    # 检查是否已有数据
    try:
        n = int(s.sql.query_one("SELECT count() FROM fact_sales_order_line") or 0)
    except Exception:
        n = 0
    if n > 0:
        output.print(f"fact_sales_order_line 已有 {n} 行，跳过灌数")
        output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "skipped": True, "rows": n}, ensure_ascii=False))
        return

    # 1. 灌入 dim_date
    output.print("\n[1/4] 灌入 dim_date...")
    dim_date_rows = []
    start_date = date(2025, 1, 1)
    end_date = date(2026, 6, 30)
    current = start_date
    while current <= end_date:
        date_key = int(current.strftime("%Y%m%d"))
        year = current.year
        month = current.month
        quarter = (month - 1) // 3 + 1
        week_of_year = current.isocalendar()[1]
        day_of_week = current.weekday()
        is_weekend = 1 if day_of_week >= 5 else 0
        year_month = current.strftime("%Y-%m")
        dim_date_rows.append({
            "date_key": date_key,
            "calendar_date": current,
            "year": year,
            "quarter": quarter,
            "month": month,
            "week_of_year": week_of_year,
            "day_of_week": day_of_week,
            "is_weekend": is_weekend,
            "year_month": year_month,
        })
        current += timedelta(days=1)
    s.sql.insert_rows("dim_date", dim_date_rows)
    output.print(f"OK dim_date 插入 {len(dim_date_rows)} 行")

    # 2. 灌入维表
    output.print("\n[2/4] 灌入维表...")

    products = [
        {"product_id": "P001", "product_code": "OIL-92", "product_name": "92号汽油", "product_category": "成品油", "product_subcategory": "汽油", "brand": "潘达", "unit": "吨", "list_price": 8200.0, "cost_price": 7100.0, "status": "在售"},
        {"product_id": "P002", "product_code": "OIL-0", "product_name": "0号柴油", "product_category": "成品油", "product_subcategory": "柴油", "brand": "潘达", "unit": "吨", "list_price": 7500.0, "cost_price": 6500.0, "status": "在售"},
        {"product_id": "P003", "product_code": "CHEM-LLDPE", "product_name": "线性低密度聚乙烯", "product_category": "化工品", "product_subcategory": "聚乙烯", "brand": "潘达", "unit": "吨", "list_price": 9200.0, "cost_price": 8100.0, "status": "在售"},
        {"product_id": "P004", "product_code": "CHEM-PP", "product_name": "聚丙烯PP", "product_category": "化工品", "product_subcategory": "聚丙烯", "brand": "潘达", "unit": "吨", "list_price": 8800.0, "cost_price": 7800.0, "status": "在售"},
        {"product_id": "P005", "product_code": "LUB-BASE", "product_name": "润滑油基础油", "product_category": "润滑油", "product_subcategory": "基础油", "brand": "潘达", "unit": "吨", "list_price": 6800.0, "cost_price": 5900.0, "status": "在售"},
        {"product_id": "P006", "product_code": "COKE-1", "product_name": "石油焦", "product_category": "副产品", "product_subcategory": "石油焦", "brand": "潘达", "unit": "吨", "list_price": 3200.0, "cost_price": 2600.0, "status": "在售"},
    ]
    for p in products:
        p["created_at"] = _SEED_DT
        p["updated_at"] = _SEED_DT

    customers = [
        {"customer_id": "C001", "customer_code": "CUS-001", "customer_name": "华东油品经销", "customer_region": "华东", "customer_type": "战略", "industry": "经销"},
        {"customer_id": "C002", "customer_code": "CUS-002", "customer_name": "华北炼化贸易", "customer_region": "华北", "customer_type": "VIP", "industry": "贸易"},
        {"customer_id": "C003", "customer_code": "CUS-003", "customer_name": "华南化工采购", "customer_region": "华南", "customer_type": "VIP", "industry": "化工"},
        {"customer_id": "C004", "customer_code": "CUS-004", "customer_name": "西南区域物流", "customer_region": "西南", "customer_type": "普通", "industry": "物流"},
        {"customer_id": "C005", "customer_code": "CUS-005", "customer_name": "华中制造集团", "customer_region": "华中", "customer_type": "普通", "industry": "制造"},
    ]
    for c in customers:
        c["created_at"] = _SEED_DT

    channels = [
        {"channel_id": "CH01", "channel_code": "DIR", "channel_name": "直销", "channel_type": "直销"},
        {"channel_id": "CH02", "channel_code": "DIST", "channel_name": "经销渠道", "channel_type": "经销"},
        {"channel_id": "CH03", "channel_code": "B2B", "channel_name": "B2B平台", "channel_type": "线上"},
    ]

    s.sql.insert_rows("dim_product", products)
    s.sql.insert_rows("dim_customer", customers)
    s.sql.insert_rows("dim_channel", channels)
    output.print(f"OK dim_product {len(products)} 行, dim_customer {len(customers)} 行, dim_channel {len(channels)} 行")

    # 3. 生成销售事实数据
    output.print("\n[3/4] 生成销售事实数据...")
    random.seed(627)
    regions = {c["customer_id"]: c["customer_region"] for c in customers}
    ctypes = {c["customer_id"]: c["customer_type"] for c in customers}
    pcats = {p["product_id"]: p["product_category"] for p in products}
    prices = {p["product_id"]: p["list_price"] for p in products}

    fact_rows = []
    line_seq = 1
    days = (end_date - start_date).days + 1

    for d_offset in range(days):
        order_date = start_date + timedelta(days=d_offset)
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
                qty = random.randint(5, 200)
                unit_price = round(prices[product_id] * random.uniform(0.92, 1.0), 2)
                discount = round(unit_price * qty * random.uniform(0, 0.05), 2)
                sales_amount = round(unit_price * qty - discount, 2)
                date_key = int(order_date.strftime("%Y%m%d"))
                fact_rows.append({
                    "order_id": order_id,
                    "order_line_id": f"L{line_seq:06d}",
                    "date_key": date_key,
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

    s.sql.insert_rows("fact_sales_order_line", fact_rows)
    output.print(f"OK fact_sales_order_line 插入 {len(fact_rows)} 行")

    # 4. 完成
    summary = {
        "ok": True,
        "space_id": space_id,
        "dim_date": len(dim_date_rows),
        "products": len(products),
        "customers": len(customers),
        "channels": len(channels),
        "fact_inserted": len(fact_rows),
    }
    output.success("灌数完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=False, default=str))
