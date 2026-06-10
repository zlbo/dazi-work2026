"""V3 本体函数公共工具（NaN/Inf 安全转换）

ClickHouse avg/avgIf 无匹配行时返回 NaN，Python 中 NaN 为 truthy，
`float(v or 0)` 无法兜底。各函数脚本内联相同实现（远程执行无法 import  sibling）。
"""

import math


def _safe_float(v, default=0.0):
    try:
        x = float(v if v is not None else default)
        return x if math.isfinite(x) else default
    except (TypeError, ValueError):
        return default


def _safe_round(v, ndigits=4, default=0.0):
    return round(_safe_float(v, default), ndigits)
