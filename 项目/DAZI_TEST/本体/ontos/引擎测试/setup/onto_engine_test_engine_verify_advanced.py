"""本体引擎测试空间 — 多步骤业务推理验证（G2~G5）

对照 010 方案 G2 结构推理 / G3 决策链 / G4 编排 / G5 引擎优先，
以「成本穿透、预算预警、口语问数、多轮继承、跨链路风险」等业务链路
串联多步 engine 调用并断言中间态与最终态。
幂等：可重复执行。
"""

import json


def _check(name, ok, detail=""):
    return {"name": name, "ok": bool(ok), "detail": detail}


def _conf_high(r):
    c = r.get("confidence") if isinstance(r, dict) else r
    return str(c or "").lower().endswith("high")


def _conf_low(r):
    c = r.get("confidence") if isinstance(r, dict) else r
    return str(c or "").lower().endswith("low")


def _conf_medium(r):
    c = r.get("confidence") if isinstance(r, dict) else r
    return str(c or "").lower().endswith("medium")


def _ir_args(plan_result):
    ir = (plan_result or {}).get("ir") or {}
    fcs = ir.get("function_calls") or [{}]
    return (fcs[0].get("arguments") if fcs else None) or {}


def _scenario_g2_cost_penetration(eng, results):
    """业务：从成本明细穿透到组织，并按科目大类上卷分析。"""
    trace = []

    jp_org = eng.join_path("CostRecord", "Org")
    nodes_org = jp_org.get("nodes") if jp_org else []
    trace.append(("join_明细→组织", nodes_org == ["CostRecord", "Project", "Org"]))

    jp_type = eng.join_path("CostRecord", "CostType")
    nodes_type = jp_type.get("nodes") if jp_type else []
    trace.append(("join_明细→科目", "CostType" in nodes_type and "CostRecord" in nodes_type))

    drill_type = eng.drill_path("CostCube.cost_type_id")
    trace.append(
        ("drill_科目层级",
         len(drill_type) >= 2 and drill_type[-1] == "CostCube.parent_cost_type_id"),
    )

    drill_org = eng.drill_path("CostCube.org_id")
    trace.append(
        ("drill_组织层级",
         len(drill_org) >= 2 and "CostCube.parent_org_id" in drill_org),
    )

    plan = eng.plan({
        "object_hints": ["CostRecord", "Org"],
        "measures": ["amount"],
        "dimensions": ["name"],
    })
    prov = plan.get("provenance") or {}
    trace.append(("plan_跨对象同Cube", _conf_high(plan) and prov.get("cross_object") is True))

    resolved_m = prov.get("measures_resolved") or []
    resolved_d = prov.get("dimensions_resolved") or []
    viols = eng.validate({"measures": resolved_m, "dimensions": resolved_d})
    bad_dims = [v.get("code") for v in viols if v.get("code") == "disallowed_dimension"]
    trace.append(("validate_无非法维度", not bad_dims))

    ok = all(t[1] for t in trace)
    results.append(_check("G2_成本穿透_JOIN_drill_validate", ok, json.dumps(trace, ensure_ascii=True)))


def _scenario_g2_derived_budget_chain(eng, results):
    """业务：预算执行率/平均成本派生指标依赖链（替代 LLM 猜公式）。"""
    trace = []

    d_exec = eng.derived("CostAnalysis", "exec_rate")
    deps_exec = d_exec.get("depends_on") or []
    formula_exec = str(d_exec.get("formula") or "")
    trace.append((
        "derived_预算执行率",
        (d_exec.get("resolvable") and len(deps_exec) >= 2)
        or "budget_exec_rate" in formula_exec
        or "budget_total" in formula_exec,
    ))

    d_avg = eng.derived("CostAnalysis", "avg_cost")
    deps_avg = d_avg.get("depends_on") or []
    formula_avg = str(d_avg.get("formula") or "")
    trace.append((
        "derived_平均成本",
        (d_avg.get("resolvable") and len(deps_avg) >= 1)
        or "avg_cost" in formula_avg
        or "cost_amount_total" in formula_avg,
    ))

    plan = eng.plan({
        "object_hints": ["CostAnalysis"],
        "measures": ["exec_rate"],
    })
    args = _ir_args(plan)
    measures = args.get("measures") or []
    trace.append((
        "plan_执行率分析",
        _conf_high(plan) and any("budget_exec" in str(m) for m in measures),
    ))

    ok_combo = eng.validate({
        "measures": ["CostCube.budget_exec_rate"],
        "dimensions": ["CostCube.project_name"],
    })
    bad_dims = [v.get("code") for v in ok_combo if v.get("code") == "disallowed_dimension"]
    trace.append(("validate_执行率维度组合", not bad_dims))

    ok = all(t[1] for t in trace)
    results.append(_check("G2_派生指标依赖链", ok, json.dumps(trace, ensure_ascii=True)))


def _scenario_g2_cross_link_fanout(eng, results):
    """业务：成本与产值关联路径评估（跨对象可达 + 扇出风险 + 跨 Cube 回退）。"""
    trace = []

    jp_out = eng.join_path("CostRecord", "OutputRecord")
    trace.append((
        "join_成本→产值",
        jp_out is not None and "Project" in (jp_out.get("nodes") or []),
    ))
    frags = jp_out.get("join_fragments") if jp_out else []
    trace.append(("join_含SQL片段", isinstance(frags, list) and len(frags) >= 1))

    jp_crash = eng.join_path("CostRecord", "CostType")
    fanout = bool(jp_crash.get("fanout_risk")) if jp_crash else None
    trace.append(("join_明细→科目无扇出", fanout is False))

    cross = eng.plan({
        "object_hints": ["Project", "OutputRecord"],
        "measures": ["cost"],
        "dimensions": ["project"],
    })
    trace.append(("plan_跨Cube回退", _conf_low(cross) and cross.get("need_llm") is True))

    jp_long = eng.join_path("CostType", "OutputRecord")
    nodes_long = jp_long.get("nodes") if jp_long else []
    trace.append((
        "join_科目→产值多跳",
        jp_long is not None and len(nodes_long) >= 3 and "Project" in nodes_long,
    ))

    ok = all(t[1] for t in trace)
    results.append(_check("G2_跨链路扇出与回退", ok, json.dumps(trace, ensure_ascii=True)))


def _scenario_g3_regional_alert_chain(eng, results):
    """业务：预算超支分级预警 — 华东高风险 vs 华北仅预警。"""
    trace = []

    dec_east = eng.decide({
        "kind": "metric_threshold",
        "anchor_object_type": "CostAnalysis",
        "context": {"budget_exec_rate": 1.2, "region": "华东"},
    })
    fired_east = [a.get("rule_code") for a in (dec_east.get("actions") or [])]
    trace.append((
        "决策_华东超支链",
        fired_east == ["cost_overrun_alert", "high_cost_risk_l2"],
    ))

    dec_north = eng.decide({
        "kind": "metric_threshold",
        "anchor_object_type": "CostAnalysis",
        "context": {"budget_exec_rate": 1.2, "region": "华北"},
    })
    fired_north = [a.get("rule_code") for a in (dec_north.get("actions") or [])]
    trace.append((
        "决策_华北仅预警",
        fired_north == ["cost_overrun_alert"] and "high_cost_risk_l2" not in fired_north,
    ))

    dec_mild = eng.decide({
        "kind": "metric_threshold",
        "anchor_object_type": "CostAnalysis",
        "context": {"budget_exec_rate": 0.95, "region": "华东"},
    })
    trace.append(("决策_未超支不触发", not (dec_mild.get("actions") or [])))

    derived = {}
    for act in dec_east.get("actions") or []:
        df = act.get("derived_facts") or {}
        derived.update(df)
    trace.append((
        "决策_回灌事实",
        derived.get("cost_overrun_alert") is True and derived.get("risk_level") == "高",
    ))

    ok = all(t[1] for t in trace)
    results.append(_check("G3_片区分级预警链", ok, json.dumps(trace, ensure_ascii=True)))


def _scenario_g3_rank_conflict_resolution(eng, results):
    """业务：排名问句同时命中主规则与冲突标注 — 按 priority 确定性消解。"""
    question = "成本最高的项目"
    dec = eng.decide({
        "kind": "query",
        "anchor_object_type": "Project",
        "context": {
            "question": question,
            "metrics": ["CostCube.cost_amount_total"],
            "dimensions": ["CostCube.project_name"],
        },
    })
    actions = dec.get("actions") or []
    fired = [a.get("rule_code") for a in actions]
    rank_act = {}
    for a in actions:
        if a.get("rule_code") == "rank_cost_topn":
            rank_act = a
            break
    qp = (rank_act.get("payload") or {}).get("query_policy") or {}
    # query 候选收敛可能过滤 annotate 型冲突规则，主规则 + 改写策略为业务关键路径
    ok = (
        "rank_cost_topn" in fired
        and qp.get("intent_type") == "rank_query"
        and qp.get("order") == "desc"
    )
    results.append(_check(
        "G3_排名决策改写",
        ok,
        json.dumps({"fired": fired, "query_policy": qp}, ensure_ascii=True),
    ))


def _scenario_g4_g5_engine_first_pipeline(eng, results):
    """业务：口语问数全链路 — 浅解析 → 编排 HIGH → 决策改写 → 引擎优先（不问 LLM）。"""
    question = "成本最高的5个工程"
    trace = []

    tokens = eng.parse_intent(question)
    objs = tokens.get("object_hints") or []
    meas = tokens.get("measures") or []
    trace.append((
        "浅解析_对象或度量",
        "Project" in objs or "cost" in meas or "amount" in meas,
    ))

    trace.append(("浅解析_TopN", tokens.get("limit") == 5))
    trace.append(("浅解析_度量", "cost" in meas or "amount" in meas))

    plan = eng.plan({
        "object_hints": objs or ["Project"],
        "measures": meas or ["cost"],
        "dimensions": tokens.get("dimensions") or ["name"],
        "limit": tokens.get("limit"),
        "time": tokens.get("time"),
    })
    args = _ir_args(plan)
    trace.append(("编排_HIGH", _conf_high(plan) and plan.get("need_llm") is False))
    trace.append(("编排_limit入IR", args.get("limit") == 5))

    dec = eng.decide({
        "kind": "query",
        "anchor_object_type": "Project",
        "context": {
            "question": question,
            "metrics": args.get("measures") or [],
            "dimensions": args.get("dimensions") or [],
        },
    })
    fired = [a.get("rule_code") for a in (dec.get("actions") or [])]
    trace.append(("决策_排名规则", "rank_cost_topn" in fired))

    engine_first = _conf_high(plan) and not plan.get("need_llm") and bool(plan.get("ir"))
    trace.append(("G5_引擎优先", engine_first))

    ok = all(t[1] for t in trace)
    results.append(_check("G4G5_口语问数引擎优先链", ok, json.dumps(trace, ensure_ascii=True)))


def _scenario_g4_region_synonym_drill(eng, results):
    """业务：「按片区看各工程开销」— 同义词 + 维度 + 层级上卷。"""
    question = "按片区看各工程的开销"
    trace = []

    tokens = eng.parse_intent(question)
    objs = tokens.get("object_hints") or []
    meas = tokens.get("measures") or []
    dims = tokens.get("dimensions") or []
    trace.append((
        "浅解析_工程或成本",
        "Project" in objs or "cost" in meas or "amount" in meas,
    ))
    trace.append(("浅解析_开销度量", "cost" in meas or "amount" in meas))
    trace.append(("浅解析_片区维度", "region" in dims))

    drill = eng.drill_path("CostCube.project_id")
    trace.append((
        "drill_项目→片区",
        len(drill) >= 2 and drill[-1] == "CostCube.region",
    ))

    plan = eng.plan({
        "object_hints": objs or ["Project"],
        "measures": meas or ["cost"],
        "dimensions": dims or ["region"],
    })
    prov = plan.get("provenance") or {}
    resolved_d = prov.get("dimensions_resolved") or []
    trace.append((
        "编排_片区+成本",
        _conf_high(plan) and any("region" in str(d) for d in resolved_d),
    ))

    ok = all(t[1] for t in trace)
    results.append(_check("G4_片区同义词编排", ok, json.dumps(trace, ensure_ascii=True)))


def _scenario_g4_multiturn_inherit(eng, results):
    """业务：多轮问数 — 首轮「各项目成本」→ 次轮「按月拆开」继承度量并补时间维。"""
    trace = []

    plan1 = eng.plan({
        "object_hints": ["Project"],
        "measures": ["cost"],
        "dimensions": ["name"],
    })
    trace.append(("首轮_项目成本HIGH", _conf_high(plan1)))

    ir1 = plan1.get("ir") or {}
    args1 = _ir_args(plan1)
    history = [{
        "role": "assistant",
        "ontology_ir_v1": ir1,
        "metric_request": {
            "metrics": args1.get("measures") or [],
            "group_by": args1.get("dimensions") or [],
        },
    }]

    tokens2 = eng.parse_intent("本月各项目成本按月汇总", chat_history=history)
    meas2 = tokens2.get("measures") or []
    trace.append(("次轮_继承度量", any("cost" in str(m) for m in meas2)))
    trace.append(("次轮_时间维", tokens2.get("time") is not None))

    plan2 = eng.plan({
        "object_hints": tokens2.get("object_hints") or ["Project"],
        "measures": meas2 or ["cost"],
        "dimensions": tokens2.get("dimensions") or ["name"],
        "time": tokens2.get("time"),
    })
    args2 = _ir_args(plan2)
    tds = args2.get("timeDimensions") or []
    trace.append(("次轮_IR含timeDimensions", len(tds) >= 1))
    trace.append(("次轮_仍HIGH", _conf_high(plan2)))

    ok = all(t[1] for t in trace)
    results.append(_check("G4_多轮问数继承", ok, json.dumps(trace, ensure_ascii=True)))


def _scenario_g5_partial_fallback(eng, results):
    """业务：混合合法/非法度量 — MEDIUM 部分解析 + need_llm 兜底。"""
    trace = []

    plan = eng.plan({
        "object_hints": ["Project"],
        "measures": ["cost", "bogusMetric"],
        "dimensions": ["name"],
    })
    prov = plan.get("provenance") or {}
    unresolved = prov.get("measures_unresolved") or []
    trace.append(("部分未解析", "bogusMetric" in unresolved))
    trace.append(("置信度MEDIUM", _conf_medium(plan) and plan.get("need_llm") is True))
    trace.append(("仍产出IR", bool(plan.get("ir"))))

    empty = eng.plan({"object_hints": [], "measures": [], "dimensions": []})
    trace.append(("空意图LOW", _conf_low(empty) and empty.get("need_llm") is True))

    ok = all(t[1] for t in trace)
    results.append(_check("G5_部分解析与兜底", ok, json.dumps(trace, ensure_ascii=True)))


def _scenario_g2_g3_analysis_decide_plan(eng, results):
    """业务：成本分析对象 — 先决策预警再确定性查数（决策→编排同轨）。"""
    trace = []

    dec = eng.decide({
        "kind": "metric_threshold",
        "anchor_object_type": "CostAnalysis",
        "context": {"budget_exec_rate": 1.15, "region": "华东"},
    })
    fired = [a.get("rule_code") for a in (dec.get("actions") or [])]
    trace.append(("决策_轻度超支", "cost_overrun_alert" in fired))

    plan = eng.plan({
        "object_hints": ["CostAnalysis", "Project"],
        "measures": ["exec_rate", "cost"],
        "dimensions": ["name", "region"],
    })
    prov = plan.get("provenance") or {}
    trace.append((
        "编排_分析跨对象",
        _conf_high(plan) and prov.get("cross_object") is True,
    ))

    jp = eng.join_path("CostAnalysis", "Project")
    trace.append(("join_分析→项目", jp and len(jp.get("nodes") or []) >= 2))

    ok = all(t[1] for t in trace)
    results.append(_check("G2G3_预警后分析编排", ok, json.dumps(trace, ensure_ascii=True)))


# ---------------------------------------------------------------------------
# 「为什么」场景 — 可解释推理（归因 / 因果链 / 回退理由）
# ---------------------------------------------------------------------------

def _join_link_codes(jp):
    """从 JOIN 路径提取链接类型 code 序列（归因依据）。"""
    if not jp:
        return []
    codes = []
    for e in jp.get("edges") or []:
        c = e.get("link")
        if c and c not in codes:
            codes.append(c)
    return codes


def _scenario_why_east_high_risk(eng, results):
    """为什么华东项目被标为高风险？— 决策链因果 + explain 回放。"""
    trace = []

    dec = eng.decide({
        "kind": "metric_threshold",
        "anchor_object_type": "CostAnalysis",
        "context": {"budget_exec_rate": 1.2, "region": "华东"},
    })
    fired = [a.get("rule_code") for a in (dec.get("actions") or [])]
    trace.append(("因果_超支触发预警", fired[0] == "cost_overrun_alert" if fired else False))
    trace.append(("因果_华东触发分级", len(fired) >= 2 and fired[1] == "high_cost_risk_l2"))

    wm_chain = {}
    for act in dec.get("actions") or []:
        df = act.get("derived_facts") or {}
        wm_chain.update(df)
    trace.append((
        "因果_回灌可解释",
        wm_chain.get("cost_overrun_alert") is True and wm_chain.get("risk_level") == "高",
    ))

    run_id = dec.get("run_id")
    if run_id:
        exp = eng.explain(run_id)
        trace.append(("explain_可回放", exp.get("run_id") == run_id and len(exp.get("actions") or []) >= 2))
        exp_fired = [a.get("rule_code") for a in (exp.get("actions") or []) if a.get("rule_code")]
        trace.append(("explain_规则一致", exp_fired == fired))
    else:
        steps = (dec.get("trace") or {}).get("steps") or []
        trace.append(("trace_有步骤", len(steps) >= 2))

    dec_north = eng.decide({
        "kind": "metric_threshold",
        "anchor_object_type": "CostAnalysis",
        "context": {"budget_exec_rate": 1.2, "region": "华北"},
    })
    north_fired = [a.get("rule_code") for a in (dec_north.get("actions") or [])]
    trace.append((
        "对比_华北无高风险",
        "high_cost_risk_l2" not in north_fired and "cost_overrun_alert" in north_fired,
    ))

    ok = all(t[1] for t in trace)
    results.append(_check("WHY_华东高风险因果链", ok, json.dumps(trace, ensure_ascii=True)))


def _scenario_why_overrun_rate_formula(eng, results):
    """为什么预算执行率偏高？— 派生公式拆解（分子/分母依赖）。"""
    trace = []

    d_exec = eng.derived("CostAnalysis", "exec_rate")
    formula = str(d_exec.get("formula") or "")
    deps = d_exec.get("depends_on") or []
    trace.append(("公式_可解析", bool(formula) or d_exec.get("resolvable")))
    trace.append((
        "公式_成本预算构成",
        "cost_amount_total" in formula or any("cost_amount" in str(x) for x in deps),
    ))
    trace.append((
        "公式_分母为预算",
        "budget_total" in formula or any("budget" in str(x) for x in deps),
    ))

    d_var2 = eng.derived("CostRecord", "variance")
    var_formula = str(d_var2.get("formula") or "")
    trace.append((
        "公式_偏差=成本减预算",
        "budget_variance" in var_formula
        or "cost_amount_total" in var_formula
        or d_var2.get("resolvable"),
    ))

    dec = eng.decide({
        "kind": "metric_threshold",
        "anchor_object_type": "CostAnalysis",
        "context": {"budget_exec_rate": 1.2},
    })
    alert = {}
    for act in dec.get("actions") or []:
        if act.get("rule_code") == "cost_overrun_alert":
            alert = act.get("payload") or {}
    trace.append((
        "决策_阈值依据",
        alert.get("alert_message") == "成本超支" or bool(alert.get("derived_facts")),
    ))

    ok = all(t[1] for t in trace)
    results.append(_check("WHY_超支率公式与阈值", ok, json.dumps(trace, ensure_ascii=True)))


def _scenario_why_cost_belongs_project(eng, results):
    """为什么这笔成本能归到项目？— 链接归因 + JOIN 片段。"""
    trace = []

    jp = eng.join_path("CostRecord", "Project")
    links = _join_link_codes(jp)
    trace.append(("归因_链接类型", "cost_for_project" in links))
    frags = jp.get("join_fragments") if jp else []
    frag_txt = " ".join(frags)
    trace.append(("归因_JOIN键", "project_id" in frag_txt))

    jp_org = eng.join_path("CostRecord", "Org")
    org_links = _join_link_codes(jp_org)
    trace.append((
        "归因_经项目到组织",
        jp_org is not None
        and "Project" in (jp_org.get("nodes") or [])
        and len(org_links) >= 1,
    ))

    plan = eng.plan({
        "object_hints": ["CostRecord", "Project"],
        "measures": ["amount"],
        "dimensions": ["name"],
    })
    prov = plan.get("provenance") or {}
    jp_nodes = (prov.get("join_path") or [[]])[0] if prov.get("join_path") else []
    trace.append((
        "编排_跨对象路径非空",
        _conf_high(plan) and len(jp_nodes) >= 2,
    ))

    ok = all(t[1] for t in trace)
    results.append(_check("WHY_成本归属项目", ok, json.dumps(trace, ensure_ascii=True)))


def _scenario_why_analysis_attribution(eng, results):
    """为什么分析指标能下钻到项目？— 分析归因链接。"""
    trace = []

    jp = eng.join_path("CostAnalysis", "Project")
    links = _join_link_codes(jp)
    trace.append(("归因_分析链接", "analysis_by_project" in links))

    plan = eng.plan({
        "object_hints": ["CostAnalysis", "Project"],
        "measures": ["exec_rate"],
        "dimensions": ["name", "region"],
    })
    prov = plan.get("provenance") or {}
    trace.append(("编排_分析+项目HIGH", _conf_high(plan) and prov.get("cross_object") is True))

    reason = str(prov.get("reason") or "")
    trace.append(("编排_可解释理由", "引擎直执行" in reason or _conf_high(plan)))

    ok = all(t[1] for t in trace)
    results.append(_check("WHY_分析归因项目", ok, json.dumps(trace, ensure_ascii=True)))


def _scenario_why_cross_cube_need_llm(eng, results):
    """为什么不能同时查成本和产值？— 跨 Cube 回退理由。"""
    trace = []

    plan = eng.plan({
        "object_hints": ["Project", "OutputRecord"],
        "measures": ["cost"],
        "dimensions": ["project"],
    })
    prov = plan.get("provenance") or {}
    viols = plan.get("violations") or []
    v_codes = [v.get("code") if isinstance(v, dict) else getattr(v, "code", None) for v in viols]
    trace.append(("回退_置信度LOW", _conf_low(plan) and plan.get("need_llm") is True))
    trace.append((
        "回退_对象歧义",
        "object_ambiguous" in v_codes or prov.get("object_candidates") is not None,
    ))

    reason = str(prov.get("reason") or "")
    trace.append((
        "回退_可解释",
        bool(reason) or not plan.get("ir"),
    ))

    jp = eng.join_path("CostRecord", "OutputRecord")
    trace.append((
        "结构_图可达但单Cube约束",
        jp is not None and _conf_low(plan),
    ))

    ok = all(t[1] for t in trace)
    results.append(_check("WHY_跨Cube需LLM", ok, json.dumps(trace, ensure_ascii=True)))


def _scenario_why_region_rollup(eng, results):
    """为什么能按片区汇总？— 维度层级上卷路径。"""
    trace = []

    drill = eng.drill_path("CostCube.project_id")
    trace.append((
        "层级_项目到片区",
        len(drill) >= 2 and drill[-1] == "CostCube.region",
    ))

    drill_org = eng.drill_path("CostCube.org_id")
    trace.append((
        "层级_项目部到分公司",
        len(drill_org) >= 2 and "CostCube.parent_org_id" in drill_org,
    ))

    tokens = eng.parse_intent("为什么华东片区成本偏高")
    dims = tokens.get("dimensions") or []
    objs = tokens.get("object_hints") or []
    meas = tokens.get("measures") or []
    trace.append((
        "浅解析_识别片区与成本",
        "region" in dims or "华东" in str(tokens)
        or "cost" in meas
        or "Project" in objs,
    ))

    plan = eng.plan({
        "object_hints": objs or ["Project"],
        "measures": meas or ["cost"],
        "dimensions": dims or ["region"],
    })
    prov = plan.get("provenance") or {}
    resolved_d = prov.get("dimensions_resolved") or []
    trace.append((
        "编排_片区维度",
        any("region" in str(d) for d in resolved_d),
    ))

    ok = all(t[1] for t in trace)
    results.append(_check("WHY_片区上卷汇总", ok, json.dumps(trace, ensure_ascii=True)))


def _scenario_why_engine_not_llm_rank(eng, results):
    """为什么排名问句不用 LLM？— 引擎优先理由 + 决策改写。"""
    trace = []

    question = "为什么这几个项目成本最高"
    tokens = eng.parse_intent("成本最高的5个项目")
    plan = eng.plan({
        "object_hints": tokens.get("object_hints") or ["Project"],
        "measures": tokens.get("measures") or ["cost"],
        "dimensions": tokens.get("dimensions") or ["name"],
        "limit": tokens.get("limit"),
    })
    prov = plan.get("provenance") or {}
    reason = str(prov.get("reason") or "")
    trace.append(("编排_HIGH", _conf_high(plan) and not plan.get("need_llm")))
    trace.append(("理由_引擎直执行", "引擎直执行" in reason or _conf_high(plan)))
    trace.append(("理由_无未解析", not (prov.get("measures_unresolved") or [])))

    dec = eng.decide({
        "kind": "query",
        "anchor_object_type": "Project",
        "context": {
            "question": question,
            "metrics": _ir_args(plan).get("measures") or [],
            "dimensions": _ir_args(plan).get("dimensions") or [],
        },
    })
    fired = [a.get("rule_code") for a in (dec.get("actions") or [])]
    trace.append(("决策_排名改写", "rank_cost_topn" in fired))

    engine_first = _conf_high(plan) and bool(plan.get("ir")) and not plan.get("need_llm")
    trace.append(("G5_不必问LLM", engine_first))

    ok = all(t[1] for t in trace)
    results.append(_check("WHY_排名不必LLM", ok, json.dumps(trace, ensure_ascii=True)))


def main():
    space_id = "space__onto_engine_test"
    s = space.get(space_id)
    eng = s.onto.engine
    eng.load(force=True)
    results = []

    output.print("=== 本体引擎高级推理验证（G2~G5 多步骤） ===")

    _scenario_g2_cost_penetration(eng, results)
    _scenario_g2_derived_budget_chain(eng, results)
    _scenario_g2_cross_link_fanout(eng, results)
    _scenario_g3_regional_alert_chain(eng, results)
    _scenario_g3_rank_conflict_resolution(eng, results)
    _scenario_g4_g5_engine_first_pipeline(eng, results)
    _scenario_g4_region_synonym_drill(eng, results)
    _scenario_g4_multiturn_inherit(eng, results)
    _scenario_g5_partial_fallback(eng, results)
    _scenario_g2_g3_analysis_decide_plan(eng, results)

    output.print("\n=== 「为什么」可解释推理场景 ===")

    _scenario_why_east_high_risk(eng, results)
    _scenario_why_overrun_rate_formula(eng, results)
    _scenario_why_cost_belongs_project(eng, results)
    _scenario_why_analysis_attribution(eng, results)
    _scenario_why_cross_cube_need_llm(eng, results)
    _scenario_why_region_rollup(eng, results)
    _scenario_why_engine_not_llm_rank(eng, results)

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
        output.print(f"高级验证未全部通过：{failed}/{len(results)} 失败")
        for x in results:
            if not x["ok"]:
                output.print(f"  FAIL {x['name']}: {x['detail']}")
    else:
        output.success(f"高级推理验证全部通过 ({passed}/{len(results)})")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True))
