# 从 v2 迁移到 v3

**文档 ID**: `guides/migrate-v2-v3`

## 快速迁移（3 步）

### 第 1 步：预览变更

```bash
dazi migrate workspace --dry-run
```

输出示例：

```
[计划]
  重命名: ontology/ → onto/
  重命名: runtime-apps/ → apps/
  创建: flows/
  创建: data/
  创建: docs/
  创建: prompts/
  创建: .dazi/
```

### 第 2 步：执行迁移

```bash
dazi migrate workspace
```

迁移前会自动备份到 `.dazi/backup/<timestamp>/`。

### 第 3 步：迁移认证

```bash
dazi auth migrate --dry-run  # 预览
dazi auth migrate            # 执行（从 ~/.dazi-app/auth.json 迁移）
```

## 配置迁移

旧版 `daziAgent.*` / `daziApp.*` 配置会在首次激活时自动提示迁移，也可手动执行：

```bash
dazi migrate config
```

## 回退

如果迁移出现问题，备份在 `.dazi/backup/<timestamp>/`，恢复方式：

```bash
cp -r .dazi/backup/<timestamp>/ontology ./ontology
```
