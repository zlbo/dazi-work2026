"""利润分析演示数据灌入 — space__misc_01

前置：先执行 profit_ontology_init.py 建表。
幂等：fact_gl_journal_entry 已有数据则跳过。

放置：项目/DAZI_TEST/本体/ontos/利润分析示例/setup/profit_seed_data.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润分析示例/setup/profit_seed_data.py --space space__misc_01 --type data
"""

import json
import random
from datetime import date, datetime, timedelta

_SEED_DT = datetime(2025, 1, 1, 0, 0, 0)
_BUDGET_VERSION = "2026年度预算"


def _calc_signed(account_type, debit, credit):
    if account_type == "收入":
        return round(credit - debit, 2)
    if account_type in ("成本", "费用"):
        return round(debit - credit, 2)
    return round(debit - credit, 2)


def _make_entry_line(seq, posting_date, account, cc, amount):
    account_type = account["account_type"]
    debit = amount if account_type in ("成本", "费用") else 0.0
    credit = amount if account_type == "收入" else 0.0
    if account_type == "收入":
        debit, credit = 0.0, amount
    signed = _calc_signed(account_type, debit, credit)
    fy = posting_date.year
    fp = posting_date.month
    entry_id = f"JE{posting_date.strftime('%Y%m%d')}{seq // 10:04d}"
    line_id = f"JL{posting_date.strftime('%Y%m%d')}{seq:05d}"
    date_key = int(posting_date.strftime("%Y%m%d"))
    return {
        "entry_id": entry_id,
        "line_id": line_id,
        "date_key": date_key,
        "posting_date": posting_date,
        "fiscal_year": fy,
        "fiscal_period": fp,
        "account_id": account["account_id"],
        "account_code": account["account_code"],
        "account_name": account["account_name"],
        "account_type": account["account_type"],
        "pl_category": account["pl_category"],
        "account_level": account["account_level"],
        "cost_center_id": cc["cost_center_id"],
        "cost_center_name": cc["cost_center_name"],
        "department": cc["department"],
        "profit_center": cc["profit_center"],
        "debit_amount": round(debit, 2),
        "credit_amount": round(credit, 2),
        "amount_signed": signed,
        "currency": "CNY",
        "voucher_no": f"V{posting_date.strftime('%Y%m')}{seq:04d}",
        "source_system": "GL",
        "description": f"{account['account_name']}-{cc['cost_center_name']}",
        "created_at": datetime.combine(posting_date, datetime.min.time()),
    }


def main():
    space_id = "space__misc_01"
    s = space.get(space_id)

    output.print("=== 利润分析演示数据灌入 ===")

    try:
        n = int(s.sql.query_one("SELECT count() FROM fact_gl_journal_entry") or 0)
    except Exception:
        n = 0
    if n > 0:
        output.print(f"fact_gl_journal_entry 已有 {n} 行，跳过灌数")
        output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "skipped": True, "rows": n}, ensure_ascii=True))
        return

    accounts = [
        {"account_id": "ACC6000", "account_code": "6000", "account_name": "营业收入", "account_type": "收入", "pl_category": "营业收入", "parent_account_id": "", "account_level": 1, "is_leaf": False, "normal_balance": "贷", "status": "启用"},
        {"account_id": "ACC6001", "account_code": "6001", "account_name": "主营业务收入", "account_type": "收入", "pl_category": "营业收入", "parent_account_id": "ACC6000", "account_level": 2, "is_leaf": True, "normal_balance": "贷", "status": "启用"},
        {"account_id": "ACC6050", "account_code": "6050", "account_name": "其他业务收入", "account_type": "收入", "pl_category": "营业收入", "parent_account_id": "ACC6000", "account_level": 2, "is_leaf": True, "normal_balance": "贷", "status": "启用"},
        {"account_id": "ACC6400", "account_code": "6400", "account_name": "营业成本", "account_type": "成本", "pl_category": "营业成本", "parent_account_id": "", "account_level": 1, "is_leaf": False, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC6401", "account_code": "6401", "account_name": "主营业务成本", "account_type": "成本", "pl_category": "营业成本", "parent_account_id": "ACC6400", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC6402", "account_code": "6402", "account_name": "原材料成本", "account_type": "成本", "pl_category": "营业成本", "parent_account_id": "ACC6400", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC6600", "account_code": "6600", "account_name": "期间费用", "account_type": "费用", "pl_category": "期间费用", "parent_account_id": "", "account_level": 1, "is_leaf": False, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC6601", "account_code": "6601", "account_name": "销售费用", "account_type": "费用", "pl_category": "期间费用", "parent_account_id": "ACC6600", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC6602", "account_code": "6602", "account_name": "管理费用", "account_type": "费用", "pl_category": "期间费用", "parent_account_id": "ACC6600", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC6603", "account_code": "6603", "account_name": "财务费用", "account_type": "费用", "pl_category": "期间费用", "parent_account_id": "ACC6600", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
    ]
    for a in accounts:
        a["created_at"] = _SEED_DT

    cost_centers = [
        {"cost_center_id": "CC01", "cost_center_code": "PC-PROD", "cost_center_name": "生产中心", "department": "生产部", "company_code": "PD", "profit_center": "制造利润中心", "status": "启用"},
        {"cost_center_id": "CC02", "cost_center_code": "PC-SALE", "cost_center_name": "销售中心", "department": "销售部", "company_code": "PD", "profit_center": "销售利润中心", "status": "启用"},
        {"cost_center_id": "CC03", "cost_center_code": "PC-MGMT", "cost_center_name": "管理中心", "department": "管理部", "company_code": "PD", "profit_center": "管理利润中心", "status": "启用"},
        {"cost_center_id": "CC04", "cost_center_code": "PC-RD", "cost_center_name": "研发中心", "department": "研发部", "company_code": "PD", "profit_center": "研发利润中心", "status": "启用"},
        {"cost_center_id": "CC05", "cost_center_code": "PC-FIN", "cost_center_name": "财务中心", "department": "财务部", "company_code": "PD", "profit_center": "财务利润中心", "status": "启用"},
    ]
    for c in cost_centers:
        c["created_at"] = _SEED_DT

    s.sql.insert_rows("dim_account", accounts)
    s.sql.insert_rows("dim_cost_center", cost_centers)
    output.print("OK 维表数据")

    leaf_accounts = [a for a in accounts if a["is_leaf"]]
    acct_dict = {a["account_id"]: a for a in accounts}
    cc_dict = {c["cost_center_id"]: c for c in cost_centers}

    random.seed(9520)
    fact_rows = []
    seq = 1
    start = date(2025, 1, 1)
    end = date(2026, 6, 30)

    base_amounts = {
        "ACC6001": 800000,
        "ACC6050": 50000,
        "ACC6401": 480000,
        "ACC6402": 120000,
        "ACC6601": 80000,
        "ACC6602": 60000,
        "ACC6603": 20000,
    }

    d = start
    while d <= end:
        if d.day <= 3:
            for acc_id, base in base_amounts.items():
                account = acct_dict[acc_id]
                for cc in cost_centers:
                    if account["account_type"] == "收入" and cc["cost_center_id"] not in ("CC01", "CC02"):
                        continue
                    if account["account_type"] == "成本" and cc["cost_center_id"] not in ("CC01", "CC04"):
                        continue
                    if account["account_type"] == "费用":
                        if account["account_id"] == "ACC6601" and cc["cost_center_id"] != "CC02":
                            continue
                        if account["account_id"] == "ACC6602" and cc["cost_center_id"] not in ("CC03", "CC04"):
                            continue
                        if account["account_id"] == "ACC6603" and cc["cost_center_id"] != "CC05":
                            continue
                    jitter = random.uniform(0.85, 1.15)
                    seasonal = 1.0 + 0.1 * ((d.month - 1) % 3)
                    amount = round(base * jitter * seasonal / max(len(cost_centers), 1) / 3, 2)
                    if amount <= 0:
                        continue
                    fact_rows.append(_make_entry_line(seq, d, account, cc, amount))
                    seq += 1
        d += timedelta(days=1)

    inserted = s.sql.insert_rows("fact_gl_journal_entry", fact_rows)
    output.print(f"OK 实际分录表插入 {inserted} 行")

    budget_rows = []
    bseq = 1
    for year in (2025, 2026):
        version = _BUDGET_VERSION if year == 2026 else f"{year}年度预算"
        for period in range(1, 13):
            if year == 2026 and period > 6:
                continue
            for account in leaf_accounts:
                base = base_amounts.get(account["account_id"], 50000)
                for cc in cost_centers:
                    if account["account_type"] == "收入" and cc["cost_center_id"] not in ("CC01", "CC02"):
                        continue
                    if account["account_type"] == "成本" and cc["cost_center_id"] not in ("CC01", "CC04"):
                        continue
                    if account["account_type"] == "费用":
                        if account["account_id"] == "ACC6601" and cc["cost_center_id"] != "CC02":
                            continue
                        if account["account_id"] == "ACC6602" and cc["cost_center_id"] not in ("CC03", "CC04"):
                            continue
                        if account["account_id"] == "ACC6603" and cc["cost_center_id"] != "CC05":
                            continue
                    budget_amt = round(base / 6 * random.uniform(0.95, 1.05), 2)
                    date_key = int(f"{year}{period:02d}01")
                    budget_rows.append({
                        "budget_id": f"BUD{year}",
                        "line_id": f"BL{year}{period:02d}{bseq:05d}",
                        "date_key": date_key,
                        "budget_version": version,
                        "fiscal_year": year,
                        "fiscal_period": period,
                        "account_id": account["account_id"],
                        "account_code": account["account_code"],
                        "account_name": account["account_name"],
                        "account_type": account["account_type"],
                        "pl_category": account["pl_category"],
                        "cost_center_id": cc["cost_center_id"],
                        "cost_center_name": cc["cost_center_name"],
                        "department": cc["department"],
                        "budget_amount": budget_amt,
                        "currency": "CNY",
                        "status": "已发布",
                        "created_at": _SEED_DT,
                    })
                    bseq += 1

    binserted = s.sql.insert_rows("fact_budget_entry", budget_rows)
    output.print(f"OK 预算表插入 {binserted} 行")

    summary = {
        "ok": True,
        "space_id": space_id,
        "accounts": len(accounts),
        "cost_centers": len(cost_centers),
        "fact_inserted": inserted,
        "budget_inserted": binserted,
    }
    output.success("灌数完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))