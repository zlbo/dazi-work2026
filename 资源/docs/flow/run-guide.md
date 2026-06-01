# Flow 运行与测试

**文档 ID**: `flow/run-guide`

**命令前缀**（`dazi-work` 根）：`.\scripts\dazi.ps1 flow …`  
**流程项目**：在 `项目/flow_*/流程/<名>/` 下执行，或使用 `--dir <流程目录>`。

---

## 1. 流程项目：单节点测试（最常用）

```powershell
cd "项目\flow_xxx\流程\MyFlow"

# 按 node_uuid 测试（CLI 内部翻译为语义 nodeId）
.\scripts\dazi.ps1 flow run node-exec --node <node_uuid> --dir .
```

**行为**

1. `GET /flows/{id}/debug-run` — 确保 `ads_flows.debug_run_id` 已绑定调试 Run  
2. `POST /flows/{id}/nodes/{nodeId}/run` — 执行单节点  
3. 成功时同步该节点 `output_variable_name` 到 **`变量/<名>.json`**  
4. 失败时写入 **`_run/<节点名>.last-error.md`**（扩展会自动打开）

扩展：右键 **节点/** 或 **code.*** → **测试运行节点**。

---

## 2. 流程项目：整流程运行

```powershell
.\scripts\dazi.ps1 flow run flow-exec --dir . --type debug
# preview：清空调试变量后全新运行
.\scripts\dazi.ps1 flow run flow-exec --dir . --type preview
```

成功后 **`flow variable sync`** 同步全部变量到 `变量/` 目录。

扩展：右键 **flow.json** / 流程目录 → **运行整流程**。

---

## 3. 查看运行期变量

变量存储在 **`flow_runs` + `flow_run_variables`**，通过 **`flows.debug_run_id`** 关联。  
**变量模型、代码节点读写方式**见 [流程变量系统指南](./variables-guide.md)。

```powershell
# 拉取单个变量（schema + 前 10 行）→ 变量/<name>.json
.\scripts\dazi.ps1 flow variable pull --name sales_df --dir .

# 同步全部调试 Run 变量
.\scripts\dazi.ps1 flow variable sync --dir .
```

设计器：节点 **`output_variable_name`** 旁 **📊** 按钮。

扩展：右键 **`变量/`** → 同步；右键 **`变量/*.json`** → 刷新。

---

## 4. 平台级 Run API（脚本 / 自动化）

```powershell
# 启动 Run
.\scripts\dazi.ps1 flow run start <flow-id> --input '{}'

# 列表
.\scripts\dazi.ps1 flow run list <flow-id> --limit 10

# 调试信息（最近 Run）
.\scripts\dazi.ps1 flow run debug <flow-id>

# 变量列表（需 --flow）
.\scripts\dazi.ps1 flow run variables-list <runId> --flow <flow-id>
```

流程项目日常开发优先用 **§1–§3** 的 `node-exec` / `flow-exec` / `variable pull`。

---

## 5. 失败分析

```powershell
# 拉取 failure-bundle 落盘
.\scripts\dazi.ps1 flow run failure --run <runId> --dir .
```

流程项目测试失败时，优先看 **`_run/*.last-error.md`**（含错误分类：缺上游变量、配置缺失、代码错误等）。

---

## 6. 相关文档

- [流程变量系统指南](./variables-guide.md) — 变量模型与代码示例  
- [数据流程项目开发指南](./flow-project-guide.md) — debug_run_id、开发循环  
- [节点代码编写指南](./node-code-guide.md) — 单节点脚本约定  
