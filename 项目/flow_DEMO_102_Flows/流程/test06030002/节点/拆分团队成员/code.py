import pandas as pd

# 拆分团队成员 - 使用原始字符串路径
excel_path = r"D:\GitHub\dazi-work\资源\files\科研项目_模拟人员混杂数据.xlsx_72326a69\原文件.xlsx"

# 读取混杂数据 Sheet
df = pd.read_excel(excel_path, sheet_name="混杂数据")

# 拆分团队成员（用中文顿号分隔）
max_members = df["团队"].str.split("、", expand=True).shape[1]
split_df = df["团队"].str.split("、", expand=True)
split_df.columns = [f"成员{i+1}" for i in range(max_members)]

# 合并结果
result_df = pd.concat([df[["科研项目"]], split_df], axis=1)