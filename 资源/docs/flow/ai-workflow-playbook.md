# 流程项目 AI 工作手册

**文档 ID**: `flow/ai-workflow-playbook`  
**适用**: Cursor / Trae / 任何 Agent 修改 `项目/<业务名>/流程/flows/<流程名>/`

> 完整文件规范见 [流程本地文件规范](./local-files-spec.md)。

---

## 1. 一分钟决策树

```text
要做什么？
├─ 新增代码节点 → node new（禁止手搓 uuid）
├─ 改 managed_file_id / output_variable_name / 连线 → project push --canvas
├─ 改 code.py / code.sql → node push --node <uuid>
├─ 目录 doctor 报错 → repair-meta，再 push --canvas / node push
└─ 运行前 → 先 push 成功，再 flow-exec / node-exec
```

---

## 2. 禁止清单

1. **禁止**只编辑 `flow.json` 而不更新 `flow.meta.json`
2. **禁止**伪造 `node_uuid`
3. **禁止**把 SQL/Python 正文写入 `flow.json`
4. **禁止**用 `project push`（无 `--canvas`）提交画布配置
5. **禁止**在本地画布节点多于平台时直接 `project pull`（覆盖本地）
6. **禁止**未 `push --canvas` 就 `flow-exec` 并声称配置已上线

---

## 3. 标准流程（改现有 excel-python）

```powershell
# 推荐绝对路径（禁止在 dazi-work 根 --dir .）
$flowDir = "D:\path\to\dazi-work\项目\<业务名>\流程\flows\<流程名>"

dazi flow project doctor --dir $flowDir
# 若不一致：
dazi flow project repair-meta --dir $flowDir

# 改 flow.json 配置后：
dazi flow project push --dir $flowDir --canvas

# 改 code.py 后：
dazi flow node push --node <node_uuid> --dir $flowDir

dazi flow run node-exec --node <node_uuid> --dir $flowDir
dazi flow run flow-exec --dir $flowDir --type debug
```

确认终端出现 **`✅ 画布已全量推送`**。

---

## 4. 提交前自检

- [ ] `doctor` 为 ✅
- [ ] 配置变更已 `push --canvas`
- [ ] 改 `code.*` 后已 **`node push`**（先于 `node-exec`）
- [ ] `node-exec` JSON `success: true`
- [ ] 有 `output_variable_name` 时已 **`variable pull`** 且 `变量/<名>.json` 合理
- [ ] `flow.json` 无代码正文
- [ ] 以上均满足后再声称完成（禁止仅凭 exit code、禁止未 push 就测代码）

---

## 5. 提示词

侧栏 **帮助 → 提示词**：`flow/flow-design`、`flow/run-fix-loop`（⭐）。
