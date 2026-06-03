import pandas as pd

# 使用 excel_source_path 读取服务端文件（由平台自动注入）
xls = pd.ExcelFile(excel_source_path)
sheet_names = xls.sheet_names

# 读取第一个sheet的数据
df = pd.read_excel(excel_source_path, sheet_name=sheet_names[0])

# 使用 set_table_output 输出到流程变量（output_variable_name 为 'excel_data'）
set_table_output('excel_data', df)