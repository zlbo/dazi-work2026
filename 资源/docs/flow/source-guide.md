# 数据源管理

**文档 ID**: `flow/source-guide`

## 列出数据源

```bash
dazi-flow source list
dazi-flow source list --space <space-id>
```

## 查看数据源中的表

```bash
dazi-flow source tables <source-id>

# 过滤 schema
dazi-flow source tables <source-id> --schema public
```

## 查看表结构

```bash
dazi-flow source table-structure <source-id> <table-name>
```

输出示例：
```
表: public.orders
列名                             类型                 可空   说明
────────────────────────────────────────────────────────────────
  id                             bigint               false  主键
  user_id                        bigint               false  用户ID
  amount                         decimal(10,2)        false  金额
  created_at                     timestamp            false  创建时间
```

## 保存表结构到工作区

```bash
dazi-flow source table-workspace <source-id> <table-name> --flow <flow-id>
```

表结构保存到 `flows/<flow-id>/data/<table-name>.schema.json`，可供 Cursor 读取作为上下文。
