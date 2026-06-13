<!-- dazi-onto-domain-backed -->
<!-- dazi-onto-scaffold -->
# 快速启动 · default

本文件为 **domain-backed** 本体实现（平台域已存在）。路径：`项目/潘达工程/本体/ontos/default/`

## 0. 任务模式（智能体 / TRAE 必读）

| 模式 | 何时使用 | 允许 | 禁止 |
| --- | --- | --- | --- |
| **待办扩展**（**默认**） | 平台域已有表/Cube/函数；以 gap 待办为主 | 读 `context/domain_inventory.md` + `plans/training/`；写 **最小补丁** | 无 gap 理由重写整域 init；复制其他 onto 全文 init |
| **对照实施** | 本地 plans 已定稿补充能力 | 对照 inventory 写 setup/functions 补丁 | 与 inventory 不一致的大改 |
| **独立规划** | 用户明确要求重新规划 | 在 `plans/` 撰写（仍须说明与平台差异） | 忽略 inventory 直接 init |

**默认路径**：读 `context/` → `plans/training/gap_*.md` → §5 补丁发布。**未确认模式时按「待办扩展」执行。**

## 1. 数据空间与本体域

| 字段 | 内容 |
| --- | --- |
| 数据空间 | 本体引擎测试 |
| 数据空间 ID | `space__onto_engine_test` |
| 本体域 code | `default` |
| 本体域名称 | 本体引擎测试 |
| 本体域 ID | `3dc87cac8ba94dad9d4b6b5460bf1494` |

- 域 ID **已绑定**（materialize 写入，无需 ensure）。
- 环境清单：**[`context/domain_inventory.md`](./context/domain_inventory.md)**
- materialize：2026-06-13T12:22:27.211Z

## 2. 当前环境（必读）

**先读** [`context/domain_inventory.md`](./context/domain_inventory.md)（表 / Cube / 对象 / 函数摘要）。

问数 gap 规划落盘：`plans/training/gap_*.md`（`dazi onto training gap pull`，Phase B）。

定稿前可对照 [本体规划指南](../../../../../资源/docs/onto/本体规划指南.md)，但以 **inventory + gap** 为实施真源。

## 3. 阶段门禁

进入 `setup/`、`functions/` 补丁前：

1. 已读 `context/domain_inventory.md`
2. 若有 open gap：已读对应 `plans/training/gap_*.md` 或用户确认无需 gap
3. 补丁范围 **≤ gap 描述**；禁止整域重建

## 4. 执行脚本前必读

- [脚本运行常见错误处理](../../../../../资源/docs/onto/脚本运行常见错误处理.md)
- 域成员：bulk 仍用 `category_mount` + `s.domain.apply_registry`；单函数 publish 加 `--mount-domain auto`

## 5. 发布与运维

```powershell
dazi onto script publish 项目/潘达工程/本体/ontos/default/functions/xxx_fn_patch.py --space space__onto_engine_test --register-function-id default.fn.<name> --mount-domain auto
dazi onto domain snapshot-pull --onto-dir 项目/潘达工程/本体/ontos/default
```

- CLI：`dazi onto domain show --domain-id 3dc87cac8ba94dad9d4b6b5460bf1494`
- 刷新快照：`dazi onto domain snapshot-pull --onto-dir 项目/潘达工程/本体/ontos/default`
