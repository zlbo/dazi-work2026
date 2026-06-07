"""生产计划演示数据灌入 — space_cate_test01

前置：先执行 prod_plan_ontology_init.py 建表；dim_date 由空间其他域提供或已存在。
幂等：fact_production_daily 已有数据则跳过。

放置：项目/DAZI_TEST/本体/ontos/生产计划/setup/prod_plan_seed_data.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/生产计划/setup/prod_plan_seed_data.py --space space_cate_test01 --type data
"""

import json
import random
from datetime import date, datetime, timedelta

_SEED_DT = datetime(2025, 1, 1, 0, 0, 0)
_PLAN_VERSION_ID = "PV_MPS_202606"
_PLAN_VERSION_CODE = "MPS-2026-06"


def _date_key(d):
    return int(d.strftime("%Y%m%d"))


def main():
    space_id = "space_cate_test01"
    s = space.get(space_id)

    output.print("=== 生产计划演示数据灌入 ===")

    try:
        n = int(s.sql.query_one("SELECT count() FROM fact_production_daily") or 0)
    except Exception:
        n = 0
    if n > 0:
        output.print(f"fact_production_daily 已有 {n} 行，跳过灌数")
        output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "skipped": True, "rows": n}, ensure_ascii=True))
        return

    random.seed(6607)

    # 1. 工厂（与设备运营域共用 plant_id，便于同空间对照）
    plants = [
        {
            "plant_id": "PL001",
            "plant_code": "PL001",
            "plant_name": "乙烯工厂",
            "company_code": "PD-CHEM",
            "plant_type": "烯烃",
            "region": "华东",
            "design_capacity": 800000.0,
            "capacity_unit": "吨/年",
            "status": "运行",
        },
        {
            "plant_id": "PL002",
            "plant_code": "PL002",
            "plant_name": "芳烃工厂",
            "company_code": "PD-CHEM",
            "plant_type": "芳烃",
            "region": "华东",
            "design_capacity": 600000.0,
            "capacity_unit": "吨/年",
            "status": "运行",
        },
    ]
    for p in plants:
        p["created_at"] = _SEED_DT

    # 2. 工作中心
    work_centers = [
        {
            "work_center_id": "WC001",
            "work_center_code": "WC001",
            "work_center_name": "裂解产线A",
            "plant_id": "PL001",
            "plant_name": "乙烯工厂",
            "center_type": "反应",
            "production_mode": "连续",
            "standard_capacity_qty": 120.0,
            "capacity_unit": "吨/日",
            "available_hours_per_day": 22.0,
            "criticality": "A",
            "status": "运行",
        },
        {
            "work_center_id": "WC002",
            "work_center_code": "WC002",
            "work_center_name": "乙烯精馏线",
            "plant_id": "PL001",
            "plant_name": "乙烯工厂",
            "center_type": "分离",
            "production_mode": "连续",
            "standard_capacity_qty": 100.0,
            "capacity_unit": "吨/日",
            "available_hours_per_day": 22.0,
            "criticality": "A",
            "status": "运行",
        },
        {
            "work_center_id": "WC003",
            "work_center_code": "WC003",
            "work_center_name": "芳烃反应线",
            "plant_id": "PL002",
            "plant_name": "芳烃工厂",
            "center_type": "反应",
            "production_mode": "连续",
            "standard_capacity_qty": 80.0,
            "capacity_unit": "吨/日",
            "available_hours_per_day": 22.0,
            "criticality": "A",
            "status": "运行",
        },
        {
            "work_center_id": "WC004",
            "work_center_code": "WC004",
            "work_center_name": "芳烃精馏线",
            "plant_id": "PL002",
            "plant_name": "芳烃工厂",
            "center_type": "分离",
            "production_mode": "连续",
            "standard_capacity_qty": 70.0,
            "capacity_unit": "吨/日",
            "available_hours_per_day": 22.0,
            "criticality": "B",
            "status": "运行",
        },
    ]
    for wc in work_centers:
        wc["created_at"] = _SEED_DT
    wc_map = {wc["work_center_id"]: wc for wc in work_centers}

    # 3. 产品
    products = [
        {
            "product_id": "PR001",
            "product_code": "PR001",
            "product_name": "乙烯",
            "product_category": "烯烃",
            "product_subcategory": "基础烯烃",
            "product_type": "成品",
            "unit": "吨",
            "standard_cycle_hours": 0.5,
            "shelf_life_days": 30,
            "status": "在产",
        },
        {
            "product_id": "PR002",
            "product_code": "PR002",
            "product_name": "丙烯",
            "product_category": "烯烃",
            "product_subcategory": "基础烯烃",
            "product_type": "成品",
            "unit": "吨",
            "standard_cycle_hours": 0.6,
            "shelf_life_days": 30,
            "status": "在产",
        },
        {
            "product_id": "PR003",
            "product_code": "PR003",
            "product_name": "苯",
            "product_category": "芳烃",
            "product_subcategory": "基础芳烃",
            "product_type": "成品",
            "unit": "吨",
            "standard_cycle_hours": 0.8,
            "shelf_life_days": 60,
            "status": "在产",
        },
        {
            "product_id": "PR004",
            "product_code": "PR004",
            "product_name": "甲苯",
            "product_category": "芳烃",
            "product_subcategory": "基础芳烃",
            "product_type": "成品",
            "unit": "吨",
            "standard_cycle_hours": 0.7,
            "shelf_life_days": 60,
            "status": "在产",
        },
        {
            "product_id": "PR005",
            "product_code": "PR005",
            "product_name": "石脑油",
            "product_category": "原料",
            "product_subcategory": "进料",
            "product_type": "关键组件",
            "unit": "吨",
            "standard_cycle_hours": 0.0,
            "shelf_life_days": 15,
            "status": "在产",
        },
        {
            "product_id": "PR006",
            "product_code": "PR006",
            "product_name": "催化剂A",
            "product_category": "辅料",
            "product_subcategory": "催化剂",
            "product_type": "关键组件",
            "unit": "千克",
            "standard_cycle_hours": 0.0,
            "shelf_life_days": 180,
            "status": "在产",
        },
    ]
    for pr in products:
        pr["created_at"] = _SEED_DT
    product_map = {pr["product_id"]: pr for pr in products}

    # 4. 计划版本
    plan_versions = [
        {
            "plan_version_id": _PLAN_VERSION_ID,
            "plan_version_code": _PLAN_VERSION_CODE,
            "plan_version_name": "2026年6月主生产计划",
            "plan_type": "MPS",
            "fiscal_year": 2026,
            "fiscal_month": 6,
            "fiscal_week": 0,
            "effective_from": date(2026, 6, 1),
            "effective_to": date(2026, 6, 30),
            "status": "已发布",
            "created_at": datetime(2026, 5, 20, 0, 0, 0),
        },
    ]

    # 灌入维表（工厂若已存在则跳过）
    try:
        plant_cnt = int(s.sql.query_one("SELECT count() FROM dim_plant") or 0)
    except Exception:
        plant_cnt = 0
    if plant_cnt == 0:
        s.sql.insert_rows("dim_plant", plants)
        output.print(f"OK dim_plant {len(plants)} 条")
    else:
        output.print(f"dim_plant 已有 {plant_cnt} 条，跳过工厂灌入")

    s.sql.insert_rows("dim_work_center", work_centers)
    output.print(f"OK dim_work_center {len(work_centers)} 条")
    s.sql.insert_rows("dim_product", products)
    output.print(f"OK dim_product {len(products)} 条")
    s.sql.insert_rows("dim_plan_version", plan_versions)
    output.print(f"OK dim_plan_version {len(plan_versions)} 条")

    # 5. 2026年6月 MPS 计划行（16 条：4 产线 × 4 产品组合）
    plan_assignments = [
        ("WC001", "PR001", 3200.0),
        ("WC001", "PR002", 1800.0),
        ("WC002", "PR001", 2800.0),
        ("WC002", "PR002", 1500.0),
        ("WC003", "PR003", 2100.0),
        ("WC003", "PR004", 1600.0),
        ("WC004", "PR003", 1900.0),
        ("WC004", "PR004", 1400.0),
    ]
    plan_rows = []
    june_start = date(2026, 6, 1)
    dk_june = _date_key(june_start)
    for idx, (wc_id, pr_id, base_qty) in enumerate(plan_assignments):
        wc = wc_map[wc_id]
        pr = product_map[pr_id]
        planned_qty = round(base_qty * random.uniform(0.95, 1.05), 2)
        planned_hours = round(planned_qty * pr["standard_cycle_hours"] * 1.2, 2)
        plan_rows.append({
            "plan_line_id": f"PLN{idx + 1:04d}",
            "date_key": dk_june,
            "plan_version_id": _PLAN_VERSION_ID,
            "plan_version_code": _PLAN_VERSION_CODE,
            "plant_id": wc["plant_id"],
            "plant_name": wc["plant_name"],
            "work_center_id": wc_id,
            "work_center_name": wc["work_center_name"],
            "product_id": pr_id,
            "product_code": pr["product_code"],
            "product_name": pr["product_name"],
            "product_category": pr["product_category"],
            "fiscal_year": 2026,
            "fiscal_month": 6,
            "fiscal_week": 0,
            "planned_qty": planned_qty,
            "planned_hours": planned_hours,
            "unit": pr["unit"],
            "priority": 1 if wc["criticality"] == "A" else 2,
            "demand_source": "销售预测",
            "status": "已确认",
            "created_at": datetime(2026, 5, 25, 0, 0, 0),
        })
    plan_inserted = s.sql.insert_rows("fact_production_plan", plan_rows)
    output.print(f"OK fact_production_plan 插入 {plan_inserted} 行")

    # 6. 生产工单（20 条）
    wo_templates = [
        ("PLN0001", "WC001", "PR001", 800.0, "已完工", 1, 0),
        ("PLN0002", "WC001", "PR002", 450.0, "已完工", 1, 0),
        ("PLN0003", "WC002", "PR001", 700.0, "生产中", 1, 0),
        ("PLN0004", "WC002", "PR002", 380.0, "已下达", 1, 0),
        ("PLN0005", "WC003", "PR003", 520.0, "已完工", 0, 3),
        ("PLN0006", "WC003", "PR004", 400.0, "生产中", 1, 0),
        ("PLN0007", "WC004", "PR003", 480.0, "已完工", 1, 0),
        ("PLN0008", "WC004", "PR004", 350.0, "已关闭", 1, 0),
        ("PLN0001", "WC001", "PR001", 600.0, "生产中", 1, 0),
        ("PLN0003", "WC002", "PR001", 500.0, "已完工", 1, 0),
        ("PLN0005", "WC003", "PR003", 400.0, "已下达", 0, 5),
        ("PLN0006", "WC003", "PR004", 300.0, "已完工", 1, 0),
        ("PLN0002", "WC001", "PR002", 350.0, "已取消", 0, 0),
        ("PLN0007", "WC004", "PR003", 420.0, "生产中", 1, 0),
        ("PLN0008", "WC004", "PR004", 280.0, "已完工", 0, 2),
        ("PLN0004", "WC002", "PR002", 320.0, "已完工", 1, 0),
        ("PLN0001", "WC001", "PR001", 550.0, "已下达", 1, 0),
        ("PLN0005", "WC003", "PR003", 380.0, "生产中", 1, 0),
        ("PLN0006", "WC003", "PR004", 260.0, "已完工", 1, 0),
        ("PLN0003", "WC002", "PR001", 450.0, "已完工", 0, 4),
    ]
    wo_rows = []
    wo_base = date(2026, 5, 15)
    for idx, (plan_line_id, wc_id, pr_id, order_qty, status, on_sched, delay) in enumerate(wo_templates):
        wc = wc_map[wc_id]
        pr = product_map[pr_id]
        release_d = wo_base + timedelta(days=idx * 3)
        planned_start = release_d + timedelta(days=1)
        planned_end = planned_start + timedelta(days=random.randint(5, 12))
        if status == "已完工":
            completed = round(order_qty * random.uniform(0.92, 1.0), 2)
            actual_start = planned_start
            actual_end = planned_end + timedelta(days=delay)
        elif status == "生产中":
            completed = round(order_qty * random.uniform(0.4, 0.75), 2)
            actual_start = planned_start
            actual_end = None
        else:
            completed = 0.0
            actual_start = None
            actual_end = None
        scrapped = round((order_qty - completed) * random.uniform(0, 0.05), 2) if completed > 0 else 0.0
        wo_rows.append({
            "work_order_id": f"WO{idx + 1:04d}",
            "date_key": _date_key(release_d),
            "release_date": release_d,
            "plan_line_id": plan_line_id,
            "plan_version_id": _PLAN_VERSION_ID,
            "plant_id": wc["plant_id"],
            "plant_name": wc["plant_name"],
            "work_center_id": wc_id,
            "work_center_name": wc["work_center_name"],
            "product_id": pr_id,
            "product_code": pr["product_code"],
            "product_name": pr["product_name"],
            "order_qty": order_qty,
            "completed_qty": completed,
            "scrapped_qty": scrapped,
            "unit": pr["unit"],
            "planned_start_date": planned_start,
            "planned_end_date": planned_end,
            "actual_start_date": actual_start,
            "actual_end_date": actual_end,
            "status": status,
            "is_on_schedule": on_sched,
            "delay_days": delay,
            "created_at": datetime.combine(release_d, datetime.min.time()),
        })
    wo_inserted = s.sql.insert_rows("fact_work_order", wo_rows)
    output.print(f"OK fact_work_order 插入 {wo_inserted} 行")

    # 7. 日生产实绩（2025-01 ~ 2026-06，按周汇总）
    daily_rows = []
    daily_seq = 1
    week_start = date(2025, 1, 6)
    end_date = date(2026, 6, 30)
    wc_product_pairs = [
        ("WC001", "PR001"), ("WC001", "PR002"),
        ("WC002", "PR001"), ("WC002", "PR002"),
        ("WC003", "PR003"), ("WC003", "PR004"),
        ("WC004", "PR003"), ("WC004", "PR004"),
    ]
    while week_start <= end_date:
        dk = _date_key(week_start)
        for wc_id, pr_id in wc_product_pairs:
            wc = wc_map[wc_id]
            pr = product_map[pr_id]
            daily_plan = round(wc["standard_capacity_qty"] * 7 * random.uniform(0.85, 1.0), 2)
            achievement = random.uniform(0.82, 1.05)
            actual = round(daily_plan * achievement, 2)
            qualified = round(actual * random.uniform(0.96, 0.995), 2)
            rework = round(actual - qualified, 2)
            scrap = round(actual * random.uniform(0, 0.02), 2)
            planned_h = round(daily_plan * pr["standard_cycle_hours"], 2)
            actual_h = round(planned_h * random.uniform(0.9, 1.08), 2)
            daily_rows.append({
                "daily_id": f"DLY{daily_seq:06d}",
                "date_key": dk,
                "calendar_date": week_start,
                "plant_id": wc["plant_id"],
                "plant_name": wc["plant_name"],
                "work_center_id": wc_id,
                "work_center_name": wc["work_center_name"],
                "product_id": pr_id,
                "product_code": pr["product_code"],
                "product_name": pr["product_name"],
                "product_category": pr["product_category"],
                "shift_code": "全天",
                "planned_qty": daily_plan,
                "actual_qty": actual,
                "qualified_qty": qualified,
                "rework_qty": rework,
                "scrapped_qty": scrap,
                "planned_hours": planned_h,
                "actual_hours": actual_h,
                "unit": pr["unit"],
                "data_source": "MES",
                "created_at": datetime.combine(week_start, datetime.min.time()),
            })
            daily_seq += 1
        week_start += timedelta(days=7)

    daily_inserted = s.sql.insert_rows("fact_production_daily", daily_rows)
    output.print(f"OK fact_production_daily 插入 {daily_inserted} 行")

    # 8. 物料需求（24 条）
    mrp_templates = [
        ("WO0001", "PR001", "PR005", 1200.0, 1180.0, 1, "齐套"),
        ("WO0001", "PR001", "PR006", 80.0, 80.0, 1, "齐套"),
        ("WO0003", "PR001", "PR005", 950.0, 900.0, 1, "部分齐套"),
        ("WO0005", "PR003", "PR005", 800.0, 750.0, 1, "部分齐套"),
        ("WO0005", "PR003", "PR006", 60.0, 45.0, 1, "缺料"),
        ("WO0006", "PR004", "PR005", 600.0, 600.0, 0, "齐套"),
        ("WO0007", "PR003", "PR005", 720.0, 720.0, 1, "齐套"),
        ("WO0009", "PR001", "PR005", 850.0, 820.0, 1, "齐套"),
        ("WO0010", "PR001", "PR005", 680.0, 680.0, 1, "齐套"),
        ("WO0011", "PR003", "PR005", 550.0, 500.0, 1, "部分齐套"),
        ("WO0014", "PR003", "PR005", 700.0, 650.0, 1, "部分齐套"),
        ("WO0014", "PR003", "PR006", 55.0, 55.0, 1, "齐套"),
    ]
    mrp_rows = []
    mrp_base = date(2026, 5, 20)
    for idx, (wo_id, parent_id, comp_id, req_qty, issue_qty, critical, kit) in enumerate(mrp_templates):
        parent = product_map[parent_id]
        comp = product_map[comp_id]
        req_d = mrp_base + timedelta(days=idx * 2)
        mrp_rows.append({
            "mrp_line_id": f"MRP{idx + 1:04d}",
            "date_key": _date_key(req_d),
            "requirement_date": req_d,
            "work_order_id": wo_id,
            "plant_id": "PL001" if parent_id in ("PR001", "PR002") else "PL002",
            "parent_product_id": parent_id,
            "parent_product_code": parent["product_code"],
            "component_product_id": comp_id,
            "component_product_code": comp["product_code"],
            "component_product_name": comp["product_name"],
            "planned_require_qty": req_qty,
            "actual_issue_qty": issue_qty,
            "unit": comp["unit"],
            "is_critical": critical,
            "kit_status": kit,
            "created_at": datetime.combine(req_d, datetime.min.time()),
        })
    mrp_inserted = s.sql.insert_rows("fact_material_requirement", mrp_rows)
    output.print(f"OK fact_material_requirement 插入 {mrp_inserted} 行")

    # 9. 产能负荷（2026年6月，按产线×周）
    load_rows = []
    load_seq = 1
    load_week = date(2026, 6, 2)
    while load_week <= date(2026, 6, 30):
        dk = _date_key(load_week)
        for wc in work_centers:
            avail = wc["available_hours_per_day"] * 7
            planned_load = round(avail * random.uniform(0.75, 0.98), 2)
            actual_load = round(planned_load * random.uniform(0.85, 1.05), 2)
            planned_out = round(wc["standard_capacity_qty"] * 7 * random.uniform(0.9, 1.0), 2)
            actual_out = round(planned_out * random.uniform(0.82, 1.03), 2)
            load_rows.append({
                "load_id": f"LD{load_seq:05d}",
                "date_key": dk,
                "calendar_date": load_week,
                "plan_version_id": _PLAN_VERSION_ID,
                "plant_id": wc["plant_id"],
                "work_center_id": wc["work_center_id"],
                "work_center_name": wc["work_center_name"],
                "available_hours": avail,
                "planned_load_hours": planned_load,
                "actual_load_hours": actual_load,
                "planned_output_qty": planned_out,
                "actual_output_qty": actual_out,
                "capacity_unit": wc["capacity_unit"],
                "created_at": datetime.combine(load_week, datetime.min.time()),
            })
            load_seq += 1
        load_week += timedelta(days=7)

    load_inserted = s.sql.insert_rows("fact_capacity_load", load_rows)
    output.print(f"OK fact_capacity_load 插入 {load_inserted} 行")

    summary = {
        "ok": True,
        "space_id": space_id,
        "work_centers": len(work_centers),
        "products": len(products),
        "plan_inserted": plan_inserted,
        "wo_inserted": wo_inserted,
        "daily_inserted": daily_inserted,
        "mrp_inserted": mrp_inserted,
        "load_inserted": load_inserted,
    }
    output.success("生产计划演示数据灌入完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))
