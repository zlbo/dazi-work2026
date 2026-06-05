# 流程本地文件规范与示例

**文档 ID**: `flow/local-files-spec`  
**适用**: `项目/<业务名>/流程/flows/<流程名>/` 目录、AI Agent、流程设计器  
**关联**: [AI 工作手册](./ai-workflow-playbook.md)、[数据流程项目开发指南](./flow-project-guide.md)

---

## 1. 三个文件的职责

| 文件 | 谁维护 | 存什么 | 禁止 |
|------|--------|--------|------|
| **`flow.json`** | 你 / 设计器 / `node new` + 编辑 | 画布：节点 `data`（配置）、`edges`、坐标；**不含**代码正文 | 手搓 `node_uuid`；嵌入大段 SQL/Python |
| **`flow.meta.json`** | **仅** `pull` / `node new` / `repair-meta` | `flowId`、uuid→`节点/` 映射、`codeHash`、画布指纹 | 手改后不同步 |
| **`节点/<名>/node.info.json`** | CLI 自动生成（只读） | uuid、类型、label、配置快照 | 当真理源编辑 |

**代码正文**只在 `节点/<名>/code.py` 或 `code.sql`。

设计器 **「打开代码」** 读取 `flow.meta.json` 的 `dir` + `codeFile`，**不会**扫描 `节点/` 猜文件。  
→ meta 缺条目 = 图上有节点但打不开代码（见 §6）。

---

## 2. 标准目录树

```text
项目/<业务名>/流程/flows/<流程名>/
├── flow.json                 # 画布真理源（轻量，无 pythonCode/sql 正文）
├── flow.meta.json            # 工程索引（CLI 维护）
├── 快速启动_<流程名>.md      # pull 后生成（含绝对路径命令、一致性检查）
├── 节点/
│   └── Excel成本报表解析/
│       ├── code.py           # 代码真理源
│       └── node.info.json    # 只读派生
├── 变量/                     # 调试 Run 派生（只读）
└── _run/                     # 测试/运行错误（*.last-error.md）
```

---

## 3. 标准示例（start → excel-python → end）

### 3.1 `flow.json`（片段）

```json
{
  "nodes": [
    {
      "id": "start-node",
      "type": "custom",
      "position": { "x": 50, "y": 250 },
      "data": { "label": "开始", "type": "start" },
      "deletable": false,
      "node_uuid": "aa1ba01e-bc96-41ab-b9e4-4b42e77aaae5"
    },
    {
      "id": "n-excel01",
      "type": "custom",
      "position": { "x": 310, "y": 250 },
      "data": {
        "label": "Excel成本报表解析",
        "type": "excel-python",
        "managed_file_id": "51853ede-9e6b-4a3a-aa7a-060cbead0862",
        "output_variable_name": "成本统计报表"
      },
      "node_uuid": "d96222ce-aaa9-4050-b782-830c2f2de9eb"
    },
    {
      "id": "end-node",
      "type": "custom",
      "position": { "x": 850, "y": 250 },
      "data": { "label": "结束", "type": "end" },
      "deletable": false,
      "node_uuid": "47c53b38-6005-4d7f-9f89-7ea56dab6b38"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "source": "start-node",
      "sourceHandle": "r",
      "target": "n-excel01",
      "targetHandle": "l"
    },
    {
      "id": "e2",
      "source": "n-excel01",
      "sourceHandle": "r",
      "target": "end-node",
      "targetHandle": "l"
    }
  ]
}
```

要点：`type` 恒为 `custom`，业务类型在 `data.type`；`node_uuid` 必须来自平台（`pull` / `node new`）。

### 3.2 `flow.meta.json`（片段）

```json
{
  "flowId": "119",
  "flowName": "vs-test-03",
  "nodes": {
    "aa1ba01e-bc96-41ab-b9e4-4b42e77aaae5": {
      "nodeId": "start-node",
      "nodeType": "start"
    },
    "d96222ce-aaa9-4050-b782-830c2f2de9eb": {
      "nodeId": "n-excel01",
      "nodeType": "excel-python",
      "dir": "节点/Excel成本报表解析",
      "codeFile": "code.py",
      "codeLanguage": "python",
      "codeHash": "abc123..."
    },
    "47c53b38-6005-4d7f-9f89-7ea56dab6b38": {
      "nodeId": "end-node",
      "nodeType": "end"
    }
  },
  "lastPulledAt": "2026-06-03T08:37:53.126Z",
  "graphFingerprint": "sha1:..."
}
```

**每个代码节点**在 `nodes` 中必须有 `dir` + `codeFile`。

### 3.3 `node.info.json`（片段，只读）

```json
{
  "_readonly": "此文件由 dazi-flow 生成，仅供查看；编辑代码请改 code.py，配置改 flow.json",
  "node_uuid": "d96222ce-aaa9-4050-b782-830c2f2de9eb",
  "nodeId": "n-excel01",
  "nodeType": "excel-python",
  "label": "Excel成本报表解析",
  "codeFile": "code.py",
  "codeLanguage": "python",
  "data": {
    "label": "Excel成本报表解析",
    "type": "excel-python",
    "managed_file_id": "51853ede-9e6b-4a3a-aa7a-060cbead0862",
    "output_variable_name": "成本统计报表"
  }
}
```

---

## 4. 错误示例（勿模仿）

| 现象 | 原因 |
|------|------|
| `flow.json` 有 3 节点，`meta.nodes` 只有 2 条 | 手改画布未 `node new` / 未 `repair-meta` |
| 有 `节点/xxx/code.py` 但设计器打不开代码 | meta 无该 uuid 的 `dir` |
| 多次 `project push` 平台仍无 `managed_file_id` | 用了 `push` 但未加 **`--canvas`** |
| `node push` 无效果 | meta 无索引 → 命令 skipped |

---

## 5. 变更类型 → 命令

| 改了什么 | 命令 |
|----------|------|
| `managed_file_id`、`output_variable_name`、连线、增删节点 | `dazi flow project push --dir . --canvas` |
| `code.py` / `code.sql` | `dazi flow node push --node <uuid> --dir .` |
| **新增代码节点** | `dazi flow node new --type <type> --dir . --label "<名>"` → 改 `flow.json` 配置 → `push --canvas` → 写 code → `node push` |
| 目录不一致 | `dazi flow project repair-meta --dir .` → `doctor` |

`project push`（**无** `--canvas`）**不会**上传 `flow.json` 配置变更。

---

## 6. 设计器「找不到代码」

1. 执行 `dazi flow project doctor --dir .`
2. 若 meta 缺条目：`dazi flow project repair-meta --dir .`
3. 再在设计器点击「打开代码」
4. **勿**在本地画布多于平台时盲目 `pull`（会覆盖 `flow.json`）

---

## 7. 内置示例目录

扩展内置：`examples/flow/minimal-excel-python/`（`dazi docs sync` 后位于 `资源/examples/flow/`）。

---

## 8. 相关文档

- [流程 AI 工作手册](./ai-workflow-playbook.md)
- [一致性检查表](../guides/flow-consistency-checklist.md)
- [节点代码编写指南](./node-code-guide.md)
