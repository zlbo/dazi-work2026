# 本体动作（Action）开发

**文档 ID**: `onto/action-guide`

## Action 概念

Action 是可被外部系统触发的本体操作，通常用于：

- 写入数据
- 触发业务流程
- 执行审批操作

## 列出动作

```bash
dazi onto action list --space <space-id>
```

## 发布 Action

脚本放在 **`项目/<业务名>/本体/ontos/<实现名>/functions/`**（可与函数脚本同目录，用文件名区分）：

```bash
dazi onto script publish 项目/<业务名>/本体/ontos/<实现名>/functions/my_action.py \
  --space <space-id> \
  --register-action-id my_action_code \
  --register-action-permission-tag "finance.write"
```

`<space-id>` 取自实现单元 **`README.md`**（`项目/<业务名>/本体/ontos/<实现名>/README.md`）。

## 更新 Action 代码

```bash
dazi onto action update-code my_action_code \
  --space <space-id> \
  --stem my_action
```

## Action 脚本结构

```python
def main(params: dict, context: dict) -> dict:
    """
    Action 入口。
    context 包含触发者信息、权限标签等。
    """
    return {"status": "ok"}
```
