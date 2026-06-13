"""本体引擎测试空间元数据灌入 — space__onto_engine_test

维度层级 + 成员同义词 + 决策规则 + 同义词缓存刷新。
前置：init + seed 已完成。
"""

import json

ENTITY_QN_PREFIX = "__dazi_ontology_v2__.entity."
ATTRIBUTE_QN_PREFIX = "__dazi_ontology_v2__.attribute."


def main():
    space_id = "space__onto_engine_test"
    s = space.get(space_id)
    output.print("=== 本体引擎测试空间元数据灌入 ===")

    # 1. 维度层级（G2 drill_path）
    output.print("\n[1/4] 维度层级...")
    h1 = s.ontology.upsert_dimension_hierarchy("组织层级", [
        {"dim": "CostCube.org_id", "label": "项目部"},
        {"dim": "CostCube.parent_org_id", "label": "分公司"},
    ])
    h2 = s.ontology.upsert_dimension_hierarchy("科目层级", [
        {"dim": "CostCube.cost_type_id", "label": "子科目"},
        {"dim": "CostCube.parent_cost_type_id", "label": "大类"},
    ])
    h3 = s.ontology.upsert_dimension_hierarchy("地域层级", [
        {"dim": "CostCube.project_id", "label": "项目"},
        {"dim": "CostCube.region", "label": "片区"},
    ])
    output.print(f"OK 层级关系 {h1 + h2 + h3} 条")

    # 2. 成员同义词
    output.print("\n[2/4] 成员同义词...")
    # 对象级同义词（entity QN）
    proj_oid = None
    cost_prop_id = None
    for ot in s.onto.list_object_types():
        if ot.get("code") == "Project":
            proj_oid = ot.get("id")
            break
    for p in s.onto.list_properties("Project"):
        if p.get("code") == "cost":
            cost_prop_id = p.get("id")
            break
    syn_count = 0
    syn_map = {}
    if proj_oid:
        entity_qn = f"{ENTITY_QN_PREFIX}{proj_oid}"
        for syn in ["工程", "项目部工程"]:
            s.ontology.remove_synonym(entity_qn, syn)
        syn_map[entity_qn] = ["工程", "项目部工程"]
    if cost_prop_id:
        attr_qn = f"{ATTRIBUTE_QN_PREFIX}{cost_prop_id}"
        for syn in ["花费", "开销", "成本额"]:
            s.ontology.remove_synonym(attr_qn, syn)
            s.ontology.remove_synonym("CostCube.cost_amount_total", syn)
        syn_map[attr_qn] = ["花费", "开销", "成本额"]
    syn_map.update({
        "CostCube.region": ["地区", "片区"],
        "OutputCube.output_amount_total": ["产值额", "营收"],
    })
    if syn_map:
        syn_count += s.ontology.add_synonyms_batch(syn_map)
    output.print(f"OK 同义词 {syn_count} 条")

    # 3. 同义词缓存刷新（引擎读 aliases 列）
    output.print("\n[3/4] 刷新同义词缓存...")
    cache_stats = s.ontology.refresh_synonym_caches()
    output.print(f"OK 对象 {cache_stats['objects']} / 属性 {cache_stats['properties']} 缓存已刷新")

    # 4. 决策规则（G3）
    output.print("\n[4/4] 决策规则...")
    rs_id = s.ontology_rules.ensure_rule_set("本体引擎测试规则集", "引擎 G3 决策验证")
    CC = "CostCube"

    rules = [
        {
            "rule_code": "rank_cost_topn",
            "rule_name": "成本排名 Top-N",
            "rule_type": "decision",
            "priority": 10,
            "description": "问句含成本排名意图时改写为 rank_query",
            "triggers": [{
                "trigger_scope": "query_intent",
                "match_mode": "any",
                "condition_dsl": {
                    "match_mode": "any",
                    "question_patterns": [
                        r".*成本.*(最高|前\d+|top).*",
                        r".*前\d+.*(项目|成本).*",
                    ],
                },
            }],
            "actions": [{
                "action_type": "rewrite_query",
                "order_no": 1,
                "action_config": {
                    "query_policy": {
                        "intent_type": "rank_query",
                        "order": "desc",
                        "limit_default": 5,
                    },
                },
            }],
        },
        {
            "rule_code": "cost_overrun_alert",
            "rule_name": "成本超支预警",
            "rule_type": "decision",
            "priority": 20,
            "description": "预算执行率超 100% 时预警",
            "triggers": [{
                "trigger_scope": "metric_threshold",
                "match_mode": "all",
                "condition_dsl": {
                    "thresholds": [
                        {"metric": "budget_exec_rate", "op": "gt", "value": 1.0},
                    ],
                },
            }],
            "actions": [{
                "action_type": "emit_alert",
                "order_no": 1,
                "action_config": {
                    "alert_level": "warn",
                    "alert_message": "成本超支",
                    "derived_facts": {
                        "cost_overrun_alert": True,
                        "alert_level": "overrun",
                    },
                },
            }],
        },
        {
            "rule_code": "high_cost_risk_l2",
            "rule_name": "华东超支高风险",
            "rule_type": "decision",
            "priority": 30,
            "description": "超支预警 + 华东片区 → 高风险分级",
            "triggers": [{
                "trigger_scope": "context",
                "match_mode": "all",
                "condition_dsl": {
                    "required_context_keys": ["cost_overrun_alert"],
                    "match_scope": {"region": "华东"},
                },
            }],
            "actions": [{
                "action_type": "route_recipe",
                "order_no": 1,
                "action_config": {
                    "risk_level": "高",
                    "derived_facts": {"risk_level": "高"},
                },
            }],
        },
        {
            "rule_code": "cost_priority_conflict",
            "rule_name": "成本排名冲突规则",
            "rule_type": "decision",
            "priority": 50,
            "description": "与 rank_cost_topn 同触发，用于冲突消解测试",
            "triggers": [{
                "trigger_scope": "query_intent",
                "match_mode": "any",
                "condition_dsl": {
                    "match_mode": "any",
                    "question_patterns": [r".*成本.*最高.*"],
                },
            }],
            "actions": [{
                "action_type": "annotate",
                "order_no": 1,
                "action_config": {"note": "冲突标注规则"},
            }],
        },
    ]
    rule_ids = []
    for spec in rules:
        rid = s.ontology_rules.upsert_rule(rule_set_id=rs_id, **spec)
        rule_ids.append(rid)
    output.print(f"OK 规则 {len(rule_ids)} 条")

    s.onto.engine.invalidate()
    output.print("OK 引擎图谱缓存失效")

    summary = {
        "ok": True,
        "hierarchies": h1 + h2 + h3,
        "synonyms": syn_count,
        "rules": len(rule_ids),
        "rule_set_id": rs_id,
    }
    output.success("元数据灌入完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True))

