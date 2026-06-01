"""库存本体初始化脚本 — space__0519

初始化内容：
1. 创建物理表（warehouse / snapshot / transaction；product_master 兼容建表）
2. 注册表到空间
3. 注册 Cube（5 个）及派生度量
4. 定义对象类型（6 种）、绑定数据源、属性、链接
5. 同步指标引用

放置：项目/onto_本体测试05/脚本/setup/inventory_ontology_init.py
发布：dazi-onto script publish 项目/onto_本体测试05/脚本/setup/inventory_ontology_init.py --space space__0519
"""

import json


def main():
    space_id = "space__0519"
    s = space.get(space_id)

    output.print("=== 库存本体初始化 ===")
    output.print(f"空间: {space_id}")

    # 1. 创建物理表
    output.print("\n[1/8] 创建物理表...")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS product_master (
            product_id String,
            product_code String,
            product_name String,
            product_category String,
            product_subcategory String,
            brand String,
            unit String,
            list_price Float64,
            cost_price Float64,
            status String,
            created_at DateTime DEFAULT now(),
            updated_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (product_id)
    """)
    output.print("OK product_master（与销售本体共用结构）")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS warehouse_dimension (
            warehouse_id String,
            warehouse_code String,
            warehouse_name String,
            warehouse_type String,
            region String,
            status String
        ) ENGINE = MergeTree()
        ORDER BY (warehouse_id)
    """)
    output.print("OK warehouse_dimension")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS inventory_balance_snapshot (
            snapshot_id String,
            snapshot_date Date,
            product_id String,
            warehouse_id String,
            on_hand_qty Float64,
            available_qty Float64,
            in_transit_qty Float64,
            reserved_qty Float64,
            safety_stock Float64,
            unit_cost Float64,
            inventory_amount Float64
        ) ENGINE = MergeTree()
        ORDER BY (snapshot_date, warehouse_id, product_id)
    """)
    output.print("OK inventory_balance_snapshot")

    s.sql.execute("""
        CREATE TABLE IF NOT EXISTS inventory_transaction (
            transaction_id String,
            transaction_time DateTime,
            transaction_date Date,
            product_id String,
            warehouse_id String,
            to_warehouse_id String,
            transaction_type String,
            source_doc_type String,
            source_doc_id String,
            quantity Float64,
            unit_cost Float64,
            amount Float64,
            batch_no String,
            operator String
        ) ENGINE = MergeTree()
        ORDER BY (transaction_date, warehouse_id, product_id, transaction_id)
    """)
    output.print("OK inventory_transaction")

    # 2. 注册表
    output.print("\n[2/8] 注册表到空间...")

    for tbl, label in [
        ("product_master", "产品/SKU主数据表"),
        ("warehouse_dimension", "仓库维度表"),
        ("inventory_balance_snapshot", "库存余额快照表"),
        ("inventory_transaction", "库存流水表"),
    ]:
        s.tables.register(tbl, label=label)
        s.tables.sync_columns(tbl)
        output.print(f"OK {tbl}")

    # 3. 注册 Cube
    output.print("\n[3/8] 注册 Cube...")

    snap = "inventory_balance_snapshot"
    snap_measures = [
        {"name": "on_hand_qty", "col": "on_hand_qty", "agg": "sum", "title": "现存量"},
        {"name": "available_qty", "col": "available_qty", "agg": "sum", "title": "可用量"},
        {"name": "in_transit_qty", "col": "in_transit_qty", "agg": "sum", "title": "在途量"},
        {"name": "inventory_amount", "col": "inventory_amount", "agg": "sum", "title": "库存金额"},
        {"name": "sku_count", "col": "product_id", "agg": "uniq", "title": "SKU数"},
        {"name": "warehouse_count", "col": "warehouse_id", "agg": "uniq", "title": "仓库数"},
    ]
    snap_dims = [
        {"name": "snapshot_date", "col": "snapshot_date", "type": "date", "title": "快照日期"},
        {"name": "product_id", "col": "product_id", "type": "string", "title": "产品ID"},
        {"name": "warehouse_id", "col": "warehouse_id", "type": "string", "title": "仓库ID"},
        {"name": "safety_stock", "col": "safety_stock", "type": "number", "title": "安全库存"},
    ]

    s.register_cube(
        name="InventoryCube",
        table=snap,
        title="库存分析主Cube",
        measures=snap_measures,
        dimensions=snap_dims,
    )
    output.print("OK InventoryCube")

    s.register_cube(
        name="WarehouseInventoryCube",
        table=snap,
        title="仓库库存Cube",
        measures=[
            {"name": "on_hand_qty", "col": "on_hand_qty", "agg": "sum", "title": "现存量"},
            {"name": "available_qty", "col": "available_qty", "agg": "sum", "title": "可用量"},
            {"name": "inventory_amount", "col": "inventory_amount", "agg": "sum", "title": "库存金额"},
            {"name": "sku_count", "col": "product_id", "agg": "uniq", "title": "SKU数"},
        ],
        dimensions=[
            {"name": "warehouse_id", "col": "warehouse_id", "type": "string", "title": "仓库ID"},
        ],
    )
    output.print("OK WarehouseInventoryCube")

    s.register_cube(
        name="SkuInventoryCube",
        table=snap,
        title="SKU库存Cube",
        measures=[
            {"name": "on_hand_qty", "col": "on_hand_qty", "agg": "sum", "title": "现存量"},
            {"name": "available_qty", "col": "available_qty", "agg": "sum", "title": "可用量"},
            {"name": "inventory_amount", "col": "inventory_amount", "agg": "sum", "title": "库存金额"},
        ],
        dimensions=[
            {"name": "product_id", "col": "product_id", "type": "string", "title": "产品ID"},
        ],
    )
    output.print("OK SkuInventoryCube")

    txn = "inventory_transaction"
    s.register_cube(
        name="InventoryMovementCube",
        table=txn,
        title="库存流水Cube",
        measures=[
            {"name": "quantity", "col": "quantity", "agg": "sum", "title": "变动数量"},
            {"name": "amount", "col": "amount", "agg": "sum", "title": "变动金额"},
            {"name": "txn_count", "col": "transaction_id", "agg": "uniq", "title": "流水笔数"},
        ],
        dimensions=[
            {"name": "transaction_date", "col": "transaction_date", "type": "date", "title": "业务日期"},
            {"name": "product_id", "col": "product_id", "type": "string", "title": "产品ID"},
            {"name": "warehouse_id", "col": "warehouse_id", "type": "string", "title": "仓库ID"},
            {"name": "transaction_type", "col": "transaction_type", "type": "string", "title": "流水类型"},
            {"name": "source_doc_type", "col": "source_doc_type", "type": "string", "title": "来源类型"},
            {"name": "transaction_id", "col": "transaction_id", "type": "string", "title": "流水ID"},
        ],
    )
    output.print("OK InventoryMovementCube")

    s.register_cube(
        name="TimeInventoryCube",
        table=snap,
        title="库存时间维度Cube",
        measures=[
            {"name": "on_hand_qty", "col": "on_hand_qty", "agg": "sum", "title": "现存量"},
            {"name": "inventory_amount", "col": "inventory_amount", "agg": "sum", "title": "库存金额"},
            {"name": "sku_count", "col": "product_id", "agg": "uniq", "title": "SKU数"},
        ],
        dimensions=[
            {"name": "snapshot_date", "col": "snapshot_date", "type": "date", "title": "快照日期"},
        ],
    )
    output.print("OK TimeInventoryCube")

    # 4. 派生度量
    output.print("\n[4/8] 配置派生度量...")

    s.upsert_derived_measures(
        "InventoryCube",
        [
            {
                "name": "stock_shortage_flag",
                "title": "缺货标记",
                "expression": "if(InventoryCube.available_qty < InventoryCube.safety_stock, 1, 0)",
                "description": "可用量低于安全库存为1",
            },
            {
                "name": "fill_rate",
                "title": "安全库存满足率",
                "expression": "if(InventoryCube.safety_stock > 0, InventoryCube.available_qty / InventoryCube.safety_stock, 0)",
                "description": "可用量/安全库存",
            },
        ],
    )
    output.print("OK 派生度量")

    # 5. 对象类型
    output.print("\n[5/8] 定义对象类型...")

    object_types = [
        ("InventoryItem", "库存物料", "可库存管理的SKU业务对象"),
        ("Warehouse", "仓库", "仓储节点业务对象"),
        ("StockBalance", "库存余额", "某时点某仓某SKU的余额对象"),
        ("StockMovement", "库存流水", "单次入出库/调拨/调整事件"),
        ("InventoryAnalysis", "库存分析", "多维度库存指标聚合对象"),
        ("ReplenishmentAlert", "补货预警", "低于安全库存的预警业务对象"),
    ]
    for code, name, desc in object_types:
        s.onto.define_object_type(code, name, description=desc)
        output.print(f"OK {code}")

    # 6. 绑定数据源
    output.print("\n[6/8] 绑定数据源...")

    bindings = [
        ("InventoryItem", "SkuInventoryCube"),
        ("Warehouse", "WarehouseInventoryCube"),
        ("StockBalance", "InventoryCube"),
        ("StockMovement", "InventoryMovementCube"),
        ("InventoryAnalysis", "InventoryCube"),
        ("ReplenishmentAlert", "InventoryCube"),
    ]
    for obj, cube in bindings:
        s.onto.bind_source(obj, "dazi_cube", config={"cube": cube})
        output.print(f"OK {obj} -> {cube}")

    # 7. 属性
    output.print("\n[7/8] 定义属性...")

    def define_props(obj_code, props):
        for code, name, role, qn in props:
            s.onto.define_property(obj_code, code, name, semantic_role=role, qualified_name=qn)

    define_props("InventoryItem", [
        ("id", "SKU ID", "dimension", "SkuInventoryCube.product_id"),
        ("on_hand_qty", "现存量", "measure", "SkuInventoryCube.on_hand_qty"),
        ("available_qty", "可用量", "measure", "SkuInventoryCube.available_qty"),
        ("inventory_amount", "库存金额", "measure", "SkuInventoryCube.inventory_amount"),
    ])
    output.print("OK InventoryItem 属性 (4)")

    define_props("Warehouse", [
        ("id", "仓库ID", "dimension", "WarehouseInventoryCube.warehouse_id"),
        ("on_hand_qty", "现存量", "measure", "WarehouseInventoryCube.on_hand_qty"),
        ("inventory_amount", "库存金额", "measure", "WarehouseInventoryCube.inventory_amount"),
        ("sku_count", "SKU数", "measure", "WarehouseInventoryCube.sku_count"),
    ])
    output.print("OK Warehouse 属性 (4)")

    define_props("StockBalance", [
        ("date", "快照日期", "dimension", "InventoryCube.snapshot_date"),
        ("on_hand_qty", "现存量", "measure", "InventoryCube.on_hand_qty"),
        ("available_qty", "可用量", "measure", "InventoryCube.available_qty"),
    ])
    output.print("OK StockBalance 属性 (3)")

    define_props("StockMovement", [
        ("id", "流水ID", "dimension", "InventoryMovementCube.transaction_id"),
        ("date", "业务日期", "dimension", "InventoryMovementCube.transaction_date"),
        ("type", "流水类型", "dimension", "InventoryMovementCube.transaction_type"),
        ("quantity", "数量", "measure", "InventoryMovementCube.quantity"),
    ])
    output.print("OK StockMovement 属性 (4)")

    define_props("InventoryAnalysis", [
        ("date", "日期", "dimension", "InventoryCube.snapshot_date"),
        ("warehouse_id", "仓库", "dimension", "InventoryCube.warehouse_id"),
        ("on_hand_qty", "现存量", "measure", "InventoryCube.on_hand_qty"),
        ("inventory_amount", "库存金额", "measure", "InventoryCube.inventory_amount"),
    ])
    output.print("OK InventoryAnalysis 属性 (4)")

    define_props("ReplenishmentAlert", [
        ("product_id", "SKU", "dimension", "InventoryCube.product_id"),
        ("warehouse_id", "仓库", "dimension", "InventoryCube.warehouse_id"),
    ])
    output.print("OK ReplenishmentAlert 属性 (2)")

    # 8. 链接类型
    output.print("\n[8/8] 定义链接与同步指标...")

    link_types = [
        ("balance_for_item", "余额属于物料", "StockBalance", "InventoryItem", "快照行对应SKU"),
        ("balance_at_warehouse", "余额位于仓库", "StockBalance", "Warehouse", "快照行所在仓"),
        ("movement_of_item", "流水变动物料", "StockMovement", "InventoryItem", "流水对应SKU"),
        ("movement_at_warehouse", "流水发生于仓库", "StockMovement", "Warehouse", "流水仓库"),
        ("item_stored_in_warehouse", "物料存放于仓", "InventoryItem", "Warehouse", "物料与仓库多对多"),
        ("analysis_by_item", "分析归因物料", "InventoryAnalysis", "InventoryItem", "指标按SKU切片"),
        ("analysis_by_warehouse", "分析归因仓库", "InventoryAnalysis", "Warehouse", "指标按仓切片"),
        ("alert_for_item", "预警针对物料", "ReplenishmentAlert", "InventoryItem", "缺货预警对象"),
        ("alert_at_warehouse", "预警位于仓库", "ReplenishmentAlert", "Warehouse", "按仓预警"),
        ("warehouse_holds_balances", "仓库持有余额", "Warehouse", "StockBalance", "仓库下多条快照"),
    ]
    for code, name, from_obj, to_obj, desc in link_types:
        s.onto.define_link_type(
            code=code,
            name=name,
            from_object_type_code=from_obj,
            to_object_type_code=to_obj,
            description=desc,
        )
        output.print(f"OK {code}")

    s.sync_metric_refs()
    output.print("OK sync_metric_refs")

    summary = {
        "ok": True,
        "space_id": space_id,
        "tables": 4,
        "cubes": 5,
        "object_types": 6,
        "link_types": 10,
    }

    output.print("\n=== 库存本体初始化完成 ===")
    output.success("初始化成功")
    output.print("__JSON_SUMMARY__" + json.dumps(summary, ensure_ascii=True, default=str))
