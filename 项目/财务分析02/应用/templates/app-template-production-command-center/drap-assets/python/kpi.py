# 生产指挥中心 KPI（script_asset 模板示例）

def main(params=None):
    params = params or {}
    rows = [
        {"label": "今日产量", "value": 12880, "unit": "件"},
        {"label": "计划达成", "value": 97.2, "unit": "%"},
        {"label": "一次合格率", "value": 99.3, "unit": "%"},
    ]
    return {
        "columns": ["label", "value", "unit"],
        "data": rows,
        "row_count": len(rows),
    }
