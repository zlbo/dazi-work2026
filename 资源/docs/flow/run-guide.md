# Flow 运行与测试

**文档 ID**: `flow/run-guide`

**命令前缀**（`dazi-work` 根）：`dazi flow …`  
**流程项目**：`--dir` 指向 `项目/<业务名>/流程/flows/<流程名>/`（**推荐绝对路径**；禁止在 `dazi-work` 根 `--dir .`）。

---

## 1. 流程项目：单节点测试（最常用）

```powershell
$flowDir = "D:\path\to\dazi-work\项目\<业务名>\流程\flows\MyFlow"

# 改 code.* 后必须先 push，再测（node-exec 执行的是平台代码，不是本地未提交文件）
dazi flow node push --node <node_uuid> --dir $flowDir
dazi flow run node-exec --node <node_uuid> --dir $flowDir

# 若节点配置了 output_variable_name，须 pull 核对（不能仅凭 node-exec 退出码）
dazi flow variable pull --name <output_variable_name> --dir $flowDir
```

**行为**

1. `node push` — 将本地 `code.*` 同步到平台 `flow_nodes.code_body`
2. `GET /flows/{id}/debug-run` — 确保 `ads_flows.debug_run_id` 已绑定调试 Run
3. `POST /flows/{id}/nodes/{nodeId}/run` — 在平台执行**已 push** 的节点代码
4. 成功时 CLI 会尝试同步该节点 `output_variable_name` 到 **`变量/<名>.json`**
5. 失败时写入 **`_run/<节点名>.last-error.md`**

**成功判据（代码节点）**：`node push` 成功 → `node-exec` JSON `success: true` →（有 `output_variable_name` 时）`variable pull` 后变量为 ready 且预览合理。

扩展：设计器/运行面板 **搭子执行** 前请确认已 `node push`；右键 **节点/** 或 **code.\*** → **测试运行节点**（同样依赖平台已 push 代码）。

---

## 2. 流程项目：整流程运行

```powershell
dazi flow run flow-exec --dir . --type debug
# preview：清空调试变量后全新运行
dazi flow run flow-exec --dir . --type preview
```

成功后 **`flow variable sync`** 同步全部变量到 `变量/` 目录。

扩展：右键 **flow.json** / 流程目录 → **运行整流程**。

---

## 3. 查看运行期变量

变量存储在 **`flow_runs` + `flow_run_variables`**，通过 **`flows.debug_run_id`** 关联。  
**变量模型、代码节点读写方式**见 [流程变量系统指南](./variables-guide.md)。

```powershell
# 拉取单个变量（schema + 前 10 行）→ 变量/<name>.json
dazi flow variable pull --name sales_df --dir .

# 同步全部调试 Run 变量
dazi flow variable sync --dir .
```

设计器：节点 **`output_variable_name`** 旁 **📊** 按钮。

扩展：右键 **`变量/`** → 同步；右键 **`变量/*.json`** → 刷新。

---

## 4. 平台级 Run API（脚本 / 自动化）

```powershell
# 启动 Run
dazi flow run start <flow-id> --input '{}'

# 列表
dazi flow run list <flow-id> --limit 10

# 调试信息（最近 Run）
dazi flow run debug <flow-id>

# 变量列表（需 --flow）
dazi flow run variables-list <runId> --flow <flow-id>
```

流程项目日常开发优先用 **§1–§3** 的 `node-exec` / `flow-exec` / `variable pull`。

---

## 5. 失败分析

```powershell
# 拉取 failure-bundle 落盘
dazi flow run failure --run <runId> --dir .
```

流程项目测试失败时，优先看 **`_run/*.last-error.md`**（含错误分类：缺上游变量、配置缺失、代码错误等）。

---

## 6. 相关文档

- [流程变量系统指南](./variables-guide.md) — 变量模型与代码示例
- [数据流程项目开发指南](./flow-project-guide.md) — debug_run_id、开发循环
- [节点代码编写指南](./node-code-guide.md) — 单节点脚本约定
