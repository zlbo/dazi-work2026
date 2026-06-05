# 流程目录一致性检查表

**文档 ID**: `guides/flow-consistency-checklist`  
**适用**: 排查「push 无效 / 设计器打不开代码 / flow-exec 少节点」

---

## CLI 一键检查

```powershell
$flowDir = "D:\path\to\dazi-work\项目\<业务名>\流程\flows\<流程名>"
dazi flow project doctor --dir $flowDir
dazi flow project repair-meta --dir $flowDir   # 若 doctor 报错
```

---

## 手工检查表

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | `flow.json` 存在 | 含 `nodes`、`edges` |
| 2 | `flow.meta.json` 存在 | 含 `flowId`、`nodes` |
| 3 | 代码节点 uuid 在 meta 中 | 每个 `excel-python` 等有 `dir`+`codeFile` |
| 4 | meta 条目数 | meta 代码索引数 = flow.json 代码节点数 |
| 5 | 代码文件存在 | `节点/<名>/code.py` 或 `code.sql` 可读 |
| 6 | `node.info.json` | pull / repair 后应有（可选但推荐） |
| 7 | 配置已上平台 | 改配置后执行过 `push --canvas` 且终端有成功提示 |
| 8 | 代码已上平台 | 改 code 后执行过 `node push` |

---

## 常见症状 → 处理

| 症状 | 处理 |
|------|------|
| 设计器打不开代码 | `repair-meta` |
| `node push` skipped | `repair-meta` |
| 平台无 managed_file_id | `push --canvas` |
| flow-exec 只跑开始 | 平台图未更新 → `push --canvas` 后重试 |

详见 [流程本地文件规范](../flow/local-files-spec.md)。
