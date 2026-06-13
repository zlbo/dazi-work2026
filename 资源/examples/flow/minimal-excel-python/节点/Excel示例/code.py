# -*- coding: utf-8 -*-
# 示例：excel-python 最小代码（复制到真实流程目录后替换 managed_file_id）
import pandas as pd

OUTPUT_VAR = "示例输出表"
raw = pd.read_excel(excel_source_path, sheet_name=0)
set_table_output(OUTPUT_VAR, raw)
