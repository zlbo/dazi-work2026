"""本体引擎测试空间 — 函数意图补充规则（G3）

与 onto_engine.fn.* 互补：问句命中时写入 derived_facts / annotate，供决策链与 LLM 上下文参考。
前置：meta_seed 规则集已存在；functions_register 可选。
"""

import json

FUNCTION_HINT_RULES = [
    {
        "rule_code": "fn_hint_region_cost",
        "rule_name": "片区分析函数提示",
        "rule_type": "decision",
        "priority": 15,
        "description": "按片区/地区问成本时，建议 onto_engine.fn.region_cost",
        "triggers": [{
            "trigger_scope": "query_intent",
            "match_mode": "any",
            "condition_dsl": {
                "match_mode": "any",
                "question_patterns": [
                    r".*按(片区|地区|区域).*",
                    r".*(各)?片区.*(成本|开销|花费).*",
                ],
            },
        }],
        "actions": [{
            "action_type": "annotate",
            "order_no": 1,
            "action_config": {
                "note": "推荐本体函数 onto_engine.fn.region_cost",
                "derived_facts": {
                    "suggested_function_id": "onto_engine.fn.region_cost",
                    "analysis_mode": "region_breakdown",
                },
            },
        }],
    },
    {
        "rule_code": "fn_hint_budget_vs_actual",
        "rule_name": "预实对比函数提示",
        "rule_type": "decision",
        "priority": 16,
        "description": "预实/超支问法时，建议 onto_engine.fn.budget_vs_actual",
        "triggers": [{
            "trigger_scope": "query_intent",
            "match_mode": "any",
            "condition_dsl": {
                "match_mode": "any",
                "question_patterns": [
                    r".*(预实|预算执行|超支|执行率).*",
                    r".*预算.*(对比|偏差).*",
                ],
            },
        }],
        "actions": [{
            "action_type": "annotate",
            "order_no": 1,
            "action_config": {
                "note": "推荐本体函数 onto_engine.fn.budget_vs_actual",
                "derived_facts": {
                    "suggested_function_id": "onto_engine.fn.budget_vs_actual",
                    "analysis_mode": "budget_vs_actual",
                },
            },
        }],
    },
    {
        "rule_code": "fn_hint_project_summary",
        "rule_name": "项目汇总函数提示",
        "rule_type": "decision",
        "priority": 17,
        "description": "各项目成本产值汇总问法",
        "triggers": [{
            "trigger_scope": "query_intent",
            "match_mode": "any",
            "condition_dsl": {
                "match_mode": "any",
                "question_patterns": [
                    r".*各项目.*(成本|产值|利润).*",
                    r".*项目.*(汇总|一览|明细).*",
                ],
            },
        }],
        "actions": [{
            "action_type": "annotate",
            "order_no": 1,
            "action_config": {
                "note": "推荐本体函数 onto_engine.fn.project_summary",
                "derived_facts": {
                    "suggested_function_id": "onto_engine.fn.project_summary",
                    "analysis_mode": "project_summary",
                },
            },
        }],
    },
    {
        "rule_code": "fn_hint_cost_extremes",
        "rule_name": "成本极值差值函数提示",
        "rule_type": "decision",
        "priority": 14,
        "description": "成本最高+最低及差值问法时，建议 onto_engine.fn.cost_extremes",
        "triggers": [{
            "trigger_scope": "query_intent",
            "match_mode": "any",
            "condition_dsl": {
                "match_mode": "any",
                "question_patterns": [
                    r".*(最前|最后|最高|最低).*(差|差值|差距).*",
                    r".*(排最前|排最后).*(哪|哪两|哪几个).*",
                    r".*(最高|最低).*(项目|成本).*(差|差值).*",
                ],
            },
        }],
        "actions": [{
            "action_type": "annotate",
            "order_no": 1,
            "action_config": {
                "note": "推荐本体函数 onto_engine.fn.cost_extremes",
                "derived_facts": {
                    "suggested_function_id": "onto_engine.fn.cost_extremes",
                    "analysis_mode": "cost_extremes_gap",
                },
            },
        }],
    },
    {
        "rule_code": "fn_hint_cost_structure",
        "rule_name": "科目结构函数提示",
        "rule_type": "decision",
        "priority": 18,
        "description": "成本结构/科目构成问法",
        "triggers": [{
            "trigger_scope": "query_intent",
            "match_mode": "any",
            "condition_dsl": {
                "match_mode": "any",
                "question_patterns": [
                    r".*(成本结构|科目构成|费用构成).*",
                    r".*按(科目|成本类型).*",
                ],
            },
        }],
        "actions": [{
            "action_type": "annotate",
            "order_no": 1,
            "action_config": {
                "note": "推荐本体函数 onto_engine.fn.cost_structure",
                "derived_facts": {
                    "suggested_function_id": "onto_engine.fn.cost_structure",
                    "analysis_mode": "cost_structure",
                },
            },
        }],
    },
]


def main():
    space_id = "space__onto_engine_test"
    s = space.get(space_id)
    output.print("=== 本体引擎测试空间 · 函数意图规则 ===")

    rs_id = s.ontology_rules.ensure_rule_set("本体引擎测试规则集", "引擎 G3 决策验证")
    rule_ids = []
    for spec in FUNCTION_HINT_RULES:
        rid = s.ontology_rules.upsert_rule(rule_set_id=rs_id, **spec)
        rule_ids.append(rid)
        output.print(f"  OK {spec['rule_code']}")

    s.onto.engine.invalidate()
    summary = {"ok": True, "rules_added": len(rule_ids), "rule_set_id": rs_id}
    output.success(f"函数意图规则 {len(rule_ids)} 条")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True))
