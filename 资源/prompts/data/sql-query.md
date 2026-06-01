# 提示词：SQL 查询生成

**提示词 ID**: `data/sql-query`  
**场景**: 根据表结构生成 SQL 查询

---

请根据以下表结构生成 SQL 查询（ClickHouse 方言）。

## 表结构

```
{{table_structures}}
```

## 查询需求

{{query_requirement}}

## ClickHouse 常用函数备忘

```sql
-- 时间函数
toDate(timestamp_col)
toStartOfMonth(date_col)
dateDiff('day', start_date, end_date)

-- 聚合函数
groupArray(col)          -- 转数组
anyLast(col)             -- 最后一个值
countIf(condition)       -- 条件计数
sumIf(col, condition)    -- 条件求和

-- 窗口函数
row_number() OVER (PARTITION BY col ORDER BY ts DESC)
```
