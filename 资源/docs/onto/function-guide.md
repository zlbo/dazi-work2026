# 本体函数开发指南

**文档 ID**: `onto/function-guide`

> **执行脚本前必读**：[`脚本运行常见错误处理.md`](./脚本运行常见错误处理.md)（CLI、SQL、`output.print_json` 等常见误用）。

## 函数生命周期

```
编写 .py → publish-preview（本地静态预检）→ publish（--register-function-id 入库）
  → function run 验证（无参回退 TEST_ARGUMENTS）→ save-test-arguments（写入 test_arguments，侧栏预填）
  → 后续改代码：update-code
```

工作路径：`项目/<业务名>/本体/ontos/<实现名>/functions/`；本地 JSON：`functions/test_arguments/<function_id>.json`。

## 新建函数

**推荐**：复制 `资源/examples/onto/_templates/ontology_function_template.py` 或 `销售示例/functions/sales_fn_*.py`，再改业务逻辑。

```bash
# 发布新函数（路径指向本体实现单元 functions/ 目录）
dazi onto script publish 项目/<业务名>/本体/ontos/<实现名>/functions/my_func.py \
  --space <space-id> \
  --register-function-id domain.fn.my_analysis
```

`<space-id>` 取自 **`项目/<业务名>/本体/ontos/<实现名>/README.md`**。

## 更新已有函数代码

```bash
dazi onto function update-code <function-id> \
  --space <space-id> \
  --stem my_func
```

`--stem` 为脚本文件名（不含扩展名），须与 `functions/` 下文件一致。

## 运行函数

```bash
dazi onto function run <function-id> \
  --space <space-id> \
  --params '{}'
```

> **`function run` 不支持 `--arguments-json-file`**。详见 [脚本运行常见错误处理](./脚本运行常见错误处理.md#4-cli-参数误用)。

PowerShell 下复杂 JSON 建议用环境变量 `DAZI_PARAMS` 或侧栏运行（使用已保存的 `test_arguments`）。详见 [本体脚本编写指南](./本体脚本编写指南.md#函数测试参数test_arguments发布后必做)。

## 保存测试参数（test_arguments）

函数 **`run` 验证通过后**，须将默认入参写入函数定义，侧栏 **Onto → 运行函数** 才会预填。

**本地文件**：`functions/test_arguments/<function_id>.json`（格式见 [本体脚本编写指南](./本体脚本编写指南.md)）。

```bash
dazi onto function save-test-arguments --function-id domain.fn.my_analysis \
    --space <space-id> \
    --arguments-json-file 项目/<业务名>/本体/ontos/<实现名>/functions/test_arguments/<function_id>.json
```

> **注意**：亦可用平台**内部 id** `ofn_xxx`（`dazi onto function list --json` 返回）；推荐 `--function-id` 别名。

## 函数脚本结构（标准模板）

本体函数与 setup/seed 脚本不同：**`main()` 无参**，平台注入 `ctx`、`space`、`onto`；**必须 return** `function_result`，**禁止** `output.print_json()`。

```python
TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30"},
    "object_type_code": "SalesAnalysis",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    start_date = params.get("start_date", "")
    end_date = params.get("end_date", "")

    rows = p.sql.query(f"SELECT sum(amount) AS total FROM fact WHERE date >= '{start_date}'")
    row = rows[0] if rows else {}
    total = float(row.get("total", 0) or 0)

    return p.function_result(
        columns=["total"],
        data=[{"total": total}],
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

| 要点 | 说明 |
| ---- | ---- |
| 入口 | **`def main():`**（无 `params` 形参） |
| 入参 | `ctx.params` → `p.get_params()` |
| 空间 / SQL | `s = space.get(ctx.space_id)` → `p.sql = s.sql` |
| 出参 | **`return p.function_result(columns=..., data=..., row_count=...)`** |
| 禁止 | `output.print_json`、`main(params: dict)`、裸 `return {"k": v}` |

可复制模板：`资源/examples/onto/_templates/ontology_function_template.py` · 参考实现：`销售示例/functions/sales_fn_get_summary.py`。

## 相关文档

- [脚本运行常见错误处理](./脚本运行常见错误处理.md)
- [本体脚本编写指南](./本体脚本编写指南.md)
- [DaziScript SDK 参考](./dazi_script_sdk_reference.md)
