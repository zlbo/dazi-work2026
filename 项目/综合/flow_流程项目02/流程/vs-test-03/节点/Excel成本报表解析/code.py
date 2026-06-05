# -*- coding: utf-8 -*-
# 画布：managed_file_id = 51853ede-9e6b-4a3a-aa7a-060cbead0862
# 画布：output_variable_name = 成本统计报表
import pandas as pd

OUTPUT_VAR = "成本统计报表"  # 必须与 output_variable_name 一致
DATA_START_ROW = 4           # 0-based，Excel 第 5 行起为数据

COLUMN_NAMES = [
    "基本信息_组织", "基本信息_年度", "基本信息_月度", "基本信息_项目",
    "成本项_管理费", "成本项_间接成本", "成本项_税金",
    "成本项_直接成本_安全文明施工费", "成本项_直接成本_材料",
    "成本项_直接成本_机械", "成本项_直接成本_劳务分包",
    "成本项_直接成本_专业分包", "成本项_直接成本_直接成本",
    "成本比较_实际成本", "成本比较_目标成本", "成本比较_实目比"
]

output.print("[excel-python] 开始")
output.print(f"source={excel_original_filename or excel_source_path}")

# ✅ 正确：读引擎注入的路径
raw = pd.read_excel(
    excel_source_path,
    sheet_name="Sheet1",
    header=None,
    skiprows=DATA_START_ROW,
    usecols="A:P",
    names=COLUMN_NAMES,
)
table = raw.dropna(how="all")

output.print(f"{OUTPUT_VAR} shape={table.shape}")
set_table_output(OUTPUT_VAR, table)  # 主输出，名称必须与 output_variable_name 一致
output.print("[excel-python] 完成")