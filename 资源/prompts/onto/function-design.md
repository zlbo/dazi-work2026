# 提示词：本体函数设计

**提示词 ID**: `onto/function-design`  
**场景**: 设计新的本体函数

---

你是一名搭子平台本体工程师。请根据以下需求设计一个本体函数（ontology function）。

**执行脚本前必读**：`资源/docs/onto/脚本运行常见错误处理.md`（`onto/script-run-troubleshooting`）。  
**必须复制结构**：`资源/examples/onto/_templates/ontology_function_template.py` 或 `销售示例/functions/sales_fn_get_summary.py`。

## 函数需求

{{function_description}}

## 要求

1. 文件名 `snake_case`，如 `cost_fn_get_summary.py`；`function_id` 如 `domain.fn.get_summary`
2. **`def main():` 无参** — 禁止 `main(params: dict)`；入参来自 `ctx.params`
3. 业务逻辑写在 **`_ontology_fn_body(p)`**；`main()` 末尾 **`return _ontology_fn_body(p)`**
4. 输出使用 **`return p.function_result(columns=..., data=..., row_count=...)`** — **禁止** `output.print_json()`、`print()` 作为平台输出
5. SQL 用 **`p.sql.query()`** 取多列；聚合勿误用 `query_one().get()`
6. 脚本顶部 **`TEST_ARGUMENTS`** 与 `functions/test_arguments/<function_id>.json` 同步
7. 中文 docstring：目的、参数、返回值、发布命令

## 输出格式（必须遵循）

```python
TEST_ARGUMENTS = {
    "v": 1,
    "arguments": { ... },
    "object_type_code": "<ObjectTypeCode>",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    # ... p.sql.query(...)
    return p.function_result(
        columns=[...],
        data=[{...}],
        row_count=1,
    )


def main():
    s = space.get(ctx.space_id or "")
    _Ports = type(
        "_Ports",
        (),
        {
            "get_params": lambda self: dict(ctx.params or {}),
            "function_result": lambda self, **kw: onto.function_result(**kw),
        },
    )
    p = _Ports()
    p.sql = s.sql
    return _ontology_fn_body(p)
```

脚本落盘：`项目/<业务名>/本体/ontos/<实现名>/functions/<file>.py`

发布与运行（dazi-work 根；**勿用** `dazi-onto`）：

```powershell
dazi onto script publish 项目/<业务名>/本体/ontos/<实现名>/functions/<file>.py --space <space-id> --register-function-id <id>
dazi onto function run <id> --space <space-id>
dazi onto function save-test-arguments <ofn_internal_id> --space <space-id> `
  --arguments-json-file 项目/<业务名>/本体/ontos/<实现名>/functions/test_arguments/<id>.json
```

详见 `onto/script-publish-run`、`onto/function-guide`。
