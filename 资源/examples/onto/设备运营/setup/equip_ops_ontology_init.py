"""化工设备运营分析本体初始化脚本 — space_cate_test01

初始化内容：
1. 创建物理表（5 维 + 4 事实，不含 dim_date）
2. 注册表到空间（含 display_name / description）
3. 注册表间关系（16 条，含 4 条 fact→dim_date）
4. 注册 Cube（7 个）及派生度量
5. 定义对象类型（10 种）、绑定数据源、属性、链接（16 种）
6. 同步指标引用
7. 输出 JSON summary

不含 apply_registry（分类在 equip_ops_category_mount.py）。

放置：项目/DAZI_TEST/本体/ontos/设备运营/setup/equip_ops_ontology_init.py
发布：dazi onto script publish 项目/DAZI_TEST/本体/ontos/设备运营/setup/equip_ops_ontology_init.py --space space_cate_test01 --type setup
规划对照：项目/DAZI_TEST/本体/ontos/设备运营/plans/化工设备运营分析本体方案.md
"""

import json

# 与规划文档 §2 对齐：display_name=侧栏显示名，description=业务说明
TABLE_REGISTRY = {
    "dim_plant": {
        "display_name": "厂区维表",
        "description": "化工生产厂区或大型装置区主数据",
        "columns": [
            {"name": "plant_id", "display_name": "厂区 ID", "description": "主键"},
            {"name": "plant_code", "display_name": "厂区编码"},
            {"name": "plant_name", "display_name": "厂区名称"},
            {"name": "company_code", "display_name": "公司代码"},
            {"name": "plant_type", "display_name": "装置类型", "description": "炼油/烯烃/芳烃/精细化工"},
            {"name": "location", "display_name": "地理位置"},
            {"name": "design_capacity", "display_name": "设计产能"},
            {"name": "capacity_unit", "display_name": "产能单位"},
            {"name": "status", "display_name": "状态", "description": "运行/检修/停产"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_process_unit": {
        "display_name": "工艺单元维表",
        "description": "装置内工艺单元（蒸馏、反应、压缩等工段）",
        "columns": [
            {"name": "unit_id", "display_name": "单元 ID", "description": "主键"},
            {"name": "unit_code", "display_name": "单元编码"},
            {"name": "unit_name", "display_name": "单元名称"},
            {"name": "plant_id", "display_name": "所属厂区", "description": "关联 dim_plant"},
            {"name": "plant_name", "display_name": "厂区名称", "description": "冗余"},
            {"name": "unit_type", "display_name": "单元类型", "description": "反应/分离/换热/公用工程"},
            {"name": "criticality", "display_name": "关键等级", "description": "A/B/C"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_equipment_type": {
        "display_name": "设备类型维表",
        "description": "设备分类主数据（泵、压缩机、反应釜、塔器等）",
        "columns": [
            {"name": "equip_type_id", "display_name": "类型 ID", "description": "主键"},
            {"name": "equip_type_code", "display_name": "类型编码"},
            {"name": "equip_type_name", "display_name": "类型名称"},
            {"name": "category", "display_name": "大类", "description": "动设备/静设备/仪表/电气"},
            {"name": "parent_type_id", "display_name": "上级类型", "description": "自关联"},
            {"name": "type_level", "display_name": "层级"},
            {"name": "is_leaf", "display_name": "末级"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_equipment": {
        "display_name": "设备主数据",
        "description": "单台设备台账；OEE 与停机分析的核心维度",
        "columns": [
            {"name": "equipment_id", "display_name": "设备 ID", "description": "主键"},
            {"name": "equipment_code", "display_name": "设备位号", "description": "如 P-101A"},
            {"name": "equipment_name", "display_name": "设备名称"},
            {"name": "equip_type_id", "display_name": "设备类型", "description": "关联 dim_equipment_type"},
            {"name": "equip_type_name", "display_name": "类型名称", "description": "冗余"},
            {"name": "category", "display_name": "设备大类", "description": "冗余"},
            {"name": "plant_id", "display_name": "所属厂区", "description": "关联 dim_plant"},
            {"name": "plant_name", "display_name": "厂区名称", "description": "冗余"},
            {"name": "unit_id", "display_name": "所属单元", "description": "关联 dim_process_unit"},
            {"name": "unit_name", "display_name": "单元名称", "description": "冗余"},
            {"name": "manufacturer", "display_name": "制造商"},
            {"name": "model", "display_name": "型号"},
            {"name": "install_date", "display_name": "投运日期"},
            {"name": "design_capacity", "display_name": "设计能力"},
            {"name": "capacity_unit", "display_name": "能力单位", "description": "t/h、m³/h 等"},
            {"name": "criticality", "display_name": "关键等级", "description": "A/B/C"},
            {"name": "production_mode", "display_name": "生产模式", "description": "连续/间歇"},
            {"name": "status", "display_name": "状态", "description": "运行/备用/检修/报废"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_downtime_reason": {
        "display_name": "停机原因维表",
        "description": "停机/故障原因码表",
        "columns": [
            {"name": "reason_id", "display_name": "原因 ID", "description": "主键"},
            {"name": "reason_code", "display_name": "原因编码"},
            {"name": "reason_name", "display_name": "原因名称"},
            {"name": "reason_category", "display_name": "原因大类", "description": "机械/电气/仪表/工艺/计划检修/外部"},
            {"name": "is_planned", "display_name": "是否计划停机", "description": "0/1"},
            {"name": "parent_reason_id", "display_name": "上级原因", "description": "自关联"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_equipment_daily_ops": {
        "display_name": "设备日运行汇总",
        "description": "每台设备每日运行 KPI 汇总；OEE 计算主源",
        "columns": [
            {"name": "ops_id", "display_name": "汇总 ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date，YYYYMMDD"},
            {"name": "calendar_date", "display_name": "统计日期"},
            {"name": "equipment_id", "display_name": "设备 ID", "description": "关联 dim_equipment"},
            {"name": "equipment_code", "display_name": "设备位号", "description": "冗余"},
            {"name": "equipment_name", "display_name": "设备名称", "description": "冗余"},
            {"name": "plant_id", "display_name": "厂区 ID", "description": "冗余"},
            {"name": "plant_name", "display_name": "厂区名称", "description": "冗余"},
            {"name": "unit_id", "display_name": "单元 ID", "description": "冗余"},
            {"name": "unit_name", "display_name": "单元名称", "description": "冗余"},
            {"name": "equip_type_id", "display_name": "设备类型", "description": "冗余"},
            {"name": "category", "display_name": "设备大类", "description": "冗余"},
            {"name": "calendar_minutes", "display_name": "日历时间", "description": "分钟"},
            {"name": "planned_downtime_min", "display_name": "计划停机", "description": "分钟"},
            {"name": "unplanned_downtime_min", "display_name": "非计划停机", "description": "分钟"},
            {"name": "runtime_min", "display_name": "运行时间", "description": "分钟"},
            {"name": "idle_min", "display_name": "待机时间", "description": "分钟"},
            {"name": "planned_output_qty", "display_name": "计划产量"},
            {"name": "actual_output_qty", "display_name": "实际产量"},
            {"name": "qualified_output_qty", "display_name": "合格产量"},
            {"name": "output_unit", "display_name": "产量单位"},
            {"name": "ideal_cycle_rate", "display_name": "理想节拍", "description": "单位/分钟"},
            {"name": "energy_consumption", "display_name": "能耗", "description": "kWh 或 GJ"},
            {"name": "energy_unit", "display_name": "能耗单位"},
            {"name": "shift_code", "display_name": "班次", "description": "早/中/晚/全天"},
            {"name": "data_source", "display_name": "数据来源", "description": "DCS/MES/手工"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_downtime_event": {
        "display_name": "停机事件明细",
        "description": "单次停机/故障事件流水",
        "columns": [
            {"name": "event_id", "display_name": "事件 ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date（事件开始日）"},
            {"name": "equipment_id", "display_name": "设备 ID", "description": "关联 dim_equipment"},
            {"name": "equipment_code", "display_name": "设备位号", "description": "冗余"},
            {"name": "equipment_name", "display_name": "设备名称", "description": "冗余"},
            {"name": "plant_id", "display_name": "厂区 ID", "description": "冗余"},
            {"name": "unit_id", "display_name": "单元 ID", "description": "冗余"},
            {"name": "reason_id", "display_name": "停机原因", "description": "关联 dim_downtime_reason"},
            {"name": "reason_code", "display_name": "原因编码", "description": "冗余"},
            {"name": "reason_name", "display_name": "原因名称", "description": "冗余"},
            {"name": "reason_category", "display_name": "原因大类", "description": "冗余"},
            {"name": "is_planned", "display_name": "是否计划停机", "description": "0/1"},
            {"name": "start_time", "display_name": "开始时间"},
            {"name": "end_time", "display_name": "结束时间"},
            {"name": "duration_min", "display_name": "停机时长", "description": "分钟"},
            {"name": "impact_level", "display_name": "影响等级", "description": "高/中/低"},
            {"name": "responsible_dept", "display_name": "责任部门", "description": "机动/电气/仪表/生产"},
            {"name": "description", "display_name": "事件描述"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_maintenance_record": {
        "display_name": "维保记录",
        "description": "计划与实际维保作业记录",
        "columns": [
            {"name": "maint_id", "display_name": "维保 ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date（计划或完成日）"},
            {"name": "equipment_id", "display_name": "设备 ID", "description": "关联 dim_equipment"},
            {"name": "equipment_code", "display_name": "设备位号", "description": "冗余"},
            {"name": "plant_id", "display_name": "厂区 ID", "description": "冗余"},
            {"name": "unit_id", "display_name": "单元 ID", "description": "冗余"},
            {"name": "maint_type", "display_name": "维保类型", "description": "预防/预测/故障维修/大修"},
            {"name": "plan_date", "display_name": "计划日期"},
            {"name": "actual_date", "display_name": "实际完成日期", "description": "可空"},
            {"name": "plan_hours", "display_name": "计划工时"},
            {"name": "actual_hours", "display_name": "实际工时"},
            {"name": "plan_cost", "display_name": "计划费用"},
            {"name": "actual_cost", "display_name": "实际费用"},
            {"name": "status", "display_name": "状态", "description": "计划/进行中/完成/逾期"},
            {"name": "is_on_schedule", "display_name": "是否按期", "description": "1=按期完成"},
            {"name": "vendor", "display_name": "维保单位"},
            {"name": "description", "display_name": "作业内容"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_equipment_plan": {
        "display_name": "设备运行计划",
        "description": "计划运行时间/产量，用于计划 vs 实际对比",
        "columns": [
            {"name": "plan_id", "display_name": "计划 ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date"},
            {"name": "equipment_id", "display_name": "设备 ID", "description": "关联 dim_equipment"},
            {"name": "equipment_code", "display_name": "设备位号", "description": "冗余"},
            {"name": "plant_id", "display_name": "厂区 ID", "description": "冗余"},
            {"name": "unit_id", "display_name": "单元 ID", "description": "冗余"},
            {"name": "plan_version", "display_name": "计划版本", "description": "如 2026月度计划"},
            {"name": "fiscal_year", "display_name": "计划年度"},
            {"name": "fiscal_month", "display_name": "计划月份", "description": "1-12"},
            {"name": "planned_runtime_min", "display_name": "计划运行时间", "description": "分钟"},
            {"name": "planned_output_qty", "display_name": "计划产量"},
            {"name": "planned_energy", "display_name": "计划能耗"},
            {"name": "output_unit", "display_name": "产量单位"},
            {"name": "status", "display_name": "状态", "description": "草稿/已发布"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
}


def main():
    space_id = "space_cate_test01"
    s = space.get(space_id)

    output.print("=== 化工设备运营分析本体初始化 ===")
    output.print(f"空间: {space_id}")

    # 1. 创建物理表
    output.print("\n[1/8] 创建物理表...")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_plant (
            plant_id String,
            plant_code String,
            plant_name String,
            company_code String,
            plant_type String,
            location String,
            design_capacity Float64,
            capacity_unit String,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (plant_code)
    """)
    output.print("OK dim_plant")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_process_unit (
            unit_id String,
            unit_code String,
            unit_name String,
            plant_id String,
            plant_name String,
            unit_type String,
            criticality String,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (plant_id, unit_code)
    """)
    output.print("OK dim_process_unit")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_equipment_type (
            equip_type_id String,
            equip_type_code String,
            equip_type_name String,
            category String,
            parent_type_id String,
            type_level Int32,
            is_leaf Boolean,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (equip_type_code)
    """)
    output.print("OK dim_equipment_type")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_equipment (
            equipment_id String,
            equipment_code String,
            equipment_name String,
            equip_type_id String,
            equip_type_name String,
            category String,
            plant_id String,
            plant_name String,
            unit_id String,
            unit_name String,
            manufacturer String,
            model String,
            install_date Date,
            design_capacity Float64,
            capacity_unit String,
            criticality String,
            production_mode String,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (plant_id, unit_id, equipment_code)
    """)
    output.print("OK dim_equipment")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_downtime_reason (
            reason_id String,
            reason_code String,
            reason_name String,
            reason_category String,
            is_planned UInt8,
            parent_reason_id String,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (reason_code)
    """)
    output.print("OK dim_downtime_reason")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_equipment_daily_ops (
            ops_id String,
            date_key Int32,
            calendar_date Date,
            equipment_id String,
            equipment_code String,
            equipment_name String,
            plant_id String,
            plant_name String,
            unit_id String,
            unit_name String,
            equip_type_id String,
            category String,
            calendar_minutes Float64,
            planned_downtime_min Float64,
            unplanned_downtime_min Float64,
            runtime_min Float64,
            idle_min Float64,
            planned_output_qty Float64,
            actual_output_qty Float64,
            qualified_output_qty Float64,
            output_unit String,
            ideal_cycle_rate Float64,
            energy_consumption Float64,
            energy_unit String,
            shift_code String,
            data_source String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (date_key, equipment_id, shift_code)
    """)
    output.print("OK fact_equipment_daily_ops")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_downtime_event (
            event_id String,
            date_key Int32,
            equipment_id String,
            equipment_code String,
            equipment_name String,
            plant_id String,
            unit_id String,
            reason_id String,
            reason_code String,
            reason_name String,
            reason_category String,
            is_planned UInt8,
            start_time DateTime,
            end_time DateTime,
            duration_min Float64,
            impact_level String,
            responsible_dept String,
            description String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (date_key, equipment_id, start_time)
    """)
    output.print("OK fact_downtime_event")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_maintenance_record (
            maint_id String,
            date_key Int32,
            equipment_id String,
            equipment_code String,
            plant_id String,
            unit_id String,
            maint_type String,
            plan_date Date,
            actual_date Nullable(Date),
            plan_hours Float64,
            actual_hours Float64,
            plan_cost Float64,
            actual_cost Float64,
            status String,
            is_on_schedule UInt8,
            vendor String,
            description String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (date_key, equipment_id, maint_id)
    """)
    output.print("OK fact_maintenance_record")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_equipment_plan (
            plan_id String,
            date_key Int32,
            equipment_id String,
            equipment_code String,
            plant_id String,
            unit_id String,
            plan_version String,
            fiscal_year Int32,
            fiscal_month Int32,
            planned_runtime_min Float64,
            planned_output_qty Float64,
            planned_energy Float64,
            output_unit String,
            status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (fiscal_year, fiscal_month, equipment_id, plan_id)
    """)
    output.print("OK fact_equipment_plan")

    # 2. 注册表（含 display_name / description）
    output.print("\n[2/8] 注册表到空间...")

    for tbl_name, meta in TABLE_REGISTRY.items():
        s.tables.register_with_meta(
            table_name=tbl_name,
            display_name=meta["display_name"],
            description=meta.get("description"),
            columns=meta["columns"],
            force_column_meta=True,
        )
        output.print(f"OK {tbl_name} ({meta['display_name']})")

    # 3. 注册表间关系（16 条，规划 §三）
    output.print("\n[3/8] 注册表间关系...")

    table_relationships = [
        {
            "from_table": "fact_equipment_daily_ops",
            "to_table": "dim_date",
            "join_sql": "fact_equipment_daily_ops.date_key = dim_date.date_key",
            "join_keys": [{"from": "date_key", "to": "date_key"}],
            "relationship_type": "many_to_one",
            "description": "日运行→日历",
        },
        {
            "from_table": "fact_downtime_event",
            "to_table": "dim_date",
            "join_sql": "fact_downtime_event.date_key = dim_date.date_key",
            "join_keys": [{"from": "date_key", "to": "date_key"}],
            "relationship_type": "many_to_one",
            "description": "停机→日历",
        },
        {
            "from_table": "fact_maintenance_record",
            "to_table": "dim_date",
            "join_sql": "fact_maintenance_record.date_key = dim_date.date_key",
            "join_keys": [{"from": "date_key", "to": "date_key"}],
            "relationship_type": "many_to_one",
            "description": "维保→日历",
        },
        {
            "from_table": "fact_equipment_plan",
            "to_table": "dim_date",
            "join_sql": "fact_equipment_plan.date_key = dim_date.date_key",
            "join_keys": [{"from": "date_key", "to": "date_key"}],
            "relationship_type": "many_to_one",
            "description": "计划→日历",
        },
        {
            "from_table": "dim_process_unit",
            "to_table": "dim_plant",
            "join_sql": "dim_process_unit.plant_id = dim_plant.plant_id",
            "join_keys": [{"from": "plant_id", "to": "plant_id"}],
            "relationship_type": "many_to_one",
            "description": "单元→厂区",
        },
        {
            "from_table": "dim_equipment",
            "to_table": "dim_equipment_type",
            "join_sql": "dim_equipment.equip_type_id = dim_equipment_type.equip_type_id",
            "join_keys": [{"from": "equip_type_id", "to": "equip_type_id"}],
            "relationship_type": "many_to_one",
            "description": "设备→类型",
        },
        {
            "from_table": "dim_equipment",
            "to_table": "dim_plant",
            "join_sql": "dim_equipment.plant_id = dim_plant.plant_id",
            "join_keys": [{"from": "plant_id", "to": "plant_id"}],
            "relationship_type": "many_to_one",
            "description": "设备→厂区",
        },
        {
            "from_table": "dim_equipment",
            "to_table": "dim_process_unit",
            "join_sql": "dim_equipment.unit_id = dim_process_unit.unit_id",
            "join_keys": [{"from": "unit_id", "to": "unit_id"}],
            "relationship_type": "many_to_one",
            "description": "设备→单元",
        },
        {
            "from_table": "fact_equipment_daily_ops",
            "to_table": "dim_equipment",
            "join_sql": "fact_equipment_daily_ops.equipment_id = dim_equipment.equipment_id",
            "join_keys": [{"from": "equipment_id", "to": "equipment_id"}],
            "relationship_type": "many_to_one",
            "description": "日运行→设备",
        },
        {
            "from_table": "fact_downtime_event",
            "to_table": "dim_equipment",
            "join_sql": "fact_downtime_event.equipment_id = dim_equipment.equipment_id",
            "join_keys": [{"from": "equipment_id", "to": "equipment_id"}],
            "relationship_type": "many_to_one",
            "description": "停机→设备",
        },
        {
            "from_table": "fact_downtime_event",
            "to_table": "dim_downtime_reason",
            "join_sql": "fact_downtime_event.reason_id = dim_downtime_reason.reason_id",
            "join_keys": [{"from": "reason_id", "to": "reason_id"}],
            "relationship_type": "many_to_one",
            "description": "停机→原因",
        },
        {
            "from_table": "fact_maintenance_record",
            "to_table": "dim_equipment",
            "join_sql": "fact_maintenance_record.equipment_id = dim_equipment.equipment_id",
            "join_keys": [{"from": "equipment_id", "to": "equipment_id"}],
            "relationship_type": "many_to_one",
            "description": "维保→设备",
        },
        {
            "from_table": "fact_equipment_plan",
            "to_table": "dim_equipment",
            "join_sql": "fact_equipment_plan.equipment_id = dim_equipment.equipment_id",
            "join_keys": [{"from": "equipment_id", "to": "equipment_id"}],
            "relationship_type": "many_to_one",
            "description": "计划→设备",
        },
        {
            "from_table": "dim_equipment_type",
            "to_table": "dim_equipment_type",
            "join_sql": "dim_equipment_type.parent_type_id = dim_equipment_type.equip_type_id",
            "join_keys": [{"from": "parent_type_id", "to": "equip_type_id"}],
            "relationship_type": "many_to_one",
            "description": "类型上级（树形）",
        },
        {
            "from_table": "dim_downtime_reason",
            "to_table": "dim_downtime_reason",
            "join_sql": "dim_downtime_reason.parent_reason_id = dim_downtime_reason.reason_id",
            "join_keys": [{"from": "parent_reason_id", "to": "reason_id"}],
            "relationship_type": "many_to_one",
            "description": "原因上级（树形）",
        },
        {
            "from_table": "fact_equipment_plan",
            "to_table": "fact_equipment_daily_ops",
            "join_sql": "fact_equipment_plan.equipment_id = fact_equipment_daily_ops.equipment_id AND fact_equipment_plan.date_key = fact_equipment_daily_ops.date_key",
            "join_keys": [
                {"from": "equipment_id", "to": "equipment_id"},
                {"from": "date_key", "to": "date_key"},
            ],
            "relationship_type": "many_to_one",
            "description": "计划对比实际（逻辑关联）",
        },
    ]
    for rel in table_relationships:
        s.tables.add_relationship(**rel)
        output.print(f"OK {rel['from_table']} -> {rel['to_table']}")

    # 4. 注册 Cube
    output.print("\n[4/8] 注册 Cube...")

    ops = "fact_equipment_daily_ops"
    downtime = "fact_downtime_event"
    maint = "fact_maintenance_record"
    plan = "fact_equipment_plan"

    ops_measures = [
        {"name": "calendar_minutes_total", "col": "calendar_minutes", "agg": "sum", "title": "日历时间合计"},
        {"name": "planned_downtime_total", "col": "planned_downtime_min", "agg": "sum", "title": "计划停机合计"},
        {"name": "unplanned_downtime_total", "col": "unplanned_downtime_min", "agg": "sum", "title": "非计划停机合计"},
        {"name": "runtime_total", "col": "runtime_min", "agg": "sum", "title": "运行时间合计"},
        {"name": "actual_output_total", "col": "actual_output_qty", "agg": "sum", "title": "实际产量"},
        {"name": "qualified_output_total", "col": "qualified_output_qty", "agg": "sum", "title": "合格产量"},
        {"name": "energy_total", "col": "energy_consumption", "agg": "sum", "title": "能耗合计"},
        {"name": "ideal_cycle_rate_avg", "col": "ideal_cycle_rate", "agg": "avg", "title": "理想节拍均值"},
        {"name": "ops_days", "col": "ops_id", "agg": "count", "title": "汇总行数"},
    ]

    ops_dims = [
        {"name": "ops_id", "col": "ops_id", "type": "string", "title": "汇总ID"},
        {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
        {"name": "calendar_date", "col": "calendar_date", "type": "date", "title": "统计日期"},
        {"name": "equipment_id", "col": "equipment_id", "type": "string", "title": "设备ID"},
        {"name": "equipment_code", "col": "equipment_code", "type": "string", "title": "设备位号"},
        {"name": "equipment_name", "col": "equipment_name", "type": "string", "title": "设备名称"},
        {"name": "plant_id", "col": "plant_id", "type": "string", "title": "厂区ID"},
        {"name": "plant_name", "col": "plant_name", "type": "string", "title": "厂区名称"},
        {"name": "unit_id", "col": "unit_id", "type": "string", "title": "单元ID"},
        {"name": "unit_name", "col": "unit_name", "type": "string", "title": "单元名称"},
        {"name": "equip_type_id", "col": "equip_type_id", "type": "string", "title": "设备类型ID"},
        {"name": "category", "col": "category", "type": "string", "title": "设备大类"},
        {"name": "shift_code", "col": "shift_code", "type": "string", "title": "班次"},
    ]

    oee_derived = [
        {
            "name": "availability",
            "title": "可用率",
            "expression": "if((OperationCube.calendar_minutes_total - OperationCube.planned_downtime_total) > 0, OperationCube.runtime_total / (OperationCube.calendar_minutes_total - OperationCube.planned_downtime_total), 0)",
            "description": "运行时间 / 计划运行时间",
        },
        {
            "name": "performance",
            "title": "性能率",
            "expression": "if(OperationCube.runtime_total > 0 and OperationCube.ideal_cycle_rate_avg > 0, (OperationCube.actual_output_total / OperationCube.runtime_total) / OperationCube.ideal_cycle_rate_avg, 0)",
            "description": "实际节拍 / 理想节拍",
        },
        {
            "name": "quality",
            "title": "质量率",
            "expression": "if(OperationCube.actual_output_total > 0, OperationCube.qualified_output_total / OperationCube.actual_output_total, 0)",
            "description": "合格产量 / 实际产量",
        },
        {
            "name": "oee",
            "title": "综合效率",
            "expression": "OperationCube.availability * OperationCube.performance * OperationCube.quality",
            "description": "可用率 × 性能率 × 质量率",
        },
        {
            "name": "load_rate",
            "title": "负荷率",
            "expression": "if((OperationCube.calendar_minutes_total - OperationCube.planned_downtime_total) > 0, OperationCube.runtime_total / (OperationCube.calendar_minutes_total - OperationCube.planned_downtime_total), 0)",
            "description": "运行时间 / 计划运行时间",
        },
        {
            "name": "energy_per_output",
            "title": "单位产量能耗",
            "expression": "if(OperationCube.actual_output_total > 0, OperationCube.energy_total / OperationCube.actual_output_total, 0)",
            "description": "能耗 / 实际产量",
        },
    ]

    subject_oee_derived = lambda cube: [
        {
            "name": "availability",
            "title": "可用率",
            "expression": f"if(({cube}.calendar_minutes_total - {cube}.planned_downtime_total) > 0, {cube}.runtime_total / ({cube}.calendar_minutes_total - {cube}.planned_downtime_total), 0)",
            "description": "可用率",
        },
        {
            "name": "performance",
            "title": "性能率",
            "expression": f"if({cube}.runtime_total > 0 and {cube}.ideal_cycle_rate_avg > 0, ({cube}.actual_output_total / {cube}.runtime_total) / {cube}.ideal_cycle_rate_avg, 0)",
            "description": "性能率",
        },
        {
            "name": "quality",
            "title": "质量率",
            "expression": f"if({cube}.actual_output_total > 0, {cube}.qualified_output_total / {cube}.actual_output_total, 0)",
            "description": "质量率",
        },
        {
            "name": "oee",
            "title": "综合效率",
            "expression": f"{cube}.availability * {cube}.performance * {cube}.quality",
            "description": "OEE",
        },
        {
            "name": "energy_per_output",
            "title": "单位产量能耗",
            "expression": f"if({cube}.actual_output_total > 0, {cube}.energy_total / {cube}.actual_output_total, 0)",
            "description": "单位产量能耗",
        },
    ]

    # OperationCube
    s.register_cube(
        name="OperationCube",
        table=ops,
        title="日运行主Cube",
        measures=ops_measures,
        dimensions=ops_dims,
    )
    output.print("OK OperationCube")

    # EquipmentCube
    s.register_cube(
        name="EquipmentCube",
        table=ops,
        title="设备运营Cube",
        measures=[
            {"name": "calendar_minutes_total", "col": "calendar_minutes", "agg": "sum", "title": "日历时间合计"},
            {"name": "planned_downtime_total", "col": "planned_downtime_min", "agg": "sum", "title": "计划停机合计"},
            {"name": "runtime_total", "col": "runtime_min", "agg": "sum", "title": "运行时间合计"},
            {"name": "unplanned_downtime_total", "col": "unplanned_downtime_min", "agg": "sum", "title": "非计划停机合计"},
            {"name": "actual_output_total", "col": "actual_output_qty", "agg": "sum", "title": "实际产量"},
            {"name": "qualified_output_total", "col": "qualified_output_qty", "agg": "sum", "title": "合格产量"},
            {"name": "energy_total", "col": "energy_consumption", "agg": "sum", "title": "能耗合计"},
            {"name": "ideal_cycle_rate_avg", "col": "ideal_cycle_rate", "agg": "avg", "title": "理想节拍均值"},
            {"name": "ops_days", "col": "ops_id", "agg": "count", "title": "汇总行数"},
        ],
        dimensions=[
            {"name": "equipment_id", "col": "equipment_id", "type": "string", "title": "设备ID"},
            {"name": "equipment_code", "col": "equipment_code", "type": "string", "title": "设备位号"},
            {"name": "equipment_name", "col": "equipment_name", "type": "string", "title": "设备名称"},
            {"name": "equip_type_id", "col": "equip_type_id", "type": "string", "title": "设备类型ID"},
            {"name": "category", "col": "category", "type": "string", "title": "设备大类"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "厂区ID"},
            {"name": "plant_name", "col": "plant_name", "type": "string", "title": "厂区名称"},
            {"name": "unit_id", "col": "unit_id", "type": "string", "title": "单元ID"},
            {"name": "unit_name", "col": "unit_name", "type": "string", "title": "单元名称"},
            {"name": "criticality", "col": "equipment_id", "type": "string", "title": "关键等级"},
            {"name": "production_mode", "col": "equipment_id", "type": "string", "title": "生产模式"},
        ],
    )
    output.print("OK EquipmentCube")

    # PlantCube
    s.register_cube(
        name="PlantCube",
        table=ops,
        title="厂区运营Cube",
        measures=[
            {"name": "calendar_minutes_total", "col": "calendar_minutes", "agg": "sum", "title": "日历时间合计"},
            {"name": "planned_downtime_total", "col": "planned_downtime_min", "agg": "sum", "title": "计划停机合计"},
            {"name": "runtime_total", "col": "runtime_min", "agg": "sum", "title": "运行时间合计"},
            {"name": "unplanned_downtime_total", "col": "unplanned_downtime_min", "agg": "sum", "title": "非计划停机合计"},
            {"name": "actual_output_total", "col": "actual_output_qty", "agg": "sum", "title": "实际产量"},
            {"name": "qualified_output_total", "col": "qualified_output_qty", "agg": "sum", "title": "合格产量"},
            {"name": "energy_total", "col": "energy_consumption", "agg": "sum", "title": "能耗合计"},
            {"name": "ideal_cycle_rate_avg", "col": "ideal_cycle_rate", "agg": "avg", "title": "理想节拍均值"},
        ],
        dimensions=[
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "厂区ID"},
            {"name": "plant_name", "col": "plant_name", "type": "string", "title": "厂区名称"},
        ],
    )
    output.print("OK PlantCube")

    # ProcessUnitCube
    s.register_cube(
        name="ProcessUnitCube",
        table=ops,
        title="工艺单元运营Cube",
        measures=[
            {"name": "calendar_minutes_total", "col": "calendar_minutes", "agg": "sum", "title": "日历时间合计"},
            {"name": "planned_downtime_total", "col": "planned_downtime_min", "agg": "sum", "title": "计划停机合计"},
            {"name": "runtime_total", "col": "runtime_min", "agg": "sum", "title": "运行时间合计"},
            {"name": "unplanned_downtime_total", "col": "unplanned_downtime_min", "agg": "sum", "title": "非计划停机合计"},
            {"name": "actual_output_total", "col": "actual_output_qty", "agg": "sum", "title": "实际产量"},
            {"name": "qualified_output_total", "col": "qualified_output_qty", "agg": "sum", "title": "合格产量"},
            {"name": "energy_total", "col": "energy_consumption", "agg": "sum", "title": "能耗合计"},
            {"name": "ideal_cycle_rate_avg", "col": "ideal_cycle_rate", "agg": "avg", "title": "理想节拍均值"},
        ],
        dimensions=[
            {"name": "unit_id", "col": "unit_id", "type": "string", "title": "单元ID"},
            {"name": "unit_name", "col": "unit_name", "type": "string", "title": "单元名称"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "厂区ID"},
            {"name": "plant_name", "col": "plant_name", "type": "string", "title": "厂区名称"},
        ],
    )
    output.print("OK ProcessUnitCube")

    # DowntimeCube
    s.register_cube(
        name="DowntimeCube",
        table=downtime,
        title="停机事件Cube",
        measures=[
            {"name": "downtime_minutes", "col": "duration_min", "agg": "sum", "title": "停机时长"},
            {"name": "event_count", "col": "event_id", "agg": "count", "title": "事件次数"},
        ],
        dimensions=[
            {"name": "event_id", "col": "event_id", "type": "string", "title": "事件ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "equipment_id", "col": "equipment_id", "type": "string", "title": "设备ID"},
            {"name": "equipment_code", "col": "equipment_code", "type": "string", "title": "设备位号"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "厂区ID"},
            {"name": "unit_id", "col": "unit_id", "type": "string", "title": "单元ID"},
            {"name": "reason_id", "col": "reason_id", "type": "string", "title": "原因ID"},
            {"name": "reason_code", "col": "reason_code", "type": "string", "title": "原因编码"},
            {"name": "reason_name", "col": "reason_name", "type": "string", "title": "原因名称"},
            {"name": "reason_category", "col": "reason_category", "type": "string", "title": "原因大类"},
            {"name": "is_planned", "col": "is_planned", "type": "int", "title": "是否计划停机"},
            {"name": "responsible_dept", "col": "responsible_dept", "type": "string", "title": "责任部门"},
        ],
    )
    output.print("OK DowntimeCube")

    # MaintenanceCube
    s.register_cube(
        name="MaintenanceCube",
        table=maint,
        title="维保记录Cube",
        measures=[
            {"name": "plan_hours", "col": "plan_hours", "agg": "sum", "title": "计划工时"},
            {"name": "actual_hours", "col": "actual_hours", "agg": "sum", "title": "实际工时"},
            {"name": "plan_cost", "col": "plan_cost", "agg": "sum", "title": "计划费用"},
            {"name": "actual_cost", "col": "actual_cost", "agg": "sum", "title": "实际费用"},
            {"name": "maint_count", "col": "maint_id", "agg": "count", "title": "维保次数"},
            {"name": "on_schedule_count", "col": "is_on_schedule", "agg": "sum", "title": "按期完成次数"},
        ],
        dimensions=[
            {"name": "maint_id", "col": "maint_id", "type": "string", "title": "维保ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "equipment_id", "col": "equipment_id", "type": "string", "title": "设备ID"},
            {"name": "equipment_code", "col": "equipment_code", "type": "string", "title": "设备位号"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "厂区ID"},
            {"name": "unit_id", "col": "unit_id", "type": "string", "title": "单元ID"},
            {"name": "maint_type", "col": "maint_type", "type": "string", "title": "维保类型"},
            {"name": "status", "col": "status", "type": "string", "title": "状态"},
        ],
    )
    output.print("OK MaintenanceCube")

    # PlanVsActualCube
    s.register_cube(
        name="PlanVsActualCube",
        table=plan,
        title="计划对比Cube",
        measures=[
            {"name": "planned_runtime_min", "col": "planned_runtime_min", "agg": "sum", "title": "计划运行时间"},
            {"name": "planned_output_qty", "col": "planned_output_qty", "agg": "sum", "title": "计划产量"},
            {"name": "planned_energy", "col": "planned_energy", "agg": "sum", "title": "计划能耗"},
            {"name": "plan_count", "col": "plan_id", "agg": "count", "title": "计划行数"},
        ],
        dimensions=[
            {"name": "plan_id", "col": "plan_id", "type": "string", "title": "计划ID"},
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "fiscal_year", "col": "fiscal_year", "type": "int", "title": "计划年度"},
            {"name": "fiscal_month", "col": "fiscal_month", "type": "int", "title": "计划月份"},
            {"name": "equipment_id", "col": "equipment_id", "type": "string", "title": "设备ID"},
            {"name": "equipment_code", "col": "equipment_code", "type": "string", "title": "设备位号"},
            {"name": "plant_id", "col": "plant_id", "type": "string", "title": "厂区ID"},
            {"name": "unit_id", "col": "unit_id", "type": "string", "title": "单元ID"},
            {"name": "plan_version", "col": "plan_version", "type": "string", "title": "计划版本"},
        ],
    )
    output.print("OK PlanVsActualCube")

    # 派生度量
    output.print("\n[4b/8] 配置派生度量...")
    s.upsert_derived_measures("OperationCube", oee_derived)
    output.print("OK OperationCube 派生度量")

    for cube_name in ("EquipmentCube", "PlantCube", "ProcessUnitCube"):
        derived = subject_oee_derived(cube_name)
        if cube_name == "ProcessUnitCube":
            derived.append({
                "name": "load_rate",
                "title": "负荷率",
                "expression": f"if(({cube_name}.calendar_minutes_total - {cube_name}.planned_downtime_total) > 0, {cube_name}.runtime_total / ({cube_name}.calendar_minutes_total - {cube_name}.planned_downtime_total), 0)",
                "description": "负荷率",
            })
        s.upsert_derived_measures(cube_name, derived)
        output.print(f"OK {cube_name} 派生度量")

    s.upsert_derived_measures(
        "DowntimeCube",
        [
            {
                "name": "avg_downtime",
                "title": "平均停机时长",
                "expression": "if(DowntimeCube.event_count > 0, DowntimeCube.downtime_minutes / DowntimeCube.event_count, 0)",
                "description": "停机时长 / 事件次数",
            },
        ],
    )
    output.print("OK DowntimeCube 派生度量")

    s.upsert_derived_measures(
        "MaintenanceCube",
        [
            {
                "name": "schedule_rate",
                "title": "维保达成率",
                "expression": "if(MaintenanceCube.maint_count > 0, MaintenanceCube.on_schedule_count / MaintenanceCube.maint_count, 0)",
                "description": "按期完成 / 维保次数",
            },
            {
                "name": "cost_variance",
                "title": "费用偏差",
                "expression": "MaintenanceCube.actual_cost - MaintenanceCube.plan_cost",
                "description": "实际费用 - 计划费用",
            },
        ],
    )
    output.print("OK MaintenanceCube 派生度量")

    # 5. 定义对象类型（10 种，规划 §5.1）
    output.print("\n[5/8] 定义对象类型...")

    s.onto.define_object_type(
        code="Plant",
        name="厂区/装置区",
        description="化工生产厂区或大型装置区",
        category_347="主数据",
    )
    s.onto.bind_source("Plant", "dazi_cube", config={"cube": "PlantCube"})
    output.print("OK Plant")

    s.onto.define_object_type(
        code="ProcessUnit",
        name="工艺单元",
        description="装置内工艺单元",
        category_347="主数据",
    )
    s.onto.bind_source("ProcessUnit", "dazi_cube", config={"cube": "ProcessUnitCube"})
    output.print("OK ProcessUnit")

    s.onto.define_object_type(
        code="EquipmentType",
        name="设备类型",
        description="设备分类主数据",
        category_347="主数据",
    )
    output.print("OK EquipmentType（无 bind_source）")

    s.onto.define_object_type(
        code="Equipment",
        name="设备",
        description="单台设备台账",
        category_347="主数据",
    )
    s.onto.bind_source("Equipment", "dazi_cube", config={"cube": "EquipmentCube"})
    output.print("OK Equipment")

    s.onto.define_object_type(
        code="DowntimeReason",
        name="停机原因",
        description="停机/故障原因码表",
        category_347="参考",
    )
    output.print("OK DowntimeReason（无 bind_source）")

    s.onto.define_object_type(
        code="OperationSnapshot",
        name="日运行汇总",
        description="设备日运行 KPI 汇总",
        category_347="事务",
    )
    s.onto.bind_source("OperationSnapshot", "dazi_cube", config={"cube": "OperationCube"})
    output.print("OK OperationSnapshot")

    s.onto.define_object_type(
        code="DowntimeEvent",
        name="停机事件",
        description="单次停机/故障事件",
        category_347="事务",
    )
    s.onto.bind_source("DowntimeEvent", "dazi_cube", config={"cube": "DowntimeCube"})
    output.print("OK DowntimeEvent")

    s.onto.define_object_type(
        code="MaintenanceRecord",
        name="维保记录",
        description="计划与实际维保作业",
        category_347="事务",
    )
    s.onto.bind_source("MaintenanceRecord", "dazi_cube", config={"cube": "MaintenanceCube"})
    output.print("OK MaintenanceRecord")

    s.onto.define_object_type(
        code="EquipmentAnalysis",
        name="设备运营分析",
        description="多维度设备运营指标聚合",
        category_347="分析",
    )
    s.onto.bind_source("EquipmentAnalysis", "dazi_cube", config={"cube": "OperationCube"})
    output.print("OK EquipmentAnalysis")

    s.onto.define_object_type(
        code="PlanAnalysis",
        name="计划对比分析",
        description="运行计划 vs 实际对比",
        category_347="分析",
    )
    s.onto.bind_source("PlanAnalysis", "dazi_cube", config={"cube": "PlanVsActualCube"})
    output.print("OK PlanAnalysis")

    # 6. 定义属性（主要对象各 3-5 个，规划 §5.2）
    output.print("\n[6/8] 定义对象属性...")

    s.onto.define_property("Plant", "id", "厂区 ID", semantic_role="dimension", qualified_name="PlantCube.plant_id")
    s.onto.define_property("Plant", "name", "厂区名称", semantic_role="dimension", qualified_name="PlantCube.plant_name")
    s.onto.define_property("Plant", "availability", "可用率", semantic_role="measure", qualified_name="PlantCube.availability")
    s.onto.define_property("Plant", "oee", "装置 OEE", semantic_role="measure", qualified_name="PlantCube.oee")
    s.onto.define_property("Plant", "energy_per_output", "单位产量能耗", semantic_role="measure", qualified_name="PlantCube.energy_per_output")

    s.onto.define_property("ProcessUnit", "id", "单元 ID", semantic_role="dimension", qualified_name="ProcessUnitCube.unit_id")
    s.onto.define_property("ProcessUnit", "name", "单元名称", semantic_role="dimension", qualified_name="ProcessUnitCube.unit_name")
    s.onto.define_property("ProcessUnit", "availability", "可用率", semantic_role="measure", qualified_name="ProcessUnitCube.availability")
    s.onto.define_property("ProcessUnit", "oee", "单元 OEE", semantic_role="measure", qualified_name="ProcessUnitCube.oee")
    s.onto.define_property("ProcessUnit", "load_rate", "负荷率", semantic_role="measure", qualified_name="ProcessUnitCube.load_rate")

    # EquipmentType / DowntimeReason 无 bind_source，跳过 define_property（平台要求 measure/dimension 须绑定 Cube）

    s.onto.define_property("Equipment", "id", "设备 ID", semantic_role="dimension", qualified_name="EquipmentCube.equipment_id")
    s.onto.define_property("Equipment", "code", "设备位号", semantic_role="dimension", qualified_name="EquipmentCube.equipment_code")
    s.onto.define_property("Equipment", "name", "设备名称", semantic_role="dimension", qualified_name="EquipmentCube.equipment_name")
    s.onto.define_property("Equipment", "runtime", "运行时间", semantic_role="measure", qualified_name="EquipmentCube.runtime_total")
    s.onto.define_property("Equipment", "availability", "可用率", semantic_role="measure", qualified_name="EquipmentCube.availability")
    s.onto.define_property("Equipment", "oee", "综合效率", semantic_role="measure", qualified_name="EquipmentCube.oee")

    s.onto.define_property("OperationSnapshot", "date", "统计日期", semantic_role="dimension", qualified_name="OperationCube.calendar_date")
    s.onto.define_property("OperationSnapshot", "runtime", "运行时间", semantic_role="measure", qualified_name="OperationCube.runtime_total")
    s.onto.define_property("OperationSnapshot", "availability", "可用率", semantic_role="measure", qualified_name="OperationCube.availability")
    s.onto.define_property("OperationSnapshot", "oee", "OEE", semantic_role="measure", qualified_name="OperationCube.oee")

    s.onto.define_property("DowntimeEvent", "id", "事件 ID", semantic_role="dimension", qualified_name="DowntimeCube.event_id")
    s.onto.define_property("DowntimeEvent", "duration", "停机时长", semantic_role="measure", qualified_name="DowntimeCube.downtime_minutes")
    s.onto.define_property("DowntimeEvent", "reason", "原因名称", semantic_role="dimension", qualified_name="DowntimeCube.reason_name")
    s.onto.define_property("DowntimeEvent", "is_planned", "是否计划", semantic_role="dimension", qualified_name="DowntimeCube.is_planned")

    s.onto.define_property("MaintenanceRecord", "id", "维保 ID", semantic_role="dimension", qualified_name="MaintenanceCube.maint_id")
    s.onto.define_property("MaintenanceRecord", "plan_hours", "计划工时", semantic_role="measure", qualified_name="MaintenanceCube.plan_hours")
    s.onto.define_property("MaintenanceRecord", "actual_hours", "实际工时", semantic_role="measure", qualified_name="MaintenanceCube.actual_hours")
    s.onto.define_property("MaintenanceRecord", "schedule_rate", "达成率", semantic_role="measure", qualified_name="MaintenanceCube.schedule_rate")

    s.onto.define_property("EquipmentAnalysis", "oee", "平均 OEE", semantic_role="measure", qualified_name="OperationCube.oee")
    s.onto.define_property("EquipmentAnalysis", "availability", "平均可用率", semantic_role="measure", qualified_name="OperationCube.availability")
    s.onto.define_property("EquipmentAnalysis", "runtime", "总运行时间", semantic_role="measure", qualified_name="OperationCube.runtime_total")
    s.onto.define_property("EquipmentAnalysis", "energy_per_output", "单位产量能耗", semantic_role="measure", qualified_name="OperationCube.energy_per_output")

    s.onto.define_property("PlanAnalysis", "planned_output", "计划产量", semantic_role="measure", qualified_name="PlanVsActualCube.planned_output_qty")
    s.onto.define_property("PlanAnalysis", "planned_runtime", "计划运行时间", semantic_role="measure", qualified_name="PlanVsActualCube.planned_runtime_min")
    s.onto.define_property("PlanAnalysis", "plan_version", "计划版本", semantic_role="dimension", qualified_name="PlanVsActualCube.plan_version")

    output.print("OK 属性定义完成")

    # 7. 定义链接类型（16 种，规划 §5.3）
    output.print("\n[7/8] 定义链接类型...")

    s.onto.define_link_type(code="unit_belongs_plant", name="单元归属厂区", from_object_type_code="ProcessUnit", to_object_type_code="Plant", category_347="归属关系")
    s.onto.define_link_type(code="equipment_belongs_plant", name="设备归属厂区", from_object_type_code="Equipment", to_object_type_code="Plant", category_347="归属关系")
    s.onto.define_link_type(code="equipment_belongs_unit", name="设备归属单元", from_object_type_code="Equipment", to_object_type_code="ProcessUnit", category_347="归属关系")
    s.onto.define_link_type(code="equipment_has_type", name="设备属于类型", from_object_type_code="Equipment", to_object_type_code="EquipmentType", category_347="归属关系")
    s.onto.define_link_type(code="snapshot_for_equipment", name="日运行归属设备", from_object_type_code="OperationSnapshot", to_object_type_code="Equipment", category_347="归属关系")
    s.onto.define_link_type(code="downtime_on_equipment", name="停机发生于设备", from_object_type_code="DowntimeEvent", to_object_type_code="Equipment", category_347="归属关系")
    s.onto.define_link_type(code="downtime_has_reason", name="停机对应原因", from_object_type_code="DowntimeEvent", to_object_type_code="DowntimeReason", category_347="归属关系")
    s.onto.define_link_type(code="maint_for_equipment", name="维保针对设备", from_object_type_code="MaintenanceRecord", to_object_type_code="Equipment", category_347="归属关系")

    s.onto.define_link_type(code="equip_type_has_parent", name="类型上级", from_object_type_code="EquipmentType", to_object_type_code="EquipmentType", category_347="层级关系")
    s.onto.define_link_type(code="reason_has_parent", name="原因上级", from_object_type_code="DowntimeReason", to_object_type_code="DowntimeReason", category_347="层级关系")

    s.onto.define_link_type(code="plan_compared_to_actual", name="计划对比实际", from_object_type_code="PlanAnalysis", to_object_type_code="EquipmentAnalysis", category_347="对比关系")

    s.onto.define_link_type(code="analysis_by_equipment", name="分析归因设备", from_object_type_code="EquipmentAnalysis", to_object_type_code="Equipment", category_347="分析归因")
    s.onto.define_link_type(code="analysis_by_plant", name="分析归因厂区", from_object_type_code="EquipmentAnalysis", to_object_type_code="Plant", category_347="分析归因")
    s.onto.define_link_type(code="analysis_by_unit", name="分析归因单元", from_object_type_code="EquipmentAnalysis", to_object_type_code="ProcessUnit", category_347="分析归因")
    s.onto.define_link_type(code="analysis_by_downtime", name="分析归因停机", from_object_type_code="EquipmentAnalysis", to_object_type_code="DowntimeEvent", category_347="分析归因")
    s.onto.define_link_type(code="analysis_by_maintenance", name="分析归因维保", from_object_type_code="EquipmentAnalysis", to_object_type_code="MaintenanceRecord", category_347="分析归因")

    output.print("OK 链接定义完成")

    # 8. 同步指标引用 + 输出摘要
    output.print("\n[8/8] 同步指标引用...")
    s.sync_metric_refs()
    output.print("OK sync_metric_refs")

    summary = {
        "ok": True,
        "space_id": space_id,
        "tables": len(TABLE_REGISTRY),
        "relationships": len(table_relationships),
        "cubes": 7,
        "objects": 10,
        "links": 16,
    }
    output.success("化工设备运营分析本体初始化完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))
