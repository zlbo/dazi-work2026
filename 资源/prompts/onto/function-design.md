# 提示词：本体函数设计

**提示词 ID**: `onto/function-design`  
**场景**: 设计新的本体函数

---

你是一名搭子平台本体工程师。请根据以下需求设计一个本体函数（ontology function）。

## 函数需求

{{function_description}}

## 要求

1. 函数名使用 snake_case，以动词开头（如 `calc_balance`、`get_user_info`）
2. `main(params: dict) -> dict` 为入口函数
3. 参数通过 `params` 字典传入，输出通过 return 返回
4. 包含完整的 docstring（中文），说明：函数目的、参数说明、返回值说明
5. 包含基本的错误处理（try/except）
6. 引用的搭子数据空间对象通过 `s` 上下文访问

## 输出格式

```python
def main(params: dict, s=None) -> dict:
    """
    [函数说明]

    Args:
        params: 包含 xxx（说明）

    Returns:
        包含 xxx（说明）
    """
    # 实现
```

发布与运行（v3，工作区根目录；**勿用** `dazi-onto`）：

```powershell
dazi onto script publish 项目/onto_<名>/脚本/functions/<file>.py --space <space-id> --register-function-id <id>
dazi onto function run <id> --space <space-id>
```

详见提示词 `onto/script-publish-run`（侧栏 帮助 → 提示词）。
