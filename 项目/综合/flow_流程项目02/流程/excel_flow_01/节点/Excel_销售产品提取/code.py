# -*- coding: utf-8 -*-
# 输入：Demo销售表_最简.xlsx（managed_file_id）
# 输出：销售表 / 产品表（2 个表变量）
# 表结构参考：资源/files/Demo销售表_最简.xlsx_e907853f/表结构.json
import pandas as pd

SHEETS = {
    "销售表": {"sheet_name": "销售表", "header": 0, "usecols": "A:H"},
    "产品表": {"sheet_name": "产品表", "header": 1, "usecols": "A:C"},
}


def _normalize_sales(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(how="all")
    if "ID" in df.columns:
        df["ID"] = pd.to_numeric(df["ID"], errors="coerce").astype("Int64")
    for col in ("数量", "金额"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "日期" in df.columns:
        df["日期"] = pd.to_datetime(df["日期"], errors="coerce")
    for col in ("地区", "产品", "规格", "颜色"):
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df


def _normalize_dim(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(how="all")
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
    return df


output.print("[excel-python] 开始")
output.print(f"source={excel_original_filename or excel_source_path}")

for var_name, kwargs in SHEETS.items():
    raw = pd.read_excel(excel_source_path, **kwargs)
    table = _normalize_sales(raw) if var_name == "销售表" else _normalize_dim(raw)
    output.print(f"{var_name} shape={table.shape}, columns={list(table.columns)}")
    set_table_output(var_name, table)

output.print("[excel-python] 完成")
