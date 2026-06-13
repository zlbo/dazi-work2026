"""本体引擎测试空间 — 本体函数锚定与分类挂载（幂等）

前置：
  1. init + seed + meta_seed 已完成
  2. 已对各 functions/*.py 执行 publish（见 README 发布命令）

本脚本：为已注册的 onto_engine.fn.* 写入 object_type_id、display_name，并挂载平台分类。
"""

import json

_ADAPTER = "dazi_script.ontology_function"

# function_id, 脚本 file_stem, 锚定对象 code, 显示名, 平台分类
# 平台 function 分类仅支持：总览分析 / 趋势分析 / 结构分析 / 预实分析 / 组织分析
FUNCTION_BINDINGS = [
    ("onto_engine.fn.get_summary", "onto_engine_fn_get_summary", "CostAnalysis", "空间总览汇总", "总览分析"),
    ("onto_engine.fn.project_summary", "onto_engine_fn_project_summary", "Project", "项目成本产值汇总", "组织分析"),
    ("onto_engine.fn.region_cost", "onto_engine_fn_region_cost", "Project", "片区成本汇总", "组织分析"),
    ("onto_engine.fn.budget_vs_actual", "onto_engine_fn_budget_vs_actual", "CostAnalysis", "项目预实对比", "预实分析"),
    ("onto_engine.fn.top_cost_projects", "onto_engine_fn_top_cost_projects", "Project", "成本 Top-N 项目", "结构分析"),
    ("onto_engine.fn.cost_extremes", "onto_engine_fn_cost_extremes", "Project", "成本极值与差值", "结构分析"),
    ("onto_engine.fn.cost_structure", "onto_engine_fn_cost_structure", "CostRecord", "成本科目结构", "结构分析"),
]


def _find_script_id(s, file_stem: str) -> str:
    """从 ads_scripts 按 file_stem 解析 script_id。"""
    stem = (file_stem or "").strip()
    for row in s.scripts.list(script_type="ontology_function", keyword=stem, limit=50):
        if (row.get("file_stem") or "").strip() == stem:
            return str(row.get("id") or "").strip()
    return ""

FUNCTION_CATEGORY_REGISTRY = {
    "function": {
        "总览分析": ["onto_engine.fn.get_summary"],
        "组织分析": ["onto_engine.fn.project_summary", "onto_engine.fn.region_cost"],
        "预实分析": ["onto_engine.fn.budget_vs_actual"],
        "结构分析": [
            "onto_engine.fn.top_cost_projects",
            "onto_engine.fn.cost_extremes",
            "onto_engine.fn.cost_structure",
        ],
    },
}


def main():
    space_id = "space__onto_engine_test"
    s = space.get(space_id)
    output.print("=== 本体引擎测试空间 · 函数锚定 ===")

    ots = {r["code"]: r["id"] for r in s.onto.list_object_types() if r.get("code")}
    reg = s.onto.list_registry()
    fn_by_id = {f.get("function_id"): f for f in (reg.get("functions") or []) if f.get("function_id")}

    bound = []
    missing = []
    for fid, file_stem, ot_code, display_name, category in FUNCTION_BINDINGS:
        if fid not in fn_by_id:
            missing.append(fid)
            output.print(f"  跳过（未 publish）: {fid}")
            continue
        script_id = _find_script_id(s, file_stem)
        if not script_id:
            missing.append(fid)
            output.print(f"  跳过（未找到脚本）: {fid} stem={file_stem}")
            continue
        ot_id = ots.get(ot_code)
        if not ot_id:
            output.print(f"  错误：对象类型不存在 {ot_code}")
            continue
        adapter_cfg = {"script_id": script_id, "entry": "main"}
        out = s.onto.register_function(
            fid,
            _ADAPTER,
            adapter_config=adapter_cfg,
            description=display_name,
            enabled=True,
            object_type_id=ot_id,
            script_id=script_id,
            entry="main",
            display_name=display_name,
            category_347=category,
        )
        bound.append({"function_id": fid, "object_type_code": ot_code, **out})
        output.print(f"  OK {fid} → {ot_code} ({category})")

    output.print("\n[分类挂载] function 平台分类...")
    cat_res = s.categories.apply_registry(
        {"function": FUNCTION_CATEGORY_REGISTRY["function"]},
        skip_missing=True,
    )

    s.onto.engine.invalidate()
    output.print("OK 引擎图谱缓存失效")

    summary = {
        "ok": True,
        "bound": len(bound),
        "missing_publish": missing,
        "category_mounts": cat_res,
    }
    if missing:
        output.print(f"提示：请先 publish 缺失函数: {', '.join(missing)}")
    output.success(f"函数锚定完成 bound={len(bound)} missing={len(missing)}")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True))
