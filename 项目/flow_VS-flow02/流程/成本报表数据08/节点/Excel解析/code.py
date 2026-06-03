# -*- coding: utf-8 -*-
# 输入：Excel成本报表08.xlsx（managed_file_id: 51853ede-9e6b-4a3a-aa7a-060cbead0862）
# 输出：成本统计报表（表变量）
import pandas as pd

OUTPUT_VAR = "成本统计报表"
DATA_START_ROW = 4  # 0-based，对应 Excel 第 5 行

COLUMN_NAMES = [
    "基本信息_组织",
    "基本信息_年度",
    "基本信息_月度",
    "基本信息_项目",
    "成本项_管理费",
    "成本项_间接成本",
    "成本项_税金",
    "成本项_直接成本_安全文明施工费",
    "成本项_直接成本_材料",
    "成本项_直接成本_机械",
    "成本项_直接成本_劳务分包",
    "成本项_直接成本_专业分包",
    "成本项_直接成本_直接成本",
    "成本比较_实际成本",
    "成本比较_目标成本",
    "成本比较_实目比",
]

NUMERIC_COLUMNS = [
    "基本信息_年度",
    "基本信息_月度",
    *COLUMN_NAMES[4:],
]
STRING_COLUMNS = ["基本信息_组织", "基本信息_项目"]


def _normalize_cost_report(df):
    df = df.copy()
    df = df.dropna(how="all")

    for col in STRING_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df.loc[df[col].isin(["", "nan", "None"]), col] = pd.NA

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


output.print("[Excel解析] 开始读取 Excel 成本报表")
output.print(f"source={excel_original_filename or excel_source_path}")

raw = pd.read_excel(
    excel_source_path,
    sheet_name="Sheet1",
    header=None,
    skiprows=DATA_START_ROW,
    usecols="A:P",
    names=COLUMN_NAMES,
)
table = _normalize_cost_report(raw)

output.print(f"{OUTPUT_VAR}: shape={table.shape}, columns={list(table.columns)}")
set_table_output(OUTPUT_VAR, table)
output.print("[Excel解析] 完成")
