"""化工设备运营分析演示数据灌入 — space_cate_test01

前置：先执行 equip_ops_ontology_init.py 建表；dim_date 由空间其他域提供或已存在。
幂等：fact_equipment_daily_ops 已有数据则跳过。

放置：项目/DAZI_TEST/本体/ontos/设备运营/setup/equip_ops_seed_data.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/设备运营/setup/equip_ops_seed_data.py --space space_cate_test01 --type data
"""

import json
import random
from datetime import date, datetime, timedelta

_SEED_DT = datetime(2025, 1, 1, 0, 0, 0)
_PLAN_VERSION = "2026月度计划"
_WEEKLY_MINUTES = 7 * 1440  # 每周一行，日历时间按 7 天计


def _date_key(d):
    return int(d.strftime("%Y%m%d"))


def main():
    space_id = "space_cate_test01"
    s = space.get(space_id)

    output.print("=== 化工设备运营分析演示数据灌入 ===")

    try:
        n = int(s.sql.query_one("SELECT count() FROM fact_equipment_daily_ops") or 0)
    except Exception:
        n = 0
    if n > 0:
        output.print(f"fact_equipment_daily_ops 已有 {n} 行，跳过灌数")
        output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "skipped": True, "rows": n}, ensure_ascii=True))
        return

    random.seed(8806)

    # 1. 厂区
    plants = [
        {
            "plant_id": "PL001",
            "plant_code": "PL001",
            "plant_name": "乙烯装置区",
            "company_code": "PD-CHEM",
            "plant_type": "烯烃",
            "location": "华东炼化基地A区",
            "design_capacity": 800000.0,
            "capacity_unit": "吨/年",
            "status": "运行",
        },
        {
            "plant_id": "PL002",
            "plant_code": "PL002",
            "plant_name": "芳烃装置区",
            "company_code": "PD-CHEM",
            "plant_type": "芳烃",
            "location": "华东炼化基地B区",
            "design_capacity": 600000.0,
            "capacity_unit": "吨/年",
            "status": "运行",
        },
    ]
    for p in plants:
        p["created_at"] = _SEED_DT

    # 2. 工艺单元（4 个）
    units = [
        {
            "unit_id": "PU001",
            "unit_code": "PU001",
            "unit_name": "裂解炉区",
            "plant_id": "PL001",
            "plant_name": "乙烯装置区",
            "unit_type": "反应",
            "criticality": "A",
            "status": "运行",
        },
        {
            "unit_id": "PU002",
            "unit_code": "PU002",
            "unit_name": "分离精馏区",
            "plant_id": "PL001",
            "plant_name": "乙烯装置区",
            "unit_type": "分离",
            "criticality": "A",
            "status": "运行",
        },
        {
            "unit_id": "PU003",
            "unit_code": "PU003",
            "unit_name": "芳烃反应区",
            "plant_id": "PL002",
            "plant_name": "芳烃装置区",
            "unit_type": "反应",
            "criticality": "A",
            "status": "运行",
        },
        {
            "unit_id": "PU004",
            "unit_code": "PU004",
            "unit_name": "芳烃精馏区",
            "plant_id": "PL002",
            "plant_name": "芳烃装置区",
            "unit_type": "分离",
            "criticality": "B",
            "status": "运行",
        },
    ]
    for u in units:
        u["created_at"] = _SEED_DT

    # 3. 设备类型树
    equip_types = [
        {"equip_type_id": "ET_DYN", "equip_type_code": "DYN", "equip_type_name": "动设备", "category": "动设备", "parent_type_id": "", "type_level": 1, "is_leaf": False, "status": "启用"},
        {"equip_type_id": "ET_STA", "equip_type_code": "STA", "equip_type_name": "静设备", "category": "静设备", "parent_type_id": "", "type_level": 1, "is_leaf": False, "status": "启用"},
        {"equip_type_id": "ET_PUMP", "equip_type_code": "PUMP", "equip_type_name": "泵", "category": "动设备", "parent_type_id": "ET_DYN", "type_level": 2, "is_leaf": True, "status": "启用"},
        {"equip_type_id": "ET_COMP", "equip_type_code": "COMP", "equip_type_name": "压缩机", "category": "动设备", "parent_type_id": "ET_DYN", "type_level": 2, "is_leaf": True, "status": "启用"},
        {"equip_type_id": "ET_REACT", "equip_type_code": "REACT", "equip_type_name": "反应釜", "category": "静设备", "parent_type_id": "ET_STA", "type_level": 2, "is_leaf": True, "status": "启用"},
        {"equip_type_id": "ET_TOWER", "equip_type_code": "TOWER", "equip_type_name": "塔器", "category": "静设备", "parent_type_id": "ET_STA", "type_level": 2, "is_leaf": True, "status": "启用"},
    ]
    for et in equip_types:
        et["created_at"] = _SEED_DT
    type_map = {et["equip_type_id"]: et for et in equip_types}

    # 4. 设备（8 台）
    equipment = [
        {
            "equipment_id": "EQ001",
            "equipment_code": "P-101A",
            "equipment_name": "裂解进料泵A",
            "equip_type_id": "ET_PUMP",
            "plant_id": "PL001",
            "unit_id": "PU001",
            "manufacturer": "大连深蓝",
            "model": "OH2-200",
            "install_date": date(2018, 6, 15),
            "design_capacity": 120.0,
            "capacity_unit": "m³/h",
            "criticality": "A",
            "production_mode": "连续",
            "status": "运行",
            "ideal_cycle_rate": 0.083,
            "output_unit": "吨",
            "energy_base": 850.0,
        },
        {
            "equipment_id": "EQ002",
            "equipment_code": "C-201B",
            "equipment_name": "裂解气压缩机B",
            "equip_type_id": "ET_COMP",
            "plant_id": "PL001",
            "unit_id": "PU001",
            "manufacturer": "沈阳鼓风机",
            "model": "MCL403",
            "install_date": date(2017, 3, 20),
            "design_capacity": 50000.0,
            "capacity_unit": "Nm³/h",
            "criticality": "A",
            "production_mode": "连续",
            "status": "运行",
            "ideal_cycle_rate": 34.7,
            "output_unit": "吨",
            "energy_base": 12000.0,
        },
        {
            "equipment_id": "EQ003",
            "equipment_code": "T-401",
            "equipment_name": "乙烯精馏塔",
            "equip_type_id": "ET_TOWER",
            "plant_id": "PL001",
            "unit_id": "PU002",
            "manufacturer": "兰石重装",
            "model": "T-1200",
            "install_date": date(2018, 9, 1),
            "design_capacity": 80.0,
            "capacity_unit": "t/h",
            "criticality": "A",
            "production_mode": "连续",
            "status": "运行",
            "ideal_cycle_rate": 1.33,
            "output_unit": "吨",
            "energy_base": 3200.0,
        },
        {
            "equipment_id": "EQ004",
            "equipment_code": "P-102B",
            "equipment_name": "回流泵B",
            "equip_type_id": "ET_PUMP",
            "plant_id": "PL001",
            "unit_id": "PU002",
            "manufacturer": "大连深蓝",
            "model": "BB2-150",
            "install_date": date(2019, 1, 10),
            "design_capacity": 90.0,
            "capacity_unit": "m³/h",
            "criticality": "B",
            "production_mode": "连续",
            "status": "运行",
            "ideal_cycle_rate": 0.062,
            "output_unit": "吨",
            "energy_base": 620.0,
        },
        {
            "equipment_id": "EQ005",
            "equipment_code": "R-301",
            "equipment_name": "芳烃反应釜",
            "equip_type_id": "ET_REACT",
            "plant_id": "PL002",
            "unit_id": "PU003",
            "manufacturer": "张化机",
            "model": "R-5000",
            "install_date": date(2019, 5, 8),
            "design_capacity": 45.0,
            "capacity_unit": "t/h",
            "criticality": "A",
            "production_mode": "连续",
            "status": "运行",
            "ideal_cycle_rate": 0.75,
            "output_unit": "吨",
            "energy_base": 4500.0,
        },
        {
            "equipment_id": "EQ006",
            "equipment_code": "C-202A",
            "equipment_name": "循环氢压缩机A",
            "equip_type_id": "ET_COMP",
            "plant_id": "PL002",
            "unit_id": "PU003",
            "manufacturer": "沈阳鼓风机",
            "model": "MCL303",
            "install_date": date(2018, 11, 22),
            "design_capacity": 35000.0,
            "capacity_unit": "Nm³/h",
            "criticality": "A",
            "production_mode": "连续",
            "status": "运行",
            "ideal_cycle_rate": 24.3,
            "output_unit": "吨",
            "energy_base": 9800.0,
        },
        {
            "equipment_id": "EQ007",
            "equipment_code": "T-402",
            "equipment_name": "二甲苯精馏塔",
            "equip_type_id": "ET_TOWER",
            "plant_id": "PL002",
            "unit_id": "PU004",
            "manufacturer": "兰石重装",
            "model": "T-900",
            "install_date": date(2020, 2, 14),
            "design_capacity": 55.0,
            "capacity_unit": "t/h",
            "criticality": "B",
            "production_mode": "连续",
            "status": "运行",
            "ideal_cycle_rate": 0.92,
            "output_unit": "吨",
            "energy_base": 2800.0,
        },
        {
            "equipment_id": "EQ008",
            "equipment_code": "P-103A",
            "equipment_name": "芳烃输送泵A",
            "equip_type_id": "ET_PUMP",
            "plant_id": "PL002",
            "unit_id": "PU004",
            "manufacturer": "大连深蓝",
            "model": "OH2-180",
            "install_date": date(2020, 8, 5),
            "design_capacity": 100.0,
            "capacity_unit": "m³/h",
            "criticality": "B",
            "production_mode": "连续",
            "status": "运行",
            "ideal_cycle_rate": 0.069,
            "output_unit": "吨",
            "energy_base": 720.0,
        },
    ]
    plant_map = {p["plant_id"]: p for p in plants}
    unit_map = {u["unit_id"]: u for u in units}
    for eq in equipment:
        et = type_map[eq["equip_type_id"]]
        pl = plant_map[eq["plant_id"]]
        un = unit_map[eq["unit_id"]]
        eq["equip_type_name"] = et["equip_type_name"]
        eq["category"] = et["category"]
        eq["plant_name"] = pl["plant_name"]
        eq["unit_name"] = un["unit_name"]
        eq["created_at"] = _SEED_DT

    eq_map = {e["equipment_id"]: e for e in equipment}

    # 5. 停机原因码表
    reasons = [
        {"reason_id": "DR_PLAN", "reason_code": "PLAN", "reason_name": "计划检修", "reason_category": "计划检修", "is_planned": 1, "parent_reason_id": "", "status": "启用"},
        {"reason_id": "DR_MECH", "reason_code": "MECH", "reason_name": "机械故障", "reason_category": "机械", "is_planned": 0, "parent_reason_id": "", "status": "启用"},
        {"reason_id": "DR_MECH_SEAL", "reason_code": "MECH-SEAL", "reason_name": "密封泄漏", "reason_category": "机械", "is_planned": 0, "parent_reason_id": "DR_MECH", "status": "启用"},
        {"reason_id": "DR_MECH_BEAR", "reason_code": "MECH-BEAR", "reason_name": "轴承损坏", "reason_category": "机械", "is_planned": 0, "parent_reason_id": "DR_MECH", "status": "启用"},
        {"reason_id": "DR_ELEC", "reason_code": "ELEC", "reason_name": "电气故障", "reason_category": "电气", "is_planned": 0, "parent_reason_id": "", "status": "启用"},
        {"reason_id": "DR_INST", "reason_code": "INST", "reason_name": "仪表故障", "reason_category": "仪表", "is_planned": 0, "parent_reason_id": "", "status": "启用"},
        {"reason_id": "DR_PROC", "reason_code": "PROC", "reason_name": "工艺异常", "reason_category": "工艺", "is_planned": 0, "parent_reason_id": "", "status": "启用"},
        {"reason_id": "DR_EXT", "reason_code": "EXT", "reason_name": "外部因素", "reason_category": "外部", "is_planned": 0, "parent_reason_id": "", "status": "启用"},
    ]
    for r in reasons:
        r["created_at"] = _SEED_DT
    reason_map = {r["reason_id"]: r for r in reasons}

    # 灌入维表
    s.sql.insert_rows("dim_plant", plants)
    output.print(f"OK dim_plant {len(plants)} 条")
    s.sql.insert_rows("dim_process_unit", units)
    output.print(f"OK dim_process_unit {len(units)} 条")
    s.sql.insert_rows("dim_equipment_type", equip_types)
    output.print(f"OK dim_equipment_type {len(equip_types)} 条")

    equip_rows = [{k: v for k, v in eq.items() if k not in ("ideal_cycle_rate", "output_unit", "energy_base")} for eq in equipment]
    s.sql.insert_rows("dim_equipment", equip_rows)
    output.print(f"OK dim_equipment {len(equip_rows)} 条")
    s.sql.insert_rows("dim_downtime_reason", reasons)
    output.print(f"OK dim_downtime_reason {len(reasons)} 条")

    # 6. 设备周运行汇总（2025-01-01 ~ 2026-06-30，每周每设备 1 行）
    ops_rows = []
    ops_seq = 1
    start = date(2025, 1, 1)
    end = date(2026, 6, 30)
    week_start = start

    while week_start <= end:
        week_end = min(week_start + timedelta(days=6), end)
        dk = _date_key(week_start)

        for eq in equipment:
            avail_target = random.uniform(0.82, 0.96)
            perf_target = random.uniform(0.88, 0.98)
            qual_target = random.uniform(0.97, 0.995)

            planned_dt = round(_WEEKLY_MINUTES * random.uniform(0.02, 0.08), 1)
            sched_runtime = _WEEKLY_MINUTES - planned_dt
            unplanned_dt = round(sched_runtime * (1 - avail_target) * random.uniform(0.5, 1.2), 1)
            unplanned_dt = min(unplanned_dt, sched_runtime * 0.25)
            runtime = round(sched_runtime - unplanned_dt, 1)
            idle = round(max(_WEEKLY_MINUTES - planned_dt - unplanned_dt - runtime, 0), 1)

            ideal_rate = eq["ideal_cycle_rate"]
            actual_out = round(runtime * ideal_rate * perf_target * random.uniform(0.92, 1.05), 2)
            qualified_out = round(actual_out * qual_target, 2)
            planned_out = round(sched_runtime * ideal_rate * random.uniform(0.95, 1.02), 2)
            energy = round(eq["energy_base"] * (runtime / _WEEKLY_MINUTES) * random.uniform(0.9, 1.1), 2)

            ops_rows.append({
                "ops_id": f"OPS{week_start.strftime('%Y%m%d')}{ops_seq:04d}{eq['equipment_id']}",
                "date_key": dk,
                "calendar_date": week_start,
                "equipment_id": eq["equipment_id"],
                "equipment_code": eq["equipment_code"],
                "equipment_name": eq["equipment_name"],
                "plant_id": eq["plant_id"],
                "plant_name": eq["plant_name"],
                "unit_id": eq["unit_id"],
                "unit_name": eq["unit_name"],
                "equip_type_id": eq["equip_type_id"],
                "category": eq["category"],
                "calendar_minutes": float(_WEEKLY_MINUTES),
                "planned_downtime_min": planned_dt,
                "unplanned_downtime_min": unplanned_dt,
                "runtime_min": runtime,
                "idle_min": idle,
                "planned_output_qty": planned_out,
                "actual_output_qty": actual_out,
                "qualified_output_qty": qualified_out,
                "output_unit": eq["output_unit"],
                "ideal_cycle_rate": ideal_rate,
                "energy_consumption": energy,
                "energy_unit": "kWh",
                "shift_code": "全天",
                "data_source": "MES",
                "created_at": datetime.combine(week_start, datetime.min.time()),
            })
            ops_seq += 1

        week_start += timedelta(days=7)

    ops_inserted = s.sql.insert_rows("fact_equipment_daily_ops", ops_rows)
    output.print(f"OK fact_equipment_daily_ops 插入 {ops_inserted} 行")

    # 7. 停机事件（24 条）
    downtime_templates = [
        ("EQ001", "DR_MECH_SEAL", "机动", "高", "进料泵机械密封泄漏，切换备用泵"),
        ("EQ002", "DR_MECH_BEAR", "机动", "高", "压缩机推力轴承温度超限停机检查"),
        ("EQ002", "DR_PLAN", "机动", "中", "压缩机年度大修"),
        ("EQ003", "DR_PROC", "生产", "高", "塔顶温度波动，降负荷运行后恢复"),
        ("EQ003", "DR_INST", "仪表", "中", "塔釜液位仪表故障导致联锁"),
        ("EQ004", "DR_MECH", "机动", "低", "回流泵振动偏大，紧固后恢复"),
        ("EQ004", "DR_ELEC", "电气", "中", "电机保护动作，检查接线"),
        ("EQ005", "DR_PROC", "生产", "高", "反应器催化剂活性下降，计划降负荷"),
        ("EQ005", "DR_PLAN", "机动", "中", "反应釜计划停车更换催化剂"),
        ("EQ006", "DR_MECH", "机动", "高", "循环氢压缩机喘振保护停机"),
        ("EQ006", "DR_ELEC", "电气", "中", "变频器故障"),
        ("EQ007", "DR_INST", "仪表", "低", "塔顶压力变送器漂移"),
        ("EQ007", "DR_EXT", "生产", "中", "上游来料中断导致降负荷"),
        ("EQ008", "DR_MECH_BEAR", "机动", "中", "输送泵轴承异响更换"),
        ("EQ001", "DR_PLAN", "机动", "中", "泵体计划保养"),
        ("EQ002", "DR_INST", "仪表", "低", "振动探头校验"),
        ("EQ003", "DR_PLAN", "机动", "高", "精馏塔计划停车检修"),
        ("EQ005", "DR_MECH", "机动", "中", "搅拌器密封更换"),
        ("EQ006", "DR_PLAN", "机动", "高", "压缩机计划检修"),
        ("EQ001", "DR_ELEC", "电气", "低", "软启动器参数复位"),
        ("EQ004", "DR_PLAN", "机动", "中", "回流泵计划保养"),
        ("EQ008", "DR_PROC", "生产", "低", "输送量不足工艺调整"),
        ("EQ006", "DR_EXT", "生产", "中", "电网波动引起停机"),
        ("EQ007", "DR_MECH", "机动", "中", "再沸器管束泄漏排查"),
    ]

    downtime_rows = []
    base_dt = datetime(2025, 2, 10, 8, 0, 0)
    for idx, (eq_id, reason_id, dept, impact, desc) in enumerate(downtime_templates):
        eq = eq_map[eq_id]
        reason = reason_map[reason_id]
        start_dt = base_dt + timedelta(days=idx * 18, hours=random.randint(0, 8))
        duration = random.uniform(60, 480) if reason["is_planned"] == 0 else random.uniform(240, 1440)
        end_dt = start_dt + timedelta(minutes=duration)
        event_date = start_dt.date()

        downtime_rows.append({
            "event_id": f"DT{idx + 1:04d}",
            "date_key": _date_key(event_date),
            "equipment_id": eq_id,
            "equipment_code": eq["equipment_code"],
            "equipment_name": eq["equipment_name"],
            "plant_id": eq["plant_id"],
            "unit_id": eq["unit_id"],
            "reason_id": reason_id,
            "reason_code": reason["reason_code"],
            "reason_name": reason["reason_name"],
            "reason_category": reason["reason_category"],
            "is_planned": reason["is_planned"],
            "start_time": start_dt,
            "end_time": end_dt,
            "duration_min": round(duration, 1),
            "impact_level": impact,
            "responsible_dept": dept,
            "description": desc,
            "created_at": start_dt,
        })

    dt_inserted = s.sql.insert_rows("fact_downtime_event", downtime_rows)
    output.print(f"OK fact_downtime_event 插入 {dt_inserted} 行")

    # 8. 维保记录（16 条）
    maint_templates = [
        ("EQ001", "预防", "完成", 1, 8, 7.5, 12000, 11500),
        ("EQ002", "预测", "完成", 1, 24, 22, 85000, 82000),
        ("EQ002", "大修", "完成", 1, 72, 68, 320000, 305000),
        ("EQ003", "预防", "完成", 0, 16, 18, 45000, 48000),
        ("EQ003", "故障维修", "完成", 1, 12, 10, 28000, 26500),
        ("EQ004", "预防", "完成", 1, 6, 5.5, 8000, 7800),
        ("EQ005", "预测", "完成", 1, 20, 19, 65000, 63000),
        ("EQ005", "大修", "进行中", 0, 48, 0, 180000, 0),
        ("EQ006", "预防", "完成", 1, 18, 17, 55000, 54000),
        ("EQ006", "故障维修", "完成", 1, 10, 12, 35000, 38000),
        ("EQ007", "预防", "逾期", 0, 8, 0, 12000, 0),
        ("EQ007", "预防", "计划", 0, 8, 0, 12000, 0),
        ("EQ008", "预防", "完成", 1, 6, 6, 9000, 9200),
        ("EQ001", "故障维修", "完成", 1, 4, 3.5, 6000, 5800),
        ("EQ004", "预测", "完成", 1, 10, 9, 15000, 14500),
        ("EQ008", "故障维修", "完成", 0, 5, 6, 7500, 8200),
    ]

    maint_rows = []
    maint_base = date(2025, 3, 1)
    for idx, (eq_id, mtype, status, on_sched, plan_h, act_h, plan_c, act_c) in enumerate(maint_templates):
        eq = eq_map[eq_id]
        plan_d = maint_base + timedelta(days=idx * 25)
        actual_d = plan_d + timedelta(days=random.randint(-2, 3)) if status in ("完成", "逾期") and act_h > 0 else None
        if status == "逾期":
            actual_d = None
        dk = _date_key(actual_d or plan_d)

        maint_rows.append({
            "maint_id": f"MR{idx + 1:04d}",
            "date_key": dk,
            "equipment_id": eq_id,
            "equipment_code": eq["equipment_code"],
            "plant_id": eq["plant_id"],
            "unit_id": eq["unit_id"],
            "maint_type": mtype,
            "plan_date": plan_d,
            "actual_date": actual_d,
            "plan_hours": float(plan_h),
            "actual_hours": float(act_h),
            "plan_cost": float(plan_c),
            "actual_cost": float(act_c),
            "status": status,
            "is_on_schedule": on_sched,
            "vendor": "机动科自营" if mtype != "大修" else "外委-石化检修",
            "description": f"{eq['equipment_name']}{mtype}作业",
            "created_at": datetime.combine(plan_d, datetime.min.time()),
        })

    maint_inserted = s.sql.insert_rows("fact_maintenance_record", maint_rows)
    output.print(f"OK fact_maintenance_record 插入 {maint_inserted} 行")

    # 9. 2026 年 6 月运行计划
    plan_rows = []
    plan_month_start = date(2026, 6, 1)
    dk_june = _date_key(plan_month_start)
    month_runtime = 30 * 1440 * 0.92

    for idx, eq in enumerate(equipment):
        planned_rt = round(month_runtime * random.uniform(0.88, 0.95), 1)
        planned_out = round(planned_rt * eq["ideal_cycle_rate"] * random.uniform(0.94, 1.0), 2)
        planned_energy = round(eq["energy_base"] * 30 * random.uniform(0.9, 1.05), 2)
        plan_rows.append({
            "plan_id": f"PLN202606{idx + 1:03d}",
            "date_key": dk_june,
            "equipment_id": eq["equipment_id"],
            "equipment_code": eq["equipment_code"],
            "plant_id": eq["plant_id"],
            "unit_id": eq["unit_id"],
            "plan_version": _PLAN_VERSION,
            "fiscal_year": 2026,
            "fiscal_month": 6,
            "planned_runtime_min": planned_rt,
            "planned_output_qty": planned_out,
            "planned_energy": planned_energy,
            "output_unit": eq["output_unit"],
            "status": "已发布",
            "created_at": datetime(2026, 5, 25, 0, 0, 0),
        })

    plan_inserted = s.sql.insert_rows("fact_equipment_plan", plan_rows)
    output.print(f"OK fact_equipment_plan 插入 {plan_inserted} 行")

    summary = {
        "ok": True,
        "space_id": space_id,
        "plants": len(plants),
        "units": len(units),
        "equip_types": len(equip_types),
        "equipment": len(equipment),
        "reasons": len(reasons),
        "ops_inserted": ops_inserted,
        "downtime_inserted": dt_inserted,
        "maint_inserted": maint_inserted,
        "plan_inserted": plan_inserted,
    }
    output.success("灌数完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))
