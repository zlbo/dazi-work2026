"""本体引擎测试空间 — 引擎能力集成验证

对照 018 方案 §4 场景矩阵，批量调用 s.onto.engine 并断言期望。
幂等：可重复执行。
"""

import json


def _check(name, ok, detail=""):
    return {"name": name, "ok": bool(ok), "detail": detail}


def main():
    space_id = "space__onto_engine_test"
    s = space.get(space_id)
    eng = s.onto.engine
    eng.load(force=True)
    results = []

    # ---- G4 plan：对象+度量 HIGH ----
    r = eng.plan({
        "object_hints": ["Project"],
        "measures": ["cost"],
    })
    results.append(_check(
        "O1_plan_project_cost_high",
        r.get("confidence") == "high" and not r.get("need_llm") and r.get("ir"),
        f"confidence={r.get('confidence')}",
    ))

    # ---- G4 跨对象同 Cube HIGH ----
    r = eng.plan({
        "object_hints": ["Project", "CostRecord"],
        "measures": ["amount"],
        "dimensions": ["name"],
    })
    prov = r.get("provenance") or {}
    results.append(_check(
        "X1_cross_object_same_cube",
        r.get("confidence") == "high" and prov.get("cross_object") is True,
        f"confidence={r.get('confidence')} cross={prov.get('cross_object')}",
    ))

    # ---- G4 跨 Cube 回退 ----
    r = eng.plan({
        "object_hints": ["Project", "OutputRecord"],
        "measures": ["cost"],
        "dimensions": ["project"],
    })
    results.append(_check(
        "X2_cross_cube_fallback",
        r.get("confidence") == "low" and r.get("need_llm"),
        f"confidence={r.get('confidence')}",
    ))

    # ---- G4 Top-N limit ----
    r = eng.plan({
        "object_hints": ["Project"],
        "measures": ["cost"],
        "dimensions": ["name"],
        "limit": 5,
    })
    lim = None
    if r.get("ir"):
        args = (r["ir"].get("function_calls") or [{}])[0].get("arguments") or {}
        lim = args.get("limit")
    results.append(_check("N1_topn_limit", lim == 5, f"limit={lim}"))

    # ---- G4 时间维度（通过 plan 传入 time）----
    r = eng.plan({
        "object_hints": ["CostRecord"],
        "measures": ["amount"],
        "time": {
            "dimension": "CostCube.date_key",
            "dateRange": [20260601, 20260630],
            "granularity": "month",
        },
    })
    td = None
    if r.get("ir"):
        args = (r["ir"].get("function_calls") or [{}])[0].get("arguments") or {}
        tds = args.get("timeDimensions") or []
        td = tds[0] if tds else None
    results.append(_check(
        "T1_time_dimension",
        td and td.get("dimension") == "CostCube.date_key",
        str(td),
    ))

    # ---- G2 JOIN 路径 ----
    jp = eng.join_path("CostRecord", "Project")
    results.append(_check(
        "J1_join_cost_project",
        jp and len(jp.get("nodes") or []) >= 2,
        str(jp.get("nodes") if jp else None),
    ))

    jp2 = eng.join_path("CostRecord", "Org")
    results.append(_check(
        "J2_join_cost_org",
        jp2 and len(jp2.get("nodes") or []) >= 2,
        str(jp2.get("nodes") if jp2 else None),
    ))

    # ---- G2 drill 路径 ----
    drill = eng.drill_path("CostCube.org_id")
    results.append(_check(
        "D1_drill_org",
        isinstance(drill, list) and len(drill) >= 1,
        str(drill),
    ))

    # ---- G2 validate 非法维度 ----
    viols = eng.validate({
        "measures": ["CostCube.cost_amount_total"],
        "dimensions": ["CostCube.cost_amount_total"],
    })
    codes = [v.get("code") for v in viols]
    results.append(_check(
        "R3_disallowed_dimension",
        "disallowed_dimension" in codes,
        str(codes),
    ))

    # ---- G3 决策：排名规则 ----
    dec = eng.decide({
        "kind": "query",
        "anchor_object_type": "Project",
        "context": {
            "question": "成本最高的5个项目",
            "metrics": ["CostCube.cost_amount_total"],
            "dimensions": ["CostCube.project_name"],
        },
    })
    fired = [a.get("rule_code") for a in (dec.get("actions") or [])]
    results.append(_check(
        "C1_rank_decision",
        "rank_cost_topn" in fired,
        str(fired),
    ))

    # ---- G3 决策：超支 + 规则链 ----
    dec2 = eng.decide({
        "kind": "metric_threshold",
        "anchor_object_type": "CostAnalysis",
        "context": {
            "budget_exec_rate": 1.2,
            "region": "华东",
        },
    })
    fired2 = [a.get("rule_code") for a in (dec2.get("actions") or [])]
    results.append(_check(
        "C3_overrun_chain",
        "cost_overrun_alert" in fired2 and "high_cost_risk_l2" in fired2,
        str(fired2),
    ))

    # ---- 同义词：工程+花费 ----
    r = eng.plan({
        "object_hints": ["工程"],
        "measures": ["花费"],
    })
    results.append(_check(
        "S1_synonym_plan",
        r.get("confidence") == "high" and r.get("ir"),
        f"confidence={r.get('confidence')}",
    ))

    passed = sum(1 for x in results if x["ok"])
    failed = len(results) - passed
    summary = {
        "ok": failed == 0,
        "passed": passed,
        "failed": failed,
        "total": len(results),
        "results": results,
    }
    if failed:
        output.print(f"验证未全部通过：{failed}/{len(results)} 失败")
        for x in results:
            if not x["ok"]:
                output.print(f"  FAIL {x['name']}: {x['detail']}")
    else:
        output.success(f"引擎验证全部通过 ({passed}/{len(results)})")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True))

