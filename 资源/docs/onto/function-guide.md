# 本体函数开发指南

**文档 ID**: `onto/function-guide`

## 函数生命周期

```
在 项目/onto_<项目名>/脚本/ 编写 .py → publish-preview（预检）→ publish（入库）→ update-code（更新）
```

## 新建函数

```bash
# 发布新函数（路径指向本体项目 脚本/ 目录）
dazi onto function publish 项目/onto_<项目名>/脚本/my_func.py \
  --space <space-id> \
  --function-id my_function \
  --display-name "我的函数" \
  --entry main
```

或使用 `script publish`（等价，见 [本体脚本编写指南](./本体脚本编写指南.md)）：

```bash
dazi onto script publish 项目/onto_<项目名>/脚本/my_func.py \
  --space <space-id> \
  --register-function-id my_function
```

`<space-id>` 取自 **`项目/onto_<项目名>/README.md`**。

## 更新已有函数代码

```bash
# 用工作副本快速更新（不做完整 publish 流程）
dazi onto function update-code <function-id> \
  --space <space-id> \
  --stem my_func
```

`--stem` 为脚本文件名（不含扩展名），须与 `脚本/` 下文件一致。

## 运行函数

```bash
dazi onto function run <function-id> \
  --space <space-id> \
  --params '{"key": "value"}'
```

## 保存测试参数

```bash
dazi onto function save-test-arguments <function-id> \
  --space <space-id> \
  --params '{"test_param": 42}'
```

## 函数脚本结构

```python
def main(params: dict) -> dict:
    """
    函数入口，params 由平台传入。
    返回值会作为函数输出。
    """
    return {"result": params.get("value", 0) * 2}
```
