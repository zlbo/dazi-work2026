"""利润成本分析演示数据灌入 — space_cate_test01

前置：先执行 profit_cost_ontology_init.py 建表。
幂等：fact_gl_journal_entry 已有数据则跳过。

放置：项目/DAZI_TEST/本体/ontos/利润成本分析/setup/profit_cost_seed_data.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/利润成本分析/setup/profit_cost_seed_data.py --space space_cate_test01 --type data
"""

import json
import random
from datetime import date, datetime, timedelta

_SEED_DT = datetime(2025, 1, 1, 0, 0, 0)
_BUDGET_VERSION = "2026年度预算"


def _calc_signed(account_type, debit, credit):
    """计算损益符号金额"""
    if account_type == "收入":
        return round(credit - debit, 2)
    if account_type in ("成本", "费用"):
        return round(debit - credit, 2)
    return round(debit - credit, 2)


def _make_entry_line(seq, posting_date, account, profit_item, cost_item, cc, amount):
    """生成分录行"""
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
        "profit_item_id": profit_item["profit_item_id"] if profit_item else "",
        "profit_item_name": profit_item["profit_item_name"] if profit_item else "",
        "cost_item_id": cost_item["cost_item_id"] if cost_item else "",
        "cost_item_name": cost_item["cost_item_name"] if cost_item else "",
        "cost_center_id": cc["cost_center_id"],
        "cost_center_name": cc["cost_center_name"],
        "department": cc["department"],
        "debit_amount": round(debit, 2),
        "credit_amount": round(credit, 2),
        "amount_signed": signed,
        "currency": "CNY",
        "voucher_no": f"V{posting_date.strftime('%Y%m')}{seq:04d}",
        "description": f"{account['account_name']}-{cc['cost_center_name']}",
        "created_at": datetime.combine(posting_date, datetime.min.time()),
    }


def main():
    space_id = "space_cate_test01"
    s = space.get(space_id)

    output.print("=== 利润成本分析演示数据灌入 ===")

    # 检查是否已有数据
    try:
        n = int(s.sql.query_one("SELECT count() FROM fact_gl_journal_entry") or 0)
    except Exception:
        n = 0
    if n > 0:
        output.print(f"fact_gl_journal_entry 已有 {n} 行，跳过灌数")
        output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "skipped": True, "rows": n}, ensure_ascii=True))
        return

    # 1. 利润项主数据
    profit_items = [
        {"profit_item_id": "PI001", "profit_item_code": "PI001", "profit_item_name": "利润总额", "profit_item_type": "汇总", "parent_profit_item_id": "", "profit_item_level": 1, "is_leaf": False, "status": "启用"},
        {"profit_item_id": "PI002", "profit_item_code": "PI002", "profit_item_name": "主营业务利润", "profit_item_type": "主营", "parent_profit_item_id": "PI001", "profit_item_level": 2, "is_leaf": True, "status": "启用"},
        {"profit_item_id": "PI003", "profit_item_code": "PI003", "profit_item_name": "其他业务利润", "profit_item_type": "其他", "parent_profit_item_id": "PI001", "profit_item_level": 2, "is_leaf": True, "status": "启用"},
        {"profit_item_id": "PI004", "profit_item_code": "PI004", "profit_item_name": "营业外利润", "profit_item_type": "营业外", "parent_profit_item_id": "PI001", "profit_item_level": 2, "is_leaf": True, "status": "启用"},
    ]
    for pi in profit_items:
        pi["created_at"] = _SEED_DT

    # 2. 成本项主数据
    cost_items = [
        {"cost_item_id": "CI001", "cost_item_code": "CI001", "cost_item_name": "总成本", "cost_item_type": "汇总", "cost_category": "汇总", "parent_cost_item_id": "", "cost_item_level": 1, "is_leaf": False, "status": "启用"},
        {"cost_item_id": "CI002", "cost_item_code": "CI002", "cost_item_name": "直接材料", "cost_item_type": "直接", "cost_category": "生产成本", "parent_cost_item_id": "CI001", "cost_item_level": 2, "is_leaf": True, "status": "启用"},
        {"cost_item_id": "CI003", "cost_item_code": "CI003", "cost_item_name": "直接人工", "cost_item_type": "直接", "cost_category": "生产成本", "parent_cost_item_id": "CI001", "cost_item_level": 2, "is_leaf": True, "status": "启用"},
        {"cost_item_id": "CI004", "cost_item_code": "CI004", "cost_item_name": "制造费用", "cost_item_type": "间接", "cost_category": "生产成本", "parent_cost_item_id": "CI001", "cost_item_level": 2, "is_leaf": True, "status": "启用"},
        {"cost_item_id": "CI005", "cost_item_code": "CI005", "cost_item_name": "期间费用", "cost_item_type": "汇总", "cost_category": "期间费用", "parent_cost_item_id": "", "cost_item_level": 1, "is_leaf": False, "status": "启用"},
        {"cost_item_id": "CI006", "cost_item_code": "CI006", "cost_item_name": "销售费用", "cost_item_type": "期间费用", "cost_category": "期间费用", "parent_cost_item_id": "CI005", "cost_item_level": 2, "is_leaf": True, "status": "启用"},
        {"cost_item_id": "CI007", "cost_item_code": "CI007", "cost_item_name": "管理费用", "cost_item_type": "期间费用", "cost_category": "期间费用", "parent_cost_item_id": "CI005", "cost_item_level": 2, "is_leaf": True, "status": "启用"},
        {"cost_item_id": "CI008", "cost_item_code": "CI008", "cost_item_name": "财务费用", "cost_item_type": "期间费用", "cost_category": "期间费用", "parent_cost_item_id": "CI005", "cost_item_level": 2, "is_leaf": True, "status": "启用"},
    ]
    for ci in cost_items:
        ci["created_at"] = _SEED_DT

    # 3. 科目主数据（关联利润项和成本项）
    accounts = [
        {"account_id": "ACC6000", "account_code": "6000", "account_name": "营业收入", "account_type": "收入", "pl_category": "营业收入", "profit_item_id": "PI002", "cost_item_id": "", "parent_account_id": "", "account_level": 1, "is_leaf": False, "normal_balance": "贷", "status": "启用"},
        {"account_id": "ACC6001", "account_code": "6001", "account_name": "主营业务收入", "account_type": "收入", "pl_category": "营业收入", "profit_item_id": "PI002", "cost_item_id": "", "parent_account_id": "ACC6000", "account_level": 2, "is_leaf": True, "normal_balance": "贷", "status": "启用"},
        {"account_id": "ACC6050", "account_code": "6050", "account_name": "其他业务收入", "account_type": "收入", "pl_category": "营业收入", "profit_item_id": "PI003", "cost_item_id": "", "parent_account_id": "ACC6000", "account_level": 2, "is_leaf": True, "normal_balance": "贷", "status": "启用"},
        {"account_id": "ACC6400", "account_code": "6400", "account_name": "营业成本", "account_type": "成本", "pl_category": "营业成本", "profit_item_id": "", "cost_item_id": "CI001", "parent_account_id": "", "account_level": 1, "is_leaf": False, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC6401", "account_code": "6401", "account_name": "主营业务成本", "account_type": "成本", "pl_category": "营业成本", "profit_item_id": "", "cost_item_id": "CI002", "parent_account_id": "ACC6400", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC6402", "account_code": "6402", "account_name": "原材料成本", "account_type": "成本", "pl_category": "营业成本", "profit_item_id": "", "cost_item_id": "CI002", "parent_account_id": "ACC6400", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC6403", "account_code": "6403", "account_name": "人工成本", "account_type": "成本", "pl_category": "营业成本", "profit_item_id": "", "cost_item_id": "CI003", "parent_account_id": "ACC6400", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC6404", "account_code": "6404", "account_name": "制造费用", "account_type": "成本", "pl_category": "营业成本", "profit_item_id": "", "cost_item_id": "CI004", "parent_account_id": "ACC6400", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC6600", "account_code": "6600", "account_name": "期间费用", "account_type": "费用", "pl_category": "期间费用", "profit_item_id": "", "cost_item_id": "CI005", "parent_account_id": "", "account_level": 1, "is_leaf": False, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC6601", "account_code": "6601", "account_name": "销售费用", "account_type": "费用", "pl_category": "期间费用", "profit_item_id": "", "cost_item_id": "CI006", "parent_account_id": "ACC6600", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC6602", "account_code": "6602", "account_name": "管理费用", "account_type": "费用", "pl_category": "期间费用", "profit_item_id": "", "cost_item_id": "CI007", "parent_account_id": "ACC6600", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
        {"account_id": "ACC6603", "account_code": "6603", "account_name": "财务费用", "account_type": "费用", "pl_category": "期间费用", "profit_item_id": "", "cost_item_id": "CI008", "parent_account_id": "ACC6600", "account_level": 2, "is_leaf": True, "normal_balance": "借", "status": "启用"},
    ]
    for a in accounts:
        a["created_at"] = _SEED_DT

    # 4. 成本中心主数据
    cost_centers = [
        {"cost_center_id": "CC01", "cost_center_code": "PC-PROD", "cost_center_name": "生产中心", "department": "生产部", "company_code": "PD", "profit_center": "制造利润中心", "cost_center_type": "生产", "status": "启用"},
        {"cost_center_id": "CC02", "cost_center_code": "PC-SALE", "cost_center_name": "销售中心", "department": "销售部", "company_code": "PD", "profit_center": "销售利润中心", "cost_center_type": "销售", "status": "启用"},
        {"cost_center_id": "CC03", "cost_center_code": "PC-MGMT", "cost_center_name": "管理中心", "department": "管理部", "company_code": "PD", "profit_center": "管理利润中心", "cost_center_type": "管理", "status": "启用"},
        {"cost_center_id": "CC04", "cost_center_code": "PC-RD", "cost_center_name": "研发中心", "department": "研发部", "company_code": "PD", "profit_center": "研发利润中心", "cost_center_type": "研发", "status": "启用"},
        {"cost_center_id": "CC05", "cost_center_code": "PC-FIN", "cost_center_name": "财务中心", "department": "财务部", "company_code": "PD", "profit_center": "财务利润中心", "cost_center_type": "管理", "status": "启用"},
    ]
    for c in cost_centers:
        c["created_at"] = _SEED_DT

    # 5. 灌入维表数据
    s.sql.insert_rows("dim_profit_item", profit_items)
    output.print(f"OK 利润项 {len(profit_items)} 条")
    s.sql.insert_rows("dim_cost_item", cost_items)
    output.print(f"OK 成本项 {len(cost_items)} 条")
    s.sql.insert_rows("dim_account", accounts)
    output.print(f"OK 科目 {len(accounts)} 条")
    s.sql.insert_rows("dim_cost_center", cost_centers)
    output.print(f"OK 成本中心 {len(cost_centers)} 条")

    # 6. 生成实际分录数据
    leaf_accounts = [a for a in accounts if a["is_leaf"]]
    acct_dict = {a["account_id"]: a for a in accounts}
    pi_dict = {pi["profit_item_id"]: pi for pi in profit_items}
    ci_dict = {ci["cost_item_id"]: ci for ci in cost_items}
    cc_dict = {c["cost_center_id"]: c for c in cost_centers}

    random.seed(9520)
    fact_rows = []
    seq = 1
    start = date(2025, 1, 1)
    end = date(2026, 6, 30)

    # 基础金额配置
    base_amounts = {
        "ACC6001": 800000,  # 主营业务收入
        "ACC6050": 50000,   # 其他业务收入
        "ACC6401": 300000,  # 主营业务成本
        "ACC6402": 150000,  # 原材料成本
        "ACC6403": 100000,  # 人工成本
        "ACC6404": 50000,   # 制造费用
        "ACC6601": 80000,   # 销售费用
        "ACC6602": 60000,   # 管理费用
        "ACC6603": 20000,   # 财务费用
    }

    d = start
    while d <= end:
        if d.day <= 3:  # 每月前3天生成凭证
            for acc_id, base in base_amounts.items():
                account = acct_dict[acc_id]
                profit_item = pi_dict.get(account["profit_item_id"], None)
                cost_item = ci_dict.get(account["cost_item_id"], None)
                
                for cc in cost_centers:
                    # 根据科目类型分配成本中心
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
                    
                    fact_rows.append(_make_entry_line(seq, d, account, profit_item, cost_item, cc, amount))
                    seq += 1
        d += timedelta(days=1)

    inserted = s.sql.insert_rows("fact_gl_journal_entry", fact_rows)
    output.print(f"OK 实际分录表插入 {inserted} 行")

    # 7. 生成预算数据
    budget_rows = []
    bseq = 1
    for year in (2025, 2026):
        version = _BUDGET_VERSION if year == 2026 else f"{year}年度预算"
        for period in range(1, 13):
            if year == 2026 and period > 6:
                continue
            for account in leaf_accounts:
                base = base_amounts.get(account["account_id"], 50000)
                profit_item = pi_dict.get(account["profit_item_id"], None)
                cost_item = ci_dict.get(account["cost_item_id"], None)
                
                for cc in cost_centers:
                    # 同样的成本中心分配逻辑
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
                        "pl_category": account["pl_category"],
                        "profit_item_id": account["profit_item_id"],
                        "profit_item_name": profit_item["profit_item_name"] if profit_item else "",
                        "cost_item_id": account["cost_item_id"],
                        "cost_item_name": cost_item["cost_item_name"] if cost_item else "",
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
        "profit_items": len(profit_items),
        "cost_items": len(cost_items),
        "accounts": len(accounts),
        "cost_centers": len(cost_centers),
        "fact_inserted": inserted,
        "budget_inserted": binserted,
    }
    output.success("灌数完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))