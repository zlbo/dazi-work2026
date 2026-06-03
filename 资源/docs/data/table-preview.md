# 数据表预览

**文档 ID**: `data/table-preview`

## 列出数据表

```bash
dazi data table list --space <space-id>
```

## 查看表结构

```bash
dazi data table schema <table-id> --space <space-id>
```

## 采样数据

```bash
dazi data table sample <table-id> --space <space-id> --rows 10
```

## 在扩展中预览

在侧栏「🗂 数据资源」→ 空间 → 数据表，点击表名打开预览 Webview：

- **Schema 标签页**：列名、类型、是否可空
- **预览标签页**：前 10 行数据

## 文件管理

```bash
# 列出平台文件
dazi data file list --space <space-id>

# 上传本地文件
dazi data file upload ./data.csv --space <space-id>

# 下载文件
dazi data file pull remote/path.csv --space <space-id>
```
