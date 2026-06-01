# 数据集（Cube）管理

**文档 ID**: `data/cube-guide`

## 什么是 Cube

Cube 是预聚合的数据集，基于数据表或视图构建，支持快速查询和分析。

## 列出 Cube

```bash
.\scripts\dazi.ps1 data cube list --space <space-id>
```

## 查看 Cube 详情

```bash
.\scripts\dazi.ps1 data cube info <cube-id> --space <space-id>
```

## 在扩展中使用

在侧栏「🗂 数据资源」→ 空间 → 数据集，点击 Cube 打开详情 Webview。
