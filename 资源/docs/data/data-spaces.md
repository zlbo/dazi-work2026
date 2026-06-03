# 数据空间管理

**文档 ID**: `data/data-spaces`

## 列出数据空间

```bash
dazi data space list
```

## 创建数据空间

```bash
dazi data space create --name "财务数据" --category-id finance
```

## 刷新数据空间

```bash
dazi data space refresh <space-id>
```

## 扩展侧栏

在 VS Code 侧栏「🗂 数据资源」节点下，按空间分组展示：

- 数据表（Tables）
- 数据集（Cubes）
- 数据源（Sources）

点击数据表可打开预览 Webview，显示表结构和前 10 行数据。
