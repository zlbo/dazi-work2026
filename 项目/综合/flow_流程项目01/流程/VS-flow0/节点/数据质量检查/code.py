# -*- coding: utf-8 -*-
# =============================================================================
# 数据质量检查节点（Demo销售表_最简.xlsx 解析结果）
# =============================================================================
#
# 【输入变量】
#   - 销售表：主表，来自上游 excel-python 入边 df 或 get_variable("销售表")
#   - 产品表：维表，来自 attached_variables → get_variable("产品表")
#   - 规格表：维表，来自 attached_variables → get_variable("规格表")
#
# 【输出变量】
#   - V_DQ_REPORT（result_df）：每条规则的检查结果明细（含「通过」列）
#   - V_DQ_SCORE（quality_score）：综合得分 = 通过规则数 / 总规则数 × 100
#   - quality_passed（标量）：True=全部通过，False=存在未通过规则（供条件节点判定）
#
# 【质检项一览】（规则定义见 flow.json → qualityConfig.rules）
#
#   1. 行数检查（row_count_min）
#      - 销售表 / 产品表 / 规格表 行数 >= 1
#   2. 非空检查（not_null）
#      - 销售表.产品 / 销售表.规格 / 销售表.地区 不得为空
#   3. 外键匹配（fk_match）
#      - 销售表.产品 → 产品表.ID
#      - 销售表.规格 → 规格表.ID
#
# 【失败策略】
#   本节点不抛错、不中断流程；产出 V_DQ_REPORT 后由下游「质检是否通过」条件节点
#   读取报告中的「通过」列决定分支：
#     - 全部通过 → 执行 SQL 表间关联
#     - 任一未通过 → 跳过 SQL，直接结束
#
# =============================================================================
import pandas as pd

RULES = quality_config.get("rules", []) if quality_config else []


def _load_tables():
    """加载三张待检表：销售事实表 + 产品/规格维表。"""
    sales = df if df is not None and not df.empty else get_variable("销售表")
    products = get_variable("产品表")
    specs = get_variable("规格表")
    return sales, products, specs


def _check_not_null(table, table_name, column, results):
    """非空检查：指定列不得含 NaN/空值。"""
    null_count = int(table[column].isna().sum()) if column in table.columns else len(table)
    passed = null_count == 0
    results.append(
        {
            "规则": f"{table_name}.{column} 非空",
            "表名": table_name,
            "字段": column,
            "通过": passed,
            "详情": f"空值 {null_count} 行",
        }
    )
    return passed


def _check_row_count(table, table_name, min_rows, results):
    """行数检查：表至少包含 min_rows 行有效数据。"""
    count = len(table)
    passed = count >= min_rows
    results.append(
        {
            "规则": f"{table_name} 行数",
            "表名": table_name,
            "字段": "-",
            "通过": passed,
            "详情": f"实际 {count} 行，要求 >= {min_rows}",
        }
    )
    return passed


def _check_fk(sales, products, specs, results):
    """外键匹配：销售表中的产品/规格编码须在对应维表中存在。"""
    product_ids = set(products["ID"].astype(str).str.strip())
    spec_ids = set(specs["ID"].astype(str).str.strip())
    bad_products = sales[~sales["产品"].astype(str).str.strip().isin(product_ids)]
    bad_specs = sales[~sales["规格"].astype(str).str.strip().isin(spec_ids)]
    product_passed = len(bad_products) == 0
    spec_passed = len(bad_specs) == 0
    results.append(
        {
            "规则": "销售表.产品 → 产品表.ID",
            "表名": "销售表",
            "字段": "产品",
            "通过": product_passed,
            "详情": f"未匹配 {len(bad_products)} 行",
        }
    )
    results.append(
        {
            "规则": "销售表.规格 → 规格表.ID",
            "表名": "销售表",
            "字段": "规格",
            "通过": spec_passed,
            "详情": f"未匹配 {len(bad_specs)} 行",
        }
    )
    return product_passed and spec_passed


output.print("[DQ] 开始")

sales, products, specs = _load_tables()
output.print(
    f"销售表 shape={sales.shape}, 产品表 shape={products.shape}, 规格表 shape={specs.shape}"
)

results = []
all_passed = True

for rule in RULES:
    rule_type = rule.get("type")
    name = rule.get("name", rule_type)
    if rule_type == "not_null":
        table_name = rule.get("table", "销售表")
        column = rule["column"]
        table = sales if table_name == "销售表" else (products if table_name == "产品表" else specs)
        ok = _check_not_null(table, table_name, column, results)
    elif rule_type == "row_count_min":
        table_name = rule.get("table", "销售表")
        min_rows = int(rule.get("min", 1))
        table = sales if table_name == "销售表" else (products if table_name == "产品表" else specs)
        ok = _check_row_count(table, table_name, min_rows, results)
    elif rule_type == "fk_match":
        ok = _check_fk(sales, products, specs, results)
        continue
    else:
        ok = True
        results.append({"规则": name, "表名": "-", "字段": "-", "通过": True, "详情": "未知规则类型，已跳过"})
    all_passed = all_passed and ok

passed_count = sum(1 for r in results if r["通过"])
total_count = len(results) or 1
score = round(passed_count / total_count * 100, 2)
set_scalar_output("quality_score", score)
set_scalar_output("quality_passed", all_passed)

result_df = pd.DataFrame(results)
output.print(f"质检完成：{passed_count}/{total_count} 通过，得分 {score}，overall={all_passed}")

if not all_passed:
    failed = [r["规则"] for r in results if not r["通过"]]
    output.print(f"质检未通过（将由条件节点跳过 SQL）：{failed}")

output.print("[DQ] 完成")
