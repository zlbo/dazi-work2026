# 提示词：本体动作设计

**提示词 ID**: `onto/action-design`  
**场景**: 设计 Action（可被外部触发的写操作）

---

你是一名搭子平台本体工程师。请根据以下需求设计一个本体动作（ontology action）。

## 动作需求

{{action_description}}

## Action 特点

- **写操作**：Action 通常执行写入、更新、触发等操作
- **权限标签**：需要指定 `permissionTag`（如 `finance.write`）
- **上下文**：可访问触发者信息（`context.user_id`、`context.org_id`）

## 函数模板

```python
def main(params: dict, context: dict, s=None) -> dict:
    """
    [动作说明]

    Args:
        params: 动作参数
        context: 触发上下文（user_id, org_id, permission_tags 等）

    Returns:
        {"status": "ok", ...}
    """
    # 权限检查（可选）
    if "finance.write" not in context.get("permission_tags", []):
        raise PermissionError("缺少 finance.write 权限")

    # 执行写操作

    return {"status": "ok"}
```

发布命令（v3；**勿用** `dazi-onto`）：

```powershell
dazi onto script publish 项目/onto_<名>/脚本/<file>.py --space <space-id> --register-action-id <action_code> --register-action-permission-tag "finance.write"
```

详见提示词 `onto/script-publish-run`。
