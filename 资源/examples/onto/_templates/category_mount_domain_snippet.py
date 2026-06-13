"""category_mount 脚本片段 — 复制到 setup/*_category_mount.py 末尾

与 CATEGORY_REGISTRY 同文件维护；DOMAIN_CODE 改为快速启动 §1 本体域 code。
"""

import json

# DOMAIN_CODE = "<快速启动 §1 本体域 code>"
# DOMAIN_NAME = "<本体域名称>"


def _flatten_for_domain(reg):
    """CATEGORY_REGISTRY → DOMAIN_REGISTRY members（relation 元组暂跳过）。"""
    kind_map = {"object": "object_type", "link": "link_type"}
    members = {}
    for kind, cats in reg.items():
        if kind == "relation":
            continue
        dk = kind_map.get(kind, kind)
        keys = []
        for items in cats.values():
            for item in items:
                if isinstance(item, tuple):
                    continue
                keys.append(item)
        if keys:
            members[dk] = keys
    return members


def _mount_categories_and_domain(s, category_registry, domain_code, domain_name):
    cat_counts = s.categories.apply_registry(category_registry, skip_missing=True)
    domain_summary = s.domain.apply_registry(
        {
            "code": domain_code,
            "name": domain_name,
            "members": _flatten_for_domain(category_registry),
        },
        strict=False,
    )
    return cat_counts, domain_summary
