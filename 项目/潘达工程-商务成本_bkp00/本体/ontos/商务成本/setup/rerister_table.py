"""重新注册表的元数据"""

def main():
    space_id = "space__panda_construction"
    s = space.get(space_id)

    TABLE_REGISTRY = {
        "fact_project_output": {
            "display_name": "项目产值事实表",
            "description": "项目产值数据；含已确认/待确认双轨制",
            "columns": [
                {"name": "id", "display_name": "记录ID", "description": "主键"},
                {"name": "project_id", "display_name": "项目ID", "description": "关联dim_project"},
                {"name": "date_key", "display_name": "日期键", "description": "关联dim_date"},
                {"name": "report_period", "display_name": "报告期间"},
                {"name": "output_value", "display_name": "产值金额"},
                {"name": "output_tax", "display_name": "税金"},
                {"name": "output_without_tax", "display_name": "不含税产值"},
                {"name": "output_type", "display_name": "产值类型"},
                {"name": "output_ratio", "display_name": "产值比例"},
                {"name": "confirm_type", "display_name": "确认类型", "description": "已确认/待确认"},
                {"name": "confirmed_output", "display_name": "已确认产值"},
                {"name": "pending_output", "display_name": "待确认产值"},
                {"name": "created_at", "display_name": "创建时间"},
            ],
        },
    }

    output.print("=== 重新注册 fact_project_output ===")
    for tbl_name, meta in TABLE_REGISTRY.items():
        output.print(f"注册表: {tbl_name}")
        output.print(f"  display_name: {meta['display_name']}")
        output.print(f"  columns 数量: {len(meta['columns'])}")
        for col in meta["columns"]:
            output.print(f"    - {col['name']} -> {col['display_name']}")

        s.tables.register_with_meta(
            table_name=tbl_name,
            display_name=meta["display_name"],
            description=meta.get("description"),
            columns=meta["columns"],
            force_column_meta=True,
        )
        output.print(f"注册完成: {tbl_name}")

    output.print("\n=== 验证注册结果 ===")
    result = s.sql.query("""
        SELECT name as column_name, comment as display_name
        FROM system.columns
        WHERE database = 'space__panda_construction'
          AND table = 'fact_project_output'
        ORDER BY name
    """)

    for row in result:
        output.print(f"字段: {row.get('column_name', 'N/A')} | 显示名: {row.get('display_name', '(空)')}")
