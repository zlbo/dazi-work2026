"""化工设备运营分析 — 347 分类挂载（init + seed + 全部函数 publish 之后执行）

放置：项目/DAZI_TEST/本体/ontos/设备运营/setup/equip_ops_category_mount.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/设备运营/setup/equip_ops_category_mount.py --space space_cate_test01 --type setup
规划对照：项目/DAZI_TEST/本体/ontos/设备运营/plans/化工设备运营分析本体方案.md 附录 B
"""

import json

CATEGORY_REGISTRY = {
    "table": {
        "维度表": [
            "dim_plant",
            "dim_process_unit",
            "dim_equipment_type",
            "dim_equipment",
            "dim_downtime_reason",
        ],
        "事实表": [
            "fact_equipment_daily_ops",
            "fact_downtime_event",
            "fact_maintenance_record",
            "fact_equipment_plan",
        ],
    },
    "cube": {
        "流程型": ["OperationCube", "DowntimeCube", "MaintenanceCube"],
        "主体型": ["EquipmentCube", "PlantCube", "ProcessUnitCube"],
        "对比型": ["PlanVsActualCube"],
    },
    "object": {
        "主数据": ["Plant", "ProcessUnit", "EquipmentType", "Equipment"],
        "参考": ["DowntimeReason"],
        "事务": ["OperationSnapshot", "DowntimeEvent", "MaintenanceRecord"],
        "分析": ["EquipmentAnalysis", "PlanAnalysis"],
    },
    "relation": {
        "时间关联": [
            ("fact_equipment_daily_ops", "dim_date"),
            ("fact_downtime_event", "dim_date"),
            ("fact_maintenance_record", "dim_date"),
            ("fact_equipment_plan", "dim_date"),
        ],
        "主数据关联": [
            ("dim_process_unit", "dim_plant"),
            ("dim_equipment", "dim_equipment_type"),
            ("dim_equipment", "dim_plant"),
            ("dim_equipment", "dim_process_unit"),
            ("fact_equipment_daily_ops", "dim_equipment"),
            ("fact_downtime_event", "dim_equipment"),
            ("fact_downtime_event", "dim_downtime_reason"),
            ("fact_maintenance_record", "dim_equipment"),
            ("fact_equipment_plan", "dim_equipment"),
        ],
        "层级自关联": [
            ("dim_equipment_type", "dim_equipment_type"),
            ("dim_downtime_reason", "dim_downtime_reason"),
        ],
        "预实关联": [
            ("fact_equipment_plan", "fact_equipment_daily_ops"),
        ],
    },
    "link": {
        "归属关系": [
            "unit_belongs_plant",
            "equipment_belongs_plant",
            "equipment_belongs_unit",
            "equipment_has_type",
            "snapshot_for_equipment",
            "downtime_on_equipment",
            "downtime_has_reason",
            "maint_for_equipment",
        ],
        "层级关系": ["equip_type_has_parent", "reason_has_parent"],
        "对比关系": ["plan_compared_to_actual"],
        "分析归因": [
            "analysis_by_equipment",
            "analysis_by_plant",
            "analysis_by_unit",
            "analysis_by_downtime",
            "analysis_by_maintenance",
        ],
    },
    "function": {
        "总览分析": ["equip_ops.fn.get_summary", "equip_ops.fn.oee_analysis"],
        "趋势分析": ["equip_ops.fn.yoy_analysis", "equip_ops.fn.mom_analysis"],
        "结构分析": [
            "equip_ops.fn.availability_analysis",
            "equip_ops.fn.downtime_breakdown",
            "equip_ops.fn.top_fault_equipment",
            "equip_ops.fn.energy_intensity",
        ],
        "预实分析": ["equip_ops.fn.plan_vs_actual"],
        "组织分析": ["equip_ops.fn.maintenance_compliance", "equip_ops.fn.unit_comparison"],
    },
}


def main():
    space_id = "space_cate_test01"
    s = space.get(space_id)
    output.print("=== 化工设备运营分析 — 347 分类挂载 ===")
    cat_counts = s.categories.apply_registry(CATEGORY_REGISTRY, skip_missing=True)
    output.print(f"OK 分类挂载: {json.dumps(cat_counts, ensure_ascii=True)}")
    output.success("分类挂载完成")
    output.print("__JSON_SUMMARY__" + json.dumps({"ok": True, "category_mounts": cat_counts}, ensure_ascii=True, default=str))
