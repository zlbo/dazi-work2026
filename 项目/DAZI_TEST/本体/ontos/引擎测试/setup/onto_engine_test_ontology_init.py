"""本体引擎测试空间初始化 — space__onto_engine_test

简化「项目成本/产值」域，覆盖 G2/G3/G4 + P1 编排能力测试所需结构。
规划对照：dazi/docs2/规划/018-本体引擎测试场景方案.md

实施顺序：init → seed → meta_seed → category_mount → engine_verify
"""

import json

TABLE_REGISTRY = {
    "dim_date": {
        "display_name": "日期维表",
        "description": "全空间共享日历，事实表通过 date_key 关联",
        "columns": [
            {"name": "date_key", "display_name": "日期键", "description": "YYYYMMDD，主键"},
            {"name": "calendar_date", "display_name": "自然日"},
            {"name": "year", "display_name": "公历年"},
            {"name": "quarter", "display_name": "季度"},
            {"name": "month", "display_name": "月"},
            {"name": "week_of_year", "display_name": "周"},
            {"name": "day_of_week", "display_name": "星期"},
            {"name": "is_weekend", "display_name": "是否周末"},
            {"name": "year_month", "display_name": "年月"},
        ],
    },
    "dim_org": {
        "display_name": "组织维表",
        "description": "公司/分公司/项目部三级组织",
        "columns": [
            {"name": "org_id", "display_name": "组织 ID", "description": "主键"},
            {"name": "org_code", "display_name": "组织编码"},
            {"name": "org_name", "display_name": "组织名称"},
            {"name": "parent_org_id", "display_name": "上级组织", "description": "自关联"},
            {"name": "org_level", "display_name": "组织层级", "description": "1公司/2分公司/3项目部"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_project": {
        "display_name": "项目维表",
        "description": "工程项目主数据",
        "columns": [
            {"name": "project_id", "display_name": "项目 ID", "description": "主键"},
            {"name": "project_code", "display_name": "项目编码"},
            {"name": "project_name", "display_name": "项目名称"},
            {"name": "region", "display_name": "片区", "description": "华东/华北/华南"},
            {"name": "project_type", "display_name": "项目类型"},
            {"name": "org_id", "display_name": "所属组织", "description": "关联 dim_org"},
            {"name": "org_name", "display_name": "组织名称", "description": "冗余"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "dim_cost_type": {
        "display_name": "成本科目维表",
        "description": "成本科目树（大类/子类）",
        "columns": [
            {"name": "cost_type_id", "display_name": "科目 ID", "description": "主键"},
            {"name": "cost_type_code", "display_name": "科目编码"},
            {"name": "cost_type_name", "display_name": "科目名称"},
            {"name": "parent_type_id", "display_name": "上级科目", "description": "自关联"},
            {"name": "status", "display_name": "状态"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_cost": {
        "display_name": "成本事实表",
        "description": "项目月度成本流水",
        "columns": [
            {"name": "cost_id", "display_name": "成本 ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date"},
            {"name": "project_id", "display_name": "项目 ID"},
            {"name": "project_name", "display_name": "项目名称", "description": "冗余"},
            {"name": "region", "display_name": "片区", "description": "冗余"},
            {"name": "org_id", "display_name": "组织 ID"},
            {"name": "org_name", "display_name": "组织名称", "description": "冗余"},
            {"name": "parent_org_id", "display_name": "上级组织 ID", "description": "冗余，供层级上卷"},
            {"name": "cost_type_id", "display_name": "成本科目 ID"},
            {"name": "cost_type_name", "display_name": "科目名称", "description": "冗余"},
            {"name": "parent_cost_type_id", "display_name": "上级科目 ID", "description": "冗余，供层级上卷"},
            {"name": "cost_amount", "display_name": "成本金额"},
            {"name": "budget_amount", "display_name": "预算金额"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
    "fact_output": {
        "display_name": "产值事实表",
        "description": "项目月度产值流水",
        "columns": [
            {"name": "output_id", "display_name": "产值 ID", "description": "主键"},
            {"name": "date_key", "display_name": "日期键", "description": "关联 dim_date"},
            {"name": "project_id", "display_name": "项目 ID"},
            {"name": "project_name", "display_name": "项目名称", "description": "冗余"},
            {"name": "region", "display_name": "片区", "description": "冗余"},
            {"name": "org_id", "display_name": "组织 ID"},
            {"name": "output_amount", "display_name": "产值金额"},
            {"name": "created_at", "display_name": "创建时间"},
        ],
    },
}


def _link_extra(keys):
    return {"join_spec": {"join_keys": keys}}


def main():
    space_id = "space__onto_engine_test"
    s = space.get(space_id)

    output.print("=== 本体引擎测试空间初始化 ===")
    output.print(f"空间: {space_id}")

    # 1. 建表
    output.print("\n[1/7] 创建物理表...")
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_date (
            date_key Int32,
            calendar_date Date,
            year Int16,
            quarter Int8,
            month Int8,
            week_of_year Int8,
            day_of_week Int8,
            is_weekend UInt8,
            year_month String
        ) ENGINE = MergeTree() ORDER BY (date_key)
    """)
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_org (
            org_id String, org_code String, org_name String,
            parent_org_id String, org_level Int32, status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree() ORDER BY (org_code)
    """)
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_project (
            project_id String, project_code String, project_name String,
            region String, project_type String, org_id String, org_name String,
            status String, created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree() ORDER BY (project_code)
    """)
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS dim_cost_type (
            cost_type_id String, cost_type_code String, cost_type_name String,
            parent_type_id String, status String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree() ORDER BY (cost_type_code)
    """)
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_cost (
            cost_id String, date_key Int32,
            project_id String, project_name String, region String,
            org_id String, org_name String, parent_org_id String,
            cost_type_id String, cost_type_name String, parent_cost_type_id String,
            cost_amount Float64, budget_amount Float64,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree() ORDER BY (date_key, project_id, cost_type_id)
    """)
    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS fact_output (
            output_id String, date_key Int32,
            project_id String, project_name String, region String,
            org_id String, output_amount Float64,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree() ORDER BY (date_key, project_id)
    """)
    output.print("OK 6 张表")

    # 2. 注册表
    output.print("\n[2/7] 注册表到空间...")
    for tbl, meta in TABLE_REGISTRY.items():
        s.tables.register_with_meta(
            table_name=tbl,
            display_name=meta["display_name"],
            description=meta.get("description"),
            columns=meta["columns"],
            force_column_meta=True,
        )
    output.print(f"OK {len(TABLE_REGISTRY)} 张表")

    # 3. 表间关系
    output.print("\n[3/7] 注册表间关系...")
    table_relationships = [
        {"from_table": "fact_cost", "to_table": "dim_date",
         "join_sql": "fact_cost.date_key = dim_date.date_key",
         "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one",
         "description": "成本→日历"},
        {"from_table": "fact_cost", "to_table": "dim_project",
         "join_sql": "fact_cost.project_id = dim_project.project_id",
         "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one",
         "description": "成本→项目"},
        {"from_table": "fact_cost", "to_table": "dim_org",
         "join_sql": "fact_cost.org_id = dim_org.org_id",
         "join_keys": [{"from": "org_id", "to": "org_id"}], "relationship_type": "many_to_one",
         "description": "成本→组织"},
        {"from_table": "fact_cost", "to_table": "dim_cost_type",
         "join_sql": "fact_cost.cost_type_id = dim_cost_type.cost_type_id",
         "join_keys": [{"from": "cost_type_id", "to": "cost_type_id"}], "relationship_type": "many_to_one",
         "description": "成本→科目"},
        {"from_table": "fact_output", "to_table": "dim_date",
         "join_sql": "fact_output.date_key = dim_date.date_key",
         "join_keys": [{"from": "date_key", "to": "date_key"}], "relationship_type": "many_to_one",
         "description": "产值→日历"},
        {"from_table": "fact_output", "to_table": "dim_project",
         "join_sql": "fact_output.project_id = dim_project.project_id",
         "join_keys": [{"from": "project_id", "to": "project_id"}], "relationship_type": "many_to_one",
         "description": "产值→项目"},
        {"from_table": "fact_output", "to_table": "dim_org",
         "join_sql": "fact_output.org_id = dim_org.org_id",
         "join_keys": [{"from": "org_id", "to": "org_id"}], "relationship_type": "many_to_one",
         "description": "产值→组织"},
        {"from_table": "dim_project", "to_table": "dim_org",
         "join_sql": "dim_project.org_id = dim_org.org_id",
         "join_keys": [{"from": "org_id", "to": "org_id"}], "relationship_type": "many_to_one",
         "description": "项目→组织"},
        {"from_table": "dim_org", "to_table": "dim_org",
         "join_sql": "dim_org.parent_org_id = dim_org.org_id",
         "join_keys": [{"from": "parent_org_id", "to": "org_id"}], "relationship_type": "many_to_one",
         "description": "组织上级"},
        {"from_table": "dim_cost_type", "to_table": "dim_cost_type",
         "join_sql": "dim_cost_type.parent_type_id = dim_cost_type.cost_type_id",
         "join_keys": [{"from": "parent_type_id", "to": "cost_type_id"}], "relationship_type": "many_to_one",
         "description": "科目上级"},
    ]
    for rel in table_relationships:
        s.tables.add_relationship(**rel)
    output.print(f"OK {len(table_relationships)} 条关系")

    # 4. Cube
    output.print("\n[4/7] 注册 Cube...")
    cost_dims = [
        {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
        {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
        {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
        {"name": "region", "col": "region", "type": "string", "title": "片区"},
        {"name": "org_id", "col": "org_id", "type": "string", "title": "组织ID"},
        {"name": "org_name", "col": "org_name", "type": "string", "title": "组织名称"},
        {"name": "parent_org_id", "col": "parent_org_id", "type": "string", "title": "上级组织ID"},
        {"name": "cost_type_id", "col": "cost_type_id", "type": "string", "title": "科目ID"},
        {"name": "cost_type_name", "col": "cost_type_name", "type": "string", "title": "科目名称"},
        {"name": "parent_cost_type_id", "col": "parent_cost_type_id", "type": "string", "title": "上级科目ID"},
    ]
    cost_measures = [
        {"name": "cost_amount_total", "col": "cost_amount", "agg": "sum", "title": "成本合计"},
        {"name": "budget_total", "col": "budget_amount", "agg": "sum", "title": "预算合计"},
        {"name": "cost_count", "col": "cost_id", "agg": "count", "title": "成本行数"},
    ]
    s.register_cube(name="CostCube", table="fact_cost", title="成本分析Cube",
                    measures=cost_measures, dimensions=cost_dims)
    s.register_cube(
        name="OutputCube", table="fact_output", title="产值分析Cube",
        measures=[
            {"name": "output_amount_total", "col": "output_amount", "agg": "sum", "title": "产值合计"},
            {"name": "output_count", "col": "output_id", "agg": "count", "title": "产值行数"},
        ],
        dimensions=[
            {"name": "date_key", "col": "date_key", "type": "int", "title": "日期键"},
            {"name": "project_id", "col": "project_id", "type": "string", "title": "项目ID"},
            {"name": "project_name", "col": "project_name", "type": "string", "title": "项目名称"},
            {"name": "region", "col": "region", "type": "string", "title": "片区"},
            {"name": "org_id", "col": "org_id", "type": "string", "title": "组织ID"},
        ],
    )
    output.print("OK CostCube + OutputCube")

    s.upsert_derived_measures("CostCube", [
        {"name": "avg_cost", "title": "平均成本",
         "expression": "if(CostCube.cost_count > 0, CostCube.cost_amount_total / CostCube.cost_count, 0)",
         "description": "成本合计/行数"},
        {"name": "budget_variance", "title": "预算偏差",
         "expression": "CostCube.cost_amount_total - CostCube.budget_total",
         "description": "成本-预算"},
        {"name": "budget_exec_rate", "title": "预算执行率",
         "expression": "if(CostCube.budget_total > 0, CostCube.cost_amount_total / CostCube.budget_total, 0)",
         "description": "成本/预算"},
    ])
    output.print("OK CostCube 派生度量")

    # 5. 对象类型
    output.print("\n[5/7] 定义对象类型...")
    objects = [
        ("Project", "项目", "工程项目主数据", "主数据", "CostCube"),
        ("CostRecord", "成本记录", "项目成本流水", "事务", "CostCube"),
        ("Org", "组织", "公司/分公司/项目部", "主数据", "CostCube"),
        ("CostType", "成本科目", "成本科目树", "参考", None),
        ("OutputRecord", "产值记录", "项目产值流水", "事务", "OutputCube"),
        ("CostAnalysis", "成本分析", "成本指标聚合分析", "分析", "CostCube"),
    ]
    for code, name, desc, cat, cube in objects:
        s.onto.define_object_type(code=code, name=name, description=desc, category_347=cat)
        if cube:
            s.onto.bind_source(code, "dazi_cube", config={"cube": cube})
    output.print(f"OK {len(objects)} 个对象")

    # 6. 属性
    output.print("\n[6/7] 定义对象属性...")
    s.onto.define_property("Project", "id", "项目ID", semantic_role="dimension",
                           qualified_name="CostCube.project_id")
    s.onto.define_property("Project", "name", "项目名称", semantic_role="dimension",
                           qualified_name="CostCube.project_name")
    s.onto.define_property("Project", "region", "片区", semantic_role="dimension",
                           qualified_name="CostCube.region")
    s.onto.define_property("Project", "cost", "成本", semantic_role="measure",
                           qualified_name="CostCube.cost_amount_total")
    s.onto.define_property("Project", "avg_cost", "平均成本", semantic_role="measure",
                           qualified_name="CostCube.avg_cost")

    s.onto.define_property("CostRecord", "date", "日期", semantic_role="dimension",
                           qualified_name="CostCube.date_key")
    s.onto.define_property("CostRecord", "cost_type", "成本科目", semantic_role="dimension",
                           qualified_name="CostCube.cost_type_name")
    s.onto.define_property("CostRecord", "amount", "成本金额", semantic_role="measure",
                           qualified_name="CostCube.cost_amount_total")
    s.onto.define_property("CostRecord", "budget", "预算金额", semantic_role="measure",
                           qualified_name="CostCube.budget_total")
    s.onto.define_property("CostRecord", "variance", "预算偏差", semantic_role="measure",
                           qualified_name="CostCube.budget_variance")

    s.onto.define_property("Org", "id", "组织ID", semantic_role="dimension",
                           qualified_name="CostCube.org_id")
    s.onto.define_property("Org", "name", "组织名称", semantic_role="dimension",
                           qualified_name="CostCube.org_name")
    s.onto.define_property("Org", "cost", "成本", semantic_role="measure",
                           qualified_name="CostCube.cost_amount_total")

    s.onto.define_property("OutputRecord", "date", "日期", semantic_role="dimension",
                           qualified_name="OutputCube.date_key")
    s.onto.define_property("OutputRecord", "output", "产值", semantic_role="measure",
                           qualified_name="OutputCube.output_amount_total")
    s.onto.define_property("OutputRecord", "project", "项目名称", semantic_role="dimension",
                           qualified_name="OutputCube.project_name")

    s.onto.define_property("CostAnalysis", "cost", "成本合计", semantic_role="measure",
                           qualified_name="CostCube.cost_amount_total")
    s.onto.define_property("CostAnalysis", "avg_cost", "平均成本", semantic_role="measure",
                           qualified_name="CostCube.avg_cost")
    s.onto.define_property("CostAnalysis", "exec_rate", "预算执行率", semantic_role="measure",
                           qualified_name="CostCube.budget_exec_rate")
    output.print("OK 属性定义")

    # 7. 链接（含 join_spec 供 G2 resolve_join_path）
    output.print("\n[7/7] 定义链接类型...")
    link_defs = [
        ("cost_for_project", "成本归属项目", "CostRecord", "Project", "归属关系",
         "many_to_one", _link_extra([{"from": "project_id", "to": "project_id"}])),
        ("output_for_project", "产值归属项目", "OutputRecord", "Project", "归属关系",
         "many_to_one", _link_extra([{"from": "project_id", "to": "project_id"}])),
        ("project_belongs_org", "项目归属组织", "Project", "Org", "归属关系",
         "many_to_one", _link_extra([{"from": "org_id", "to": "org_id"}])),
        ("org_has_parent", "组织上级", "Org", "Org", "层级关系",
         "many_to_one", _link_extra([{"from": "parent_org_id", "to": "org_id"}])),
        ("cost_has_type", "成本归属科目", "CostRecord", "CostType", "归属关系",
         "many_to_one", _link_extra([{"from": "cost_type_id", "to": "cost_type_id"}])),
        ("costtype_has_parent", "科目上级", "CostType", "CostType", "层级关系",
         "many_to_one", _link_extra([{"from": "parent_type_id", "to": "cost_type_id"}])),
        ("analysis_by_project", "分析归因项目", "CostAnalysis", "Project", "分析归因",
         "many_to_one", _link_extra([{"from": "project_id", "to": "project_id"}])),
    ]
    for code, name, fr, to, cat, card, extra in link_defs:
        s.onto.define_link_type(
            code=code, name=name,
            from_object_type_code=fr, to_object_type_code=to,
            category_347=cat, cardinality=card, extra=extra,
        )
    output.print(f"OK {len(link_defs)} 条链接")

    s.sync_metric_refs()
    s.onto.engine.invalidate()
    output.print("OK sync_metric_refs + 引擎图谱缓存失效")

    summary = {
        "ok": True, "space_id": space_id,
        "tables": len(TABLE_REGISTRY),
        "relationships": len(table_relationships),
        "cubes": 2, "objects": len(objects), "links": len(link_defs),
    }
    output.success("本体引擎测试空间初始化完成")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True))

