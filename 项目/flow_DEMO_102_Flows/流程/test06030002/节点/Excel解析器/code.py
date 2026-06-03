import pandas as pd

# Excel 解析器 - 使用原始字符串路径
excel_path = r"D:\GitHub\dazi-work\资源\files\科研项目_模拟人员混杂数据.xlsx_72326a69\原文件.xlsx"
df = pd.read_excel(excel_path, sheet_name="混杂数据")
result_df = df