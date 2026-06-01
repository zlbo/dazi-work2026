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
.\scripts\dazi.ps1 onto space list
```

## 初始化本地工作区

```bash
.\scripts\dazi.ps1 onto space init --space-id <space-id>
```

本地目录结构：
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

## 拉取快照

将远端本体数据同步到本地：

```bash
.\scripts\dazi.ps1 onto space snapshot --space-id <space-id>
```

快照保存到 `onto/<space-id>/snapshot.json`。
