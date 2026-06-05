import pandas as pd

output.print("[Excel解析] 开始读取Excel文件")
output.print(f"source={excel_original_filename or excel_source_path}")

df_people = pd.read_excel(excel_source_path, sheet_name="人员名单", header=0, usecols="A:B")
output.print(f"人员名单: shape={df_people.shape}, columns={list(df_people.columns)}")

df_mixed = pd.read_excel(excel_source_path, sheet_name="混杂数据", header=0, usecols="A:B")
output.print(f"混杂数据: shape={df_mixed.shape}, columns={list(df_mixed.columns)}")

set_table_output("人员名单", df_people)
set_table_output("混杂数据", df_mixed)

output.print("[Excel解析] 完成")