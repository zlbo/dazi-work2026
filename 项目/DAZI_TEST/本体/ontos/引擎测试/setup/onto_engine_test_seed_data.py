"""本体引擎测试空间灌数 — space__onto_engine_test

前置：onto_engine_test_ontology_init.py
幂等：fact_cost 已有数据则跳过；若仅有部分表有数据（历史 INSERT 失败残留），先 TRUNCATE 再灌。
"""

import json
from datetime import date, datetime, timedelta

_SEED_DT = datetime(2025, 1, 1, 0, 0, 0)

_SEED_TABLES = (
    "fact_cost",
    "fact_output",
    "dim_project",
    "dim_cost_type",
    "dim_org",
    "dim_date",
)


def _date_key(d):
    return int(d.strftime("%Y%m%d"))


def _count_table(s, table):
    try:
        return int(s.sql.query_one(f"SELECT count() FROM {table}") or 0)
    except Exception:
        return 0


def _truncate_seed_tables(s):
    """清理半灌残留（如 dim_date 重复、事实表为空）。"""
    for tbl in _SEED_TABLES:
        s.sql.execute(f"TRUNCATE TABLE IF EXISTS {tbl}")


def main():
    space_id = "space__onto_engine_test"
    s = space.get(space_id)
    output.print("=== 本体引擎测试空间灌数 ===")

    fact_n = _count_table(s, "fact_cost")
    if fact_n > 0:
        output.print(f"fact_cost 已有 {fact_n} 行，跳过灌数")
        output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "skipped": True}, ensure_ascii=True))
        return

    partial = any(_count_table(s, t) > 0 for t in _SEED_TABLES)
    if partial:
        output.print("检测到半灌残留，先 TRUNCATE 六张表…")
        _truncate_seed_tables(s)

    # 1. dim_date（2025-01 ~ 2026-06）
    output.print("\n[1/6] 灌入 dim_date...")
    dim_date_rows = []
    cur = date(2025, 1, 1)
    end = date(2026, 6, 30)
    while cur <= end:
        dim_date_rows.append({
            "date_key": _date_key(cur),
            "calendar_date": cur,
            "year": cur.year,
            "quarter": (cur.month - 1) // 3 + 1,
            "month": cur.month,
            "week_of_year": cur.isocalendar()[1],
            "day_of_week": cur.weekday(),
            "is_weekend": 1 if cur.weekday() >= 5 else 0,
            "year_month": cur.strftime("%Y-%m"),
        })
        cur += timedelta(days=1)
    s.sql.insert_rows("dim_date", dim_date_rows)
    output.print(f"OK dim_date {len(dim_date_rows)} 行")

    # 2. dim_org（1 公司 + 2 分公司 + 4 项目部）
    output.print("\n[2/6] 灌入 dim_org...")
    orgs = [
        {"org_id": "ORG_CO", "org_code": "CO", "org_name": "搭子建设集团",
         "parent_org_id": "", "org_level": 1, "status": "启用"},
        {"org_id": "ORG_HD", "org_code": "HD", "org_name": "华东分公司",
         "parent_org_id": "ORG_CO", "org_level": 2, "status": "启用"},
        {"org_id": "ORG_HB", "org_code": "HB", "org_name": "华北分公司",
         "parent_org_id": "ORG_CO", "org_level": 2, "status": "启用"},
        {"org_id": "ORG_HN", "org_code": "HN", "org_name": "华南分公司",
         "parent_org_id": "ORG_CO", "org_level": 2, "status": "启用"},
        {"org_id": "ORG_P1", "org_code": "P1", "org_name": "浦东项目部",
         "parent_org_id": "ORG_HD", "org_level": 3, "status": "启用"},
        {"org_id": "ORG_P2", "org_code": "P2", "org_name": "虹桥项目部",
         "parent_org_id": "ORG_HD", "org_level": 3, "status": "启用"},
        {"org_id": "ORG_P3", "org_code": "P3", "org_name": "京沪项目部",
         "parent_org_id": "ORG_HB", "org_level": 3, "status": "启用"},
        {"org_id": "ORG_P4", "org_code": "P4", "org_name": "津滨项目部",
         "parent_org_id": "ORG_HB", "org_level": 3, "status": "启用"},
        {"org_id": "ORG_P5", "org_code": "P5", "org_name": "广深项目部",
         "parent_org_id": "ORG_HN", "org_level": 3, "status": "启用"},
        {"org_id": "ORG_P6", "org_code": "P6", "org_name": "深中项目部",
         "parent_org_id": "ORG_HN", "org_level": 3, "status": "启用"},
    ]
    org_rows = [
        {
            "org_id": o["org_id"],
            "org_code": o["org_code"],
            "org_name": o["org_name"],
            "parent_org_id": o["parent_org_id"],
            "org_level": o["org_level"],
            "status": o["status"],
            "created_at": _SEED_DT,
        }
        for o in orgs
    ]
    s.sql.insert_rows("dim_org", org_rows)
    output.print(f"OK dim_org {len(org_rows)} 行")

    # 3. dim_cost_type（2 大类 + 4 子类）
    output.print("\n[3/6] 灌入 dim_cost_type...")
    cost_types = [
        {"cost_type_id": "CT_LAB", "cost_type_code": "LAB", "cost_type_name": "人工费",
         "parent_type_id": "", "status": "启用"},
        {"cost_type_id": "CT_MAT", "cost_type_code": "MAT", "cost_type_name": "材料费",
         "parent_type_id": "", "status": "启用"},
        {"cost_type_id": "CT_LAB_WAGE", "cost_type_code": "WAGE", "cost_type_name": "工资",
         "parent_type_id": "CT_LAB", "status": "启用"},
        {"cost_type_id": "CT_LAB_OT", "cost_type_code": "OT", "cost_type_name": "加班费",
         "parent_type_id": "CT_LAB", "status": "启用"},
        {"cost_type_id": "CT_MAT_STEEL", "cost_type_code": "STEEL", "cost_type_name": "钢材",
         "parent_type_id": "CT_MAT", "status": "启用"},
        {"cost_type_id": "CT_MAT_CONC", "cost_type_code": "CONC", "cost_type_name": "混凝土",
         "parent_type_id": "CT_MAT", "status": "启用"},
    ]
    type_rows = [
        {
            "cost_type_id": ct["cost_type_id"],
            "cost_type_code": ct["cost_type_code"],
            "cost_type_name": ct["cost_type_name"],
            "parent_type_id": ct["parent_type_id"],
            "status": ct["status"],
            "created_at": _SEED_DT,
        }
        for ct in cost_types
    ]
    s.sql.insert_rows("dim_cost_type", type_rows)
    output.print(f"OK dim_cost_type {len(type_rows)} 行")

    # 4. dim_project（6 项目，成本梯度唯一可判）
    output.print("\n[4/6] 灌入 dim_project...")
    projects = [
        {"project_id": "PRJ01", "project_code": "P-001", "project_name": "浦东大桥改造",
         "region": "华东", "project_type": "桥梁", "org_id": "ORG_P1", "org_name": "浦东项目部",
         "cost_base": 50000},
        {"project_id": "PRJ02", "project_code": "P-002", "project_name": "虹桥枢纽配套",
         "region": "华东", "project_type": "市政", "org_id": "ORG_P2", "org_name": "虹桥项目部",
         "cost_base": 40000},
        {"project_id": "PRJ03", "project_code": "P-003", "project_name": "京沪线维护",
         "region": "华北", "project_type": "铁路", "org_id": "ORG_P3", "org_name": "京沪项目部",
         "cost_base": 35000},
        {"project_id": "PRJ04", "project_code": "P-004", "project_name": "津滨高速段",
         "region": "华北", "project_type": "公路", "org_id": "ORG_P4", "org_name": "津滨项目部",
         "cost_base": 30000},
        {"project_id": "PRJ05", "project_code": "P-005", "project_name": "广深城际段",
         "region": "华南", "project_type": "铁路", "org_id": "ORG_P5", "org_name": "广深项目部",
         "cost_base": 25000},
        {"project_id": "PRJ06", "project_code": "P-006", "project_name": "深中通道试验",
         "region": "华南", "project_type": "桥梁", "org_id": "ORG_P6", "org_name": "深中项目部",
         "cost_base": 20000},
    ]
    project_rows = [
        {
            "project_id": p["project_id"],
            "project_code": p["project_code"],
            "project_name": p["project_name"],
            "region": p["region"],
            "project_type": p["project_type"],
            "org_id": p["org_id"],
            "org_name": p["org_name"],
            "status": "在建",
            "created_at": _SEED_DT,
        }
        for p in projects
    ]
    s.sql.insert_rows("dim_project", project_rows)
    output.print(f"OK dim_project {len(project_rows)} 行")

    # 5. fact_cost（~6项目×18月×2科目 ≈ 216 行，确定性金额）
    output.print("\n[5/6] 灌入 fact_cost...")
    parent_map = {o["org_id"]: o["parent_org_id"] for o in orgs}
    type_parent = {ct["cost_type_id"]: ct["parent_type_id"] for ct in cost_types}
    leaf_types = [ct for ct in cost_types if ct["parent_type_id"]]
    cost_rows = []
    cid = 0
    month_start = date(2025, 1, 1)
    months = []
    while month_start <= date(2026, 6, 1):
        months.append(month_start)
        if month_start.month == 12:
            month_start = date(month_start.year + 1, 1, 1)
        else:
            month_start = date(month_start.year, month_start.month + 1, 1)

    for mi, m in enumerate(months):
        dk = _date_key(m)
        for p in projects:
            for ct in leaf_types[:2]:  # 每项目每月 2 个子科目
                cid += 1
                base = p["cost_base"] * (1 + mi * 0.02)
                amount = base * (1.0 if ct["cost_type_code"] == "WAGE" else 0.6)
                # 华东项目近月超支（budget_exec_rate > 1）
                if p["region"] == "华东" and mi >= len(months) - 3:
                    budget = amount * 0.75
                else:
                    budget = amount * 1.1
                cost_rows.append({
                    "cost_id": f"C{cid:05d}",
                    "date_key": dk,
                    "project_id": p["project_id"],
                    "project_name": p["project_name"],
                    "region": p["region"],
                    "org_id": p["org_id"],
                    "org_name": p["org_name"],
                    "parent_org_id": parent_map.get(p["org_id"], ""),
                    "cost_type_id": ct["cost_type_id"],
                    "cost_type_name": ct["cost_type_name"],
                    "parent_cost_type_id": type_parent.get(ct["cost_type_id"], ""),
                    "cost_amount": round(amount, 2),
                    "budget_amount": round(budget, 2),
                    "created_at": _SEED_DT,
                })
    s.sql.insert_rows("fact_cost", cost_rows)
    output.print(f"OK fact_cost {len(cost_rows)} 行")

    # 6. fact_output（部分月缺失，~96 行）
    output.print("\n[6/6] 灌入 fact_output...")
    out_rows = []
    oid = 0
    for mi, m in enumerate(months):
        if mi % 3 == 2:  # 每季末月跳过部分项目
            skip = {"PRJ03", "PRJ06"}
        else:
            skip = set()
        dk = _date_key(m)
        for p in projects:
            if p["project_id"] in skip:
                continue
            oid += 1
            out_rows.append({
                "output_id": f"O{oid:05d}",
                "date_key": dk,
                "project_id": p["project_id"],
                "project_name": p["project_name"],
                "region": p["region"],
                "org_id": p["org_id"],
                "output_amount": round(p["cost_base"] * 1.3 * (1 + mi * 0.01), 2),
                "created_at": _SEED_DT,
            })
    s.sql.insert_rows("fact_output", out_rows)
    output.print(f"OK fact_output {len(out_rows)} 行")

    # 写入后校验
    verify = {t: _count_table(s, t) for t in _SEED_TABLES}
    output.print(f"校验行数: {verify}")

    summary = {
        "ok": True,
        "dim_date": verify.get("dim_date", 0),
        "dim_org": verify.get("dim_org", 0),
        "dim_project": verify.get("dim_project", 0),
        "fact_cost": verify.get("fact_cost", 0),
        "fact_output": verify.get("fact_output", 0),
    }
    output.success("灌数完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True))
