# -*- coding: utf-8 -*-
# 画布：managed_file_id 见 flow.json
# 画布：output_variable_name = 成本统计报表
import pandas as pd

OUTPUT_VAR = "成本统计报表"
DATA_START_ROW = 4  # 0-based，Excel 第 5 行起为数据

SOURCE_COLUMNS = [
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

RENAME_COLUMNS = {
    "基本信息_组织": "组织",
    "基本信息_年度": "年度",
    "基本信息_月度": "月度",
    "基本信息_项目": "项目",
    "成本项_管理费": "月度管理费",
    "成本项_间接成本": "间接成本",
    "成本项_税金": "税金",
    "成本项_直接成本_安全文明施工费": "安全文明施工费",
    "成本项_直接成本_材料": "材料",
    "成本项_直接成本_机械": "机械",
    "成本项_直接成本_劳务分包": "劳务分包",
    "成本项_直接成本_专业分包": "专业分包",
    "成本项_直接成本_直接成本": "直接成本",
    "成本比较_实际成本": "实际成本",
    "成本比较_目标成本": "目标成本",
    "成本比较_实目比": "实目比",
}

ALL_COLUMN_NAMES = [
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

output.print("[excel-python] 开始")
output.print(f"source={excel_original_filename or excel_source_path}")

raw = pd.read_excel(
    excel_source_path,
    sheet_name="Sheet1",
    header=None,
    skiprows=DATA_START_ROW,
    usecols="A:P",
    names=ALL_COLUMN_NAMES,
)
df = raw.dropna(how="all").reset_index(drop=True)

# 去除总计行（须在裁剪列之前，依赖「基本信息_项目」）
df = df[~df.astype(str).apply(lambda x: x.str.contains("合计|总计|汇总", na=False)).any(axis=1)]

df = df[SOURCE_COLUMNS].rename(columns=RENAME_COLUMNS)

output.print(f"{OUTPUT_VAR} shape={df.shape}, columns={list(df.columns)}")
set_table_output(OUTPUT_VAR, df)
output.print("[excel-python] 完成")
