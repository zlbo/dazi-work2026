"""本体函数模板 — 复制到 项目/<业务名>/本体/ontos/<实现名>/functions/ 后修改

function_id 示例：domain.fn.my_analysis
发布：dazi onto script publish .../functions/my_fn_xxx.py --space <space-id> --register-function-id domain.fn.my_analysis

★ 本体函数输出规范（勿改 main 结构）：
  - main() 无参；通过 ctx.space_id / ctx.params 读入参
  - 业务逻辑写在 _ontology_fn_body(p)
  - 返回 p.function_result(...) 或 return _ontology_fn_body(p)
  - 禁止 output.print_json()（OutputModule 无此方法）
参考：资源/examples/onto/销售示例/functions/sales_fn_get_summary.py
"""

TEST_ARGUMENTS = {
    "v": 1,
    "arguments": {"start_date": "2025-01-01", "end_date": "2026-06-30"},
    "object_type_code": "MyObjectTypeCode",
}


def _ontology_fn_body(p):
    params = dict(p.get_params() or {})
    # start_date = params.get("start_date", "")
    # end_date = params.get("end_date", "")

    # rows = p.sql.query("SELECT ...")
    # row = rows[0] if rows else {}

    data = [{"example_metric": 0}]

    return p.function_result(
        columns=["example_metric"],
        data=data,
        row_count=len(data),
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
