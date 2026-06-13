"""本体引擎测试空间 — OntologyGraph / networkx 图谱不变式验证

对照 002 §2「唯一图源」：验证从 DB 装配的 MultiDiGraph 结构、Cube schema、
层级、派生度量、链接 JOIN 键等**结构不变式**（不断言具体业务常量字符串）。

与 engine_verify 互补：后者测 plan/decide 行为，本脚本测图谱本身是否正确装配。
幂等：可重复执行。
"""

import json


def _check(name, ok, detail=""):
    return {"name": name, "ok": bool(ok), "detail": detail}


def _codes(summary):
    return {o.get("code") for o in (summary.get("objects") or [])}


def _link_by_code(summary):
    return {lk.get("code"): lk for lk in (summary.get("links") or [])}


def main():
    space_id = "space__onto_engine_test"
    s = space.get(space_id)
    eng = s.onto.engine
    results = []

    output.print("=== OntologyGraph / networkx 图谱验证 ===")

    # 1) 装配与 summary 基线（与 init 脚本产出对齐，用计数而非业务文案）
    summary1 = eng.load(force=True)
    trace = []
    trace.append(("对象数≥6", summary1.get("object_count", 0) >= 6))
    trace.append(("链接数≥7", summary1.get("link_count", 0) >= 7))
    trace.append(("层级数≥3", summary1.get("hierarchy_count", 0) >= 3))
    codes = _codes(summary1)
    trace.append(("含核心对象", {"Project", "CostRecord", "OutputRecord", "CostAnalysis"}.issubset(codes)))
    results.append(_check("GRAPH_装配基线", all(t[1] for t in trace), json.dumps(trace, ensure_ascii=True)))

    # 2) 节点：Cube 绑定与属性
    trace = []
    for code, expect_cube in [
        ("Project", "CostCube"),
        ("CostRecord", "CostCube"),
        ("OutputRecord", "OutputCube"),
        ("CostAnalysis", "CostCube"),
    ]:
        node = eng.object(code) or {}
        trace.append((f"节点_{code}_cube", node.get("cube") == expect_cube))
        trace.append((f"节点_{code}_有属性", len(node.get("properties") or []) >= 1))
    node_ct = eng.object("CostType") or {}
    trace.append(("参考对象无Cube", not node_ct.get("cube")))
    results.append(_check("GRAPH_节点Cube绑定", all(t[1] for t in trace), json.dumps(trace, ensure_ascii=True)))

    # 3) 边：链接含 JOIN 键（结构依据，不断言 link code 名称）
    summary = eng.graph()
    links = summary.get("links") or []
    trace = []
    with_keys = [lk for lk in links if (lk.get("join_key_count") or 0) >= 1]
    trace.append(("多数链接有JOIN键", len(with_keys) >= 5))
    # 成本明细必须能连到项目（归因链存在）
    reaches_project = any(
        lk.get("from") == "CostRecord" and lk.get("to") == "Project"
        for lk in links
    )
    trace.append(("存在_明细→项目边", reaches_project))
    analysis_link = _link_by_code(summary).get("analysis_by_project")
    if analysis_link:
        trace.append((
            "分析归因边",
            analysis_link.get("from") == "CostAnalysis"
            and analysis_link.get("to") == "Project"
            and (analysis_link.get("join_key_count") or 0) >= 1,
        ))
    else:
        trace.append(("分析归因边", any(
            lk.get("from") == "CostAnalysis" and lk.get("to") == "Project"
            for lk in links
        )))
    results.append(_check("GRAPH_边与JOIN键", all(t[1] for t in trace), json.dumps(trace, ensure_ascii=True)))

    # 4) 推理层交叉验证：图谱边 → join_path 可达（networkx 最短路消费同一图源）
    trace = []
    pairs = [
        ("CostRecord", "Project"),
        ("CostRecord", "Org"),
        ("CostAnalysis", "Project"),
        ("CostRecord", "OutputRecord"),
    ]
    for a, b in pairs:
        jp = eng.join_path(a, b)
        trace.append((f"可达_{a}→{b}", jp is not None and len(jp.get("nodes") or []) >= 2))
    results.append(_check("GRAPH_JOIN路径可达", all(t[1] for t in trace), json.dumps(trace, ensure_ascii=True)))

    # 5) 派生度量 + drill 层级（图级 schema 附加数据）
    trace = []
    d = eng.derived("CostAnalysis", "exec_rate")
    trace.append(("派生_可解析", d.get("resolvable") or bool(d.get("formula"))))
    deps = d.get("depends_on") or []
    trace.append(("派生_有依赖", len(deps) >= 1 or "budget" in str(d.get("formula", ""))))
    drill = eng.drill_path("CostCube.project_id")
    trace.append(("层级_项目上卷", len(drill) >= 2))
    results.append(_check("GRAPH_派生与层级", all(t[1] for t in trace), json.dumps(trace, ensure_ascii=True)))

    # 6) 缓存 / 失效：invalidate 后重载结构一致
    trace = []
    n1 = summary1.get("object_count")
    l1 = summary1.get("link_count")
    eng.invalidate()
    summary2 = eng.load(force=True)
    trace.append(("失效后对象数一致", summary2.get("object_count") == n1))
    trace.append(("失效后链接数一致", summary2.get("link_count") == l1))
    trace.append(("失效后层级数一致", summary2.get("hierarchy_count") == summary1.get("hierarchy_count")))
    results.append(_check("GRAPH_缓存失效一致", all(t[1] for t in trace), json.dumps(trace, ensure_ascii=True)))

    passed = sum(1 for x in results if x["ok"])
    failed = len(results) - passed
    summary_out = {
        "ok": failed == 0,
        "passed": passed,
        "failed": failed,
        "total": len(results),
        "results": results,
    }
    if failed:
        output.print(f"图谱验证未全部通过：{failed}/{len(results)} 失败")
        for x in results:
            if not x["ok"]:
                output.print(f"  FAIL {x['name']}: {x['detail']}")
    else:
        output.success(f"OntologyGraph 验证全部通过 ({passed}/{len(results)})")
    output.print("__JSON_SUMMARY__" + json.dumps(summary_out, ensure_ascii=True))
