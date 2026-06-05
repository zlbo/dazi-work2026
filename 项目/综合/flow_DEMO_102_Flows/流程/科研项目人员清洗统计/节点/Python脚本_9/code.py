# -*- coding: utf-8 -*-
# 上游 output_variable_name = 项目人员关联
# 本节点 output_variable_name = 变量7lb
import pandas as pd

output.print("[Python脚本 9] 开始")

# 整图跑时 df 可能有值；单节点测试时优先 get_variable
if df is None or df.empty:
    df = get_variable("项目人员关联")

output.print(f"输入数据: shape={df.shape}, columns={list(df.columns)}")
output.print(f"输入人员数: {df['员工姓名'].nunique()}, 项目数: {df['科研项目'].nunique()}")

# 姓名空值保护，避免 str.startswith 报错
name_series = df["员工姓名"].astype(str)
valid_mask = df["员工姓名"].notna() & (name_series.str.strip() != "") & (name_series != "nan")
df_valid = df[valid_mask].copy()
output.print(f"有效姓名记录: {len(df_valid)} / {len(df)}")

# 筛选姓李的员工
li_mask = df_valid["员工姓名"].str.startswith("李")
df_li = df_valid[li_mask].copy()
output.print(f"姓李记录数: {len(df_li)}, 姓李员工数: {df_li['员工姓名'].nunique()}")

if df_li.empty:
    output.print("警告: 未找到姓李的员工，输出空表（保留标准列结构）")
    result_df = pd.DataFrame(columns=["员工姓名", "参与项目数", "参与项目列表", "员工编码", "匹配状态"])
else:
    # 注意：不要用 apply(list) 直接输出 —— 嵌套 list 列会导致 Parquet 落盘后 schema 拉取失败
    grouped = (
        df_li.groupby("员工姓名", as_index=False)
        .agg(
            参与项目数=("科研项目", "nunique"),
            参与项目列表=("科研项目", lambda s: "、".join(sorted(s.astype(str).unique()))),
            员工编码=("员工编码", "first"),
            匹配状态=("匹配状态", "first"),
        )
        .sort_values("参与项目数", ascending=False)
        .reset_index(drop=True)
    )
    count = len(grouped)
    output.print(f"姓李且参加过项目的员工数量: {count}")
    output.print(f"输出预览(前3行):\n{grouped.head(3).to_string(index=False)}")
    result_df = grouped

output.print(f"最终输出: shape={result_df.shape}, columns={list(result_df.columns)}")
output.print("[Python脚本 9] 完成")
