"""利润分析01 灌数 — space__onto_engine_test

前置：profit01_ontology_init.py；引擎测试 seed 已灌 fact_cost / fact_output。
幂等：dim_account 已有数据则跳过。
"""

import json
from datetime import datetime

SPACE_ID = "space__onto_engine_test"
_SEED_DT = datetime(2025, 1, 1, 0, 0, 0)
_BUDGET_VERSION = "2025年度预算"
_BUDGET_ID = "BUD2025"


def _count(s, table):
    try:
        return int(s.sql.query_one(f"SELECT count() AS n FROM {table}") or 0)
    except Exception:
        return 0


def _month_date_key(year, month):
    return year * 10000 + month * 100 + 1


def main():
    s = space.get(SPACE_ID)
    output.print("=== 利润分析01 灌数 ===")

    if _count(s, "dim_account") > 0:
        output.print("dim_account 已有数据，跳过灌数")
        output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "skipped": True}, ensure_ascii=True))
        return

    if _count(s, "fact_cost") == 0:
        output.print("WARN fact_cost 为空，请先运行引擎测试 seed")
        return

    # 1. dim_account
    output.print("\n[1/5] 灌入 dim_account...")
    accounts = [
        {"account_id": "ACC_REV", "account_code": "6000", "account_name": "营业收入",
         "account_type": "收入", "pl_category": "营业收入", "parent_account_id": "",
         "account_level": 1, "is_leaf": 0, "normal_balance": "贷", "status": "启用"},
        {"account_id": "ACC_REV01", "account_code": "6001", "account_name": "工程收入",
         "account_type": "收入", "pl_category": "营业收入", "parent_account_id": "ACC_REV",
         "account_level": 2, "is_leaf": 1, "normal_balance": "贷", "status": "启用"},
        {"account_id": "ACC_COST", "account_code": "6400", "account_name": "营业成本",
         "account_type": "成本", "pl_category": "营业成本", "parent_account_id": "",
         "account_level": 1, "is_leaf": 0, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC_COST01", "account_code": "6401", "account_name": "人工成本",
         "account_type": "成本", "pl_category": "营业成本", "parent_account_id": "ACC_COST",
         "account_level": 2, "is_leaf": 1, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC_COST02", "account_code": "6402", "account_name": "材料费",
         "account_type": "成本", "pl_category": "营业成本", "parent_account_id": "ACC_COST",
         "account_level": 2, "is_leaf": 1, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC_EXP", "account_code": "6600", "account_name": "期间费用",
         "account_type": "费用", "pl_category": "期间费用", "parent_account_id": "",
         "account_level": 1, "is_leaf": 0, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC_EXP01", "account_code": "6601", "account_name": "管理费用",
         "account_type": "费用", "pl_category": "期间费用", "parent_account_id": "ACC_EXP",
         "account_level": 2, "is_leaf": 1, "normal_balance": "借", "status": "启用"},
    ]
    acc_rows = [{**a, "created_at": _SEED_DT} for a in accounts]
    s.sql.insert_rows("dim_account", acc_rows)
    output.print(f"OK dim_account {len(acc_rows)} 行")

    # 2. bridge
    output.print("\n[2/5] 灌入 bridge_cost_type_account...")
    bridge = [
        ("CT_LAB", "ACC_COST01"), ("CT_LAB_WAGE", "ACC_COST01"), ("CT_LAB_OT", "ACC_COST01"),
        ("CT_MAT", "ACC_COST02"), ("CT_MAT_CONC", "ACC_COST02"), ("CT_MAT_STEEL", "ACC_COST02"),
    ]
    bridge_rows = [{
        "cost_type_id": ct,
        "account_id": acc,
        "mapping_type": "默认",
        "effective_from": _SEED_DT.date(),
        "created_at": _SEED_DT,
    } for ct, acc in bridge]
    s.sql.insert_rows("bridge_cost_type_account", bridge_rows)
    output.print(f"OK bridge {len(bridge_rows)} 行")

    # 预聚合 actual（供 fact_pl_budget.actual_amount）
    output_rows = s.sql.query("""
        SELECT project_id, intDiv(date_key, 100) AS ym, sum(output_amount) AS amt
        FROM fact_output GROUP BY project_id, ym
    """) or []
    rev_map = {(r["project_id"], int(r["ym"])): float(r.get("amt") or 0) for r in output_rows}

    cost_rows_raw = s.sql.query("""
        SELECT c.project_id, intDiv(c.date_key, 100) AS ym, b.account_id,
               sum(c.cost_amount) AS amt
        FROM fact_cost c
        INNER JOIN bridge_cost_type_account b ON c.cost_type_id = b.cost_type_id
        GROUP BY c.project_id, ym, b.account_id
    """) or []
    cost_map = {
        (r["project_id"], int(r["ym"]), r["account_id"]): float(r.get("amt") or 0)
        for r in cost_rows_raw
    }

    # 3. fact_pl_budget（6 项目 × 12 期 × 末级科目）
    output.print("\n[3/5] 灌入 fact_pl_budget...")
    projects = s.sql.query(
        "SELECT project_id, project_name, org_id, org_name, region FROM dim_project ORDER BY project_id"
    ) or []
    budget_accounts = [a for a in accounts if a["is_leaf"] == 1]
    pl_rows = []
    line_no = 0
    for proj in projects:
        pid = proj["project_id"]
        for month in range(1, 13):
            dk = _month_date_key(2025, month)
            ym = dk // 100
            for acc in budget_accounts:
                line_no += 1
                base = 80000 if acc["account_type"] == "收入" else 50000
                if acc["account_type"] == "费用":
                    base = 8000
                amt = base * (1 + (line_no % 5) * 0.02)
                if acc["account_type"] == "收入":
                    actual = rev_map.get((pid, ym), 0.0)
                elif acc["account_type"] == "成本":
                    actual = cost_map.get((pid, ym, acc["account_id"]), 0.0)
                else:
                    actual = 0.0
                pl_rows.append({
                    "budget_id": _BUDGET_ID,
                    "line_id": f"PL{line_no:06d}",
                    "date_key": dk,
                    "fiscal_year": 2025,
                    "fiscal_period": month,
                    "budget_version": _BUDGET_VERSION,
                    "project_id": pid,
                    "project_name": proj.get("project_name", ""),
                    "org_id": proj.get("org_id", ""),
                    "org_name": proj.get("org_name", ""),
                    "region": proj.get("region", ""),
                    "account_id": acc["account_id"],
                    "account_code": acc["account_code"],
                    "account_name": acc["account_name"],
                    "account_type": acc["account_type"],
                    "pl_category": acc["pl_category"],
                    "budget_amount": round(amt, 2),
                    "actual_amount": round(actual, 2),
                    "currency": "CNY",
                    "status": "已发布",
                    "created_at": _SEED_DT,
                })
    s.sql.insert_rows("fact_pl_budget", pl_rows)
    output.print(f"OK fact_pl_budget {len(pl_rows)} 行")

    # 4. fact_project_profit 物化
    output.print("\n[4/5] 灌入 fact_project_profit...")
    profit_rows_raw = s.sql.query("""
        SELECT
            p.project_id,
            p.project_name,
            p.region,
            p.org_id,
            p.org_name,
            intDiv(o.date_key, 100) AS ym,
            sum(o.output_amount) AS revenue,
            coalesce(c.total_cost, 0) AS cost
        FROM dim_project p
        INNER JOIN fact_output o ON p.project_id = o.project_id
        LEFT JOIN (
            SELECT project_id, intDiv(date_key, 100) AS ym, sum(cost_amount) AS total_cost
            FROM fact_cost
            GROUP BY project_id, ym
        ) c ON p.project_id = c.project_id AND intDiv(o.date_key, 100) = c.ym
        GROUP BY p.project_id, p.project_name, p.region, p.org_id, p.org_name, ym, c.total_cost
        ORDER BY ym, p.project_id
    """) or []
    profit_rows = []
    for i, row in enumerate(profit_rows_raw):
        ym = int(row.get("ym") or 202501)
        year, month = ym // 100, ym % 100
        dk = _month_date_key(year, month)
        rev = float(row.get("revenue") or 0)
        cost = float(row.get("cost") or 0)
        gp = rev - cost
        margin = gp / rev if rev > 0 else 0
        profit_rows.append({
            "profit_id": f"PP{i + 1:06d}",
            "date_key": dk,
            "year": year,
            "month": month,
            "year_month": f"{year}-{month:02d}",
            "fiscal_year": year,
            "fiscal_period": month,
            "project_id": row.get("project_id", ""),
            "project_name": row.get("project_name", ""),
            "region": row.get("region", ""),
            "org_id": row.get("org_id", ""),
            "org_name": row.get("org_name", ""),
            "revenue": round(rev, 2),
            "cost": round(cost, 2),
            "gross_profit": round(gp, 2),
            "profit_margin": round(margin, 4),
            "created_at": _SEED_DT,
        })
    if profit_rows:
        s.sql.insert_rows("fact_project_profit", profit_rows)
    output.print(f"\n[5/5] OK fact_project_profit {len(profit_rows)} 行")

    summary = {
        "ok": True,
        "dim_account": len(acc_rows),
        "bridge": len(bridge_rows),
        "fact_pl_budget": len(pl_rows),
        "fact_project_profit": len(profit_rows),
    }
    output.success("利润分析01 灌数完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True))
