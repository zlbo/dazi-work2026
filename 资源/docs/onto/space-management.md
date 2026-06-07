# 本体空间管理

**文档 ID**: `onto/space-management`

## 空间概念

本体空间（Space）是搭子平台的基础组织单位，每个空间包含：

- 函数定义（FunctionDef）
- 动作定义（ActionDef）
- 规则（Rule）
- 脚本（Script）

## 列出空间

```bash
dazi onto space list
```

## 初始化本地工作区

```bash
dazi onto space init --space-id <space-id>
```

本地目录结构（**历史/遗留布局**，由 CLI `space init` 生成）：

```
onto/<space-id>/
  editorial/
    functions/    ← 函数工作副本
    actions/      ← 动作工作副本
  functions/      ← 函数定义元数据
  actions/        ← 动作定义元数据
  rules/          ← 规则元数据
  scripts/        ← 脚本文件
  .dazi-space.json
```

> **推荐工作区结构（v3）**：日常开发与文档约定使用 **`项目/<业务名>/本体/ontos/<实现名>/`** 实现单元布局（`README.md` 为 `space_id` 权威来源，`plans/`、`setup/`、`functions/`、`快速启动_<实现名>.md`）。`dazi onto space init` 生成的 **`onto/<space-id>/`** 仅用于 CLI 拉取快照、同步脚本等**对照/迁移**场景，**不应**作为新建本体项目的主开发路径。详见 **[本体规划指南](./本体规划指南.md)**、**[本体脚本编写指南](./本体脚本编写指南.md)**。

## 拉取快照

将远端本体数据同步到本地：

```bash
dazi onto space snapshot --space-id <space-id>
```

快照保存到 `onto/<space-id>/snapshot.json`。
