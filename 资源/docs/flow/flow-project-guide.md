# 数据流程项目开发指南

**文档 ID**: `flow/flow-project-guide`  
**适用**: `dazi-vscode` v3.1+、`dazi-work` 工作区、`项目/flow_*` 流程项目

---

## 1. 定位与核心约定

| 维度       | 说明                                                            |
| ---------- | --------------------------------------------------------------- | ------------------- |
| CLI 入口   | `dazi flow …` → `dazi-flow`（Trae / VS Code / Cursor 交付环境） |
| 工作区     | `dazi-work` + `项目/flow_<名>/`                                 |
| 本地流程树 | `流程/<名>/flow.json` + `节点/<名>/code.*`                      |
| 画布真理源 | **`flow.json`**（= 平台 `config_json` 镜像，代码已剥离）        |
| 代码真理源 | \*\*`节点/<名>/code.sql                                         | py`** + `node push` |
| 主交互     | **资源管理器右键** + MVP 流程设计器                             |
| AI         | **Cursor 侧读文件** + `dazi-flow mcp`                           |

API 根路径：**`{serverUrl}/api/data-pipelines/v1`**（搭子数据流程引擎）。

---

## 2. 工作区目录

```text
dazi-work/
├── scripts/
│   └── dazi.ps1              ← 终端/Trae 中运行搭子 CLI 的入口
└── 项目/
    └── flow_数据集成01/
        ├── README.md                  项目元信息
        ├── 快速启动.md                项目级入门
        ├── 规划/
        └── 流程/
            └── 客户数据清洗/          ← 一个流程 = 一个目录
                ├── 快速启动_<流程名>.md   pull 后生成（flowId、常用命令、AI 单文件入口）
                ├── flow.json          ★ 画布（节点配置 + 边，不含代码正文）
                ├── flow.meta.json     flowId、uuid 映射、代码指纹
                ├── 节点/
                │   └── SQL查询/
                │       ├── code.sql   ★ 代码唯一真理源
                │       └── node.info.json
                ├── 变量/              调试 Run 变量只读派生（schema + 预览）
                │   └── sales_df.json
                └── _run/              测试/运行产物（*.last-error.md 等）
```

**关键约定**

- 节点 `type` 在画布上恒为 `"custom"`，**业务类型在 `data.type`**（如 `sql-query`、`python-script`）。
- 流程项目**不绑定**数据空间；`connectionId` 只是节点配置字段。
- `flow.json` 由设计器/CLI 管理；AI 若手改拓扑，**必须**遵守 [§6.2 画布节点与连线规范](#62-画布节点与连线规范ai-创建--编辑-flowjson-必读)（节点 200px、锚点 `l/t/r/b/true/false`、条件分支）。
- 改代码请编辑 `code.*`，不要把代码正文写回 `flow.json`。

---

## 3. CLI 怎么跑：`dazi.ps1` 与 `dazi-flow`

### 3.1 调用链（Trae / VS Code / Cursor 交付环境）

```text
dazi flow <子命令...>
        │
        ▼  node bundled/clis/dazi.js
        │  （设置 DAZI_BUNDLED_DIR，cwd = dazi-work 根）
        ▼
   forward → node bundled/clis/dazi-flow.js <子命令...>
```

- **没有**全局 `dazi-flow` 命令；与本体一致，统一走 **`dazi`**。
- 扩展侧栏/右键菜单与上述 CLI **同源**（同一套 bundled `dazi-flow.js`）。
- 首次使用：在 **`dazi-work` 根**执行 `.\scripts\doctor-cli.ps1` → `dazi auth login`。

### 3.2 命令写法对照

| 文档/扩展内部               | 在 `dazi-work` 根目录终端   |
| --------------------------- | --------------------------- |
| `dazi-flow project pull …`  | `dazi flow project pull …`  |
| `dazi-flow node push …`     | `dazi flow node push …`     |
| `dazi-flow run node-exec …` | `dazi flow run node-exec …` |
| `dazi-flow variable pull …` | `dazi flow variable pull …` |

**工作目录技巧**：多数命令支持 `--dir <流程目录>`。也可 **`cd` 到流程目录**后省略 `--dir`（cwd 即 `流程/<名>/`）。

```powershell
# 在 dazi-work 根
cd D:\path\to\dazi-work
dazi auth whoami

# 拉取平台流程到本地（首次）
dazi flow project pull --flow 98 --dir "项目\flow_流程项目01\流程\MyFlow0529"

# 进入流程目录后，后续命令可省略 --dir
cd "项目\flow_流程项目01\流程\MyFlow0529"
dazi flow project status
dazi flow node push --node <node_uuid>
```

**常用子命令速查**（拉取 / 提交 / 测试 / 变量等）见 [Flow 文档索引 · 流程项目常用命令](./flows-guide.md#流程项目flow_-常用命令)。Plan、数据源等专题见 [执行计划](./plan-guide.md)、[数据源管理](./source-guide.md)。

---

## 4. 推荐开发循环

```text
1. 新建或拉取
   扩展：项目/flow_* → 新建流程 / 拉取平台流程
   CLI： flow project pull --flow <id> --dir <流程目录>

2. 改代码
   打开 节点/<名>/code.sql 或 code.py
   （详见 [节点代码编写指南](./node-code-guide.md)）

3. 改画布配置（连线、connectionId、output_variable_name…）
   右键 flow.json → 打开流程设计器 → 保存 flow.json
   （AI 手改拓扑须遵守 [§6.2 画布节点与连线规范](#62-画布节点与连线规范ai-创建--编辑-flowjson-必读)）

4. 单节点测试
   右键 节点/ 或 code.* → 测试运行节点
   CLI： flow run node-exec --node <uuid> --dir .

5. 查看变量（表变量 schema + 前 10 行）
   设计器属性面板 output_variable_name 旁 📊
   或： flow variable pull --name <变量名> --dir .

6. 提交到平台
   右键 → 提交流程（智能：代码脏节点 + 画布变更）
   CLI： flow project push --dir . --canvas

7. 失败时
   阅读 _run/*.last-error.md（整流程另见 flow.last-run.md）
   - **对话模式**：用户确认后再交 AI 修复（扩展不自动改库）
   - **Agent 模式**：AI 自行改错循环，见 `快速启动_<流程名>.md` §AI 自主运行与改错闭环 或提示词 `flow/run-fix-loop`
```

---

## 5. 同步策略（pull / push）

| 操作          | API / 行为                                                                                  |
| ------------- | ------------------------------------------------------------------------------------------- |
| **pull**      | `GET /flows/{id}/snapshot` 一次拿全 → 拆成 `flow.json` + `节点/*/code.*` + `flow.meta.json` |
| **push 代码** | 仅脏节点：`PATCH /flows/{id}/flow-nodes/{uuid}`（乐观锁 `expected_version`）                |
| **push 画布** | `PUT /flows/{id}` body `{ data: 完整 document }`（`--canvas`）                              |
| **status**    | 本地 `code.*` 的 sha1 与 meta 中 `codeHash` 比对                                            |

冲突时：先 **拉取** 或 **`node push --force`**（慎用覆盖）。

---

## 6. 资源管理器菜单（主交互）

| 右键对象                    | 常用命令                                               |
| --------------------------- | ------------------------------------------------------ |
| `flow.json` / 流程目录      | 打开设计器、拉取、**提交**、状态、运行整流程           |
| `节点/<名>/`                | 打开代码、拉取/提交节点、**测试运行**                  |
| `节点/<名>/code.*`          | 提交、测试、拉取                                       |
| `变量/`                     | 同步变量到本地                                         |
| `变量/<名>.json`            | 刷新变量、查看变量信息                                 |
| `项目/flow_*`               | 新建流程、拉取平台流程                                 |
| **数据资源 → 文件上传管理** | 浏览平台登记文件、**拉取到本地资源**、复制 AI 附加说明 |

设计器工具栏：**保存 / 校验 / 运行 / 提交 / 拉取**。

---

## 6.1 文件上传管理（Excel 等流程数据源）

侧栏 **数据资源 → 文件上传管理** 展示平台 `managed_files` 目录树（与 Web 端「文件上传管理」同源）。

**拉取到本地** 后写入工作区：

```text
dazi-work/资源/files/<显示名>_<fileId前8位>/
├── 文件信息.json      登记元数据 + managed_file_id
├── 原文件.xlsx        二进制原文件
├── 原生解析.md        Excel 原生解析（无缓存时会触发 parse）
├── 表结构.json        AI 表结构（需平台已生成）
└── 报表布局.json      复杂报表 RLIR（需平台「报表布局」页签已生成）
```

- **excel-python 节点**画布请使用 **`managed_file_id`**（即 `文件信息.json` 中的 `file_id`），**不是** data upload 的 `id`。
- **Excel 文件（`.xlsx`/`.xls`）优先 `excel-python`**，**不要用 `file-source`**（file-source 仅透传原始文件、不解析 Excel）。
- 拉取后可用 **「复制 AI 附加说明」** 或在 Cursor 聊天中 `@` 引用上述文件，辅助编写流程与解析逻辑。

CLI 等价命令：

```powershell
dazi flow managed-files list
dazi flow managed-files dirs --path excel
dazi flow managed-files pull --file-id <uuid> --relative-dir excel
```

---

## 6.2 画布节点与连线规范（AI 创建 / 编辑 flow.json 必读）

Web 端 `@xyflow/react` 与 VS Code MVP 设计器共用同一套 **`flow.json` 拓扑约定**。AI 新建或修改流程时，**必须**遵守本节，否则画布错位、连线无法渲染、条件分支执行错误。

> 代码正文写在 `节点/<名>/code.*`，**不要**塞进 `flow.json`；本节只规范 **节点位置、锚点、边**。

### 6.2.1 节点尺寸与布局

| 项             | 规范值         | 说明                                               |
| -------------- | -------------- | -------------------------------------------------- |
| 最小宽度       | **200px**      | 对齐 Web `CustomNode` 的 `min-w-[200px]`           |
| 典型高度       | **约 88px**    | header（约 36px）+ body（约 52px）；内容多时会增高 |
| 边框 / 圆角    | 2px / 8px      | 与系统设计器一致                                   |
| 锚点直径       | **12px**       | 对应 Tailwind `w-3 h-3`                            |
| 横向间距       | **≥ 260px**    | 相邻节点 `position.x` 差值，避免 200px 宽节点重叠  |
| 纵向间距       | **≥ 140px**    | 相邻节点 `position.y` 差值                         |
| 首节点参考坐标 | `x: 80, y: 80` | 从左上网格起点排布                                 |

**结构**：每个节点为 **header（标题）+ body（状态摘要）** 双层；`position` 为节点**左上角**在画布上的像素坐标。

**推荐排布**（AI 新建流程时）：

```text
[开始] --260px--> [SQL] --260px--> [条件] --260px--> [Python-True]
                                      |
                                   140px ↓
                                  [Python-False] --260px--> [结束]
```

### 6.2.2 锚点（连线端点）约定

锚点 ID 写入边的 **`sourceHandle`**（输出端）与 **`targetHandle`**（输入端）。**必须显式填写**，不要省略后依赖推断。

| 锚点 ID | 节点上的位置      | 角色               | 用于                               |
| ------- | ----------------- | ------------------ | ---------------------------------- |
| `l`     | 左侧中点          | **输入**（target） | 常规入边（最常见）                 |
| `t`     | 顶部中点          | **输入**（target） | 自下方节点连入                     |
| `r`     | 右侧中点          | **输出**（source） | 常规出边（最常见）                 |
| `b`     | 底部中点          | **输出**（source） | 连到下方节点                       |
| `true`  | 右侧 **30%** 高度 | **输出**（source） | **仅** `condition` 节点 True 分支  |
| `false` | 右侧 **70%** 高度 | **输出**（source） | **仅** `condition` 节点 False 分支 |

**合法组合**

- `sourceHandle` 只能是：`r` | `b` | `true` | `false`
- `targetHandle` 只能是：`l` | `t`
- **禁止**把 `l`/`t` 写在 `sourceHandle`，或把 `r`/`b`/`true`/`false` 写在 `targetHandle`
- **禁止**自连接（`source === target`）
- 同一对 `(source, target, sourceHandle, targetHandle)` 只能有一条边

**常用拓扑与锚点配对**

| 场景                | sourceHandle | targetHandle |
| ------------------- | ------------ | ------------ |
| 左 → 右（主流水线） | `r`          | `l`          |
| 上 → 下             | `b`          | `t`          |
| 右 → 下             | `r`          | `t`          |
| 下 → 左             | `b`          | `l`          |
| 条件 True 分支      | `true`       | `l` 或 `t`   |
| 条件 False 分支     | `false`      | `l` 或 `t`   |

**边 `id` 命名**（与 React Flow 一致，便于 diff）：

```text
xy-edge__{source节点id}{sourceHandle}-{target节点id}{targetHandle}
```

示例：`xy-edge__start-noder-sql-1l`

### 6.2.3 各类节点锚点一览

| `data.type`  | 输入 `l`/`t` | 输出 `r`/`b` | 输出 `true`/`false` | 备注                               |
| ------------ | :----------: | :----------: | :-----------------: | ---------------------------------- |
| `start`      |      —       |   `r`, `b`   |          —          | 无入边；语义 id 常为 `start-node`  |
| `end`        |   `l`, `t`   |      —       |          —          | 无出边；语义 id 常为 `end-node`    |
| `condition`  |   `l`, `t`   |      —       | **`true`, `false`** | **不用** `r`/`b`                   |
| 其他业务节点 |   `l`, `t`   |   `r`, `b`   |          —          | 如 `sql-query`、`python-script` 等 |

画布上节点 **`type` 恒为 `"custom"`**，业务类型在 **`data.type`**。

### 6.2.4 条件节点（`condition`）

**画布**

- `data.type`: `"condition"`
- `data.label`: 显示名（如「金额判断」）
- 条件表达式写在 **`节点/<名>/code.py`**（平台键 `pythonCode`），**不要**写进 `flow.json`
- 必须有 **至少一条入边**（`targetHandle` 为 `l` 或 `t`）
- 两条出边应分别使用 **`sourceHandle: "true"`** 与 **`sourceHandle: "false"`**（各连不同下游）
- 可视化：True 分支 **绿色**、False 分支 **红色**（Web / VS Code 设计器均如此）

**运行**

- 对入边上游表注入 **`df`**（不注入 `get_variable`）
- `code.py` 为 Python 表达式，求值结果为布尔值，决定走 True 还是 False 边
- 单节点测试前须先运行入边上游；详见 [流程变量系统指南 §6.7](./variables-guide.md#67-condition条件分支)

**条件节点示例 `code.py`**

```python
# 表达式或单行，eval 后决定分支
df.shape[0] > 0 and df["amount"].sum() > 10000
```

**反例（AI 勿犯）**

- 从条件节点用 `sourceHandle: "r"` 连下游 → **错误**，应用 `true` 或 `false`
- 只连 True 不连 False → 允许保存，但 False 分支下游永远不会被调度
- 两条出边都用 `true` → **错误**，分支无法区分

### 6.2.5 `flow.json` 边（edges）字段

每条边 **最少** 包含：

```json
{
  "id": "xy-edge__start-noder-sql-1l",
  "source": "start-node",
  "target": "sql-1",
  "sourceHandle": "r",
  "targetHandle": "l"
}
```

- **`source` / `target`**：节点的语义 **`id`** 字段（不是 `node_uuid`）
- **`sourceHandle` / `targetHandle`**：见 §6.2.2
- 条件分支边示例：

```json
{
  "id": "xy-edge__cond-1true-py-okl",
  "source": "cond-1",
  "target": "py-ok",
  "sourceHandle": "true",
  "targetHandle": "l"
}
```

### 6.2.6 完整拓扑示例（AI 参考）

```json
{
  "nodes": [
    {
      "id": "start-node",
      "type": "custom",
      "node_uuid": "00000000-0000-0000-0000-000000000001",
      "position": { "x": 80, "y": 120 },
      "data": { "type": "start", "label": "开始" }
    },
    {
      "id": "sql-1",
      "type": "custom",
      "node_uuid": "00000000-0000-0000-0000-000000000002",
      "position": { "x": 340, "y": 120 },
      "data": {
        "type": "sql-query",
        "label": "汇总销售",
        "output_variable_name": "sales_agg"
      }
    },
    {
      "id": "cond-1",
      "type": "custom",
      "node_uuid": "00000000-0000-0000-0000-000000000003",
      "position": { "x": 600, "y": 120 },
      "data": { "type": "condition", "label": "金额判断" }
    },
    {
      "id": "py-ok",
      "type": "custom",
      "node_uuid": "00000000-0000-0000-0000-000000000004",
      "position": { "x": 860, "y": 80 },
      "data": {
        "type": "python-script",
        "label": "大额处理",
        "output_variable_name": "big_deal"
      }
    },
    {
      "id": "py-skip",
      "type": "custom",
      "node_uuid": "00000000-0000-0000-0000-000000000005",
      "position": { "x": 860, "y": 220 },
      "data": {
        "type": "python-script",
        "label": "小额跳过",
        "output_variable_name": "small_deal"
      }
    },
    {
      "id": "end-node",
      "type": "custom",
      "node_uuid": "00000000-0000-0000-0000-000000000006",
      "position": { "x": 1120, "y": 120 },
      "data": { "type": "end", "label": "结束" }
    }
  ],
  "edges": [
    {
      "id": "xy-edge__start-noder-sql-1l",
      "source": "start-node",
      "target": "sql-1",
      "sourceHandle": "r",
      "targetHandle": "l"
    },
    {
      "id": "xy-edge__sql-1r-cond-1l",
      "source": "sql-1",
      "target": "cond-1",
      "sourceHandle": "r",
      "targetHandle": "l"
    },
    {
      "id": "xy-edge__cond-1true-py-okl",
      "source": "cond-1",
      "target": "py-ok",
      "sourceHandle": "true",
      "targetHandle": "l"
    },
    {
      "id": "xy-edge__cond-1false-py-skipl",
      "source": "cond-1",
      "target": "py-skip",
      "sourceHandle": "false",
      "targetHandle": "l"
    },
    {
      "id": "xy-edge__py-okr-end-nodel",
      "source": "py-ok",
      "target": "end-node",
      "sourceHandle": "r",
      "targetHandle": "l"
    },
    {
      "id": "xy-edge__py-skipr-end-nodel",
      "source": "py-skip",
      "target": "end-node",
      "sourceHandle": "r",
      "targetHandle": "l"
    }
  ]
}
```

> `node_uuid` 由平台分配；AI **新建节点**应走 `flow node new` 或设计器「组件」面板，**不要**伪造 uuid。仅调整连线/坐标时可只改 `edges` 与 `position`。

### 6.2.7 AI 自检清单

创建或修改 `flow.json` 后，逐项核对：

1. 存在 **`start`** 与 **`end`** 节点，且可达（从 start 沿边能到 end）
2. 每条边的 **`sourceHandle` / `targetHandle`** 已填写且组合合法（§6.2.2）
3. **`condition`** 节点的出边仅使用 **`true` / `false`**，不用 `r` / `b`
4. 相邻节点 **`position` 间距** ≥ 260（横）/ 140（纵）
5. 节点 **`type`** 为 `"custom"`，业务类型在 **`data.type`**
6. 代码类节点无内嵌 `pythonCode` / `sql`（应在 `节点/*/code.*`）
7. 变量名在 `output_variable_name` 中**全局不重名**（见 [variables-guide](./variables-guide.md)）
8. 改动画布后执行 **`flow project push --dir . --canvas`**

### 6.2.8 设计器交互（人工）

VS Code **打开流程设计器**（右键 `flow.json`）时：

- 从**输出**锚点拖到**输入**锚点：新建连线（自动写入 handle）
- **点击连线**选中；**Delete** 或中点 **×** 删除
- 条件分支显示 **绿色 True / 红色 False** 标签
- 开始 / 结束 / 条件节点左侧有色条；拖拽连线时有虚线预览

保存或 **`project push --canvas`** 后，与 Web 设计器互通。

---

## 7. 变量从哪里来（debug_run_id）

运行期变量不在 `flow.json` 里，而在 **`ads_flows.debug_run_id` → `flow_runs.id` → `flow_run_variables`**。

1. 单节点测试或整流程运行前，服务端会 **`GET /flows/{id}/debug-run`**（无则创建并写回 `debug_run_id`）。
2. 节点配置了 **`output_variable_name`** 且执行成功后，输出写入该调试 Run（表 → Parquet，标量 → 库字段）。
3. 查看变量时 CLI 同样先确保 debug-run，再 `GET /flows/{id}/variables`，拉 schema + preview 到 **`变量/<name>.json`**。

**代码节点如何用变量**（`get_variable`、SQL 表名、`result_df` 等）见 **[流程变量系统指南](./variables-guide.md)**。

变量尚未产出时，占位 JSON 会提示：**先运行产出该变量的上游节点**。

---

## 8. 相关文档

| 文档                                        | 内容                                                       |
| ------------------------------------------- | ---------------------------------------------------------- |
| [流程变量系统指南](./variables-guide.md)    | 变量模型、`output_variable_name`、各节点读写变量与代码示例 |
| [节点代码编写指南](./node-code-guide.md)    | `python-script`、`sql-query` 等单节点代码约定              |
| [Flow 运行与测试](./run-guide.md)           | `node-exec`、`flow-exec`、变量命令                         |
| [CLI 调用约定](../guides/cli-invocation.md) | `dazi.ps1`、Trae 扩展路径、doctor                          |
| [CLI 命令速查](../guides/cli-reference.md)  | 完整命令表                                                 |
| [Flow 管理入门](./flows-guide.md)           | 文档索引、**AI 创建流程速查**、平台级 Flow 操作            |

---

## 9. 常见问题

| 现象                 | 处理                                                                                |
| -------------------- | ----------------------------------------------------------------------------------- |
| `dazi-flow` 找不到   | 使用 `dazi flow …`，运行 `doctor-cli.ps1`                                           |
| 提交 HTTP 405        | 画布提交须 `PUT /flows/{id}`，用 `project push --canvas`，勿对 `apply-patch` 发 PUT |
| 变量查看失败         | 先 **测试节点** 或 **运行流程**；确认 `flow.meta.json` 有 `flowId`                  |
| 节点测试报缺上游变量 | 先运行上游节点，或 **运行整流程（debug）** 再测当前节点                             |
| 代码改了平台没更新   | `node push` 或 `project push`；看 `project status` 是否脏                           |
