# Flow 快照管理

**文档 ID**: `flow/snapshot-guide`

## 快照概念

快照（Snapshot）是 Flow 图结构的本地副本，包含：
- 所有节点（Node）定义
- 节点间连接（Edge）
- 节点配置（Config）

## 拉取快照

```bash
dazi-flow snapshot pull --flow <flow-id>

# 指定输出目录
dazi-flow snapshot pull --flow <flow-id> --out ./my-snapshots/
```

## 推送图快照

将本地修改推送回平台：

```bash
# 预览变更
dazi-flow snapshot push-graph --flow <flow-id> --dry-run

# 执行推送
dazi-flow snapshot push-graph --flow <flow-id>
```

## 使用场景

| 场景 | 命令 |
|------|------|
| 备份当前 Flow 配置 | `snapshot pull` |
| 批量修改节点配置后同步 | `snapshot push-graph` |
| 在 Cursor 中查看 Flow 结构 | 打开 `flows/<id>/snapshot.json` |
| CI/CD 中恢复 Flow | `snapshot push-graph` |
