# functions

本体函数脚本。发布须带 `--register-function-id`，与 `plans/` 规划文档中的 function_id 一致。

**新建函数**：复制 `资源/examples/onto/_templates/ontology_function_template.py`（`dazi examples show onto/template/ontology-function`），或参考 `销售示例/functions/sales_fn_get_summary.py`。

**输出规范**：`main()` 无参 → `return _ontology_fn_body(p)` → `p.function_result(...)`。**禁止** `output.print_json()`。

- [本体函数开发指南](../../../../../../资源/docs/onto/function-guide.md)
- [脚本运行常见错误处理 · §3 函数输出](../../../../../../资源/docs/onto/脚本运行常见错误处理.md)
