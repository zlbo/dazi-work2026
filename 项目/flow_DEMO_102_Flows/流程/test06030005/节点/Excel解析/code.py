# -*- coding: utf-8 -*-
import pandas as pd

# 读取Excel文件的所有sheet
excel_file = pd.ExcelFile(excel_source_path)
sheet_names = excel_file.sheet_names

# 遍历每个sheet并输出为表
for sheet_name in sheet_names:
    # 读取sheet数据
    df = excel_file.parse(sheet_name)
    # 将每个sheet输出为单独的表
    set_table_output(sheet_name, df)