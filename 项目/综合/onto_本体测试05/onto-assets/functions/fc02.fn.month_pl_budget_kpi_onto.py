# 本体函数脚本（从服务端拉取）
# function_id: fc02.fn.month_pl_budget_kpi_onto
# script_id: 75387d4c-8238-4d46-a8c7-7e6a472b5e08
# space_id: space__0519

"""FC02 B2：月利润/预算/达成率（两次 semantic.query_aggregate，文档 201 §8）"""

_PAI = "cube_fin_cockpit02_profit"
_BAD = "cube_fin_cockpit02_budget_m"
_SEM = "semantic.query_aggregate"


def _to_float(v):
    if v is None:
        return None
    if isinstance(v, bool):
        return None
    try:
        if isinstance(v, (int, float)):
            x = float(v)
            if x != x:
                return None
            return x
        return float(v)
    except Exception:
        return None


def _pick_measure(row, needles):
    if not row or not isinstance(row, dict):
        return None
    keys = list(row.keys())
    for needle in needles:
        n = needle.lower()
        for k in keys:
            kl = str(k).lower()
            if n in kl:
                f = _to_float(row.get(k))
                if f is not None:
                    return f
    for k in keys:
        f = _to_float(row.get(k))
        if f is not None:
            return f
    return None


def main():
    args = dict(ctx.params or {})
    space.get(ctx.space_id)
    sid = ctx.space_id

    if args.get("date_key") is not None:
        dk = int(args["date_key"])
        if dk < 19000101 or dk > 20991231:
            output.error("date_key 超出合理范围")
            return None
        ymi = dk // 100
    else:
        ym = str(args.get("year_month") or "").strip()
        parts = ym.split("-")
        if len(parts) == 2 and len(parts[0]) == 4 and len(parts[1]) == 2:
            ymi = int(parts[0]) * 100 + int(parts[1])
        else:
            output.error("需要提供 year_month(YYYY-MM) 或 date_key(YYYYMMDD)")
            return None

    vid_raw = args.get("version_id")
    vid = int(vid_raw) if vid_raw is not None and str(vid_raw).strip() != "" else 1
    if vid < 0 or vid > 255:
        output.error("version_id 无效")
        return None

    ym_str = "{:04d}-{:02d}".format(ymi // 100, ymi % 100)
    y, mo = divmod(ymi, 100)
    date_key_first = y * 10000 + mo * 100 + 1

    # ir_p：利润侧 Ontology IR（对象类型 FinPLMonthFact，度量 amount），与前端 irProfitMonthTotal 等价。
    ir_p = {
        "version": "onto-ir-1",
        "space_id": sid,
        "object_set": {
            "object_type_code": "FinPLMonthFact",
            "filters": [
                {"member": _PAI + ".year_month", "operator": "equals", "values": [ym_str]},
            ],
        },
        "function_calls": [
            {
                "function_id": _SEM,
                "arguments": {"measures": ["amount"], "dimensions": [], "limit": 32},
            }
        ],
    }
    # ir_b：预算侧 Ontology IR（FinBudgetMonthFact，度量 budget_value；date_key 月初 + version_id），与 irBudgetMonthTotal 等价。
    ir_b = {
        "version": "onto-ir-1",
        "space_id": sid,
        "object_set": {
            "object_type_code": "FinBudgetMonthFact",
            "filters": [
                {"member": _BAD + ".date_key", "operator": "equals", "values": [date_key_first]},
                {"member": _BAD + ".version_id", "operator": "equals", "values": [vid]},
            ],
        },
        "function_calls": [
            {
                "function_id": _SEM,
                "arguments": {"measures": ["budget_value"], "dimensions": [], "limit": 32},
            }
        ],
    }

    # --- 利润侧语义聚合 ---
    # rp：onto.query_aggregate_ir → 与 POST .../app/query-aggregate 同脊骨；为 dict，含 ok、columns、data、row_count、metric_request 等。
    rp = onto.query_aggregate_ir(ir_p)
    if not rp.get("ok"):
        output.error(rp.get("error") or "利润语义聚合失败")
        return None
    # dp：rp["data"]，即利润查询结果表体，类型为 list[dict]；无维度时通常 1 行，键名为语义层/ClickHouse 列别名（如含 amount）。
    dp = rp.get("data") or []
    if not dp:
        actual_total = None
    else:
        # 从首行 dict 中解析 amount 聚合值（列名不固定，故用 _pick_measure 按关键字匹配）。
        actual_total = _pick_measure(dp[0], ["amount"])

    # --- 预算侧语义聚合 ---
    # rb：预算 IR 的执行结果体，形状与 rp 相同；ok 为 False 时表示 IR/语义层校验失败等。
    rb = onto.query_aggregate_ir(ir_b)
    if not rb.get("ok"):
        output.error(rb.get("error") or "预算语义聚合失败")
        return None
    # db：rb["data"]，预算查询结果行列表（此处变量名 db 仅表示 budget 的 data 行，勿与数据库会话混淆）。
    db = rb.get("data") or []
    if not db:
        budget_total = None
    else:
        budget_total = _pick_measure(db[0], ["budget_value"])

    # ach：达成率 = 利润合计 / 预算合计；分母为 0 时与 B1 SQL 一致，结果为 None。
    ach = None
    if actual_total is not None and budget_total is not None and budget_total != 0:
        ach = actual_total / budget_total

    row = {
        "year_month": ym_str,
        "version_id": vid,
        "actual_total": actual_total,
        "budget_total": budget_total,
        "achievement_rate": ach,
    }
    cols = list(row.keys())
    return onto.function_result(columns=cols, data=[row], row_count=1)
