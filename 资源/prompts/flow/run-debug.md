# 提示词：Run 调试分析（项目态）

**提示词 ID**: `flow/run-debug`  
**场景**: 分析流程项目运行失败，并给出可执行修复步骤

---

以下是搭子 Flow 运行的调试信息，请分析失败原因并给出修复建议。  
默认上下文是 `项目/flow_*/流程/<流程名>/` 的流程目录。

## 调试输出

```
{{debug_output}}
```

> 若用户未粘贴输出：AI **应主动读取** `_run/*.last-error.md`、`_run/flow.last-run.md`（及 `变量/` 下 schema），必要时自行执行 `.\scripts\dazi.ps1 flow run ...` 复现；Agent 模式见 `flow/run-fix-loop`。

## 分析要求

1. 找出**失败节点**及其错误信息
2. 分析**根本原因**（数据问题/配置问题/代码问题）
3. 给出**具体修复步骤**（按“改哪里 + 跑什么命令 + 如何验证”）
4. 如果是脚本错误，提供修复后的代码
5. 若涉及画布/连线/节点配置，明确要求 `flow project push --canvas`

## 常见问题类型

| 症状 | 可能原因 |
|------|---------|
| `KeyError` | 字段名不一致，检查上游变量 schema（`变量/<name>.json`） |
| `TypeError` | 数据类型不符，检查字段类型 |
| `ConnectionError` | 数据源连接失败，检查数据源配置 |
| `PermissionError` | 缺少权限，检查登录状态与权限 |
| 节点超时 | 数据量过大或查询未优化 |
| 上游变量缺失 | 未先运行上游节点或整流程 |

## 命令约束（必须遵守）

- 命令前缀统一：`.\scripts\dazi.ps1 flow ...`（在 `dazi-work` 根）
- 在流程目录执行时，保留 `--dir .`，避免误跑到其他流程
- 禁止输出裸 `dazi-flow ...` 作为最终命令

## 重新运行

分析完成后，**必须给出可执行的修复与重跑命令**；若用户委托 Agent 模式，应进入改错循环（见 `flow/run-fix-loop`）。

```powershell
# 仅重测失败节点（优先）
.\scripts\dazi.ps1 flow run node-exec --node <node_uuid> --dir .

# 整流程回归（必要时）
.\scripts\dazi.ps1 flow run flow-exec --dir . --type debug

# 拉取变量确认修复效果
.\scripts\dazi.ps1 flow variable pull --name <output_variable_name> --dir .
```

## 回答格式要求

1. **失败点**：节点名 / node_uuid / 关键报错
2. **修复动作**：改 `flow.json` 还是改 `节点/<名>/code.*`
3. **执行命令**：按顺序给出可直接复制的命令
4. **提交动作**：
   - 只改代码：`.\scripts\dazi.ps1 flow node push --node <node_uuid> --dir .`
   - 改了拓扑或节点配置：`.\scripts\dazi.ps1 flow project push --dir . --canvas`
